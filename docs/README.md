# Engineering Documentation

This directory is the authoritative engineering record for the Actuator Health Monitoring System.

## Convention

Each development phase has one numbered Markdown document. Markdown is the source of truth because engineering changes remain readable and reviewable in Git diffs and pull requests. Word/PDF documents may be generated later as deliverables, but they shall not become a competing source of truth.

## DEV-001 — Design-before-implementation workflow

**Status:** Accepted

Rev-1 of the Actuator Health Monitoring System shall be fully specified and baselined at product and subsystem level before physical implementation begins.

The design stage shall establish requirements, architecture, subsystem designs, interfaces, calculations, component selections, calibration strategy, firmware/software architecture, diagnostic strategy, BOM/build information, and verification procedures.

Physical measurements and implementation-dependent results may remain `TBD` during design where they cannot legitimately be known before hardware exists.

After the Rev-1 design baseline is complete, implementation shall proceed from the documented design. Verification shall then populate the planned tests with measured results and identify any necessary deviations or redesign.

### Consequence for phase closure

A design phase does **not** require execution of future hardware tests before it can close. It must instead provide a sufficiently complete design baseline and a defined verification method so later implementation can be performed and checked against the documentation.

Detailed test steps that do not change product design should be consolidated into verification procedures rather than promoted into separate product decisions.

## Rev-1 development stages

### Stage A — Product definition and detailed design

| Phase | Topic | Status |
|---|---|---|
| 1 | System Requirements | Complete / baselined |
| 2 | System Architecture | Complete / baselined |
| 3 | ACS724 Sensor Design and Verification Plan | Design complete / ready for review |
| 4 | Measurement-Chain Requirements and Error-Budget Allocation | Planned |
| 5 | Analog Front End and Anti-Alias Filter Design | Planned |
| 6 | ADC and Deterministic Acquisition Design | Planned |
| 7 | MCU Firmware and Signal-Processing Architecture | Planned |
| 8 | Diagnostics / Health-Monitoring Logic | Planned |
| 9 | Communication Interface Design | Planned |
| 10 | Power and Protection Design | Planned |
| 11 | Calibration and PC/MATLAB Analysis Design | Planned |
| 12 | System Integration, Wiring, BOM and Build Specification | Planned |
| 13 | System Verification and Acceptance Plan | Planned |
| 14 | Rev-1 Design Review and Design Freeze | Planned |

### Stage B — Implementation

| Phase | Topic | Status |
|---|---|---|
| 15 | Rev-1 Hardware / Firmware / Software Implementation | Planned after design freeze |

### Stage C — Verification and finalization

| Phase | Topic | Status |
|---|---|---|
| 16 | Subsystem Verification, Calibration and System Validation | Planned after implementation |
| 17 | Final Results, Limitations and Product Documentation | Planned after validation |

The ordering of future design phases may be refined only through an explicit engineering-documentation update; implementation shall not begin merely because an individual subsystem design is available.

## Engineering record rule

Where practical, work remains traceable as:

`Requirement → Architecture → Design → Implementation → Verification → Evidence → PASS/FAIL`

Only explicitly approved decisions are baselined. Unknown values remain `TBD` until calculated, measured, or otherwise justified.

One engineering phase normally uses one branch and one pull request. During design, product decisions are committed as approved; verification details may be consolidated when they are procedural rather than independent design choices.
