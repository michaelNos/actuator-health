# Phase 12 — System Integration, Wiring, BOM and Build Specification

**Status:** In development  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 12 converts the accepted subsystem designs from Phases 1–11 into one coherent, buildable Rev-1 specification. Physical implementation, firmware coding, calibration and laboratory verification remain after design freeze.

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

`motor current → ACS724 → VOUT → AFE/anti-alias filter → ADC → MCU → USB → PC/MATLAB`

## 12.2 — Actuator current-path wiring architecture

### INT-002 — Dedicated high-side sensor current path with fixed polarity convention

**Status:** Accepted

`bench PSU (+) → ACS724 IP+ → ACS724 IP− → motor (+) → motor (−) → bench PSU (−)`

Dedicated current-rated conductors/connectors shall be used; no motor current through solderless breadboard, MCU header wiring or measurement-ground conductors.

## 12.3 — Measurement-electronics power distribution

### INT-003 — UNO-derived coherent 5 V measurement domain

**Status:** Accepted

`USB-C → UNO R4 WiFi → UNO +5 V header → ACS724 VCC + MCP6022 VDD`, with common `GND_MEAS`. Motor power remains on the separate bench-PSU path. Actual measurement rail is characterized rather than assumed exactly 5.000 V.

## 12.4 — Ground/reference and laboratory-instrument architecture

### INT-004 — Common measurement ground with designated analog test points

**Status:** Accepted

`GND_MEAS = GND_UNO = GND_AFE = GND_ACS724-secondary`

Required test points: `TP_GND`, `TP_5V`, `TP_SENSOR`, `TP_AFE`. Instrument grounds shall not be assumed floating; ordinary probe grounds shall not be casually connected to actuator-current nodes.

## 12.5 — ACS724 secondary-side interface

### INT-005 — Direct sensor-to-AFE interface with stock FILTER and local decoupling

**Status:** Accepted

`5V_MEAS → ACS724 VCC`; `GND_MEAS → ACS724 GND`; `ACS724 VOUT → TP_SENSOR → AFE`.

Stock **1 nF FILTER** remains unchanged. Add **100 nF** local VCC-GND bypass capacitance.

## 12.6 — AFE implementation and component-value freeze

### INT-006A — Unity-gain Sallen-Key section realization

**Status:** Accepted

Two cascaded unity-gain Sallen-Key low-pass sections implement the fourth-order Butterworth response.

### INT-006B — Standard component values and nominal response

**Status:** Accepted

| Section | R1 | R2 | C1 | C2 | Nominal f0 | Nominal Q |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Low-Q | 9.76 kΩ | 9.76 kΩ | 1.2 nF | 1.0 nF | ≈14.89 kHz | ≈0.548 |
| High-Q | 4.07 kΩ | 4.07 kΩ | 6.8 nF | 1.0 nF | ≈15.00 kHz | ≈1.304 |

Use **1% resistors** and preferably **≤5% capacitors**. Nominal response: approximately −0.124 dB at 10 kHz, −2.99 dB at 15 kHz and −41.9 dB at 50 kHz.

### INT-006C — MCP6022 channel allocation, supply and decoupling

**Status:** Accepted

`ACS724 VOUT → low-Q channel A → high-Q channel B → TP_AFE → ADC`.

`VDD → 5V_MEAS`, `VSS → GND_MEAS`; **100 nF** local IC bypass plus **10 µF** AFE reservoir capacitance.

### INT-006D — Complete MCP6022 PDIP-8 net-level AFE circuit and headroom

**Status:** Accepted

| Pin | Function | Rev-1 connection |
| ---: | --- | --- |
| 1 | OUTA | low-Q output / high-Q input source |
| 2 | IN−A | tied to pin 1 |
| 3 | IN+A | low-Q `N2A` |
| 4 | VSS | `GND_MEAS` |
| 5 | IN+B | high-Q `N2B` |
| 6 | IN−B | tied to pin 7 |
| 7 | OUTB | `TP_AFE` / ADC source |
| 8 | VDD | `5V_MEAS` |

Low-Q: `TP_SENSOR → 9.76k → N1A → 9.76k → N2A → pin3`; `N2A → 1.0nF → GND`; `N1A → 1.2nF → pin1`; `pin1 → pin2`.

High-Q: `pin1 → 4.07k → N1B → 4.07k → N2B → pin5`; `N2B → 1.0nF → GND`; `N1B → 6.8nF → pin7`; `pin7 → pin6`; `pin7 → TP_AFE`.

Nominal valid 0.5–4.5 V span leaves approximately 0.5 V rail headroom; no level shift/attenuation required. Actual headroom is verified in Stage B.

## 12.7 — ADC interface and input protection

### INT-007 — Pending approval

Candidate only, **not baselined**: `TP_AFE → 1 kΩ → A0`, 100 pF from ADC-side node to `GND_MEAS`, no external clamp diodes. Explicit approval remains required.

## 12.8 — MCU I/O and resource allocation

### INT-008 — Minimal dedicated acquisition-resource reservation

**Status:** Accepted

Reserve UNO **A0** (subject to INT-007), one ADC channel, one hardware timer for deterministic **100 kS/s**, one DMA/DTC-class transfer resource, and the USB/native serial path. Other MCU resources remain uncommitted unless required later.

## 12.9 — USB/PC physical and logical integration boundary

### INT-009 — Asynchronous USB host interface independent of real-time monitoring

**Status:** Accepted

UNO R4 WiFi USB-C is the sole baseline host interface. It supports normal telemetry, requested waveform capture and configuration/calibration exchange. USB/PC timing shall not control deterministic ADC sampling or real-time diagnostics.

