# Waveform CSV Manual Analysis Workflow

**Project:** Actuator Health Monitoring System  
**Purpose:** Define a repeatable manual method for interpreting DOS1102S CSV waveform exports during ACS724 dynamic/filter verification.

## 1. Current channel convention

For the present dynamic-response bench setup, the physical channel assignment is fixed as:

- **CH1 = voltage across the 68 Ω reference resistor**
- **CH2 = ACS724 VOUT**

This mapping is a laboratory wiring convention. A CSV file itself identifies only the oscilloscope channel; it does not know what physical node the probe was connected to. Therefore every analysis shall first confirm both the CSV header channel and the documented physical wiring.

## 2. One CSV per channel

The DOS1102/DOS1102S CSV save workflow uses a selected waveform source such as CH1 or CH2. In the files generated during this project, each CSV contains one channel column and identifies that channel in the header.

Therefore, when both input/reference current and ACS724 output are required for quantitative comparison, save **two CSV files for the same operating condition**:

1. CH1 CSV — reference-resistor waveform;
2. CH2 CSV — ACS724 output waveform.

Both files shall be captured without changing generator frequency/amplitude, filter configuration, wiring, timebase, probe attenuation, coupling, or acquisition settings between them where practical.

A screenshot may show both channels simultaneously, but it is supporting evidence; it does not replace preserving the numerical CSV data for each channel.

## 3. Step 1 — inspect the CSV header before calculations

Before interpreting waveform values, record or verify:

- channel identity: CH1 or CH2;
- number of samples `N`;
- sample/time interval `Δt`;
- probe attenuation;
- frequency or automatic measurements if exported;
- peak-to-peak or RMS values if exported;
- file/configuration identity.

Do not infer the physical signal from the waveform shape alone.

## 4. Step 2 — derive acquisition properties

From the sample interval:

`fs = 1 / Δt`

where `fs` is the sampling rate.

For `N` samples:

`T ≈ N × Δt`

is the approximate captured record duration.

The Nyquist frequency is:

`fN = fs / 2`

For FFT work, the approximate frequency resolution of a record of duration `T` is:

`Δf = 1 / T`

These quantities shall be checked before concluding that a CSV can represent a requested frequency band.

## 5. Step 3 — compare acquisition conditions

Two files should only be directly compared when the intentionally changed variable is known and the important acquisition/test conditions are otherwise held constant.

Check, where applicable:

- same sample interval / sampling rate;
- same record length / sample count;
- same probe attenuation;
- same channel coupling;
- same generator frequency;
- same generator amplitude;
- same reference resistor;
- same wiring and grounding;
- same sensor supply;
- same FILTER configuration except for the capacitor intentionally under test.

If these differ, document the difference before interpreting amplitude changes as filter behavior.

## 6. Step 4 — interpret CH1 as the current reference

CH1 measures the voltage across the reference resistor:

`RREF = 68 Ω`

Ohm's law gives:

`I(t) = VCH1(t) / 68 Ω`

For peak-to-peak values:

`Ipp = VCH1,pp / 68 Ω`

For a centered sinusoid:

`Ipk = Ipp / 2`

and:

`Irms = Ipk / √2`

Example:

If:

`VCH1,pp = 1.14 V`

then:

`Ipp = 1.14 / 68 ≈ 16.8 mA p-p`

and for a zero-centered sine:

`Ipk ≈ 8.4 mA`.

CH1 is therefore the measured current reference. The function-generator amplitude setting alone shall not be treated as the actual primary current because the generator has non-zero source impedance and the complete circuit determines the delivered current.

## 7. Step 5 — verify the input before comparing filters

Before comparing ACS724 output between two FILTER configurations, compare CH1 first.

If CH1 amplitude remains approximately unchanged, the injected current is approximately unchanged and a CH2 change can reasonably be attributed to the sensor/filter configuration, subject to the other controls.

If CH1 changes significantly, the experiment no longer has a constant input. In that case, raw CH2 amplitudes shall not be compared directly; use the gain ratio described below.

