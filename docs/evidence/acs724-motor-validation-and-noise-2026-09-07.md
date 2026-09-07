# ACS724 Motor Validation and Noise Exploration — 2026-09-07

**Status:** Stage B/C bench evidence record  
**Sensor:** Pololu #4048 / ACS724LLCTR-05AU  
**Purpose:** validate the calibrated ACS724 against the real motor, then determine whether the present oscilloscope setup is ready for dynamic motor-current capture.

## 1. Relationship to the DC calibration

The preceding resistor-load calibration established the practical bench conversion:

`VOUT = 0.46910 + 0.74472·I`

and therefore:

`I = (VOUT - 0.46910) / 0.74472`

where `VOUT` is in volts and `I` is in amperes.

This evidence record uses that measured low-current calibration. It does not replace the limitations already recorded in `docs/16-acs724-dc-calibration.md`.

---

## 2. Steady motor-current validation

The motor current path was:

`PSU+ → ACS724 IP+ → ACS724 IP− → motor → PSU−`

The ACS724 signal side remained powered from the Arduino.

At the validated 4.00 V motor operating point, one steady-state measurement gave:

- PSU voltage: **4.00 V**
- PSU current: **35 mA**
- PSU power: **0.140 W**
- ACS724 `VOUT-to-GND`: **0.495 V**

Using the measured calibration:

`I_SENSOR = (0.495 - 0.46910) / 0.74472 = 0.0348 A`

Therefore:

`I_SENSOR ≈ 34.8 mA`

Comparison with the PSU indication:

- sensor-derived current: **34.8 mA**
- PSU indication: **35.0 mA**
- difference: approximately **0.2 mA**, or approximately **0.6%** relative to the PSU indication

The PSU power indication is internally consistent with the displayed voltage/current:

`4.00 V × 0.035 A = 0.140 W`

### Result

**The calibrated ACS724 DC transfer successfully reproduced the steady motor current at the tested 4 V operating point.**

This is a strong bench validation of the calibrated low-current transfer against the real motor. It is not a formal accuracy certification because the PSU display is not an independently calibrated current reference.

A later motor-on observation showed approximately 34 mA on the PSU and approximately 0.493 V on the multimeter, also consistent with the same general operating region. That separate observation is retained as supporting evidence rather than merged numerically with the validated 35 mA / 0.495 V point.

---

## 3. Oscilloscope connection troubleshooting

The first oscilloscope attempts produced contradictory results: the multimeter showed approximately 0.464–0.470 V at ACS724 OUT while CH1 appeared near 0 V.

Inspection of the instrument front panel showed that the probe BNC had been connected to the **AFG Output** connector rather than the yellow **CH1 input**.

After moving the BNC to CH1:

- CH1 immediately measured approximately **0.463 V** at the zero-current ACS724 output;
- this agreed closely with the multimeter reading;
- the apparent trigger/offset contradictions from the earlier configuration were resolved.

### Measurement rule established

**Before debugging oscilloscope settings, verify the complete physical signal path: probe tip, ground reference, probe attenuation, channel input connector, coupling, and channel configuration.**

Measurements taken while the probe BNC was connected to the AFG output are not valid ACS724 waveform evidence.

---

## 4. Zero-current DC level and sensor supply

With motor current off and the sensor powered from the Arduino:

- multimeter zero-current `VOUT-to-GND`: approximately **0.464–0.470 V**
- oscilloscope DC measurement after correct CH1 connection: approximately **0.463 V**
- oscilloscope measurement of ACS724 `VCC-to-GND`: approximately **4.60–4.63 V** in the observed runs

The zero-current output is consistent with the sensor's ratiometric behavior and the measured supply being below the nominal 5.0 V value.

These are raw bench observations; no silent correction for multimeter or PSU indication error is applied.

---

## 5. Noise-control experiments

The dynamic startup capture was deliberately deferred after a large noisy band became visible on ACS724 OUT.

The following experiments were used to separate instrument/setup noise from sensor/output-chain noise.

### 5.1 Probe / ground control

With the probe tip referenced to the same ground node as the probe ground clip, under the later AC-coupled / 20 MHz-limited configuration, repeated examples showed approximately:

- `Vpp`: **53–70 mV**
- RMS-type scope reading: **4.6–4.9 mV**

An earlier shorted-probe check under a different acquisition/timebase configuration showed a much smaller result of approximately **4.8 mVpp** and approximately **1.1 mV RMS**.

Because these tests were not made with completely identical acquisition settings, they shall not be combined into a single noise-floor number. They demonstrate that the apparent measurement floor is configuration-dependent and must be quantified using a controlled repeatable method.

### 5.2 ACS724 supply ripple/noise observation

With the probe on ACS724 VCC, AC coupling was used to remove the approximately 4.6 V DC component and expose small variations.

One repeated configuration showed approximately:

- `Vpp`: **~104–130 mV**
- RMS-type scope reading: **~11.6–12.2 mV**

The waveform contained narrow spikes; therefore peak-to-peak was strongly influenced by occasional extrema.

These built-in scope readings are descriptive bench evidence only. They are not yet a statistically controlled supply-noise characterization.

### 5.3 ACS724 OUT, motor OFF

