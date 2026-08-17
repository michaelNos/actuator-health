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

## 8.3 — Healthy reference and current-pattern anomaly

### DIAG-003 — Deliberately calibrated, frozen healthy reference baseline

**Status:** Accepted

Rev-1 shall establish a **motor-specific healthy reference baseline** during implementation/characterization for use in current-signature condition comparison.

The reference may include, where demonstrated useful for the selected motor:

- normal running mean/RMS current under defined operating/load conditions;
- characteristic startup/inrush behavior;
- current-ripple characteristics;
- dominant spectral components and/or band-energy features in the accepted diagnostic band.

A **current-pattern anomaly** shall represent a significant, persistent deviation from the applicable healthy reference rather than deviation from a universal fixed spectral/ripple threshold.

The healthy reference shall be established deliberately from known-good operation and then treated as **frozen configuration/calibration data** during ordinary monitoring. Rev-1 shall not continuously adapt the healthy baseline to incoming operating data, because doing so could gradually normalize real degradation.

Updating the baseline shall require a deliberate recalibration/re-characterization action under known acceptable operating conditions.

Overload and stall/jam criteria remain explicit diagnostic mechanisms under DIAG-002; healthy-reference comparison supplements rather than replaces those fault criteria.

Exact reference values, allowable deviations, feature weighting and anomaly persistence remain `TBD` until implementation measurements identify useful motor-specific signatures.

### Rationale

Normal current signature depends strongly on the motor and mechanical operating condition. A motor-specific reference makes current-pattern diagnostics meaningful while freezing the accepted reference prevents gradual degradation from being learned as normal behavior.

## Phase 8 design topic remaining

Determine whether any additional diagnostic persistence/confidence/state-latching behavior materially affects the product architecture; otherwise Phase 8 can close without creating procedural detail.

## Planned output

Phase 8 shall close with diagnostic logic sufficiently defined for Phase 7 firmware outputs to feed it and for Stage B implementation to tune motor-specific thresholds without redefining the diagnostic architecture.

No Phase 8 engineering decision is baselined until explicitly approved.
