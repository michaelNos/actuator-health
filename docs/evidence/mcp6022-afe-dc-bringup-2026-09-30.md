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


### AFG-side measurement after installing the 10 × 100 nF coupling bank

With the temporary coupling/bias fixture connected, CH1 was moved to the **AFG side of the capacitor bank** while CH2 remained at MCP6022 pin 7 / TP_AFE.

Photographed CH1 measurements:

- \`Vpp = 520.0 mV\`;
- \`Vrms = 176.4 mV\`;
- mean = \`-9.526 mV\`;
- frequency = \`100.0 Hz\`.

This confirms that the DOS1102S AFG itself is still producing the expected approximately 0.5 Vpp, 100 Hz, zero-centered sine at the source side of the coupling network.

Therefore the previously observed very small AC component at the R1/bias node is **not caused by the AFG failing to generate the sine**. The attenuation/problem lies in the coupling-bank / bias-node implementation or its loading, and must be localized before interpreting the AFE output.

The simultaneous CH2 reading at pin 7 is not treated as AFE transfer evidence at this stage because the actual R1-input AC waveform has not yet been re-established.


### Measurement across the coupling bank

CH1 remained on the AFG side of the capacitor bank and CH2 was moved to the bias-node / R1-input side.

Photographed values:

- CH1: \`Vpp = 520.0 mV\`, mean = \`-9.579 mV\`, \`Vrms = 176.1 mV\`, frequency = \`99.80 Hz\`;
- CH2: \`Vpp = 148.0 mV\`, displayed mean = approximately \`1.100 V\`, displayed RMS = approximately \`1.100 V\`, automatic frequency = \`247.5 Hz\`.

CH2 is not a clean 100 Hz sine, so its automatic frequency readout is not interpreted as the actual excitation frequency.

The approximately 1.10 V CH2 DC level is inconsistent with the previously verified divider-alone bias of 0.44 V. A correctly functioning series coupling capacitor should not intentionally shift the divider's DC operating point from 0.44 V to 1.10 V.

Therefore this capture is **not accepted as coupling-network transfer evidence**. The next diagnostic is to measure the actual DC voltage at the bias-node / R1 input with a multimeter while the AFG/coupling bank is connected and running, to distinguish a real DC-node shift from a scope-node/measurement-placement issue.


### DC multimeter check with AFG and coupling bank connected

With the AFG running at 100 Hz / 0.5 Vpp and the 10 × 100 nF coupling bank connected, the user measured the R1-input / bias node with a multimeter in DC-voltage mode:

- observed DC voltage: approximately **0.57–0.60 V**.

This differs materially from the divider-alone value of **0.44 V**.

For an ideal series coupling capacitor, the divider should establish the DC operating point independently of the AFG's zero-centered DC level. Therefore the observed upward shift indicates that the present coupling/bias implementation or its connected load is altering the DC node.

No AFE transfer conclusion is drawn from this state.

Next diagnostic: isolate the bias/coupling source from the AFE by disconnecting R1 from the bias node, leaving only the divider + capacitor bank + AFG, and remeasure the bias node DC voltage. This distinguishes a source-network problem from loading/nonlinearity in the AFE path.


### Physical bias-node topology clarification

The user clarified the actual breadboard topology. One five-hole breadboard strip forms the complete bias node and contains:

- the lower end of the 10 kΩ resistor, whose other end goes to +5 V;
- the upper end of the 1 kΩ resistor, whose other end goes to GND;
- the R1 input connection;
- one side of the 10 × 100 nF capacitor bank;
- scope CH2 probe tip.

The opposite side of the capacitor bank connects to AFG OUT.

Therefore R1 is only one branch from the common bias node. Disconnecting R1 alone does **not** remove the 10 kΩ / 1 kΩ divider from the bias node and should not, by itself, collapse the divider node to 0 V.

The earlier interpretation that the bias node might have been physically created through the R1 connection is withdrawn. A reported 0 V reading after disconnecting R1 must instead be treated as a node-identification/measurement-placement discrepancy until repeated at the actual common five-hole strip.


### Divider-node diagnostic with R1 disconnected

With R1 disconnected while the divider/coupling-side node remained otherwise identified as the common five-hole bias strip, the user measured approximately **4.54 V DC** from that node to GND.

This is incompatible with the intended divider values/connection:

- 10 kΩ from +5 V to the node;
- 1 kΩ from the node to GND.

With a ~4.8–4.9 V supply, that intended divider should produce only about 0.44 V.

A node near 4.5 V instead indicates that the effective divider ratio is strongly weighted toward +5 V. Possible causes include swapped resistor values/positions, a wrong resistor value, or a missing/high-resistance ground-side path.

Next diagnostic: power off and verify the two divider resistors individually, preferably with one leg of each isolated from the common node, before reconnecting the AFG/coupling network.


### Correction — 4.54 V divider-node reading taken in different power state

The user clarified that the approximately **4.54 V** reading was taken while the bench PSU was OFF. The Arduino/UNO power path may still have been energizing part of the measurement domain.

After restoring the normal PSU connection, the measured 5 V rail was approximately **4.85 V**.

Therefore the earlier 4.54 V reading must **not** be used to diagnose the 10 kΩ / 1 kΩ divider as swapped or faulty. That interpretation is withdrawn.

The valid divider-alone operating-point measurement remains approximately **0.44 V** at the bias node with the intended supply state active.

All subsequent bias/coupling measurements must keep the power-source configuration unchanged and explicitly record that state.


### Bias/coupling network test with R1 disconnected

With R1 disconnected from the temporary source fixture, CH1 measured the AFG side of the capacitor bank and CH2 measured the common bias node.

Photographed measurements:

- CH1: \`Vpp = 528.0 mV\`, mean = \`-8.887 mV\`, \`Vrms = 175.9 mV\`, frequency = \`100.0 Hz\`;
- CH2: \`Vpp = 76.0 mV\`, mean = approximately \`468.6 mV\`, RMS = approximately \`468.6 mV\`;
- CH2 automatic frequency: no valid reading.

Interpretation:

The DC bias is present at the bias node, consistent with the independently measured divider operating point near 0.44 V. However, CH2 does not show a clear coherent 100 Hz sine; the visible variation is dominated by noise/spikes and the automatic frequency detector cannot lock.

Therefore the 76 mV raw Vpp must not be interpreted as the actual transmitted 100 Hz sine amplitude.

This result establishes:

- AFG source side is valid at ~0.53 Vpp / 100 Hz;
- DC bias node is valid;
- the AC path through the capacitor bank has **not yet been validated**.

Next diagnostic: without changing wiring, raise the AFG frequency to 1 kHz while keeping 0.5 Vpp. A correctly connected AC-coupling bank should pass a much larger, clearly sinusoidal signal at the bias node because the capacitor reactance is ten times lower at 1 kHz than at 100 Hz. If CH2 remains essentially flat/noisy, the bank connection itself is suspect.


### 1 kHz coupling-network check

With R1 disconnected, AFG at 1 kHz and 0.5 Vpp, CH1 remained on the AFG side of the temporary capacitor bank and CH2 on the bias-node side.

Observed from the scope image:

- CH1: about 524 mVpp, 176.2 mV RMS, mean about -6.6 mV, frequency 1.000 kHz.
- CH2: about 48 mVpp, DC level about 0.412 V, no stable frequency reading.

Interpretation: the AFG source and DC bias are present, but a clear 1 kHz sine is not reaching the bias node. For an intended 1 uF coupling bank and the 10 kOhm / 1 kOhm divider, 1 kHz should pass with little attenuation. The next diagnostic is therefore the capacitor-bank breadboard interconnection itself. No AFE transfer result is accepted from this state.


### Root cause found: AFG was not connected to the capacitor-bank input bus

Continuity testing showed that AFG OUT was not electrically connected to the intended AFG-side bus of the 10 x 100 nF capacitor bank. This explains the earlier observation that the AFG itself was producing the correct sine while almost no coherent AC appeared at the bias node.

After correcting that missing connection, the bias-node waveform became clearly periodic at approximately 1 kHz. In the first post-fix scope image, CH2 at the bias node showed approximately 998.6 Hz and a DC level near 472.5 mV, confirming that the AC-coupling path is now active while the positive DC bias remains present.

The simultaneous CH1 reading in that image was approximately 4.93 V DC, indicating CH1 was no longer probing the AFG-side signal node. Therefore no amplitude-transfer ratio is calculated from this image. The next measurement must put CH1 back on the AFG-side capacitor-bank bus and keep CH2 on the bias node.


### 1 kHz source/bias check after reconnecting the capacitor-bank input

Scope image observations with R1 disconnected:

- CH1 at the AFG-side bus: 544 mVpp, 177.5 mV RMS, mean -7.842 mV, 1.000 kHz.
- CH2 at the bias node: mean 480.2 mV, raw Vpp 84 mV, no stable frequency indication.

The source and DC bias are present, but the bias node still does not show a clear 1 kHz sine. The next diagnostic is to verify the actual value code printed on the ceramic capacitors.


### Capacitor value confirmed

The installed ceramic capacitors are marked `104`, which denotes 100 nF each. With ten such capacitors wired in parallel, the intended nominal total is therefore 1.0 uF. The capacitor value itself is therefore consistent with the intended temporary coupling network. Since the AFG source is valid but the bias node still does not show a clear 1 kHz sine, the remaining diagnostic focus is the external interconnection between the capacitor-bank output bus, the bias node, and common ground.


### Isolated capacitor-bank validation — PASS

The temporary coupling bank was isolated from the bias divider and AFE. A 1 kOhm resistor was connected from the bank output to GND_MEAS. The AFG drove the bank input at 1 kHz / 0.5 Vpp.

Scope image observations:

- CH1 / AFG side: 496 mVpp, 1.000 kHz, mean about -7.605 mV, RMS 169.6 mV.
- CH2 / bank output into 1 kOhm: 488 mVpp, 1.000 kHz, mean about 0.305 mV, RMS 166.2 mV.

Amplitude ratio:

`488 / 496 ≈ 0.984`

Thus the isolated coupling bank transfers about 98.4% of the 1 kHz amplitude into a 1 kOhm load. This is consistent with the intended nominal total capacitance of approximately 1 uF and confirms that the 10 x 100 nF capacitor bank itself is functioning correctly.

Engineering conclusion: **capacitor-bank isolation gate PASS.** The earlier loss of the 1 kHz signal occurred elsewhere in the bias-network / node implementation or measurement placement, not inside the capacitor bank itself.


### Biased source validation at 1 kHz

With R1 disconnected, CH1 measured the AFG side and CH2 the biased node. Observed: CH1 496 mVpp at 1.000 kHz; CH2 480 mVpp at 1.000 kHz; CH2 mean about 414.2 mV. The amplitude ratio is 480/496 = 0.968. Both traces are clean sinusoids. Result: temporary biased-source gate PASS at 1 kHz. This is a source-fixture result, not yet an AFE transfer measurement.


### Biased source with R1 reconnected — PASS

With R1 reconnected to the validated temporary biased source, CH1 remained on the AFG-side bus and CH2 measured the bias node / R1 input.

Observed from the scope image:

- CH1: 496 mVpp, 1.001 kHz, mean about -7.879 mV.
- CH2: 500 mVpp, 1.000 kHz, mean about 428.5 mV.

The biased source remains clean and essentially unchanged when loaded by the AFE input through R1. Therefore the temporary source is now validated under the actual R1-connected condition.

The previous approximately 4.608 V CH2 reading is superseded by this verified bias-node measurement and is not used as the operating-point value.


### First valid AFE AC transfer point — 1 kHz

After validating the temporary biased source, CH1 was moved to the actual R1 input / bias node and CH2 remained at MCP6022 pin 7 / TP_AFE. The AFG was 1 kHz, 0.5 Vpp.

Observed from the scope image:

- CH1 / R1 input: 480 mVpp, 1.000 kHz, mean about 415.3 mV.
- CH2 / TP_AFE: 480 mVpp, 1.000 kHz, mean about 431.8 mV.

Measured magnitude ratio from displayed Vpp values:

`|H(1 kHz)| = 480 / 480 = 1.000`, corresponding to approximately 0 dB.

Both waveforms are visibly sinusoidal and unclipped. This is the first valid low-frequency AC transfer point through the complete Rev-1 AFE path. The screenshot does not provide a quantified phase measurement, so no numerical phase value is accepted from this capture.

Engineering result: **1 kHz AFE magnitude gate PASS**.


### 5 kHz AFE check — not accepted

With CH1 at the actual R1 input and CH2 at MCP6022 pin 7 / TP_AFE, the AFG frequency was changed to 5 kHz with all other conditions unchanged.

Observed from the scope image:

- CH1: 504 mVpp, 5.000 kHz, mean about 414.2 mV.
- CH2: 380 mVpp, 5.000 kHz, mean about 434.2 mV.

Measured magnitude ratio:

`380 / 504 ≈ 0.754`, equivalent to about `-2.45 dB`.

For the present implementation, using 10 kOhm in the low-Q section while retaining the intended capacitor values and high-Q stage, the predicted complete AFE magnitude at 5 kHz remains approximately unity (about 0.999, roughly -0.01 dB). Therefore the observed -2.45 dB is not accepted as valid designed behavior.

Next diagnostic: keep CH1 at the R1 input and move CH2 from pin 7 to MCP6022 pin 1 / OUTA to measure the low-Q stage alone. This will localize whether the excessive attenuation appears already in stage A or is introduced in the high-Q stage.


### 5 kHz low-Q stage isolation — excessive attenuation already present in stage A

Diagnostic configuration:

- AFG: 5 kHz, 0.5 Vpp.
- CH1: actual biased R1 input.
- CH2: MCP6022 pin 1 / OUTA.
- Grounds unchanged.

Observed from the scope image:

- CH1: 512 mVpp, 5.000 kHz.
- CH2: 420 mVpp, 5.000 kHz.
- CH2 mean: about 436.7 mV.

Measured low-Q stage magnitude ratio:

`420 / 512 ≈ 0.820`

which corresponds to approximately:

`20*log10(0.820) ≈ -1.72 dB`.

For the physical low-Q implementation with R1 = R2 = 10 kOhm and the intended 1.2 nF / 1.0 nF capacitors, the predicted 5 kHz magnitude is approximately 0.924 (about -0.69 dB).

Therefore the observed attenuation is materially larger than predicted. The excessive 5 kHz attenuation is already present in the first low-Q stage, so the next diagnostic should isolate whether the MCP6022 follower itself is reproducing N2A correctly or whether the error lies in the passive Sallen-Key network/component values/wiring.


### Pin-3 diagnostic capture invalid because stimulus disappeared

For the intended next diagnostic, CH1 was to remain on the biased R1 input and CH2 was moved to MCP6022 pin 3 / N2A while the AFG should remain at 5 kHz, 0.5 Vpp.

The submitted scope capture did not contain the expected 5 kHz stimulus:

- CH1: about 33.6 mVpp, mean about 476.7 mV, auto-frequency about 220.8 Hz.
- CH2: about 110 mVpp, mean about 30.8 mV, auto-frequency about 1.974 kHz.

Neither waveform is a clean 5 kHz sine, so this capture is not used to characterize N2A or the op-amp follower.

Next action: without moving either probe, verify that the AFG output remains ON at 5.000 kHz and 0.500 Vpp, then repeat the screen capture.


### Correction to invalid pin-3 capture

The operator confirmed that the AFG was physically disconnected during the prior pin-3 diagnostic capture. Therefore the disappearance of the 5 kHz stimulus was caused by the disconnected source, not by the AFE.

That capture remains invalid for transfer characterization, but it must not be interpreted as evidence of an AFE fault.

After reconnecting the AFG, the source waveform visibly returned. The next controlled diagnostic is to place CH1 back on the biased R1 input while keeping CH2 on MCP6022 pin 3 / N2A, with the AFG at 5 kHz and 0.5 Vpp.


### Correction: post-reconnect screenshot already used R1-input / pin-3 probe placement

The operator clarified that the latest screenshot after reconnecting the AFG already used the intended diagnostic configuration:

- CH1 on the biased R1 input.
- CH2 on MCP6022 pin 3 / N2A.
- AFG at 5 kHz, 0.5 Vpp, output ON.

The screenshot is too blurred to extract trustworthy numerical scope readouts, so no numeric Vpp values are accepted from it. Qualitatively, however, CH1 clearly contains the strong periodic 5 kHz stimulus while CH2 at N2A does not show a comparable clean sine.

This localizes the excessive attenuation upstream of the op-amp follower, within the passive low-Q Sallen-Key input network / its wiring, rather than at the MCP6022 voltage-follower action itself.

Next diagnostic: keep CH1 at the R1 input and move CH2 from N2A to N1A, the node between R1 and R2. This determines whether the signal is already lost across R1 or later across the R2/N2A portion of the network.


### N1A diagnostic capture — invalid because input DC bias is absent

Intended configuration:

- CH1: biased R1 input.
- CH2: N1A, the node between R1 and R2.
- AFG: 5.000 kHz, 0.500 Vpp.

Observed from the scope image:

- CH1: 512 mVpp, 5.000 kHz, mean about -6.14 mV.
- CH2: 440 mVpp, 5.000 kHz, mean about -9.01 mV.

Although the raw AC ratio is `440/512 ≈ 0.859`, this capture is not accepted as a valid low-Q-node transfer result because the intended external DC bias is absent. Earlier valid biased-input captures showed the R1 input mean near 0.42 V; here CH1 is centered near 0 V.

With the MCP6022 operating from a single positive supply, a zero-centered ~0.5 Vpp stimulus drives part of the waveform below ground and invalidates the intended linear AFE test condition.

Next action: do not change the filter wiring. Verify the DC voltage of the physical bias node / R1 input relative to GND_MEAS with a multimeter while the PSU and AFG are connected as intended. Expected value is approximately 0.4-0.45 V.


### Valid 5 kHz N1A localization after restoring PSU power

The operator confirmed that the PSU had mistakenly been OFF during the previous zero-bias capture. With the PSU restored, the intended external bias returned.

Diagnostic configuration:

- CH1: biased R1 input.
- CH2: N1A, the node between R1 and R2.
- AFG: 5.000 kHz, 0.500 Vpp.
- PSU ON.

Observed from the scope image:

- CH1: 512 mVpp, 5.000 kHz, mean about 472.0 mV.
- CH2: 512 mVpp, 5.000 kHz, mean about 467.7 mV.

Measured ratio across the R1 input-to-N1A interval:

`512 / 512 = 1.000`

Within the scope's displayed amplitude resolution, there is no measurable 5 kHz amplitude loss across R1. Therefore the excessive attenuation previously seen at OUTA is not introduced across R1.

Next localization step: keep CH1 at the biased R1 input and move CH2 from N1A to N2A / MCP6022 pin 3. This isolates the R2 / N2A portion of the low-Q network under a valid biased operating condition.


### 5 kHz N2A localization — node pulled near ground

Configuration:

- CH1: biased R1 input.
- CH2: N2A / MCP6022 pin 3.
- AFG: 5.000 kHz, 0.500 Vpp.
- PSU ON.

Observed from the scope image:

- CH1: 504 mVpp, 5.000 kHz, mean about 463.9 mV.
- CH2: 64.0 mVpp, mean about 16.84 mV; automatic frequency did not lock.

This is not accepted as normal low-pass behavior. The preceding N1A measurement was approximately 512 mVpp with mean about 467.7 mV, so the signal and DC bias are healthy through R1. At N2A, however, both the AC amplitude and especially the DC bias collapse close to ground.

In the intended topology, the N2A-to-GND capacitor is 1.0 nF. At DC it should act effectively open, so N2A should remain close to the input bias voltage through R1/R2. A mean near 16.8 mV therefore indicates an unintended DC path to ground, wrong physical node, wrong component/wiring, or similar fault around N2A.

Next diagnostic: with power OFF, check continuity between N2A / MCP6022 pin 3 and GND_MEAS before changing any wiring.


### Power-off N2A-to-ground continuity check

With PSU power OFF, continuity between N2A / MCP6022 pin 3 and GND_MEAS produced a beep.

A continuity beep alone is not yet accepted as proof of a hard short because the meter can respond transiently while capacitive or semiconductor paths charge. The next diagnostic is therefore a direct resistance measurement from N2A to GND_MEAS, held long enough for the reading to settle.

For the intended topology, the N2A-to-ground capacitor is only 1.0 nF and should not provide a steady DC low-resistance path. A settled low resistance would indicate an unintended DC path or wiring/component fault; a reading that rises toward high resistance / OL would instead indicate a transient continuity response.


### Critical correction: recent intended pin-3 measurements were actually taken on pin 4 / GND

The operator identified a probe-placement error: the recent measurements described as MCP6022 pin 3 / N2A were physically taken on MCP6022 pin 4, which is VSS / GND.

Therefore the following observations and interpretations are invalid and must not be used for engineering conclusions:

- the apparent loss of the 5 kHz signal at "pin 3 / N2A";
- the approximately 64 mVpp / approximately 16.8 mV mean capture attributed to N2A;
- the inferred conclusion that N2A was being pulled toward ground;
- the inferred localization of a passive low-Q network fault between N1A and N2A;
- the continuity-beep observation attributed to N2A-to-GND, because the probe was actually on pin 4 / GND and a beep is therefore expected.

These measurements are retained only as traceability of the probe-placement mistake.

The valid 5 kHz evidence established before this mistake remains:

- R1 input: approximately 512 mVpp.
- N1A: approximately 512 mVpp with the PSU ON and normal bias restored.
- OUTA / pin 1: approximately 420 mVpp.

The correct next diagnostic is to measure MCP6022 pin 3 / N2A physically, using the verified DIP orientation:

- pin 4 = VSS / GND, bottom-left;
- pin 3 = +IN A, immediately above pin 4 on the left side.

No further fault conclusion is accepted until the true pin-3 measurement is repeated.


### Correct 5 kHz pin-3 / N2A measurement

After correcting the earlier probe-placement mistake, CH2 was placed on the actual MCP6022 pin 3 / N2A.

Configuration:

- CH1: biased R1 input.
- CH2: MCP6022 pin 3 / N2A.
- AFG: 5.000 kHz, 0.500 Vpp.
- PSU ON.

Observed from the scope image:

- CH1: 496 mVpp, 5.000 kHz, mean about 473.4 mV.
- CH2: 376 mVpp, 5.000 kHz, mean about 446.6 mV.

Measured ratio:

`376 / 496 ≈ 0.758`

which corresponds to approximately:

`20*log10(0.758) ≈ -2.41 dB`.

This confirms that substantial attenuation is already present at N2A. However, a direct simultaneous N2A-versus-OUTA comparison is still required before deciding whether the MCP6022 follower is behaving correctly or whether the discrepancy lies exclusively in the passive Sallen-Key network.

Next diagnostic: keep CH2 on pin 3 / N2A and move CH1 from the R1 input to pin 1 / OUTA. At 5 kHz the follower should reproduce the pin-3 waveform essentially 1:1.


### 5 kHz direct N2A-to-OUTA follower check — PASS

Configuration:

- CH2: MCP6022 pin 3 / N2A.
- CH1: MCP6022 pin 1 / OUTA.
- AFG: 5.000 kHz, 0.500 Vpp.
- PSU ON.

Observed from the scope image:

- CH1 / OUTA: 440 mVpp, 5.000 kHz, mean about 459.5 mV.
- CH2 / N2A: 432 mVpp, 5.000 kHz, mean about 447.6 mV.

Measured follower ratio:

`440 / 432 ≈ 1.019`.

Within the oscilloscope's displayed amplitude resolution, OUTA reproduces the N2A waveform closely. Therefore the MCP6022 channel-A voltage follower is not the primary cause of the excessive 5 kHz attenuation.

The remaining discrepancy is upstream in the passive low-Q network and/or its implemented component values/wiring.

Next diagnostic: keep CH2 on N2A / pin 3 and move CH1 from OUTA / pin 1 to N1A. This gives a simultaneous N1A-to-N2A ratio across the R2/C2 portion of the stage. For R2 = 10 kOhm and C2 = 1.0 nF at 5 kHz, the ideal ratio |N1A/N2A| is approximately sqrt(1 + (2*pi*f*R2*C2)^2) ≈ 1.048.


### 5 kHz simultaneous N1A-to-N2A check

Configuration:

- CH1: N1A.
- CH2: N2A / MCP6022 pin 3.
- AFG: 5.000 kHz, 0.500 Vpp.
- PSU ON.

Observed from the scope image:

- CH1 / N1A: 448 mVpp, 5.000 kHz, mean about 462.4 mV.
- CH2 / N2A: 392 mVpp, 5.000 kHz, mean about 438.8 mV.

Measured ratio:

`N2A/N1A = 392/448 ≈ 0.875`.

For the intended R2 = 10 kOhm and C2 = 1.0 nF, the ideal relation at N2A is

`|N2A/N1A| = 1/sqrt(1 + (2*pi*f*R2*C2)^2)`

which at 5 kHz gives approximately 0.954.

Therefore the measured 0.875 is materially lower than expected. The discrepancy is now localized to the R2/C2 portion of the low-Q stage or its implemented component values/wiring.

Next diagnostic: with power OFF, measure the resistance directly across R2. The intended value is 10 kOhm.


### R2 resistance check

With PSU power OFF, R2 was measured directly as approximately 9.76 kOhm.

This matches the original schematic value of 9.76 kOhm and rules out an incorrect R2 resistance as the cause of the excessive N1A-to-N2A attenuation.

This measurement also corrects the earlier working assumption that the physical low-Q R2 was 10 kOhm: the measured physical value is 9.76 kOhm.

Next diagnostic: verify the actual C2 value/marking for the capacitor from N2A to GND_MEAS. The intended value is 1.0 nF.


### C2 marking check

The capacitor connected as C2 in the low-Q N2A-to-ground position is marked `102`, corresponding to a nominal capacitance of 1.0 nF.

With measured R2 = 9.76 kOhm and nominal C2 = 1.0 nF, the expected 5 kHz N2A/N1A magnitude is approximately 0.956. The measured ratio was approximately 0.875.

If interpreted as a simple R2-C2 relation, the measured ratio corresponds to an effective capacitance of roughly 1.8 nF. This does not prove that C2 itself is 1.8 nF; unintended parallel capacitance or wiring around N2A can produce the same effect.

Next diagnostic: power OFF and verify C2 wiring by continuity: one C2 lead must connect to N2A / pin 3, and the other C2 lead must connect to GND_MEAS.


### Bias fixture continuity check 1 — PASS

With PSU power OFF, the operator verified that all four intended BIAS_NODE points have continuity with each other:

- bottom of the 10 kOhm divider resistor;
- top of the 1 kOhm divider resistor;
- output side of the 10 x 100 nF coupling-capacitor bank;
- AFE R1 input.

This confirms that the physical breadboard implements the common BIAS_NODE connection shown in the dedicated temporary fixture schematic.

Next check: verify continuity from the top of the 10 kOhm resistor to 5V_MEAS.


### Bias-fixture verification found missing 10 kOhm-to-BIAS_NODE connection

With PSU power OFF, continuity checks against the dedicated temporary bias-fixture schematic showed:

- 5V_MEAS to one physical end of the 10 kOhm resistor: continuity present.
- the opposite physical end of the 10 kOhm resistor to BIAS_NODE: no continuity.

Therefore the temporary bias divider is not physically wired as documented. The required topology is:

`5V_MEAS -> 10 kOhm -> BIAS_NODE -> 1 kOhm -> GND_MEAS`.

This is a confirmed wiring discrepancy in the temporary test fixture. No further AFE frequency-response conclusions should be drawn until the bias-side end of the 10 kOhm resistor is connected to BIAS_NODE and the divider is revalidated.


### Correction: 10 kOhm continuity interpretation was premature

The previous entry incorrectly treated a no-beep result involving the 10 kOhm divider resistor as proof that the resistor was disconnected from BIAS_NODE.

That conclusion is withdrawn.

A continuity tester commonly does not beep through a 10 kOhm resistor, so a measurement path that includes the resistor can legitimately produce no beep even when the divider is wired correctly.

The correct verification is node-to-lead continuity:

- directly probe the physical 5V-side resistor lead to the 5V_MEAS node;
- directly probe the physical BIAS-side resistor lead to the BIAS_NODE row.

Those checks should test only the wiring connection on each side and must not include the 10 kOhm resistance itself.

No physical rewiring is authorized from the previous no-beep result alone.
