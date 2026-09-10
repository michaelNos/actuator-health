# ACS724 100 Hz positive-current baseline closure — 2026-09-10

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — ACS724 dynamic/FILTER validation  
**Status:** 100 Hz positive-current magnitude baseline accepted for normalized FILTER sweep; absolute phase not accepted.

## 1. Purpose

This record closes the 100 Hz bring-up and validation work for the temporary MCP6022 positive-bias stimulus fixture before proceeding to higher-frequency ACS724 FILTER measurements.

The objective of this work was not merely to obtain a visible waveform. It was to establish a defensible 100 Hz reference point under conditions that are valid for the ACS724LLCTR-05AU unidirectional sensor, with:

- current remaining positive for the complete cycle;
- independently measured primary current on CH1;
- ACS724 VIOUT on CH2;
- coherent extraction of the known excitation frequency rather than use of raw peak-to-peak noise;
- repeatability checks;
- a zero-primary-current control to test whether apparent 100 Hz VIOUT response is caused by electrical feedthrough rather than Hall response.

This record consolidates the evidence accumulated after the earlier PRs that documented fixture construction, first positive-current capture, CH1 resolution correction, and stronger-stimulus testing.

---

## 2. Fixture configuration at baseline closure

### 2.1 Sensor

The project sensor is the Pololu #4048 carrier using ACS724LLCTR-05AU.

Established project facts used here:

- specified primary-current range: 0 A to 5 A, unidirectional;
- nominal sensitivity at 5 V: approximately 0.8 V/A;
- nominal zero-current output at 5 V: approximately 0.5 V;
- project bench DC calibration established earlier:

`VOUT = 0.46910 + 0.74472 * I`

with `I` in amperes;

- stock carrier FILTER capacitor: 1 nF;
- stock carrier bandwidth is much higher than 100 Hz, so 100 Hz is used as the low-frequency reference point for later normalized transfer measurements.

### 2.2 MCP6022 positive-bias driver

The temporary dynamic-test driver uses MCP6022 channel A as an equal-ratio inverting level shifter around a buffered reference.

Measured resistor values:

- `RIN = 99.1 kOhm`;
- `RF = 99.0 kOhm`.

The implemented relation is approximately:

`VDRV = 2*VREF - VAFG`

with the driver output on MCP6022 pin 1.

The purpose of the positive DC bias is to prevent the AFG sine from reversing primary-current direction during half of each cycle.

### 2.3 Primary-current path

The validated current path is:

`MCP6022 pin 1 -> 220 ohm -> ACS724 IP+ -> ACS724 IP- -> RREF 68.8 ohm -> GND`

Current direction was physically checked against the carrier `+i` arrow and is:

`220-ohm side -> RREF side`

which is the defined positive-current direction.

### 2.4 Oscilloscope measurement convention

Formal sensor measurements use:

- `CH1 = voltage across RREF = 68.8 ohm`;
- `CH2 = ACS724 VIOUT`;
- both channels DC coupled;
- both channel grounds referenced to the common circuit ground because the DOS1102S channel grounds are common.

The current reference is calculated directly from CH1:

`I(t) = VRREF(t) / 68.8 ohm`

For driver-validation checks only, CH2 is temporarily moved from ACS724 VIOUT to MCP6022 pin 1.

---

## 3. Analysis method

Raw oscilloscope `PK-PK` values are not used as the primary transfer metric for ACS724 VIOUT because VIOUT contains broadband spikes/noise much larger than the sinusoidal Hall component.

For each frozen CH1/CH2 CSV pair, the known excitation frequency is extracted by least-squares fitting:

`v(t) = V0 + A*sin(2*pi*f*t) + B*cos(2*pi*f*t)`

The coherent peak magnitude is:

`Vpk = sqrt(A^2 + B^2)`

and the coherent peak-to-peak magnitude is:

`Vpp,f = 2*Vpk`.

For CH1:

`Ipp,f = VRREF,pp,f / 68.8`

For CH2:

`G(f) = VOUT,pp,f / Ipp,f`

