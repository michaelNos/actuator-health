# Sampling, phase, spectrum, transfer function, and ACS724 dynamics — study questions

**Project:** Actuator Health Monitoring System  
**Date:** 2026-09-18  
**Purpose:** Educational note answering the questions raised during Stage B ACS724 dynamic/FILTER validation.

This is a **study note**, not an engineering-baseline approval. Numerical examples from the current bench work are used to explain the concepts. Accepted engineering decisions remain in `docs/`.

The current measurement convention is:

- **CH1:** voltage across the measured reference resistor `R8 = 67 Ω`, used to calculate primary current: `I = V_CH1 / 67 Ω`.
- **CH2:** Pololu #4048 / ACS724 `OUT` voltage relative to circuit ground.
- The temporary MCP6022 fixture creates a **positive-biased periodic current** through the ACS724 primary path.
- Current dynamic work uses coherent extraction of a known excitation frequency from noisy data.

---

## 1. How can I determine Δt, sampling rate, Nyquist frequency, record duration, and captured cycles myself — before running the measurement?

The first job is **not to read Δt from a CSV after the experiment**. The goal is to plan the acquisition from the signal frequency, then use the oscilloscope itself to verify that the selected acquisition actually provides the required sample rate.

### 1.1 What Δt means

`Δt` is the time between two consecutive stored samples:

`sample n ---- Δt ---- sample n+1 ---- Δt ---- sample n+2`

Sample rate and sample interval are reciprocals:

`fs = 1 / Δt`

therefore:

`Δt = 1 / fs`

Examples:

- `fs = 25 kSa/s` → `Δt = 1/25000 = 40 µs`
- `fs = 250 kSa/s` → `Δt = 1/250000 = 4 µs`

So to determine `Δt` yourself, determine the **actual sample rate currently used by the scope**, then take its reciprocal.

### 1.2 Method A — read the current sample rate from the oscilloscope

If the scope shows the current acquisition sample rate, use that value directly.

For example, if the scope reports:

`250 kSa/s`

then:

`Δt = 1/(250000) = 4 µs`

If it reports:

`25 kSa/s`

then:

`Δt = 40 µs`

Do not confuse the instrument's advertised **maximum** sample rate with the sample rate of the current acquisition. The scope may reduce the current sample rate when a longer time window is selected.

### 1.3 Method B — use record length and the actual stored acquisition duration

If you know:

- number of stored samples `N`;
- total duration represented by those stored samples `Trecord`;

then approximately:

`Δt ≈ Trecord / N`

and:

`fs ≈ N / Trecord`

More exactly, if the first and last stored samples are both included:

`Δt = (t_last - t_first)/(N - 1)`

For acquisition planning with 10000 points, the difference between `N` and `N-1` is very small.

Example:

`N = 10000`

`Trecord = 40 ms`

then:

`Δt ≈ 0.040/10000 = 4 µs`

and:

`fs ≈ 250 kSa/s`

### 1.4 Method C — inspect adjacent stored points on the stopped scope display

If the scope allows you to show individual sample dots and zoom deeply into a stopped record:

1. stop acquisition;
2. display/zoom until individual stored points are visible;
3. use time cursors between two adjacent points;
4. the horizontal time difference is approximately `Δt`.

This is the most direct physical interpretation of sample interval.

### 1.5 Why time/div alone is not enough

Suppose the display says:

`20 ms/div`

and there are 10 horizontal divisions.

That tells you the **visible screen width** is:

`10 × 20 ms = 200 ms`

But that does **not automatically prove** that the entire stored 10000-point record is exactly 200 ms long.

The stored acquisition may extend beyond the visible grid, and the instrument can decimate or display only part of stored memory.

Therefore do not calculate:

`Δt = (10 × time/div)/record_length`

unless you have verified that the displayed span and the full stored record are the same thing.

The safe workflow is:

`signal requirement → desired sample rate → scope setting → verify actual fs/record duration on the scope`

### 1.6 How to choose Δt before pressing RUN

Start from the signal frequency.

If the target signal frequency is `fsig`, then its period is:

`Tsig = 1/fsig`

Choose how many samples you want per cycle. For the present phase/waveform work, approximately **20–25 or more samples per cycle** is a useful engineering target, not a universal law.

Then:

`Δt_wanted = Tsig / samples_per_cycle`

and equivalently:

`fs_target = samples_per_cycle × fsig`

#### Example: design the 10 kHz acquisition before measuring

Target:

`fsig = 10 kHz`

Signal period:

`Tsig = 1/10000 = 100 µs`

Choose:

`25 samples/cycle`

Required sample interval:

`Δt_wanted = 100 µs / 25 = 4 µs`

Required sample rate:

`fs_target = 1/4 µs = 250 kSa/s`

So before touching RUN, the target is already known:

`10 kHz → 100 µs/cycle → 4 µs/sample → 250 kSa/s → 25 samples/cycle`

Now set the oscilloscope acquisition/timebase so that the **actual current sample rate** is approximately 250 kSa/s or faster.

### 1.7 Then determine record duration and captured cycles

If the scope stores `N = 10000` points at:

`fs = 250 kSa/s`

then:

`Trecord = N/fs = 10000/250000 = 40 ms`

At 10 kHz:

`cycles = Trecord × fsig = 0.040 × 10000 = 400 cycles`

So the complete designed acquisition is:

`10 kHz signal`

`→ 100 µs period`

`→ 4 µs desired sample spacing`

`→ 250 kSa/s sample rate`

`→ 25 samples/cycle`

`→ 10000 samples`

`→ 40 ms record`

`→ 400 captured cycles`

#### Same calculation for 1 kHz

At:

`fsig = 1 kHz`

period:

`Tsig = 1 ms`

For the same 25 samples/cycle:

`Δt_wanted = 1 ms/25 = 40 µs`

`fs_target = 25 kSa/s`

With 10000 samples:

`Trecord = 10000/25000 = 0.4 s`

Captured cycles:

`0.4 × 1000 = 400`

This is why preserving 25 samples/cycle requires a sample interval ten times shorter when the signal frequency becomes ten times higher:

- 1 kHz → `Δt = 40 µs`
- 10 kHz → `Δt = 4 µs`

### 1.8 After the acquisition, verify what actually happened

After the capture, verify that the scope actually used the intended settings:

1. actual sample rate;
2. record length;
3. actual record duration;
4. resulting samples/cycle;
5. resulting captured-cycle count.

CSV timestamps can be used later as an independent verification, but they are **not required to understand or plan Δt**.

### 1.9 From Δt to Nyquist

Once `Δt` is known:

`fs = 1/Δt`

and:

`fNyquist = fs/2`

Example with `Δt = 4 µs`:

`fs = 250 kSa/s`

`fNyquist = 125 kHz`

For a 10 kHz signal, this gives:

`samples_per_cycle = 250/10 = 25`

This is comfortably above the theoretical two-samples-per-cycle Nyquist boundary and is much more suitable for waveform and phase measurements.

### 1.10 Bench calculation checklist

Before running a periodic test, write down:

1. `fsig = ?`
2. `Tsig = 1/fsig = ?`
3. desired samples/cycle = ?
4. `Δt_wanted = Tsig/samples_per_cycle = ?`
5. `fs_target = 1/Δt_wanted = ?`
6. record length `N = ?`
7. `Trecord = N/fs = ?`
8. captured cycles `= Trecord × fsig = ?`
9. Nyquist `= fs/2 = ?`
10. verify the actual `fs` on the oscilloscope before accepting the measurement.

That is the manual acquisition-design process to use even if ChatGPT does not exist.

---

## 2. Is residual noise equal to ACS724 OUT minus IP−? Should CH1 and CH2 be equal?

**No. This is the most important correction in this note.**

CH1 and CH2 are not two measurements of the same physical quantity.

CH1 is the voltage across R8:

`V_CH1 = I_primary * R8`

CH2 is the sensor output:

`V_CH2 ≈ VZERO + S(f) * I_primary`

where:

- `VZERO` is the ACS724 zero-current output;
- `S(f)` is its frequency-dependent sensitivity in V/A.

Therefore CH1 and CH2 should **not** normally be equal in volts.

For example, if the current variation is 7 mApp:

`V_CH1,pp = 0.007 * 67 ≈ 0.469 Vpp`

With approximately 0.8 V/A sensor sensitivity:

`V_CH2,pp ≈ 0.007 * 0.8 = 5.6 mVpp`

Those are intentionally very different voltages.

### What residual means

For CH2 we fit:

`Vfit(t) = VDC + Vtarget(t)`

Then:

