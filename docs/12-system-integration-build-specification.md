# Phase 12 — System Integration, Wiring, BOM and Build Specification

**Status:** In development  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 12 converts the accepted subsystem designs from Phases 1–11 into one coherent, buildable Rev-1 specification.

Unlike the preceding architecture phases, this phase intentionally goes deeper. It shall freeze enough integration detail that another engineer could identify the required hardware, understand every subsystem boundary, wire the Rev-1 correctly, know which values/interfaces are fixed versus TBD, and proceed into Stage B without inventing missing product architecture.

Phase 12 still does **not** perform the physical build, firmware implementation, calibration or laboratory verification. Those activities remain after the Rev-1 design freeze.

## Accepted design baseline entering Phase 12

The integrated design must preserve at least the following accepted constraints:

- low-voltage Rev-1 actuator/motor: **≤24 V DC**;
- calibrated current range: **0–5 A**, unidirectional;
- current sensor: **Pololu #4048 / ACS724LLCTR-05AU**;
- nominal sensor transfer: approximately **0.5–4.5 V for 0–5 A** at nominal 5 V;
- diagnostic information band: **DC–10 kHz**;
- sensor carrier remains in its stock approximately **90 kHz** configuration;
- deliberate AFE anti-alias filtering is separate from the ACS724 FILTER capacitor;
- deterministic ADC acquisition baseline: **100 kS/s**;
- MCU platform: **Arduino UNO R4 WiFi / Renesas RA4M1**;
- AFE active device: **MCP6022-I/P** where required by the accepted AFE design;
- system accuracy target after calibration: **≤ ±0.10 A**, stretch **±0.05 A**;
- reported-current resolution target: **≤10 mA**;
- actuator and measurement-electronics power paths are deliberately separated;
- ACS724, AFE and ADC/reference relationship use a coherent measurement-domain strategy;
- high motor current shall not flow through sensitive measurement-ground wiring or solderless breadboard;
- USB serial is the Rev-1 PC/MATLAB communication interface;
- real-time acquisition/diagnostics remain independent of PC/MATLAB;
- automatic motor shutdown is not part of Rev-1;
- bench PSU current limiting is the initial active motor-current protection mechanism;
- Rev-1 hobby hardware shall never be connected directly to industrial mains or a 400 V motor circuit.

## 12.1 — Integrated Rev-1 topology and physical partitioning

### INT-001 — Four-region integrated system topology

**Status:** Accepted

Rev-1 shall be integrated as four deliberate physical/electrical regions:

1. **Actuator/high-current region** — bench PSU, high-current wiring/connectors, ACS724 primary current path and low-voltage DC motor/actuator.
2. **Analog measurement region** — ACS724 secondary/output-side electronics, MCP6022-based AFE, deliberate anti-alias filtering and ADC-interface/protection circuitry.
3. **Digital/processing region** — Arduino UNO R4 WiFi / RA4M1 performing deterministic ADC acquisition, buffering, calibrated-current conversion, signal-feature extraction, diagnostics and communication management.
4. **Host region** — USB-connected PC/MATLAB environment for telemetry, waveform capture, calibration/characterization and engineering analysis.

The integrated signal path is:

`motor current → ACS724 primary conductor → Hall measurement → ACS724 VOUT → AFE/anti-alias filter → ADC → MCU processing/diagnostics → USB → PC/MATLAB`

The actuator current path is conceptually:

`bench PSU (+) → ACS724 IP+ → ACS724 IP− → DC motor/actuator → bench PSU (−)`

The ACS724 primary conductor forms the boundary between the multi-ampere actuator-current path and the low-voltage measurement signal chain. Motor current shall not be routed through the AFE, MCU, USB or measurement-ground wiring.

The four-region partition is a functional and physical integration rule, not a claim that all four regions are mutually galvanically isolated. In particular, the analog measurement and MCU regions intentionally share the required low-voltage measurement reference, and USB/bench-instrument grounding may introduce additional earth/reference relationships that must be respected during implementation.

