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

## 13.1 — Verification hierarchy and sequence

### VER-001 — Progressive four-level verification hierarchy

**Status:** Accepted

Rev-1 verification shall proceed progressively through four levels:

1. **Component/subsystem verification** — establish that individual hardware/firmware elements materially affecting system performance behave as required before relying on them in higher-level tests.
2. **Measurement-chain verification** — verify the integrated sensor → AFE → ADC → calibrated-current path, including accuracy, noise, frequency response and sampling behavior.
3. **Diagnostics/data verification** — verify current-feature computation, diagnostic behavior, data integrity, host communication and configuration/calibration traceability using a measurement chain whose relevant behavior has already been established.
4. **Complete-system verification** — demonstrate the acceptance-relevant requirements with the integrated Rev-1 motor, measurement electronics, firmware and host workflow operating together.

`component/subsystem → measurement chain → diagnostics/data → complete system`

A material failure at a lower level shall be investigated and resolved, or formally recorded as an accepted deviation, before dependent higher-level acceptance is claimed.

Passing a lower-level test does **not** automatically verify a system-level requirement. Requirements stated for the complete measurement/system chain shall be independently demonstrated at the applicable integrated level. In particular, the **≤ ±0.10 A calibrated system-current accuracy requirement** must be demonstrated on the complete calibrated measurement chain; subsystem calculations or individual-component passes alone are insufficient.

Each executed acceptance test shall retain, at minimum:

- test identity;
- result status: **PASS**, **FAIL** or **NOT TESTED**;
- measured/observed result sufficient to support the status;
- applicable Build ID/configuration/calibration identity;
- retained evidence or an unambiguous reference to it.

A **NOT TESTED** result is not equivalent to PASS and cannot satisfy an acceptance requirement.

### Rationale

Progressive verification localizes defects before they become ambiguous system-level failures while preserving the distinction between subsystem evidence and proof of final product requirements. Recording the exact build/configuration with each result also prevents evidence from one system state being incorrectly applied to another.

## 13.2 — Requirements-to-verification traceability

### VER-002 — Mandatory requirement → verification → acceptance → evidence mapping

**Status:** Accepted

Every mandatory acceptance-relevant Rev-1 requirement shall have an explicit verification route before Phase 13 closes. The traceability relationship is:

`requirement → verification ID → method → acceptance criterion → retained evidence`

No requirement is considered covered merely because it appears in a design document or because a related subsystem test exists. Where one requirement needs more than one verification activity, all required activities shall be identified. Conversely, one verification activity may support several requirements where the evidence genuinely demonstrates each criterion.

The Phase 13 verification matrix shall include at least the following baseline coverage:

| Rev-1 requirement / design claim | Verification intent | Acceptance basis |
| --- | --- | --- |
| 0–5 A calibrated unidirectional range | complete-chain calibrated-current verification across the valid range | valid readings throughout intended range; overrange treated separately |
| ≤ ±0.10 A system current accuracy after calibration | compare complete-chain calibrated current against an appropriate reference | absolute current error ≤0.10 A over the accepted verification conditions |
| ±0.05 A stretch accuracy | evaluate from the same calibrated evidence | may be claimed only if demonstrated; failure does not fail the mandatory ±0.10 A requirement |
| ≤10 mA reported-current resolution | verify numerical reporting and useful distinguishability/noise behavior | reporting and effective measurement behavior support the accepted resolution requirement without confusing resolution with accuracy |
| DC–10 kHz diagnostic information band | verify complete relevant analog-chain response through the required band | required signal information is preserved through 10 kHz within the accepted response limits |
| anti-alias AFE: ≤1 dB at 10 kHz, ≥20 dB at 50 kHz | measured AFE/chain frequency-response verification | both attenuation criteria satisfied |
| deterministic 100 kS/s acquisition | timing/sample-rate verification independent of USB host timing | measured sample timing/rate meets the deterministic acquisition requirement with no unacceptable sample loss/jitter behavior |
| startup/current waveform capture | operate/capture representative motor startup | waveform captured with correct time/current interpretation and without invalid saturation for the accepted test condition |
| average/load and changing-load information | controlled motor operating-condition comparison | expected current/load changes are measurable and retained in data/features |
| commutation/current-ripple information | waveform/spectral observation under suitable motor operation | repeatable current structure is observable within the implemented measurement band where physically present |
| overload detection ≤1 s | controlled sustained-overload condition | valid overload criteria produce detection within ≤1 s |
| stall detection ≤100 ms | controlled stall/jam condition with safe current limiting | valid stall criteria produce detection within ≤100 ms |
| no automatic Rev-1 shutdown claim | observe diagnostic response without relying on MCU motor interruption | detection is reported; bench PSU current limit/protection remains independent |
| 0–5 A validity boundary distinct from survival | controlled approach to/outside valid range without exceeding safe hardware conditions | software/data clearly identify invalid/overrange rather than reporting false calibrated current |
| USB/PC/MATLAB engineering interface | capture/configuration/export/import exercise | data and metadata transfer correctly; host activity does not control deterministic sampling |
| Build/configuration/calibration traceability | inspect retained dataset and verification records | evidence unambiguously identifies applicable hardware, firmware, calibration, motor and configuration identities |
| ≤24 VDC laboratory actuator architecture | build inspection and powered integration verification | Rev-1 actuator supply does not exceed accepted low-voltage boundary |
| separated high-current and measurement wiring | inspection plus integration checks | motor current follows the dedicated rated path and is not carried by breadboard/Dupont/measurement-ground conductors |

This table is the baseline matrix, not permission to omit a requirement discovered during the final traceability audit. Phase 13 closure shall compare the authoritative requirements/design documents against the verification matrix and add any missing acceptance-relevant coverage.

Detailed laboratory procedures, exact test-point counts, scope timebases, fixture construction and sample-count choices remain Stage C procedure details unless a particular value is necessary to define whether the requirement passes.

### Rationale

Traceability prevents verification from becoming a collection of interesting experiments that fails to prove the product requirements. Defining the acceptance basis before observing the final results also prevents criteria from being relaxed retrospectively to turn a failure into a pass.

## 13.3 — Calibration and complete-chain accuracy acceptance

### VER-003 — Independent post-calibration complete-chain accuracy verification

**Status:** Accepted

The mandatory current-accuracy requirement shall be verified on the complete calibrated measurement chain:

`I_reference → ACS724 → AFE → ADC → calibration → I_reported`

For each verification condition, current error shall be evaluated as:

`e_I = I_reported - I_reference`

The mandatory acceptance criterion is:

`|e_I| ≤ 0.10 A`

throughout the accepted **0–5 A calibrated measurement range** under the defined verification conditions.

Calibration and verification data shall be meaningfully independent. The same exact set of current points used to fit the calibration model shall not by itself be used to claim independent accuracy verification. Stage C shall therefore establish calibration coefficients using multiple reference-current points spanning the intended range and then evaluate the calibrated system at separate verification points, including intermediate current values not used for fitting.

The verification set shall include, at minimum at product level:

- zero-current behavior;
- representative low-, mid- and high-range current conditions;
- one or more intermediate points not used as calibration-fit points;
- evidence near the upper valid measurement range without intentionally exceeding safe hardware/test conditions.

The exact number and spacing of points are Stage C procedure details provided the resulting evidence adequately covers the valid range and includes independent points.

The current reference used for calibration/verification shall have sufficient known accuracy, resolution and stability relative to the **±0.10 A** system requirement that reference uncertainty does not make the pass/fail conclusion meaningless. The exact reference instrument/fixture may be selected during implementation/verification from suitable available or procured equipment; its suitability shall be documented with the retained evidence.

Acceptance evidence shall preserve the applicable calibration identity and include the measured reference current, reported current and resulting residual/error at each verification point. A residual table and/or error-versus-current plot shall be retained so range-dependent behavior and outliers are visible rather than hidden by a single aggregate statistic.