`e(t) = V_CH2,measured(t) - Vfit(t)`

So residual is **CH2 minus its own modeled DC + wanted coherent component**.

It is not:

`CH2 - CH1`

The residual can contain noise, harmonics, interference, drift, quantization, and any other waveform content not included in the model.

---

## 3. What is apparent transfer? Is it power?

No. The dynamic transfer used here is not power.

At one frequency:

`H(f) = VOUT_AC(f) / IPRIMARY_AC(f)`

Its units are:

`V/A`

That is a frequency-dependent sensor sensitivity or transfer gain.

We sometimes say **apparent transfer** because the measured ratio can include:

- the real ACS724 response;
- FILTER-pin dynamics;
- noise;
- measurement uncertainty;
- acquisition/channel effects.

Until those effects are isolated, the measured number is an estimate of the complete observed chain, not automatically the exact intrinsic sensor sensitivity.

Example:

`V_CH2,pp = 5.8 mV`

`Ipp = 6.8 mA`

then:

`|H| = 5.8e-3 / 6.8e-3 ≈ 0.85 V/A`

No watt unit appears.

---

## 4. How can I determine phase without ChatGPT?

For two clean periodic signals of the same frequency, use the oscilloscope's time cursors.

1. Measure the period `T`.
2. Choose corresponding points on CH1 and CH2, preferably rising zero crossings or equivalent peaks.
3. Measure their time displacement `Δt_phase`.
4. Convert to phase:

   `phase_deg = 360° * Δt_phase / T`

If CH2 occurs later than CH1, CH2 **lags**, so with our convention its phase is negative.

Example at 10 kHz:

`T = 1/10000 = 100 µs`

If CH2 occurs 16 µs after CH1:

`φ = -360 * 16/100 = -57.6°`

For noisy CH2, a single cursor crossing can be inaccurate. The coherent sine/cosine fit uses all samples and is therefore more robust, but the cursor method is the direct manual method.

The DOS1102S specification also lists automatic `Phase A→B` and delay measurements, but any automatic result should be checked against known controls when millivolt-level noisy signals are involved.

---

## 5. At 1 kHz or 10 kHz, are we sending AC current? Why does current change faster or slower?

The AFG generates a periodic voltage, normally a sine.

In our temporary fixture the MCP6022 shifts it so the current through the ACS724 remains **positive**. Therefore the current is best described as:

`i(t) = IDC + IAC*sin(2πft + φ)`

So it contains:

- a DC bias;
- an AC variation/ripple.

It is **not** a bipolar current that necessarily reverses direction every half-cycle.

Frequency tells us how fast the repeating change happens:

- 100 Hz → period = 10 ms
- 1 kHz → period = 1 ms
- 10 kHz → period = 100 µs

At 10 kHz the current completes 10000 oscillations each second. At 100 Hz it completes only 100.

The current changes because the driving voltage changes. In the temporary mostly resistive primary path, current follows the drive relatively quickly. In a strongly inductive load, inductance would oppose rapid current change according to `V = L di/dt`.

Also, this is not an **impulse**. An impulse is a short transient event. We are applying a periodic sinusoidal stimulus.

---

## 6. How can I analyze spectrum and harmonics manually?

Use the scope's FFT function or MATLAB/another numerical tool.

### On the oscilloscope

1. Select FFT/math mode.
2. Choose the source channel.
3. Use a suitable frequency span so the fundamental and several harmonics are visible.
4. Identify the fundamental `f0`.
5. Look at integer multiples:

   `2f0, 3f0, 4f0, ...`

For a 1 kHz stimulus:

- fundamental = 1 kHz
- second harmonic = 2 kHz
- third = 3 kHz
- fourth = 4 kHz

Use frequency/amplitude cursors to read the peaks.

### Important FFT ideas

Frequency-bin spacing is approximately:

`Δf = fs/N = 1/Trecord`

A longer record gives finer frequency resolution.

If the record does not contain an integer number of cycles, energy can spread into nearby bins. This is spectral leakage. A window such as Hanning/Hann reduces leakage but changes spectral shape and amplitude scaling.

For quantitative work, keep the FFT settings and window documented. For a first manual inspection, first identify which peaks are stable and whether they occur at the expected harmonics.

---

## 7. If the fundamental is highest and harmonics are much smaller, is the fundamental the wanted result and the rest just noise?

For the present **transfer measurement at a commanded frequency**, the fundamental is the main wanted component.

