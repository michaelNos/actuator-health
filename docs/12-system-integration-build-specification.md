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

Core available hardware: UNO R4 WiFi, Pololu #4048 ACS724-05AU, MCP6022-I/P, Philips/Saeco 24 V gearmotor, Jesverty SPS-3010V, HANMATEK DOS1102S, and general passive-component assortments.

Required/verify procurement includes: 9.76 kΩ 1% ×2; 4.07 kΩ 1% ×2; controlled-tolerance 1.0 nF ×2, 1.2 nF ×1, 6.8 nF ×1; 10 µF reservoir if absent; current-rated wire/connectors; inline fuse holder; low-current hookup wire as needed; prototype construction hardware as needed.

Filter resistors shall be **1% metal-film**. Filter capacitors should preferably be **C0G/NP0** or another stable controlled-tolerance dielectric. Exact fuse rating is selected after safe Stage B motor-current characterization.

## 12.13 — Wiring/interconnect specification

### INT-013 — 18 AWG motor-current harness with segregated low-level wiring

**Status:** Accepted

The complete Rev-1 motor-current path shall use **18 AWG stranded insulated copper conductors** as the baseline harness specification:

`PSU+ → inline fuse holder → ACS724 IP+ → ACS724 IP− → polarized motor connection → motor → PSU−`

The ACS724 primary-path pigtails shall be soldered directly into the carrier's high-current connection holes unless an equally suitable mechanically secure current-rated termination is deliberately selected during assembly. The pigtails shall be strain relieved so cable movement and connector forces are not transferred directly to the sensor PCB.

Where a detachable motor/PSU interconnect is required, use a **polarized two-conductor connector rated at least 10 A and 30 VDC**. The existing Philips/Saeco motor connector may be reused only if its current/voltage/mechanical condition can be verified suitable; otherwise replace it with a connector meeting the accepted rating.

The inline fuse holder shall be located in the positive actuator-supply path close to the PSU-side connection where practical. Its wiring and contact rating shall be at least consistent with the selected 18 AWG harness and Rev-1 current envelope. The fuse value itself remains TBD until Stage B motor characterization.

Low-current measurement-electronics connections (`5V_MEAS`, `GND_MEAS`, sensor VOUT, AFE nets, ADC signal) shall use ordinary suitable **22–24 AWG hookup/jumper wiring** or equivalent board interconnect. These conductors shall not be used in the motor-current path.

Analog/signal wiring shall be kept short and separated from the motor/high-current harness where practical. Long parallel routing between sensitive analog lines and motor-current conductors shall be avoided.

The build shall use an unambiguous polarity/color convention. Baseline convention:

- red high-current conductor: actuator `PSU+ / +24 V` side;
- black high-current conductor: actuator return / `PSU−`;
- red low-current conductor: `5V_MEAS`;
- black low-current conductor: `GND_MEAS`;
- a distinct non-red/non-black color: analog signal nets.

Labels shall identify `PSU+`, `FUSE`, `IP+`, `IP−`, `MOTOR+`, `MOTOR−`, `PSU−`, `5V_MEAS`, `GND_MEAS`, `TP_SENSOR`, `TP_AFE` and `A0` where applicable.

Motor-current wiring, Dupont jumpers and analog hookup wire shall be treated as different interconnect classes and shall not be substituted for one another merely because a connector physically fits.

### Rationale

A fixed 18 AWG harness provides conservative current-carrying margin for the ≤5 A calibrated Rev-1 measurement envelope and expected startup/stall characterization while remaining practical for a laboratory build. Explicit separation between high-current and analog wiring reduces contact-heating, breadboard misuse and noise-coupling risks and makes the final build unambiguous.

## Phase 12 integration work packages remaining

- Complete **INT-007 — ADC interface and input protection** after explicit approval.
- **INT-014 — Mechanical/assembly constraints**.
- **INT-015 — Configuration and build identity**.
- **INT-016 — Integration completeness review**.

Additional integration decisions may be introduced if detailed reconciliation exposes a genuine build-defining gap.

## Phase 12 completion criterion

Phase 12 is complete only when another engineer can proceed into the Rev-1 build without inventing missing product-level wiring, component, interface or protection decisions. Hardware-dependent measured quantities may remain `TBD — measure during implementation/verification`; build-blocking TBDs may not.
