# Phase 5 — Analog Front End and Anti-Alias Filter Design

**Status:** Design complete / baselined  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 5 defines the Rev-1 Analog Front End between the ACS724 sensor output and MCU ADC. The design preserves approximately unity gain while deliberately filtering content above the diagnostic band before sampling.

## Accepted design inputs

- ACS724 nominal valid output: approximately **0.5–4.5 V** for **0–5 A**.
- AFE residual-error allocation: **±15 mA / ±12 mV nominal equivalent**.
- Effective ADC-facing voltage resolution target: **≤2 mV**.
- Diagnostic passband: **DC–10 kHz**.
- At 10 kHz: attenuation target **≤1 dB**.
- At 50 kHz: attenuation target **≥20 dB**.
- Nominal sampling rate: **100 kS/s**.
- Active device: **MCP6022-I/P** dual RRIO op-amp.

## AFE-001 — Dual-op-amp unity-gain active low-pass AFE

**Status:** Accepted

Rev-1 uses both MCP6022 amplifiers as two cascaded second-order low-pass stages for an overall fourth-order response:

`ACS724 → 2nd-order active LPF → 2nd-order active LPF → ADC`

The AFE operates at approximately unity gain and introduces no intentional level shift.

## AFE-002 — Fourth-order Butterworth response at nominal 15 kHz cutoff

**Status:** Accepted

The accepted response is a **fourth-order Butterworth low-pass** with nominal overall cutoff:

`fc = 15 kHz`

The ideal response provides approximately 0.17 dB attenuation at 10 kHz and 41.8 dB at 50 kHz, satisfying the Phase 4 targets with margin.

## AFE-003 — Two Sallen-Key sections with tolerance-controlled components

**Status:** Accepted

The response is realized using two cascaded **unity-gain Sallen-Key** sections. Target Butterworth section Q values are approximately **0.5412** and **1.3066**.

Phase 12 subsequently froze the practical component realization:

| Section | R1 | R2 | C1 | C2 | Nominal f0 | Nominal Q |
|---|---:|---:|---:|---:|---:|---:|
| Low-Q | 9.76 kΩ | 9.76 kΩ | 1.2 nF | 1.0 nF | ≈14.89 kHz | ≈0.548 |
| High-Q | 4.07 kΩ | 4.07 kΩ | 6.8 nF | 1.0 nF | ≈15.00 kHz | ≈1.304 |

Use **1% resistors** and preferably **≤5% stable capacitors**. The calculated practical response remains compliant with the Phase 4 requirements.

The second MCP6022 output is the ADC-facing active buffer. Phase 12 finalized the downstream ADC isolation/interface network separately.

## Verification handoff

Implementation/verification shall confirm:

- no clipping over valid 0–5 A operation;
- DC/passband gain and offset remain within allocation;
- realized filter response satisfies the 10 kHz and 50 kHz requirements;
- ADC-facing drive/settling is acceptable;
- measured response replaces nominal assumptions where materially different.

**Phase 5 status: DESIGN COMPLETE / BASELINED**