But harmonics are **not automatically noise**.

A harmonic is a deterministic component at an integer multiple of the fundamental. It can be caused by:

- waveform distortion;
- nonlinearity;
- clipping;
- asymmetry;
- the stimulus generator/fixture;
- the sensor or other circuitry.

Random/broadband noise is different: it is not locked to exact integer multiples in the same deterministic way.

So:

- for `H(1 kHz)`, use the coherent 1 kHz component;
- do not add 3 kHz or 5 kHz into the 1 kHz gain;
- but keep harmonics as diagnostic information because they can reveal distortion or later become health-monitoring features.

The third harmonic in CH1 during our tests was therefore **unmodeled residual content**, but not necessarily random noise.

---

## 8. Why does filtering increase phase lag?

Consider a first-order RC low-pass:

`H(jω) = 1 / (1 + jωRC)`

Its phase is:

`φ = -atan(ωRC)`

A capacitor must charge and discharge. It cannot reproduce rapid input changes instantaneously. As frequency increases, the output waveform increasingly trails the input waveform.

At very low frequency:

`ωRC << 1 → φ ≈ 0°`

At the corner frequency:

`ωRC = 1 → φ = -45°`

Far above the corner:

`ωRC >> 1 → φ approaches -90°`

The lag is not an arbitrary penalty added by mathematics; it is the time-domain consequence of energy storage in the capacitor.

---

## 9. What does “close to Nyquist” mean?

For sample rate `fs`, Nyquist frequency is:

`fN = fs/2`

A sinusoid at Nyquist has only two samples per cycle in the ideal limiting case.

Our old 10 kHz acquisition used:

`fs = 25 kSa/s`

Therefore:

`fN = 12.5 kHz`

and:

`samples_per_cycle = 25/10 = 2.5`

So 10 kHz was very close to the theoretical sampling limit.

It was technically below Nyquist, but there was very little margin. Harmonics above 12.5 kHz could alias into lower frequencies, and waveform/phase interpretation became fragile.

After changing acquisition:

`fs = 250 kSa/s`

At 10 kHz:

`samples_per_cycle = 25`

and Nyquist is 125 kHz. That is much healthier for quantitative work.

Nyquist is a mathematical minimum for reconstructing an ideally band-limited signal, **not a recommendation to measure real analog waveforms with only two or three points per cycle**.

---

## 10. Are we measuring OUT and IP− to calculate residual noise?

No.

We measure them simultaneously for two different purposes:

- CH1 at IP−/R8 gives the primary-current reference.
- CH2 at ACS724 OUT gives the sensor response.

We calculate the transfer:

`H(f) = V_CH2(f) / (V_CH1(f)/R8)`

Residual is calculated separately from one channel after fitting its model.

For CH2:

`e_CH2(t) = V_CH2(t) - [VDC + fitted_target_sine(t)]`

For CH1 we can calculate a separate CH1 residual in the same way.

CH1 is not subtracted from CH2 to obtain noise.

---

## 11. How can I determine VDC manually from an AC-varying signal?

If the scope uses DC coupling, the simplest definition is the time average:

`VDC = (1/N) * Σ v[n]`

On the scope, use a **Mean/Average** voltage measurement if available.

For a clean symmetric sine with no distortion:

`VDC ≈ (Vmax + Vmin)/2`

Example:

`Vmax = 0.506 V`

`Vmin = 0.494 V`

then:

`VDC ≈ 0.500 V`

For a distorted/noisy waveform, the arithmetic mean over many complete cycles is better than midpoint-of-extremes because Vmax and Vmin are sensitive to noise spikes.

---

## 12. How do I understand sine and cosine from the AFG?

The AFG normally generates **one sinusoid**. We are not physically generating a separate sine and cosine.

Mathematically:

`sin(ωt)`

and:

`cos(ωt)`

have the same shape and frequency; cosine is simply sine shifted by 90°:

`cos(ωt) = sin(ωt + 90°)`

Our analysis writes:

`A sin(ωt) + B cos(ωt)`

because that combination can represent a sine of **any phase**:

`C sin(ωt + φ)`

with:

`C = sqrt(A² + B²)`

`φ = atan2(B,A)`

The sine/cosine pair is therefore an analysis coordinate system. The AFG still generates one periodic waveform.

---

## 13. What does −0.49 dB represent?

