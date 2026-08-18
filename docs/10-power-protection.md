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

## Phase 10 design topics remaining

- 5 V measurement rail and ADC/reference relationship;
- grounding/reference and noise-return strategy;
- electrical protection boundaries for the sensor, AFE, ADC/MCU and actuator-current path.

## Planned output

Phase 10 shall close with a coherent Rev-1 power/reference/protection architecture that can be converted into exact wiring and BOM details during Phase 12 and implementation.

No Phase 10 engineering decision is baselined until explicitly approved.
