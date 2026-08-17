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

## 6.1 — ADC operating resolution and reference strategy

### ADC-001 — 14-bit conversion baseline with measured effective performance

**Status:** Accepted

Rev-1 shall use the RA4M1 ADC in **14-bit conversion mode** as the design baseline.

For a nominal 5 V full-scale ADC range, ideal quantization is approximately:

- 12-bit: `5 V / 4096 ≈ 1.22 mV/LSB`;
- 14-bit: `5 V / 16384 ≈ 0.305 mV/LSB`.

Both are nominally below the accepted **2 mV effective usable voltage-resolution requirement**, but 14-bit operation provides additional quantization margin and is available in the selected MCU.

Nominal bit depth shall not be treated as effective resolution or measurement accuracy. ADC noise, reference/supply behavior, source settling, timing and other practical effects shall be characterized during implementation/verification. The system must demonstrate the accepted ≤2 mV useful-resolution requirement under its actual acquisition conditions.

No oversampling is required merely to satisfy the nominal Phase 4 resolution requirement. Oversampling or averaging may later be used for specific low-bandwidth measurements only if it does not compromise the required signal information.

The final ADC reference/supply implementation shall be coordinated with the Phase 10 power design because the ACS724 transfer is ratiometric with its supply. Phase 6 therefore establishes the conversion-resolution baseline without prematurely claiming an exact reference voltage or reference accuracy.

### Rationale

Using the MCU's available 14-bit mode provides comfortable quantization margin without requiring an external ADC solely for resolution. Explicitly separating nominal converter bits from measured effective performance preserves the system-level accuracy and resolution requirements.

## Phase 6 design topics remaining

### 6.2 — Deterministic sampling trigger

Define the hardware-timed architecture that establishes the 100 kS/s sample cadence independently of application-loop timing.

**Status:** To be decided.

### 6.3 — Sample transfer and buffering

Define how completed ADC samples move into memory and how acquisition is decoupled from later processing/communication without requiring register-level implementation detail yet.

**Status:** To be decided.

## Planned output

Phase 6 shall close with a coherent ADC/acquisition architecture that Phase 7 firmware can implement deterministically and later verify for sample rate, jitter, useful resolution, overrun behavior and data integrity.

No Phase 6 engineering decision is baselined until explicitly approved.