The earlier `-0.49 dB` number represented an **amplitude ratio**, not absolute voltage and not directly power.

For amplitudes:

`dB = 20 log10(A2/A1)`

A value of `-0.49 dB` corresponds to:

`A2/A1 = 10^(-0.49/20) ≈ 0.945`

So the second amplitude is about **94.5%** of the reference amplitude: approximately 5.5% lower.

Negative dB means attenuation relative to the chosen reference.

That `-0.49 dB` was from the first 10 kHz result compared with the 1 kHz estimate. It was **not the final multi-run estimate**. The later complex-average comparison gave approximately `-0.70 dB`.

---

## 14. What is a complex transfer phasor?

At one frequency, a sinusoid can be represented by:

- magnitude;
- phase.

A phasor stores both together.

For the transfer:

`H(f) = Vout_phasor / Iin_phasor`

It can be written as:

`H = a + jb`

or:

`H = |H| ∠ φ`

Example:

`H(10 kHz) ≈ 0.784 ∠ -59.9° V/A`

means:

- magnitude: about 0.784 V/A;
- output lags the current reference by about 59.9° under the corrected measurement convention.

Complex averaging is useful because it averages the in-phase and quadrature information together. Simply averaging magnitudes would ignore whether individual estimates point in different phase directions.

---

## 15. Does the ACS724 FILTER allow only signals below 15.5 kHz to pass?

No.

The approximately 15.5 kHz value was our estimated **corner frequency** for the FILTER-pin RC network using:

`RF ≈ 1.8 kΩ`

and total capacitance approximately:

`C ≈ 1 nF + 4.7 nF = 5.7 nF`

Then:

`fc = 1/(2πRFC) ≈ 15.5 kHz`

A low-pass filter is not a brick wall.

At `fc` a first-order low-pass has magnitude:

`1/sqrt(2) ≈ 0.707`

which is `-3.01 dB`.

Signals above `fc` still pass, but with progressively greater attenuation and phase lag. Far above `fc`, a first-order pole approaches a -20 dB/decade magnitude slope.

Also, 15.5 kHz is not the ACS724's entire internal bandwidth. It is an estimate for the external FILTER capacitor acting with the device's internal FILTER resistance. Allegro specifies the unfiltered ACS724 analog bandwidth around 120 kHz and provides the FILTER pin so the user can trade bandwidth for lower noise.

---

## 16. If CH1 and CH2 measure the same node, can phase still be different? Why?

Electrically, if both probes measure exactly the same node relative to the same ground at the same time, the true phase difference should be approximately:

`0°`

In our same-node control, however, the exported CH1 and CH2 data showed about `-14.5°` difference.

At 10 kHz:

`Δt_sample = 4 µs`

One sample corresponds to:

`360° * 4 µs / 100 µs = 14.4°`

At 1 kHz:

`Δt_sample = 40 µs`

One sample again corresponds to:

`360° * 40 µs / 1 ms = 14.4°`

Advancing CH2 by one stored sample reduced the same-node phase difference to approximately zero.

So that phase was **not a real electrical phase difference**. It was an acquisition/export channel-alignment artifact in those CSV records.

When CH1 is on R8 and CH2 is on ACS OUT, additional phase difference can be physically real because the ACS724 and its filtering have dynamic response.

---

## 17. What does H(10k)/H(1k) tell us? What does a ratio generally tell us?

A ratio compares one quantity with another reference.

If:

`R = A2/A1`

then:

- `R = 1`: equal;
- `R < 1`: A2 is smaller;
- `R > 1`: A2 is larger.

For frequency response, use the **complex ratio**:

`Hnorm = H(10 kHz) / H(1 kHz)`

Magnitude:

`|Hnorm| = |H10| / |H1|`

Phase:

`φnorm = φ10 - φ1`

Using the corrected current estimates:

`|H1| ≈ 0.850 V/A`

`|H10| ≈ 0.784 V/A`

Therefore:

`|H10/H1| = 0.784/0.850 ≈ 0.922`

In dB:

`20 log10(0.922) ≈ -0.70 dB`

With phases approximately:

`φ1 = -18.18°`

`φ10 = -59.87°`

then:

`Δφ = -59.87 - (-18.18) ≈ -41.69°`

This normalized ratio is useful because constant absolute sensitivity factors largely cancel. It tells us **how the system changes with frequency**, which is what a frequency-response measurement is meant to show.