With motor current off and the probe on ACS724 OUT, one consistent 1 ms/div observation showed approximately:

- `Vpp`: **~200 mV**
- RMS-type scope reading: **~47.6 mV**

The output disturbance was much larger than the same-ground control and larger than the observed VCC ripple in the tested configurations.

### 5.4 20 MHz oscilloscope bandwidth limit

Enabling the oscilloscope's **20 MHz bandwidth limit** produced no meaningful reduction in the observed ACS724 OUT disturbance in the tested condition:

- before: approximately **200 mVpp**, approximately **47.6 mV RMS-type reading**
- after 20 MHz limit: approximately the same values

Interpretation:

**The dominant observed disturbance is not confined to the removed 20–110 MHz portion of the oscilloscope bandwidth.**

This does not establish the detailed noise spectrum or prove a single physical source.

---

## 6. Motor OFF versus motor ON comparison

With the same general AC-coupled ACS724 OUT measurement configuration:

- motor OFF: approximately **47.6 mV RMS-type reading**
- motor ON at 4.00 V: approximately **48.6 mV RMS-type reading**

The motor-on run also showed approximately 34 mA on the PSU and approximately 0.493 V DC output on the multimeter.

### Result

Turning the motor on changed the large RMS-type disturbance only slightly in the observed test.

Therefore:

**The dominant disturbance visible on ACS724 OUT was already present at zero motor current and cannot be attributed primarily to the running motor from this experiment.**

The source remains unresolved. Plausible contributors include the sensor output noise itself, sensor supply behavior, breadboard/wiring pickup, grounding, USB/Arduino environment, probe arrangement, and acquisition configuration. No individual contributor is accepted as the cause without further controlled testing.

---

## 7. FFT exploration

The DOS1102S FFT function was used as an exploratory tool with a Hanning window.

Several spans were examined, including approximately:

- **0–12.5 kHz** (`1.25 kHz/div`, center approximately `6.25 kHz`)
- **0–1.25 kHz** (`125 Hz/div`, center approximately `625 Hz`)

Motor OFF and motor ON spectra were compared with matched display settings where practical.

### Observation

No strong, stable, clearly motor-generated spectral line was identified in the tested low-frequency views. The OFF and ON spectra remained broadly similar relative to the large background/noise floor.

### Limitation

This FFT work was exploratory only:

- screenshots were inspected visually;
- no exported waveform samples were analyzed;
- no averaged spectra or statistical confidence bounds were generated;
- no cursor-based quantitative peak table was recorded;
- several intermediate FFT span/center settings changed during learning and are not valid OFF/ON comparison pairs.

Therefore the FFT screenshots shall **not** be used to claim absence of motor spectral content. The correct conclusion is only that **no obvious repeatable motor spectral component was resolved with the present bench signal quality and exploratory FFT procedure**.

---

## 8. Engineering conclusions

The work establishes the following:

1. The calibrated ACS724 correctly reproduces the tested steady motor current near 35 mA.
2. The oscilloscope can measure the ACS724 DC output correctly once the probe is connected to the actual CH1 input.
3. The present dynamic measurement is dominated by a large disturbance that exists even with zero motor current.
4. The 20 MHz oscilloscope bandwidth limit does not materially remove that disturbance.
5. Motor ON versus OFF produces only a small change in the observed RMS-type disturbance under the tested conditions.
6. Exploratory FFT views from 0–1.25 kHz and 0–12.5 kHz did not reveal an obvious stable motor-related line above the existing background.
7. A startup-current waveform should **not** yet be accepted as motor-current evidence until the measurement-chain noise is quantified and controlled.

---

## 9. Evidence-quality limitation

The current visual record consists primarily of phone photographs/video of the DOS1102S screen.

The project verification plan already requires preservation of original instrument exports where practical. Therefore native DOS1102S screenshots/waveform exports shall be preferred for future quantitative evidence and stored in the repository without modification before analysis.

---

## 10. Immediate next actions

The next work shall follow the existing Phase 3 verification plan rather than adding an arbitrary filter only to make the trace look cleaner.

Recommended sequence:

1. **Verify the DOS1102S USB export path** using a known function-generator waveform so file format, time scale, voltage scale, sample count, and import interpretation are proven.
2. **Export a controlled zero-current ACS724 waveform** with fixed, documented settings and analyze it in MATLAB for mean, RMS/standard-deviation-type noise, peak-to-peak, and equivalent current-domain noise using the measured sensitivity.
3. **Repeat the planned supply-source comparison** under controlled settings: bench 5 V → Arduino 5 V → bench 5 V, keeping probe/acquisition configuration fixed where practical.
4. Re-check the same-ground measurement-system floor under the identical acquisition settings used for the sensor waveform.
5. Only after the noise source and usable SNR are understood, proceed to the designed analog-front-end / anti-alias filtering and repeat motor OFF/ON and startup tests.
6. Preserve the formal Rev-1 **DC–10 kHz diagnostic band**. Do not modify the ACS724 FILTER configuration without an explicit design decision and verification that this band remains preserved.

**Immediate next bench task:** verify and use native DOS1102S waveform export, then perform the first reproducible zero-current noise analysis from exported samples.
