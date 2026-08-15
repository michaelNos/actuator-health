# Phase 1 — System Requirements

**Status:** Complete / baselined  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 1 defines what the Rev-1 laboratory system must measure and what operating behaviours it must support before implementation details are selected.

The Rev-1 system is a low-voltage DC actuator/motor condition-monitoring prototype based on current measurement and waveform analysis. The architecture should remain conceptually scalable toward future industrial three-phase motor monitoring, but Rev-1 hardware is not industrial-rated equipment.

## REQ-SIG-001 — Current measurement and waveform analysis

**Status:** Accepted

The system shall acquire sufficient current-waveform information to characterize:

- average actuator load,
- startup behaviour,
- commutation/current ripple,
- changing mechanical load,
- overload,
- and stall conditions.

The acquired data shall support both time-domain and frequency-domain analysis.

## REQ-BW-001 — Diagnostic measurement bandwidth

**Status:** Accepted

The current-acquisition subsystem shall preserve diagnostic signal content from DC through 10 kHz.

`DC–10 kHz` means signal content from 0 Hz through 10,000 Hz. It includes average current, slow variations, periodic components, harmonics, commutation ripple, and other diagnostic content within this band.

## REQ-BW-002 — Higher-frequency characterization

**Status:** Accepted

Frequency components above the diagnostic bandwidth shall be characterized with laboratory instrumentation during validation to determine whether extending the acquisition bandwidth is justified.

## Phase 1 baseline decisions

### 1. Rev-1 actuator class

- Rev-1 uses a low-voltage DC actuator/motor.
- A brushed DC motor is preferred for laboratory validation because it is simple to drive and produces useful commutation-current structure.
- The architecture shall remain replaceable at the sensing front end for future industrial three-phase monitoring.

### 2. Electrical operating envelope

- Current-measurement range: **0–5 A**, constrained by the selected ACS724-05AU sensor.
- Monitoring electronics: nominally **5 V where applicable**.
- Rev-1 actuator supply: low-voltage DC, **maximum architectural limit 24 V**.
- Exact motor operating voltage/current remains dependent on final motor selection.

### 3. Operating behaviours and faults

The system shall support characterization of:

- startup/inrush,
- normal running,
- changing mechanical load,
- commutation/current-spectrum behaviour,
- overload,
- stall.

### 4. Sampling frequency

Nominal acquisition target: **100 kS/s**.

At 100 kS/s:

- sampling period = **10 µs**,
- Nyquist frequency = **50 kHz**,
- a 10 kHz signal is represented by 10 samples per period,
- the 10–50 kHz region provides practical transition space for analog anti-alias filtering.

The theoretical Nyquist minimum for 10 kHz bandwidth is not treated as an adequate practical design target.

### 5. Measurement accuracy

Laboratory system-level target after calibration: **≤ ±0.10 A**.

Stretch target: **±0.05 A**.

Reported current resolution target: **≤ 10 mA**.

ADC bit resolution alone shall not be treated as measurement accuracy. The final error budget must include sensor, analog-front-end, ADC, reference/supply, noise, temperature, and calibration effects.

### 6. Overload definition

Overload shall be based on:

- current above a configurable overload threshold,
- persisting longer than a configurable persistence time.

Threshold and persistence values shall be derived from characterization of the actual test actuator rather than guessed in Phase 1.

### 7. Stall definition

Physical stall means a powered/commanded actuator is not rotating.

Because Rev-1 is initially current-only, stall detection shall be inferred from current behaviour. Candidate indicators include:

- elevated current,
- loss/reduction/change of normal commutation behaviour,
- persistence for a defined interval.

Exact stall criteria remain to be experimentally derived.

### 8. Fault-detection latency

Targets:

- stall: **≤ 100 ms** after stall criteria become valid,
- sustained overload: **≤ 1 s** after overload criteria become valid.

Persistence parameters remain configurable and require later validation.

### 9. Protection philosophy

- During early development, the bench power supply current limit is the primary actuator-side protection.
- Measurement and diagnosis are validated before automatic shutdown is enabled.
- A later design may use a MOSFET, relay, or external protection interface commanded by diagnostics.
- Critical faults may later be latched until reset.

### 10. Laboratory environment

Rev-1 baseline:

- indoor laboratory,
- approximately 20–30 °C,
- dry environment,
- low-voltage DC actuator supply ≤24 V,
- nominal monitoring electronics around 5 V where applicable,
- short laboratory wiring.

Later characterization should intentionally investigate supply variation, noise, motor-generated disturbances, and temperature influence where justified.

### 11. Verification approach

Requirements shall be verified using combinations of:

- engineering analysis and calculations,
- inspection,
- controlled laboratory testing,
- demonstration.

Objective evidence may include:

- oscilloscope measurements,
- multimeter/reference readings,
- bench-supply settings/readings,
- raw ADC logs,
- firmware logs,
- MATLAB analysis and plots.

## Key fixed Rev-1 hardware constraints established before detailed design

- Current sensor: Pololu #4048 using Allegro ACS724LLCTR-05AU, 0–5 A unidirectional.
- MCU platform: Arduino UNO R4 WiFi / Renesas RA4M1.
- Oscilloscope: HANMATEK DOS1102S with waveform generator.
- Bench supply: Jesverty SPS-3010V.
- AFE experimentation op-amp: MCP6022-I/P.

These selections constrain later design work but do not by themselves prove that the system meets the Phase 1 performance requirements.

## Safety scope

Rev-1 is a low-voltage laboratory system. The Pololu ACS724 carrier, Arduino, breadboard, and ordinary oscilloscope probes shall not be connected directly to an industrial 400 V three-phase circuit. Future industrial implementation requires appropriately rated isolated transducers and installation practices.

## Phase 1 baseline summary

Phase 1 establishes the Rev-1 measurement purpose, operating range, diagnostic bandwidth, nominal sampling rate, accuracy target, target operating/fault conditions, detection-latency goals, protection philosophy, laboratory environment, and verification method.

**Phase 1 status: COMPLETE / BASELINED**
