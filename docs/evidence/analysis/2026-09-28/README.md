# 2026-09-28 ACS724 post-fix dynamic-analysis manifest

This directory entry documents the CSV set used by the post-fix dynamic-characterization report.

Primary report:

- [ACS724 post-fix dynamic characterization and AFE handoff](../../acs724-postfix-dynamic-characterization-and-afe-handoff-2026-09-28.md)

Reproducible analysis helper:

- [`analysis/acs724_coherent_transfer.py`](../../../../analysis/acs724_coherent_transfer.py)

## Analysis convention

At commanded frequency `f`, each channel is fitted as:

`v(t) = VDC + A sin(2πft) + B cos(2πft)`

Then:

`Vpp = 2 sqrt(A²+B²)`

`phase = atan2(B,A)`

For current-on transfer captures:

`Ipp = VCH1,pp / 67 Ω`

`|H| = VCH2,pp / Ipp`

Raw phase:

`φraw = φCH2 - φCH1`

For the acquisition modes validated by same-node controls, corrected phase advances CH2 by one stored sample:

`φcorrected = φraw + 360° f Δt`

wrapped to the normal ±180° range.

This correction is evidence-based for the tested modes; it is not a universal oscilloscope rule.

## Dataset manifest

### Corrected 5 kHz current-on set

- `data_39_000-5kHz-4p7nF-2msdiv-current-ON-1.csv`
- `data_39_001-5kHz-4p7nF-2msdiv-current-ON-2.csv`
- `data_39_002-5kHz-4p7nF-2msdiv-current-ON-3.csv`
- `data_39_003-5kHz-4p7nF-2msdiv-current-ON-4..csv`
- `data_39_004-5kHz-4p7nF-2msdiv-current-ON-5.csv`

Acquisition: 10K, Δt = 4 µs, 250 kSa/s, 40 ms record, 50 samples/cycle.

### Corrected 1 kHz ten-run set

- `data_39_005-1kHz-4p7nF-20msdiv-current-ON-postfix-1.csv`
- `data_39_006-1kHz-4p7nF-20msdiv-current-ON-postfix-2.csv`
- `data_39_007-1kHz-4p7nF-20msdiv-current-ON-postfix-3.csv`
- `data_39_008-1kHz-4p7nF-20msdiv-current-ON-postfix-4.csv`
- `data_39_009-1kHz-4p7nF-20msdiv-current-ON-postfix-5.csv`
- `data_39_010-1kHz-4p7nF-20msdiv-current-ON-postfix-6.csv`
- `data_39_011-1kHz-4p7nF-20msdiv-current-ON-postfix-7.csv`
- `data_39_012-1kHz-4p7nF-20msdiv-current-ON-postfix-8.csv`
- `data_39_013-1kHz-4p7nF-20msdiv-current-ON-postfix-9.csv`
- `data_39_014-1kHz-4p7nF-20msdiv-current-ON-postfix-10.csv`

Acquisition: 10K, Δt = 40 µs, 25 kSa/s, 400 ms record, 25 samples/cycle.

### Corrected 10 kHz ten-run set

- `data_39_015-10kHz-4p7nF-2msdiv-current-ON-postfix-1.csv`
- `data_39_016-10kHz-4p7nF-2msdiv-current-ON-postfix-2.csv`
- `data_39_017-10kHz-4p7nF-2msdiv-current-ON-postfix-3.csv`
- `data_39_018-10kHz-4p7nF-2msdiv-current-ON-postfix-4.csv`
- `data_39_019-10kHz-4p7nF-2msdiv-current-ON-postfix-5.csv`
- `data_39_020-10kHz-4p7nF-2msdiv-current-ON-postfix-6.csv`
- `data_39_021-10kHz-4p7nF-2msdiv-current-ON-postfix-7.csv`
- `data_39_022-10kHz-4p7nF-2msdiv-current-ON-postfix-8.csv`
- `data_39_023-10kHz-4p7nF-2msdiv-current-ON-postfix-9.csv`
- `data_39_024-10kHz-4p7nF-2msdiv-current-ON-postfix-10.csv`

