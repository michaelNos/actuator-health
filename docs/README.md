# Engineering Documentation

This directory is the authoritative engineering record for the Actuator Health Monitoring System.

## Convention

Each development phase has one numbered Markdown document:

- `01-system-requirements.md`
- `02-system-architecture.md`
- `03-acs724-sensor-characterization.md`
- and so on.

Markdown is used as the source of truth because engineering changes remain readable and reviewable in Git diffs and pull requests. Word/PDF documents may be generated later as deliverables, but they should not become a second competing source of truth.

## Current phase status

| Phase | Topic | Status |
|---|---|---|
| 1 | System Requirements | Complete / baselined |
| 2 | System Architecture | Complete / baselined |
| 3 | ACS724 Sensor Theory and Characterization | Next |
| 4 | Measurement Error Budget | Planned |
| 5 | Analog Front End | Planned |
| 6 | Deterministic ADC Acquisition | Planned |
| 7 | Calibration | Planned |
| 8 | Communication | Planned |
| 9 | Power Design | Planned |
| 10 | Noise / EMC Experiments | Planned |
| 11 | Validation Plan | Planned |
| 12 | MATLAB / Signal Analysis | Planned |
| 13 | Robust Prototype | Planned |
| 14 | Final Documentation / Demonstration | Planned |

## Engineering record rule

Where practical, work should remain traceable as:

`Requirement → Architecture → Design → Implementation → Verification → Evidence → PASS/FAIL`

Only explicitly approved decisions are baselined. Unknown values remain TBD until calculated, measured, or otherwise justified.
