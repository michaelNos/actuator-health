# Phase 14 — Rev-1 Design Freeze and Implementation Handoff

**Status:** Design complete / ready for PR review  
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

`Stage A design freeze ≠ immutable forever`

but

`material post-freeze change → explicit engineering revision + traceability`

## 14.2 — Frozen versus implementation-selectable items

### FRZ-002 — Implementation freedom is bounded by the frozen product baseline

**Status:** Accepted

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

- exact RA4M1 ADC/timer/register configuration used to realize deterministic sampling;
- exact DTC/DMA-like transfer strategy;
- acquisition/buffer sizes and internal scheduling details;
- FFT length, window, overlap and related DSP realization details;
- detailed serial framing and integrity mechanism within the accepted communication contract;
- MATLAB script/function/file organization;
- motor-derived diagnostic thresholds, persistence/tuning values and healthy-reference values;
- measured calibration coefficients and calibration identity;
- final fuse rating selected from motor characterization and current-path capability;
- exact physical component placement/routing that preserves the frozen wiring/isolation rules.

An implementation-selectable choice becomes a controlled design change if it alters or invalidates a frozen requirement, architecture boundary, safety assumption, interface contract or acceptance criterion.

Examples: changing FFT length while preserving accepted behavior is an implementation choice; changing 100 kS/s to 20 kS/s is not. Tuning a stall threshold from measured motor data is an implementation choice; replacing the ACS724 architecture is not.

`implementation freedom is permitted only inside the frozen Rev-1 design envelope`

## 14.3 — Measured-TBD register and closure ownership

### FRZ-003 — Deferred measured values remain explicit until Stage B/C evidence closes them

**Status:** Accepted

Values intentionally left unknown during Stage A remain in a controlled measured-TBD register. A TBD shall not be removed merely by assuming or estimating a convenient value where physical characterization or verification is required.

| Measured / derived TBD | Primary closure stage | Closure evidence / purpose |
| --- | --- | --- |
| motor no-load current | Stage B characterization | measured repeatable operating-current data |
| motor representative loaded current | Stage B characterization | controlled load/current observations |
| startup/inrush peak and duration | Stage B characterization | captured startup waveform and conditions |
| current under controlled stall/jam | Stage B characterization | current-limited safe stall waveform/data |
| actual ACS724 zero-current output | Stage B calibration | measured sensor/chain zero behavior |
| actual ACS724/chain sensitivity and gain | Stage B calibration | reference-current calibration data |
| complete-chain offset/gain calibration coefficients | Stage B calibration | fitted calibration record with calibration ID |
| implemented AFE frequency response | Stage B, confirmed Stage C | measured transfer-response evidence |
| ADC/complete-chain noise and effective resolution | Stage B, confirmed Stage C | raw data and noise/resolution statistics |
| actual 100 kS/s timing and jitter behavior | Stage B, confirmed Stage C | independent timing evidence |
| normal motor ripple/commutation/spectral characteristics | Stage B characterization | valid waveform/spectral captures |
| healthy-reference feature values/tolerances | Stage B characterization/calibration | healthy baseline and reference configuration |
| overload threshold/persistence values | Stage B diagnostic tuning | motor-derived configuration verified against ≤1 s |
| stall/jam threshold/persistence values | Stage B diagnostic tuning | motor-derived configuration verified against ≤100 ms |
| anomaly thresholds/tolerances | Stage B diagnostic tuning | healthy/fault evidence supporting configuration |
| final inline fuse rating | Stage B after motor characterization | selection from measured current and path capability |
| bench-PSU current-limit settings | Stage B/C procedure setup | documented safe settings appropriate to test |
| complete-chain calibrated accuracy across 0–5 A | Stage C verification | independent evidence against ±0.10 A |
| usable ≤10 mA reported-current resolution | Stage C verification | controlled distinguishability/noise evidence |
| final diagnostic latency and false-detection performance | Stage C verification | timestamped event evidence |

Stage B owns characterization, calibration, implementation and tuning. Stage C owns independent acceptance evidence where a measured value is tied to a mandatory requirement. A Stage B measurement does not automatically count as Stage C acceptance where Phase 13 requires independent verification.

