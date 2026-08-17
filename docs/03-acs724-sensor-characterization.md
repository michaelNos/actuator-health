# Phase 3 — ACS724 Sensor Theory and Characterization

**Status:** In progress  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 3 develops and experimentally validates the current-sensor model used by the Rev-1 laboratory prototype before the complete analog front end is designed.

The selected laboratory sensor is the Pololu #4048 carrier using the Allegro ACS724LLCTR-05AU Hall-effect current-sensor IC.

This phase shall distinguish clearly between datasheet facts, calculations, proposed engineering decisions, accepted decisions, and measured results. Unknown values remain **TBD** until derived or measured.

## Phase workflow

No Phase 3 engineering decision is accepted merely because it appears in discussion or as a proposal. Decisions are baselined in this document only after explicit approval.

The Phase 3 pull request remains a draft while the phase is being developed.

## 3.1 — Hall-effect current sensing

**Status:** Complete / accepted

### SENS-001 — Rev-1 Hall-effect current-sensing principle

**Status:** Accepted

Rev-1 shall use the selected ACS724 Hall-effect current sensor as an in-series current transducer. Actuator current shall flow through the sensor primary conductor, while the low-voltage sensing electronics shall derive an analog output from the current-generated magnetic field. The primary current path and low-voltage sensing electronics shall remain galvanically isolated through the sensor architecture.

### Rationale

The ACS724 measures the magnetic field produced by current flowing through its low-resistance primary copper conductor. Its Hall sensing and internal signal-conditioning electronics convert that magnetic information into an analog output voltage without a direct conductive signal connection to the primary current path.

This establishes two distinct electrical roles:

- **Primary/current path:** carries the physical actuator current through the sensor.
- **Measurement/signal side:** contains the low-voltage Hall sensing electronics and analog output that feed the later AFE and ADC stages.

The ACS724 is therefore inserted in series with the actuator-current path; it is not used as an external clamp around an untouched conductor.

## 3.2 — Exact ACS724-05AU variant

**Status:** Complete / accepted

### SENS-002 — Rev-1 sensor operating range and polarity

**Status:** Accepted

Rev-1 shall use the ACS724LLCTR-05AU within its specified **0 A to 5 A unidirectional sensing range**.

At a nominal sensor supply of 5 V, the nominal zero-current output is **0.5 V** and the nominal sensitivity is **800 mV/A**.

The unidirectional range means the specified measurement range is intended for one current polarity, which matches the normal current direction of the Rev-1 DC actuator. This does not imply that a DC-motor current waveform is constant: startup transients, commutation ripple, load variation and other time-varying components may still be present and are part of the waveform we intend to measure.

A current waveform that must be measured accurately in both positive and negative directions, such as a bipolar AC waveform or a reversing-current application, requires a sensing arrangement with an appropriate bidirectional range.

Values outside the specified 0 A to 5 A range shall not be treated as calibrated valid measurements merely because the sensor may continue to produce an output.

### Rationale

The selected 05AU variant allocates its useful analog output span to one current polarity. This provides 800 mV/A nominal sensitivity at 5 V, which is advantageous for resolving current changes in the Rev-1 low-voltage DC actuator while preserving the selected 0 A to 5 A Phase 1 measurement range.

### SENS-003 — Sensor supply dependence

**Status:** Accepted

The Rev-1 ACS724-05AU sensor model shall account for the dependence of zero-current output and sensitivity on the sensor supply voltage.

The nominal **0.5 V zero-current output** and **800 mV/A sensitivity** shall be treated as nominal values associated with a **5 V sensor supply**, rather than as supply-independent constants.

Actual sensor-supply behaviour shall be considered during characterization and calibration. The design shall not assume an ideal fixed 5.000 V supply when evaluating measurement accuracy.

### Rationale

The ACS724 output is ratiometric with its supply. A change in sensor supply voltage changes the sensor output scaling, including the zero-current output and sensitivity. Ignoring this dependence would create a current-conversion error even if the Hall sensing element itself were functioning normally.

This supply dependence therefore becomes an input to later transfer-function definition, characterization, calibration and the Phase 4 measurement-error budget.

### SENS-004 — Sensor bandwidth configuration

**Status:** Accepted

Rev-1 shall initially use the Pololu #4048 carrier in its stock FILTER configuration, including the carrier's existing **1 nF FILTER capacitor**, giving an approximate carrier bandwidth of **90 kHz**.

No additional FILTER capacitance shall be added during the initial ACS724 sensor characterization.

The ACS724 IC bandwidth is higher than the Rev-1 required **DC to 10 kHz** diagnostic measurement bandwidth, so the sensor itself is not expected to be the limiting element for that requirement.

