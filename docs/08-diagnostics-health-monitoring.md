# Phase 8 — Diagnostics / Health-Monitoring Logic

**Status:** In development  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 8 defines how Rev-1 interprets validated current-domain features as actuator operating-condition information and diagnostic states.

This phase establishes the product-level diagnostic model, baseline fault/condition logic and threshold-learning philosophy. Exact thresholds that depend on the selected motor and measured behavior remain `TBD` until implementation/verification rather than being invented during Stage A.

## Accepted design inputs

- calibrated **0–5 A** current measurement;
- time-domain features including mean, RMS, peak/minimum and peak-to-peak ripple;
- startup/inrush information;
- spectral/dominant-component or band-energy information over **0–10 kHz**;
- multi-timescale processing windows;
- explicit measurement-pipeline health/validity state;
- stall detection requirement: **≤100 ms after valid stall criteria**;
- sustained overload detection requirement: **≤1 s**;
- Rev-1 has no speed sensor, so stall/jam inference is current-based;
- automatic protective shutdown is not assumed; diagnostics and protection remain separate concepts.

## 8.1 — Diagnostic output model

### DIAG-001 — Separate operating state from condition assessment

**Status:** Accepted

Rev-1 diagnostics shall represent **operating state** separately from **condition assessment** rather than reducing all behavior to a single OK/fault flag.

The baseline operating-state model shall distinguish:

- stopped / no-load-current region;
- startup;
- running;
- abnormal or unknown operating state when available evidence does not support a normal state classification.

The baseline condition assessment shall distinguish:

- normal;
- overload;
- stall/jam;
- current-pattern anomaly;
- diagnostic unavailable.

This separation allows current behavior to be interpreted in context. For example, a high-current transient during startup may be normal while similar current persisting during the running state may indicate overload or stall/jam.

If the Phase 7 measurement-pipeline health state indicates that required evidence is invalid, the appropriate result is **diagnostic unavailable**, not an actuator fault inferred from compromised data.

Exact motor-dependent state-transition thresholds remain `TBD` until implementation/verification.

### Rationale

Current magnitude alone is not sufficient to interpret actuator condition. Separating operating state from condition assessment prevents expected transient behavior from being misclassified and provides a clear representation for unavailable diagnostics when the monitoring system itself cannot supply trustworthy evidence.

## 8.2 — Overload and stall/jam logic

### DIAG-002 — Persistent multi-feature fault detection

**Status:** Accepted

Rev-1 shall distinguish **overload** from **stall/jam** using operating context, persistence and current-signal features rather than treating any instantaneous high-current sample as a fault.

**Overload** shall primarily be inferred from elevated load-current behavior that exceeds a motor-specific overload criterion for a required persistence interval while the actuator is in an applicable operating state. The logic shall be designed to satisfy the accepted **≤1 s sustained-overload detection latency** once valid overload criteria are present.

Conceptually:

`elevated load current + persistence + applicable operating state → overload`

**Stall/jam** shall use combined current evidence because Rev-1 has no speed sensor. The baseline inference shall require high-current behavior together with a significant loss/change of the normal commutation/current-ripple pattern and persistence consistent with the accepted **≤100 ms stall-detection latency** after valid stall criteria are present.

Conceptually:

`high current + current-pattern change + persistence + applicable operating state → stall/jam`

Startup shall be treated as a distinct operating context so that expected startup/inrush current does not automatically satisfy running-state overload or stall criteria.

Exact current thresholds, persistence values within the accepted latency limits, and quantitative current-pattern criteria remain `TBD` until the selected Rev-1 motor is characterized during implementation/verification.

A detected overload or stall/jam is a **diagnostic result**, not automatically a protective shutdown command. Any active shutdown/protection behavior requires separate design and validation.

### Rationale

High current can occur normally during startup or changing load, so magnitude alone is insufficient. Combining persistence and operating context reduces false positives. For stall/jam, adding current-pattern evidence provides an independent current-domain indication of changed mechanical/electrical behavior when no speed sensor is available.

## Phase 8 design topics remaining

- startup/load/commutation-pattern condition interpretation beyond the explicit overload/stall cases;
- baseline/reference and threshold adaptation philosophy;
- handling of diagnostic persistence/confidence where it materially affects product behavior.

Closely related choices will be grouped. Exact numeric thresholds that require the physical Rev-1 motor remain `TBD` with a defined calibration/verification method.

## Planned output

Phase 8 shall close with diagnostic logic sufficiently defined for Phase 7 firmware outputs to feed it and for Stage B implementation to tune motor-specific thresholds without redefining the diagnostic architecture.

No Phase 8 engineering decision is baselined until explicitly approved.