Physical implementation shall preserve practical separation between high-current/noisy motor wiring and sensitive analog wiring. The exact enclosure, board placement and wire lengths are not frozen in Phase 12 unless later integration analysis shows they are necessary to guarantee the design.

### Rationale

The partition makes the accepted architecture buildable while preserving the critical distinction between the motor-energy path and the measurement signal path. It provides a concrete basis for later wiring, grounding, protection and assembly decisions without incorrectly treating the entire laboratory setup as galvanically isolated.

## 12.2 — Actuator current-path wiring architecture

### INT-002 — Dedicated high-side sensor current path with fixed polarity convention

**Status:** Accepted

The Rev-1 actuator-current path shall be wired as:

`bench PSU (+) → ACS724 IP+ → ACS724 IP− → motor/actuator (+) → motor/actuator (−) → bench PSU (−)`

This establishes the positive current convention through the unidirectional ACS724-05AU and keeps the sensor on the positive/high side of the low-voltage actuator supply.

The current path shall use dedicated insulated copper conductors and connectors suitable for the selected motor's normal, startup and controlled fault-test currents. The path shall not pass through a solderless breadboard, MCU header wiring or measurement-ground conductors.

The ACS724 primary terminals and all motor-current connections shall be mechanically secure. The final assembly shall provide strain relief or equivalent support so that motor/PSU leads do not load the sensor PCB or create intermittent high-current contacts.

The physical build shall clearly identify at least:

- `PSU+`;
- `ACS724 IP+`;
- `ACS724 IP−`;
- `MOTOR+`;
- `MOTOR−`;
- `PSU−`.

The **0–5 A** range is the calibrated measurement range, not a requirement to operate the motor continuously near 5 A and not the electrical survival rating. The selected motor shall provide useful measurement margin below 5 A during normal operation while still allowing controlled startup/load/stall experiments without routinely exceeding the valid measurement range.

Because the Rev-1 sensor variant is unidirectional, the build shall preserve the defined current direction through the sensor. Bidirectional/regenerative current characterization is outside the Rev-1 calibrated scope.

### Procurement dependency

The exact motor/actuator has **not yet been selected**, and dedicated current-rated motor wiring/connectors are **not yet available**. These are explicit Phase 12 procurement items.

The current-path topology is nevertheless frozen. Exact conductor gauge, connector type and current rating shall be selected after INT-011 freezes the Rev-1 motor electrical envelope. Those choices must be completed before Phase 12 closure because they are build-defining, not measurement-dependent TBDs.

### Rationale

A fixed current direction is required by the unidirectional ACS724 transfer function. A dedicated high-current path prevents motor current from flowing through inappropriate prototyping interconnects and creates a clean basis for later wire/connector sizing once the motor is selected.

## 12.3 — Measurement-electronics power distribution

### INT-003 — UNO-derived coherent 5 V measurement domain

**Status:** Accepted

Rev-1 measurement electronics shall use the Arduino UNO R4 WiFi board's **+5 V header rail** as the common measurement-electronics supply while the UNO R4 WiFi itself is powered through its USB-C connection during normal laboratory development.

The measurement-power topology is:

`USB-C → UNO R4 WiFi power architecture → UNO +5 V header → ACS724 VCC + MCP6022 VDD`

and the corresponding low-voltage reference is:

`UNO GND → ACS724 GND + MCP6022 VSS/GND + ADC measurement reference domain`

The motor/actuator shall **not** be powered from the UNO 5 V rail. It remains exclusively on the separate bench-PSU actuator path defined by INT-001/INT-002.

The ACS724 output is ratiometric with its supply. Rev-1 therefore intentionally keeps the sensor supply and ADC voltage interpretation within the same board-level measurement/reference architecture rather than assuming an independent ideal 5.000 V sensor supply. The actual measurement rail shall be treated as approximately 5 V and characterized during implementation/calibration; software and engineering calculations shall not assume it is exactly 5.000 V.

