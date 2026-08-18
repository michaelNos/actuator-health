# Phase 12 — System Integration, Wiring, BOM and Build Specification

**Status:** In development  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 12 converts the accepted subsystem designs from Phases 1–11 into one coherent, buildable Rev-1 specification.

Unlike the preceding architecture phases, this phase intentionally goes deeper. It shall freeze enough integration detail that another engineer could identify the required hardware, understand every subsystem boundary, wire the Rev-1 correctly, know which values/interfaces are fixed versus TBD, and proceed into Stage B without inventing missing product architecture.

Phase 12 still does **not** perform the physical build, firmware implementation, calibration or laboratory verification. Those activities remain after the Rev-1 design freeze.

## Accepted design baseline entering Phase 12

- Rev-1 actuator/motor: **≤24 V DC** laboratory operation.
- Calibrated current range: **0–5 A**, unidirectional.
- Current sensor: **Pololu #4048 / ACS724LLCTR-05AU**.
- Diagnostic band: **DC–10 kHz**; deterministic ADC baseline: **100 kS/s**.
- MCU: **Arduino UNO R4 WiFi / Renesas RA4M1**.
- AFE: **MCP6022-I/P**, approximately unity gain.
- System accuracy after calibration: **≤ ±0.10 A**, stretch **±0.05 A**.
- Reported-current resolution: **≤10 mA**.
- USB serial is the Rev-1 PC/MATLAB interface.
- Automatic motor shutdown is not part of Rev-1; bench-PSU current limiting is the initial active motor-current protection.
- Rev-1 hobby hardware shall never be connected directly to industrial mains or a 400 V motor circuit.

## 12.1 — Integrated Rev-1 topology and physical partitioning

### INT-001 — Four-region integrated system topology

**Status:** Accepted

Rev-1 is partitioned into:

1. **Actuator/high-current region** — bench PSU, current-rated wiring/connectors, ACS724 primary path and motor.
2. **Analog measurement region** — ACS724 secondary side, MCP6022 AFE, anti-alias filtering and ADC interface/protection.
3. **Digital/processing region** — UNO R4 / RA4M1 for deterministic acquisition, processing, diagnostics and communication.
4. **Host region** — USB-connected PC/MATLAB for telemetry, waveform capture, calibration and engineering analysis.

Integrated signal path:

`motor current → ACS724 → VOUT → AFE/anti-alias filter → ADC → MCU → USB → PC/MATLAB`

The ACS724 primary conductor separates the multi-ampere actuator-current path from the low-voltage measurement signal chain. This partition does not imply that all laboratory regions are mutually galvanically isolated.

## 12.2 — Actuator current-path wiring architecture

### INT-002 — Dedicated high-side sensor current path with fixed polarity convention

**Status:** Accepted

Current path:

`bench PSU (+) → ACS724 IP+ → ACS724 IP− → motor (+) → motor (−) → bench PSU (−)`

Dedicated insulated current-rated conductors/connectors shall be used. Motor current shall not pass through a solderless breadboard, MCU header wiring or measurement-ground conductors. Connections shall be mechanically secure and strain relieved.

The **0–5 A** range is the calibrated measurement range, not a continuous-current target or survival rating. Bidirectional/regenerative current characterization is outside Rev-1 scope.

**Procurement dependency:** the exact motor and current-rated wiring/connectors are not yet selected/available. Exact conductor gauge and connector type shall be frozen after INT-011 establishes the motor electrical envelope.

## 12.3 — Measurement-electronics power distribution

### INT-003 — UNO-derived coherent 5 V measurement domain

**Status:** Accepted

Normal development power topology:

`USB-C → UNO R4 WiFi → UNO +5 V header → ACS724 VCC + MCP6022 VDD`

with:

`UNO GND → ACS724 GND + MCP6022 VSS/GND + ADC measurement reference domain`

The motor remains exclusively on the separate bench-PSU actuator path.

The actual measurement rail is approximately 5 V and shall be characterized during implementation/calibration rather than assumed to equal exactly 5.000 V. No external precision 5 V regulator/reference is required unless measured performance later demonstrates it is necessary to satisfy the accepted accuracy requirement.

Independent external 5 V sources shall not be paralleled with the UNO rail by assumption.

## 12.4 — Ground/reference and laboratory-instrument architecture

### INT-004 — Common measurement ground with designated analog test points