---

## 18. How are propagation delay, response time, and rise time calculated?

These are normally **measured from a step response**, not derived from one universal formula.

According to the ACS724 datasheet definitions:

### Propagation delay, tpd

Measure the time between:

- input current reaching 20% of its final step value;
- sensor output reaching 20% of its corresponding final change.

`tpd = t(output 20%) - t(input 20%)`

### Response time, tRESPONSE

Measure the time between:

- input current reaching 90% of its final value;
- sensor output reaching 90% of its corresponding final value.

`tRESPONSE = t(output 90%) - t(input 90%)`

### Rise time, tr

This belongs to the output waveform itself:

`tr = t(output 90%) - t(output 10%)`

For a simple first-order system:

`tr(10–90%) ≈ 2.197τ`

and approximately:

`fc ≈ 0.35/tr`

But the actual ACS724 is more complex than one ideal RC pole, so use datasheet definitions or measured step data for the real device.

Do not confuse these three quantities:

- propagation delay asks **when the output starts following relative to the input**;
- rise time asks **how long the output takes to travel from 10% to 90%**;
- response time compares the input's 90% time with the output's 90% time.

Primary source: Allegro ACS724 datasheet, section “Response Characteristics Definitions and Performance Data”.

---

## 19. Why does RC = f/fc?

It does **not**.

The correct dimensionless expression is:

`ωRC = f/fc`

Derivation:

`fc = 1/(2πRC)`

and:

`ω = 2πf`

Therefore:

`ωRC = (2πf)RC`

From the corner-frequency equation:

`2πRC = 1/fc`

so:

`ωRC = f/fc`

This matters because:

- `RC` has units of seconds;
- `f/fc` has no units.

They cannot be equal by themselves.

The low-pass magnitude can therefore be written either as:

`|H| = 1/sqrt(1+(ωRC)²)`

or:

`|H| = 1/sqrt(1+(f/fc)²)`

and phase as:

`φ = -atan(ωRC) = -atan(f/fc)`

---

## 20. Why does delay contribute to phase shift?

A time delay means the output waveform is shifted to the right in time:

`y(t) = x(t - td)`

For a sine:

`x(t) = sin(2πft)`

then:

`y(t) = sin[2πf(t-td)]`

Expand:

`y(t) = sin(2πft - 2πf td)`

So the phase shift caused by pure delay is:

`φ = -2πf td` radians

or:

`φ = -360° * f * td`

This explains why the same physical delay creates more phase shift at higher frequency.

Example for `td = 2 µs`:

At 1 kHz:

`φ = -360 * 1000 * 2e-6 = -0.72°`

At 10 kHz:

`φ = -7.2°`

The time delay stayed 2 µs, but the 10 kHz period is ten times shorter, so 2 µs occupies ten times more of one cycle.

This is why sensor propagation delay, filter dynamics, probe/channel skew, and digital sample offset all matter in phase measurements.

---

## Compact self-check

Before any future frequency-response capture, be able to answer these without software assistance:

1. What is the target signal frequency and period?
2. What sample rate will the selected acquisition produce?
3. How many samples per cycle will that give?
4. What is Nyquist frequency?
5. How long is the record?
6. How many cycles will be captured?
7. Which node represents current and which represents sensor output?
8. What gain unit should the transfer have?
9. Is a measured phase difference physical or could it be channel timing skew?
10. Is a spectral line a harmonic, interference component, or broadband noise?

If those ten questions are clear before the capture, the measurement is much easier to interpret correctly afterward.

## Primary references

- Allegro MicroSystems, **ACS724 datasheet**: https://www.allegromicro.com/-/media/files/datasheets/acs724-datasheet.ashx
- Pololu, **ACS724 Current Sensor Carrier -5A to +5A, 5V (item #4048)**: https://www.pololu.com/product/4048
- HANMATEK, **DOS1102S product/manual center**: https://hanmatek.com/en-eu/pages/manuals-center
- Related project notes:
  - [Oscilloscope acquisition and triggering](oscilloscope-acquisition-and-triggering.md)
  - [Signal-analysis concepts used in ACS724 dynamic validation](signal-analysis-concepts-for-acs724-dynamic-validation-2026-09-11.md)
  - [ACS724 noise, bandwidth, and FFT](acs724-noise-bandwidth-and-fft.md)
