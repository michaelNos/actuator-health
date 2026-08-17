# Phase 6 — ADC and Deterministic Acquisition Design

**Status:** In development  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 6 defines how Rev-1 converts the filtered analog current signal into a deterministic digital sample stream on the Arduino UNO R4 WiFi / Renesas RA4M1.

This phase establishes the product-level ADC resolution/reference strategy, deterministic 100 kS/s timing architecture, and sample-transfer/buffering concept. Register-level implementation and debugging remain deferred to Stage B.

## Accepted design inputs

- ADC-facing nominal valid signal: approximately **0.5–4.5 V**.
- Required diagnostic band: **DC–10 kHz**.
- Nominal sampling rate: **100 kS/s**, giving `Ts = 10 µs` and Nyquist = **50 kHz**.
- Effective ADC-facing voltage resolution requirement: **≤2 mV**.
- ADC/reference residual-error allocation: **±10 mA**, nominally **±8 mV** equivalent.
- AFE: buffered fourth-order Butterworth low-pass, nominal **15 kHz** cutoff.
- Main MCU: **Renesas RA4M1**, 48 MHz, ADC capable of up to 14-bit conversion.
- Ordinary high-level `analogRead()` behavior shall not be assumed to provide deterministic 100 kS/s acquisition.

## Phase 6 design topics

### 6.1 — ADC operating resolution and reference strategy

Select the Rev-1 ADC operating mode and reference/supply relationship needed to meet useful resolution and accuracy requirements.

**Status:** To be decided.

### 6.2 — Deterministic sampling trigger

Define the hardware-timed architecture that establishes the 100 kS/s sample cadence independently of application-loop timing.

**Status:** To be decided.

### 6.3 — Sample transfer and buffering

Define how completed ADC samples move into memory and how acquisition is decoupled from later processing/communication without requiring register-level implementation detail yet.

**Status:** To be decided.

## Planned output

Phase 6 shall close with a coherent ADC/acquisition architecture that Phase 7 firmware can implement deterministically and later verify for sample rate, jitter, useful resolution, overrun behavior and data integrity.

No Phase 6 engineering decision is baselined until explicitly approved.
