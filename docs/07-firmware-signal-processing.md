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

## 7.1 — Firmware data-flow architecture

### FW-001 — Layered producer/consumer processing pipeline

**Status:** Accepted

Rev-1 firmware shall separate acquisition, signal processing, diagnostics and communication so that variable application workload cannot disturb the deterministic ADC sample cadence.

The primary data flow is:

`ADC acquisition → raw sample buffer → calibration → signal processing → diagnostics → communication`

Firmware responsibilities are divided into three timing classes:

1. **Hard real-time acquisition** — hardware timer, ADC and DMA/DTC establish and preserve the 100 kS/s sample stream. Application code shall not control individual sample timing.
2. **Buffer-rate processing** — completed sample buffers are validated, converted into calibrated current-domain data, and used for feature extraction.
3. **Background/non-real-time work** — communication, reporting, commands and other non-critical tasks operate without becoming part of the acquisition timing path.

The calibrated current conversion shall retain explicit calibration parameters such as measured offset and sensitivity rather than embedding nominal sensor constants as immutable assumptions.

Each completed data block shall carry validity/status information sufficient to identify conditions such as acquisition overrun, invalid measurement range or other known data-integrity faults. Invalid or incomplete blocks shall not silently propagate into later diagnostic decisions as though they were trustworthy measurements.

### Rationale

This layered producer/consumer structure preserves deterministic sampling while allowing processing and communication workloads to vary. It also maintains traceability from raw ADC data to calibrated current, features and diagnostics, and gives later stages an explicit mechanism for rejecting compromised data.

## 7.2 — Calibrated-current and feature interface

### FW-002 — Compact calibrated-current + diagnostic-feature data product

**Status:** Accepted

Each valid completed acquisition block shall be transformed into a consistent current-domain data product containing the information needed by later diagnostics without coupling those diagnostics to raw ADC codes.

The calibrated-current representation shall retain:

- calibrated current samples derived from the active offset/sensitivity calibration;
- sample-rate/timing identity sufficient to interpret the samples correctly;
- validity and quality state, including known overrange and acquisition-overrun conditions.

From valid calibrated-current data, the signal-processing layer shall provide a compact baseline feature set for Phase 8:

- mean current;
- RMS current;
- peak and minimum current;
- peak-to-peak current ripple;
- startup/inrush peak when the operating context requires it;
- frequency-domain information over the accepted **0–10 kHz** diagnostic band;
- dominant spectral components and/or band-energy information suitable for detecting changes in commutation/current-pattern behavior.

The architecture intentionally does not freeze exact FFT length, window function, spectral-bin count, DSP library, numerical representation or optimization strategy during Stage A. Those choices shall be made during implementation where they can be reconciled with RA4M1 memory/CPU performance and measured motor behavior.

Feature outputs shall inherit the validity of the source data. Features derived from a known invalid/incomplete acquisition block shall not be presented to diagnostics as valid evidence.

### Rationale

The diagnostic layer should operate on physical current quantities and meaningful signal features rather than ADC implementation details. A compact interface also avoids prematurely implementing a large collection of metrics before measurements show which features are useful for the selected Rev-1 motor.

## Phase 7 design topics remaining

- define processing-window/data-product behavior only where it materially affects architecture;
- define firmware observability and failure handling needed to trust the measurement pipeline.

The number of formal decisions is intentionally not fixed. Closely related choices will be grouped and implementation details deferred.

## Planned output

Phase 7 shall close with a firmware and signal-processing architecture that Phase 8 diagnostics can consume and Stage B can implement without redefining the fundamental data flow.

No Phase 7 engineering decision is baselined until explicitly approved.
