# Dynamic Measurement Lessons: MCP6022 Fixture, Sampling, FILTER, Phase, Feedthrough, and SNR

Actuator Health Monitoring System — study note, 2026-09-28.

This note collects the learning from the corrected ACS724 dynamic-characterization campaign. It is educational support material. The authoritative engineering result is recorded in:

- [ACS724 post-fix dynamic characterization and AFE handoff](../docs/evidence/acs724-postfix-dynamic-characterization-and-afe-handoff-2026-09-28.md)

The study goal is to understand **why** each measurement was performed, what the equations mean physically, how the oscilloscope data are interpreted, and why the project now moves from raw-sensor testing to Analog Front End bring-up.

---

## 1. MCP6022 package numbering: the mistake that changed the diagnosis

For a PDIP-8 package viewed from the top with the notch at the top:

```text
             notch / pin-1 marker
                    ↓
              ┌─────────┐
      OUT A  1│         │8  VDD
      -IN A  2│         │7  OUT B
      +IN A  3│         │6  -IN B
        VSS  4│         │5  +IN B
              └─────────┘
```

The numbering is counter-clockwise.

That means:

- left side top → bottom: 1, 2, 3, 4;
- right side top → bottom: **8, 7, 6, 5**.

A very common mistake is to imagine the right side as 5, 6, 7, 8 from top to bottom. That is wrong.

### Why the earlier supply test appeared to work

The top-right physical leg was being called “pin 5”, but physically it was the real pin 8. Therefore putting +5 V on that physical leg actually powered the MCP6022 correctly even though the spoken pin number was wrong.

This explains why the circuit could appear partly functional while later diagnostic statements about “pin 5” or “pin 7” became contradictory.

### General lesson

For IC troubleshooting, do not say only “pin 5”.

Say:

> **bottom-right physical leg, actual MCP6022 pin 5 (+IN B)**

until orientation is fully established.

Package orientation is part of the measurement definition.

---

## 2. What the two MCP6022 amplifiers do in this fixture

The MCP6022 contains two independent op-amps, A and B, sharing one power supply.

### Channel B — reference buffer

Channel B is wired as a voltage follower:

- pin 5 receives `VREF_RAW`;
- pin 6 is connected to pin 7;
- pin 7 is the output `VREF_BUF`.

Negative feedback makes:

`V7 ≈ V5`

while the output can supply more current than the high-resistance divider should be asked to supply.

The raw divider is approximately 1.25 V ideally. A multimeter can load a high-resistance divider, so a direct reading near 1.15 V does not automatically mean the divider ratio is wrong.

### Channel A — biased inverting driver

Channel A has:

- pin 3 at `VREF_BUF`;
- AFG input through `RIN` to pin 2;
- feedback `RF` from pin 1 to pin 2.

For an ideal op-amp in negative feedback:

`V2 ≈ V3 = VREF`

Apply Kirchhoff's current law at pin 2:

`(VAFG - VREF)/RIN + (VOUT - VREF)/RF ≈ 0`

Rearrange:

`VOUT ≈ (1 + RF/RIN)VREF - (RF/RIN)VAFG`

For `RF = RIN`:

`VOUT ≈ 2VREF - VAFG`

So if the AFG produces a ±1 V sine around 0 V and VREF is about 1.25 V:

`VOUT ≈ 2.5 V - VAFG`

which swings approximately 1.5–3.5 V.

The minus sign means the waveform is inverted around the bias level. The important project function is that the resulting current remains positive so the unidirectional ACS724-05AU can be exercised without reverse current.

---

## 3. Why the op-amp output did not “double” before feedback existed

A non-inverting input voltage does not automatically appear doubled at the output.

The factor of two came from the **closed-loop resistor network**:

`1 + RF/RIN`

When the resistor feedback network is absent, that gain relation is not established.

This is a general op-amp lesson:

> Gain is created by the surrounding feedback network, not by the pin number or by the op-amp alone.

---

## 4. Supply bypass versus bulk capacitance

The 100 nF capacitor placed directly between MCP6022 VDD and VSS is a **decoupling/bypass capacitor**.

The IC draws current that changes quickly as its output moves. Breadboard wires and supply leads have nonzero resistance and inductance. The local 100 nF capacitor can provide or absorb a small, fast current locally so the supply pins see a more stable voltage.

A larger capacitor or several 100 nF capacitors in parallel can provide more local stored charge for slower changes.

The roles are complementary:

- **100 nF close to the IC:** fast/high-frequency supply disturbances;
- **bulk capacitance:** slower/larger supply variations.

Capacitors in parallel add:

`C_total = C1 + C2 + ...`

so ten 100 nF capacitors give nominally:

`10 × 100 nF = 1 µF`

The local 100 nF should still remain even if bulk capacitance is added.

---

## 5. Never use continuity/resistance mode on a powered circuit

A multimeter in continuity or resistance mode injects its own test current or voltage.

If the circuit is externally powered at the same time:

- the meter reading is not a valid resistance measurement;
- external voltage can confuse the meter;
- the measurement can stress the instrument or circuit.

Therefore:

> continuity/resistance checks → PSU OFF

Voltage mode is used when the circuit is powered.

---

## 6. What `M: 2 ms` means on this oscilloscope

The DOS1102S screen shows a horizontal timebase such as:

`M: 2 ms`

This means approximately **2 ms per horizontal division**.

For the current project configuration with record depth fixed at 10K, exported CSVs have empirically shown:

- `M: 20 ms/div` → Δt ≈ 40 µs → 25 kSa/s → 400 ms stored record;
- `M: 2 ms/div` → Δt ≈ 4 µs → 250 kSa/s → 40 ms stored record.

The operator does not directly set “250 kSa/s” in our bench workflow. We set the actual available screen control, then verify the CSV.

### Meaning of kSa/s

`kSa/s` means **kilo-samples per second**.

`250 kSa/s = 250,000 samples each second`

If:

`fs = 250,000 samples/s`

then:

`Δt = 1/fs = 4 µs`

The sample interval is the time between neighboring stored voltage measurements.

---

## 7. Samples per cycle

For signal frequency `f_signal`:

`T_signal = 1/f_signal`

If the sample interval is `Δt`:

`samples/cycle = T_signal/Δt = fs/f_signal`

Examples from this project:

### 1 kHz at 25 kSa/s

`25000 / 1000 = 25 samples/cycle`

### 5 kHz at 250 kSa/s

`250000 / 5000 = 50 samples/cycle`

### 7.5 kHz at 250 kSa/s

`250000 / 7500 ≈ 33.3 samples/cycle`

### 10 kHz at 250 kSa/s

`250000 / 10000 = 25 samples/cycle`

Nyquist requires only more than two samples per cycle for an ideal band-limited signal, but that is a theoretical boundary, not a good practical target for accurate waveform and phase work.

For this project, around 25 samples/cycle is a useful working minimum for quantitative phase/amplitude work.

---

## 8. Why raw Vpp is not the same as the wanted sine amplitude

Raw peak-to-peak is:

`Vpp_raw = Vmax - Vmin`

If noise spikes or harmonics are present, they change Vmax and Vmin.

Suppose the wanted 5 kHz sine is only 5.5 mVpp but random/structured variation occasionally adds ±20 mV. Raw Vpp can become tens of millivolts even though the coherent 5 kHz component is still only about 5.5 mVpp.

That is why the project fits the target frequency explicitly.

---

## 9. Coherent sine fitting

At a known test frequency `f`, model the waveform as:

`v(t) = VDC + A sin(2πft) + B cos(2πft)`

Why both sine and cosine?

Because a sine with arbitrary phase can always be represented by a weighted sum of sine and cosine at the same frequency.

The target-frequency peak amplitude is:

`Vpk = sqrt(A² + B²)`

Peak-to-peak:

`Vpp = 2sqrt(A² + B²)`

Phase:

`φ = atan2(B, A)`

This is closely related to calculating one Fourier/DFT component.

The AFG still generates only one sine waveform. Sine and cosine are analysis coordinates.

---

## 10. Current from CH1

CH1 is measured across the 67 Ω reference resistor.

Ohm's law:

`I(t) = V_R8(t)/67 Ω`

For the coherent peak-to-peak component:

`Ipp = VCH1,pp/67 Ω`

Example:

`VCH1,pp = 0.469 V`

then:

`Ipp = 0.469/67 ≈ 0.0070 A = 7.0 mApp`

The reference resistor therefore converts the primary current waveform into a voltage waveform that the scope can measure.

---

## 11. Apparent transfer

The experimental transfer at one frequency is:

`H(f) = VOUT(f) / Iprimary(f)`

The unit is:

`V/A`

It is called **apparent transfer** during characterization because the complete experiment contributes:

