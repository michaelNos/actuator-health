# Phase 11 — Calibration and PC/MATLAB Analysis Design

**Status:** Design complete  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 11 defines the Rev-1 calibration architecture and the role of the PC/MATLAB environment in calibration, waveform analysis, characterization and diagnostic development.

This phase defines what must be calibrated, how calibration data is conceptually represented/applied, and which analysis responsibilities belong on the PC. Exact scripts, file formats, fitting commands, plotting details and laboratory procedures remain Stage B work.

## Accepted design inputs

- system current-accuracy target: **≤ ±0.10 A after calibration**; stretch target **±0.05 A**;
- reported-current resolution target: **≤10 mA**;
- calibrated current range: **0–5 A**;
- nominal ACS724 model: `VOUT = Voffset + S × I`, with nominal `Voffset ≈ 0.5 V` and `S ≈ 0.8 V/A` at nominal 5 V;
- offset and sensitivity are calibration parameters, not exact universal constants;
- measurement/reference rail behavior affects the ratiometric sensor conversion;
- deterministic acquisition baseline: **100 kS/s**, diagnostic band **DC–10 kHz**;
- firmware produces calibrated-current data, features and validity/health state;
- USB telemetry plus on-demand waveform capture is the accepted Rev-1 PC interface;
- healthy motor current-signature reference data is deliberately established during characterization and frozen during ordinary monitoring.

## 11.1 — Calibration model

### CAL-001 — Two-parameter linear current calibration

**Status:** Accepted

Rev-1 shall use a measured two-parameter linear calibration as the baseline current-conversion model rather than relying on nominal ACS724 offset and sensitivity values.

The calibrated relationship may be represented as:

`I = aV + b`

or equivalently by measured `Voffset` and sensitivity `S` in:

`I = (V - Voffset) / S`

Calibration shall determine both zero-current offset and gain/sensitivity from measured reference-current data spanning the intended **0–5 A** range.

The calibration shall use multiple known current points rather than a single-point correction. Residual error across the range shall be evaluated against the accepted **≤ ±0.10 A** system accuracy requirement.

If measured residuals demonstrate that a linear model cannot satisfy the requirement, a more appropriate compensation model may be introduced based on evidence. Rev-1 shall not adopt higher-order or temperature-dependent compensation merely by assumption.

Temperature compensation remains `TBD` unless implementation measurements demonstrate that temperature-dependent residual error is significant enough to threaten the accuracy requirement.

### Rationale

The ACS724's nominal offset and sensitivity are not exact device-specific calibration constants. Measuring both offset and gain corrects the dominant linear errors while preserving a simple, auditable conversion model. Evaluating residuals across the full calibrated range ensures that calibration performance is demonstrated rather than inferred from nominal sensor specifications.

## 11.2 — Calibration ownership and traceability

### CAL-002 — Versioned, traceable active calibration record

**Status:** Accepted

Rev-1 shall represent calibration as an explicit, versioned record rather than as undocumented constants embedded in firmware.

The calibration record shall contain, as applicable:

- the active offset/gain coefficients or equivalent `Voffset`/`S` parameters;
- a calibration version or unique identity;
- date/time or revision identity sufficient to trace when the calibration was established;
- relevant measurement/reference conditions needed to interpret the calibration correctly;
- validity/status information indicating whether the record is accepted for measurement use.

Firmware shall apply one identifiable **active calibration set** when converting measurements into current-domain data. Data exported to the PC/MATLAB environment shall retain enough calibration identity to determine which calibration produced the reported current values.

A missing, invalid or incompatible calibration shall propagate through the Phase 7 measurement-pipeline health mechanism rather than silently reverting to nominal constants while claiming calibrated accuracy.

The exact nonvolatile storage structure, serialization format, host-file representation and update mechanism are Stage B implementation choices.

### Rationale

Calibration is part of the measurement system, not merely a mathematical constant. Versioning and traceability make results reproducible, prevent ambiguity after recalibration, and allow captured data to be associated with the exact conversion parameters that generated it.