Acquisition: 10K, Δt = 4 µs, 250 kSa/s, 40 ms record, 25 samples/cycle.

### Same-node timing controls

- `data_39_025-10kHz-same-node-R8-timing-control.csv`
- `data_39_026-1kHz-same-node-R8-timing-control-postfix.csv`

These establish the approximately one-stored-sample CH2 lag.

### Open-primary feedthrough controls

- `data_39_027-10kHz-open-primary-postfix-feedthrough-1.csv` — filename says 10 kHz, but actual CH1 stimulus is 1 kHz.
- `data_39_028-10kHz-open-primary-postfix-feedthrough-1.csv` — actual dominant CH1 component is 10 kHz even though the scope header reports approximately 5 kHz.
- `data_39_029-5kHz-open-primary-postfix-feedthrough-1.csv` — 5 kHz.

These controls are not transfer measurements because CH1 is on MCP6022 pin 1 rather than across R8.

### 7.5 kHz ten-run set

- `data_39_037-7p5kHz-4p7nF-2msdiv-current-ON-postfix-1.csv`
- `data_39_038-7p5kHz-4p7nF-2msdiv-current-ON-postfix-2.csv`
- `data_39_039-7p5kHz-4p7nF-2msdiv-current-ON-postfix-3.csv`
- `data_39_040-7p5kHz-4p7nF-2msdiv-current-ON-postfix-4.csv`
- `data_39_041-7p5kHz-4p7nF-2msdiv-current-ON-postfix-5.csv`
- `data_39_042-7p5kHz-4p7nF-2msdiv-current-ON-postfix-6.csv`
- `data_39_043-7p5kHz-4p7nF-2msdiv-current-ON-postfix-7.csv`
- `data_39_044-7p5kHz-4p7nF-2msdiv-current-ON-postfix-8.csv`
- `data_39_045-7p5kHz-4p7nF-2msdiv-current-ON-postfix-9.csv`
- `data_39_046-7p5kHz-4p7nF-2msdiv-current-ON-postfix-10.csv`

Acquisition: 10K, Δt = 4 µs, 250 kSa/s, 40 ms record, about 33.3 samples/cycle.

### Interleaved-frequency control

- A1: `data_39_048-5kHz-interleaved-postfix-A1.csv`
- A2: `data_39_049-7p5kHz-interleaved-postfix-A2.csv`
- A3: `data_39_050-10kHz-interleaved-postfix-A3.csv`
- A4: `data_39_051-5kHz-interleaved-postfix-A4.csv`
- A5: `data_39_052-7p5kHz-interleaved-postfix-A5.csv`
- A6: `data_39_053-10kHz-interleaved-postfix-A6.csv`

The sequence was deliberately interleaved to separate frequency dependence from simple elapsed-time/warm-up drift.

## Numbering note

No conclusion is drawn from absent sequence numbers such as 030–036 or 047. They are not part of this accepted dataset unless the corresponding raw files are later supplied and explicitly reviewed.

## Aggregate values used in the report

| Set | Complex-average magnitude | Complex-average corrected phase | Mean CH2 residual RMS |
|---|---:|---:|---:|
| 1 kHz, 10 runs | 0.8857 V/A | -6.51° | 13.166 mV |
| 5 kHz, 5 runs | 0.8708 V/A | -23.32° | 14.805 mV |
| 7.5 kHz, 10 runs | 0.7352 V/A | -36.46° | 14.408 mV |
| 10 kHz, 10 runs | 0.8032 V/A | -50.29° | 14.913 mV |

These aggregates are descriptive. They are not frozen calibration constants because the individual CH2 complex estimates remain too variable.

## Preservation rule

The raw DOS1102S exports remain primary evidence and must not be silently edited to “repair” headers, frequency labels, discontinuities, or phase alignment. Corrections and interpretations belong in analysis metadata, scripts, or derived reports.
