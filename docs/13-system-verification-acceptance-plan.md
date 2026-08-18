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

## 13.2 — Requirements-to-verification traceability

### VER-002 — Mandatory requirement → verification → acceptance → evidence mapping

**Status:** Accepted

Every mandatory acceptance-relevant Rev-1 requirement shall have an explicit verification route before Phase 13 closes. The traceability relationship is:

`requirement → verification ID → method → acceptance criterion → retained evidence`

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

Phase 13 closure shall compare the authoritative requirements/design documents against the verification matrix and add any missing acceptance-relevant coverage.

## 13.3 — Calibration and complete-chain accuracy acceptance

### VER-003 — Independent post-calibration complete-chain accuracy verification

**Status:** Accepted

The mandatory current-accuracy requirement shall be verified on the complete calibrated measurement chain:

`I_reference → ACS724 → AFE → ADC → calibration → I_reported`

`e_I = I_reported - I_reference`

Mandatory acceptance:

`|e_I| ≤ 0.10 A`

throughout the accepted **0–5 A calibrated measurement range** under the defined verification conditions.

Calibration and verification data shall be meaningfully independent. Separate verification points, including intermediate values not used for calibration fitting, shall be used. The reference shall have sufficient known accuracy, resolution and stability relative to the ±0.10 A requirement that pass/fail remains meaningful. Evidence shall retain calibration identity, reference current, reported current and residual/error. The ±0.05 A stretch target may be claimed only if independently demonstrated.

## 13.4 — Noise and useful-resolution acceptance

### VER-004 — Separate raw-chain noise/resolution from usable reported-current resolution

**Status:** Accepted

Rev-1 verification shall distinguish **raw acquisition-chain voltage resolution/noise** from **usable reported-current resolution**. ADC nominal bit depth alone is not evidence that either requirement is achieved.

PASS requires both **≤2 mV effective raw-chain voltage resolution/noise equivalent** under intended acquisition conditions and **≤10 mA usable reported-current resolution**. Noise shall not create materially unstable reporting, repeated false threshold crossings or false diagnostics. Raw 100 kS/s samples need not individually remain within 10 mA.

## 13.5 — AFE frequency-response and anti-alias acceptance

### VER-005 — Measured AFE transfer response with mandatory 10 kHz and 50 kHz criteria

**Status:** Accepted

The implemented AFE shall be verified experimentally rather than accepted from calculation alone.

`A(f) = 20 log10(Vout(f) / Vin(f))`

Mandatory criteria:

`A(10 kHz) ≥ -1 dB`

`A(50 kHz) ≤ -20 dB`

The measured response shall also demonstrate approximately unity low-frequency/passband behavior and no unacceptable peaking, oscillation or instability. Sufficient response coverage around the passband, approximately 15 kHz transition region and approach to 50 kHz shall establish a coherent realized response.

## 13.6 — Deterministic ADC sampling/timing acceptance

### VER-006 — Measured deterministic 100 kS/s acquisition independent of host timing

**Status:** Accepted

Rev-1 shall demonstrate nominal:

`fs = 100 kS/s`

`Ts = 10 µs`

Acceptance requires valid sample ordering/continuity for accepted captures, host-independent conversion timing, no unexplained missing/duplicated/reordered samples, and measured timing quality compatible with the DC–10 kHz diagnostic band. USB activity or host scheduling shall not pace ADC conversions or silently corrupt continuity.

## 13.7 — Waveform/data integrity and USB/MATLAB acceptance

### VER-007 — End-to-end capture integrity from ADC buffer to MATLAB

**Status:** Accepted

Rev-1 shall demonstrate that waveform data delivered to the PC/MATLAB environment remains a faithful, interpretable representation of the ordered measurement sequence acquired by the MCU.

The verification path is:

`ADC samples → MCU acquisition/buffer → USB transport → PC/MATLAB import`

Stage C shall demonstrate that, for an accepted complete waveform capture:

- sample ordering is preserved;
- no unexplained sample loss, duplication or corruption occurs;
- sample count/length agrees with the capture metadata;
- the sample-rate/timing metadata corresponds to the active acquisition configuration;
- the active calibration, Build ID, motor/configuration and relevant measurement-validity information are associated with the dataset;
- MATLAB reconstructs a time axis consistent with the acquisition timing and converts/interprets current using the applicable calibration/configuration;
- normal USB communication does not disturb the deterministic ADC acquisition established by VER-006;
- an incomplete capture, buffer overflow or communication loss is explicitly identifiable as incomplete/invalid rather than silently represented as a complete valid waveform.

A known injected signal and/or representative motor-current waveform may be observed independently on the oscilloscope and compared with the imported MATLAB waveform as an end-to-end sanity check. Exact sample-for-sample equality is not required between independent instruments; amplitude, dominant frequency, timing and waveform structure shall be consistent within the expected behavior of the respective paths.

