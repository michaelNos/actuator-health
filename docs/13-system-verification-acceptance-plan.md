# Phase 13 — System Verification and Acceptance Plan

**Status:** Design complete / ready for PR review  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 13 defines how the implemented Rev-1 design will be proven against the accepted Phase 1–12 baseline. It defines verification coverage, objective acceptance logic, evidence requirements, treatment of measured TBDs and final system acceptance.

This phase does **not** claim that physical verification has already passed. Exact laboratory commands, scope settings, sample counts, fixture details and troubleshooting sequences remain Stage B/C work unless needed to define pass/fail.

## Accepted Rev-1 baseline

Verification covers the integrated design including:

- 0–5 A calibrated unidirectional current measurement;
- ≤ ±0.10 A system current accuracy after calibration; ±0.05 A stretch target;
- ≤10 mA reported-current resolution and ≤2 mV effective ADC-domain voltage-resolution/noise target;
- DC–10 kHz diagnostic information band and characterization above 10 kHz;
- deterministic 100 kS/s acquisition;
- fourth-order approximately 15 kHz Butterworth AFE;
- ACS724 + MCP6022 + RA4M1/UNO R4 measurement chain;
- real-time current features, measurement-pipeline validity and overload/stall/anomaly diagnostics;
- USB/PC/MATLAB engineering interface;
- Philips/Saeco 24 VDC Rev-1 gearmotor;
- protection, overrange and safe low-voltage laboratory operation;
- configuration/calibration/healthy-reference/build traceability.

## Verification philosophy

Verification is **requirement-driven and evidence-based**. A calculation or design prediction is not physical verification. Measured TBDs are populated during implementation/verification. If measurement contradicts a design assumption, the result is retained and the design is corrected or formally revised rather than the acceptance criterion being retrospectively changed to manufacture a pass.

## 13.1 — VER-001: Progressive verification hierarchy

**Status:** Accepted

Verification proceeds through four levels:

`component/subsystem → measurement chain → diagnostics/data → complete system`

A material lower-level failure is resolved or formally recorded before dependent higher-level acceptance is claimed. Lower-level success does not automatically prove a system-level requirement; for example, the ≤±0.10 A requirement must be demonstrated on the complete calibrated chain.

Each acceptance test records at minimum: test identity; **PASS / FAIL / NOT TESTED**; measured/observed result; applicable Build/configuration/calibration identity; and retained evidence. `NOT TESTED` never equals PASS.

## 13.2 — VER-002: Requirements-to-verification traceability

**Status:** Accepted

Every mandatory acceptance-relevant requirement shall map as:

`requirement → verification ID → method → acceptance criterion → retained evidence`

One test may support several requirements only where its evidence genuinely proves each criterion. No mandatory requirement may close Phase 13 without a verification route.

Baseline coverage includes measurement range/accuracy/resolution, bandwidth and anti-alias behavior, deterministic acquisition, waveform/features, overload/stall/anomaly behavior, measurement-pipeline validity, communication integrity, MATLAB analysis, power/protection/integration, and configuration traceability.

## 13.3 — VER-003: Independent post-calibration accuracy verification

**Status:** Accepted

The complete chain is verified:

`I_reference → ACS724 → AFE → ADC → active calibration → I_reported`

`e_I = I_reported - I_reference`

Mandatory criterion throughout the accepted 0–5 A range:

`|e_I| ≤ 0.10 A`

Calibration-fit points and independent verification points shall not be the identical dataset. Verification includes zero, representative low/mid/high conditions, intermediate points not used for fitting, and evidence near the upper valid range. The reference measurement must have sufficient known accuracy/resolution/stability for a meaningful ±0.10 A decision. Residuals and calibration identity are retained. The ±0.05 A stretch target is reported only if independently demonstrated.

## 13.4 — VER-004: Noise and useful resolution

**Status:** Accepted

Raw acquisition-chain behavior and reported-current resolution are separate quantities. ADC bit depth or display digits alone do not prove either.

PASS requires both:

1. measured complete ADC-facing chain behavior supporting **≤2 mV effective voltage resolution/noise equivalent** under defined acquisition conditions; and
2. **≤10 mA usable reported-current resolution** demonstrated by the implemented reporting path.

Raw 100 kS/s samples need not individually remain within 10 mA. Noise/filtering shall not create materially unstable reporting, false threshold crossings or false diagnostics. Any filtering affecting diagnostics is part of the verified configuration and its delay counts toward latency.

## 13.5 — VER-005: AFE frequency response and anti-alias behavior

**Status:** Accepted

The real built AFE is measured with simultaneous input/output observation. For sinusoidal excitation:

`A(f) = 20 log10(Vout/Vin)`

Mandatory criteria:

`A(10 kHz) ≥ -1 dB`

`A(50 kHz) ≤ -20 dB`

The measured curve shall also show approximately unity low-frequency/passband behavior and no unacceptable peaking, oscillation or instability. Coverage through the passband, approximately 15 kHz transition region and toward 50 kHz shall establish a physically coherent realized response.

