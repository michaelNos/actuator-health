# Phase 4 — Measurement-Chain Requirements and Error-Budget Allocation

**Status:** In development  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 4 converts the accepted system requirements and ACS724 sensor design baseline into quantitative measurement-chain constraints for the later Analog Front End and ADC design phases.

This phase defines product-level requirements for signal range, accuracy allocation, useful resolution, bandwidth/anti-alias expectations, and measurement-valid versus electrical-survival behavior. It does **not** design the complete AFE, select final filter component values, configure ADC registers, or execute hardware measurements.

Under **DEV-001**, hardware-dependent quantities remain `TBD` where they cannot legitimately be established before implementation and verification.

## Accepted design inputs

The following inputs are already baselined by Phases 1–3 and are not reopened by Phase 4 unless a contradiction is found:

- valid Rev-1 current measurement range: **0 A to 5 A**, unidirectional;
- nominal ACS724 transfer at 5 V: `VOUT = 0.5 V + 0.8 V/A × I`;
- nominal sensor output span over the valid range: approximately **0.5 V to 4.5 V**;
- sensor output is supply-dependent/ratiometric and actual offset/sensitivity are calibration parameters;
- required diagnostic signal band: **DC to 10 kHz**;
- nominal acquisition target: **100 kS/s**;
- Nyquist frequency at 100 kS/s: **50 kHz**;
- system current-accuracy target after calibration: **≤ ±0.10 A**;
- stretch current-accuracy target: **±0.05 A**;
- reported current-resolution target: **≤ 10 mA**;
- the stock ACS724 carrier bandwidth is approximately **90 kHz**, so the AFE must provide deliberate anti-alias filtering;
- values outside 0–5 A shall not be treated as calibrated valid measurements merely because the sensor or downstream electronics may still produce a voltage.

## 4.1 — Measurement-chain signal range, headroom and overrange

### MEAS-001 — Preserve the native ACS724 signal span

**Status:** Accepted

Rev-1 shall preserve approximately unity DC/passband gain from the ACS724 through the Analog Front End rather than deliberately amplifying or compressing the sensor output solely to occupy more ADC range.

The nominal valid sensor range therefore remains approximately:

- `0 A → 0.5 V`;
- `5 A → 4.5 V`.

For a nominal 0–5 V ADC input range this leaves approximately **0.5 V nominal headroom at each rail**.

The later AFE/ADC design shall ensure that expected sensor, supply, AFE and component variation does not cause clipping within the valid **0–5 A** measurement range.

Values corresponding to current outside the calibrated 0–5 A range may still produce an ADC code, but shall be treated as **overrange / invalid measurement**, not as valid extrapolated current.

Near-rail or saturated ADC conditions shall be detectable by the later firmware as measurement overrange/saturation.

Electrical survival remains distinct from measurement validity. The later AFE/protection design shall prevent plausible abnormal sensor/transient voltages from damaging the ADC input, but exact clamp/protection circuitry is deferred to the appropriate later design phases.

Measured `Voffset`, sensitivity and practical rail margin remain verification-stage quantities and shall not be invented during Phase 4.

### Rationale

The native ACS724 span already uses approximately 4 V of a nominal 5 V ADC range. Additional analog scaling would provide limited resolution benefit while adding gain/offset error and reducing headroom. Preserving the native span therefore gives a simpler and more robust Rev-1 measurement chain.

## Phase 4 design topics remaining

### 4.2 — Accuracy budget allocation

Allocate the **±0.10 A** system requirement across the major measurement-chain contributors without pretending that hardware-dependent sensor, temperature, noise, or calibration residuals are already known.

Candidate contributors include:

- residual sensor error after calibration;
- AFE gain/offset error;
- ADC/reference error;
- noise;
- supply/ratiometric effects;
- temperature and other residual effects.

**Status:** To be decided.

### 4.3 — Resolution and useful ADC performance

Translate the **≤10 mA** reported-current resolution target into voltage-domain and ADC-domain constraints while keeping resolution distinct from accuracy and nominal ADC bit depth distinct from effective usable resolution.

Nominal sensor sensitivity gives:

`10 mA × 0.8 V/A = 8 mV`

**Status:** To be decided.

### 4.4 — Bandwidth and anti-alias requirement handoff

Translate the **DC–10 kHz** diagnostic band and **100 kS/s** acquisition target into quantitative requirements that Phase 5 can use to select an anti-alias filter topology and cutoff.

Nyquist alone shall not be treated as sufficient anti-alias protection.

**Status:** To be decided.

## Planned Phase 4 output

Phase 4 will close with a compact measurement-chain specification containing:

- ADC-facing signal-range/headroom requirement;
- quantitative current and voltage error-budget allocation;
- minimum useful resolution/noise requirement;
- bandwidth and anti-alias handoff to Phase 5;
- overrange/rail behavior requirements;
- explicit `TBD` items to be measured later;
- traceability to the accepted Phase 1–3 inputs.

Only explicitly approved Phase 4 engineering decisions are baselined.
