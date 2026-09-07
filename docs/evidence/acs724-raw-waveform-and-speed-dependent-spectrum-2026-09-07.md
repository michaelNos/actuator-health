# ACS724 Raw Waveform Export and Speed-Dependent Spectrum — 2026-09-07

**Status:** Stage B/C bench evidence record  
**Sensor:** Pololu #4048 / ACS724LLCTR-05AU  
**Oscilloscope:** HANMATEK DOS1102S  
**Date:** 2026-09-07

## 1. Purpose

This record continues `acs724-motor-validation-and-noise-2026-09-07.md`. The earlier scope FFT work was exploratory and screenshot-based. This experiment establishes a numerical DOS1102S CSV export path and uses exported CH1 samples for reproducible OFF/ON and motor-speed spectral comparisons.

The calibrated low-current sensor sensitivity remains:

`S = 0.74472 V/A`

No Stage A baseline, ACS724 FILTER value, or AFE design decision is changed by this evidence.

## 2. USB export investigation

Native scope evidence was saved to USB in several forms before the CSV path was established:

- BMP screenshots preserve the displayed scope/FFT state.
- BIN files preserve native scope/Math data and metadata, but their proprietary numeric representation was not accepted for quantitative analysis without format validation.
- CSV waveform export was then found and used for CH1 numerical samples.

An initial CSV (`data_20_006.csv`) was captured while the scope's probe attenuation metadata was 10X although the physical probe was at 1X. Its voltage scale is therefore invalid for quantitative use. The physical probe and CH1 attenuation setting were subsequently both set to **1X**.

`data_20_007.csv` and `data_20_008.csv` confirmed corrected 1X numerical export, but the operator no longer remembered which file was motor OFF and which was motor ON. They are retained as raw exploratory evidence and are not used for state-dependent conclusions.

## 3. Validated CSV acquisition format

For the controlled captures used below, the DOS1102S CSV contains:

- source: CH1;
- probe attenuation: 1X;
- sample count: **10,000**;
- sample interval: **100 us**;
- sample rate: **10 kS/s**;
- record duration: **1.000 s**.

Thus the FFT bin spacing for a direct 1 s transform is **1 Hz**.

The exported waveform values are centered close to zero in these captures and are therefore treated as AC/ripple data. They are not used to infer the motor's DC current from the CSV mean. DC current remains supported by the PSU indication and the earlier DC-coupled ACS724 calibration/validation.

## 4. Reproducible analysis method

`analysis/acs724_raw_csv_fft.py` implements the analysis used for this record:

1. parse the DOS1102S CH1 CSV;
2. remove the sample mean;
3. calculate population standard deviation and peak-to-peak;
4. apply a **Hamming** window;
5. compute a single-sided FFT;
6. correct spectral amplitude for the Hamming coherent gain;
7. express sinusoidal spectral amplitude as RMS;
8. inspect the 20–300 Hz motor region;
9. convert spectral voltage amplitude to equivalent current using `S = 0.74472 V/A`.

The spectral current conversion is:

`I_rms = V_rms / S`

The resulting peak amplitude is an equivalent sensor-current component under the measured low-current calibration. It is not yet a production diagnostic threshold.

## 5. First controlled OFF/ON pair

Files:

- `data_20_009off.csv` — motor OFF
- `data_20_010on.csv` — motor ON

Results:

| State | sigma_V | Vpp | strongest 20–300 Hz component |
|---|---:|---:|---:|
| OFF | 25.282 mV | 256 mV | no corresponding strong ~83 Hz line; strongest unrelated bin ~229 Hz at 1.160 mVrms |
| ON | 26.303 mV | 296 mV | **83 Hz, 5.302 mVrms** |

At 83 Hz, the ON spectral amplitude corresponds to approximately:

`5.302 mV / 0.74472 V/A = 7.12 mArms`

The total broadband standard deviation changed only modestly, while a localized low-frequency component became visible in the ON spectrum.

## 6. OFF/ON repeatability sequence

A second controlled sequence was captured without intentionally changing scope settings:

- `data_20_011off.csv`
- `data_20_012on.csv`
- `data_20_013off.csv`
- `data_20_014on.csv`

Results:

| File | State | sigma_V | Vpp | strongest 20–300 Hz component |
|---|---|---:|---:|---:|
| 011 | OFF | 25.091 mV | 228 mV | 164 Hz, 1.328 mVrms |
| 012 | ON | 26.038 mV | 244 mV | **80 Hz, 4.314 mVrms** |
| 013 | OFF | 25.556 mV | 244 mV | 257 Hz, 1.167 mVrms |
| 014 | ON | 27.457 mV | 592 mV | **80 Hz, 3.750 mVrms** |

The ~80 Hz component appeared in both ON captures and was not comparably present in either adjacent OFF capture.

Equivalent current amplitudes for the two ON peaks are approximately:

- 012: **5.79 mArms**;
- 014: **5.03 mArms**.

Capture 014 also contains a large isolated excursion, producing 592 mV Vpp. This reinforces that Vpp is highly sensitive to rare extrema and should not be used alone as the primary noise metric.

### Result

The OFF→ON→OFF→ON sequence provides repeatability evidence that the ~80 Hz component is associated with motor operation under the tested bench conditions.

It does **not** yet identify the physical mechanism. Possible mechanisms include rotational, brush/commutator, torque-ripple, or other motor/load periodicity. No mechanism is accepted without further evidence.

## 7. Motor-voltage / speed-dependence experiment

The next experiment tested whether the motor-related spectral component moves with motor operating speed. The motor was run unloaded/lightly loaded at three supply voltages. The PSU observations were:

