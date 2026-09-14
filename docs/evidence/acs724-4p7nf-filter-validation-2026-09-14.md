# ACS724 4.7 nF external FILTER validation — 2026-09-14

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — ACS724 dynamic/FILTER validation  
**Status:** Experimental 4.7 nF FILTER candidate demonstrated repeatable broadband-noise reduction at 1 kHz; 10 kHz transfer magnitude is not accepted because coherent feedthrough was demonstrated with zero primary current.

## 1. Purpose

This record documents the first physical validation of the external `4.7 nF` ACS724 FILTER capacitor candidate after the schematic was updated and merged.

The experiment asks two separate questions:

1. Does the external FILTER capacitor reduce unwanted broadband variation on ACS724 VIOUT?
2. Can the temporary MCP6022/ACS724 fixture still provide a trustworthy current-to-voltage transfer measurement across the intended diagnostic band?

The second question became critical at 10 kHz, where an open-primary control demonstrated a coherent output component even when no primary current flowed through the ACS724.

No result in this record freezes `4.7 nF` as the final product FILTER value.

---

## 2. Configuration

### 2.1 FILTER modification

The Pololu #4048 carrier contains the stock approximately `1 nF` FILTER capacitor.

The Stage-B experimental change adds:

`ACS724 FILTER -> 4.7 nF -> GND`

Therefore the approximate total FILTER capacitance used for first-order prediction is:

`CTOTAL ~= 1.0 nF + 4.7 nF = 5.7 nF`.

Using the project approximation `RFILTER ~= 1.8 kOhm`:

`fc ~= 1 / (2*pi*1.8 kOhm*5.7 nF) ~= 15.5 kHz`.

This is a prediction used to guide the experiment, not a measured pole frequency.

### 2.2 Primary-current reference

The current-on path is:

`MCP6022 pin 1 -> 220 Ohm -> ACS724 IP+ -> ACS724 IP- -> R8 -> GND`

For the measurements in this record the current-reference resistor is the currently measured:

`R8 = 67 Ohm`.

Formal current-on scope convention:

- `CH1 = voltage across R8`;
- `CH2 = ACS724 VIOUT`;
- `Ipp = VCH1,pp / 67 Ohm`.

For the open-primary feedthrough control, the connection from the 220-Ohm resistor to ACS724 `IP+` was opened and CH1 was moved to MCP6022 pin 1. CH2 remained on ACS724 VIOUT.

### 2.3 Analysis method

The commanded frequency is extracted by coherent least-squares fitting:

`v(t) = V0 + A*sin(2*pi*f*t) + B*cos(2*pi*f*t)`.

Coherent peak-to-peak amplitude is:

`Vpp,f = 2*sqrt(A^2 + B^2)`.

Residual RMS is calculated after removal of the fitted DC and commanded-frequency component. It is used here as a practical measure of the remaining broadband/non-coherent content.

Raw oscilloscope `PK-PK` values are not used as the sensor-transfer metric.

---

## 3. Valid 1 kHz measurements before adding 4.7 nF

Two valid Sample-mode 1 kHz captures established the immediate pre-filter comparison state. Both used 10,000 samples at `dt = 2 us`, therefore `fs = 500 kSa/s` and 500 samples/cycle.

### Capture 006 / 007

- CH1 coherent 1 kHz: `472.56 mVpp`;
- CH1 residual RMS: `4.11 mV`;
- inferred current: `7.053 mApp`;
- CH2 coherent 1 kHz: `4.383 mVpp`;
- CH2 residual RMS: `26.6 mV`;
- apparent gain: `0.621 V/A`.

### Repeat 008 / 009

- CH1 coherent 1 kHz: `472.25 mVpp`;
- CH1 residual RMS: `4.11 mV`;
- inferred current: `7.048 mApp`;
- CH2 coherent 1 kHz: `3.845 mVpp`;
- CH2 residual RMS: `25.2 mV`;
- apparent gain: `0.545 V/A`.

Interpretation before the FILTER change:

- the reference-current generation/acquisition was highly repeatable;
- the small CH2 coherent component varied materially and remained buried in approximately 25-27 mV RMS residual content;
- no 1 kHz sensitivity was accepted.

---

