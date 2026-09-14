# 100 Hz Average-64 CSV check — 2026-09-14

**Finding:** The existing stopped capture gives a **provisional sensitivity of approximately 0.78 V/A** when the paired analysis allows for CH1's phase discontinuity at 170.4 ms. A single stationary sine fit is unsuitable. Noise, unresolved CSV behavior, and unestablished repeatability prevent accepting this as a calibration.

The user reported CH1 stable at 480 mVpp after the Sample instruction, then rising from approximately 100 to 475 mVpp after selecting Average 64 and appearing stable. The user subsequently clarified that **the display was stable and acquisition was stopped before producing this CSV pair**, exactly as instructed. The 100 Hz setting was explicitly confirmed. The filenames include 2pp; a fresh generator amplitude measurement was not provided.

## Files and provenance

The archived CSV files retain the original uploaded bytes, including line endings.

| Channel | Original file | SHA-256 |
| --- | --- | --- |
| CH1 | [data_27_000_CH1_avg100Hz_2pp.csv](../../raw/2026-09-14/data_27_000_CH1_avg100Hz_2pp.csv) | `0232a79e041c727434beb9e28c0956ef6659507fa825931b9ee3c2426c97e805` |
| CH2 | [data_27_001_CH2_avg100Hz_2pp.csv](../../raw/2026-09-14/data_27_001_CH2_avg100Hz_2pp.csv) | `17e527fb7f1c2e3cf3a7571fde9f91a140c4fc79d04d012d806c4836c09706a7` |

Each file contains 10,000 consecutive samples, spaced 20 µs apart. The exported rate is 50,000 points/s; the first-to-last span is 0.19998 s. Time in this analysis starts at the first exported sample, not at an independently established trigger timestamp. Acquisition mode and STOP status come from the user's confirmation; those fields are absent from the CSV headers.

## Readout versus saved samples

| Quantity | CH1 | CH2 |
| --- | ---: | ---: |
| CSV header Vpp | 479.5 mV | 82.00 mV |
| Maximum minus minimum of exported samples | 488 mV | 236 mV |
| Smallest spacing between distinct exported voltage levels | 8 mV | 4 mV |
| Header voltage per ADC value | 0.5 mV | 0.25 mV |
| Mean of exported values | −7.9304 mV | 203.3836 mV |

These differences are recorded, not corrected. They do not establish which processing stage the CSV represents or prove a firmware defect. In particular, the CH2 mean in the file must not replace the previously reported physical OUT-to-GND reading of 0.498 V.

## The discontinuity

Between one-based sample indices **8520 and 8521**, CH1 changes from **−104 mV to +64 mV** in one exported interval: a **168 mV step**.

![Full CH1 export and detail of the 168 mV discontinuity](ch1-discontinuity.svg)

Plot voltages are the CSV's stored coordinates. The full-record panel shows every fourth point for clarity; the detail panel and calculations use every sample.

The following fits diagnose the record. Splitting at the jump does not repair the original evidence or turn either section into an accepted calibration result.

| CH1 interval | Independently fitted frequency | Fitted sine Vpp | Residual RMS |
| --- | ---: | ---: | ---: |
| Samples 1–8520 | 99.99895 Hz | 477.510 mV | 4.286 mV |
| Samples 8521–10000 | 100.01418 Hz | 476.617 mV | 4.321 mV |
| Whole record, single sine | 99.05844 Hz | 340.069 mV | 118.640 mV |

Both sections have amplitudes close to the settled screen reading. At a fixed 100 Hz, their fitted phases differ by approximately 186.4° (equivalently −173.6°). Their partial cancellation explains why a whole-record sine fit reports a much smaller amplitude. The whole-record fitted frequency near 99.06 Hz is not evidence that the generator was set incorrectly.

## What can be said about CH2

At a fixed 100 Hz:

| Interval used diagnostically | Fitted CH2 sine Vpp | CH2 residual RMS |
| --- | ---: | ---: |
| Samples 1–8520 | 5.332 mV | 21.917 mV |
| Samples 8521–10000 | 6.705 mV | 21.775 mV |
| Whole record | 3.541 mV | 21.949 mV |

