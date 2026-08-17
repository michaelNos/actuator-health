# Phase 5 — Analog Front End and Anti-Alias Filter Design

**Status:** In development  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 5 defines the Rev-1 Analog Front End between the ACS724 sensor output and the MCU ADC input. It shall implement the accepted Phase 4 signal-range, error-budget and anti-alias requirements without unnecessarily rescaling the sensor signal.

This phase selects the product-level AFE topology, buffering/filter strategy and component-level design needed for a buildable Rev-1. Exact physical wiring, scope setup and implementation/debug procedure remain deferred to Stage B.

## Accepted design inputs

- ACS724 nominal valid output: approximately **0.5–4.5 V** for **0–5 A** at nominal 5 V supply.
- Preserve approximately unity DC/passband gain.
- Valid 0–5 A operation shall not clip.
- AFE residual-error allocation: **±15 mA**, nominally **±12 mV** equivalent.
- Effective ADC-facing voltage resolution target: **≤2 mV**.
- Diagnostic passband: **DC–10 kHz**.
- At 10 kHz: attenuation target **≤1 dB**.
- At 50 kHz: attenuation target **≥20 dB**.
- Nominal sampling rate: **100 kS/s**.
- MCP6022-I/P is available: dual RRIO op-amp, approximately 10 MHz GBW, 2.5–5.5 V supply.

## Phase 5 design topics

### 5.1 — AFE topology and buffering

Select the signal path between ACS724 and ADC, including whether/how the MCP6022 is used and how ADC loading is isolated from the sensor/filter network.

**Status:** To be decided.

### 5.2 — Anti-alias filter realization

Select filter family/order and cutoff that satisfy the accepted 10 kHz passband and 50 kHz attenuation targets.

**Status:** To be decided.

### 5.3 — ADC-input interface and protection handoff

Define the required ADC-facing drive/isolation behavior and identify protection requirements without duplicating the complete Phase 10 power/protection design.

**Status:** To be decided.

## Planned output

Phase 5 shall close with a coherent AFE schematic-level design basis including topology, filter response, component values/tolerances, expected signal range, error-budget compatibility and verification handoff.

No Phase 5 engineering decision is baselined until explicitly approved.