No external precision 5 V regulator/reference is required in the Rev-1 baseline. Such a component may be introduced only if implementation evidence shows that the accepted **≤ ±0.10 A** calibrated system-accuracy requirement cannot be achieved with the baseline architecture.

The ACS724 and MCP6022 shall receive local supply decoupling close to their supply connections. Exact decoupling components and placement are frozen with the component-level analog/BOM integration decisions later in Phase 12.

The build shall avoid connecting independent external 5 V sources in parallel with the UNO 5 V rail. Any alternate powering arrangement used during laboratory work must first be checked against the UNO R4 power architecture rather than assuming that two nominally 5 V sources can safely be tied together.

### Rationale

Using the UNO-derived measurement rail minimizes unnecessary power hardware and preserves the first-order ratiometric relationship between the ACS724 signal and the ADC measurement domain. The added analog loads are the sensor and AFE, not the motor. Characterizing the actual rail during calibration is more appropriate than adding a precision reference without evidence that it is needed.

## 12.4 — Ground/reference and laboratory-instrument architecture

### INT-004 — Common measurement ground with designated analog test points

**Status:** Accepted

Rev-1 shall use one common low-voltage measurement reference for the sensor secondary side, AFE and MCU/ADC:

`GND_MEAS = GND_UNO = GND_AFE = GND_ACS724-secondary`

The actuator/motor current return remains a dedicated high-current conductor from the motor back to the bench PSU. Motor load current shall not use `GND_MEAS` conductors as part of its return path.

The integrated build shall provide or clearly identify the following measurement points:

- `TP_GND` — measurement-electronics reference ground;
- `TP_5V` — measurement-domain supply rail;
- `TP_SENSOR` — raw ACS724 `VOUT` before the deliberate AFE anti-alias filter;
- `TP_AFE` — filtered AFE output presented toward the ADC interface.

Ordinary single-ended oscilloscope measurements of `TP_SENSOR`, `TP_AFE` and `TP_5V` shall reference `TP_GND`.

The Rev-1 design shall **not assume oscilloscope or function-generator grounds are floating or isolated**. Before connecting laboratory equipment, its ground/earth relationship shall be understood. An ordinary ground-referenced probe ground shall not be casually connected to `PSU+`, `ACS724 IP+`, `ACS724 IP−` or another actuator-current node because doing so may create an unintended current path or short through instrument/earth wiring.

Any measurement directly across a floating/high-current actuator node shall require an explicitly appropriate measurement method rather than reusing the low-level analog probing convention by assumption. Exact differential-probing technique and instrument setup are Stage B laboratory-procedure details.

The same rule applies to the integrated function generator: its output return/ground relationship shall be established before connection to the AFE or other circuit node. Bench PSU and function-generator outputs shall not be directly paralleled to combine DC and AC sources.

### Rationale

The ACS724 output, AFE and ADC require a common reference for accurate single-ended measurement, while the motor-current return must remain outside that sensitive path. Explicit test points make intended low-voltage probing unambiguous, and the instrument-ground rule prevents the isolation provided by the current sensor from being defeated by an accidental earth-referenced laboratory connection.

## Phase 12 integration work packages remaining

5. **INT-005 — ACS724 secondary-side interface**
6. **INT-006 — AFE implementation and component-value freeze**
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

Additional integration decisions may be introduced if the detailed reconciliation exposes a genuine build-defining gap.

## Phase 12 completion criterion

Phase 12 is complete only when the Rev-1 design has a sufficiently concrete integration specification that implementation does not require invention of missing product-level wiring, component, interface or protection decisions.

Hardware-dependent measured quantities may remain `TBD — measure during implementation/verification` where measurement is genuinely required. A TBD that prevents the hardware from being built is not acceptable at Phase 12 closure.

No Phase 12 engineering decision is baselined until explicitly approved.