## 11.3 — PC/MATLAB analysis role

### CAL-003 — MATLAB as offline engineering and characterization environment

**Status:** Accepted

MATLAB shall serve as the Rev-1 **offline engineering, characterization, calibration and diagnostic-development environment** rather than as a required component of real-time monitoring.

The PC/MATLAB environment shall support, as applicable:

- calibration fitting and residual/error analysis;
- current-waveform visualization and inspection;
- FFT/spectral and band-energy analysis;
- comparison of healthy and abnormal motor behavior;
- development and tuning of diagnostic thresholds/features;
- generation of engineering verification plots and analysis results.

The MCU remains responsible for real-time acquisition, calibrated-current processing, health-state handling and deployed diagnostic logic. Loss or absence of the MATLAB connection shall not prevent the embedded monitor from performing its designed real-time functions.

Datasets retained for engineering analysis shall include enough metadata to reproduce their interpretation, including as applicable sample-rate/timing identity, calibration identity, measurement validity/health information and test/dataset identity. Exact file format, script structure, plotting conventions and import/export implementation remain Stage B choices.

### Rationale

Separating embedded monitoring from engineering analysis keeps the deployed Rev-1 architecture autonomous while allowing MATLAB to use its stronger visualization, fitting and signal-analysis capabilities during development and verification. Metadata-bearing datasets also make later comparisons and calibration results traceable rather than dependent on undocumented laboratory context.

## 11.4 — Measurement calibration versus healthy diagnostic reference

### CAL-004 — Separate, versioned calibration and healthy-reference datasets

**Status:** Accepted

Rev-1 shall treat **measurement calibration** and the **healthy diagnostic reference** as separate configuration datasets because they represent different engineering functions.

Measurement calibration converts the electrical measurement into an accurate physical current quantity:

`ADC/voltage measurement → calibrated amperes`

The healthy diagnostic reference describes expected current behavior for a known-good motor/operating condition:

`calibrated current/features → condition comparison`

Recalibrating the measurement chain shall therefore not automatically redefine healthy motor behavior. Conversely, establishing a new healthy reference shall not alter the electrical current-conversion coefficients.

Both datasets shall be independently identifiable/versioned. The healthy-reference dataset shall retain compatibility information identifying the measurement calibration and relevant processing/configuration context under which it was established.

After a material calibration or signal-processing change, the existing healthy reference shall be checked for compatibility. If the change alters the numerical current/features sufficiently that the old reference is no longer valid, a new healthy reference shall be deliberately characterized rather than silently reusing or automatically adapting the old one.

Exact compatibility metadata and storage format remain Stage B implementation choices.

### Rationale

Conflating calibration with healthy behavior would make measurement corrections unintentionally redefine the diagnostic baseline. Keeping them separate preserves traceability and ensures that both measurement accuracy and condition-monitoring references change only through deliberate engineering actions.

## Phase 11 design status

CAL-001 through CAL-004 define the Rev-1 calibration and PC-analysis architecture:

`raw measurement → versioned calibration → calibrated current/features → versioned healthy reference → diagnostics`

MATLAB supports calibration, characterization and diagnostic development, while the MCU remains responsible for deployed real-time monitoring.

## Verification handoff

Implementation/verification shall demonstrate that:

- the measured linear calibration is evaluated across the 0–5 A range against the ≤ ±0.10 A requirement;
- calibration identity and validity are traceable through exported measurement data;
- invalid/missing calibration cannot silently produce data represented as calibrated;
- MATLAB can reproduce calibration, waveform and spectral analyses from metadata-bearing datasets;
- real-time monitoring remains functional without MATLAB connected;
- healthy-reference data is distinguishable from measurement calibration and compatibility is checked after material calibration/processing changes.

## Planned output

Phase 11 closes with a calibration and PC-analysis architecture that Phase 12 can integrate into the Rev-1 build specification and Stage B can implement without redefining the measurement model.
