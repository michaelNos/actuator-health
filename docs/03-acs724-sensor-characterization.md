# Phase 3 — ACS724 Sensor Design and Verification Plan

**Status:** Design complete / ready for review  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 3 defines the Rev-1 current-sensor subsystem around the Pololu #4048 carrier using the Allegro ACS724LLCTR-05AU Hall-effect current-sensor IC.

Under the accepted **DEV-001 design-before-implementation workflow**, this phase establishes the sensor design baseline, downstream interface assumptions, error model, calibration intent, and verification plan before physical implementation begins.

Measured characterization results are intentionally not required for design-stage closure. Values that can only be established on real hardware remain `TBD` and shall be populated during the later implementation and verification stages.

## 3.1 — Sensor design baseline

### Sensing principle and system boundary

Rev-1 uses the selected ACS724 as an **in-series Hall-effect current transducer**. Actuator current flows through the sensor primary conductor; low-voltage Hall sensing and internal signal conditioning convert the current-generated magnetic field into an analog output voltage.

The primary current path and low-voltage sensing electronics are galvanically isolated through the sensor architecture. The sensor is inserted in series with the actuator-current path; it is not an external clamp around an untouched conductor.

This baseline originates from **SENS-001**.

### Exact sensor variant, range and polarity

Rev-1 uses the **ACS724LLCTR-05AU** on the Pololu #4048 carrier within its specified **0 A to 5 A unidirectional measurement range**.

At nominal `VCC = 5 V`:

- nominal zero-current output: `Voffset = 0.5 V`;
- nominal sensitivity: `S = 0.8 V/A`;
- nominal transfer model: `VOUT = Voffset + S × I`;
- nominal inverse model: `I = (VOUT - Voffset) / S`.

The nominal output span implied by the accepted transfer model is therefore:

- at `I = 0 A`: `VOUT = 0.5 V`;
- at `I = 5 A`: `VOUT = 4.5 V`.

The 05AU range is one-polarity, not "constant DC". Startup transients, commutation ripple, load variation and other time-varying components may exist while current remains positive. Applications requiring accurate positive and negative current measurement require an appropriate bidirectional sensing arrangement.

Values outside 0 A to 5 A shall not be treated as calibrated valid measurements merely because an output voltage may still be produced.

This baseline originates from **SENS-002** and **SENS-008**.

### Sensor supply dependence

The ACS724 output is supply-dependent/ratiometric. The nominal `0.5 V` zero-current output and `0.8 V/A` sensitivity are values associated with nominal `5 V` operation and shall not be treated as supply-independent exact constants.

Characterization and calibration shall therefore record actual sensor `VCC`; the design shall not assume an ideal fixed `5.000 V` supply when evaluating measurement accuracy.

The selected Pololu carrier is intended for the sensor's 5 V-class supply range; Rev-1 uses nominal 5 V operation. The exact runtime compensation/reference strategy belongs to the later measurement-chain/ADC design.

This baseline originates from **SENS-003** and is carried into the later error budget.

### Bandwidth and FILTER configuration

Initial Rev-1 design uses the Pololu #4048 carrier in its **stock FILTER configuration**, including the existing **1 nF FILTER capacitor**, giving an approximate assembled-carrier bandwidth of **90 kHz**. The bare ACS724 IC has a higher vendor bandwidth, so bare-IC and carrier bandwidth shall not be conflated.

No additional FILTER capacitance is introduced in the sensor design baseline.

The sensor bandwidth is substantially above the accepted **DC to 10 kHz diagnostic signal band**. The stock sensor FILTER network is therefore **not** treated as the complete ADC anti-alias filter. Deliberate anti-alias filtering remains an Analog Front End responsibility for the later `100 kS/s` acquisition chain.

Any future change to the sensor FILTER configuration shall require verification that the DC to 10 kHz diagnostic band is preserved.

This baseline originates from **SENS-004** and **SENS-010**.

### Primary current-path insertion effect

The ACS724 primary conductor has nominal resistance of approximately **1.2 mΩ** and is treated as a real series insertion effect:

`Vdrop = I × Rprimary`

`Ploss = I² × Rprimary`

The low resistance minimizes disturbance of the actuator-current path but does not make the sensor electrically invisible.