Phase is calculated from the fitted sine/cosine coefficients of both channels. Phase is treated more conservatively than magnitude because CH2 noise remained high throughout the 100 Hz work.

For the future FILTER sweep, the primary quantity of interest is the normalized magnitude:

`H(f) = G(f) / G(100 Hz)`

and:

`HdB(f) = 20*log10(H(f))`.

This normalization is important: the FILTER sweep depends on relative frequency response, not on forcing the 100 Hz absolute gain to equal either the nominal datasheet sensitivity or the previous DC calibration exactly.

---

## 4. Measurement-development history

### 4.1 First synchronized positive-current capture

The first synchronized CH1/CH2 positive-current capture demonstrated that the fixture architecture could produce a valid unidirectional stimulus, but CH1 had inadequate vertical resolution.

The CH1 CSV contained only four distinct values:

- 400 mV;
- 480 mV;
- 560 mV;
- 640 mV.

The resulting provisional gain was not accepted.

This limitation was documented previously and led directly to a finer CH1 vertical scale.

### 4.2 Corrected CH1 vertical resolution

After reducing the CH1 volts/div and positioning the DC-biased waveform correctly, the CH1 export contained 36 distinct values rather than four.

The coherent CH1 fit became strong and repeatable, establishing that CH1 acquisition resolution was no longer the dominant limitation.

The remaining limitation was CH2 SNR.

### 4.3 Stimulus-amplitude increase

The AFG setting was increased in controlled steps while repeatedly checking that:

- MCP6022 pin 1 remained sinusoidal and unclipped;
- current remained positive for the whole cycle;
- the current-reference signal remained clean.

At the 2.00 Vpp AFG setting, the driver-validation screen showed approximately:

- MCP6022 pin 1 average: 2.522 V;
- MCP6022 pin 1 raw `Vpp`: 2.020 V;
- therefore approximate driver extremes: 1.512 V to 3.532 V;
- RREF average: 589.3 mV;
- RREF raw `Vpp`: 480.0 mV.

Using the screen values for the positive-current safety check:

`VRREF,min = 0.5893 - 0.480/2 = 0.3493 V`

therefore:

`Imin = 0.3493 / 68.8 = 5.08 mA`

and:

`Imax = (0.5893 + 0.480/2) / 68.8 = 12.05 mA`.

Thus the 2.00 Vpp stimulus was directly demonstrated to stay positive for the complete cycle with substantial margin.

---

## 5. 2.00 Vpp current-on repeatability series

Three independent current-on measurements were analyzed at 100 Hz with the AFG set to 2.00 Vpp.

### 5.1 Run A — files 011 / 012

`011 = CH1 / RREF`  
`012 = CH2 / ACS724 VIOUT`

Coherent 100 Hz results:

- CH1: `VRREF,100 = 474.185 mVpp`;
- CH1 fit `R^2 = 0.999715`;
- inferred current: `I100 = 6.892 mApp`;
- CH2: `VOUT,100 = 5.873 mVpp`;
- transfer magnitude: `G100 = 0.8522 V/A`;
- fitted CH2-CH1 phase: approximately `-0.97 deg`;
- CH2 residual RMS after DC and 100 Hz fit: approximately `30.03 mV RMS`.

The full-record magnitude was plausible, but short five-cycle block estimates remained noisy:

- gain approximately 0.728 to 1.036 V/A;
- phase approximately -18.7 to +34.9 deg.

This run alone was therefore insufficient for acceptance.

### 5.2 Run B — files 013 / 014

`013 = CH1 / RREF`  
`014 = CH2 / ACS724 VIOUT`

Coherent 100 Hz results:

- CH1: `VRREF,100 = 470.989 mVpp`;
- CH1 fit `R^2 = 0.999717`;
- inferred current: `I100 = 6.846 mApp`;
- CH2: `VOUT,100 = 6.233 mVpp`;
- transfer magnitude: `G100 = 0.9105 V/A`;
- fitted CH2-CH1 phase: approximately `+7.59 deg`;
- CH2 residual RMS: approximately `30.03 mV RMS`.

