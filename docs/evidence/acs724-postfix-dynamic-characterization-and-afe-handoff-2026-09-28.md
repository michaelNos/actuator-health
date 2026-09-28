# ACS724 Post-Fix Dynamic Characterization and AFE Handoff — 2026-09-28

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B implementation / subsystem characterization  
**Status:** Raw ACS724 dynamic-characterization campaign closed for the present fixture; AFE bring-up is the next development step  
**Sensor:** Pololu #4048 / Allegro ACS724LLCTR-05AU  
**Experimental FILTER:** stock carrier 1 nF plus external 4.7 nF to GND, approximately 5.7 nF total  
**Primary reference resistor:** measured R8 = 67 Ω  
**Scope:** HANMATEK DOS1102S  
**Important limitation:** this report does not freeze a final AC sensitivity or final FILTER value.

## 1. Purpose

This report closes the corrected-wiring dynamic-characterization campaign performed after the ACS724 FILTER ground connection was physically repaired and after a MCP6022 package-orientation mistake was identified.

The report records:

- the corrected temporary MCP6022 positive-bias stimulus fixture;
- the MCP6022 pin-numbering incident and its consequences for earlier troubleshooting;
- the verified acquisition settings used for 1, 5, 7.5, and 10 kHz work;
- coherent-fit current and sensor-output results;
- the measured dual-channel CSV timing skew and its correction;
- open-primary feedthrough controls;
- repeated and interleaved transfer measurements;
- the limits imposed by low CH2 signal-to-residual ratio;
- the engineering decision to stop trying to identify a precise raw-sensor AC transfer with this small-signal fixture;
- the provisional decision to retain the added 4.7 nF FILTER capacitor while proceeding to Analog Front End bring-up.

The governing workflow remains:

`predict → connect/configure → measure → compare → understand → document`

Only measured or directly calculated values are treated as established. A plausible model is not promoted into a measured device parameter.

---

## 2. Physical configuration after correction

### 2.1 MCP6022 package orientation

The MCP6022 PDIP-8 is numbered counter-clockwise in top view:

```text
             notch / dot
                ↓
          ┌───────────┐
 OUT A  1 │           │ 8  VDD (+5 V)
 -IN A  2 │           │ 7  OUT B
 +IN A  3 │           │ 6  -IN B
 VSS    4 │           │ 5  +IN B
          └───────────┘
```

The right-hand side is therefore **8, 7, 6, 5 from top to bottom**, not 5, 6, 7, 8.

During troubleshooting, the physical right-side legs had temporarily been named as if their numbers increased downward. The supply happened to work because the top-right physical leg was connected to +5 V, but that leg is actual pin 8. Several intermediate conclusions about “pin 5”, “pin 7”, and “pin 8” were consequently based on incorrect names and are not valid diagnostic evidence.

After the numbering error was recognized, the physical package was reinterpreted correctly and the fixture was restored.

### 2.2 Correct fixture roles

- pin 8 = VDD = +5 V;
- pin 4 = VSS = circuit GND;
- 100 nF local bypass capacitor between pins 8 and 4;
- channel B buffers the reference:
  - pin 5 = VREF_RAW input;
  - pin 6 connected to pin 7;
  - pin 7 = VREF_BUF;
- channel A is the biased inverting driver:
  - pin 3 = VREF_BUF;
  - AFG through approximately 99 kΩ to pin 2;
  - feedback approximately 99 kΩ from pin 1 to pin 2;
  - pin 1 = VDRV.

For approximately equal input and feedback resistors:

`VDRV ≈ 2·VREF_BUF − VAFG`

With the AFG generating a zero-centered sine, this shifts the primary-current stimulus into the positive-current region required by the unidirectional ACS724 05AU variant.

### 2.3 Supply decoupling

The local 100 nF capacitor between MCP6022 pins 8 and 4 remains required as high-frequency supply bypassing. Additional parallel capacitance may serve as bulk/local energy storage for slower rail disturbances, but it does not replace the local 100 nF bypass.

The distinction is:

- local 100 nF bypass: fast/high-frequency current demand and supply disturbance;
- bulk capacitance: slower/larger rail variation.

### 2.4 Primary-current path

For current-on transfer measurements:

`MCP6022 pin 1 → 220 Ω → ACS724 IP+ → ACS724 IP− → R8 67 Ω → GND`

Scope convention:

- CH1 tip = R8 top / ACS724 IP− side;
- CH1 ground = circuit GND;
- CH2 tip = ACS724 OUT;
- CH2 ground = circuit GND.

Therefore:

`I_primary(t) = V_CH1(t) / 67 Ω`

The two DOS1102S channel grounds are common and are not isolated.

---

## 3. FILTER configuration and prediction

The Pololu carrier already contains approximately 1 nF at FILTER. The temporary external capacitor is 4.7 nF:

`C_total ≈ 1 nF + 4.7 nF = 5.7 nF`

Using the ACS724 FILTER-resistance approximation:

`R_F ≈ 1.8 kΩ`

the simple first-order estimate is:

`f_c ≈ 1/(2πR_FC_total) ≈ 15.5 kHz`

This is a design approximation, not a complete ACS724 dynamic model.

Larger diagnostic capacitors were previously shown to reduce broadband CH2 variation, but they also lower bandwidth:

| Added capacitor | Approx. total C | Approx. simple-pole fc |
|---|---:|---:|
| 4.7 nF | 5.7 nF | 15.5 kHz |
| 10 nF | 11 nF | 8.0 kHz |
| 22 nF | 23 nF | 3.8 kHz |
| 100 nF | 101 nF | 0.88 kHz |

The Rev-1 diagnostic band remains DC–10 kHz. Therefore 10 nF and 22 nF cannot be selected merely because their traces look quieter: their simple estimated corners would already encroach strongly on or fall below the required band.

**Current engineering disposition:** retain 4.7 nF as a provisional Stage-B FILTER candidate. It is not frozen as the final Rev-1 value.

---

## 4. Acquisition method

### 4.1 Coherent component fit

For a target frequency f, each channel is modeled as:

`v(t) = VDC + A·sin(2πft) + B·cos(2πft)`

The fitted peak amplitude is:

`Vpk = sqrt(A² + B²)`

and:

`Vpp = 2·sqrt(A² + B²)`

with phase:

`φ = atan2(B, A)`

This method extracts only the component coherent with the commanded test frequency. It is intentionally different from raw oscilloscope Vpp, which can be inflated by noise spikes, harmonics, and unrelated spectral content.

For CH1:

`Ipp = VCH1,pp / 67 Ω`

For CH2:

`|H(f)| = VCH2,pp / Ipp`

Units are V/A.

The per-channel residual is the measured waveform minus that channel's DC-plus-target-sine fit. It is **not** CH2 minus CH1.

### 4.2 Current acquisition settings

For 1 kHz:

- `M: 20 ms/div`
- depth 10K
- CSV sample interval = 40 µs
- sample rate = 25 kSa/s
- stored duration = 400 ms
- 25 samples/cycle
- 400 cycles

For 5, 7.5, and 10 kHz:

- `M: 2 ms/div`
- depth 10K
- CSV sample interval = 4 µs
- sample rate = 250 kSa/s
- stored duration = 40 ms
- 5 kHz: 50 samples/cycle, 200 cycles
- 7.5 kHz: 33.3 samples/cycle, 300 cycles
- 10 kHz: 25 samples/cycle, 400 cycles

All quantitative CSV captures used:

- Sample acquisition;
- synchronized ALL export;
- DC coupling;
- 1× probes;
- 20 MHz bandwidth limit ON;
- acquisition stopped before CSV export.

The operator-facing setting is `M: ... ms/div`; sample interval and sample rate are verified afterward from the CSV.

---

## 5. Corrected 5 kHz bring-up

A failed 5 kHz test initially appeared to show almost no primary stimulus. Troubleshooting eventually exposed the MCP6022 right-side pin-numbering mistake. After correcting the physical interpretation and rebuilding the fixture:

- MCP6022 pin 1 showed approximately 2.1 Vpp at 5 kHz;
- CH1 across R8 showed approximately 0.496 Vpp on the scope;
- the primary stimulus was therefore restored.

The 0.496 V raw scope Vpp corresponds to approximately 7.4 mApp through 67 Ω, while coherent-fit CSV values were near 7.0 mApp. The difference is expected because raw Vpp includes non-fundamental content and extremes.

The earlier “missing 5 kHz” measurement is not used as sensor-response evidence.

---

## 6. Post-fix transfer measurements

### 6.1 1 kHz — ten-run set

All ten files are post-fix captures with verified FILTER ground and corrected fixture wiring.

