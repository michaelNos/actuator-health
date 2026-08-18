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

## Phase 10 design topics

The phase will resolve the minimum product-defining choices for:

- actuator versus measurement-electronics power architecture;
- 5 V measurement rail and ADC/reference relationship;
- grounding/reference and noise-return strategy;
- electrical protection boundaries for the sensor, AFE, ADC/MCU and actuator-current path.

## Planned output

Phase 10 shall close with a coherent Rev-1 power/reference/protection architecture that can be converted into exact wiring and BOM details during Phase 12 and implementation.

No Phase 10 engineering decision is baselined until explicitly approved.
