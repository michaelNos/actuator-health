# Signal-analysis concepts used in ACS724 dynamic validation — 2026-09-11

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — ACS724 dynamic/FILTER validation  
**Purpose:** Study record explaining the mathematical and measurement concepts used to judge the 100 Hz baseline and later frequency-response points.

This document is intentionally educational. It does not change the frozen 100 Hz engineering decision. It explains how the quantities used in the Stage B evidence records are defined, calculated, interpreted, and limited.

---

## 1. Coherent sine fit used in the project

For a known test frequency `f0`, each captured channel is modeled as:

`v(t) = V0 + A*sin(2*pi*f0*t) + B*cos(2*pi*f0*t)`

where:

- `V0` is the DC/mean term;
- `A` is the fitted sine coefficient;
- `B` is the fitted cosine coefficient;
- `f0` is the commanded excitation frequency, for example 100 Hz;
- `t` is the CSV time vector.

The coefficients are found by least squares: choose `V0`, `A`, and `B` so that the sum of squared differences between the measured samples and the fitted model is as small as possible.

For each sample `i`:

`y_i = measured sample`

`yhat_i = V0 + A*sin(2*pi*f0*t_i) + B*cos(2*pi*f0*t_i)`

The residual is:

`r_i = y_i - yhat_i`

The coherent peak amplitude at `f0` is:

`Vpk = sqrt(A^2 + B^2)`

and therefore:

`Vpp = 2*sqrt(A^2 + B^2)`

This is why the project does not use raw oscilloscope `Vpp` for noisy ACS724 VIOUT measurements: raw peak-to-peak is dominated by the largest excursions, while the coherent fit extracts only the part that repeats exactly at the known excitation frequency.

---

## 2. What fit R^2 means

`R^2` is the coefficient of determination. It answers:

> How much of the measured sample-to-sample variation is explained by the fitted model?

Define:

`SSE = sum((y_i - yhat_i)^2)`

This is the residual sum of squares: variation not explained by the model.

Define:

`SST = sum((y_i - ybar)^2)`

where `ybar` is the mean of all samples. `SST` is the total measured variation around the mean.

Then:

`R^2 = 1 - SSE/SST`

Interpretation:

- `R^2 = 1`: the fitted DC + sine/cosine model explains the record perfectly;
- `R^2 = 0`: it explains no more variation than simply using the mean;
- values close to 1 indicate a very clean waveform at the modeled frequency;
- low `R^2` can occur even when a real coherent component exists, if that component is small compared with broadband noise or other unmodeled content.

### Project interpretation

CH1 across RREF at the stronger 100 Hz stimulus produced `R^2` values around 0.998–0.999. This means the RREF waveform is dominated by a clean 100 Hz sinusoid and is an excellent current reference.

CH2 at ACS724 VIOUT had a much lower fit quality because the wanted 100 Hz component was only a few millivolts while the waveform contained tens of millivolts RMS of broadband/unmodeled variation. A low CH2 `R^2` therefore does not automatically mean that the fitted 100 Hz component is fictitious; it means the 100 Hz sinusoid explains only a small fraction of the total CH2 variance.

Important limitation: `R^2` is a model-fit metric, not a direct signal-quality certification. A waveform can have high `R^2` but still be systematically wrong, clipped, incorrectly scaled, or measured from the wrong node.

---

## 3. Residual and residual RMS

After the fitted DC + target-frequency sinusoid is calculated, the residual is what remains:

`r_i = y_i - yhat_i`

The residual RMS is:

`RMS_residual = sqrt((1/N)*sum(r_i^2))`

where `N` is the number of samples.

This is the root-mean-square size of everything not explained by the chosen model.

### Physical meaning

Residual RMS may contain:

- broadband electrical noise;
- interference at other frequencies;
- harmonics of the test frequency;
- switching spikes;
- slow drift;
- oscilloscope quantization;
- measurement pickup;
- waveform distortion;
- model mismatch;
- any real signal content not included in the fit.

Therefore the phrase **residual noise** in the project is shorthand. Strictly, residual RMS is not guaranteed to be pure random noise. It is the RMS of the unmodeled remainder.

### Why RMS is used

Positive and negative residual samples would cancel if they were simply averaged. Squaring removes the sign, averaging measures mean energy-like magnitude, and the square root returns the result to volts.

For example, a CH2 residual RMS near 30 mV means that after removing the fitted DC and coherent 100 Hz sine, the remaining waveform has an RMS magnitude of about 30 mV.