| File | Ipp (mA) | CH2 coherent Vpp (mV) | |H| (V/A) | Corrected phase (°) | CH2 residual RMS (mV) |
|---|---:|---:|---:|---:|---:|
| `data_39_005...postfix-1.csv` | 6.7885 | 6.5423 | 0.9637 | -6.00 | 13.190 |
| `data_39_006...postfix-2.csv` | 6.8000 | 5.5006 | 0.8089 | -3.85 | 13.313 |
| `data_39_007...postfix-3.csv` | 6.8042 | 5.9190 | 0.8699 | -4.81 | 13.243 |
| `data_39_008...postfix-4.csv` | 6.8207 | 5.8011 | 0.8505 | -13.01 | 13.219 |
| `data_39_009...postfix-5.csv` | 6.7860 | 5.3697 | 0.7913 | -8.56 | 13.343 |
| `data_39_010...postfix-6.csv` | 6.8106 | 5.8478 | 0.8586 | -5.50 | 13.029 |
| `data_39_011...postfix-7.csv` | 6.7890 | 5.8991 | 0.8689 | -9.36 | 13.056 |
| `data_39_012...postfix-8.csv` | 6.7808 | 6.0044 | 0.8855 | -3.70 | 13.008 |
| `data_39_013...postfix-9.csv` | 6.7934 | 6.6093 | 0.9729 | -3.70 | 12.935 |
| `data_39_014...postfix-10.csv` | 6.7703 | 6.7546 | 0.9977 | -7.08 | 13.325 |

Aggregate:

- mean Ipp = 6.7943 mA;
- Ipp range = 6.7703–6.8207 mA;
- scalar mean |H| = 0.8868 V/A;
- sample SD of |H| = 0.0696 V/A;
- complex-average transfer = **0.8857 ∠ -6.51° V/A**;
- mean CH2 residual RMS = 13.166 mV.

CH1 is highly repeatable. CH2 coherent magnitude still scatters significantly.

CH1 is not a pure sine. Across the ten 1 kHz records, the mean fitted fundamental is approximately 455.2 mVpp and the third harmonic is approximately 43.9 mVpp. Harmonics are deterministic distortion content and are not automatically random noise.

### 6.2 5 kHz — five-run set

| Run | Ipp (mA) | CH2 coherent Vpp (mV) | |H| (V/A) | Corrected phase (°) | CH2 residual RMS (mV) |
|---|---:|---:|---:|---:|---:|
| 1 | 6.9699 | 5.4875 | 0.7873 | -21.50 | 14.516 |
| 2 | 7.0010 | 5.5848 | 0.7977 | -22.39 | 15.079 |
| 3 | 7.0015 | 6.9670 | 0.9951 | -28.60 | 15.158 |
| 4 | 6.9692 | 6.7702 | 0.9714 | -22.26 | 15.058 |
| 5 | 7.0048 | 5.6611 | 0.8082 | -20.80 | 14.213 |

Aggregate:

- mean Ipp = 6.9893 mA;
- scalar mean |H| = 0.8719 V/A;
- sample SD = 0.1022 V/A;
- complex average = **0.8708 ∠ -23.32° V/A**;
- mean CH2 residual RMS = 14.805 mV.

The current reference remains stable while CH2 magnitude varies substantially.

### 6.3 7.5 kHz — ten-run set

| Run | Ipp (mA) | |H| (V/A) | Corrected phase (°) | CH2 residual RMS (mV) |
|---|---:|---:|---:|---:|
| 1 | 6.8984 | 0.7876 | -19.48 | 14.285 |
| 2 | 6.8972 | 0.8512 | -44.77 | 14.118 |
| 3 | 6.9081 | 0.9292 | -26.77 | 14.731 |
| 4 | 6.8991 | 0.8901 | -45.92 | 14.484 |
| 5 | 6.8962 | 0.8107 | -39.17 | 14.334 |
| 6 | 6.9046 | 0.6668 | -32.25 | 14.475 |
| 7 | 6.8972 | 0.6706 | -47.01 | 14.495 |
| 8 | 6.8997 | 0.5827 | -53.59 | 14.473 |
| 9 | 6.9056 | 0.6843 | -30.23 | 14.318 |
| 10 | 6.9009 | 0.5987 | -27.61 | 14.366 |

Aggregate:

- mean Ipp = 6.9007 mA;
- scalar mean |H| = 0.7472 V/A;
- sample SD = 0.1227 V/A;
- complex average = **0.7352 ∠ -36.46° V/A**;
- mean CH2 residual RMS = 14.408 mV.

