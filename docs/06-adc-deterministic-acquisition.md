# Phase 6 — ADC and Deterministic Acquisition Design

**Status:** Design complete  
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

## 6.2 — Deterministic sampling trigger

### ADC-002 — Hardware-timer-triggered 100 kS/s acquisition

**Status:** Accepted

Rev-1 shall establish the ADC sampling cadence using a **hardware timer trigger**, not by repeatedly calling a blocking/high-level ADC read function from the application loop.

The nominal sampling period is:

`Ts = 1 / 100 kS/s = 10 µs`

A hardware timer shall generate the periodic conversion trigger so that ADC sample timing is independent of main-loop execution time, communication activity and ordinary application workload.

The intended timing architecture is:

`hardware timer → periodic 10 µs trigger → ADC conversion`

The exact RA4M1 timer peripheral/channel, event routing, ADC registers and low-level configuration are implementation details deferred to Stage B. Phase 7 firmware architecture shall treat this hardware-timed sample cadence as the authoritative acquisition clock.

Implementation/verification shall measure the achieved sample rate and timing stability/jitter rather than assuming that configuration values alone prove deterministic behavior.

### Rationale

Current-signature and frequency-domain analysis depend on known, regular sample spacing. Software-loop timing can vary with interrupts, processing and communication and therefore is not an acceptable source of the 100 kS/s acquisition clock. Hardware triggering decouples conversion timing from those variable workloads.

## 6.3 — Sample transfer and buffering

### ADC-003 — Hardware-assisted transfer with double buffering

**Status:** Accepted

Completed ADC samples shall be transferred into RAM using a **hardware-assisted transfer mechanism**, preferably the RA4M1 DMA/DTC capability, rather than requiring application code to service every sample synchronously.

Rev-1 shall use a **double-buffer (ping-pong) acquisition concept**:

1. the acquisition hardware fills one sample buffer;
2. firmware may process or consume the other completed buffer;
3. when the active buffer is complete, the buffer roles swap;
4. acquisition timing remains governed by the hardware trigger established in ADC-002.

The architecture is therefore conceptually:

`timer → ADC → DMA/DTC → RAM buffer A/B`

with processing, diagnostics and communication operating on completed buffers rather than controlling individual conversion timing.

The exact DMA/DTC channel, transfer configuration, interrupt arrangement, buffer length and memory layout are implementation/Phase 7 details.

If firmware cannot consume completed buffers before they are reused, the system shall detect and report an **acquisition overrun/data-loss condition**. Samples shall not be silently overwritten while downstream logic continues as though the stream were complete.

### Rationale

At 100 kS/s a new sample is produced every 10 µs. Hardware-assisted transfer and double buffering decouple this fixed-rate acquisition from variable processing and communication workload, reduce per-sample CPU burden, and provide a clear boundary for detecting inability to keep pace with the acquisition stream.

## Verification handoff

Implementation and verification shall demonstrate:

- actual 100 kS/s sample cadence and acceptable timing stability;
- effective ADC-domain voltage resolution of 2 mV or better under intended conditions;
- correct sample ordering and buffer transitions;
- absence of silent sample loss;
- explicit detection of forced/real buffer-overrun conditions;
- no clipping throughout the valid ADC-facing signal range.

## Phase 6 design status

ADC-001 through ADC-003 define the product-level Rev-1 ADC and deterministic acquisition architecture. Register configuration, exact timer/event/DMA selection, buffer sizing and implementation debugging remain deliberately deferred under DEV-001.

## Planned output

Phase 6 closes with a coherent ADC/acquisition architecture that Phase 7 firmware can implement deterministically and later verify for sample rate, jitter, useful resolution, overrun behavior and data integrity.
