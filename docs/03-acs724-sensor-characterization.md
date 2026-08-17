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

### SENS-013 — Zero-current offset and noise test

**Status:** Accepted

The ACS724 zero-current characterization shall be performed with the sensor electronics powered and **no current flowing through the primary current path**.

The test shall record repeated `VOUT` measurements together with the actual sensor supply voltage `VCC` and approximate test temperature.

The mean zero-current output shall be treated as the measured zero-current offset under the recorded test conditions. Short-term variation around that mean shall be characterized separately as output noise using suitable statistical measurements and/or oscilloscope observations.

Offset and noise shall not be combined into a single characterization value.

### Rationale

Offset is a systematic shift in the mean sensor output at zero primary current, whereas noise is the short-term variation of individual measurements around that mean. Separating the two allows the offset to be used as a calibration parameter while preserving noise as an independent limit on repeatability and effective resolution.

Powering the sensor with the primary path at true zero current isolates the sensor's own zero-current behaviour from load-current variation. Recording `VCC` and temperature preserves the operating conditions needed to interpret the result.

### SENS-014 — Dynamic bandwidth verification

**Status:** Accepted

Phase 3 dynamic characterization shall, where practical, verify ACS724 response using a controlled periodic primary-current stimulus at multiple frequencies through the accepted **DC to 10 kHz diagnostic band**.

The test shall compare the ACS724 output waveform with an independent representation of the applied current and shall evaluate amplitude response and, where practical, phase behaviour.

In addition to the Rev-1 requirement-oriented verification through 10 kHz, Phase 3 shall include an **educational extended frequency sweep** toward and, where practical, beyond the Pololu carrier's vendor-stated approximately **90 kHz bandwidth**. The purpose of this extension is to observe the frequency-response roll-off and experimentally estimate the carrier bandwidth/cutoff behaviour.

Experimental confirmation of the vendor bandwidth is a study and characterization objective, not a Rev-1 system-acceptance requirement. Failure to reproduce the vendor value with the available laboratory stimulus/measurement setup shall be reported as a test limitation rather than silently interpreted as sensor failure unless the test method itself has been validated.

The exact dynamic-current stimulus circuit remains **TBD** until the available function-generator capability and suitable current-driving/reference hardware are established.

### Rationale

The system requirement only demands preservation of current information through 10 kHz, so that band remains the formal engineering verification target. Extending the sweep toward the carrier bandwidth provides a useful laboratory lesson in frequency response, gain roll-off and bandwidth measurement without changing the Rev-1 requirement.

Because the oscilloscope function generator is a signal source rather than inherently a multi-ampere current source, the dynamic-current driver and reference method must be designed before the extended sweep is treated as valid evidence.

### SENS-015 — Bandwidth estimation method

**Status:** Accepted

For the educational extended dynamic characterization, frequency response shall be evaluated from the ratio of ACS724 output AC amplitude to independently measured primary-current AC amplitude.

The resulting transfer magnitude shall be normalized to a low-frequency reference. The experimental bandwidth shall be estimated from the frequency at which the normalized amplitude approaches **0.707 of the low-frequency value**, corresponding to approximately **−3 dB**.

The measured response shall be compared with the vendor-stated carrier bandwidth while distinguishing the bandwidth of the bare ACS724 IC from the bandwidth of the Pololu carrier with its installed FILTER capacitor.

### Rationale

Bandwidth is not established merely by observing that a waveform remains visible at a particular frequency. A normalized amplitude-response measurement provides a reproducible way to observe gain roll-off and estimate the conventional −3 dB cutoff point.

Separating bare-IC and assembled-carrier bandwidth prevents the carrier's FILTER network from being incorrectly attributed to the sensor IC itself and makes the extended sweep a useful study of practical frequency-response measurement.

### SENS-016 — Dynamic stimulus strategy

**Status:** Accepted

Phase 3 shall initially attempt the educational frequency-response characterization using the DOS1102S function generator as a **small-signal excitation source**, not as a multi-ampere power source.

Actual primary current shall be independently derived from a suitable series reference resistor or equivalent current-reference method rather than inferred solely from the generator setting.