A strong time ordering appeared:

- runs 1–5 complex average ≈ **0.8400 ∠ -35.39° V/A**;
- runs 6–10 complex average ≈ **0.6308 ∠ -37.90° V/A**.

The phase remained broadly similar while coherent magnitude moved downward. This motivated the interleaved-frequency control.

### 6.4 10 kHz — ten-run set

| Run | Ipp (mA) | |H| (V/A) | Corrected phase (°) | CH2 residual RMS (mV) |
|---|---:|---:|---:|---:|
| 1 | 6.8308 | 0.8187 | -56.03 | 15.227 |
| 2 | 6.7769 | 0.7837 | -45.36 | 14.669 |
| 3 | 6.8283 | 0.7700 | -46.54 | 14.543 |
| 4 | 6.7745 | 0.9302 | -51.49 | 15.043 |
| 5 | 6.7950 | 0.8217 | -45.48 | 14.977 |
| 6 | 6.7732 | 0.7614 | -52.70 | 14.761 |
| 7 | 6.7995 | 0.7362 | -33.36 | 15.205 |
| 8 | 6.7910 | 0.7737 | -71.82 | 14.768 |
| 9 | 6.7824 | 0.9523 | -53.69 | 14.567 |
| 10 | 6.7618 | 0.7877 | -44.93 | 15.373 |

Aggregate:

- mean Ipp = 6.7914 mA;
- scalar mean |H| = 0.8136 V/A;
- sample SD = 0.0720 V/A;
- complex average = **0.8032 ∠ -50.29° V/A**;
- mean CH2 residual RMS = 14.913 mV.

Again, CH1 current is stable while CH2 estimates scatter.

---

## 7. Dual-channel timing control

A phase result between CH1 and CH2 cannot be interpreted physically until channel-to-channel timing skew is measured.

### 7.1 10 kHz same-node control

Both probes were placed on the same R8 node.

File:

`data_39_025-10kHz-same-node-R8-timing-control.csv`

Measured coherent components:

- CH1 = 453.471 mVpp, phase -30.495°;
- CH2 = 453.930 mVpp, phase -44.419°;
- raw CH2−CH1 phase = **-13.924°**.

At 10 kHz with Δt = 4 µs, one stored sample is:

`360° × 10000 × 4 µs = 14.4°`

Advancing CH2 by one stored sample leaves approximately:

**+0.476°**

Amplitude mismatch is only about 0.10%.

Waveform correlation improves from approximately 0.9565 to 0.9966 after the one-sample alignment.

### 7.2 1 kHz same-node control

File:

`data_39_026-1kHz-same-node-R8-timing-control-postfix.csv`

Measured coherent components:

- CH1 = 454.488 mVpp, phase +2.944°;
- CH2 = 454.955 mVpp, phase -11.847°;
- raw CH2−CH1 phase = **-14.791°**.

At 1 kHz with Δt = 40 µs, one stored sample is again:

`360° × 1000 × 40 µs = 14.4°`

After one-sample correction:

**-0.391°**

Correlation improves from approximately 0.9543 to 0.9968.

### 7.3 Accepted interpretation

The exported CH2 waveform appears approximately one stored sample behind CH1 in both tested acquisition modes.

The exact internal cause is unknown. It may involve channel digitization, digital processing, memory alignment, or export behavior, but none of these mechanisms has been demonstrated.

Accepted engineering statement:

> The DOS1102S CSV data show an approximately one-stored-sample CH2 lag relative to CH1 under the tested modes. Transfer-phase results are corrected by advancing CH2 one stored sample.

The correction is frequency dependent in degrees because a fixed sample interval occupies a different fraction of a period:

- 1 kHz at 40 µs: +14.4°;
- 5 kHz at 4 µs: +7.2°;
- 7.5 kHz at 4 µs: +10.8°;
- 10 kHz at 4 µs: +14.4°.

---

## 8. Open-primary feedthrough controls

Purpose: determine whether coherent CH2 output could be caused by direct AFG/MCP6022 coupling instead of primary current.

Configuration:

- ACS724 powered;
- FILTER +4.7 nF connected correctly to GND;
- AFG/MCP6022 running;
- primary path intentionally open at the 220 Ω → IP+ connection;
- CH1 moved to MCP6022 pin 1;
- CH2 remained on ACS724 OUT.