The residual is much larger than the sine component. These figures depend on the chosen interval and have not been assigned calibration uncertainty. The user confirms both exports followed STOP. The paired model below assumes corresponding indices describe corresponding times; the export's internal mapping has not been independently verified, and no cross-channel phase calibration is claimed.

For scale, the settled CH1 readout of 475 mVpp through measured R8 = 67 Ω implies approximately 7.09 mApp. Nominal sensor sensitivity of 0.8 V/A predicts approximately **5.67 mVpp** at CH2. [Pololu #4048 specification](https://www.pololu.com/product/4048)

## Paired response from the existing stopped capture

**Purpose:** Estimate the repeating sensor response without treating the phase jump as a reduction in signal amplitude. Fit CH1's timing separately on each side of the jump, then compare CH2 against that reference using every paired sample.

For each section, fit CH1 at the confirmed 100 Hz. Let its fitted changing component be `u = a·sin(ωt) + b·cos(ωt)`, with `ω = 2π·100`. Also form `v = a·cos(ωt) − b·sin(ωt)`, the same reference advanced by 90°. This second component allows CH2 to have a phase shift; it does not force perfect alignment.

Fit all 10,000 CH2 samples to `CH2 = c_section + g·u + h·v`. The two sections have separate offsets, but share g and h. Because CH1 measures voltage across R8, sensitivity is `67 Ω × sqrt(g² + h²)`. No samples are discarded, moved, or changed.

| Paired-model quantity | Result |
| --- | ---: |
| Samples used | 10,000 |
| Fitted CH1 current swing, before / after jump | 7.127 / 7.113 mApp |
| Common CH2-to-CH1 amplitude ratio | 0.01157 V/V |
| Provisional sensitivity | **0.775 V/A**, reported as **approximately 0.78 V/A** |
| Corresponding fitted CH2 swing | Approximately 5.52 mVpp |
| CH2 residual RMS | 21.90 mV |
| Separate-section sensitivity estimates, before / after | 0.748 / 0.943 V/A |

The provisional result is near the nominal 0.8 V/A. It does **not** establish calibration accuracy: the residual is large, the shorter section contains only about three cycles, and repeatability and measurement uncertainty have not been established. The section estimates show how much a noisy single-record result can depend on the available interval. The common-response model also assumes corresponding times in the two exports and one linear response across the jump. Its fitted phase is a model parameter, not a calibrated sensor-delay measurement.

The cause of the discontinuity remains unknown. Possibilities include a real transient or behavior in acquisition, stored-record ordering, or export. The user's STOP confirmation removes the basis for requesting another export merely to stop acquisition first.

## Method and reproduction

[check_average_csv.py](check_average_csv.py) reads the unchanged raw files and writes [metrics.json](metrics.json) and the plot. It requires Python with NumPy, SciPy, and Matplotlib.

From the repository root:

```bash
python docs/evidence/analysis/2026-09-14/check_average_csv.py
```

The diagnostic sine model is `y(t) = c + a·sin(2πft) + b·cos(2πft)`. Linear least squares determines c, a, and b at each frequency; fitted Vpp is `2·sqrt(a²+b²)`. CH1's free frequency uses a 95–105 Hz grid search followed by bounded minimization around its best grid point. The paired response uses fixed 100 Hz and the section-specific reference described above. Residual RMS is computed from all samples in the stated interval.

The largest absolute CH1 sample step defines the two diagnostic intervals. No rows are removed, reordered, or overwritten. The CSV header ADC factor is not applied again: the voltage column already declares mV. Raw Vpp and fitted sine Vpp are kept distinct.

## Correction to the requested next step

The previous version requested another stable, stopped export. The user confirmed this was already how the supplied pair was produced. **That repeat request is withdrawn.** This revision analyzes the existing evidence; it records no new bench measurement and accepts no final calibration.

See the [acquisition lesson and bench sequence](../../../../study/oscilloscope-acquisition-and-triggering.md) for the settings and their purpose.
