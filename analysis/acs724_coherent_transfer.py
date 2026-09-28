"""Coherent transfer analysis for DOS1102S two-channel CSV exports.

Project use:
  CH1 = voltage across R8 current-reference resistor
  CH2 = ACS724 OUT

The script fits DC + sine + cosine at a commanded frequency, converts CH1 to
primary current, calculates the apparent transfer magnitude, and reports both
raw and one-sample-corrected CH2-CH1 phase.

The one-sample correction is not a generic oscilloscope assumption. It is
enabled explicitly because same-node controls in this project measured an
approximately one-stored-sample CH2 lag at both:
  1 kHz, dt = 40 us
  10 kHz, dt = 4 us

Use --no-one-sample-correction for datasets where that control does not apply.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np

RREF_OHM = 67.0


def parse_time_interval(text: str) -> float:
    text = text.strip()
    units = [
        ("ms", 1e-3),
        ("us", 1e-6),
        ("ns", 1e-9),
        ("s", 1.0),
    ]
    for suffix, scale in units:
        if text.lower().endswith(suffix):
            return float(text[: -len(suffix)]) * scale
    raise ValueError(f"Unsupported time interval: {text!r}")


def load_dos1102s_all(path: Path):
    lines = path.read_text(encoding="utf-8-sig").splitlines()

    metadata: dict[str, str] = {}
    header_index = None

    for i, line in enumerate(lines):
        if line.startswith("index,"):
            header_index = i
            break
        if ":," in line:
            key, value = line.split(":,", 1)
            metadata[key.strip()] = value.strip()

    if header_index is None:
        raise ValueError(f"No sample table found in {path}")

    header = next(csv.reader([lines[header_index]]))
    if "CH1_Voltage(mV)" not in header or "CH2_Voltage(mV)" not in header:
        raise ValueError(f"Expected CH1 and CH2 columns in {path}")

    ch1_index = header.index("CH1_Voltage(mV)")
    ch2_index = header.index("CH2_Voltage(mV)")

    ch1_mv = []
    ch2_mv = []

    for row in csv.reader(lines[header_index + 1 :]):
        if len(row) <= max(ch1_index, ch2_index):
            continue
        if not row[ch1_index].strip() or not row[ch2_index].strip():
            continue
        ch1_mv.append(float(row[ch1_index]))
        ch2_mv.append(float(row[ch2_index]))

    dt_field = metadata.get("Time interval")
    if not dt_field:
        raise ValueError(f"Missing Time interval metadata in {path}")

    dt_text = dt_field.split(",")[0].strip()
    dt_s = parse_time_interval(dt_text)

    return (
        metadata,
        np.asarray(ch1_mv, dtype=float) / 1000.0,
        np.asarray(ch2_mv, dtype=float) / 1000.0,
        dt_s,
    )


def fit_component(y_v: np.ndarray, dt_s: float, frequency_hz: float):
    n = len(y_v)
    t = np.arange(n, dtype=float) * dt_s

    omega_t = 2.0 * np.pi * frequency_hz * t
    x = np.column_stack(
        (
            np.ones(n),
            np.sin(omega_t),
            np.cos(omega_t),
        )
    )

    dc_v, a_v, b_v = np.linalg.lstsq(x, y_v, rcond=None)[0]
    fitted = x @ np.array([dc_v, a_v, b_v])
    residual = y_v - fitted

    vpk = math.hypot(a_v, b_v)
    vpp = 2.0 * vpk
    phase_deg = math.degrees(math.atan2(b_v, a_v))

    return {
        "dc_v": float(dc_v),
        "vpp_v": float(vpp),
        "phase_deg": float(phase_deg),
        "residual_rms_v": float(np.sqrt(np.mean(residual**2))),
        "raw_vpp_v": float(np.ptp(y_v)),
    }


def wrap_phase_deg(value: float) -> float:
    return (value + 180.0) % 360.0 - 180.0


def analyze_transfer(
    path: Path,
    frequency_hz: float,
    rref_ohm: float = RREF_OHM,
    one_sample_correction: bool = True,
):
    metadata, ch1_v, ch2_v, dt_s = load_dos1102s_all(path)

    if len(ch1_v) != len(ch2_v):
        raise ValueError("CH1 and CH2 sample counts differ")

    ch1 = fit_component(ch1_v, dt_s, frequency_hz)
    ch2 = fit_component(ch2_v, dt_s, frequency_hz)

    current_pp_a = ch1["vpp_v"] / rref_ohm
    h_mag_v_per_a = ch2["vpp_v"] / current_pp_a

    raw_phase_deg = wrap_phase_deg(ch2["phase_deg"] - ch1["phase_deg"])

    correction_deg = 0.0
    if one_sample_correction:
        correction_deg = 360.0 * frequency_hz * dt_s

    corrected_phase_deg = wrap_phase_deg(raw_phase_deg + correction_deg)

    n = len(ch1_v)
    fs_hz = 1.0 / dt_s

    return {
        "file": path.name,
        "frequency_hz": frequency_hz,
        "samples": n,
        "dt_s": dt_s,
        "fs_hz": fs_hz,
        "duration_s": n * dt_s,
        "samples_per_cycle": fs_hz / frequency_hz,
        "ch1_fit_vpp_v": ch1["vpp_v"],
        "current_fit_ipp_a": current_pp_a,
        "ch2_fit_vpp_v": ch2["vpp_v"],
        "h_mag_v_per_a": h_mag_v_per_a,
        "phase_raw_deg": raw_phase_deg,
        "phase_correction_deg": correction_deg,
        "phase_corrected_deg": corrected_phase_deg,
        "ch1_residual_rms_v": ch1["residual_rms_v"],
        "ch2_residual_rms_v": ch2["residual_rms_v"],
        "metadata": metadata,
    }


def format_result(result: dict) -> str:
    return (
        f"{result['file']}: "
        f"f={result['frequency_hz']:.1f} Hz, "
        f"N={result['samples']}, "
        f"dt={result['dt_s'] * 1e6:.3f} us, "
        f"fs={result['fs_hz'] / 1e3:.3f} kSa/s, "
        f"samples/cycle={result['samples_per_cycle']:.2f}, "
        f"Ipp={result['current_fit_ipp_a'] * 1e3:.4f} mA, "
        f"CH2={result['ch2_fit_vpp_v'] * 1e3:.4f} mVpp, "
        f"|H|={result['h_mag_v_per_a']:.4f} V/A, "
        f"phase_raw={result['phase_raw_deg']:.2f} deg, "
        f"phase_corrected={result['phase_corrected_deg']:.2f} deg, "
        f"CH2_residual={result['ch2_residual_rms_v'] * 1e3:.3f} mVrms"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("frequency_hz", type=float)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--rref", type=float, default=RREF_OHM)
    parser.add_argument(
        "--no-one-sample-correction",
        action="store_true",
        help="Report raw CH2-CH1 phase without the project-specific one-sample correction.",
    )
    args = parser.parse_args()

    results = []
    for file in args.files:
        result = analyze_transfer(
            file,
            frequency_hz=args.frequency_hz,
            rref_ohm=args.rref,
            one_sample_correction=not args.no_one_sample_correction,
        )
        results.append(result)
        print(format_result(result))

    if len(results) > 1:
        phasors = np.asarray(
            [
                r["h_mag_v_per_a"]
                * np.exp(1j * np.deg2rad(r["phase_corrected_deg"]))
                for r in results
            ]
        )
        mean_phasor = np.mean(phasors)
        magnitudes = np.asarray([r["h_mag_v_per_a"] for r in results])

        print(
            "aggregate: "
            f"complex |H|={abs(mean_phasor):.4f} V/A, "
            f"complex phase={np.angle(mean_phasor, deg=True):.2f} deg, "
            f"scalar mean |H|={np.mean(magnitudes):.4f} V/A, "
            f"sample SD={np.std(magnitudes, ddof=1):.4f} V/A"
        )


if __name__ == "__main__":
    main()
