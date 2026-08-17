# Phase 7 — MCU Firmware and Signal-Processing Architecture

**Status:** In development  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 7 defines the Rev-1 firmware architecture that consumes deterministic ADC buffers, converts raw measurements into calibrated current-domain data, extracts useful current-signal features, and supplies the later diagnostic and communication layers.

This phase defines product-level firmware responsibilities and data flow. Register-level code, exact buffer sizes, DSP implementation details, optimization and debugging remain deferred to Stage B.

## Accepted design inputs

- deterministic **100 kS/s** ADC acquisition;
- 14-bit ADC conversion baseline with measured effective performance required;
- hardware-timer-triggered conversions;
- hardware-assisted transfer into double-buffered RAM;
- explicit acquisition-overrun detection;
- current signal band **DC–10 kHz**;
- calibrated current range **0–5 A**;
- current conversion based on measured/calibrated offset and sensitivity;
- required support for time-domain and frequency-domain current-signature analysis;
- later diagnostics must support load, startup/inrush, overload, stall/jam and current-pattern behavior.

## Phase 7 design topics

The phase will define only the firmware choices needed to make Rev-1 coherent and implementable, including:

- acquisition/data-flow ownership and separation of real-time from non-real-time work;
- raw ADC to calibrated-current conversion and data-quality flags;
- signal-processing feature set/interface needed by diagnostics;
- processing-window/data-product strategy where it materially affects the architecture;
- fault/overrun handling and observability needed for trustworthy measurements.

The number of formal decisions is intentionally not fixed. Closely related choices will be grouped and implementation details deferred.

## Planned output

Phase 7 shall close with a firmware and signal-processing architecture that Phase 8 diagnostics can consume and Stage B can implement without redefining the fundamental data flow.

No Phase 7 engineering decision is baselined until explicitly approved.
