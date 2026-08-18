# Phase 5 — Analog Front End and Anti-Alias Filter Design

**Status:** Design complete / baselined  
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

### Rationale

The native ACS724 span already uses most of a nominal 0–5 V ADC range, so extra gain provides little benefit and consumes headroom. A fourth-order response provides substantially more transition-band attenuation than a simple first-order RC network while the dual MCP6022 allows the complete active filter to be implemented with one available package.

## 5.2 — Anti-alias filter realization

### AFE-002 — Fourth-order Butterworth response at nominal 15 kHz cutoff

**Status:** Accepted

The Rev-1 AFE shall implement an overall **fourth-order Butterworth low-pass response** using the two cascaded second-order active stages established by AFE-001.

The nominal overall cutoff frequency shall be:

`fc = 15 kHz`

For an ideal fourth-order Butterworth response this gives approximately:

- attenuation at **10 kHz**: **0.17 dB**;
- attenuation at **50 kHz**: **41.8 dB**.

This provides margin against the Phase 4 requirements of no more than 1 dB attenuation at 10 kHz and at least 20 dB attenuation at 50 kHz.

Butterworth is selected because its monotonic, maximally flat magnitude response avoids deliberate passband ripple in the current-signature measurement band.

The available MCP6022, with approximately 10 MHz gain-bandwidth product, has substantial bandwidth margin relative to the 15 kHz filter frequency. Practical response including op-amp behavior and component tolerances shall nevertheless be verified during implementation.

### Rationale

The 15 kHz nominal cutoff leaves the complete DC–10 kHz diagnostic band comfortably inside the passband while a fourth-order response provides strong attenuation before the 50 kHz Nyquist frequency.

## 5.3 — Component realization, ADC interface and protection handoff

### AFE-003 — Two Sallen-Key sections with tolerance-controlled components

**Status:** Accepted

The fourth-order Butterworth response shall be realized as two cascaded **unity-gain Sallen-Key** second-order sections using the two MCP6022 amplifiers.

The normalized Butterworth section quality factors are:

- `Q1 ≈ 0.5412`;
- `Q2 ≈ 1.3066`.

The two sections therefore shall not be treated as two identical generic RC filters. Their resistor/capacitor ratios shall be selected to realize the required pole Q values at the nominal 15 kHz design frequency.

The schematic/BOM realization shall use **1% resistors** and suitably tolerance-controlled capacitors. Final standard R/C values shall be documented in the Phase 12 build specification after the practical component set is reconciled with availability; their calculated response must remain compliant with the accepted Phase 4 limits.

The output of the second MCP6022 stage shall serve as the ADC-facing active buffer. Any small series isolation component required by the RA4M1 ADC input and the final abnormal-voltage clamp/protection network shall be finalized using the ADC requirements of Phase 6 and protection design of Phase 10 rather than being independently optimized in Phase 5.

The intended DC/passband gain remains approximately unity and no intentional level shift is introduced.

### Verification handoff

Implementation/verification shall confirm:

- no clipping over the valid 0–5 A measurement range;
- practical DC/passband gain and offset contribution remain within the AFE error allocation;
- the realized filter satisfies the 10 kHz and 50 kHz attenuation requirements;
- the ADC-facing signal is stable and free from problematic drive/settling behavior;
- measured component/filter behavior is used where it differs materially from nominal calculation.

## Phase 5 design status

AFE-001 through AFE-003 define the product-level Rev-1 AFE architecture. Detailed physical wiring, final build-layout choices, ADC-specific isolation/protection details and measured response remain assigned to the later design/build/verification phases under DEV-001.

## Planned output

Phase 5 closes with a coherent AFE design basis covering topology, target filter response, section realization, component-tolerance expectations, ADC buffering and verification handoff.
