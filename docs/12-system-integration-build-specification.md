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

## Phase 12 integration work packages

Because Phase 12 is the integration/build-definition phase, it may contain as many coherent decisions as are required. Decisions will not be artificially limited to three or four.

The planned work packages are:

1. **INT-001 — Rev-1 integrated system topology and physical partitioning**
   - freeze the complete end-to-end hardware partition;
   - distinguish high-current, analog measurement, digital/MCU and PC domains;
   - define which interconnections cross each boundary.

2. **INT-002 — Actuator current-path wiring architecture**
   - PSU, sensor primary path, motor and return topology;
   - connector/current-carrying requirements;
   - breadboard prohibition for the motor-current path;
   - current direction/polarity convention.

3. **INT-003 — Measurement-electronics power distribution**
   - source and distribution of the 5 V measurement domain;
   - sensor/AFE/MCU relationships;
   - decoupling and supply partitioning requirements;
   - power-up assumptions that affect validity.

4. **INT-004 — Ground/reference and laboratory-instrument connection architecture**
   - measurement-ground topology;
   - motor-return segregation;
   - USB/PC ground implications;
   - oscilloscope/function-generator grounding constraints.

5. **INT-005 — ACS724 secondary-side interface**
   - exact functional connections required between sensor carrier and AFE;
   - supply, ground and VOUT routing;
   - stock FILTER configuration retained;
   - sensor connector/interface definition.

6. **INT-006 — AFE implementation and component-value freeze**
   - convert the accepted Phase 5 topology into an actual Rev-1 circuit;
   - freeze op-amp channel usage;
   - freeze resistor/capacitor values and tolerances where product-defining;
   - confirm expected DC gain, range, cutoff and headroom.

7. **INT-007 — ADC interface and input protection**
   - AFE-to-RA4M1 ADC connection;
   - ADC pin/channel allocation;
   - required local RC/protection components;
   - valid/overrange behavior at the electrical interface.

8. **INT-008 — MCU I/O and resource allocation**
   - freeze the Rev-1 pins/peripherals needed for ADC, communication and any required status/control interfaces;
   - reserve resources where needed to prevent later integration conflicts;
   - detailed register programming remains Stage B.

9. **INT-009 — USB/PC physical and logical integration boundary**
   - physical PC connection;
   - communication dependency rules;
   - capture/telemetry integration assumptions.

10. **INT-010 — Protection implementation**
    - freeze required ADC/AFE protection components;
    - decide whether Rev-1 requires a fuse or other passive current-path protection in addition to PSU current limiting;
    - polarity/miswiring protections where justified;
    - preserve distinction between measurement overrange and hardware survival.

11. **INT-011 — Rev-1 motor/actuator selection requirements**
    - determine whether a specific motor must be frozen before design review;
    - if not yet purchased, define electrical/mechanical selection envelope sufficient to buy one without redesigning the monitor.

12. **INT-012 — Complete BOM and procurement status**
    - required components, quantities, key ratings/tolerances and selected part identities;
    - distinguish already available / to purchase / optional laboratory equipment;
    - avoid false precision for generic hardware where rating is what matters.

13. **INT-013 — Wiring/interconnect specification**
    - produce a connection table/net-level build specification;
    - distinguish high-current wiring from low-level signal wiring;
    - define connector labels and polarity/current-direction markings;
    - exact physical wire lengths remain implementation detail.

14. **INT-014 — Mechanical/assembly constraints**
    - define which circuits may use solderless breadboard during development and which must not;
    - mounting/strain-relief expectations for sensor and motor-current wiring;
    - separation of noisy/high-current wiring from analog signal wiring.

15. **INT-015 — Configuration and build identity**
    - define what constitutes one Rev-1 hardware/firmware/calibration configuration;
    - ensure captured data can be traced to build and calibration identity.

16. **INT-016 — Integration completeness review**
    - reconcile interfaces against Phases 1–11;
    - identify unresolved build-blocking TBDs;
    - carry non-blocking measured values forward to implementation/verification;
    - prepare the design for Phase 13 verification planning and Phase 14 freeze.

Additional integration decisions may be introduced if the detailed reconciliation exposes a genuine build-defining gap.

## Phase 12 completion criterion

Phase 12 is complete only when the Rev-1 design has a sufficiently concrete integration specification that implementation does not require invention of missing product-level wiring, component, interface or protection decisions.

Hardware-dependent measured quantities may remain `TBD — measure during implementation/verification` where measurement is genuinely required. A TBD that prevents the hardware from being built is not acceptable at Phase 12 closure.

No Phase 12 engineering decision is baselined until explicitly approved.