The current stimulus repeated extremely closely relative to Run A.

Five-cycle block results still varied substantially:

- gain approximately 0.752 to 1.141 V/A;
- phase approximately -12.5 to +18.1 deg.

The second run supported magnitude repeatability but still did not justify accepting phase.

### 5.3 Run C — long record, files 015 / 016

`015 = CH1 / RREF`  
`016 = CH2 / ACS724 VIOUT`

The time interval was 100 us and the record contained 10,000 samples, giving approximately 1.0 s total duration and about 100 cycles at 100 Hz.

Coherent results:

- CH1: `VRREF,100 = 470.821 mVpp`;
- CH1 fit `R^2 = 0.998591`;
- inferred current: `I100 = 6.843 mApp`;
- CH2: `VOUT,100 = 6.017 mVpp`;
- transfer magnitude: `G100 = 0.8792 V/A`;
- fitted CH2-CH1 phase: approximately `-6.35 deg`;
- CH2 residual RMS: approximately `28.92 mV RMS`.

Splitting the long record into two independent 50-cycle halves gave:

- first half gain: approximately `0.911 V/A`;
- second half gain: approximately `0.863 V/A`.

This was significantly more stable than the earlier five-cycle estimates and demonstrated the value of longer coherent averaging.

---

## 6. Repeatability summary

The three independent 2.00 Vpp full-record transfer magnitudes are:

| Run | G100 |
|---|---:|
| A | 0.8522 V/A |
| B | 0.9105 V/A |
| C, long record | 0.8792 V/A |

Arithmetic mean:

`mean(G100) = 0.8807 V/A`

Sample standard deviation:

`SD = 0.0292 V/A`

Relative sample standard deviation:

`SD / mean = 3.32 %`.

The long-record result lies almost exactly at the three-run mean.

For comparison only:

- nominal datasheet sensitivity is approximately 0.8 V/A at 5 V;
- previous project DC calibration slope is 0.74472 V/A.

The 100 Hz absolute AC magnitude therefore remains somewhat higher than the previous DC slope. That discrepancy is retained as an observed limitation; it is not silently corrected or calibrated away.

For FILTER development the accepted practical baseline is the measured low-frequency response itself, and later points will be normalized to it.

---

## 7. Feedthrough / pickup controls

Before accepting the 100 Hz magnitude as predominantly Hall-current response, the primary-current path was opened and the 100 Hz electrical environment was left active.

### 7.1 Open-primary test with CH1 on RREF — files 017 / 018

The 220-ohm connection to ACS724 IP+ was disconnected.

With the primary path open:

- CH1 on the open RREF node still showed approximately `8.135 mVpp` coherent at 100 Hz;
- CH2 / VIOUT showed approximately `1.122 mVpp` coherent at 100 Hz.

The open RREF node was therefore demonstrably picking up the 100 Hz environment and was not an appropriate feedthrough reference.

This test established the existence of pickup on a floating/open measurement node, but did not establish a coherent ACS724 feedthrough transfer.

### 7.2 Proper feedthrough control with CH1 on MCP6022 pin 1 — files 019 / 020

The primary path remained open, but CH1 was moved to the actual MCP6022 driver output.

Results:

- CH1 / MCP6022 pin 1 coherent 100 Hz amplitude: `1.9816 Vpp`;
- CH1 fit `R^2 = 0.998709`;
- CH2 / ACS724 VIOUT coherent 100 Hz amplitude: `0.556 mVpp`;
- CH2 residual RMS: approximately `29.62 mV RMS`.

The VIOUT 100 Hz component was below the local neighboring spectral background in this control and its phase relative to pin 1 was not stable between two 50-cycle halves:

- first half relative phase: approximately `123.6 deg`;
- second half relative phase: approximately `175.9 deg`.

Therefore no stable coherent 100 Hz electrical feedthrough from the MCP6022 driver into ACS724 VIOUT was demonstrated by this control.

The current-on long-record VIOUT component was approximately 6.017 mVpp, compared with only 0.556 mVpp in this no-current control, and the control component itself lacked stable phase/spectral significance.

