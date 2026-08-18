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

## 14.2 — Frozen versus implementation-selectable items

### FRZ-002 — Implementation freedom is bounded by the frozen product baseline

**Status:** Accepted

Stage B shall distinguish **frozen product/design decisions** from **implementation-selectable details**.

Frozen decisions include, at minimum:

- calibrated 0–5 A unidirectional current range;
- ≤ ±0.10 A mandatory calibrated system-current accuracy target;
- ≤10 mA usable reported-current resolution target;
- DC–10 kHz diagnostic information band;
- deterministic 100 kS/s acquisition baseline;
- Pololu #4048 / ACS724LLCTR-05AU + MCP6022 + UNO R4 / RA4M1 measurement architecture;
- fourth-order approximately 15 kHz Butterworth AFE realization and accepted interface boundaries;
- current-domain diagnostic architecture, including overload ≤1 s and current-based stall/jam ≤100 ms acceptance requirements;
- USB PC/MATLAB engineering-interface architecture;
- 24 VDC Rev-1 motor and accepted power/protection philosophy;
- measurement-validity/overrange behavior and independence of protective current limiting from MCU diagnostics;
- mandatory verification and PASS criteria established through Phase 13.

Implementation-selectable or measurement-derived details include, where the earlier baseline deliberately permits them:

- exact RA4M1 ADC/timer/register configuration used to realize the frozen deterministic sampling behavior;
- exact DTC/DMA-like transfer strategy supported by the selected implementation environment;
- acquisition/buffer sizes and internal scheduling details that preserve required continuity and timing;
- FFT length, window, overlap and related DSP realization details within the accepted diagnostic architecture;
- detailed serial packet/framing realization and integrity mechanism, provided the accepted communication behavior and versioning/integrity requirements are met;
- MATLAB script/function/file organization;
- motor-derived diagnostic thresholds, persistence/tuning values and healthy-reference values;
- measured calibration coefficients and calibration identity;
- final fuse rating selected from motor characterization and current-path capability;
- exact physical component placement, routing and mechanical arrangement that preserve the frozen electrical/wiring/isolation rules.

An implementation-selectable choice becomes a controlled design change if it alters or invalidates a frozen requirement, architecture boundary, safety assumption, interface contract or acceptance criterion.

Examples:

- changing FFT length while preserving the accepted diagnostic behavior is an implementation choice;
- selecting ADC registers/timers that demonstrably produce 100 kS/s is an implementation choice;
- changing nominal sampling from 100 kS/s to 20 kS/s is **not** an implementation choice;
- tuning a stall threshold from measured motor data is an implementation choice;
- replacing the ACS724 with a different current-sensor architecture is **not** an implementation choice;
- choosing a fuse rating from measured motor current is an implementation output;
- removing the independent bench-current-limit/protection boundary is **not** an implementation choice.

The governing rule is:

`implementation freedom is permitted only inside the frozen Rev-1 design envelope`

### Rationale

The implementation must have enough freedom to realize hardware and firmware efficiently without forcing arbitrary low-level choices during design. At the same time, labeling a material product change as an "implementation detail" would defeat the purpose of the design freeze. This boundary provides a practical test for deciding when engineering-change control is required.

## 14.3 — Measured-TBD register and closure ownership

### FRZ-003 — Deferred measured values remain explicit until Stage B/C evidence closes them

**Status:** Accepted

Values intentionally left unknown during Stage A shall remain in a controlled **measured-TBD register**. A TBD shall not be removed merely by assuming, estimating or selecting a convenient value where the baseline requires physical characterization or verification.

The initial Rev-1 register is:

