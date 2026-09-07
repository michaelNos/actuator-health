# Actuator Health Monitoring System

Engineering development repository for a laboratory-scale actuator condition-monitoring system based initially on current measurement and waveform analysis of a low-voltage DC actuator.

Rev-1 is developed **design-first**: the product is specified and baselined at system and subsystem level before physical implementation begins. Implementation and verification then follow the approved engineering documentation rather than completing the design ad hoc on the bench.

## Current project status

The Rev-1 Stage A architecture, subsystem designs, verification plan, and implementation handoff are frozen. **Stage B implementation and bench validation are now in progress.**

Completed Stage B work includes:

- initial DC motor and bench-supply characterization;
- ACS724 current-sensor bring-up;
- low-current DC calibration and linearity verification;
- steady-state motor-current validation;
- oscilloscope measurement-path troubleshooting and controlled noise investigation;
- HANMATEK DOS1102S USB export workflow using BMP, BIN, and CSV;
- reproducible raw-waveform analysis from exported CSV data;
- controlled OFF/ON spectral comparison and repeatability testing;
- first speed-dependent motor-current spectral observation.

The present low-current bench calibration is:

```text
VOUT = 0.46910 + 0.74472 * I
I    = (VOUT - 0.46910) / 0.74472
```

where `VOUT` is in volts and `I` is in amperes.

At the validated 4 V operating point, the calibrated ACS724 reproduced approximately **34.8 mA** while the PSU indicated **35 mA**. This is strong bench agreement, but not a formal accuracy certification because the PSU display is not an independently calibrated current reference.

## Latest dynamic-measurement result

Controlled 1-second CH1 CSV captures were acquired at **10 kS/s** with matched oscilloscope settings. Repeated OFF/ON testing showed a low-frequency component that appears with motor operation and is not comparably present in adjacent OFF captures.

A follow-up operating-point test showed the dominant motor-related component moving with motor supply voltage / speed:

| Motor supply | PSU current | PSU power | Dominant component |
|---:|---:|---:|---:|
| 4.0 V | 34 mA | 0.135 W | ~81 Hz |
| 5.0 V | 35 mA | 0.175 W | ~108 Hz |
| 6.0 V | 36 mA | 0.216 W | ~134 Hz |

This is strong evidence that the feature is associated with the running motor rather than fixed bench interference. Its exact physical mechanism has **not** yet been assigned, and it is **not** accepted as a health or fault signature.

The broadband ACS724 output background remains much larger than the localized motor-related spectral component, so measurement-chain noise characterization remains an active Stage B task.

## Immediate next engineering work

The next controlled verification step is a **same-ground noise-floor capture** using the same oscilloscope acquisition settings as the valid ACS724 CSV measurements. This will quantify how much of the approximately 25 mV RMS-type background originates in the measurement setup itself.

The planned sensor-supply comparison then follows:

```text
bench 5 V -> Arduino 5 V -> bench 5 V
```

with the sensor, probe, grounding, and acquisition configuration held fixed as far as practical.

Only after the dominant background-noise contributors are understood will the project proceed to the designed analog-front-end / anti-alias implementation and full dynamic verification.

The formal Rev-1 diagnostic band remains **DC-10 kHz**. The current 10 kS/s scope CSV captures are suitable for the present low-frequency investigation only; they do not satisfy final full-band verification.

## Project documentation

The `docs/` directory is the authoritative engineering record. The `study/` directory contains supporting learning material, and `analysis/` contains reproducible analysis code.

Key Stage B records currently include:

- [Stage B Implementation Log](docs/15-stage-b-implementation-log.md)
- [ACS724 DC Calibration](docs/16-acs724-dc-calibration.md)
- [ACS724 Motor Validation and Noise Exploration](docs/evidence/acs724-motor-validation-and-noise-2026-09-07.md)
- [ACS724 Raw Waveform Export and Speed-Dependent Spectrum](docs/evidence/acs724-raw-waveform-and-speed-spectrum-2026-09-07.md)
- [`analysis/acs724_raw_csv_fft.py`](analysis/acs724_raw_csv_fft.py) for reproducible DOS1102S CSV analysis

Raw instrument exports are preserved under the relevant `docs/evidence/raw/` folders. Original evidence should remain unchanged; analysis must not silently alter source files.

See the [documentation index](docs/README.md) for the authoritative documentation convention and the complete Rev-1 record.

## Measurement hardware currently in use

- **Current sensor:** Pololu #4048 / ACS724LLCTR-05AU, unidirectional 0-5 A
- **Controller:** Arduino UNO R4 WiFi
- **Oscilloscope:** HANMATEK DOS1102S, 110 MHz, integrated AFG
- **Bench PSU:** Jesverty SPS-3010V
- **Multimeter:** VC830L
- **Test actuator:** low-voltage brushed DC motor used for Stage B bench validation

The stock ACS724 carrier includes a **1 nF FILTER capacitor**, corresponding to approximately **90 kHz** sensor bandwidth. No additional ACS724 FILTER capacitance has been accepted for Rev-1 at this stage.

## Development workflow

Engineering work is controlled through documentation, explicit decisions, measured evidence, and pull requests.

One engineering phase or controlled change is developed on one branch and one pull request. Only explicitly approved engineering decisions are baselined. Values that legitimately depend on hardware, calibration, or measurements remain `TBD` until evidence exists rather than being invented.

The project owner performs the final manual merge.

## Project objective

The goal is not only to measure motor current. The final system is intended to acquire trustworthy actuator-current data, extract meaningful features, detect abnormal behavior, propagate measurement validity, and support repeatable health-monitoring decisions with a documented verification trail.

## Safety scope

Rev-1 is a low-voltage laboratory prototype. Hobby development hardware, breadboards, the Pololu ACS724 carrier, and ordinary oscilloscope probes are not to be connected directly to industrial 400 V three-phase circuits. Future industrial scaling requires appropriately rated isolated sensing and industrial installation practices.
