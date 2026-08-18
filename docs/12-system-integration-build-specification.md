# Phase 12 — System Integration, Wiring, BOM and Build Specification

**Status:** Design complete / ready for PR review  
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

### INT-007 — Dedicated A0 interface with series isolation and local sampling capacitor

**Status:** Accepted

The Rev-1 AFE-to-ADC interface shall be:

`TP_AFE → 1 kΩ series resistor → ADC_IN / UNO A0`

with a **100 pF capacitor from the ADC-side A0 node to `GND_MEAS`**.

The local RC pole is approximately:

`fc = 1 / (2π × 1 kΩ × 100 pF) ≈ 1.59 MHz`

This network is therefore not an additional anti-alias filter and has negligible intended effect on the accepted DC–10 kHz diagnostic band. The 1 kΩ resistor provides source isolation and limits transient current into the ADC input; the 100 pF capacitor provides local charge support for the ADC sample-and-hold interface.

UNO **A0 is dedicated to the Rev-1 current-monitoring ADC signal**. The RA4M1 ADC shall be configured during Stage B with sampling/acquisition time sufficient to settle through the accepted source/interface network while maintaining the required deterministic **100 kS/s** sample rate.

No external Schottky clamp diodes are included in the baseline Rev-1 ADC interface. Under normal operation the MCP6022 output and RA4M1 ADC share the same approximately 5 V measurement domain, while the valid signal is nominally approximately **0.5–4.5 V**. Additional clamp devices would add leakage/capacitance to the precision measurement node without providing credible protection against a gross 24 V misconnection.

Approaching or reaching the ADC rails shall be treated as clipping/overrange and shall not be interpreted as a calibrated current value. Accidental connection of the 24 V actuator rail to A0 is explicitly **outside the Rev-1 ADC protection capability** and is prevented by the physical/wiring segregation rules rather than by this small-signal interface network.

Stage B verification shall demonstrate:

- correct ADC settling at 100 kS/s;
- no meaningful passband degradation from the interface network;
- no clipping throughout the intended valid 0.5–4.5 V AFE span;
- effective ADC-domain voltage resolution of **≤2 mV** under actual acquisition conditions.

### Rationale

A small series resistor and local capacitor provide practical ADC-drive isolation without burdening the precision analog path or duplicating the deliberately designed 15 kHz anti-alias filter. Avoiding unnecessary clamps preserves low leakage/capacitance while keeping the system boundary explicit: the ADC interface is protected for intended low-voltage analog operation, not arbitrary actuator-rail miswiring.

## 12.8 — MCU I/O and resource allocation

### INT-008 — Minimal dedicated acquisition-resource reservation

**Status:** Accepted

Reserve UNO **A0**, one ADC channel, one hardware timer for deterministic **100 kS/s**, one DMA/DTC-class transfer resource, and the USB/native serial path. Other MCU resources remain uncommitted unless required later.

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

Required/verify procurement includes: 9.76 kΩ 1% ×2; 4.07 kΩ 1% ×2; controlled-tolerance 1.0 nF ×2, 1.2 nF ×1, 6.8 nF ×1; **1 kΩ resistor ×1; 100 pF capacitor ×1** for the ADC interface; 10 µF reservoir if absent; current-rated wire/connectors; inline fuse holder; low-current hookup wire as needed; prototype construction hardware as needed.

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

## 12.14 — Mechanical and assembly constraints

### INT-014 — Secure open laboratory prototype with physically controlled current and analog regions

**Status:** Accepted

Rev-1 shall be implemented as a **secure open laboratory prototype**. A finished product enclosure is not required for Rev-1, but the assembly shall be mechanically stable, electrically controlled and suitable for repeatable bench testing.

The **motor/high-current path shall not use a solderless breadboard**. The 18 AWG current harness, inline fuse holder, ACS724 primary path and motor connections shall use mechanically secure current-rated terminations. Current-path wiring shall be routed and restrained so accidental movement cannot pull conductors free or transfer excessive force into component PCBs.

The **ACS724 carrier shall be mechanically supported**. Its 18 AWG primary-current pigtails shall receive strain relief so repeated cable movement does not flex the carrier or its solder joints.