### 8.1 Accidental 1 kHz control

File name:

`data_39_027-10kHz-open-primary-postfix-feedthrough-1.csv`

Despite its filename, CH1 spectral content and the CSV header show the actual stimulus was 1 kHz.

Results:

- CH1 coherent 1 kHz = 1.9866 Vpp;
- CH2 coherent 1 kHz = 0.0635 mVpp;
- CH2 residual RMS = 2.559 mV.

The coherent feedthrough component is tiny compared with the approximately 5–7 mVpp current-on response. Its phase is not meaningful because it is deeply buried in residual variation.

### 8.2 10 kHz control

File:

`data_39_028-10kHz-open-primary-postfix-feedthrough-1.csv`

The scope header reported 5 kHz, but direct analysis of CH1 shows a dominant 10 kHz component.

Results:

- CH1 coherent 10 kHz = 1.8953 Vpp;
- CH2 coherent 10 kHz = 0.0734 mVpp;
- CH2 residual RMS = 2.717 mV.

Compared with a representative current-on 10 kHz coherent response of approximately 5.45 mVpp, this is about 1.35% in amplitude, roughly -37 dB.

### 8.3 5 kHz control

File:

`data_39_029-5kHz-open-primary-postfix-feedthrough-1.csv`

Results:

- CH1 coherent 5 kHz = 1.9820 Vpp;
- CH2 coherent 5 kHz = 0.0132 mVpp;
- CH2 residual RMS = 2.705 mV.

Compared with the approximately 6.09 mVpp mean current-on 5 kHz coherent response, this is about 0.22%, roughly -53 dB.

### 8.4 Conclusion

Direct MCP6022/AFG feedthrough is too small to explain the measured current-on coherent CH2 signal at 1, 5, or 10 kHz.

The feedthrough tests therefore strengthen the conclusion that the current-on coherent component is current dependent.

They do **not** prove that every measured amplitude/phase value is an accurate intrinsic ACS724 transfer parameter, because low SNR and other measurement-chain effects remain.

---

## 9. Interleaved-frequency control

The 7.5 kHz sequential runs showed a large magnitude change with run order. To test whether this was simple warm-up/time drift, the frequency was interleaved while wiring remained unchanged:

5 kHz → 7.5 kHz → 10 kHz → 5 kHz → 7.5 kHz → 10 kHz.

| Seq. | f | Ipp (mA) | |H| (V/A) | Corrected phase | CH2 residual RMS |
|---|---:|---:|---:|---:|---:|
| A1 | 5 kHz | 7.0220 | 0.5560 | -20.92° | 14.649 mV |
| A2 | 7.5 kHz | 6.9005 | 0.7981 | -43.76° | 14.597 mV |
| A3 | 10 kHz | 6.8069 | 0.8954 | -42.30° | 14.340 mV |
| A4 | 5 kHz | 7.0425 | 1.0560 | -40.35° | 14.339 mV |
| A5 | 7.5 kHz | 6.8993 | 0.7714 | -26.34° | 14.712 mV |
| A6 | 10 kHz | 6.8408 | 0.7686 | -28.56° | 14.234 mV |

At 5 kHz the apparent transfer magnitude nearly doubled, from 0.556 to 1.056 V/A, while Ipp changed only from 7.022 to 7.043 mA.

At 7.5 kHz, magnitude stayed relatively close while phase moved approximately 17°.

At 10 kHz, both magnitude and phase changed.

There is no common monotonic direction with elapsed time. Therefore a simple warm-up drift does not explain the observed variation.

The current-reference channel remains stable; the uncertainty is concentrated on the small CH2 coherent component.

---

## 10. What the averaged frequency response does and does not mean

Using the main repeated sets:

- 1 kHz complex average ≈ **0.886 ∠ -6.5° V/A**;
- 5 kHz complex average ≈ **0.871 ∠ -23.3° V/A**;
- 7.5 kHz complex average ≈ **0.735 ∠ -36.5° V/A**;
- 10 kHz complex average ≈ **0.803 ∠ -50.3° V/A**.

The phase averages form a broadly smooth progression with frequency.

However, the interleaved experiment demonstrates that individual complex estimates can move strongly even when primary current remains stable. The CH2 residual is typically approximately 13–15 mV RMS while the wanted coherent CH2 component is only approximately 4–7 mVpp.

Therefore:

1. the repeated averages are useful descriptive evidence;
2. they are **not accepted as a precision AC calibration**;
3. a fitted physical pole/delay model shall not be frozen from these data;
4. the apparent 7.5 kHz magnitude dip shall not be labeled a real notch;
5. the raw-sensor fixture has reached an SNR/measurement-repeatability limit.

The DC calibration remains separately established as:

`VOUT = 0.46910 + 0.74472·I`

with inverse:

`I = (VOUT - 0.46910)/0.74472`

and R² approximately 0.999997 over the low-current calibration interval. The dynamic values above do not replace that DC calibration.

---

## 11. Why the 4.7 nF capacitor remains provisional

The corrected-ground experiments established an important qualitative fact: increasing FILTER capacitance can reduce broadband CH2 variation. A 100 nF diagnostic capacitor reduced broadband output noise strongly, but its simple estimated pole is around 0.88 kHz and therefore makes it unsuitable for a DC–10 kHz Rev-1 diagnostic band.

The 4.7 nF added capacitor gives a simple estimated corner near 15.5 kHz. It therefore represents a more defensible compromise for continued development:

- meaningful noise reduction is possible;
- 10 kHz remains below the simple estimated corner;
- unlike 10 nF, 22 nF, or 100 nF, it does not intentionally place the simple FILTER corner inside the formal diagnostic band.

This is not a final selection. Final acceptance belongs to the complete AFE/ADC verification.

---

## 12. Measurement lessons that become engineering rules

1. **Physical package orientation must be explicit.** For PDIP devices, use notch/dot plus physical position and pin number together.
2. **Do not diagnose a floating/unpowered op-amp as if it were in normal closed-loop operation.**
3. **Continuity/resistance mode is used only on an unpowered circuit.**
4. **Raw Vpp is not the coherent target-frequency amplitude.**
5. **Scope automatic frequency readouts can be wrong for distorted/noisy waveforms; use the sampled waveform/spectrum when needed.**
6. **Acquisition settings must be chosen for samples per cycle, then verified from exported Δt.**
7. **Same-node controls are mandatory before interpreting inter-channel phase.**
8. **Open-primary controls are required before attributing small coherent CH2 signals to current sensing.**
9. **More repeated captures cannot overcome a fundamental SNR limitation indefinitely.**
10. **FILTER capacitance is a bandwidth/noise tradeoff, not a “make the trace smooth” control.**

---

## 13. Closure decision

The present raw-ACS724 dynamic campaign is sufficiently mature to close as a Stage-B characterization activity.

Established:

- corrected MCP6022 fixture operation;
- stable primary-current stimulus;
- physically verified FILTER-to-GND connection;
- provisional 4.7 nF FILTER candidate;
- coherent-fit analysis method;
- valid acquisition settings through 10 kHz;
- repeatable one-stored-sample CH2 CSV timing skew;
- negligible direct stimulus-generator feedthrough relative to current-on response;
- strong evidence that CH2 low SNR, not CH1 stimulus instability, is the dominant limitation in precise AC transfer estimation.

Not established:

- final ACS724 AC sensitivity;
- exact intrinsic ACS724 phase response;
- unique pole/delay model;
- final FILTER value;
- final measurement-chain bandwidth;
- final noise performance at the ADC input.

---

## 14. Next development step — Analog Front End bring-up

The next Stage-B task is **AFE bring-up and independent validation**.

The frozen Rev-1 architecture already includes an MCP6022-based fourth-order approximately 15 kHz Butterworth AFE. The reason to proceed now is directly supported by the raw-sensor experiment:

- the sensor's wanted dynamic signal is only a few millivolts peak-to-peak;
- CH2 residual is much larger than the coherent signal;
- the final system must present a controlled, conditioned signal to the RA4M1 ADC;
- the AFE is the designed subsystem responsible for signal conditioning and anti-alias behavior before deterministic 100 kS/s acquisition.

The AFE shall first be tested **independently of the ACS724** with a known input signal. The first objectives are:

1. verify supply and DC operating points;
2. verify that each stage is stable and not saturated;
3. verify intended gain;
4. verify the filter response against the Stage-A design;
5. verify no clipping over the planned input range;
6. only then connect ACS724 OUT → AFE → scope/ADC.

This separation prevents sensor noise, AFE errors, and ADC/acquisition errors from being mixed into one troubleshooting problem.

The next chat should therefore begin from **AFE schematic/design review and bench bring-up planning**, not from another raw ACS724 frequency sweep.