- ACS724 magnetic/current conversion;
- ACS724 internal signal dynamics;
- FILTER network;
- measurement noise;
- scope channel timing;
- probe/acquisition effects;
- fitting uncertainty.

Only after controls isolate these effects can the result be treated as intrinsic sensor behavior.

---

## 12. Residual is not CH2 minus CH1

CH1 and CH2 have different physical meanings and different units after conversion:

- CH1 represents primary current through R8;
- CH2 is sensor output voltage.

The residual for CH2 is:

`residual_CH2(t) = measured_CH2(t) - fitted_CH2_model(t)`

where the fitted model contains DC plus the target-frequency sine.

The residual can include:

- random noise;
- harmonics;
- interference;
- drift;
- quantization;
- spectral lines not included in the model;
- model mismatch.

Calling it simply “sensor noise” would overstate what is known.

---

## 13. Why harmonics are not automatically noise

At the 1 kHz test, CH1 showed a substantial third harmonic.

Across the ten corrected 1 kHz records:

- mean 1 kHz fundamental ≈ 455.2 mVpp;
- mean 3 kHz component ≈ 43.9 mVpp.

A harmonic is deterministic periodic content at an integer multiple of the fundamental.

Possible causes include:

- nonlinear source/driver behavior;
- clipping;
- asymmetry;
- sensor or circuit nonlinearity.

For calculating `H(1 kHz)`, the 1 kHz component is the wanted reference. The 3 kHz component is not added into the 1 kHz gain, but it should not be dismissed as random noise.

---

## 14. Same-node phase control

Phase between two different nodes can include both real circuit phase and measurement-system skew.

To discover the measurement skew, put both probes on the **same physical node**.

True circuit phase difference should then be approximately 0°.

### 10 kHz result

Both probes on R8:

- raw CH2−CH1 phase ≈ -13.92°;
- sample interval = 4 µs.

One sample at 10 kHz corresponds to:

`360° × 10000 × 4e-6 = 14.4°`

After shifting CH2 forward by one stored sample:

`-13.92° + 14.4° ≈ +0.48°`

### 1 kHz result

- raw phase ≈ -14.79°;
- sample interval = 40 µs.

Again:

`360° × 1000 × 40e-6 = 14.4°`

After one-sample correction:

`-14.79° + 14.4° ≈ -0.39°`

The same-node controls therefore show that the exported CH2 waveform is approximately one stored sample behind CH1.

### What we do not know

We do not know whether the cause is:

- ADC sequencing;
- analog channel path delay;
- digital pipeline;
- memory alignment;
- CSV export alignment;
- firmware.

Do not invent the cause.

The accepted fact is only the measured alignment behavior.

---

## 15. Why one sample corresponds to different phase at different frequencies

A fixed time delay `Δt` gives phase:

`φ = -360° f Δt`

With Δt = 4 µs:

- 5 kHz → 7.2°;
- 7.5 kHz → 10.8°;
- 10 kHz → 14.4°.

The time shift is unchanged, but a high-frequency cycle is shorter. The same 4 µs therefore occupies a larger fraction of the cycle.

This is also why pure propagation delay produces phase that becomes increasingly negative with frequency.

---

## 16. Why open-primary feedthrough testing matters

Suppose CH2 contains a 5 kHz sine while the AFG is driving the MCP6022.

There are at least two hypotheses:

1. ACS724 is responding to actual primary current;
2. AFG/MCP6022 signal is coupling electrically into the sensor output without primary current.

To test hypothesis 2, open the primary-current path while leaving the AFG, MCP6022, ACS724 power, and FILTER operating.

If the coherent CH2 component remains large, coupling is a concern.

If it collapses, the current-on signal is much more likely to be current dependent.

### Results

At 5 kHz open-primary:

- CH1 driver ≈ 1.982 Vpp;
- CH2 target component ≈ 0.013 mVpp.

At 10 kHz open-primary:

- CH1 driver ≈ 1.895 Vpp;
- CH2 target component ≈ 0.073 mVpp.

The current-on CH2 component is around several millivolts peak-to-peak.

Therefore direct generator/fixture feedthrough is far too small to explain the current-on coherent response.

---

## 17. Why the scope's automatic frequency display can be wrong

A scope's frequency counter or automatic measurement has to decide which crossings or waveform feature represent one period.

If the waveform is distorted, noisy, contains strong harmonics, or has unusual shape, the automatic algorithm can lock onto a harmonic or subharmonic.