Every closed TBD retains enough context to identify the build, firmware, calibration/configuration, motor and test condition. A later implementation change that invalidates the measurement reopens the affected item. No numerical value is introduced solely to eliminate a TBD.

## 14.4 — Stage B implementation sequence and entry criteria

### FRZ-004 — Progressive subsystem bring-up before complete Rev-1 integration

**Status:** Accepted

Stage B proceeds progressively:

`inspect/setup → motor characterization → ACS724 bring-up → AFE bring-up → deterministic ADC acquisition → calibration/current conversion → USB/MATLAB → healthy characterization → diagnostics tuning → protection finalization → complete build → integration checks`

Working sequence:

1. inspect parts and establish safe bench/current-limit setup;
2. characterize the 24 V motor;
3. bring up and characterize the ACS724 carrier;
4. build and characterize the MCP6022 AFE independently;
5. implement and characterize deterministic RA4M1 100 kS/s acquisition;
6. integrate calibration, current conversion and validity behavior;
7. implement USB transport and MATLAB engineering tooling;
8. characterize healthy motor-current signatures;
9. tune overload/stall/anomaly configuration from measured behavior;
10. finalize fuse and current-limit configuration;
11. assemble the complete Rev-1 build;
12. perform Stage B integration checks before formal acceptance.

Stage B may begin after Phase 14 is approved/merged, the items needed for the next activity are available, the applicable frozen design can be identified, and the work can be performed without violating an unresolved safety dependency. Material defects are resolved, documented as limitations, or escalated through engineering change before dependent acceptance work proceeds.

## 14.5 — Stage C verification sequence and evidence handoff

### FRZ-005 — Formal acceptance uses a stable identified Stage B configuration

**Status:** Accepted

Stage B develops, characterizes, calibrates and tunes the system. Stage C independently determines whether the resulting Rev-1 configuration satisfies the frozen requirements and Phase 13 acceptance criteria.

The Stage C sequence follows the Phase 13 hierarchy:

`component/subsystem → measurement chain → diagnostics/data → complete system`

Before formal Stage C acceptance, Stage B shall hand over a stable identified configuration including, as applicable:

`Build ID + hardware revision + firmware revision + calibration ID + configuration ID + motor ID`

Formal acceptance evidence shall be produced against that identified configuration. Acceptance tests shall not be silently converted into tuning sessions. If a mandatory test fails, the observed FAIL is retained. The system returns to Stage B for correction/tuning where appropriate; the changed calibration/configuration/build receives a distinguishable identity; and affected verification is repeated.

For example, if current-based stall detection is measured at 140 ms against the mandatory ≤100 ms criterion, the test is FAIL for that configuration. Adjusting a threshold or persistence parameter creates a changed configuration and requires the affected verification to be rerun rather than rewriting the original result.

Stage C evidence shall retain the traceability and result-status requirements established in Phase 13. Only evidence belonging to the accepted configuration may support final Rev-1 acceptance unless an explicit analysis demonstrates that a particular unchanged result remains valid across a controlled revision.

## 14.6 — Engineering change control after design freeze

### FRZ-006 — Material post-freeze changes require explicit impact analysis and re-verification

**Status:** Accepted

A post-freeze change is material when it affects a frozen requirement, product/component architecture, electrical interface, safety/protection assumption, sampling or diagnostic architecture, calibration meaning, communication contract or verification PASS criterion.

Material changes follow:

`problem/evidence → impact analysis → proposed change → approval → baseline update → implementation → affected verification repeated`

The change record shall identify why the frozen baseline is inadequate, what is changed, which requirements/design documents/configurations are affected, and which prior characterization or verification evidence must be repeated or invalidated.

Implementation-selectable details already permitted by FRZ-002 do not require formal change control merely because a low-level implementation choice is made. They do require normal configuration/source-control traceability where relevant.

A failed test shall not be hidden by silently modifying the requirement or implementation. The original result remains part of the engineering record; correction and re-verification establish the new result.

## 14.7 — Future FPGA / Verilog extension boundary

### FRZ-007 — FPGA/Verilog processing is a post-Rev-1 extension, not a Rev-1 dependency

**Status:** Accepted

