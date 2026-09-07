# 15 — Stage B Implementation Log

**Status:** Working implementation record  
**Relationship to Stage A:** Stage A Rev-1 remains frozen. This file records Stage B bench implementation, measurements, limitations, and next actions. It does not silently change frozen design decisions.

## Working method

All Stage B work follows:

`predict → connect/configure → measure → compare → understand → document`

Measurements are recorded as observed. Unknown or missing values remain unknown until retrieved or remeasured.

---

## B-001 — Target actuator identification

The target actuator is the small Philips/Saeco 24 VDC brew-system motor with worm-style output shaft/gearing. Larger grinder motors observed on the bench are not part of the primary characterization at this stage.

---

## B-002 — Motor winding resistance

Measured with the multimeter across the motor terminals:

- initial observed resistance: approximately **33 Ω**
- while the rotor/worm was slowly moved: approximately **30–60 Ω**

The variation with rotor position is treated as an observed brushed-motor/commutator effect. No single fixed winding resistance is assumed from this measurement.

---

## B-003 — Low-voltage motor characterization

### 3 V test

Observed behavior:

- self-start was unreliable
- one observed non-start condition: approximately **97 mA** on the PSU display
- after slight mechanical movement, the motor started
- running current after start: approximately **34–35 mA**

Conclusion:

**3 V is not a reliable self-start condition for the tested motor in the tested condition.** This result is not classified as a motor fault.

### 4 V test

Observed behavior:

- self-start was reliable in the repeated tests performed
- steady PSU current: approximately **35–36 mA**
- brief PSU-display indication during startup: approximately **60–75 mA**

Limitation:

The PSU display is too slow to establish the true instantaneous startup-current peak. The 60–75 mA observation is therefore only a display observation, not a validated startup-peak measurement.

---

## B-004 — Motor-voltage oscilloscope test

CH1 was connected directly across the motor:

- probe tip → motor positive
- probe ground → motor negative / PSU−

This measures `V_motor(t)`, not motor current.

At steady 4 V operation, the trace showed the expected DC level with small disturbances/spikes. Their exact physical origin has not yet been proven and they are not yet diagnostic evidence.

---

## B-005 — PSU turn-on transient separation

A single-shot capture of PSU turn-on initially appeared to show a slow motor-voltage rise. A control experiment was then repeated with the motor disconnected.

A similar voltage rise remained with no motor connected.

Conclusion:

**The observed 0 → 4 V ramp is primarily associated with the bench-PSU output turn-on behavior, not directly with motor acceleration.**

Measured 10–90% rise time for the nominal 0 → 4.00 V transition:

`t_10-90 ≈ 73.0 ms`

Equivalent first-order interpretation only:

- `τ ≈ 73.0 ms / 2.197 ≈ 33.2 ms`
- `f_c ≈ 1 / (2π τ) ≈ 4.8 Hz`

The 4.8 Hz value is **not** a measured motor bandwidth, ACS724 bandwidth, or complete PSU control-loop bandwidth. It is only an equivalent first-order interpretation of this measured turn-on edge.

---

## B-006 — ACS724 identification and signal-side bring-up

Hardware identified as **Pololu #4048 ACS724LLCTR-05AU**, unidirectional 0–5 A current-sensor carrier.

Relevant nominal values used for prediction:

- sensor supply range: **4.5–5.5 V**
- nominal sensitivity at 5 V: **800 mV/A**
- nominal zero-current output at 5 V: **0.5 V**

The 3-pin signal header was soldered successfully.

Earlier stable zero-current output after improving physical connections:

`V0 ≈ 0.49 V`

An earlier unstable clip arrangement produced approximately 0.43 V and was rejected as a reliable baseline.

A later zero-current characterization was performed, but the exact noise RMS/Vpp values are missing from the accessible transcript. Those values must not be reconstructed. If required, they must be retrieved from a saved scope image or deliberately remeasured and labeled as a new measurement.

---

## B-007 — Breadboard / Arduino supply troubleshooting

During ACS724 signal-side wiring, an incorrect breadboard connection caused the Arduino UNO R4 WiFi to stop operating. Power was removed and the incorrect jumpers were removed. The Arduino resumed normal operation.

This event established a procedural rule for the remaining bench work:

**Use explicit breadboard coordinates and verify one connection at a time before applying power.**

The breadboard topology used in this project is treated as:

- each numbered five-hole group `a–e` is internally connected
- each numbered five-hole group `f–j` is internally connected
- the center gap isolates `a–e` from `f–j`
- adjacent numbered rows are not connected
- power rails are separate from the numbered terminal strips and must be wired explicitly

Current intended signal-side arrangement:

- Arduino 5 V → breadboard positive rail
- Arduino GND → breadboard ground rail
- positive rail → ACS724 VCC row
- ground rail → ACS724 GND row
- ACS724 OUT left unconnected until measurement

---

## B-008 — Multimeter / supply indication check

Raw measurements with the currently used VC830L multimeter:

- Arduino `5V` to `GND`: approximately **4.5 V**
- Jesverty PSU set to **5.00 V**, measured directly at PSU output with no load: approximately **4.8–4.9 V**
- ACS724 zero-current OUT under the current Arduino-powered arrangement: approximately **0.47–0.48 V**

Interpretation limitation:

The PSU comparison suggests the multimeter may indicate approximately 0.1–0.2 V below the PSU set/display value near 5 V, but this is **not a formal multimeter calibration**. The true Arduino 5 V rail therefore remains uncertain from these measurements alone.

Do not silently correct raw measurements by adding 0.1–0.2 V. Record raw readings and instrument/reference uncertainty separately.

---

## B-009 — Prediction for first motor-current measurement through ACS724

Previously measured unloaded motor current at 4 V:

`I_run ≈ 35 mA`

Using nominal ACS724 sensitivity:

`ΔV = 0.8 V/A × 0.035 A ≈ 28 mV`

Using the earlier practical zero baseline `V0 ≈ 0.49 V`, predicted running output is approximately:

`V_OUT,run ≈ 0.518 V`

This is a prediction only. The actual value has not yet been measured with motor current routed through the ACS724.

---

## Immediate next action

Establish the high-current path with PSU output OFF:

`PSU+ → ACS724 IP+ → ACS724 IP− → motor → PSU−`

Keep the ACS724 signal side powered separately from the Arduino 5 V/GND arrangement.

Before startup-waveform work, first validate the DC transfer by recording:

- motor-off zero-current output `V0`
- steady-running output `V_RUN`
- simultaneous PSU current indication

Then calculate the first sensor-derived current using the nominal sensitivity:

`I = (V_RUN - V0) / 0.8`

and compare it with the PSU indication.

Only after this DC check succeeds should the oscilloscope be used to capture the true ACS724 output waveform during motor startup.