This baseline originates from **SENS-005**.

### Isolation interpretation and laboratory safety boundary

The ACS724's **2400 V RMS dielectric-strength figure is a short-duration insulation test rating**, not a continuous working voltage.

Continuous working-voltage limits, dielectric-test voltage, surge capability, creepage and clearance are distinct quantities and shall not be substituted for one another.

For Rev-1, the Pololu carrier remains restricted to the established **low-voltage laboratory scope of 24 V or less**. IC-level isolation ratings do not justify connecting the hobby carrier, Arduino, breadboard, ordinary oscilloscope probes or other laboratory hardware directly to industrial mains or a 400 V motor circuit.

Future industrial scaling requires an appropriately rated complete sensing and installation solution, not reuse of the hobby carrier merely because the IC contains an isolation barrier.

This baseline originates from **SENS-006**.

## 3.2 — Error model and calibration intent

Nominal sensor values are not exact. Phase 3 distinguishes the following sensor-level contributors:

1. offset error;
2. sensitivity/gain error;
3. supply-dependent variation;
4. temperature-dependent variation;
5. output noise;
6. frequency/dynamic-response error;
7. non-ideal total output behaviour specified by the sensor vendor.

Actual zero-current offset and sensitivity shall be experimentally characterized and used as calibration parameters where practical. Calibration may reduce systematic offset/gain error but shall not be assumed to remove random noise, temperature drift outside the calibrated condition, or finite-bandwidth effects.

The Phase 1 **±0.10 A current-accuracy target** is a system requirement. It is not considered demonstrated by nominal sensor values alone and shall not be assigned entirely to the ACS724. The final allocation and compliance assessment belong to the later measurement-chain error budget including sensor, AFE, ADC/reference, calibration and reference-instrument contributions.

This baseline originates from **SENS-007** and **SENS-009**.

## 3.3 — Handoff to downstream design phases

The following Phase 3 outputs are design inputs to the later AFE, ADC, calibration and system-integration phases:

| Quantity / interface | Rev-1 Phase 3 baseline | Downstream consequence |
|---|---|---|
| Measured quantity | Primary actuator current | Sensor remains in series with actuator path |
| Valid measurement range | 0 A to 5 A, unidirectional | Later electronics shall not claim valid bipolar/current-overrange measurement |
| Nominal sensor supply | 5 V | Supply/reference behaviour must be included in measurement-chain design |
| Nominal transfer | `VOUT = 0.5 V + 0.8 V/A × I` at 5 V | AFE/ADC shall accommodate nominal 0.5 V to 4.5 V sensor span |
| Diagnostic signal band | DC to 10 kHz | AFE shall preserve this band |
| Carrier bandwidth | approx. 90 kHz, stock 1 nF FILTER | AFE must provide deliberate anti-alias filtering before 100 kS/s ADC acquisition |
| Primary resistance | approx. 1.2 mΩ | Include insertion drop/heating where relevant |
| Isolation use | Low-voltage Rev-1 laboratory system | Do not derive industrial-mains system safety from IC rating alone |
| Calibration parameters | `Voffset`, `S` | Later calibration and firmware/software conversion shall retain them explicitly |

Exact final wiring, connector allocation, ADC-reference topology and complete build instructions are **not missing Phase 3 sensor decisions**; they are intentionally resolved in the later integration/build-specification phases after the downstream electronics are designed.

## 3.4 — Verification plan to execute after design freeze

The following verification plan consolidates the previously accepted characterization-method decisions. These controls remain traceable but are treated as a coherent verification procedure rather than as separate pieces of product functionality.

### Static characterization

The sensor shall later be characterized using a controlled low-voltage DC current path independent of the actuator motor.

For valid characterization points:

- bench-PSU current limiting is configured before output enable;
- an independent current-reference method is used rather than assuming the PSU display is exact;
- zero current and multiple safe points across the usable 0 A to 5 A range are recorded where the available load/reference hardware permits;
- the motor is not used as the primary calibration load;
- `IREF`, `VOUT`, actual `VCC`, approximate temperature and relevant PSU/test conditions are recorded;
- multiple points are used to derive measured `Voffset`, sensitivity `S`, and linear-model residuals;
- ascending/descending sweeps are used where practical to expose heating, drift, repeatability or hysteresis-like effects.