The later Analog Front End shall provide the deliberate anti-alias filtering required for the **DC to 10 kHz measurement path** and **100 kS/s ADC acquisition** rather than relying on the stock sensor bandwidth as the anti-alias filter.

### Rationale

Keeping the stock sensor configuration during characterization avoids mixing sensor evaluation with Analog Front End design. The Pololu carrier bandwidth remains much wider than the required 10 kHz signal band, while content above the 50 kHz Nyquist frequency of a 100 kS/s ADC must later be attenuated by a deliberately designed anti-alias filter.

### SENS-005 — Primary current-path resistance

**Status:** Accepted

The Rev-1 sensor model shall include the ACS724 primary-conductor resistance, nominally approximately **1.2 mΩ**, as an insertion effect in the actuator-current path.

The resulting voltage drop and resistive dissipation shall be considered when evaluating sensor heating and disturbance of the actuator circuit:

`Vdrop = I × Rprimary`

`Ploss = I² × Rprimary`

### Rationale

The ACS724 is inserted in series with the actuator current, so its primary conductor cannot be electrically invisible. The very low primary-path resistance minimizes the voltage drop and power loss while still allowing the measured current to generate the magnetic field used by the Hall sensing elements.

### SENS-006 — Isolation-rating interpretation

**Status:** Accepted

The ACS724 isolation specifications shall be interpreted according to their defined purpose. The **2400 V RMS dielectric-strength value** is a short-duration insulation test rating and shall not be treated as a continuous working voltage.

The IC datasheet's continuous working-voltage, surge, creepage and clearance specifications shall be documented separately from dielectric-test voltage.

For Rev-1, the Pololu carrier remains restricted to the established **low-voltage laboratory application of 24 V or less**. IC-level isolation ratings shall not be used to justify direct connection of the hobby carrier, breadboard, Arduino, or ordinary laboratory equipment to industrial mains or 400 V motor circuits.

### Rationale

A dielectric withstand test verifies that an isolation barrier can survive a specified high test voltage for a limited test duration. It is not the same quantity as the voltage permitted continuously across the barrier in service.

Safe system-level working voltage also depends on the complete implementation, including carrier PCB geometry, connectors, wiring, insulation, environment and applicable safety requirements. Therefore the IC's isolation test rating cannot by itself establish the safe operating voltage of the complete laboratory prototype.

### SENS-007 — Sensor accuracy characterization principle

**Status:** Accepted

The Rev-1 current conversion shall not assume that the nominal ACS724-05AU zero-current output and sensitivity are exact.

Datasheet sensitivity error, voltage-offset error, total output error and temperature dependence shall be treated as measurement-system error sources.

The actual sensor offset and sensitivity shall therefore be experimentally characterized and later calibrated. The Phase 1 **±0.10 A current-accuracy target shall not be considered demonstrated by nominal datasheet values alone**.

### Rationale

The ACS724 datasheet specifies finite offset, sensitivity and total-output error, and these quantities vary with temperature. At full-scale current, the specified total-output error can be comparable to or larger than the Phase 1 ±0.10 A target when nominal scaling is used without calibration.

The Rev-1 laboratory environment is near room temperature, but the individual carrier's actual offset and gain still need to be measured. These measured values will later feed the calibration procedure and Phase 4 measurement-error budget.

## 3.3 — Sensor transfer function

**Status:** Complete / accepted

### SENS-008 — Current conversion model

**Status:** Accepted

Rev-1 shall use the parameterized ACS724 current-to-voltage transfer model:

`VOUT = Voffset + S × I`

and the inverse current-conversion model:

`I = (VOUT - Voffset) / S`

At a nominal sensor supply of `VCC = 5 V`, the initial nominal parameters are `Voffset = 0.5 V` and `S = 0.8 V/A`.

The offset and sensitivity shall remain explicit model/calibration parameters rather than permanently fixed exact constants. Characterization and later calibration may replace the nominal values with measured values for the individual sensor/carrier.

### Rationale

The forward equation describes how actuator current becomes an analog sensor output voltage. The inverse equation is required by the measurement system because the ADC observes voltage while downstream processing requires current in amperes.

Keeping offset and sensitivity as parameters preserves the supply dependence and sensor-to-sensor variation already established by SENS-003 and SENS-007 and allows calibration to improve the current conversion without changing the fundamental model.

## 3.4 — Error mechanisms

**Status:** Complete / accepted at sensor-characterization level

### SENS-009 — Sensor error characterization categories

**Status:** Accepted

Rev-1 sensor characterization shall distinguish between:

1. **offset error**,
2. **sensitivity/gain error**,
3. **temperature-dependent variation**,
4. **output noise**, and
5. **frequency/dynamic-response error**.

Supply dependence established by SENS-003 and total-output error established by SENS-007 shall remain part of the sensor error model.

Offset and sensitivity shall be treated as calibration parameters where practical. Noise, temperature dependence and dynamic behaviour shall be characterized separately rather than assuming that calibration removes them.

### Rationale

Fixed or slowly varying systematic errors can often be reduced by calibration, but random noise and frequency-dependent behaviour are different phenomena. A single offset/gain correction cannot remove random sample-to-sample variation, temperature drift outside the calibrated condition, or signal attenuation/phase change caused by finite bandwidth.

This distinction is important because the project must preserve current-waveform features such as commutation ripple and other time-varying signatures, not only average current.

A complete numerical system error budget, including ADC and AFE contributions, remains reserved for Phase 4.

## 3.5 — Bandwidth and FILTER pin

**Status:** Complete / accepted at sensor-characterization level

### SENS-010 — FILTER-pin role

**Status:** Accepted

The ACS724 FILTER pin shall be treated as a means of trading sensor bandwidth for output-noise reduction.

Any future change from the stock Pololu FILTER configuration shall require verification that the resulting sensor response still preserves the accepted **DC to 10 kHz diagnostic band**.

The ACS724 FILTER pin shall not by itself be considered the complete ADC anti-alias filter. Deliberate anti-alias filtering remains an Analog Front End design responsibility.

### Rationale

Restricting analog bandwidth excludes out-of-band noise and can improve effective measurement resolution, but excessive filtering would also attenuate real diagnostic current-waveform content. The Rev-1 design therefore preserves the stock sensor bandwidth during initial characterization and defers deliberate anti-alias filter design to the later AFE phase.

## 3.6 — Characterization and test plan

**Status:** In progress

### SENS-011 — Static characterization method

**Status:** Accepted

Initial ACS724 static characterization shall use a **controlled low-voltage DC current path independent of the actuator**, with the bench PSU current limit configured before the output is enabled.

For each characterization point, an independent reference current measurement and the ACS724 output voltage shall be recorded. Characterization shall include zero current and multiple points across the 0 A to 5 A range where the available load and reference instrument can safely support them.

The actuator motor shall not be used as the primary reference load for deriving sensor offset, sensitivity or linearity.

The required high-current load hardware is currently **TBD** and shall be selected before the high-current characterization is executed. The existing 1/4 W resistor assortment shall not be used as a multi-ampere power load.

### Rationale

A motor is a poor calibration reference because its current varies with commutation, speed, mechanical load and operating state. A controlled DC load provides stable current points that can be compared directly with the sensor output.

An independent reference measurement prevents the bench PSU display from being assumed to be an exact current standard. Multiple known current points allow the measured offset, sensitivity and linearity of the individual ACS724 carrier to be derived.

### SENS-012 — Static characterization data record

**Status:** Accepted

For each valid static characterization point, Rev-1 shall record at minimum:

- independent reference current `IREF`,
- ACS724 output voltage `VOUT`,
- actual sensor supply voltage `VCC`,
- approximate test temperature,
- relevant bench-PSU and test conditions.

Multiple points across the usable range shall be used to derive the measured offset and sensitivity and to calculate residuals from the fitted linear model.

Where practical, ascending and descending current sweeps shall be used to expose drift, heating, repeatability, or hysteresis-like effects that could be hidden by a single one-direction sweep.

Phase 3 shall report the measured sensor error contribution. Final compliance with the Phase 1 **±0.10 A system current-accuracy requirement** shall be determined through the Phase 4 system error budget rather than assigning the complete accuracy allowance to the sensor alone.

### Rationale

Because the ACS724 is ratiometric and temperature-sensitive, a current/output pair without supply and temperature context is insufficient for reproducible characterization. Repeated points and model residuals provide evidence of linearity and repeatability beyond a simple two-point gain calculation.

The sensor is only one contributor to total measurement error; the later AFE, ADC, voltage reference/supply, calibration method and reference measurement also consume part of the system accuracy budget.

Remaining characterization work shall define the zero-current/noise test and any feasible dynamic/bandwidth verification before Phase 3 test execution is treated as complete.

## 3.7 — Phase output

**Status:** TBD

The completed phase is expected to contain:

- sensor operating model,
- transfer equation,
- operating range and key limits,
- relevant error mechanisms,
- bandwidth and filtering behaviour,
- electrical/interface assumptions,
- characterization method,
- measured results when hardware is available,
- limitations and remaining TBD items.