| Motor supply | PSU current | PSU power |
|---:|---:|---:|
| 4.0 V | 34 mA | 0.135 W |
| 5.0 V | 35 mA | 0.175 W |
| 6.0 V | 36 mA | 0.216 W |

The small displayed power discrepancy at 4 V (`4.0 V × 34 mA = 0.136 W` versus displayed 0.135 W) is retained as the raw PSU observation and is consistent with display rounding/resolution; it is not silently corrected.

Raw waveform files:

- `data_20_015-4v.csv`
- `data_20_016-5v.csv`
- `data_20_017-6v.csv`

Analysis:

| Supply | sigma_V | Vpp | dominant motor-related frequency | spectral amplitude | equivalent current amplitude |
|---:|---:|---:|---:|---:|---:|
| 4 V | 25.346 mV | 252 mV | **81 Hz** | **3.921 mVrms** | **5.27 mArms** |
| 5 V | 27.563 mV | 592 mV | **108 Hz** | **5.844 mVrms** | **7.85 mArms** |
| 6 V | 28.455 mV | 592 mV | **134 Hz** | **8.053 mVrms** | **10.81 mArms** |

At 6 V a smaller component near **67 Hz** (~2.04 mVrms) is also present. Because 67 Hz is approximately half of 134 Hz, it is noteworthy but its physical origin is not assigned.

### Result

The dominant low-frequency component moves substantially with motor supply/operating speed:

`4 V -> 81 Hz`

`5 V -> 108 Hz`

`6 V -> 134 Hz`

This behavior strongly supports the conclusion that the detected component is motor-operation-dependent rather than a fixed 50 Hz mains component or a stationary bench tone.

The PSU current changes only slightly (34→36 mA) while the spectral frequency changes strongly. For the lightly loaded DC motor this is consistent with increased applied voltage primarily increasing motor speed/back-EMF rather than causing a proportional increase in steady current.

## 8. Waveform DC-level observation

During manual operation, the operator observed the displayed ACS724 waveform jump upward when the motor was switched on. This is qualitatively consistent with the ACS724 transfer:

`VOUT = V0 + S*I`

and with the earlier validated ~35 mA DC motor current. At 35 mA the calibrated transfer predicts a DC shift of approximately:

`0.74472 V/A × 0.035 A = 26.1 mV`.

The present AC-centered CSV files are not used to quantify that DC shift. A future explicitly DC-coupled raw capture is required if the shift is to be quantified from exported waveform samples.

## 9. Relationship to the earlier exploratory FFT conclusion

The earlier evidence record correctly stated that screenshot-based exploratory FFT work did not resolve an obvious repeatable motor spectral line and that this did **not** prove absence of motor spectral content.

The new raw CSV analysis supersedes that exploratory limitation for the tested low-frequency condition: a repeatable motor-associated component is now numerically resolved, and its frequency moves from ~81 to 108 to 134 Hz as motor supply voltage is increased from 4 to 5 to 6 V.

This is a new measurement result, not a contradiction of the earlier limited screenshot conclusion.

## 10. Evidence retained and validity classification

All original instrument exports are to be preserved unchanged before processing.

Validity classification:

- BMP files: native visual evidence of scope/FFT display state.
- BIN files: native instrument evidence; retained, but not used for quantitative amplitude conclusions because the proprietary numeric representation has not been validated.
- `data_20_006.csv`: raw export retained; **invalid for voltage-amplitude conclusions** due 10X scope metadata vs 1X physical probe mismatch.
- `data_20_007.csv`, `data_20_008.csv`: corrected 1X exports retained; **state labels unknown**, so excluded from OFF/ON conclusions.
- `009off` through `014on`: valid labeled 1X OFF/ON evidence for the present bench experiment.
- `015-4v` through `017-6v`: valid labeled 1X motor-ON voltage/speed-dependence evidence for the present bench experiment.

## 11. Engineering conclusions

1. DOS1102S raw CH1 CSV export has been demonstrated with known sample interval, sample count, and probe scaling.
2. Controlled 1X captures contain 10,000 samples at 10 kS/s for 1.000 s.
3. Broadband waveform standard deviation remains large (~25–28 mV), and much of it exists with the motor OFF.
4. Despite the broadband background, FFT analysis resolves a localized component around 80–83 Hz when the motor runs near the original 4 V operating point.
5. The OFF→ON→OFF→ON test shows that this component follows motor state repeatably.
6. Raising motor voltage from 4 to 5 to 6 V moves the dominant component approximately 81→108→134 Hz.
7. The frequency movement is strong evidence that the component is related to motor operation/speed, but the exact physical mechanism has not yet been established.
8. The result demonstrates why frequency-domain features can reveal motor behavior even when total RMS/noise changes only modestly.
9. No health/fault threshold, motor-speed calibration, or fault-diagnostic claim is accepted from this experiment alone.
10. No filtering or Stage A architecture decision is changed by this result.

## 12. Next engineering actions

1. Preserve all original BMP/BIN/CSV exports and the reproducible analysis script.
2. Repeat selected operating points later to quantify frequency/amplitude variability and confidence bounds.
3. If motor RPM can be measured independently, compare the spectral component and harmonics with shaft/commutator frequency to identify its physical origin.
4. Continue controlled measurement-chain noise characterization, including same-ground floor and the planned sensor-supply comparison under identical acquisition settings.
5. Proceed toward the designed AFE/anti-alias implementation while preserving the formal DC–10 kHz diagnostic band.
6. Later repeat motor spectral measurements through the implemented acquisition chain and compare with the oscilloscope reference.

**Accepted present conclusion:** the ACS724 bench chain has reproducibly detected a motor-operation-dependent low-frequency current feature whose dominant frequency increases with motor supply/operating speed. Its diagnostic meaning remains to be established.