The periodic stimulus shall remain within the ACS724-05AU unidirectional operating regime, using positive-current bias where necessary.

If the resulting ACS724 output does not provide sufficient signal-to-noise ratio for reliable gain measurement, a higher-current external driver shall be designed as a subsequent test method rather than increasing generator loading beyond its established capability.

### Rationale

Bandwidth measurement requires a controlled, measurable periodic current but does not require operation at the 5 A full-scale current. Starting with a small-signal method minimizes additional hardware and allows the actual current waveform to be measured independently.

The generator setting alone is not accepted as the current reference because source impedance and load affect delivered current. The ACS724-05AU is unidirectional, so any periodic test current must remain within the intended one-polarity operating regime.

### SENS-017 — Positive-biased dynamic stimulus

**Status:** Accepted

The initial small-signal dynamic test shall preferentially use the function generator's DC-offset capability to produce a periodic stimulus whose primary current remains positive throughout the cycle.

The test shall satisfy:

`IDC > IAC`

such that the instantaneous primary current does not intentionally reverse polarity and remains within the ACS724-05AU specified 0 A to 5 A measurement range.

Actual current shall continue to be derived from the independent reference measurement rather than from nominal generator amplitude or offset settings.

A separate bench-PSU-plus-generator summing topology shall not be improvised by directly connecting the two sources. If external DC-bias injection becomes necessary, its coupling/summing network shall first be deliberately designed and verified.

The exact DOS1102S usable DC-offset range and resulting test values remain **TBD until verified on the instrument or its documentation**.

### Rationale

A zero-centred sinusoidal current reverses direction every half-cycle and would leave the intended one-polarity measurement regime of the 05AU variant. Adding positive DC bias permits a sinusoidal small-signal current to be measured while keeping the instantaneous current positive.

Using a single generator's verified offset capability is the simplest initial method. Directly paralleling an independent bench supply and function generator is not an acceptable way to combine DC and AC sources because the sources can drive each other unless a deliberate coupling or summing network is used.

### SENS-018 — Phase 3 test-hardware readiness

**Status:** Accepted

Before Phase 3 static or dynamic characterization results are accepted as engineering evidence:

1. the independent current-reference method shall be identified and its relevant accuracy/range documented;
2. the static 0 A to 5 A test shall use a load with adequate voltage, current and power rating;
3. the dynamic test shall use a characterized current-reference element such as `RREF` or an equivalent validated reference method;
4. the multi-ampere primary-current path shall use suitable conductors and connections rather than a solderless breadboard; and
5. missing equipment or exact component values shall remain **TBD** until selected and verified.

The zero-current characterization may be executed before the high-current load is available because it does not require current through the primary path.

### Rationale

A characterization result is only as trustworthy as its stimulus and reference measurement. Unknown reference-instrument uncertainty, an under-rated power load, or unsuitable high-current wiring could invalidate the result or create avoidable hardware risk.

Separating zero-current characterization from the later powered-current tests allows useful Phase 3 measurements to begin without pretending that the complete static and dynamic test setup is already ready.

### SENS-019 — Characterization execution order

**Status:** Accepted

The first physical ACS724 characterization shall be the **zero-primary-current test** established by SENS-013.

Before power is applied, the exact Pololu #4048 supply, output, ground and primary-current connections shall be identified and the wiring shall be inspected.

With the primary path carrying no current, the sensor shall then be powered at its intended laboratory supply and the actual `VCC` and `VOUT` shall be measured. The zero-current output shall be observed using both a DC measurement and, where practical, an oscilloscope observation of short-term output variation.

Powered-current static and dynamic tests shall follow only after their required load/reference hardware has satisfied SENS-018.

### Rationale

Starting at zero primary current provides the lowest-risk first hardware check and establishes the individual carrier's zero-current offset and short-term output behaviour before power-current variables are introduced.

The inspect–wire–verify–power–measure sequence reduces the risk of wiring errors and creates a reproducible baseline before the static and dynamic characterization stages.

### SENS-020 — Supply-source comparison

**Status:** Accepted

Initial zero-current characterization shall be performed with both a controlled laboratory 5 V supply and, separately, the Arduino UNO R4 WiFi 5 V rail.

