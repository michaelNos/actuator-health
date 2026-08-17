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

## 5.1 — AFE topology and buffering

### AFE-001 — Dual-op-amp unity-gain active low-pass AFE

**Status:** Accepted

Rev-1 shall use the available **MCP6022** as the active element of the Analog Front End, using both internal op-amps to implement two cascaded second-order low-pass stages for an overall **fourth-order** anti-alias response.

The AFE shall operate at approximately **unity gain** through the diagnostic passband. It shall not intentionally amplify, attenuate, or level-shift the ACS724 signal solely to occupy more ADC range.

The intended signal path is:

`ACS724 → 2nd-order active LPF → 2nd-order active LPF → ADC`

The active stages provide filtering and buffering between the sensor and ADC so that ADC input behavior does not directly load the ACS724 output/filter network.

Exact filter family, pole frequencies, Q values, resistor/capacitor values, and ADC-facing isolation details are resolved in the remaining Phase 5 design.

### Rationale

The native ACS724 span already uses most of a nominal 0–5 V ADC range, so extra gain provides little benefit and consumes headroom. A fourth-order response provides substantially more transition-band attenuation than a simple first-order RC network while the dual MCP6022 allows the complete active filter to be implemented with one available package.

## Phase 5 design topics remaining

### 5.2 — Anti-alias filter realization

Select filter family/order and cutoff that satisfy the accepted 10 kHz passband and 50 kHz attenuation targets.

**Status:** To be decided.

### 5.3 — ADC-input interface and protection handoff

Define the required ADC-facing drive/isolation behavior and identify protection requirements without duplicating the complete Phase 10 power/protection design.

**Status:** To be decided.

## Planned output

Phase 5 shall close with a coherent AFE schematic-level design basis including topology, filter response, component values/tolerances, expected signal range, error-budget compatibility and verification handoff.

No Phase 5 engineering decision is baselined until explicitly approved.