The **low-current AFE may initially be assembled on a solderless breadboard**. The AFE shall nevertheless be compact. If Stage B verification shows that breadboard parasitics, contact quality, noise pickup or mechanical instability prevent accepted performance, the AFE shall migrate to perfboard or another soldered prototype construction without changing the accepted circuit topology unless a formal design revision is required.

The analog measurement region shall be kept physically separated from the motor body and motor-current harness where practical. Test points `TP_GND`, `TP_5V`, `TP_SENSOR` and `TP_AFE` shall remain physically accessible without disturbing the high-current wiring.

## 12.15 — Configuration and build identity

### INT-015 — Versioned build/configuration identity for measurement traceability

**Status:** Accepted

Every meaningful Rev-1 engineering dataset, calibration/reference record and verification result shall be traceable to the system configuration that produced it.

`Build ID = (hardware revision, firmware revision, calibration ID, motor ID, configuration ID)`

At minimum, measurement/capture metadata shall identify hardware revision, firmware revision/Git commit, active calibration ID, motor ID, acquisition configuration ID, and diagnostic/reference identity where applicable.

A configuration/calibration change that can materially alter numerical interpretation or diagnostic results shall produce a new corresponding identity/version rather than silently reusing the previous identifier. Exact serialization/file naming remains Stage B implementation detail.

## 12.16 — Integration completeness review

### INT-016 — Rev-1 integration baseline complete

**Status:** Accepted

The Phase 12 integration review confirms that the accepted subsystem designs from Phases 1–11 have been reconciled into one coherent Rev-1 build specification with no remaining product-level interface, component, wiring, protection or configuration decision that blocks later implementation.

The integrated Rev-1 current path is:

`24 V bench PSU → series fuse → ACS724 primary path → Philips/Saeco 24 VDC gearmotor → PSU return`

The integrated measurement path is:

`ACS724 VOUT → fourth-order MCP6022 Butterworth AFE → 1 kΩ / 100 pF ADC interface → UNO R4 A0 / RA4M1 ADC → deterministic 100 kS/s acquisition → MCU processing/diagnostics → USB → PC/MATLAB`

The Phase 1 product requirements remain represented in the integrated design: 0–5 A calibrated current range, DC–10 kHz diagnostic band, 100 kS/s acquisition, ≤ ±0.10 A calibrated system-accuracy target, ≤10 mA reported-current resolution, startup/load/overload/stall characterization, and low-voltage ≤24 V laboratory operation.

The following remaining quantities are legitimate **implementation/verification TBDs** rather than missing design decisions:

- actual ACS724 zero-current offset, sensitivity, noise and residual calibration error;
- actual 5 V measurement rail/reference behavior;
- realized AFE gain, offset, frequency response and clipping margin;
- RA4M1 ADC effective resolution, settling and noise at 100 kS/s;
- motor no-load, representative load, startup/inrush and stall/jam currents;
- final overload/stall diagnostic thresholds and persistence values derived from characterization;
- final replaceable fuse rating selected after safe motor-current characterization;
- exact physical mounting/baseplate and other non-electrical implementation conveniences.

None of these values requires invention of a new product architecture before construction can begin. They shall be populated through Stage B/C implementation, calibration and verification as defined by DEV-001.

The integration review also corrected stale repository status/index information for earlier completed phases. Documentation status cleanup does not change their approved engineering content.

### Phase 12 handoff

Phase 12 provides Phase 13 with a concrete Rev-1 system to verify and Phase 14 with a complete integration baseline to review for design freeze.

Implementation shall **not** begin yet. Stage A continues with:

- Phase 13 — System Verification and Acceptance Plan;
- Phase 14 — Rev-1 Design Review and Design Freeze.

Only after the Phase 14 design freeze may Stage B physical implementation begin.

## Phase 12 completion criterion

The Phase 12 completion criterion is satisfied: another engineer can proceed toward the Rev-1 implementation after design freeze without inventing missing product-level wiring, component, interface or protection decisions.

**Phase 12 status: DESIGN COMPLETE / READY FOR PR REVIEW**
