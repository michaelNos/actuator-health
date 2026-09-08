# Phase 3 Extension — ACS724 FILTER Development: Theory, Prediction, and Pre-Build Record

**Status:** UNDERSTAND + PREDICT complete; BUILD not started  
**Project:** Actuator Health Monitoring System  
**Date:** 2026-09-08

## Purpose

This document records the theory, calculations, engineering interpretation, and pre-build decisions established before modifying the ACS724 FILTER network.

The project workflow remains:

`understand -> design -> predict -> build -> measure -> validate -> document`

This record intentionally stops before the build step. No external FILTER capacitor has yet been accepted as the final Rev-1 design value.

The formal diagnostic signal band remains:

`DC to 10 kHz`

The objective of the FILTER-development phase is therefore not to make the oscilloscope trace as smooth as possible. The objective is to reduce unnecessary broadband output noise while preserving diagnostically useful current information through 10 kHz with a known amplitude, phase, and transient-response tradeoff.

---

## 1. Experimental context entering FILTER development

The preceding zero-current noise-isolation work established the following bench observations:

- repeatable zero-current ACS724 `VOUT` disturbance of approximately `29.55 mV RMS` under the tested configuration;
- oscilloscope/probe floor approximately `1.43 mV RMS`, much smaller than the observed sensor-output disturbance;
- motor physically removed during the decisive zero-current noise tests;
- bench-supply versus Arduino-supply A-B-A comparison changed measured `VCC` noise substantially while `VOUT` noise remained near 30 mV RMS;
- the 20 MHz oscilloscope bandwidth limiter reduced measured high-frequency `VCC` noise as expected;
- the approximately 30 mV RMS `VOUT` disturbance is therefore real and repeatable in the present bench configuration, but it has **not** been proven to be purely intrinsic ACS724 IC noise.

Remaining possible contributors include the sensor itself, its FILTER network, carrier layout, output-node coupling, grounding/local coupling, and other analog implementation effects.

This motivates a controlled FILTER-capacitance experiment.

---

## 2. ACS724 FILTER-node model

For filter-development calculations, the relevant ACS724 signal-conditioning section is modeled as an internal resistance feeding the FILTER node, with capacitance from FILTER to ground:

```text
internal signal
     |
     R_F(int) ~= 1.8 kOhm
     |
     +-------> buffered internal/output path -> VOUT
     |
     C_F
     |
    GND
```

The Pololu #4048 carrier already includes approximately:

`C_stock = 1 nF`

from FILTER to ground.

The simple first-order design model therefore uses:

`R_F = 1.8 kOhm`

and

`C_total = C_stock + C_ext`

where `C_ext` is any additional capacitor intentionally placed between FILTER and GND.

Because parallel capacitors add:

`C_total = 1 nF + C_ext`

The stock `1 nF` carrier configuration gives a simple RC prediction near `88.4 kHz`, consistent with the carrier's approximate `90 kHz` bandwidth statement. This agreement is used as a useful sanity check for candidate calculations.

The RC model is a design approximation. The complete IC has additional internal dynamics, so final bandwidth shall be established by measurement rather than calculation alone.

---

## 3. Capacitor polarity and selected component type

The available candidate capacitors are small ceramic capacitors:

- `2.2 nF`, marking `222`;
- `3.3 nF`, marking `332`;
- `4.7 nF`, marking `472`.

These ceramic capacitors are **non-polarized**. Either lead may be connected to FILTER or GND.

A polarized capacitor has designated positive and negative terminals and must normally be installed with the correct DC polarity. Electrolytic and many tantalum capacitors are common polarized examples. Their construction enables relatively large capacitance in a compact package, but reverse connection can cause leakage, damage, heating, or failure.

The ACS724 FILTER candidates in this study do not require a polarized capacitor. A small ceramic capacitor is appropriate for this low-capacitance, high-frequency filtering function.

---

## 4. RC circuit voltages, current, and impedance

For a sinusoidal source applied to a series RC low-pass:

```text
Vin ---- R ----+---- Vout = V_C
               |
               C
               |
              GND
```

The resistor impedance is:

`Z_R = R`

The capacitor impedance is:

`Z_C = 1 / (j omega C)`

with:

`omega = 2 pi f`

The same series current flows through the resistor and capacitor:

`I = Vin / (R + Z_C)`

The component voltages are:

`V_R = I R`

`V_C = I Z_C`

Kirchhoff's voltage law remains:

`Vin = V_R + V_C`

However, for AC sinusoidal steady state this is a **phasor** sum. `V_R` and `V_C` do not generally have the same phase, so their magnitudes must not simply be added arithmetically.