For each supply configuration, the actual sensor `VCC`, mean zero-current `VOUT`, approximate temperature and short-term output variation shall be recorded.

Differences in zero-current output shall first be evaluated against the ACS724 supply-dependent/ratiometric behaviour before being interpreted as sensor error.

Differences in measured noise shall be treated as configuration-level observations unless further testing isolates the responsible source.

The bench-supply configuration shall serve as the initial controlled baseline.

### Rationale

Using both available 5 V sources turns the initial zero-current test into a controlled comparison rather than a single functional check. Because the ACS724 zero-current output and sensitivity depend on supply voltage, actual `VCC` must be measured before output differences are interpreted.

Comparing short-term output behaviour under both sources is educational and may reveal configuration-dependent noise, but the comparison alone does not establish which individual element causes any observed difference.

### SENS-021 — Supply-comparison controls

**Status:** Accepted

For the bench-supply versus Arduino-5-V zero-current comparison, the **supply source shall be the intentionally changed variable**. The sensor, zero-primary-current condition, measurement points, instruments, probe configuration and relevant oscilloscope settings shall otherwise be held constant where practical.

`VCC` shall be measured at the ACS724 carrier rather than inferred solely from the nominal source setting.

Where practical, the comparison shall use an **A–B–A sequence** — bench supply, Arduino supply, bench supply again — to help distinguish supply-dependent differences from time-, temperature- or drift-related changes.

Any unavoidable differences in wiring, grounding, USB connection or other test conditions shall be recorded as potential confounding variables.

### Rationale

A controlled comparison is only meaningful when the intended independent variable is separated from other changing conditions. Holding the measurement configuration constant reduces ambiguity when comparing mean zero-current output and short-term noise.

Repeating the bench-supply baseline after the Arduino measurement provides a simple check for time-dependent drift or warming that could otherwise be mistaken for a supply-source effect.

### SENS-022 — Zero-current comparison evidence record

**Status:** Accepted

For each `A1–B–A2` zero-current supply-comparison step, Phase 3 shall record at minimum:

- supply configuration and sequence position;
- actual ACS724 `VCC` measured at the carrier;
- zero-current `VOUT`;
- approximate test temperature;
- relevant wiring, USB and grounding state;
- oscilloscope observation of `VOUT`; and
- oscilloscope settings required to interpret and reproduce the observation.

The same measurement method and oscilloscope configuration shall be maintained across the comparison where practical.

Raw readings and waveform evidence shall be preserved separately from later interpretation. Numerical noise metrics may be added once the available instrument measurement method has been verified.

### Rationale

A standardized evidence record makes the A–B–A comparison reproducible and prevents later conclusions from depending on memory or screenshots whose settings are unknown.

Keeping raw observations separate from interpretation preserves the evidence needed to revisit conclusions if later testing reveals a confounding factor or measurement limitation.

### SENS-023 — Measurement-system noise-floor control

**Status:** Accepted

Before interpreting zero-current oscilloscope variation as ACS724 output noise, Phase 3 shall characterize the relevant **measurement-system noise floor** using the same oscilloscope channel, probe and comparable acquisition settings with the probe input referenced to ground.

The sensor-connected measurement and the measurement-system control shall use comparable probe grounding and oscilloscope configuration.

Observed variation shall not automatically be attributed entirely to the ACS724. Probe pickup, oscilloscope input noise, grounding, supply-related disturbance and environmental interference shall remain possible contributors until isolated experimentally.

Any quantitative separation of independent noise contributions shall use an appropriate noise metric and combination method rather than direct subtraction of peak-to-peak values.

### Rationale

An oscilloscope trace contains contributions from the device under test and the measurement chain. Measuring the setup with an ideally zero input establishes the practical floor against which sensor-connected variation can be interpreted.

Peak-to-peak values from independent random-noise sources are not generally separable by direct arithmetic subtraction, so quantitative decomposition requires a suitable statistical or RMS-type metric and an explicitly justified model.

Remaining characterization work shall establish the numerical noise metric used for Phase 3 comparison before powered-current Phase 3 test execution is treated as complete.

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
