# Phase 11 — Calibration and PC/MATLAB Analysis Design

**Status:** In development  
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

## Phase 11 design topics remaining

- calibration ownership/storage/application and traceability;
- PC/MATLAB analysis responsibilities and reproducible data products;
- relationship between calibration data and the healthy diagnostic reference.

## Planned output

Phase 11 shall close with a calibration and PC-analysis architecture that Phase 12 can integrate into the Rev-1 build specification and Stage B can implement without redefining the measurement model.

No Phase 11 engineering decision is baselined until explicitly approved.