For an ideal series RC circuit, resistor voltage is in phase with current while capacitor voltage lags current by 90 degrees. The input phasor is the vector sum of those two component-voltage phasors.

---

## 5. First-order RC low-pass transfer function

The low-pass output is the capacitor voltage. Using the impedance-divider relation:

`H(j omega) = Vout / Vin = Z_C / (R + Z_C)`

Substituting:

`Z_C = 1 / (j omega C)`

gives:

`H(j omega) = 1 / (1 + j omega R C)`

This is the canonical first-order RC low-pass transfer function.

Its magnitude is:

`|H| = 1 / sqrt(1 + (omega R C)^2)`

or, using cutoff frequency:

`|H(f)| = 1 / sqrt(1 + (f / f_c)^2)`

The phase is:

`phi(f) = -atan(f / f_c)`

The cutoff frequency is:

`f_c = 1 / (2 pi R C)`

At `f = f_c`:

- amplitude ratio = `1 / sqrt(2) = 0.707`;
- attenuation = approximately `-3.01 dB`;
- phase = `-45 degrees`.

Important interpretation: setting `f_c = 10 kHz` would mean a genuine 10 kHz diagnostic component is already reduced to about 70.7% of its low-frequency amplitude. Therefore the desired diagnostic-band edge and the filter's -3 dB cutoff shall not automatically be treated as the same frequency.

---

## 6. Frequency-domain physical interpretation

Capacitor impedance magnitude is:

`|Z_C| = 1 / (2 pi f C)`

Therefore:

- at low frequency, capacitor impedance is large and the signal is weakly shunted to ground;
- at high frequency, capacitor impedance becomes smaller and more high-frequency content is diverted toward ground;
- increasing capacitance reduces capacitor impedance at any given nonzero frequency and therefore lowers the filter bandwidth.

Thus:

`C up -> f_c down -> stronger high-frequency attenuation`

The same filtering applies to high-frequency noise components as to high-frequency deterministic signals.

---

## 7. Noise fundamentals

### 7.1 Random noise adds by power, not direct voltage magnitude

Independent random RMS noise contributions combine by root-sum-square:

`V_total = sqrt(V_1^2 + V_2^2 + ...)`

This is why broadband RMS noise does not scale linearly with bandwidth.

### 7.2 White-noise density

For approximately flat voltage-noise density:

`e_n [V/sqrt(Hz)]`

integrated RMS noise over an ideal rectangular bandwidth `B` is:

`V_n,rms = e_n sqrt(B)`

Therefore:

`V_n,rms proportional to sqrt(B)`

Examples of the scaling law:

- bandwidth reduced by factor 2 -> RMS noise reduced by `sqrt(2)`;
- bandwidth reduced by factor 4 -> RMS noise reduced by factor 2;
- bandwidth reduced by factor 9 -> RMS noise reduced by factor 3.

This square-root relationship applies under the white-noise and independent-random-process assumptions.

---

## 8. Equivalent Noise Bandwidth of a first-order RC filter

For deterministic signal amplitude, the filter transfer magnitude is:

`|H(f)| = 1 / sqrt(1 + (f/f_c)^2)`

Noise power is proportional to voltage squared, so the power-transfer function is:

`|H(f)|^2 = 1 / (1 + (f/f_c)^2)`

For flat input noise power spectral density `S_0`, total output noise power is:

`V_n,rms^2 = S_0 integral_0^infinity |H(f)|^2 df`

Substitute:

`|H(f)|^2 = 1 / (1 + (f/f_c)^2)`

Let:

`x = f / f_c`

so:

`df = f_c dx`

Then:

`V_n,rms^2 = S_0 f_c integral_0^infinity 1/(1+x^2) dx`

Because:

`integral 1/(1+x^2) dx = atan(x)`

and:

`atan(infinity) - atan(0) = pi/2`

we obtain:

`V_n,rms^2 = S_0 (pi/2) f_c`

Therefore the first-order RC equivalent noise bandwidth is:

`ENBW = (pi/2) f_c`

or:

`ENBW ~= 1.571 f_c`

This does **not** mean signals are passed flat to `1.571 f_c`. ENBW is the width of an ideal rectangular filter that would pass the same total white-noise power as the real RC filter.

The reason `ENBW > f_c` is that a first-order RC does not stop transmission abruptly at `f_c`; frequencies above cutoff still contribute progressively attenuated noise power.

For flat voltage-noise density:

`V_n,rms = e_n sqrt((pi/2) f_c)`

---