That does **not** mean the sensor itself has exactly 30 mV RMS intrinsic noise. The value includes the whole measurement chain and all unmodeled content in that acquisition.

---

## 4. How phase is calculated from the sine fit

The fitted AC part is:

`A*sin(omega*t) + B*cos(omega*t)`

where:

`omega = 2*pi*f0`

Any single sinusoid can also be written as:

`C*sin(omega*t + phi)`

Using:

`sin(x + phi) = sin(x)*cos(phi) + cos(x)*sin(phi)`

we obtain:

`A = C*cos(phi)`

`B = C*sin(phi)`

therefore:

`C = sqrt(A^2 + B^2)`

and:

`phi = atan2(B, A)`

`atan2` is used rather than ordinary `atan(B/A)` because it preserves the correct quadrant and therefore the correct phase sign/range.

### Transfer phase between CH1 and CH2

Each channel gets its own fitted phase:

`phi_CH1 = atan2(B1, A1)`

`phi_CH2 = atan2(B2, A2)`

The sensor/output phase relative to the current reference is:

`Delta_phi = phi_CH2 - phi_CH1`

and then wrapped into a convenient interval such as `-180 deg ... +180 deg`.

### Critical condition

Phase comparison is meaningful only if both channels represent the same acquisition time reference. That is why the project freezes one acquisition and exports CH1 and CH2 without resuming acquisition.

If CH1 and CH2 came from unrelated acquisitions with arbitrary start times, their absolute fitted phases would not be directly comparable.

### Why phase was not accepted at 100 Hz

The 100 Hz gain magnitude became reasonably repeatable, but CH2 phase changed noticeably between shorter blocks and repeated runs. When the coherent output is only a few millivolts inside much larger residual variation, small noise changes can rotate the fitted phasor substantially. Therefore the project accepted the practical 100 Hz magnitude baseline but did not accept precision phase.

---

## 5. What a spectral component is

A time-domain waveform tells us voltage versus time. Spectral analysis asks a different question:

> How much of this waveform exists at each frequency?

A Fourier transform / discrete Fourier transform represents the record as a sum of sinusoidal components at different frequencies.

For a sampled record, each analyzed frequency has a complex spectral coefficient:

`X(f) = Re{X(f)} + j*Im{X(f)}`

This coefficient contains both:

- magnitude at that frequency;
- phase at that frequency.

A **spectral component at 100 Hz** therefore means the part of the measured waveform associated with a sinusoid at 100 Hz.

A clean 100 Hz sine ideally creates a strong spectral line at 100 Hz. Noise produces energy over many frequencies. Distortion creates harmonics such as 200 Hz, 300 Hz, etc.

### Relation to the coherent sine fit

The known-frequency least-squares fit and a Fourier component at the same frequency are closely related. Both project the waveform onto sine and cosine basis functions at that frequency.

The least-squares form is convenient in this project because:

- the exact commanded test frequency is already known;
- DC can be included explicitly;
- amplitude and phase are obtained directly;
- the complete spectrum does not have to be interpreted merely to extract one known component.

The FFT/DFT is useful when we want to inspect the surrounding spectrum, harmonics, interference, or local noise floor.

---

## 6. Spectral leakage and frequency bins

A finite record does not contain an infinite-duration sine. The DFT evaluates discrete frequency locations called **bins**.

Approximate bin spacing is:

`Delta_f = fs/N = 1/Trecord`

where:

- `fs` is sample rate;
- `N` is sample count;
- `Trecord` is total record duration.

If the record contains an integer number of cycles of the sine and the frequency lies exactly on a DFT bin, its energy can be concentrated strongly in one bin.

If not, its energy spreads into neighboring bins. This is called **spectral leakage**.

Window functions can reduce leakage at the cost of changing amplitude/noise bandwidth and widening the main spectral lobe. Therefore any quantitative spectrum calculation must state or control the window and amplitude correction if precision is required.

---

## 7. What neighboring spectral noise means

Suppose the wanted signal is at 100 Hz. We inspect spectral amplitudes in frequencies near 100 Hz but exclude the 100 Hz target itself.

Those nearby components estimate the local spectral background around the signal.

In the Stage B analysis, a robust local indicator used was the **median amplitude of neighboring spectral components** in a local frequency region around the target, excluding the target component itself.

Why the median rather than the maximum?

- one accidental interferer or spike can dominate the maximum;
- the median better represents the typical local background level.

This local spectral background is what was informally called **neighboring spectral noise**.

It should not be confused with residual RMS:

- residual RMS measures the total time-domain RMS of everything left after the fit;
- neighboring spectral noise estimates typical frequency-domain amplitude near the target frequency.

