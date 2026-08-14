# Phase 2 — System Architecture

**Status:** In progress  
**Project:** Actuator Health Monitoring System

## ARCH-001 — System boundary

**Status:** Accepted

The Actuator Health Monitoring System shall include the current-sensing front end, analog signal conditioning, ADC acquisition, embedded processing, diagnostics, and communication functions.

The actuator, its mechanical load, power source, PC/MATLAB environment, and laboratory instruments shall remain external to the core monitoring system.

The monitoring system may provide a shutdown command, while the high-power switching equipment may remain outside the core monitoring system.

### Rationale

This separation keeps the monitoring architecture modular. The laboratory current-sensing front end can later be replaced by appropriately rated industrial current transducers without requiring the complete acquisition, processing, diagnostic, and communication architecture to be redesigned.

## ARCH-002 — Subsystem decomposition

**Status:** Accepted

The Actuator Health Monitoring System shall consist of six logical subsystems:

1. **Current sensing** — converts actuator current into an analog measurement signal.
2. **Analog front end (AFE)** — protects, buffers, conditions, and anti-alias filters the sensor signal before ADC conversion.
3. **ADC acquisition** — samples the conditioned analog signal at deterministic times and buffers the resulting digital samples.
4. **Signal processing** — converts samples into calibrated electrical quantities and extracts time-domain and frequency-domain features.
5. **Diagnostics** — interprets measurements and extracted features to determine operating state and faults such as overload or stall.
6. **Communication** — transfers measurements, diagnostics, status, and engineering data through UART, CAN, and RS-485 interfaces.

Protection/shutdown control shall be treated as a future extension driven by the diagnostics subsystem.

### Rationale

Separating measurement, processing, diagnostics, and communication keeps responsibilities clear and allows individual subsystems to evolve independently. In particular, future industrial current-sensing hardware can replace the laboratory ACS724 sensing front end while retaining much of the downstream acquisition, processing, diagnostics, and communication architecture.

The anti-alias filter is part of the Analog Front End rather than a separate subsystem because it prepares the analog signal specifically for ADC conversion.

## ARCH-003 — Explicit subsystem interfaces

**Status:** Accepted

The six logical subsystems shall communicate through explicitly defined interfaces. Physical sensing and analog interfaces shall be separated from digital processing and diagnostic interfaces so that sensing hardware can be replaced without unnecessary changes to downstream software.

### Interface classes

| Interface | Source → Destination | Information type |
|---|---|---|
| IF-01 | Actuator current → Current sensing | Physical electrical current |
| IF-02 | Current sensing → Analog front end | Analog sensor voltage |
| IF-03 | Analog front end → ADC acquisition | Conditioned analog voltage |
| IF-04 | ADC acquisition → Signal processing | Timestamped digital samples |
| IF-05 | Signal processing → Diagnostics | Calibrated current values and extracted features |
| IF-06 | Diagnostics → Communication | Operating state, warning and fault information |
| IF-07 | Communication → External device | UART / CAN / RS-485 data |
| IF-08 (future) | Diagnostics → Protection system | Shutdown / control command |

### Rationale

Explicit interface definitions support modularity and make the architecture scalable. A future industrial current transducer may replace the ACS724 sensing subsystem provided the downstream analog interface remains compatible or is adapted by the AFE.

## ARCH-004 — Data representation and traceability

**Status:** Accepted

The acquisition and processing architecture shall preserve four distinct data levels:

1. **Raw ADC samples** — direct ADC conversion results before calibration.
2. **Calibrated current measurements** — samples converted into physical current units.
3. **Calculated features** — time-domain and frequency-domain properties derived from windows or blocks of samples.
4. **Diagnostic information** — operating states, warnings, and fault flags derived from measurements and features.

Raw ADC data shall remain accessible for calibration, validation, and debugging.

Deterministic sample timing shall be represented by a known sampling period and sample index. Acquisition blocks may carry an absolute or block-start timestamp rather than storing a separate timestamp with every individual sample.

### Example data flow

```text
raw ADC samples
       |
       v
calibrated current [A]
       |
       v
features
(mean / RMS / peak / ripple / spectrum)
       |
       v
diagnostic state
(NORMAL / WARNING / FAULT)
```

### Rationale

Separating raw measurements, engineering quantities, calculated features, and diagnostic interpretation preserves traceability. It allows MATLAB analysis and validation to return to the original ADC samples rather than relying only on processed or classified outputs.

At a nominal sampling rate of 100 kS/s, the sampling interval is 10 us. A known block-start time plus sample index is sufficient to reconstruct individual sample times while avoiding unnecessary timestamp storage for every sample.

## ARCH-005 — Power-domain architecture

**Status:** Accepted

The Rev-1 system shall separate the actuator power domain from the monitoring-electronics power domain.

The actuator shall be powered from an external low-voltage DC source.

The current-sensor signal electronics, Analog Front End, and MCU shall operate from the low-voltage monitoring domain, nominally 5 V where applicable, and shall share a defined signal-ground reference.

Local supply decoupling shall be provided at the sensing and analog circuitry.

The actuator-current conductor and low-voltage sensor electronics shall remain galvanically separated through the current-sensing element.

A later development stage shall investigate operation from a common external supply with protection, regulation, filtering, and measured supply-noise performance.

### Rationale

Separating the actuator and monitoring supplies establishes a controlled low-noise baseline for sensor and ADC validation. Motor switching, startup current, commutation, and load transients can disturb the actuator supply; keeping the sensitive measurement electronics on a separate supply initially prevents those disturbances from being unintentionally coupled into every measurement.

The monitoring-side ACS724 output, AFE, and ADC require a common signal reference so that the sensor output voltage is interpreted correctly. The high-current conductor itself remains galvanically separated from this signal-ground domain through the Hall-effect sensing element.

## System context

```text
External actuator supply
        |
        v
Actuator / motor ---- Mechanical load
        |
        | measured current
        v
==================================================
       ACTUATOR HEALTH MONITORING SYSTEM
==================================================
Current sensing
        |
Analog front end
(protection / buffering / anti-alias filtering)
        |
ADC acquisition
        |
Signal processing
        |
Diagnostics
        |
Communication
(UART / RS-485 / CAN)
==================================================
        |
        v
External PC / MATLAB / industrial controller

Separate monitoring-electronics supply:
5 V monitoring rail -> sensor electronics / AFE / MCU
```

Laboratory oscilloscope, multimeter, and bench power supply are external development and verification tools.

## Open architecture work

- Industrial scalability
- Architecture verification
