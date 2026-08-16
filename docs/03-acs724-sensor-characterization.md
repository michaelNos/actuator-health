# Phase 3 — ACS724 Sensor Theory and Characterization

**Status:** In progress  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 3 develops and experimentally validates the current-sensor model used by the Rev-1 laboratory prototype before the complete analog front end is designed.

The selected laboratory sensor is the Pololu #4048 carrier using the Allegro ACS724LLCTR-05AU Hall-effect current-sensor IC.

This phase shall distinguish clearly between datasheet facts, calculations, proposed engineering decisions, accepted decisions, and measured results. Unknown values remain **TBD** until derived or measured.

## Phase workflow

No Phase 3 engineering decision is accepted merely because it appears in discussion or as a proposal. Decisions are baselined in this document only after explicit approval.

The Phase 3 pull request remains a draft while the phase is being developed.

## 3.1 — Hall-effect current sensing

**Status:** Complete / accepted

### SENS-001 — Rev-1 Hall-effect current-sensing principle

**Status:** Accepted

Rev-1 shall use the selected ACS724 Hall-effect current sensor as an in-series current transducer. Actuator current shall flow through the sensor primary conductor, while the low-voltage sensing electronics shall derive an analog output from the current-generated magnetic field. The primary current path and low-voltage sensing electronics shall remain galvanically isolated through the sensor architecture.

### Rationale

The ACS724 measures the magnetic field produced by current flowing through its low-resistance primary copper conductor. Its Hall sensing and internal signal-conditioning electronics convert that magnetic information into an analog output voltage without a direct conductive signal connection to the primary current path.

This establishes two distinct electrical roles:

- **Primary/current path:** carries the physical actuator current through the sensor.
- **Measurement/signal side:** contains the low-voltage Hall sensing electronics and analog output that feed the later AFE and ADC stages.

The ACS724 is therefore inserted in series with the actuator-current path; it is not used as an external clamp around an untouched conductor.

## 3.2 — Exact ACS724-05AU variant

**Status:** In progress

### SENS-002 — Rev-1 sensor operating range and polarity

**Status:** Accepted

Rev-1 shall use the ACS724LLCTR-05AU within its specified **0 A to 5 A unidirectional sensing range**.

At a nominal sensor supply of 5 V, the nominal zero-current output is **0.5 V** and the nominal sensitivity is **800 mV/A**.

The unidirectional range means the specified measurement range is intended for one current polarity, which matches the normal current direction of the Rev-1 DC actuator. This does not imply that a DC-motor current waveform is constant: startup transients, commutation ripple, load variation and other time-varying components may still be present and are part of the waveform we intend to measure.

A current waveform that must be measured accurately in both positive and negative directions, such as a bipolar AC waveform or a reversing-current application, requires a sensing arrangement with an appropriate bidirectional range.

Values outside the specified 0 A to 5 A range shall not be treated as calibrated valid measurements merely because the sensor may continue to produce an output.

### Rationale

The selected 05AU variant allocates its useful analog output span to one current polarity. This provides 800 mV/A nominal sensitivity at 5 V, which is advantageous for resolving current changes in the Rev-1 low-voltage DC actuator while preserving the selected 0 A to 5 A Phase 1 measurement range.

Remaining topics to establish from primary sources:

- supply dependence / ratiometric behaviour,
- bandwidth,
- FILTER pin behaviour,
- primary conductor resistance,
- isolation ratings,
- working voltage versus dielectric-test voltage,
- temperature and error specifications.

## 3.3 — Sensor transfer function

**Status:** TBD

Derive the forward and inverse current/voltage relationships using the exact datasheet definitions for the selected ACS724 variant.

## 3.4 — Error mechanisms

**Status:** TBD

Characterize relevant sources including offset, sensitivity error, total output error, noise, temperature effects, supply variation, ADC contribution, and calibration influence.

A complete system numerical error budget is reserved for Phase 4 unless a Phase 3 calculation is needed to characterize the sensor itself.

## 3.5 — Bandwidth and FILTER pin

**Status:** TBD

Establish sensor bandwidth, the relationship between bandwidth and noise, FILTER-pin behaviour, and its interaction with the later AFE anti-alias filter.

## 3.6 — Characterization and test plan

**Status:** TBD

Define safe laboratory methods for measuring:

- zero-current output,
- output versus known current,
- linearity,
- noise,
- bandwidth where feasible.

The test method and known-current stimulus shall be defined before measurements are treated as evidence.

## 3.7 — Phase output

**Status:** TBD

The completed phase is expected to contain:

- sensor operating model,
- transfer equation,
- operating range and key limits,
- relevant error mechanisms,
- bandwidth and filtering behaviour,
- electrical/interface assumptions,
- characterization method,
- measured results when hardware is available,
- limitations and remaining TBD items.
