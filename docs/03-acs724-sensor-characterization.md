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

To document from primary sources:

- unidirectional operating range,
- zero-current output,
- sensitivity,
- output range,
- supply dependence / ratiometric behaviour where applicable,
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