A waveform can have large broadband residual RMS but still have a clearly identifiable narrow coherent line at 100 Hz.

---

## 8. How a spectral component is compared in dB

For voltage/current/amplitude ratios:

`dB = 20*log10(A2/A1)`

For power ratios:

`dB = 10*log10(P2/P1)`

The factor 20 appears for voltage/current amplitudes because, for fixed impedance, power is proportional to amplitude squared.

### A. Target component versus neighboring spectral background

If:

`Vtarget = amplitude of 100 Hz component`

`Vnoise = median neighboring spectral amplitude`

then:

`contrast_dB = 20*log10(Vtarget/Vnoise)`

Examples:

- `0 dB` means equal amplitudes;
- `+6.02 dB` means target amplitude is about 2 times the reference;
- `+20 dB` means about 10 times;
- a negative result means the target amplitude is smaller than the reference level.

A result such as `+9.9 dB` means the coherent target amplitude is about `10^(9.9/20) ~= 3.1` times the local median spectral amplitude.

### B. Frequency-response normalization

For the future FILTER sweep, the magnitude at frequency `f` can be normalized to the accepted 100 Hz baseline:

`Hnorm(f) = G(f)/G(100 Hz)`

then:

`H_dB(f) = 20*log10(G(f)/G(100 Hz))`

Examples:

- `0 dB`: same amplitude gain as the baseline;
- `-3.01 dB`: amplitude ratio about 0.707;
- `-6.02 dB`: amplitude ratio about 0.5;
- `-20 dB`: amplitude ratio 0.1.

These are two different uses of dB:

1. signal-versus-local-noise contrast;
2. normalized transfer magnitude versus baseline.

They must not be mixed.

---

## 9. What four independent five-cycle sections meant

The early 100 Hz record contained about 20 cycles.

To test repeatability, the record was divided into four contiguous, non-overlapping sections:

- section 1: cycles 1–5;
- section 2: cycles 6–10;
- section 3: cycles 11–15;
- section 4: cycles 16–20.

Each section was fitted separately using the same known-frequency sine/cosine model.

For every section we recalculated:

- CH1 coherent amplitude;
- CH2 coherent amplitude;
- gain `VOUT/I`;
- phase difference.

If the measurement is robust, these values should remain reasonably similar from block to block.

If gain and phase jump strongly between five-cycle blocks, the full-record result may be strongly dependent on averaging noise rather than being a stable short-term measurement.

The word **independent** here means separate non-overlapping data blocks. It does not prove perfect statistical independence; slowly varying or correlated noise can influence multiple blocks.

Later, when the record was extended to about 100 cycles, much longer blocks such as 50-cycle halves became significantly more stable. That was evidence that longer coherent averaging improves the estimate.

---

## 10. What driver validation means in this project

The MCP6022 circuit is not the sensor under test. It is the temporary signal generator/level-shifting driver used to create positive current through the ACS724.

Before interpreting an ACS724 VIOUT waveform, the project temporarily measures:

- CH1 = RREF voltage/current reference;
- CH2 = MCP6022 pin 1 driver output.

The driver-validation check asks:

1. Is the intended frequency present?
2. Is the driver amplitude approximately as expected?
3. Is the waveform sinusoidal rather than visibly distorted?
4. Is its DC center where expected?
5. Does the output remain away from the supply rails?
6. Does RREF confirm that primary current remains positive throughout the cycle?
7. Does the load current scale sensibly when stimulus amplitude changes?

Only after these conditions are satisfied is CH2 moved from MCP6022 pin 1 to ACS724 VIOUT.

This prevents attributing source/driver failure to sensor behavior.

---

## 11. What clipping is

Clipping occurs when a circuit or measurement system cannot reproduce the requested waveform beyond some limit.

For example, if an amplifier powered from 0 V and 5 V is commanded to produce a sine that would mathematically require -0.5 V or 5.5 V, the real output cannot follow that request. Peaks flatten near the achievable limits.

Conceptually:

ideal sine:

`... smooth rounded peak ...`

clipped sine:

`... flat-topped peak ...`

Clipping can happen in several places:

- op-amp output approaching its supply/output-swing limit;
- generator output limit;
- ADC input range;
- oscilloscope vertical acquisition range;
- another circuit element saturating.

Why clipping is dangerous for transfer measurements:

- amplitude is no longer linearly related to input;
- strong harmonics are created;
- phase can shift;
- the current waveform may no longer be sinusoidal;
- fitted fundamental magnitude can become misleading.

