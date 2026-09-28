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

## Historical next action after B-009

At this point the planned next action was to route motor current through the ACS724 and perform a DC comparison. That action was subsequently completed and superseded by the later Stage-B work recorded below.

---

## B-010 — ACS724 DC calibration completed

A controlled resistor-load calibration established the bench transfer:

`VOUT = 0.46910 + 0.74472·I`

with `VOUT` in volts and `I` in amperes.

Inverse:

`I = (VOUT - 0.46910)/0.74472`

Coefficient of determination:

`R² ≈ 0.999997`

over the measured low-current interval up to approximately 0.208 A.

This is the practical calibration of this bench sensor under the recorded conditions. It does not imply full 0–5 A production calibration or temperature invariance.

A later motor check gave approximately 34.8 mA sensor-derived current against an approximately 35 mA PSU indication. The PSU display is not treated as a precision reference.

---

## B-011 — Temporary MCP6022 positive-current stimulus fixture

A temporary MCP6022 fixture was built because the AFG did not provide a usable DC-offset function for the required positive-only ACS724 stimulus.

The fixture is **not** the frozen Rev-1 AFE. It exists only for Stage-B dynamic sensor characterization.

Key configuration:

- MCP6022 pin 8 = +5 V;
- pin 4 = GND;
- 100 nF local bypass between pins 8 and 4;
- channel B buffers the reference;
- channel A implements an approximately unity-ratio biased inverting driver;
- driver output → 220 Ω → ACS724 IP+ → IP− → R8 = 67 Ω → GND;
- CH1 measures R8;
- CH2 measures ACS724 OUT.

During 2026-09-28 troubleshooting, a physical package-numbering mistake was identified: the right-hand side of a PDIP-8 is 8, 7, 6, 5 from top to bottom in top view. Earlier temporary diagnoses that depended on incorrectly named right-side pins are invalid. After correcting orientation, the 5 kHz stimulus returned to approximately 2.1 Vpp at MCP6022 pin 1 and approximately 0.5 Vpp raw across R8.

---

## B-012 — ACS724 FILTER candidate and corrected ground connection

The carrier stock FILTER capacitance is approximately 1 nF. The current experimental addition is 4.7 nF from FILTER to GND, giving approximately 5.7 nF total.

Using the approximate internal FILTER resistance 1.8 kΩ:

`fc ≈ 1/(2π·1.8 kΩ·5.7 nF) ≈ 15.5 kHz`

A physical FILTER-ground connection problem was found and corrected during the characterization campaign.

After the correction, larger diagnostic capacitances clearly reduced broadband CH2 variation. However:

- +10 nF gives an approximate simple corner near 8 kHz;
- +22 nF gives approximately 3.8 kHz;
- +100 nF gives approximately 0.88 kHz.

Because the formal diagnostic band is DC–10 kHz, the larger values are not accepted merely for producing a quieter trace.

**Disposition:** +4.7 nF remains the provisional Stage-B FILTER candidate. Final selection is deferred to complete analog-chain verification.

---

## B-013 — Corrected dynamic characterization through 10 kHz

The corrected post-fix campaign used coherent sine fitting rather than raw scope Vpp.

For target frequency `f`:

`v(t) = VDC + A sin(2πft) + B cos(2πft)`

`Vpp = 2 sqrt(A²+B²)`

`Ipp = VCH1,pp / 67 Ω`

`H(f) = VCH2(f) / Iprimary(f)`

Main repeated-set complex averages:

- 1 kHz: approximately **0.886 ∠ -6.5° V/A**;
- 5 kHz: approximately **0.871 ∠ -23.3° V/A**;
- 7.5 kHz: approximately **0.735 ∠ -36.5° V/A**;
- 10 kHz: approximately **0.803 ∠ -50.3° V/A**.

These values are descriptive repeated-set results, not accepted final AC calibration constants.

Primary-current excitation was highly stable. Typical CH2 coherent signal was only approximately 4–7 mVpp while CH2 residual RMS was approximately 13–15 mV.

A 7.5 kHz ten-run block showed a large magnitude change between its first and second halves. An interleaved 5 → 7.5 → 10 → 5 → 7.5 → 10 kHz sequence did not show a common monotonic time/warm-up trend. The limiting uncertainty is therefore concentrated in the small CH2 coherent estimate rather than in primary-current repeatability.

Detailed evidence: [post-fix dynamic characterization report](evidence/acs724-postfix-dynamic-characterization-and-afe-handoff-2026-09-28.md).

---

## B-014 — Scope phase-skew and feedthrough controls

### Same-node timing control

Both probes were connected to the same R8 node.

Observed raw CH2−CH1 phase:

- 10 kHz / 4 µs sample interval: approximately -13.92°;
- 1 kHz / 40 µs sample interval: approximately -14.79°.

One stored sample corresponds to 14.4° in both of those specific cases. Advancing CH2 by one sample reduced the same-node phase to approximately +0.48° at 10 kHz and -0.39° at 1 kHz.

Accepted statement:

**The DOS1102S exported CH2 waveform appears approximately one stored sample behind CH1 in the tested modes. The internal cause is unknown.**

### Open-primary feedthrough

With the primary path open but AFG/MCP6022 operating:

- 1 kHz CH2 coherent component ≈ 0.0635 mVpp;
- 5 kHz ≈ 0.0132 mVpp;
- 10 kHz ≈ 0.0734 mVpp.

These are far smaller than the current-on several-millivolt coherent response and are deeply buried in their own residual variation.

Conclusion:

**Direct AFG/MCP6022 feedthrough is not a plausible dominant explanation for the current-on coherent CH2 signal.**

---

## B-015 — Raw-sensor dynamic campaign closure

The campaign established:

- a working positive-current fixture;
- stable primary-current reference;
- corrected FILTER grounding;
- practical acquisition settings through 10 kHz;
- coherent-fit analysis;
- measured one-sample CH2 CSV timing skew;
- negligible direct stimulus-generator feedthrough;
- a clear raw-output SNR/repeatability limitation.

The campaign did **not** establish:

- final ACS724 AC sensitivity;
- unique intrinsic sensor phase/pole model;
- final FILTER capacitance;
- final end-to-end measurement-chain bandwidth.

Collecting more identical raw-sensor captures is not expected to resolve the remaining uncertainty efficiently.

---

## Immediate next action — AFE bring-up

Proceed to **independent Analog Front End bring-up and validation**.

Do not connect the ACS724 to the AFE as the first test.

Start from the frozen AFE design and:

1. identify each stage and component role;
2. verify power and DC operating points;
3. predict low-frequency gain and designed filter response;
4. apply a known clean input stimulus;
5. measure AFE input and output simultaneously;
6. verify gain, phase/roll-off, stability, and clipping margin;
7. only after the AFE behaves as designed connect `ACS724 OUT → AFE`;
8. then proceed toward deterministic RA4M1 ADC acquisition.

Reason: the raw ACS724 experiment has isolated the next bottleneck as signal conditioning / measurement-chain SNR rather than stimulus instability. The AFE is the designed subsystem responsible for conditioning the sensor signal before ADC integration.