The frozen Rev-1 signal path remains:

`ACS724 → analog AFE → RA4M1 → USB → PC/MATLAB`

FPGA/Verilog work is explicitly reserved as a future engineering extension after Rev-1 implementation and verification. It is not required to build, calibrate or accept Rev-1 and shall not become an implementation blocker.

A future extension may reuse live or recorded Rev-1 current data to investigate hardware realization of functions such as digital filtering, mean/RMS/peak calculations, threshold/event detection, spectral processing, fixed-point arithmetic, pipelining and deterministic streaming processing.

The engineering purpose is to compare suitable MCU software DSP with FPGA hardware processing and study the consequences for determinism, throughput, latency, numeric representation and resource use. FPGA functionality shall not be added merely to claim that the project contains Verilog.

If a future FPGA revision changes the accepted acquisition/diagnostic architecture, it becomes a separately controlled revision rather than being retroactively treated as part of Rev-1.

## 14.8 — Final Stage A completeness audit and implementation handoff

### FRZ-008 — Stage A closes only after a cross-phase implementation-readiness audit

**Status:** Accepted

The final Stage A audit reviewed the authoritative Phase 1–13 baseline together with the Phase 14 freeze decisions for:

1. **consistency** — later decisions do not silently contradict frozen requirements;
2. **completeness** — the product architecture and interfaces needed to begin implementation are defined;
3. **TBD correctness** — remaining unknowns genuinely require implementation, characterization, tuning or verification rather than representing forgotten Stage A decisions;
4. **verification closure** — mandatory Rev-1 requirements have measurable verification routes and objective acceptance logic.

The audit specifically cross-checked the Phase 1 requirements against the later sensor/AFE/ADC, firmware/diagnostic, communication, power/protection, calibration, integration and Phase 13 verification baselines. The major frozen values remain coherent: 0–5 A calibrated unidirectional range, DC–10 kHz diagnostic band, 100 kS/s deterministic acquisition, ≤±0.10 A mandatory calibrated accuracy, ≤10 mA reported-current resolution, overload ≤1 s, current-based stall/jam ≤100 ms and ≤24 VDC Rev-1 laboratory operation.

The audit also confirmed that higher-frequency characterization above 10 kHz remains a validation obligation rather than being lost at freeze; deterministic acquisition remains hardware-timed and independent of USB workload; communication remains versioned/integrity-aware downstream of acquisition; protection remains independent of diagnostic shutdown; and Stage C acceptance remains requirement-driven rather than inferred from Stage B bring-up success.

No implementation-blocking Stage A contradiction or missing product-level decision was identified. Remaining open numerical values are appropriately measurement/configuration-derived and are controlled by FRZ-003. Register-level firmware details, buffer/DSP choices, calibration coefficients, motor-derived thresholds, healthy-reference values, fuse rating and measured performance are therefore legitimate Stage B/C outputs rather than reasons to continue Stage A design.

### Handoff decision

**READY FOR STAGE B IMPLEMENTATION**, subject to Phase 14 PR review and merge.

This decision means the design is sufficiently defined to begin implementation. It does **not** mean that the physical Rev-1 has passed any Stage C acceptance test.

If Stage B exposes a frozen assumption that is physically incorrect or infeasible, FRZ-006 engineering change control applies.

## Phase 14 closure summary

Accepted Phase 14 decisions:

1. **FRZ-001** — authoritative Rev-1 Stage A baseline;
2. **FRZ-002** — frozen versus implementation-selectable boundary;
3. **FRZ-003** — measured-TBD register and closure ownership;
4. **FRZ-004** — Stage B implementation sequence and entry criteria;
5. **FRZ-005** — Stage C verification sequence and evidence handoff;
6. **FRZ-006** — engineering-change control after freeze;
7. **FRZ-007** — future FPGA/Verilog extension boundary;
8. **FRZ-008** — final Stage A audit and READY FOR STAGE B handoff decision.

The proposed procurement-blocker work package was rejected during review and is not part of the Phase 14 baseline.

## Completion criterion

Phase 14 is complete when this document is approved and merged. At that point Stage A design is frozen and complete, and work proceeds to Stage B implementation under the controlled baseline above.