This is why we explicitly validated the 2.00 Vpp stimulus at MCP6022 pin 1 before using it for the ACS724 measurement.

---

## 12. Electrical feedthrough and crosstalk

The intended signal path is:

`AFG -> MCP6022 -> primary current -> ACS724 Hall response -> VIOUT`

But an unwanted signal can reach VIOUT through another path.

Examples include:

- capacitive coupling between nearby wires/breadboard rows;
- shared-ground impedance;
- supply-rail coupling;
- coupling through probe leads;
- electromagnetic coupling;
- coupling internal to measurement equipment;
- direct circuit crosstalk between driver and sensor-output wiring.

This unwanted path is called **feedthrough** or **crosstalk**.

The danger is that a 100 Hz signal at VIOUT might look like a real Hall-current response even if no primary current is flowing.

### Control experiment used in the project

The primary-current path was opened by disconnecting the 220 ohm resistor from ACS724 IP+ while keeping the AFG/MCP6022 stimulus running.

This removes the intended Hall-current mechanism while preserving much of the same electrical environment.

A proper control then used:

- CH1 = MCP6022 pin 1 as a direct reference to the still-running stimulus;
- CH2 = ACS724 VIOUT;
- primary path open.

If a stable coherent 100 Hz VIOUT component with repeatable phase remains, that is evidence of feedthrough/crosstalk.

In the documented 100 Hz control, no stable coherent feedthrough strong enough to explain the current-on response was demonstrated.

---

## 13. What a phasor is

A phasor is a compact complex-number representation of a sinusoid at one fixed frequency.

For:

`v(t) = Vpk*sin(omega*t + phi)`

we can represent the sinusoidal component as:

`Vphasor = Vpk * exp(j*phi)`

or equivalently:

`Vphasor = Vpk*(cos(phi) + j*sin(phi))`

The phasor therefore contains both:

- amplitude `Vpk`;
- phase `phi`.

It can be pictured as an arrow in the complex plane:

- arrow length = amplitude;
- arrow angle = phase.

### Why phasors matter for feedthrough subtraction

Suppose the measured output contains both true sensor response and unwanted feedthrough:

`Vmeasured = Vsensor + Vfeedthrough`

At one frequency this is a **vector/complex addition**, not merely addition of magnitudes.

Therefore:

`Vsensor = Vmeasured - Vfeedthrough`

must be performed as phasor subtraction.

It is generally wrong to calculate:

`|Vsensor| = |Vmeasured| - |Vfeedthrough|`

unless both happen to have exactly the same phase.

### Example

Suppose:

`Vmeasured = 6 mV at 0 deg`

`Vfeedthrough = 1 mV at +90 deg`

As complex values:

`Vmeasured = 6 + j0 mV`

`Vfeedthrough = 0 + j1 mV`

therefore:

`Vsensor = 6 - j1 mV`

Its magnitude is:

`|Vsensor| = sqrt(6^2 + 1^2) = 6.083 mV`

and its phase is approximately:

`atan2(-1,6) = -9.46 deg`

Simply subtracting magnitudes would give `5 mV`, which is wrong.

This is why the project did not blindly subtract the amplitude of the first open-primary VIOUT control from the current-on result.

---

## 14. Connection between fitted coefficients and phasors

From the model:

`v(t) = V0 + A*sin(omega*t) + B*cos(omega*t)`

we already calculated:

`Vpk = sqrt(A^2 + B^2)`

`phi = atan2(B,A)`

Therefore the fitted sine/cosine coefficients directly define a phasor.

Conceptually:

`Vphasor = Vpk * exp(j*phi)`

This is why coherent fitting gives both transfer magnitude and transfer phase.

For two synchronized channels:

`H(f) = Vout_phasor / Iin_phasor`

The magnitude is:

`|H| = |Vout| / |Iin|`

and phase is:

`angle(H) = phi_out - phi_in`

For CH1 measured across RREF:

`Iin_phasor = Vref_phasor / RREF`

because a pure resistor does not add ideal phase shift between its voltage and current.

---

## 15. Residual RMS versus spectral noise versus coherent component

These three quantities answer different questions.

### Coherent component

> How large is the sine specifically at the commanded test frequency?

Example unit: `mVpp at 100 Hz`.

### Residual RMS

> After removing DC and the fitted target-frequency sinusoid, how large is everything else in the time record in RMS terms?

Example unit: `mV RMS`.

### Neighboring spectral noise/background

> Around the target frequency, how large are typical nearby frequency-domain components compared with the target spectral line?