## 4. 1 kHz measurements with 4.7 nF external FILTER capacitor

### Capture 012 / 013

- CH1 coherent: `466.1 mVpp`;
- CH1 residual RMS: `4.45 mV`;
- inferred current: `6.96 mApp`;
- CH2 coherent: `6.13 mVpp`;
- CH2 residual RMS: `15.5 mV`;
- apparent gain: approximately `0.88 V/A`.

### Repeat 014 / 015

- CH1 coherent: `464.87 mVpp`;
- CH1 residual RMS: `4.31 mV`;
- inferred current: `6.94 mApp`;
- CH2 coherent: `6.35 mVpp`;
- CH2 residual RMS: `16.29 mV`;
- apparent gain: approximately `0.915 V/A`.

### 1 kHz interpretation

The CH2 residual RMS changed from approximately `25-27 mV` before the external capacitor to approximately `15.5-16.3 mV` with the capacitor installed.

This corresponds to roughly a 38-42% reduction relative to the two immediate valid unfiltered 1 kHz captures.

The reduction reproduced in an independent capture. Therefore the following observation is accepted:

**The 4.7 nF external FILTER capacitor materially and repeatably reduced broadband/non-coherent VIOUT variation in the 1 kHz test configuration while a coherent 1 kHz component remained measurable.**

The apparent 1 kHz gains are not promoted to an accepted sensor sensitivity or transfer point by this result alone.

---

## 5. 100 Hz measurements with 4.7 nF

### Capture 016 / 017

- CH1 coherent: `460.54 mVpp`;
- CH1 residual RMS: `4.12 mV`;
- inferred current: `6.874 mApp`;
- CH2 coherent: `4.474 mVpp`;
- CH2 residual RMS: `10.95 mV`;
- apparent gain: `0.651 V/A`.

This first capture did not reproduce the historical accepted low-frequency magnitude and was not treated as evidence of FILTER attenuation.

### Repeat 018 / 019

- CH1 coherent: `469.17 mVpp`;
- CH1 residual RMS: `4.63 mV`;
- inferred current: `7.002 mApp`;
- CH2 coherent: `6.427 mVpp`;
- CH2 residual RMS: `11.18 mV`;
- apparent gain: `0.918 V/A`.

The repeat is reasonably close to the historical practical unfiltered 100 Hz baseline `0.8792 V/A`.

### 100 Hz interpretation

The two filtered 100 Hz coherent CH2 magnitudes did not repeat closely enough to establish a new filtered 100 Hz baseline from this pair alone.

The data do **not** support a claim that the 4.7 nF capacitor attenuates 100 Hz. Such attenuation would also be inconsistent with the first-order prediction for an approximately 15.5 kHz pole.

The residual RMS was repeatable at approximately 11 mV in these two captures, but the coherent amplitude was not.

---

## 6. 10 kHz acquisition and current-on measurements

### 6.1 Acquisition clarification

The valid 10 kHz records use:

- `dt = 0.20000 us`;
- `fs = 5 MSa/s`;
- 500 samples per 10 kHz cycle.

An earlier interpretation incorrectly read `0.20000 us` as `200 us`. The valid 10 kHz files must therefore **not** be discarded for sampling-rate reasons.

### 6.2 Current-on capture 024 / 025

- CH1 coherent: `471.19 mVpp`;
- CH1 residual RMS: `4.09 mV`;
- inferred current: `7.033 mApp`;
- CH2 coherent 10 kHz: `9.04 mVpp`;
- CH2 residual RMS: `18.37 mV`;
- apparent gain: `1.286 V/A`.

### 6.3 Current-on repeat 026 / 027

- CH1 coherent: `475.89 mVpp`;
- CH1 residual RMS: `3.96 mV`;
- inferred current: `7.103 mApp`;
- CH2 coherent 10 kHz: `10.25 mVpp`;
- CH2 residual RMS: `21.44 mV`;
- apparent gain: `1.443 V/A`.

### 6.4 Current-on interpretation

CH1 repeated closely, showing that the primary-current excitation and acquisition remained stable.

The apparent CH2/current gains of `1.286 V/A` and `1.443 V/A` are not physically credible as a simple low-pass response relative to the established low-frequency behavior. They are therefore **not accepted as ACS724 transfer magnitudes**.