## 13.6 — VER-006: Deterministic 100 kS/s acquisition

**Status:** Accepted

Rev-1 shall demonstrate nominal:

`fs = 100 kS/s`, `Ts = 10 µs`.

Verification must observe actual acquisition timing rather than infer it from configuration constants or PC throughput. PASS requires valid ordering/continuity for accepted captures, no unexplained missing/duplicated/reordered samples, host-independent conversion timing and measured jitter/timing quality compatible with the DC–10 kHz diagnostic band. USB/host scheduling shall not pace conversions. Overrun/gaps must become explicit validity faults rather than apparently continuous data.

## 13.7 — VER-007: Data, communication and MATLAB integrity

**Status:** Accepted

End-to-end path:

`ADC samples → MCU buffer/processing → USB → PC/MATLAB`

PASS requires accepted captures to preserve sample ordering, count, timing identity, validity and current interpretation without unexplained loss/duplication/corruption. Incomplete captures or overflows are explicitly invalid/incomplete.

The communication implementation shall additionally demonstrate the Phase 9 contract:

- normal telemetry correctly conveys selected measurement/features, operating state, diagnostics/event history and health information;
- sequence/continuity information exposes missing or discontinuous transmitted data;
- the PC identifies protocol/data-format version and rejects or explicitly handles incompatible data;
- the selected framing integrity mechanism detects corrupted framed communication;
- waveform capture preserves timing, ordering and validity metadata;
- normal telemetry/capture workload does not disturb VER-006 acquisition.

MATLAB shall reproduce time/current interpretation, calibration analysis and waveform/spectral analysis from metadata-bearing datasets. A known injected signal and/or motor waveform may be cross-checked against the oscilloscope for consistent amplitude/frequency/timing structure. Real-time embedded monitoring shall remain functional with MATLAB/PC absent.

## 13.8 — VER-008: Diagnostic features, overload, stall and anomaly behavior

**Status:** Accepted

Representative operation shall demonstrate valid processing of startup/inrush, mean/RMS/load changes, ripple/commutation information where physically present, and implemented time/frequency-domain features. Absence of a physical spectral feature is not a failure if it is genuinely absent below verified capability; the system shall not invent one.

Controlled overload acceptance:

`t_overload ≤ 1 s`

from the instant the implemented overload criteria become valid.

Controlled current-based stall/jam acceptance:

`t_stall ≤ 100 ms`

from the instant the implemented combined stall criteria become valid. Rev-1 has no speed sensor, so this proves current-based stall inference, not independent zero-RPM measurement.

The Phase 8 diagnostic contract shall also be verified:

- startup context is not repeatedly misclassified by running-state fault criteria;
- invalid required measurement evidence produces **diagnostic unavailable**, not an actuator fault;
- a deliberately established known-good **healthy reference** is used for current-pattern anomaly comparison;
- persistence/hysteresis prevents unstable threshold chatter;
- qualified diagnostic events remain available as event/history information after live-state recovery;
- representative normal startup/load behavior does not show unacceptable systematic false overload/stall indications.

Motor-dependent thresholds, healthy-reference values, persistence/recovery constants and anomaly limits are measured/tuned in Stage B/C and become versioned accepted configuration rather than guessed Stage-A constants.

## 13.9 — VER-009: Overrange, internal validity and protection

**Status:** Accepted

`measurement valid ≠ hardware survived`.

The valid calibrated range is 0–5 A. In-range operation shall not prematurely clip. Safely produced out-of-range/clipped conditions shall be reported invalid/overrange rather than as trustworthy calibrated current.

Implemented measurement-pipeline validity shall be exercised non-destructively, including where applicable acquisition overrun/sample gap, ADC saturation, missing/invalid/incompatible calibration, invalid processing continuity/window and detectable processing failure. Compromised evidence shall not propagate as a valid condition conclusion.

Installed fuse/fuse holder, current-rated wiring and bench-PSU current limiting are checked against actual motor characterization. The diagnostic MCU is not credited as the independent protective shutdown mechanism.

Destructive misuse tests are prohibited: no intentional actuator-supply short merely to blow a fuse, no intentional absolute-maximum violation, and no deliberate 24 V application to A0. The 5 A measurement boundary is not automatically a survival/fuse/shutdown threshold.

## 13.10 — VER-010: Power, grounding and physical integration

**Status:** Accepted

Before dynamic motor acceptance, the physical assembly is inspected and electrically checked against Phase 12.

Actuator path:

`PSU+ → inline fuse → ACS724 IP+ → IP− → motor → PSU−`

Measurement domain:

`UNO 5V_MEAS/GND_MEAS → ACS724 secondary + MCP6022 AFE → A0`

Unpowered checks verify polarity/routing, 18 AWG motor-current harness, secure current-rated connections, no motor current through breadboard/Dupont/GND_MEAS, primary/secondary segregation, correct 5 V measurement wiring, decoupling, AFE/ADC connection, absence of unintended 24 V paths into the ADC domain, accessible documented test points and adequate mechanical support/strain relief.