## 8. Step 6 — interpret CH2 as ACS724 VOUT

CH2 measures ACS724 output voltage.

Conceptually:

`VOUT(t) = Voffset + VAC(t) + noise(t)`

The DC offset is required for absolute current conversion, but the dynamic frequency-response test is primarily interested in the AC component at the applied stimulus frequency.

The relevant AC amplitude may be obtained using a fitted sine, FFT component, or consistent oscilloscope amplitude measurement. Peak-to-peak values may also be used when the waveform is sufficiently sinusoidal and the same amplitude convention is used for both current and voltage.

Do not mix peak, peak-to-peak, and RMS quantities in one gain calculation.

## 9. Step 7 — calculate sensor transfer gain

For each frequency:

`G(f) = VOUT,AC / IAC`

Units are volts per ampere (`V/A`).

Use the same amplitude definition in numerator and denominator, e.g.:

`G(f) = VOUT,pp / Ipp`

or:

`G(f) = VOUT,rms / Irms`.

At sufficiently low frequency, measured gain should be reasonably consistent with the calibrated sensor sensitivity under the current test conditions. The current project calibration is approximately:

`S = 0.74472 V/A`.

This value is a useful sanity check, not a substitute for the dynamic measurement.

## 10. Step 8 — normalize for frequency-response comparison

Choose a low-frequency reference, for example 1 kHz if it is confirmed to be well inside the passband.

Normalize gain as:

`Hnorm(f) = G(f) / G(fref)`

Then convert to decibels:

`Gain_dB(f) = 20 log10(Hnorm(f))`

Interpretation:

- `Hnorm = 1` → `0 dB`;
- `Hnorm ≈ 0.891` → about `-1 dB`;
- `Hnorm = 0.707` → about `-3 dB`.

The measured -3 dB point estimates the effective filter bandwidth.

## 11. Step 9 — compare with the theoretical FILTER prediction

For the first-order ACS724 FILTER model:

`|H(f)| = 1 / sqrt(1 + (f/fc)^2)`

with:

`fc = 1 / (2πRFCtotal)`.

Measured normalized gain should be compared against this prediction at the same frequencies, especially at the formal project band edge of 10 kHz.

A disagreement is not automatically an error; it may indicate sensor internal dynamics, component tolerance, measurement uncertainty, stimulus limitations, coupling, or non-ideal circuit behavior.

## 12. Noise-file analysis

For zero-current FILTER noise measurements, remove the mean/DC level before calculating variation.

Useful quantities are:

- mean output;
- standard deviation / RMS-type variation after mean removal;
- peak-to-peak variation;
- FFT or spectral density when needed.

Equivalent current-domain RMS noise can be estimated using measured sensitivity:

`σI = σV / S`.

Peak-to-peak shall not be converted to RMS by a fixed factor unless the waveform/statistical distribution justifies it.

## 13. Minimum manual-analysis checklist

For every new CSV:

1. Read the header.
2. Identify CH1 or CH2.
3. Confirm what that channel was physically connected to.
4. Calculate/check `fs`, record duration, and Nyquist frequency.
5. Verify acquisition conditions against the comparison file.
6. For CH1, convert resistor voltage to current using `I = V/68 Ω`.
7. For CH2, isolate the AC sensor response from DC offset and noise.
8. Confirm the input current remained comparable.
9. Calculate `G(f) = VOUT,AC/IAC`.
10. Normalize to the low-frequency reference.
11. Convert normalized magnitude to dB.
12. Compare measured result with the theoretical filter prediction.
13. Record limitations rather than forcing agreement.

## 14. Interpretation rule

The CSV is evidence of sampled voltage versus time for the channel named in its header. The meaning of that voltage comes from the documented wiring. Therefore quantitative analysis shall always maintain the chain:

`CSV header -> physical channel mapping -> acquisition validation -> electrical conversion -> normalized comparison -> engineering conclusion`.

This prevents a channel-label mistake from becoming a false electrical conclusion.