Engineering interpretation:

**The accepted 100 Hz current-on magnitude is predominantly a genuine current-dependent ACS724 response rather than a demonstrated coherent electrical-feedthrough artifact.**

---

## 8. Accepted 100 Hz baseline

### 8.1 Accepted for the FILTER sweep

The following are accepted as the practical 100 Hz baseline state:

- the MCP6022 fixture can produce a valid positive-current sinusoidal primary-current stimulus;
- the 2.00 Vpp AFG operating condition has been directly checked for driver headroom and positive current;
- CH1 / RREF is a high-quality coherent current reference at 100 Hz;
- three independent 2.00 Vpp runs give repeatable full-record gain magnitudes around 0.88 V/A;
- the long-record 100-cycle transfer magnitude is `0.8792 V/A`;
- the three-run mean is `0.8807 V/A`, with sample SD `0.0292 V/A` or approximately `3.32 %`;
- a proper open-primary control did not demonstrate stable coherent 100 Hz driver-to-VIOUT feedthrough.

For subsequent normalized frequency-response calculations, use:

`G100,baseline = 0.8792 V/A`

from the long 100-cycle run as the primary numerical baseline, while retaining the three-run distribution as repeatability evidence.

### 8.2 Not accepted

The following are **not** accepted at this point:

- precision absolute phase at 100 Hz;
- a claim that the true absolute ACS724 sensitivity is exactly 0.8792 V/A under all conditions;
- replacement of the previous DC calibration by the 100 Hz value;
- any external FILTER capacitor choice;
- any higher-frequency transfer point.

CH2 broadband residual noise remains approximately 29-30 mV RMS, much larger than the approximately 6 mVpp coherent 100 Hz Hall component. Coherent averaging makes magnitude usable, but phase remains too sensitive to noise for acceptance.

---

## 9. Why 100 Hz is now sufficient as the reference point

The purpose of the upcoming dynamic FILTER sweep is to determine relative attenuation versus frequency.

For each frequency:

`G(f) = VOUT,f / I(f)`

and the normalized response is:

`H(f) = G(f) / 0.8792`

so 100 Hz becomes:

`H(100 Hz) = 1`

and therefore:

`HdB(100 Hz) = 0 dB`.

This approach avoids confusing the FILTER measurement with the unresolved difference between nominal sensitivity, prior DC calibration slope, and the measured 100 Hz AC gain.

The frequency sweep will answer a different question:

**How much of the low-frequency current-to-voltage response remains at each higher frequency?**

That is the quantity needed to validate the stock FILTER behavior and later compare external FILTER capacitor candidates.

---

## 10. Boundary before 1 kHz work

A first 1 kHz CH1/CH2 CSV pair (`021` / `022`) has already been captured, but it is **not accepted as a 1 kHz transfer point** and is intentionally not incorporated into the baseline.

The initial 1 kHz export used a 100 us sample interval, giving only 10 samples per 1 kHz cycle. The CH1 record also showed substantial harmonic content and reduced sine-fit quality compared with the 100 Hz baseline. Therefore the apparent 1 kHz gain drop from that first attempt must not be interpreted as ACS724 FILTER attenuation.

The project is paused at this boundary specifically to document and freeze the 100 Hz methodology before repeating 1 kHz with an acquisition configuration suitable for the higher frequency.

---

## 11. Next controlled task

Proceed to 1 kHz only after this 100 Hz baseline record is reviewed/merged.

The next experiment will preserve:

- AFG amplitude at the validated 2.00 Vpp operating condition;
- positive-bias MCP6022 fixture;
- `RREF = 68.8 ohm`;
- formal convention `CH1 = RREF`, `CH2 = ACS724 VIOUT` for the sensor capture;
- coherent extraction at the exact commanded frequency;
- frozen-acquisition CH1/CH2 pairing.

Before accepting the 1 kHz sensor result, the higher-frequency acquisition must first demonstrate that the MCP6022 output and RREF current waveform are clean and adequately sampled.

No 1 kHz transfer point and no FILTER capacitor value are approved by this record.
