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

## Phase 11 design topics

The phase will resolve the minimum product-defining choices for:

- calibration model and parameters;
- calibration ownership/storage/application and traceability;
- PC/MATLAB analysis responsibilities and reproducible data products;
- relationship between calibration data and the healthy diagnostic reference.

## Planned output

Phase 11 shall close with a calibration and PC-analysis architecture that Phase 12 can integrate into the Rev-1 build specification and Stage B can implement without redefining the measurement model.

No Phase 11 engineering decision is baselined until explicitly approved.
