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

## System context

```text
External power source
        |
        v
Actuator / motor ---- Mechanical load
        |
        | measured current
        v
==================================================
       ACTUATOR HEALTH MONITORING SYSTEM
==================================================
Current sensing front end
        |
Analog signal conditioning
        |
Anti-alias filtering
        |
ADC acquisition
        |
Embedded processing and diagnostics
        |
UART / RS-485 / CAN
==================================================
        |
        v
External PC / MATLAB / industrial controller
```

Laboratory oscilloscope, multimeter, and bench power supply are external development and verification tools.

## Open architecture work

- ARCH-002 — subsystem decomposition and responsibilities
- Interface definitions
- Signal and data flow
- Power architecture
- Industrial scalability
- Architecture verification
