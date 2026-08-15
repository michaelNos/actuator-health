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

**Status:** In progress

Topics to establish:

- magnetic field produced by current,
- Hall effect,
- primary current conductor,
- Hall sensing element,
- galvanic isolation between the primary current path and low-voltage sensing electronics,
- internal signal-conditioning role of the ACS724,
- relationship between physical current and the analog output signal.

**Accepted Phase 3 decisions:** None yet.

## 3.2 — Exact ACS724-05AU variant

**Status:** TBD

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