## 12.10 — Protection implementation

### INT-010 — Layered motor, electronics and measurement-validity protection

**Status:** Accepted

The actuator-current path is:

`bench PSU (+) → series fuse → ACS724 IP+ → ACS724 IP− → motor → bench PSU (−)`

The bench PSU adjustable current limit is the primary active motor-current protection. A replaceable series fuse near PSU+ provides passive backup. The exact fuse rating remains a Stage B selection after safe motor-current characterization; it is not chosen merely from the 5 A measurement range.

Software/diagnostics distinguish overrange/invalid measurement from electrical damage. **5 A is the calibrated measurement-validity boundary, not automatically a hardware survival, fuse or shutdown threshold.**

## 12.11 — Rev-1 motor/actuator selection

### INT-011 — Philips/Saeco 24 VDC brew-group gearmotor selected as Rev-1 actuator

**Status:** Accepted

The Rev-1 actuator is the available **Philips/Saeco 24 VDC brew-group gearmotor** recovered from the user's failed coffee machine.

Motor-specific no-load, normal-load, startup/inrush and stall/jam currents remain **TBD — measure during Stage B implementation/verification**. Normal/intended tests should remain within the 0–5 A calibrated range wherever practical; any excursion above 5 A is treated as measurement overrange and constrained by PSU current limiting.

## 12.12 — Rev-1 BOM and procurement status

### INT-012 — Build BOM classification and procurement baseline

**Status:** Accepted

The Rev-1 BOM is classified into hardware already available, items requiring purchase/verification, and values that genuinely depend on Stage B characterization.

| Item | Rev-1 requirement | Status / action |
| --- | --- | --- |
| Arduino UNO R4 WiFi | RA4M1 acquisition/processing platform | **Available** |
| Pololu #4048 / ACS724-05AU | 0–5 A current sensor | **Available** |
| MCP6022-I/P | dual op-amp for AFE | **Available** |
| Philips/Saeco gearmotor | 24 VDC Rev-1 actuator | **Available** |
| Jesverty SPS-3010V | motor bench supply with adjustable current limit | **Available** |
| HANMATEK DOS1102S | verification oscilloscope/function generator | **Available** |
| 100 nF ceramic capacitors | ACS724 and MCP6022 local bypass | **Available from component assortment; verify values before assembly** |
| 10 µF capacitor | AFE local reservoir | **Verify availability/value before assembly; purchase if absent** |
| 9.76 kΩ 1% resistors ×2 | low-Q filter | **Purchase unless exact suitable parts are verified available** |
| 4.07 kΩ 1% resistors ×2 | high-Q filter | **Purchase unless exact suitable parts are verified available** |
| 1.0 nF ≤5% capacitors ×2 | filter | **Purchase controlled-tolerance parts unless verified suitable parts are available** |
| 1.2 nF ≤5% capacitor ×1 | filter | **Purchase** |
| 6.8 nF ≤5% capacitor ×1 | filter | **Purchase** |
| Current-rated insulated copper wire | motor/high-current path | **Purchase** |
| Current-rated connectors/terminals | PSU/sensor/motor interconnect | **Purchase** |
| Inline/series fuse holder | motor-path passive protection | **Purchase** |
| Replaceable fuse(s) | motor-path backup protection | **Rating TBD after safe Stage B motor characterization** |
| USB-C data cable | UNO ↔ PC | **Verify available** |
| Low-current hookup/jumper wire | 5 V measurement-domain interconnect | **Verify available; purchase if absent** |
| Prototype construction hardware | breadboard/perfboard/terminal support as appropriate | **Verify available; final physical use constrained by INT-013/INT-014** |

For the filter network, use **1% metal-film resistors**. The filter capacitors should preferably be **C0G/NP0 ceramic** (or another suitably stable, controlled-tolerance dielectric) because their capacitance directly determines the filter pole/Q realization. Generic high-K ceramic assortment parts shall not be assumed suitable merely because their nominal capacitance matches.

The motor/high-current path shall not use ordinary Dupont jumper leads or solderless-breadboard contacts. Dedicated current-rated wire and connectors are mandatory procurement items.

The exact fuse rating is deliberately not purchased/frozen yet. Initial motor characterization shall be performed with conservative bench-PSU current limiting; measured startup, normal and controlled-stall behavior then informs the replaceable fuse selection while respecting conductor, connector and sensor-path ratings.

Exact current-wire gauge and connector family remain to be finalized in INT-013. Their selection shall support the Rev-1 current envelope with appropriate margin and shall not depend on the precision measurement range being interpreted as a hardware survival rating.

### Rationale

This BOM freezes the components that define the accepted electrical design while separating true procurement gaps from quantities that can only be chosen responsibly after the real motor is characterized. Precision filter components are treated as deliberate design parts rather than whatever values happen to be present in a general-purpose assortment.

## Phase 12 integration work packages remaining

- Complete **INT-007 — ADC interface and input protection** after explicit approval.
- **INT-013 — Wiring/interconnect specification**.
- **INT-014 — Mechanical/assembly constraints**.
- **INT-015 — Configuration and build identity**.
- **INT-016 — Integration completeness review**.

Additional integration decisions may be introduced if detailed reconciliation exposes a genuine build-defining gap.

## Phase 12 completion criterion

Phase 12 is complete only when another engineer can proceed into the Rev-1 build without inventing missing product-level wiring, component, interface or protection decisions. Hardware-dependent measured quantities may remain `TBD — measure during implementation/verification`; build-blocking TBDs may not.