This discrepancy triggered the open-primary control below.

---

## 7. 10 kHz open-primary feedthrough control — files 028 / 029

The primary-current path was opened between the 220-Ohm resistor and ACS724 `IP+`. Therefore no closed primary-current path existed through the ACS724.

CH1 was moved from R8 to MCP6022 pin 1. CH2 remained on ACS724 VIOUT.

Acquisition remained valid at 5 MSa/s.

Coherent results:

- CH1 / MCP6022 pin 1: `2.001 Vpp @ 10 kHz`;
- CH1 residual RMS: `19.75 mV`;
- CH2 / ACS724 VIOUT: `7.114 mVpp @ 10 kHz`;
- CH2 residual RMS: `18.01 mV`.

The key observation is:

`VIOUT,10kHz = 7.114 mVpp` with the ACS724 primary path open.

Therefore a substantial coherent 10 kHz component exists on VIOUT without primary current.

This demonstrates a fixture/environment feedthrough or coupling mechanism at 10 kHz. The present evidence does not identify the exact physical coupling path.

For comparison:

- current-on capture 024/025: `9.04 mVpp` coherent on CH2;
- current-on repeat 026/027: `10.25 mVpp` coherent on CH2;
- open-primary control 028/029: `7.114 mVpp` coherent on CH2.

A large fraction of the current-on coherent CH2 magnitude can therefore not be assumed to be Hall-current response.

The scalar amplitudes must **not** be directly subtracted. In general:

`Vmeasured = VHall + Vfeedthrough`

is a complex/phasor relationship. Separation requires trustworthy relative amplitude and phase or another measurement configuration that suppresses/isolate the coupling.

---

## 8. Accepted observations

The following observations are accepted from this experiment:

1. The external `4.7 nF` FILTER capacitor was physically tested only after the corresponding schematic change had been completed, following the project rule that schematic changes precede physical circuit changes.
2. At 1 kHz, the 4.7 nF capacitor reduced CH2 residual RMS from approximately 25-27 mV to approximately 15.5-16.3 mV in two repeatable captures.
3. The primary-current reference CH1 remained clean and repeatable during the filtered 1 kHz and 10 kHz work.
4. Valid 10 kHz CSV acquisition was achieved at 5 MSa/s, giving 500 samples/cycle.
5. The 10 kHz current-on apparent gains are not acceptable ACS724 transfer measurements.
6. With the primary path open, ACS724 VIOUT still contained a coherent `7.114 mVpp` component at 10 kHz while MCP6022 pin 1 remained driven at approximately `2.001 Vpp`.
7. Coherent fixture/environment coupling is therefore demonstrated at 10 kHz and must be resolved or accounted for before accepting the high-frequency sensor transfer.

---

## 9. Not accepted / limitations

The following are explicitly **not** accepted:

- `4.7 nF` as the frozen/final product FILTER value;
- the measured 1 kHz apparent gains as a new absolute sensor calibration;
- either filtered 100 Hz capture as a replacement for the previously accepted `0.8792 V/A` practical baseline;
- `1.286 V/A` or `1.443 V/A` as the ACS724 10 kHz sensitivity;
- scalar subtraction of the open-primary 10 kHz amplitude from the current-on amplitude;
- a specific physical explanation for the demonstrated 10 kHz coupling;
- precision phase-based correction until phase reliability is independently established.

The temporary MCP6022 fixture remains a Stage-B validation fixture and is not the frozen Rev-1 4th-order approximately 15 kHz Butterworth product AFE.

---

## 10. Engineering consequence and next action

The 4.7 nF candidate has demonstrated useful noise reduction, but the experiment has exposed a new limiting mechanism: coherent 10 kHz coupling into the ACS724 VIOUT measurement.

The next work must therefore investigate and reduce or isolate this coupling before continuing to interpret high-frequency CH2/current ratios as sensor transfer magnitude.

Before any further physical circuit modification, the schematic must be updated first.

The immediate bench restoration after the open-primary control is to reconnect:

`220 Ohm -> ACS724 IP+`

returning the fixture to the documented schematic configuration.

No additional FILTER component value is selected by this record.