The exact high-current load remains `TBD` until selected. Existing 1/4 W resistor assortments shall not be used as multi-ampere loads. The multi-ampere primary path shall use suitable conductors/connections rather than a solderless breadboard.

This plan consolidates **SENS-011**, **SENS-012** and the relevant readiness requirements of **SENS-018**.

### Zero-current offset, supply comparison and noise

The first sensor characterization executed after implementation shall be the zero-primary-current test.

The sensor electronics are powered while the primary path carries no current. The test records repeated `VOUT`, actual `VCC` at the carrier, approximate temperature and relevant configuration state.

The mean output is treated as measured zero-current offset under the recorded conditions. Short-term variation around the mean is treated separately as noise.

Initial supply comparison uses:

`A1 = bench 5 V supply → B = Arduino UNO R4 WiFi 5 V rail → A2 = bench 5 V supply`

The supply source is the intentionally changed variable. Sensor, zero-current condition, measurement points, instruments, probe configuration and relevant oscilloscope settings are held constant where practical. Unavoidable wiring, grounding or USB differences are recorded as possible confounding variables.

The measurement-system noise floor is measured using the same oscilloscope channel/probe and comparable settings with the probe input referenced to ground before observed variation is attributed to the sensor.

Primary quantitative noise metric:

`standard deviation / equivalent RMS-type variation after mean removal`

Peak-to-peak may be retained as descriptive evidence but is not the sole statistical noise value. Where valid sampled data and characterized sensitivity are available:

`σI = σV / S`

Independent RMS-type noise contributions may only be separated mathematically when the assumptions of the combination model are justified; peak-to-peak values shall not simply be subtracted.

The same acquisition method, observation duration and sample count are used across A1/B/A2 and the noise-floor control where practical. Exact numerical record length, sample rate and observation duration remain `TBD` until the real DOS1102S data path is verified.

This plan consolidates **SENS-013**, **SENS-019**, and **SENS-020 through SENS-025**.

### Dynamic response and educational bandwidth verification

Later dynamic characterization shall verify the sensor response through the formal **DC to 10 kHz diagnostic band** using controlled periodic primary-current stimulus and an independent representation of actual current.

Transfer magnitude is evaluated from:

`A(f) = ACS724 output AC amplitude / reference-current AC amplitude`

The result is normalized to a low-frequency reference. Experimental bandwidth is estimated where the normalized amplitude approaches:

`0.707 ≈ -3 dB`

In addition to the formal 10 kHz requirement-oriented verification, an educational extended sweep shall, where practical, continue toward and beyond the Pololu carrier's approximately 90 kHz vendor bandwidth to observe roll-off. This extended check is a study objective, not a Rev-1 acceptance requirement.

The initial method uses the DOS1102S function generator as a **small-signal source**, not as a multi-ampere power source. Actual primary current is derived from a suitable characterized reference element such as `RREF` rather than from generator settings alone.

Because the 05AU variant is unidirectional, the periodic stimulus remains positive:

`IDC > IAC`

A positive generator DC offset is preferred where the instrument supports the required settings. A bench PSU and function-generator output shall not be directly paralleled to improvise a bias source. If an external bias/driver is needed, a deliberate coupling/summing/driver network shall be designed first.

If the available small-signal current produces insufficient sensor-output SNR, a higher-current external driver shall be designed later rather than overloading the generator.

Exact `RREF`, generator settings and any higher-current driver remain `TBD` until the implementation-stage test hardware is selected and verified.

This plan consolidates **SENS-014 through SENS-017** and the dynamic-test readiness requirement of **SENS-018**.

### Data evidence and MATLAB analysis

Raw measurement evidence shall be preserved separately from interpretation.

For each controlled zero-current comparison step, the record includes at minimum:

- configuration / sequence identity;
- actual `VCC` measured at the carrier;
- zero-current `VOUT`;
- approximate temperature;
- relevant wiring/USB/grounding state;
- oscilloscope waveform observation;
- oscilloscope settings needed to interpret the observation.

Where practical, exported DOS1102S waveform samples are the primary quantitative dataset. Screenshots and built-in RMS/peak-to-peak measurements are supporting evidence and cross-checks.

