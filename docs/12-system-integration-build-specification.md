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

Rev-1 is partitioned into actuator/high-current, analog measurement, digital/processing and host regions.

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

with common `GND_MEAS` for UNO, ACS724 secondary side and MCP6022. The motor remains exclusively on the separate bench-PSU actuator path.

The actual measurement rail is approximately 5 V and shall be characterized during implementation/calibration rather than assumed to equal exactly 5.000 V. No external precision 5 V regulator/reference is required unless measured performance later demonstrates it is necessary.

## 12.4 — Ground/reference and laboratory-instrument architecture

### INT-004 — Common measurement ground with designated analog test points

**Status:** Accepted

`GND_MEAS = GND_UNO = GND_AFE = GND_ACS724-secondary`

Required identified test points are `TP_GND`, `TP_5V`, `TP_SENSOR` and `TP_AFE`.

Oscilloscope/function-generator grounds shall not be assumed floating. Ordinary probe grounds shall not be casually connected to actuator-current nodes. Differential/high-current measurements require an appropriate verified method during Stage B.

## 12.5 — ACS724 secondary-side interface

### INT-005 — Direct sensor-to-AFE interface with stock FILTER and local decoupling

**Status:** Accepted

`5V_MEAS → ACS724 VCC`

`GND_MEAS → ACS724 GND`

`ACS724 VOUT → TP_SENSOR → AFE input`

The Pololu carrier's stock **1 nF FILTER capacitor remains unchanged**. Provide **100 nF ceramic local bypass capacitance** between sensor VCC and GND close to the carrier supply connection.

## 12.6 — AFE implementation and component-value freeze

Phase 5 established a fourth-order Butterworth low-pass AFE using the two MCP6022 amplifiers as cascaded unity-gain Sallen-Key second-order sections, with nominal overall cutoff near **15 kHz**.

### INT-006A — Unity-gain Sallen-Key section realization

**Status:** Accepted

Both sections use unity-gain Sallen-Key low-pass topology with equal resistor pairs within each section. Target Q values are approximately 0.5412 and 1.3066.

### INT-006B — Standard component values and nominal response

**Status:** Accepted

| Section | R1 | R2 | C1 | C2 | Nominal f0 | Nominal Q |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Low-Q | 9.76 kΩ | 9.76 kΩ | 1.2 nF | 1.0 nF | ≈14.89 kHz | ≈0.548 |
| High-Q | 4.07 kΩ | 4.07 kΩ | 6.8 nF | 1.0 nF | ≈15.00 kHz | ≈1.304 |

Use **1% resistors** and preferably **≤5% tolerance capacitors**. Nominal cascaded response is approximately −0.124 dB at 10 kHz, −2.99 dB at 15 kHz and −41.9 dB at 50 kHz.

### INT-006C — MCP6022 channel allocation, supply and decoupling

**Status:** Accepted

Signal order:

`ACS724 VOUT → low-Q channel A → high-Q channel B → TP_AFE → ADC interface`

`MCP6022 VDD → 5V_MEAS`; `VSS → GND_MEAS`.

Provide **100 nF** local bypass directly across the MCP6022 supply and **10 µF** bulk/local reservoir capacitance near the AFE.

### INT-006D — Complete MCP6022 PDIP-8 net-level AFE circuit and headroom

**Status:** Accepted

MCP6022-I/P PDIP-8 allocation:

| Pin | Function | Rev-1 connection |
| ---: | --- | --- |
| 1 | OUTA | low-Q output / Stage B input |
| 2 | IN−A | tied to pin 1 |
| 3 | IN+A | low-Q node `N2A` |
| 4 | VSS | `GND_MEAS` |
| 5 | IN+B | high-Q node `N2B` |
| 6 | IN−B | tied to pin 7 |
| 7 | OUTB | `TP_AFE` / ADC-interface source |
| 8 | VDD | `5V_MEAS` |

Low-Q stage:

`TP_SENSOR → R1A 9.76 kΩ → N1A → R2A 9.76 kΩ → N2A → pin 3`

`N2A → C2A 1.0 nF → GND_MEAS`

`N1A → C1A 1.2 nF → pin 1`; `pin 1 → pin 2`.

High-Q stage:

`pin 1 → R1B 4.07 kΩ → N1B → R2B 4.07 kΩ → N2B → pin 5`

`N2B → C2B 1.0 nF → GND_MEAS`

`N1B → C1B 6.8 nF → pin 7`; `pin 7 → pin 6`; `pin 7 → TP_AFE`.

The nominal valid 0.5–4.5 V AFE span leaves approximately 0.5 V headroom from each nominal 5 V supply rail. No deliberate level shift or attenuation is required. Actual swing/distortion/clipping margin is verified in Stage B.

## 12.7 — ADC interface and input protection

### INT-007 — Pending approval

A candidate interface has been proposed but is **not baselined**: `TP_AFE → 1 kΩ → A0`, with 100 pF from the ADC-side node to `GND_MEAS` and no external clamp diodes. This remains pending explicit approval and shall not be treated as a frozen Rev-1 circuit.

## 12.8 — MCU I/O and resource allocation

### INT-008 — Minimal dedicated acquisition-resource reservation

**Status:** Accepted

Rev-1 shall reserve only the MCU resources required by the accepted monitoring architecture:

- **UNO A0** — reserved exclusively for the current-monitoring ADC signal, subject to final INT-007 electrical-interface approval;
- **one RA4M1 ADC channel** — dedicated to current acquisition;
- **one hardware timer resource** — dedicated to deterministic **100 kS/s** ADC triggering;
- **one hardware-assisted transfer resource (DMA/DTC as appropriate to the final RA4M1 implementation)** — dedicated to moving ADC samples into RAM/buffers without software-timed per-sample acquisition;
- **USB/native serial communication path** — reserved for Rev-1 PC/MATLAB telemetry, status and waveform transfer.

The remaining analog and digital I/O shall remain uncommitted unless a later Phase 12 integration decision identifies a genuine Rev-1 requirement. Rev-1 shall not reserve MCU PWM/motor-driver outputs merely because a motor is present: the baseline monitor does not command or power the motor. Likewise, RS-485/CAN resources are not reserved because those interfaces are outside the accepted Rev-1 communication baseline.

Exact RA4M1 timer instance/channel, ADC channel mapping corresponding to the UNO A0 header, event-link routing, DMA/DTC configuration, interrupt assignments and register settings remain Stage B implementation details. Those choices must implement the already accepted deterministic-acquisition architecture without changing its external product behavior.

### Rationale

Reserving the functional resources now prevents later integration conflicts while avoiding unnecessary pin/peripheral commitments. It preserves flexibility for implementation and future expansion without weakening the deterministic 100 kS/s acquisition requirement.

## Phase 12 integration work packages remaining

- Complete **INT-007 — ADC interface and input protection** after explicit approval.
- **INT-009 — USB/PC physical and logical integration boundary**.
- **INT-010 — Protection implementation**.
- **INT-011 — Rev-1 motor/actuator selection requirements**.
- **INT-012 — Complete BOM and procurement status**.
- **INT-013 — Wiring/interconnect specification**.
- **INT-014 — Mechanical/assembly constraints**.
- **INT-015 — Configuration and build identity**.
- **INT-016 — Integration completeness review**.

Additional integration decisions may be introduced if detailed reconciliation exposes a genuine build-defining gap.

## Phase 12 completion criterion

Phase 12 is complete only when another engineer can proceed into the Rev-1 build without inventing missing product-level wiring, component, interface or protection decisions. Hardware-dependent measured quantities may remain `TBD — measure during implementation/verification`; build-blocking TBDs may not.
