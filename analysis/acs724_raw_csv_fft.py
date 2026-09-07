"""Reproducible analysis for DOS1102S ACS724 CSV exports.

Expected CSV format:
  metadata lines
  index,CH1_Voltage(mV)
  ... samples ...

The script removes the waveform mean, applies a Hamming window, and reports
single-sided RMS spectral amplitudes with coherent-gain correction.
"""
from pathlib import Path
import csv
import numpy as np

SENSITIVITY_V_PER_A = 0.74472


def load_dos1102s_csv(path: Path):
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    metadata = {}
    data_start = None
    for i, line in enumerate(lines):
        if line.strip() == "index,CH1_Voltage(mV)":
            data_start = i + 1
            break
        if ":," in line:
            key, value = line.split(":,", 1)
            metadata[key.strip()] = value.strip()
    if data_start is None:
        raise ValueError(f"No CH1 sample table found in {path}")
    values_mv = []
    for row in csv.reader(lines[data_start:]):
        if len(row) >= 2 and row[1].strip():
            values_mv.append(float(row[1]))
    dt_text = metadata.get("Time interval", "")
    if not dt_text.endswith("us"):
        raise ValueError(f"Unsupported/missing time interval: {dt_text!r}")
    dt_s = float(dt_text[:-2]) * 1e-6
    return metadata, np.asarray(values_mv, dtype=float), dt_s


def analyze(path: Path):
    metadata, y_mv, dt_s = load_dos1102s_csv(path)
    fs = 1.0 / dt_s
    n = len(y_mv)
    centered_mv = y_mv - np.mean(y_mv)
    sigma_mv = float(np.std(centered_mv, ddof=0))
    vpp_mv = float(np.ptp(y_mv))

    window = np.hamming(n)
    coherent_gain = np.mean(window)
    spectrum = np.fft.rfft(centered_mv * window)
    freq_hz = np.fft.rfftfreq(n, dt_s)
    peak_mv = 2.0 * np.abs(spectrum) / (n * coherent_gain)
    rms_mv = peak_mv / np.sqrt(2.0)
    if len(rms_mv):
        rms_mv[0] /= 2.0

    # Report the strongest non-DC component in the low-frequency motor region.
    band = (freq_hz >= 20.0) & (freq_hz <= 300.0)
    band_indices = np.flatnonzero(band)
    strongest = band_indices[np.argmax(rms_mv[band])]
    f_peak = float(freq_hz[strongest])
    a_peak_mv_rms = float(rms_mv[strongest])
    a_peak_ma_rms = a_peak_mv_rms / SENSITIVITY_V_PER_A

    return {
        "file": path.name,
        "samples": n,
        "fs_hz": fs,
        "duration_s": n / fs,
        "mean_mv": float(np.mean(y_mv)),
        "sigma_mv": sigma_mv,
        "vpp_mv": vpp_mv,
        "peak_hz_20_300": f_peak,
        "peak_mv_rms": a_peak_mv_rms,
        "peak_ma_rms": a_peak_ma_rms,
        "metadata": metadata,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    for file in args.files:
        result = analyze(file)
        print(
            f"{result['file']}: N={result['samples']}, "
            f"fs={result['fs_hz']:.1f} Hz, T={result['duration_s']:.3f} s, "
            f"mean={result['mean_mv']:.3f} mV, sigma={result['sigma_mv']:.3f} mV, "
            f"Vpp={result['vpp_mv']:.1f} mV, "
            f"peak={result['peak_hz_20_300']:.1f} Hz / "
            f"{result['peak_mv_rms']:.3f} mVrms / "
            f"{result['peak_ma_rms']:.3f} mArms"
        )