This happened in the 10 kHz work: the scope header could report approximately 5 kHz while direct spectral analysis of the stored CH1 waveform clearly showed 10 kHz as the dominant component.

General lesson:

> Instrument automatic measurements are useful, but the stored waveform is the evidence. Cross-check surprising readouts against the waveform/spectrum.

---

## 18. FILTER capacitance: why bigger is not automatically better

For the ACS724 FILTER approximation:

`fc = 1/(2πR_FC_total)`

Increasing C:

- decreases cutoff frequency;
- reduces high-frequency noise;
- attenuates more high-frequency signal;
- increases phase lag;
- slows transient response.

This is the central tradeoff.

The project requires DC–10 kHz diagnostic information. Therefore a filter that makes the trace beautifully quiet but suppresses the 10 kHz information is not a good design.

Approximate simple-pole values:

- +4.7 nF → fc ≈ 15.5 kHz;
- +10 nF → fc ≈ 8 kHz;
- +22 nF → fc ≈ 3.8 kHz;
- +100 nF → fc ≈ 0.88 kHz.

The 100 nF experiment was useful diagnostically because it showed that FILTER capacitance can reduce broadband CH2 variation. It was never a plausible final value for a 10 kHz measurement band.

---

## 19. First-order RC model versus a real sensor

A simple low-pass:

`H_RC(jω) = 1/(1 + jωRC)`

has magnitude:

`|H| = 1/sqrt(1 + (f/fc)²)`

and phase:

`φ = -atan(f/fc)`

The ACS724 is more than this one external RC:

- Hall sensing;
- internal amplifiers/filters;
- propagation delay;
- output stage;
- FILTER-pin network.

Therefore an empirical response can show phase lag not explained by the external FILTER RC alone.

But with only a few noisy frequency points, fitting “one pole + one pure delay” is not unique. Pole frequency and delay can trade off mathematically.

A good-looking fitted model is **not proof** of the internal physical model.

---

## 20. Why the repeated averages looked smooth but were not enough

The repeated-set complex averages were approximately:

- 1 kHz: 0.886 ∠ -6.5° V/A;
- 5 kHz: 0.871 ∠ -23.3° V/A;
- 7.5 kHz: 0.735 ∠ -36.5° V/A;
- 10 kHz: 0.803 ∠ -50.3° V/A.

The phase progression looks plausible and smooth.

However, individual measurements changed strongly while CH1 current remained stable.

The decisive example was the interleaved 5 kHz pair:

- A1: 0.556 V/A;
- A4: 1.056 V/A;

while current changed only from:

- 7.022 mApp;
- 7.043 mApp.

So a smooth average can hide unstable individual estimates.

This is why repeated averages must be examined together with:

- individual-run scatter;
- controls;
- residual level;
- time ordering;
- SNR.

---

## 21. Signal-to-residual problem

Typical wanted CH2 coherent signal:

`about 4–7 mVpp`

Typical CH2 residual:

`about 13–15 mV RMS`

These units are not directly the same amplitude convention, but the comparison immediately shows the basic difficulty: the target coherent sine is a small component inside much larger remaining variation.

Coherent fitting can recover a repeating component below the broadband residual because many cycles are observed, but the estimate can still have substantial uncertainty if structured residual content overlaps the target frequency or its phase wanders.

More captures do not magically remove every problem. Repeating a fundamentally low-SNR measurement can eventually become an exercise in averaging unstable estimates.

---

## 22. Complex averaging

At one frequency, write each transfer estimate as a phasor:

`H_k = |H_k| e^(jφ_k)`

Complex averaging means:

`H_avg = (1/N) Σ H_k`

This averages both in-phase and quadrature information.

It is preferable to separately averaging magnitude and phase when phases vary, because phase is circular and a pair such as +179° and -179° is actually close together, not 358° apart.

But complex averaging does **not** make bad data good. The individual distribution and repeatability must still be inspected.

---

## 23. Why the interleaved experiment was designed

The sequential 7.5 kHz block showed magnitude decreasing between the first and second halves.

One hypothesis was warm-up drift.

A proper test changes the order so frequency and elapsed time are not locked together:

`5 → 7.5 → 10 → 5 → 7.5 → 10 kHz`

If simple warm-up were dominant, the response would tend to move coherently with time.

Instead:

- 5 kHz changed dramatically upward;
- 7.5 kHz magnitude stayed similar but phase changed;
- 10 kHz moved differently.

Therefore simple monotonic warm-up does not explain the behavior.