Example unit: `mVpp-equivalent spectral amplitude` or a target/background ratio in dB, depending on the analysis normalization.

None of these should be substituted blindly for another.

---

## 16. Why a coherent signal can be smaller than residual RMS and still be measurable

This was important for ACS724 VIOUT.

Imagine a 6 mVpp sine buried inside broadband random variation with about 30 mV RMS total residual magnitude.

The random/noisy part changes sign and phase unpredictably from cycle to cycle.

The true 100 Hz sine repeats at exactly the same frequency and phase relationship.

When many cycles are analyzed coherently, the repeating component adds consistently while incoherent noise tends to average down.

This is why extending the record from about 20 cycles to about 100 cycles improved the stability of the 100 Hz gain estimate without increasing the electrical stimulus.

This is also why raw oscilloscope peak-to-peak values were unsuitable: raw peaks respond strongly to broadband spikes, while coherent fitting asks only for the repeatable component at the commanded frequency.

---

## 17. Why block-to-block stability is important

A full-record fit always produces a number. That alone does not prove the number is trustworthy.

A useful robustness check is to divide the record into separate blocks and repeat the calculation.

If the result is real and sufficiently above the uncertainty/noise environment, then:

- gain should remain reasonably consistent;
- phase should remain reasonably consistent;
- the current reference should remain stable.

Large block-to-block jumps indicate that:

- the record may be too short;
- SNR may be insufficient;
- interference may be dominating;
- phase may not yet be measurable precisely;
- the stimulus or measurement may not be stationary.

This is why the project did not immediately accept early full-record gain numbers even when a numerical value could be calculated.

---

## 18. Practical interpretation hierarchy for this project

When judging each future frequency point, use this order:

1. **Driver validity** — correct node, correct frequency, no visible clipping, sensible amplitude/headroom.
2. **Current validity** — CH1/RREF clean enough, sufficient sampling/resolution, primary current stays within the valid positive range.
3. **Synchronized acquisition** — CH1 and CH2 from the same frozen record.
4. **Coherent component** — fit the exact commanded frequency.
5. **Fit quality / residuals** — inspect `R^2`, residual RMS, distortion and harmonics.
6. **Spectral context** — verify the target line stands sensibly above neighboring spectral background and check for unexpected harmonics/interference.
7. **Repeatability** — compare blocks and/or repeated acquisitions.
8. **Controls** — when suspicious, remove the intended physical mechanism and test for feedthrough/crosstalk.
9. **Only then interpret transfer magnitude/phase**.

A mathematically calculated gain is not automatically an accepted engineering measurement.

---

## 19. Compact formula reference

Known-frequency fit:

`v(t) = V0 + A*sin(2*pi*f*t) + B*cos(2*pi*f*t)`

Peak amplitude:

`Vpk = sqrt(A^2 + B^2)`

Peak-to-peak amplitude:

`Vpp = 2*Vpk`

Phase:

`phi = atan2(B,A)`

Residual:

`r_i = y_i - yhat_i`

Residual RMS:

`RMSres = sqrt(sum(r_i^2)/N)`

Coefficient of determination:

`R^2 = 1 - sum(r_i^2)/sum((y_i-ybar)^2)`

Current from RREF:

`Iphasor = V_RREF_phasor / RREF`

Transfer phasor:

`H(f) = VOUT_phasor / I_phasor`

Transfer magnitude:

`|H| = |VOUT|/|I|`

Transfer phase:

`angle(H) = phi_VOUT - phi_I`

Amplitude ratio in dB:

`20*log10(A2/A1)`

Normalized frequency response:

`H_dB(f) = 20*log10(G(f)/G(100 Hz))`

Phasor addition/subtraction:

`Vmeasured = Vsensor + Vfeedthrough`

`Vsensor = Vmeasured - Vfeedthrough`

---

## 20. Engineering status after this study record

This document explains the analysis concepts only. The current Stage B engineering state remains:

- accepted practical 100 Hz normalized-sweep magnitude baseline: `G100 = 0.8792 V/A`;
- prior independent DC calibration remains a separate result and is not replaced;
- precision 100 Hz phase remains unaccepted;
- no stable coherent feedthrough sufficient to explain the 100 Hz current-on response was demonstrated in the proper open-primary control;
- first 1 kHz files `021`/`022` remain quarantined/non-accepted because of inadequate sampling and distorted CH1 capture;
- no external ACS724 FILTER capacitor has been approved yet.

The next engineering work after this study gate is to re-establish a valid 1 kHz acquisition with adequate time resolution and validated driver/current waveforms before interpreting any 1 kHz transfer result.