| Measured / derived TBD | Primary closure stage | Closure evidence / purpose |
| --- | --- | --- |
| motor no-load current | Stage B characterization | measured repeatable operating-current data |
| motor representative loaded current | Stage B characterization | controlled load/current observations |
| startup/inrush peak and duration | Stage B characterization | captured startup waveform and conditions |
| current under controlled stall/jam | Stage B characterization | current-limited safe stall waveform/data |
| actual ACS724 zero-current output | Stage B calibration | measured sensor/chain zero behavior |
| actual ACS724/chain sensitivity and gain | Stage B calibration | reference-current calibration data |
| complete-chain offset/gain calibration coefficients | Stage B calibration | fitted calibration record with calibration ID |
| implemented AFE frequency response | Stage B characterization, confirmed Stage C | measured transfer-response evidence including 10 kHz/50 kHz criteria |
| ADC/complete-chain noise and effective resolution | Stage B characterization, confirmed Stage C | captured raw data and noise/resolution statistics |
| actual 100 kS/s timing and jitter behavior | Stage B implementation characterization, confirmed Stage C | independent timing evidence |
| normal motor ripple/commutation/spectral characteristics | Stage B characterization | valid waveform/spectral captures under documented conditions |
| healthy-reference feature values/tolerances | Stage B characterization/calibration | healthy baseline dataset and derived reference configuration |
| overload threshold/persistence values | Stage B diagnostic tuning | motor-derived configuration subsequently verified against ≤1 s requirement |
| stall/jam threshold/persistence values | Stage B diagnostic tuning | motor-derived configuration subsequently verified against ≤100 ms requirement |
| anomaly thresholds/tolerances | Stage B diagnostic tuning | healthy/fault-condition evidence supporting selected configuration |
| final inline fuse rating | Stage B after motor characterization | documented selection from measured motor current and current-path capability |
| bench-PSU current-limit settings for characterization/fault tests | Stage B/C procedure setup | documented safe settings appropriate to each test |
| complete-chain calibrated accuracy across 0–5 A | Stage C verification | independent post-calibration evidence against ±0.10 A mandatory criterion |
| usable ≤10 mA reported-current resolution | Stage C verification | controlled distinguishability/noise evidence |
| final diagnostic detection latency and false-detection performance | Stage C verification | timestamped event evidence under accepted configuration |

Stage B owns **characterization, calibration, implementation and tuning** needed to turn these unknowns into controlled configuration values. Stage C owns **independent acceptance evidence** where a measured value is tied to a mandatory requirement.

A Stage B measurement does not automatically count as Stage C acceptance where Phase 13 requires independent verification. Conversely, Stage C shall not be forced to invent configuration values that should have been established during Stage B.

Every closed TBD shall retain sufficient context to identify the build, firmware, calibration/configuration, motor and test condition that produced it. If a later implementation change invalidates the measurement, the corresponding TBD/configuration item shall be reopened or re-characterized rather than silently reusing stale evidence.

No numerical value shall be introduced solely to eliminate a TBD. If physical evidence is unavailable, the item remains explicitly open.

### Rationale

A controlled TBD is an engineering commitment to obtain missing evidence; an undocumented assumption is a hidden design risk. Assigning closure stages prevents characterization, tuning and final acceptance from being mixed together and preserves the independence required by the verification plan.

## Phase 14 work packages

Phase 14 will establish:

1. authoritative design-freeze baseline and configuration boundary — **FRZ-001 accepted**;
2. frozen versus implementation-selectable items — **FRZ-002 accepted**;
3. measured-TBD register and closure ownership — **FRZ-003 accepted**;
4. Stage B implementation sequence and entry criteria;
5. Stage C verification sequence and evidence handoff;
6. engineering-change control after design freeze;
7. implementation readiness / procurement-blocker review;
8. future-extension boundary, including FPGA/Verilog work outside Rev-1;
9. final Stage A completeness audit and handoff decision.

Additional work packages may be introduced only if the freeze audit exposes a genuine implementation-blocking gap.

## Completion criterion

Phase 14 is complete when the Rev-1 design baseline is explicitly frozen, remaining measured/implementation TBDs are controlled and assigned to later work, and implementation can begin without silently redefining accepted product requirements or architecture.