**Status:** Accepted

`GND_MEAS = GND_UNO = GND_AFE = GND_ACS724-secondary`

The motor-current return remains a separate high-current conductor to the bench PSU.

Required identified test points:

- `TP_GND` — measurement reference;
- `TP_5V` — measurement rail;
- `TP_SENSOR` — raw ACS724 VOUT;
- `TP_AFE` — filtered AFE output toward the ADC.

Ordinary single-ended probing of the low-voltage analog chain references `TP_GND`. Oscilloscope/function-generator grounds shall not be assumed floating. Ordinary probe grounds shall not be casually connected to actuator-current nodes such as `PSU+`, `IP+` or `IP−`. Differential/high-current measurements require an appropriate verified method during Stage B.

## 12.5 — ACS724 secondary-side interface

### INT-005 — Direct sensor-to-AFE interface with stock FILTER and local decoupling

**Status:** Accepted

`5V_MEAS → ACS724 VCC`

`GND_MEAS → ACS724 GND`

`ACS724 VOUT → TP_SENSOR → AFE input`

The Pololu carrier's stock **1 nF FILTER capacitor remains unchanged**, preserving the accepted approximately 90 kHz carrier bandwidth. It is not the ADC anti-alias filter.

Provide **100 nF ceramic local bypass capacitance** between sensor VCC and GND close to the carrier supply connection. No additional gain/divider/offset network is inserted before the accepted AFE. `TP_SENSOR` exposes the raw sensor output before deliberate AFE filtering.

## 12.6 — AFE implementation and component-value freeze

Phase 5 established a fourth-order Butterworth low-pass AFE using the two MCP6022 amplifiers as cascaded unity-gain Sallen-Key second-order sections, with nominal overall cutoff near **15 kHz**. Phase 12 freezes the practical realization.

### INT-006A — Unity-gain Sallen-Key section realization

**Status:** Accepted

Both second-order sections shall use the unity-gain Sallen-Key low-pass topology with equal resistor pairs within each section. For this realization:

`f0 = 1 / (2π R sqrt(C1 C2))`

`Q = 0.5 sqrt(C1 / C2)`

The fourth-order Butterworth sections target:

- low-Q section: `Q1 ≈ 0.5412`;
- high-Q section: `Q2 ≈ 1.3066`.

The sections therefore deliberately use different capacitor ratios; they shall not be implemented as two identical RC networks.

### INT-006B — Standard component values and nominal response

**Status:** Accepted

The Rev-1 filter values are frozen as:

| Section | R1 | R2 | C1 | C2 | Nominal f0 | Nominal Q |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Low-Q | 9.76 kΩ | 9.76 kΩ | 1.2 nF | 1.0 nF | ≈14.89 kHz | ≈0.548 |
| High-Q | 4.07 kΩ | 4.07 kΩ | 6.8 nF | 1.0 nF | ≈15.00 kHz | ≈1.304 |

Use **1% resistors** and preferably **≤5% tolerance capacitors** suitable for stable filter use.

The nominal cascaded response is approximately:

- **10 kHz:** `−0.124 dB`;
- **15 kHz:** `−2.99 dB`;
- **50 kHz:** `−41.9 dB`.

This satisfies the accepted Phase 4 limits of no more than 1 dB attenuation at 10 kHz and at least 20 dB attenuation at the 50 kHz Nyquist frequency with substantial nominal margin.

The exact E96 resistor values and tolerance-controlled capacitors are treated as BOM items if not already available. The design shall not be degraded merely to use unsuitable assortment parts. Actual filter response and component tolerances shall be verified during implementation.

### INT-006C — MCP6022 channel allocation, supply and decoupling

**Status:** Accepted

The MCP6022-I/P dual op-amp shall implement the two Sallen-Key sections in this signal order:

`ACS724 VOUT → low-Q section → high-Q section → TP_AFE → ADC interface`

Channel allocation:

- **MCP6022 channel A:** low-Q section (`Q ≈ 0.548`);
- **MCP6022 channel B:** high-Q section (`Q ≈ 1.304`).

The low-Q-first/high-Q-second ordering is frozen for Rev-1.

Power connections:

- `MCP6022 VDD → 5V_MEAS`;
- `MCP6022 VSS → GND_MEAS`.

Provide:

- **100 nF ceramic local bypass capacitor** directly between MCP6022 VDD and VSS, physically close to the IC supply pins;
- **10 µF bulk/local reservoir capacitor** between `5V_MEAS` and `GND_MEAS` near the AFE analog section.

### INT-006D — Complete MCP6022 PDIP-8 net-level AFE circuit and headroom

**Status:** Accepted

The MCP6022-I/P PDIP-8 pin allocation is frozen as:

| Pin | Function | Rev-1 connection |
| ---: | --- | --- |
| 1 | OUTA | low-Q stage output / Stage B input |
| 2 | IN−A | tied to pin 1 for unity-gain follower |
| 3 | IN+A | low-Q Sallen-Key input node `N2A` |
| 4 | VSS | `GND_MEAS` |
| 5 | IN+B | high-Q Sallen-Key input node `N2B` |
| 6 | IN−B | tied to pin 7 for unity-gain follower |
| 7 | OUTB | `TP_AFE` / ADC-interface source |
| 8 | VDD | `5V_MEAS` |

#### Low-Q stage — channel A

Net-level connections:

`TP_SENSOR / ACS724 VOUT → R1A 9.76 kΩ → N1A`

`N1A → R2A 9.76 kΩ → N2A → MCP6022 pin 3 (IN+A)`

`N2A → C2A 1.0 nF → GND_MEAS`

`N1A → C1A 1.2 nF → MCP6022 pin 1 (OUTA)`

`MCP6022 pin 1 (OUTA) → MCP6022 pin 2 (IN−A)`

Pin 1 is also the source feeding the second filter stage.

#### High-Q stage — channel B

Net-level connections:

`MCP6022 pin 1 (OUTA) → R1B 4.07 kΩ → N1B`

`N1B → R2B 4.07 kΩ → N2B → MCP6022 pin 5 (IN+B)`

`N2B → C2B 1.0 nF → GND_MEAS`

`N1B → C1B 6.8 nF → MCP6022 pin 7 (OUTB)`

`MCP6022 pin 7 (OUTB) → MCP6022 pin 6 (IN−B)`

`MCP6022 pin 7 (OUTB) → TP_AFE → ADC interface`

The `C1A` and `C1B` capacitors are deliberately connected between the first resistor-junction node and the corresponding op-amp output; they are not additional shunt capacitors to ground. These feedback connections are required by the selected unity-gain Sallen-Key realization.

#### Supply and local decoupling

`pin 8 (VDD) → 5V_MEAS`

`pin 4 (VSS) → GND_MEAS`

A **100 nF ceramic capacitor** shall be connected locally between pins 8 and 4. The accepted **10 µF** analog-section reservoir capacitor shall be connected between `5V_MEAS` and `GND_MEAS` near the AFE.

#### Voltage/headroom check

The nominal valid ACS724/AFE signal range is approximately:

`0.5 V ≤ V_AFE ≤ 4.5 V`

with an approximately 5 V MCP6022 supply. This leaves approximately **0.5 V nominal headroom from each supply rail**. The accepted unity-gain AFE therefore requires no deliberate level shift or attenuation for the Rev-1 valid measurement range.

Rail-to-rail operation shall not be interpreted as permission to operate exactly at the rails. Actual minimum/maximum AFE output, distortion, loading and clipping margin shall be verified during Stage B. Excursions caused by sensor overrange or faults are handled by the ADC-interface/protection design rather than by redefining the valid 0–5 A calibrated range.

## Phase 12 integration work packages remaining

7. **INT-007 — ADC interface and input protection**
8. **INT-008 — MCU I/O and resource allocation**
9. **INT-009 — USB/PC physical and logical integration boundary**
10. **INT-010 — Protection implementation**
11. **INT-011 — Rev-1 motor/actuator selection requirements**
12. **INT-012 — Complete BOM and procurement status**
13. **INT-013 — Wiring/interconnect specification**
14. **INT-014 — Mechanical/assembly constraints**
15. **INT-015 — Configuration and build identity**
16. **INT-016 — Integration completeness review**

Additional integration decisions may be introduced if detailed reconciliation exposes a genuine build-defining gap.

## Phase 12 completion criterion

Phase 12 is complete only when another engineer can proceed into the Rev-1 build without inventing missing product-level wiring, component, interface or protection decisions. Hardware-dependent measured quantities may remain `TBD — measure during implementation/verification`; build-blocking TBDs may not.