PASS requires a valid complete capture to traverse `AFE/ADC → MCU → USB → MATLAB` without unexplained loss, duplication, reordering or corruption, while retaining enough metadata for correct time/current interpretation and explicitly exposing incomplete/invalid data.

## 13.8 — Diagnostic-feature, overload and stall acceptance

### VER-008 — Current-signature behavior and controlled overload/stall detection

**Status:** Accepted

Rev-1 shall verify that the implemented diagnostic path extracts and reports useful current-signature information in addition to measuring current magnitude.

Normal/representative operation shall provide evidence that the implemented system can observe and consistently process, where physically present in the selected motor/test condition:

- startup/inrush waveform behavior;
- average/current level and changes associated with changing mechanical/electrical load;
- repeatable commutation/current-ripple structure;
- implemented time-domain and spectral diagnostic features derived from valid waveform data.

Absence of a particular spectral/commutation feature in a physical operating condition is not by itself a system failure if the feature is not physically present above the verified measurement/noise capability. The system shall not invent such a feature; retained evidence shall distinguish observed motor behavior from processing capability.

#### Overload acceptance

A controlled, safe condition shall be created in which the **implemented and documented overload criteria become valid**. Detection latency shall be measured from the instant those criteria are satisfied to the corresponding diagnostic assertion/report.

Mandatory criterion:

`t_overload ≤ 1 s`.

#### Stall/jam acceptance

A controlled stall/jam condition shall be created only with bench-current limiting and the accepted protection measures in place. Because Rev-1 has no independent speed/position sensor, this test verifies the **current-based stall diagnostic**, not an independent measurement of zero mechanical RPM.

Detection latency shall be measured from the instant the implemented current-based stall criteria become valid to diagnostic assertion/report.

Mandatory criterion:

`t_stall ≤ 100 ms`.

The latency clock shall therefore not begin merely when an operator starts applying load or touches the mechanism; it begins when the defined diagnostic input/criteria are actually satisfied. This keeps latency attributable to the monitoring system rather than to an uncontrolled mechanical transition.

#### False-detection behavior

Representative normal startup/inrush and ordinary load changes shall be exercised. They shall not repeatedly or systematically produce false overload/stall indications under the configuration being accepted. Any filtering, persistence or threshold logic used to suppress false detections is part of the verified configuration and its delay is included in the applicable detection-latency measurement.

Rev-1 shall report diagnostic events but shall not rely on MCU-controlled automatic motor shutdown to pass these tests. Bench PSU current limiting and independent protection remain the safety boundary.

### Acceptance

PASS requires:

1. representative normal current-signature behavior is captured and processed consistently from valid waveform data;
2. overload detection occurs within **≤1 s** from valid overload criteria;
3. current-based stall/jam detection occurs within **≤100 ms** from valid stall criteria; and
4. representative normal startup/load behavior does not demonstrate unacceptable systematic false overload/stall detections.

Evidence shall retain the waveform/data around each event, applicable diagnostic configuration/thresholds, Build ID/calibration identity, criterion-satisfaction time, diagnostic-assertion time and calculated latency.

### Rationale

Measuring latency from a defined diagnostic criterion separates algorithm response time from an uncontrolled mechanical transition. Testing normal behavior as well as fault conditions prevents a trivially sensitive detector from passing latency requirements while producing unusable false alarms. The explicit current-based scope also avoids claiming mechanical stall confirmation from a system that intentionally has no speed sensor in Rev-1.

## Phase 13 work packages

The plan will define, at an appropriate product level:

1. verification levels and sequencing — **VER-001 accepted**;
2. requirements-to-verification traceability — **VER-002 accepted**;
3. calibration and complete-chain accuracy acceptance — **VER-003 accepted**;
4. noise and useful-resolution acceptance — **VER-004 accepted**;
5. AFE frequency-response and anti-alias acceptance — **VER-005 accepted**;
6. deterministic ADC sampling/timing acceptance — **VER-006 accepted**;
7. waveform/data-integrity and USB/MATLAB acceptance — **VER-007 accepted**;
8. diagnostic-feature, overload and stall acceptance — **VER-008 accepted**;
9. overrange, fault handling and protection checks;
10. power/grounding/integration checks;
11. build/configuration/calibration traceability evidence;
12. system-level acceptance and treatment of deviations;
13. final verification completeness review.

Additional verification groups may be introduced where the requirements/design baseline exposes a genuine acceptance gap.

## Completion criterion

Phase 13 is complete when every acceptance-relevant Rev-1 requirement and material design claim has a clear verification route and acceptance criterion, such that Stage C can execute the verification without inventing what constitutes a pass.