## 9. Time-domain transient response of the same first-order low-pass

The frequency-domain and time-domain descriptions represent the same physical system.

The RC time constant is:

`tau = R C`

Because:

`f_c = 1 / (2 pi R C)`

we also have:

`tau = 1 / (2 pi f_c)`

Thus bandwidth and transient speed are directly linked:

- higher bandwidth -> smaller `tau` -> faster response;
- lower bandwidth -> larger `tau` -> slower response.

### 9.1 Step response for an initially uncharged capacitor

For a step from `0 V` to `V_S` at `t = 0`:

`V_C(t) = V_S (1 - exp(-t/tau))`

`I_C(t) = (V_S/R) exp(-t/tau)`

`V_R(t) = V_S exp(-t/tau)`

At the instant immediately after the step:

- capacitor voltage cannot jump instantaneously;
- for an initially uncharged capacitor, `V_C(0+) = 0`;
- the capacitor can therefore be approximated as a short circuit **only at that initial instant for this specific zero-initial-voltage step case**;
- current is maximum: `I_C(0+) = V_S/R`.

At DC steady state:

- capacitor current tends to zero;
- capacitor voltage tends to `V_S`;
- the capacitor is approximated as an open circuit for steady DC.

### 9.2 Settling percentages

For the charging step:

| Time | Capacitor voltage relative to final value | Current relative to initial value |
|---|---:|---:|
| `0` | 0% | 100% |
| `1 tau` | 63.2% | 36.8% |
| `2 tau` | 86.5% | 13.5% |
| `3 tau` | 95.0% | 5.0% |
| `4 tau` | 98.2% | 1.83% |
| `5 tau` | 99.33% | 0.67% |

The phrase "fully charged at 5 tau" is therefore an engineering approximation. At `5 tau` the response has reached approximately 99.3% of its final value, not mathematically 100%.

### 9.3 General capacitor-voltage continuity rule

A capacitor voltage cannot change instantaneously under finite current:

`V_C(0+) = V_C(0-)`

For more general first-order transitions:

`V_C(t) = V_final + (V_initial - V_final) exp(-t/tau)`

This form is preferred when the capacitor is not initially uncharged.

---

## 10. Stock FILTER prediction

Using:

`R_F = 1.8 kOhm`

`C_total = 1.0 nF`

we obtain:

`tau = 1.80 us`

`f_c = 88.42 kHz`

`ENBW = 138.89 kHz`

Approximate 99.3% settling time:

`5 tau = 9.0 us`

At 10 kHz:

- amplitude ratio = `0.9937`;
- amplitude remaining = `99.37%`;
- attenuation = `-0.055 dB`;
- phase = `-6.45 degrees`.

This confirms that the stock FILTER configuration has little effect on the formal 10 kHz diagnostic-band edge.

---

## 11. Candidate FILTER predictions

### 11.1 Candidate A — 2.2 nF external

Total capacitance:

`C_total = 1.0 nF + 2.2 nF = 3.2 nF`

Predicted values:

- `tau = 5.76 us`;
- `f_c = 27.63 kHz`;
- `ENBW = 43.40 kHz`;
- `5 tau = 28.8 us`.

At 10 kHz:

- amplitude ratio = `0.9403`;
- amplitude remaining = `94.03%`;
- attenuation = `-0.535 dB`;
- phase = `-19.90 degrees`.

Using the measured baseline `29.55 mV RMS` and assuming the reducible portion behaves as broadband white noise governed by this bandwidth change:

`V_n,new / V_n,stock = sqrt(f_c,new / f_c,stock)`

Predicted RMS noise:

`29.55 mV -> approximately 16.52 mV RMS`

This is the **conservative candidate**: strong theoretical noise reduction with relatively small 10 kHz amplitude loss.

### 11.2 Candidate B — 3.3 nF external

Total capacitance:

`C_total = 1.0 nF + 3.3 nF = 4.3 nF`

Predicted values:

- `tau = 7.74 us`;
- `f_c = 20.56 kHz`;
- `ENBW = 32.30 kHz`;
- `5 tau = 38.7 us`.

At 10 kHz:

- amplitude ratio = `0.8993`;
- amplitude remaining = `89.93%`;
- attenuation = `-0.922 dB`;
- phase = `-25.93 degrees`.

White-noise-only prediction from the measured `29.55 mV RMS` baseline:

`29.55 mV -> approximately 14.25 mV RMS`

This is the **more aggressive candidate**: lower theoretical noise than 2.2 nF, but with greater 10 kHz amplitude and phase impact and a slower transient response.

### 11.3 Candidate C — 4.7 nF external

