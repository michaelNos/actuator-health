# Phase 14 — Rev-1 Design Freeze and Implementation Handoff

**Status:** In development  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 14 closes Stage A design work by freezing the accepted Rev-1 product baseline and defining the controlled handoff into implementation, calibration and physical verification.

This phase does not redesign accepted subsystems and does not claim that the physical prototype has passed verification. Its purpose is to establish exactly what is frozen, what remains an implementation choice, which measured TBDs must be resolved during Stage B/C, and how changes after freeze are controlled.

## Accepted baseline entering Phase 14

Phases 1–13 are merged and constitute the authoritative Rev-1 design/verification baseline. The integrated product includes:

- Philips/Saeco 24 VDC brew-group gearmotor as Rev-1 actuator;
- Pololu #4048 / ACS724LLCTR-05AU current sensor;
- calibrated 0–5 A unidirectional measurement range;
- MCP6022-based fourth-order approximately 15 kHz Butterworth AFE;
- UNO R4 WiFi / Renesas RA4M1 deterministic 100 kS/s acquisition;
- DC–10 kHz diagnostic band;
- ≤ ±0.10 A mandatory calibrated system-current accuracy target;
- ≤10 mA usable reported-current resolution target;
- current-domain startup/load/ripple/overload/stall/anomaly diagnostics;
- USB PC/MATLAB engineering interface;
- bench-PSU current limiting plus series fuse protection architecture;
- versioned build/calibration/configuration traceability;
- requirement-driven verification and acceptance plan.

## 14.1 — Authoritative Rev-1 design-freeze baseline

### FRZ-001 — Merged Phases 1–13 define the frozen Stage A product baseline

**Status:** Accepted

The merged contents of **Phases 1–13** constitute the authoritative Rev-1 Stage A baseline for requirements, architecture, subsystem design, integration and verification acceptance.

After Phase 14 closes, the following categories are considered frozen product-level decisions unless changed through explicit engineering change control:

- system requirements and accepted performance targets;
- sensor/measurement architecture and calibrated 0–5 A validity range;
- AFE topology and accepted component realization;
- ADC/sampling architecture and deterministic 100 kS/s baseline;
- firmware/signal-processing responsibilities and validity propagation;
- diagnostic architecture and fault/condition model;
- communication architecture and PC/MATLAB boundary;
- power/protection architecture;
- calibration/healthy-reference architecture;
- integrated wiring/build topology and physical partitioning;
- verification methods and mandatory acceptance criteria.

The freeze does **not** mean that every implementation value is already known. Items deliberately deferred to measurement, tuning or implementation remain valid Stage B/C outputs rather than unclosed Stage A design gaps. Examples include motor characterization currents, actual sensor/AFE/ADC behavior, calibration coefficients, diagnostic thresholds/persistence values, healthy-reference values, fuse rating, exact buffer sizes, DSP window/FFT details and measured timing/noise results.

Stage B may choose or tune implementation details only within the boundaries already permitted by the frozen design. Such choices shall not silently change a product requirement, architecture boundary, accepted interface, safety/protection assumption or verification criterion.

If implementation or verification demonstrates that a frozen decision is incorrect, infeasible or materially inadequate, the result shall be retained and the baseline shall be revised explicitly through controlled engineering change. The implementation shall not simply diverge from the documentation without recording that change.

Therefore:

`Stage A design freeze ≠ immutable forever`

but:

`material post-freeze change → explicit engineering revision + traceability`

### Rationale

A design freeze creates a stable reference from which the physical implementation can be built and verified. Allowing legitimate measured/implementation parameters to remain open prevents false precision, while requiring controlled changes prevents the prototype from evolving into a different undocumented product during debugging.

## Phase 14 work packages

Phase 14 will establish:

1. authoritative design-freeze baseline and configuration boundary — **FRZ-001 accepted**;
2. frozen versus implementation-selectable items;
3. measured-TBD register and closure ownership;
4. Stage B implementation sequence and entry criteria;
5. Stage C verification sequence and evidence handoff;
6. engineering-change control after design freeze;
7. implementation readiness / procurement-blocker review;
8. future-extension boundary, including FPGA/Verilog work outside Rev-1;
9. final Stage A completeness audit and handoff decision.

Additional work packages may be introduced only if the freeze audit exposes a genuine implementation-blocking gap.

## Completion criterion

Phase 14 is complete when the Rev-1 design baseline is explicitly frozen, remaining measured/implementation TBDs are controlled and assigned to later work, and implementation can begin without silently redefining accepted product requirements or architecture.
