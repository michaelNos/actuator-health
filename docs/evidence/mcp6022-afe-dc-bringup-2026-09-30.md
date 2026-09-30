# MCP6022 Rev-1 AFE DC bring-up — 2026-09-30

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — independent AFE bring-up  
**Status:** Initial DC continuity/supply/unity-path check completed

## Purpose

Validate the newly built Rev-1 MCP6022 analog front end at DC before applying an AC stimulus.

## Measured supply

Measured directly across the MCP6022 supply pins:

- pin 8 (VDD) relative to pin 4 (VSS): **4.92 V**

Result: **PASS** for the present 5 V measurement-domain bring-up check.

## DC signal-path measurements

Observed DC voltages:

- `TP_SENSOR`: **0.49 V**
- MCP6022 pin 3 (+IN A): **0.48 V**
- MCP6022 pin 1 / OUTA: **0.49 V**
- MCP6022 pin 5 (+IN B): **0.49 V**
- MCP6022 pin 7 / TP_AFE: **0.49 V**
- `ADC_IN`: **0.49 V**

Interpretation:

The two unity-gain Sallen-Key sections pass the present DC level essentially unchanged through the complete AFE path. The approximately 10 mV difference observed at pin 3 is not assigned to a specific cause from this one measurement.

No AC transfer conclusion is made from this test.

## Continuity note

The user reported continuity checks as beeping. Because the AFE includes supply capacitors across `5V_MEAS` and `GND_MEAS`, a continuity meter may beep transiently while charging those capacitors. A sustained low-resistance short between the supply rails would be a fault; the powered 4.92 V measurement is consistent with the rails not being hard-shorted.

## Next step

Perform independent low-frequency AC validation with a known AFG stimulus, ensuring only one active source drives `TP_SENSOR` at a time.


## Physical implementation checkpoint

Before the DC test, the previous temporary characterization fixture was removed from the breadboard and the Rev-1 AFE wiring was rebuilt from the accepted schematic.

Established physical state:

- MCP6022 powered on the 5 V measurement domain;
- 100 nF local bypass fitted across the MCP6022 supply;
- 10 µF local reservoir fitted across the same supply rails;
- both Sallen-Key op-amp channels physically connected;
- ADC-facing passive interface connected;
- ACS724 output not used as an active test stimulus during independent AFE bring-up;
- low-Q resistors are being implemented as **10 kΩ** parts for the breadboard build rather than the original 9.76 kΩ frozen nominal value.

The 10 kΩ substitution is a deliberate Stage-B implementation deviation and must be reflected in the implementation documentation/schematic before formal acceptance. It slightly shifts the low-Q natural frequency and therefore must be included in later AC prediction/comparison.

Exact AC behavior has **not** yet been validated.

## What this checkpoint proves

The present measurements establish several important facts.

### 1. The MCP6022 is receiving the intended supply

The measured 4.92 V directly across pins 8 and 4 proves that the supply reaches the IC itself through the breadboard connections.

This is stronger evidence than measuring only the breadboard rails.

### 2. The complete AFE has a valid DC operating path

At DC, capacitors behave approximately as open circuits after settling. The two Sallen-Key sections therefore reduce to their unity-gain feedback behavior.

The observed chain:

\`\`\`text
TP_SENSOR      0.49 V
pin 3          0.48 V
OUTA / pin 1   0.49 V
pin 5          0.49 V
TP_AFE / pin 7 0.49 V
ADC_IN         0.49 V
\`\`\`

shows that the DC operating level propagates through both op-amp stages and the ADC interface without a large offset, saturation, rail collapse, or gross wiring error.

### 3. Both op-amp feedback loops are functioning at DC

Channel A output is approximately equal to its non-inverting input level, and channel B output is approximately equal to its non-inverting input level.

This is consistent with the intended unity-gain follower behavior embedded inside the Sallen-Key topology.

### 4. The ADC interface does not disturb the DC level

The voltage at \`ADC_IN\` remains approximately the same as \`TP_AFE\`.

This is expected because the 1 kΩ / 100 pF interface is not intended to create a meaningful DC voltage drop when the ADC input is effectively high impedance.

## What this checkpoint does NOT prove

This test does **not** yet prove:

- the 15 kHz Butterworth response;
- the low-Q or high-Q pole frequencies;
- the expected Q values;
- AC magnitude accuracy;
- AC phase behavior;
- noise performance;
- clipping/headroom across the full intended 0.5–4.5 V span;
- ADC settling at 100 kS/s;
- integrated ACS724 → AFE behavior.

Those require controlled AC measurements and later ADC integration.

## Engineering gate

**DC bring-up gate: PASS.**

The AFE is ready for the first controlled AC stimulus test, subject to the rule that only one active source drives \`TP_SENSOR\` at a time.


## DOS1102S AFG constraint discovered before AC injection

Before connecting the AFG to \`TP_SENSOR\`, the generator output was checked directly with scope CH1.

User-observed settings/results:

- sine, 100 Hz;
- minimum practical AFG setting used: 0.5 Vpp;
- measured CH1: approximately **520 mVpp**;
- measured mean: approximately **-8 mV**;
- measured sine RMS: approximately **176 mV**.

Interpretation:

The built-in DOS1102S AFG is operating essentially zero-centered in this configuration. The user's instrument does not expose a DC-offset setting. Therefore the previously proposed direct \`0.5 Vpp + 0.5 V offset\` injection is **not available on this instrument and is withdrawn**.

A zero-centered 520 mVpp sine would extend below \`GND_MEAS\`, so it must **not** be connected directly to \`TP_SENSOR\` for Rev-1 AFE validation.

The next AC-validation step requires an explicit external bias/injection network or another verified positive-biased source. Per project method, that physical test network must be represented and understood before bench connection.


## Direct zero-centered AFG connection — invalid stimulus observation

A brief direct connection of the DOS1102S AFG output to `TP_SENSOR` produced a new observation:

- With AFG already connected to R1, CH1 measured approximately **520 mVpp**, mean approximately **-8 mV**, and approximately **176 mV RMS**.
- In the later TP_SENSOR configuration, the measured mean was approximately **+171 mV**.
- The user subsequently confirmed that **ACS724 VOUT and AFG OUT were both connected to TP_SENSOR at the same time**.

Interpretation:

This was **source contention**: two active voltage outputs were connected to one node. ACS724 VOUT was attempting to hold the node near its approximately 0.49 V zero-current output while the AFG was attempting to impose a zero-centered sine. The observed +171 mV mean is therefore not an AFE transfer result.

The earlier tentative suggestion that the AFE itself might be clamping the negative half-cycle is superseded by the confirmed wiring condition above.

Engineering conclusion:

**This measurement is invalid for AFE characterization because two active sources drove TP_SENSOR simultaneously.**

For independent AFE testing, only one active source may drive TP_SENSOR at a time. If the AFG is used, ACS724 VOUT must be disconnected first.


## First 100 Hz AFE stimulus attempts and bias-fixture troubleshooting

### AFG substituted directly for ACS724 at the R1 input

The normal ACS724/TP_SENSOR connection to the input side of R1 was disconnected. The DOS1102S AFG was then used as the only active source driving the R1 input.

AFG setting:

- sine;
- 100 Hz;
- minimum available amplitude setting: 0.5 Vpp.

Observed at the R1 input with CH1:

- \`Vpp ≈ 520 mV\`;
- \`Vrms ≈ 176 mV\`;
- mean ≈ \`-8 to -10 mV\`;
- frequency ≈ 100 Hz.

Interpretation:

The source presented to the AFE is therefore approximately a 0.52 Vpp sine centered close to 0 V. Its approximate extrema are around ±0.26 V. This is not a valid operating-point stimulus for the 0-to-5 V single-supply AFE because the negative half-cycle asks the AFE to process a voltage below \`GND_MEAS\`.

### AFE output under the zero-centered 100 Hz stimulus

With CH1 at the R1 input and CH2 at MCP6022 pin 7 / \`TP_AFE\`, the screen showed a visibly bottom-clipped CH2 waveform.

One photographed capture showed approximately:

- CH1: \`Vpp = 488 mV\`, mean = \`16.79 mV\`, frequency = \`99.80 Hz\`;
- CH2: \`Vpp = 356 mV\`, mean = \`98.40 mV\`;
- CH2 automatic frequency readout = \`150.6 Hz\`.

The CH2 automatic frequency readout is not treated as the excitation frequency because the waveform is strongly non-sinusoidal/clipped. The commanded/source frequency remains approximately 100 Hz.

Engineering interpretation:

This is **not a frequency-response measurement**. It demonstrates that a zero-centered AFG sine is outside the intended single-supply input operating region. The lower part of the requested waveform cannot be reproduced normally, so amplitude/phase from this capture must not be used as filter-transfer evidence.

### Why an external DC bias is required

The DOS1102S AFG used here does not provide a verified usable positive DC-offset control in the user's instrument setup. Therefore the AC sine must be shifted upward externally before being used for AFE characterization.

The intended principle is:

\`\`\`text
zero-centered AFG AC
        |
        | through coupling capacitor
        v
positive DC bias node ----> R1 / AFE input
\`\`\`

A resistor divider establishes the positive DC operating point. The coupling capacitor blocks the AFG's DC level while allowing the changing AC component to be superimposed on that bias.

This changes the signal center without intentionally changing the wanted sine frequency.

### 10 kΩ / 1 kΩ divider diagnostic

A temporary divider was assembled:

\`\`\`text
5V_MEAS -- 10 kΩ --+-- bias node
                   |
                   1 kΩ
                   |
                GND_MEAS
\`\`\`

With an approximately 4.8 V measured supply, the ideal divider prediction is:

\`Vbias = 4.8 × 1k / (10k + 1k) ≈ 0.436 V\`.

Troubleshooting measurements:

- initial bias-node reading with the coupling arrangement connected: approximately **0 V**;
- measured supply side of the 10 kΩ resistor: approximately **4.8 V**;
- in-circuit resistance from bias node/R1 input to GND on the 2 kΩ meter range: approximately **1.5 kΩ**;
- after isolating the AFG/coupling path and powering the divider alone: bias node measured **0.44 V**.

Conclusion:

**The divider itself is working correctly.** The measured 0.44 V agrees closely with the 0.436 V prediction. The earlier collapse toward 0 V occurred only when the coupling arrangement was connected, so that state must not be treated as a valid biased source.

### Coupling-capacitor inventory correction

The user clarified that the available parts are **ten 100 nF capacitors**, not one 10 µF capacitor.

Therefore:

\`10 × 100 nF in parallel = 1000 nF = 1 µF\`.

The previous instruction assuming an available 10 µF coupling capacitor is withdrawn.

For capacitors in parallel, every capacitor must connect across the same two electrical nodes:

\`\`\`text
AFG-side node  --||--  bias-side node
               --||--
               --||--
                 ...
               --||--   (10 × 100 nF)
\`\`\`

Because these 100 nF parts are ceramic/non-polarized, orientation is irrelevant.

### Why 1 µF changes the divider-design requirement

With the present 10 kΩ / 1 kΩ divider, the divider's Thevenin resistance is:

\`Rth = 10k || 1k ≈ 909 Ω\`.

A 1 µF coupling capacitor with roughly this resistance produces a high-pass corner on the order of:

\`fc ≈ 1 / (2π × 909 Ω × 1 µF) ≈ 175 Hz\`

before adding source/output resistance and other loading.

Therefore a 100 Hz test would already be substantially attenuated by the temporary coupling network itself. That would contaminate the AFE measurement.

A higher-resistance divider such as 100 kΩ / 10 kΩ would keep approximately the same ~0.44 V bias while raising the divider resistance by 10×, moving the coupling corner down to roughly 17.5 Hz with 1 µF. This is currently a **design candidate only**; resistor availability and the actual test-network behavior must be verified before implementation.

## Current engineering status

Established:

- Rev-1 AFE DC path: PASS.
- DOS1102S minimum practical sine setting used here: 0.5 Vpp.
- Zero-centered AFG injection produces an invalid/clipped AFE waveform.
- 10 kΩ / 1 kΩ divider alone produces the predicted ~0.44 V bias.
- Available coupling inventory clarified as 10 × 100 nF = 1 µF when wired in parallel.

Not yet established:

- a validated biased 100 Hz source;
- a valid 100 Hz AFE gain/phase point;
- any filter-response measurement.

Next action:

Implement and verify a bias/coupling fixture whose own high-pass corner is well below the 100 Hz baseline, then validate the biased source at the R1 input **before** measuring \`TP_AFE\`.


### Clarification — powered vs unpowered bias reading

The user clarified that the earlier approximately **0.41 V** reading at the R1 input was taken with the **PSU OFF** and must not be treated as the operating bias voltage.

With the same temporary bias network and the **PSU ON**, the R1 input/bias node measured **0.44 V**.

Therefore the valid powered divider result remains:

- supply side approximately 4.8 V;
- bias node approximately 0.44 V;
- agreement with the 10 kΩ / 1 kΩ divider prediction is good.

The unpowered 0.41 V observation is not used for bias validation.