Total capacitance:

`C_total = 1.0 nF + 4.7 nF = 5.7 nF`

Predicted values:

- `tau = 10.26 us`;
- `f_c = 15.51 kHz`;
- `ENBW = 24.37 kHz`;
- `5 tau = 51.3 us`.

At 10 kHz:

- amplitude ratio = `0.8405`;
- amplitude remaining = `84.05%`;
- attenuation = `-1.509 dB`;
- phase = `-32.81 degrees`.

White-noise-only prediction from the measured `29.55 mV RMS` baseline:

`29.55 mV -> approximately 12.38 mV RMS`

This candidate appears increasingly aggressive for a system whose formal diagnostic band extends to 10 kHz.

---

## 12. Consolidated candidate comparison

| External C | Total C | Predicted `f_c` | `tau` | `5 tau` | Gain @ 10 kHz | Loss @ 10 kHz | Phase @ 10 kHz | ENBW | Predicted RMS noise* |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 nF | 1.0 nF | 88.42 kHz | 1.80 us | 9.0 us | 99.37% | -0.055 dB | -6.45 deg | 138.89 kHz | 29.55 mV |
| **2.2 nF** | **3.2 nF** | **27.63 kHz** | **5.76 us** | **28.8 us** | **94.03%** | **-0.535 dB** | **-19.90 deg** | **43.40 kHz** | **16.52 mV** |
| **3.3 nF** | **4.3 nF** | **20.56 kHz** | **7.74 us** | **38.7 us** | **89.93%** | **-0.922 dB** | **-25.93 deg** | **32.30 kHz** | **14.25 mV** |
| 4.7 nF | 5.7 nF | 15.51 kHz | 10.26 us | 51.3 us | 84.05% | -1.509 dB | -32.81 deg | 24.37 kHz | 12.38 mV |

`*` Predicted RMS noise assumes the measured baseline disturbance is dominated by flat broadband noise shaped by the FILTER bandwidth. This is a hypothesis to be tested, not an established sensor specification.

---

## 13. Engineering interpretation of the tradeoff

The filter-design problem is multi-dimensional. Lowering bandwidth gives potential noise improvement but simultaneously causes:

1. greater attenuation near the 10 kHz diagnostic-band edge;
2. greater phase lag near the upper diagnostic band;
3. slower transient response and more smearing of sharp current changes.

The predicted returns also diminish as capacitance is increased.

Moving from 2.2 nF to 3.3 nF changes the white-noise prediction from approximately:

`16.52 mV -> 14.25 mV RMS`

while 10 kHz amplitude changes from:

`94.03% -> 89.93%`

Moving further from 3.3 nF to 4.7 nF only improves the white-noise prediction to approximately:

`12.38 mV RMS`

while reducing the 10 kHz amplitude further to:

`84.05%`

Thus the current pre-build interpretation is:

- `2.2 nF` = best conservative candidate;
- `3.3 nF` = best aggressive candidate;
- `4.7 nF` = useful comparison point but likely unnecessarily aggressive for the current DC-to-10-kHz requirement.

No final FILTER capacitor value is approved before measurement.

---

## 14. Transient interpretation for actuator-current signals

A real current step contains very high-frequency spectral content. A low-pass filter cannot reproduce an ideal vertical edge.

For the `3.3 nF` external candidate (`tau = 7.74 us`), a step response reaches approximately:

- 63.2% after `7.74 us`;
- 86.5% after `15.48 us`;
- 95.0% after `23.22 us`;
- 98.2% after `30.96 us`;
- 99.33% after `38.7 us`.

For the `2.2 nF` external candidate (`tau = 5.76 us`), approximate 99.3% settling occurs after `28.8 us`.

This is the time-domain expression of the same bandwidth tradeoff seen in the Bode response.

Later health-monitoring algorithms may use not only spectral amplitude but also startup or switching transients. Therefore time-domain distortion shall be considered when selecting the final sensor FILTER setting.

---

## 15. Important distinction: sensor FILTER versus final anti-alias filter

Changing the ACS724 FILTER capacitor is **not** equivalent to completing the system anti-alias design.

The sensor FILTER experiment answers:

> How much sensor/output-chain noise reduction can be obtained while preserving the required diagnostic information?

The complete acquisition design still requires coordinated selection of:

`sensor bandwidth -> analog front end -> anti-alias filter -> ADC sample rate`

The existing Rev-1 architecture targets `100 kS/s` ADC acquisition. Deliberate system-level anti-alias filtering remains a later AFE responsibility.

