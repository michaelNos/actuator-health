# Phase 13 — System Verification and Acceptance Plan

**Status:** In development  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 13 defines how the completed Rev-1 design will be proven against its accepted requirements after implementation. It establishes verification coverage, acceptance logic, evidence expectations and the treatment of measured TBDs without prematurely writing detailed laboratory procedures.

This phase does **not** perform verification and does not invent measured results. Exact scope settings, sample counts, command sequences, fixture details and troubleshooting procedures remain Stage B/C implementation and verification work.

## Accepted baseline entering Phase 13

The verification plan shall cover the integrated design baselined through Phase 12, including:

- 0–5 A calibrated unidirectional current measurement;
- ≤ ±0.10 A system current-accuracy target after calibration, with ±0.05 A stretch target;
- ≤10 mA reported-current resolution;
- DC–10 kHz diagnostic information band;
- deterministic 100 kS/s acquisition;
- fourth-order approximately 15 kHz Butterworth anti-alias AFE;
- ACS724 + MCP6022 + RA4M1/UNO R4 measurement chain;
- real-time current features and overload/stall diagnostic behavior;
- USB/PC/MATLAB engineering interface;
- 24 VDC Philips/Saeco Rev-1 gearmotor;
- protection, overrange/validity and safe low-voltage laboratory behavior;
- configuration/calibration/build traceability.

## Verification philosophy

Verification shall be **requirement-driven and evidence-based**. Each acceptance-relevant requirement shall have a defined verification method, pass/fail criterion and retained evidence. A requirement is not considered verified merely because the design calculation predicts compliance.

Measured quantities that were legitimately left TBD during design shall be populated during implementation/verification and assessed against the applicable acceptance requirement. Where a measured result contradicts the design assumption, the result shall be retained and the design shall be corrected rather than adjusted retrospectively to manufacture a pass.

## Phase 13 work packages

The plan will define, at an appropriate product level:

1. verification levels and sequencing;
2. requirements-to-verification traceability;
3. sensor and complete measurement-chain calibration/accuracy acceptance;
4. noise and useful-resolution acceptance;
5. AFE frequency-response and anti-alias acceptance;
6. deterministic ADC sampling/timing acceptance;
7. waveform/data-integrity and USB/MATLAB acceptance;
8. diagnostic-feature, overload and stall acceptance;
9. overrange, fault handling and protection checks;
10. power/grounding/integration checks;
11. build/configuration/calibration traceability evidence;
12. system-level acceptance and treatment of deviations;
13. final verification completeness review.

Additional verification groups may be introduced where the requirements/design baseline exposes a genuine acceptance gap.

## Completion criterion

Phase 13 is complete when every acceptance-relevant Rev-1 requirement and material design claim has a clear verification route and acceptance criterion, such that Stage C can execute the verification without inventing what constitutes a pass.