Controlled power-up then verifies ≤24 V actuator supply, correct 5V_MEAS polarity, plausible sensor/AFE DC points and absence of unexpected excessive current, heating, clipping, oscillation or unstable wiring behavior.

## 13.11 — VER-011: Build/configuration/calibration traceability

**Status:** Accepted

Every acceptance-relevant result shall identify the exact system state:

`hardware revision → firmware revision → calibration ID → motor ID → configuration ID`

Evidence shall recover firmware/Git identity, active calibration coefficients/validity, acquisition settings, diagnostic thresholds/persistence/filtering, motor/test configuration and corresponding raw/processed evidence. Material changes create distinguishable identities; evidence from an old state cannot silently be relabeled.

Measurement calibration and the healthy diagnostic reference remain separate, independently versioned datasets. After material calibration or signal-processing change, healthy-reference compatibility is checked; an incompatible reference must be deliberately re-characterized rather than silently reused or automatically adapted.

## 13.12 — VER-012: System-level acceptance and deviations

**Status:** Accepted

Overall Rev-1 acceptance requires **every mandatory requirement to have traceable PASS evidence for the accepted build/configuration**.

- mandatory `FAIL` prevents overall acceptance;
- mandatory `NOT TESTED` prevents overall acceptance;
- failure of a stretch goal does not fail Rev-1 unless it is separately mandatory;
- evidence from incompatible builds/configurations shall not be mixed to manufacture a complete pass;
- unresolved deviations are explicitly recorded.

A deviation may be accepted without changing overall PASS only when it does not contradict a mandatory Rev-1 requirement. If a mandatory requirement cannot be met, the system remains unaccepted until corrected/retested or the engineering baseline itself is formally revised with rationale and affected verification repeated. Requirements shall not be retrospectively relaxed merely because a test failed.

## 13.13 — VER-013: Final verification completeness audit

**Status:** Accepted / audit performed

Phase 13 closure audited the accepted Phase 1–12 design handoffs against:

`requirement/design claim → verification method → objective acceptance basis → required evidence`

The audit identified and closed several coverage gaps that were not explicit enough in the initial VER-001…011 draft:

1. **Phase 1 REQ-BW-002:** characterization above the 10 kHz diagnostic band is required to determine whether future bandwidth extension is justified. Stage C shall therefore inspect available sensor/AFE current information above 10 kHz with laboratory instrumentation where safely measurable and retain the observation; this is characterization, not a requirement to extend Rev-1 bandwidth.
2. **Phase 7 validity propagation:** invalid calibration, processing continuity/failure and acquisition gaps are now explicitly covered by VER-006/007/009.
3. **Phase 8 diagnostic contract:** diagnostic-unavailable behavior, healthy-reference anomaly comparison, persistence/hysteresis and retained event history are now explicitly covered by VER-008.
4. **Phase 9 communication contract:** protocol/data-format version handling, sequence continuity, framed-data integrity detection and normal telemetry content are now explicitly covered by VER-007.
5. **Phase 11 calibration/reference separation:** missing/invalid calibration behavior, MATLAB reproducibility/independence and healthy-reference compatibility are explicitly covered by VER-007/009/011.
6. **Phase 12 integration:** current-path segregation, test points, mechanical support, build identity and motor-dependent fuse selection are covered by VER-009/010/011.

No contradictory mandatory acceptance criterion was found between the audited baseline and this verification plan. Motor-specific current thresholds, fuse value, healthy-reference values, diagnostic persistence/recovery constants, detailed DSP parameters, actual rail values, timing/jitter measurements and calibration coefficients remain legitimate **measured/implementation TBDs**; they are not missing Stage-A requirements. They shall be recorded under the applicable Build/configuration identity when established.

### Additional bandwidth-characterization acceptance route

For REQ-BW-002, PASS means the planned higher-frequency characterization was performed with suitable laboratory instrumentation over the practically observable region above 10 kHz, the observation/limitations were retained, and a reasoned conclusion was recorded on whether a future Rev should investigate wider acquisition bandwidth. Rev-1 is **not** required to preserve >10 kHz content through its accepted 15 kHz anti-alias architecture.

## Verification evidence classes

Depending on the verification item, retained evidence may include:

- oscilloscope screenshots/exports and generator settings;
- reference current/voltage readings and instrument identity/specification basis;
- raw ADC/capture files and firmware logs;
- MATLAB scripts/results/plots sufficient to reproduce analysis;
- calibration residual tables and calibration records;
- diagnostic event waveforms and latency calculations;
- communication continuity/integrity/version tests;
- photographs/inspection records of wiring, fuse, test points and build configuration;
- Build ID and configuration metadata.

## Phase 13 closure

VER-001 through VER-013 are **accepted**. The final completeness audit has been performed and its discovered gaps have been incorporated into the verification plan.

Phase 13 therefore defines how Rev-1 will be accepted or rejected once implemented and physically tested. It does **not** claim that Rev-1 has already passed verification.

**Phase 13 status: DESIGN COMPLETE / READY FOR PR REVIEW**
