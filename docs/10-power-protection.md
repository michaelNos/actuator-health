# Phase 10 — Power and Protection Design

**Status:** In development  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 10 defines the Rev-1 low-voltage power architecture and protection boundaries for the actuator current-monitoring system.

The design shall preserve measurement integrity while keeping the actuator power path separate from the low-voltage sensing/processing domain. This phase defines product-level supply, grounding/reference and protection choices; exact wiring and bench procedure remain Stage B work.

## Accepted design inputs

- Rev-1 actuator domain: **≤24 V DC** laboratory operation;
- ACS724 carrier measurement range: **0–5 A** unidirectional;
- ACS724 and AFE nominally operate from approximately **5 V**;
- Arduino UNO R4 WiFi / RA4M1 is the processing platform;
- ADC-facing valid signal is approximately **0.5–4.5 V**;
- sensor behavior is ratiometric with its supply, so supply/reference behavior affects measurement accuracy;
- actuator power and sensing/processing power are architecturally separate domains;
- bench PSU current limiting is the initial actuator-current protection mechanism;
- automatic motor shutdown is not part of the accepted Rev-1 diagnostic design;
- hobby Rev-1 hardware shall never be connected directly to 400 V industrial mains.

## 10.1 — Power-domain architecture

### PWR-001 — Separate actuator and measurement-electronics power domains

**Status:** Accepted

Rev-1 shall maintain a deliberate separation between the actuator power path and the low-voltage measurement/processing power path.

The actuator path is conceptually:

`bench PSU → ACS724 primary current path → motor/actuator`

The measurement-electronics path is conceptually:

`USB and/or regulated electronics supply → ACS724 electronics + AFE + MCU`

Motor load current shall flow through the ACS724 primary conductor and appropriate current-carrying wiring/connectors, not through the MCU/AFE supply distribution or a solderless breadboard.

The ACS724 provides Hall-effect current measurement across the sensor's isolation barrier; the primary motor-current conductor is not electrically part of the sensor signal-output path.

The actuator supply remains limited to **≤24 V DC** for Rev-1. The laboratory bench supply's adjustable current limit shall be the initial active current-protection mechanism for powered motor testing. The current limit shall be configured appropriately before output enable during implementation.

Rev-1 does not require an integrated motor power converter or automatic diagnostic-controlled shutdown. Diagnostic detection and protective actuation remain separate functions unless a later revision explicitly designs and validates an active shutdown path.

### Rationale

Separating the high-current actuator path from sensitive measurement electronics reduces coupling of motor-current disturbances into the sensing/processing supply and preserves the architecture's isolation boundary. The existing laboratory PSU already provides controlled low-voltage actuator power and adjustable current limiting, so adding an integrated actuator supply or shutdown stage would increase Rev-1 complexity without being necessary to validate the monitoring concept.

## 10.2 — Measurement rail and ADC reference relationship

### PWR-002 — Coherent 5 V measurement/reference domain

**Status:** Accepted

Rev-1 shall use a coherent **5 V measurement/reference domain** so that the ACS724 supply, AFE supply and ADC voltage interpretation are intentionally related rather than treated as independent ideal 5.000 V quantities.

Conceptually:

`5 V measurement domain → ACS724 electronics + MCP6022 AFE + ADC reference/supply relationship`

Because the ACS724 output is ratiometric with its supply, changes in sensor supply voltage affect both offset and sensitivity. The ADC conversion/calibration therefore shall account for the actual relationship between the sensor supply and ADC reference rather than assuming a fixed nominal value in software.

Phase 10 establishes this reference architecture but does not freeze the exact regulator/reference implementation. Final component selection, decoupling and distribution details shall be completed with the integration/BOM work, while actual rail/reference behavior remains subject to implementation measurement and calibration.

### Rationale

Treating the sensor supply and ADC reference as unrelated ideal voltages would convert supply variation into measurement error. A coherent measurement/reference domain allows the ratiometric behavior to be managed deliberately and keeps the power architecture consistent with the Phase 4 accuracy allocation and Phase 6 ADC requirements.

## 10.3 — Grounding and current-return architecture

### PWR-003 — Common measurement reference with segregated actuator-current return

**Status:** Accepted

The low-voltage measurement electronics shall use a common signal/reference ground shared by the ACS724 secondary/output-side electronics, MCP6022 AFE and MCU/ADC as required for correct single-ended signal interpretation.

Conceptually:

`GND_sensor = GND_AFE = GND_MCU`

The high-current actuator return shall be physically routed through the actuator power wiring back to its bench supply and shall not use sensitive measurement-ground conductors as part of the motor-current path:

`I_motor` shall not flow through `GND_measurement`.

This requirement concerns current-return routing and noise control; it does not mean that every conductor or laboratory instrument is galvanically isolated. USB, oscilloscope and function-generator ground relationships shall be checked during implementation before connections are made.

Exact star-point placement, wire routing, connector assignment, decoupling placement and physical layout are Phase 12/Stage B details. They shall implement the principle that large/pulsed actuator currents are kept out of the sensitive analog/ADC return path.

### Rationale

The sensor output, AFE and ADC require a defined common voltage reference, while motor current can create substantial voltage drops and switching/commutation noise in shared conductors. Keeping the high-current return out of the measurement reference path reduces ground-induced measurement error and noise without falsely assuming that all bench equipment is isolated.

## Phase 10 design topic remaining

Define the electrical protection boundaries for the sensor, AFE, ADC/MCU and actuator-current path without expanding into detailed wiring or bench procedure.

## Planned output

Phase 10 shall close with a coherent Rev-1 power/reference/protection architecture that can be converted into exact wiring and BOM details during Phase 12 and implementation.

No Phase 10 engineering decision is baselined until explicitly approved.
