# Phase 4 — Measurement-Chain Requirements and Error-Budget Allocation

**Status:** Design complete / baselined  
**Project:** Actuator Health Monitoring System

Phase 4 is complete and baselined. It defines the accepted Rev-1 measurement-chain requirements, including the approximately 0.5–4.5 V valid sensor span for 0–5 A, unity-gain signal-chain strategy, ≤ ±0.10 A calibrated system target and subsystem error allocation, ≤2 mV effective ADC-facing resolution requirement, DC–10 kHz diagnostic band, and quantitative anti-alias handoff requirements of ≤1 dB attenuation at 10 kHz and ≥20 dB attenuation at 50 kHz.

Hardware-dependent offset, sensitivity, noise, supply, temperature and practical ADC/AFE behavior remain implementation/verification quantities under DEV-001 rather than unclosed design decisions.

## Accepted quantitative baseline

- Current measurement range: **0–5 A**, unidirectional.
- Nominal sensor signal: approximately **0.5–4.5 V**.
- Preserve approximately unity DC/passband gain.
- System current accuracy after calibration: **≤ ±0.10 A**.
- Stretch target: **±0.05 A**, claimable only if verified.
- Reported current resolution: **≤10 mA**.
- Effective ADC-facing voltage resolution requirement: **≤2 mV**.
- Diagnostic bandwidth: **DC–10 kHz**.
- Nominal sample rate: **100 kS/s**, Nyquist **50 kHz**.
- Anti-alias target at 10 kHz: **≤1 dB attenuation**.
- Anti-alias target at 50 kHz: **≥20 dB attenuation**.
- Values outside 0–5 A are overrange/invalid measurements even if electronics still produce an ADC code.
- Electrical survival and calibrated measurement validity are separate requirements.

## Accepted conservative error allocation

| Contributor | Current-domain allocation | Nominal voltage equivalent |
|---|---:|---:|
| Sensor + calibration residual | ±50 mA | ±40 mV |
| AFE residual error | ±15 mA | ±12 mV |
| ADC/reference residual error | ±10 mA | ±8 mV |
| Noise contribution | ±10 mA | ±8 mV |
| Supply/temperature and other residual effects | ±15 mA | ±12 mV |
| **Worst-case total** | **±100 mA** | **±80 mV** |

These are design allocations, not measured-performance claims. Verification must populate the actual contributions.

## Verification handoff

Later implementation/verification shall establish actual sensor calibration residual, AFE gain/offset and filter behavior, ADC useful resolution/reference behavior, noise, supply/temperature influence, valid-range clipping margin and overrange behavior.

**Phase 4 status: DESIGN COMPLETE / BASELINED**