**MATLAB is the primary reproducible Phase 3 analysis environment.** Original instrument exports are preserved unchanged before conversion or processing. A version-controlled workflow shall calculate the applicable mean, standard-deviation/RMS-type noise, peak-to-peak variation and equivalent current-domain noise, and may later extend to calibration fitting, residuals and frequency response.

Before exported waveform data are accepted for quantitative analysis, the actual DOS1102S export/import path is verified using a known or independently interpretable waveform. A simple function-generator sine wave is an approved procedure-level choice for this validation; it is not a separate product-design decision.

The validation establishes, where applicable:

- exported file type and structure;
- sample count;
- time/sample-interval representation;
- voltage scaling and units;
- channel identity;
- relevant acquisition metadata;
- agreement of imported quantities such as mean, peak-to-peak and frequency with the original oscilloscope observation.

Exact file format, parser/import implementation and final numerical acquisition settings remain `TBD` until the actual instrument is exercised.

This plan consolidates **SENS-022**, **SENS-026**, **SENS-027** and **SENS-028**.

## 3.5 — Verification readiness gates

Before later powered-current characterization results are accepted as engineering evidence:

1. the independent current-reference method and relevant accuracy/range are documented;
2. the static load has adequate voltage/current/power rating;
3. the dynamic current-reference element is characterized;
4. multi-ampere wiring/connections are suitable for the current;
5. oscilloscope/generator grounding relationships are understood before connection;
6. missing equipment and exact component values remain `TBD` until selected and verified.

Zero-current characterization may execute before the high-current load exists because it requires no primary current.

These gates originate from **SENS-018** and **SENS-019**.

## 3.6 — Deferred implementation/verification results

The following values are intentionally **not fabricated during design** and remain `TBD` until Stage B/C work:

- measured zero-current offset of the individual carrier;
- measured sensitivity of the individual carrier;
- static-transfer residuals / measured linearity;
- short-term output noise and equivalent current noise;
- bench-supply versus Arduino-supply comparison results;
- practical measurement-system noise floor;
- independent current-reference uncertainty;
- exact high-current static load and safe test points;
- exact dynamic `RREF` and stimulus amplitudes;
- actual DOS1102S export format, usable record length and acquisition settings;
- measured response through 10 kHz;
- educational measured -3 dB carrier bandwidth;
- any implementation-dependent temperature/heating observations.

These are **planned verification outputs**, not missing product-definition decisions.

## 3.7 — Decision traceability after consolidation

The historical accepted decisions remain traceable as follows:

| Decision IDs | Consolidated role |
|---|---|
| SENS-001 to SENS-006 | Sensor principle, exact part/range, supply/bandwidth configuration, insertion effect and isolation interpretation |
| SENS-007 to SENS-010 | Transfer/error/calibration model and FILTER role |
| SENS-011 to SENS-013 | Static and zero-current characterization method |
| SENS-014 to SENS-017 | Dynamic-response and bandwidth-verification method |
| SENS-018 to SENS-019 | Test-hardware readiness and execution order |
| SENS-020 to SENS-025 | Controlled supply/noise comparison and statistical measurement controls |
| SENS-026 to SENS-028 | Raw-data preservation, MATLAB workflow and DOS1102S import validation |

The consolidation does not revoke any accepted technical content. It reclassifies detailed characterization controls as one coherent **verification plan**, avoiding artificial inflation of product-design decisions.

## 3.8 — Phase 3 completion assessment

Phase 3 design-stage closure criteria are satisfied:

- selected sensor and sensing principle defined;
- operating range and polarity defined;
- transfer model defined;
- supply dependence defined;
- bandwidth/FILTER baseline defined;
- primary-path insertion effect defined;
- isolation interpretation and laboratory safety boundary defined;
- error/calibration model defined;
- downstream AFE/ADC handoff defined;
- static, zero-current/noise and dynamic verification methods defined;
- data-evidence and MATLAB-analysis method defined;
- implementation-dependent unknowns explicitly separated as `TBD`.

**Conclusion:** Phase 3 is complete as a **product-design phase** under DEV-001. Physical characterization will be executed later after the complete Rev-1 design has been frozen and implemented.

The next product-design phase is **Phase 4 — Measurement-Chain Requirements and Error-Budget Allocation**.