If any mandatory verification point produces `|e_I| > 0.10 A`, the complete-chain accuracy requirement is **FAIL** for that build/configuration until the cause is corrected and verification repeated, or the requirement/design is formally revised through the engineering change process.

The **±0.05 A stretch target** shall be evaluated from the same independent verification evidence. It may be reported as achieved only if the measured evidence supports it throughout the claimed conditions; failure to meet the stretch target does not by itself fail the mandatory ±0.10 A acceptance requirement.

### Rationale

Using the complete chain proves the actual system requirement rather than isolated component accuracy. Separating calibration-fit points from verification points prevents the calibration model from being evaluated only against the data that created it, while retaining residuals across the range exposes nonlinearities or range-dependent errors that a single-point check could miss.

## 13.4 — Noise and useful-resolution acceptance

### VER-004 — Separate raw-chain noise/resolution from usable reported-current resolution

**Status:** Accepted

Rev-1 verification shall distinguish **raw acquisition-chain voltage resolution/noise** from **usable reported-current resolution**. ADC nominal bit depth alone is not evidence that either requirement is achieved.

The accepted raw-chain target is an effective ADC-facing voltage resolution/noise contribution of **≤2 mV equivalent** under the intended acquisition conditions. With the nominal ACS724 sensitivity of approximately 0.8 V/A, 2 mV corresponds nominally to approximately 2.5 mA; this provides design margin relative to the 10 mA reported-current requirement but does not by itself prove that requirement.

Stage C shall characterize the complete measurement chain under at least zero-current and stable-current conditions using representative 100 kS/s acquisition. The retained evidence shall quantify the observed raw-sample distribution/noise using appropriate statistics and/or peak behavior rather than inferring useful resolution from ADC code width.

The mandatory reported-current requirement is **≤10 mA usable resolution**. Verification shall demonstrate that the intended reported-current representation can meaningfully resolve a current change of approximately 10 mA under the accepted operating conditions. This may use controlled nearby current levels and the legitimate filtering/averaging/feature computation defined by the implemented system.

The 10 mA requirement does **not** require every individual 100 kS/s raw sample to remain within a 10 mA band. Raw samples preserve the diagnostic bandwidth and may contain higher instantaneous noise; the reporting path may legitimately reduce noise provided it does not falsify the measurement or invalidate timing/bandwidth requirements applicable to that path.

Noise shall not cause materially unstable reported current, repeated false threshold crossings or false diagnostic events under a stable valid input. Any filtering/averaging used to satisfy usable reporting resolution shall be part of the recorded configuration and shall be included when verifying diagnostic latency requirements if those diagnostics depend on the filtered quantity.

Acceptance evidence shall include the applicable Build ID/calibration/configuration, acquisition conditions, raw voltage/code noise characterization, current-equivalent interpretation, and evidence demonstrating the usable reported-current increment.

### Acceptance

PASS requires both:

1. measured complete raw ADC-facing chain behavior supports **≤2 mV effective voltage resolution/noise equivalent** under the defined acquisition condition; and
2. the implemented reporting path demonstrates **≤10 mA usable reported-current resolution** without unacceptable instability or false diagnostic behavior.

Failure of either mandatory criterion is a VER-004 failure for that build/configuration.

### Rationale

Nominal ADC resolution and numerical display precision can both exaggerate real measurement capability. Measuring raw-chain noise and independently demonstrating the smallest useful reported-current change establishes what the system can actually resolve while preserving the distinction between high-bandwidth waveform acquisition and lower-noise reporting.

## Phase 13 work packages

The plan will define, at an appropriate product level:

1. verification levels and sequencing — **VER-001 accepted**;
2. requirements-to-verification traceability — **VER-002 accepted**;
3. sensor and complete measurement-chain calibration/accuracy acceptance — **VER-003 accepted**;
4. noise and useful-resolution acceptance — **VER-004 accepted**;
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
