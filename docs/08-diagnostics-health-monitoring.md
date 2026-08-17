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

## Phase 8 design topics

The phase will define a lean set of product-level choices covering:

- diagnostic state/output model;
- overload and stall/jam logic;
- startup/load/commutation-pattern condition interpretation;
- baseline/reference and threshold adaptation philosophy where needed;
- handling of invalid measurement-pipeline data and diagnostic confidence/availability.

Closely related choices will be grouped. Exact numeric thresholds that require the physical Rev-1 motor remain `TBD` with a defined calibration/verification method.

## Planned output

Phase 8 shall close with diagnostic logic sufficiently defined for Phase 7 firmware outputs to feed it and for Stage B implementation to tune motor-specific thresholds without redefining the diagnostic architecture.

No Phase 8 engineering decision is baselined until explicitly approved.
