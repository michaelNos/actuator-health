# Phase 9 — Communication Interface Design

**Status:** In development  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 9 defines how Rev-1 communicates measurement, diagnostic and system-health information to a PC/MATLAB/controller without disturbing deterministic acquisition.

This phase selects the Rev-1 physical/logical communication strategy and the product-level data interface. Exact packet encoding, host software implementation, connector wiring and debugging remain deferred to Stage B unless required to make the architecture buildable.

## Accepted design inputs

- deterministic 100 kS/s acquisition must remain independent of communication workload;
- calibrated current data, signal features, diagnostic states and measurement-pipeline health are available from Phases 7–8;
- PC/MATLAB analysis and logging are required;
- Arduino UNO R4 WiFi is the Rev-1 MCU platform;
- MAX485 and MCP2551 modules are available but shall not be selected merely because they are on hand;
- Rev-1 is a low-voltage laboratory system; industrial scalability remains architectural rather than direct reuse of hobby hardware.

## Phase 9 design topics

The phase will resolve the minimum product-defining choices needed for communication, including:

- primary Rev-1 physical interface;
- separation of live telemetry from high-rate/raw data transfer where needed;
- message/data model and integrity/versioning requirements;
- industrial-interface scalability only where it affects Rev-1 architecture.

## Planned output

Phase 9 shall close with a communication architecture that supports practical Rev-1 logging/analysis while preserving deterministic acquisition and leaving a clean path toward later industrial interfaces.

No Phase 9 engineering decision is baselined until explicitly approved.