The ACS724 FILTER network is therefore an upstream bandwidth/noise optimization mechanism, not automatically the final anti-alias solution.

---

## 16. Pre-build wiring definition

For the upcoming zero-current FILTER experiment:

- ACS724 carrier powered from bench supply at nominal `5.00 V`;
- oscilloscope probe tip connected to `VOUT`;
- oscilloscope ground connected to sensor `GND`;
- motor disconnected;
- primary current terminals `IP+` and `IP-` left without a current path so `I_P = 0 A`;
- Arduino disconnected;
- external ceramic capacitor connected directly between the carrier's FILTER pad and nearby GND pad;
- capacitor leads kept as short as practical;
- power removed before inserting or changing the capacitor.

The external capacitor is in parallel with the stock 1 nF carrier capacitor.

---

## 17. Build/measure sequence approved for the next step

The first hardware sequence shall preserve all practical setup variables except external FILTER capacitance:

`Stock -> 2.2 nF external -> 3.3 nF external -> Stock`

The final Stock step is an A2-style return control to detect drift or accidental setup changes.

For each state, the intended measurements include:

- mean `VOUT`;
- RMS / standard deviation after mean removal;
- peak-to-peak as supporting information;
- FFT / spectral evidence;
- acquisition sample rate and duration;
- oscilloscope bandwidth setting;
- relevant VCC and wiring state.

The 10 kS/s, 1-second acquisition previously used for low-frequency motor spectra has Nyquist frequency only 5 kHz and therefore cannot characterize a 15-90 kHz FILTER response. A separate higher-sample-rate capture is required for FILTER bandwidth/noise characterization.

A practical target for the higher-bandwidth capture is approximately `>= 500 kS/s`, preferably around `1 MS/s` where the instrument/data path permits.

The existing 10 kS/s capture may still be retained as a secondary low-frequency FFT view.

---

## 18. Hypotheses to be tested during BUILD/MEASURE

### H1 — FILTER capacitance controls a meaningful part of the observed zero-current disturbance

If the approximately 30 mV RMS output disturbance contains a substantial broadband component shaped by the sensor FILTER bandwidth, adding 2.2 nF or 3.3 nF should reduce measured RMS noise significantly and the Stock return condition should move back toward the original baseline.

### H2 — White-noise square-root bandwidth prediction is only approximate

The idealized predictions of approximately:

- `16.52 mV RMS` for 2.2 nF external;
- `14.25 mV RMS` for 3.3 nF external;
- `12.38 mV RMS` for 4.7 nF external;

are not acceptance criteria. Deviations are expected if the measured disturbance contains low-frequency interference, 1/f noise, discrete spectral lines, coupling, instrument contributions, or other non-white processes.

### H3 — 2.2 nF and 3.3 nF are the most relevant candidates

The likely engineering trade is expected to lie between:

- 2.2 nF external: more conservative preservation of the 10 kHz band;
- 3.3 nF external: stronger noise reduction with larger upper-band amplitude/phase impact.

The experiment shall determine whether the additional noise benefit of 3.3 nF justifies its larger signal/transient penalty.

---

## 19. Decision gate after measurement

A final external FILTER value shall only be selected after comparing measured:

1. zero-current RMS noise reduction;
2. spectral-noise change;
3. measured or verified amplitude response through 10 kHz;
4. phase behavior where relevant;
5. transient-response implications;
6. repeatability of the Stock -> candidate -> Stock control sequence.

The final decision shall be based on the required diagnostic information content, not appearance of the oscilloscope trace.

---

## 20. Current project state

Completed before build:

- RC low-pass physical interpretation;
- capacitor impedance and AC current/voltage relationships;
- transfer-function derivation;
- cutoff, magnitude, and phase relationships;
- white-noise bandwidth scaling;
- root-sum-square noise interpretation;
- first-order RC ENBW derivation;
- transient step-response equations;
- time constant and settling interpretation;
- stock, 2.2 nF, 3.3 nF, and 4.7 nF quantitative predictions;
- candidate tradeoff assessment;
- intended zero-current build topology and controlled test sequence.

Next state:

`BUILD -> MEASURE -> VALIDATE`

No final additional ACS724 FILTER capacitance is yet accepted into the Rev-1 design baseline.

---

## References

- Allegro MicroSystems, ACS724/ACS725 current sensor datasheet.
- Pololu #4048 ACS724LLCTR-05AU current sensor carrier documentation.
- Existing project document: `docs/03-acs724-sensor-characterization.md`.
- Existing project evidence: `docs/evidence/acs724-zero-current-noise-isolation-2026-09-07.md`.