This is a general experimental-design lesson:

> If two variables always change together, you cannot tell which caused the result. Interleave or randomize one variable to separate them.

---

## 24. Why we stop this experiment instead of collecting 100 more files

We have already isolated several major alternatives:

- primary current is stable;
- FILTER ground is physically verified;
- direct generator feedthrough is negligible;
- channel timing skew is measured and correctable;
- acquisition has enough samples/cycle;
- repeated CH2 estimates still vary strongly.

The remaining limitation is therefore not “we need ten more identical files.” The experiment has reached the point of diminishing returns with this small raw ACS724 signal.

A mature engineering experiment has a stopping rule. Here the stopping rule is:

> Continue only if another measurement can distinguish between remaining hypotheses or materially reduce design uncertainty.

More identical raw-sensor captures no longer satisfy that rule.

---

## 25. Why the AFE is the correct next step

The frozen architecture includes a designed Analog Front End before the RA4M1 ADC.

The raw-sensor tests demonstrated why it exists:

- ACS724 dynamic changes are only a few millivolts in this low-current fixture;
- the ADC needs a controlled amplitude range;
- broadband content must be limited before deterministic sampling;
- gain, filtering, and operating point must be known;
- the final measurement chain must be validated as a chain, not as an oscilloscope-only experiment.

The next experiment should therefore validate the AFE by itself with a known input.

This separates:

`known stimulus → AFE response`

from:

`ACS724 → AFE → ADC`

If the AFE does not behave correctly with a known clean stimulus, connecting the sensor would only add another unknown.

---

## 26. Planned AFE learning sequence

The next development step should be studied and executed in this order:

1. Read the frozen AFE schematic and identify every stage.
2. Explain the purpose of each resistor, capacitor, op-amp input/output, bias/reference connection, and power connection.
3. Predict DC operating points with no AC input.
4. Predict low-frequency gain.
5. Predict the intended Butterworth poles/corner behavior.
6. Build or verify one stage at a time.
7. Power it with no sensor attached and check for saturation/oscillation.
8. Apply a known low-amplitude sine.
9. Measure input and output simultaneously.
10. Check gain at low frequency.
11. Sweep selected frequencies around the designed corner.
12. Compare measured magnitude/phase with design.
13. Check clipping margin.
14. Only after independent AFE validation connect ACS724 OUT.
15. Only after analog-chain validation move to RA4M1 deterministic ADC acquisition.

This preserves the project method:

`predict → connect/configure → measure → compare → understand → document`

---

## 27. Compact review questions

**Q: Why is top-right MCP6022 leg pin 8 rather than pin 5?**  
A: PDIP numbering is counter-clockwise in top view: 1–4 down the left side, then 5–8 up the right side.

**Q: What does 250 kSa/s mean?**  
A: 250,000 stored samples per second.

**Q: What does `M: 2 ms` mean?**  
A: 2 ms per horizontal division; in the current fixed-10K project setup it has produced 4 µs CSV sample spacing.

**Q: Why use coherent-fit Vpp instead of raw Vpp?**  
A: It extracts only the commanded frequency rather than including noise spikes and other harmonics in the extrema.

**Q: Why divide CH1 voltage by 67 Ω?**  
A: CH1 measures the voltage across R8; Ohm's law gives primary current.

**Q: Why can CH2 residual be larger than the wanted sine while the sine is still measurable?**  
A: Repetition over many cycles allows coherent extraction of a component even when larger non-coherent/other-frequency variation is present.

**Q: What did the same-node control prove?**  
A: The exported CH2 waveform is approximately one stored sample behind CH1 under the tested acquisition modes.

**Q: Did it prove the oscilloscope uses sequential ADC conversion?**  
A: No. The internal cause remains unknown.

**Q: What did open-primary controls prove?**  
A: Direct AFG/MCP6022 feedthrough is too small to explain the current-on coherent CH2 signal.

**Q: Why not install 22 nF just because noise is lower?**  
A: Its estimated FILTER corner would be only about 3.8 kHz, strongly compromising the required 10 kHz band.

**Q: Is 4.7 nF now final?**  
A: No. It is the provisional candidate carried into the next stage.

**Q: Why stop raw dynamic characterization now?**  
A: The remaining precision problem is low CH2 SNR/repeatability, and more identical captures do not resolve the design uncertainty efficiently.

**Q: What is next?**  
A: Independent bring-up and validation of the designed analog front end before connecting the ACS724 and before ADC integration.
