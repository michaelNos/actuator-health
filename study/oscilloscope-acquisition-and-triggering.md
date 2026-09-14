# Oscilloscope Acquisition and Triggering

Actuator Health Monitoring System — study note, 2026-09-13.

This lesson explains the HANMATEK DOS1102S settings used during the rewired ACS724 fixture experiment. Bench observations below are provisional; the CH1 amplitude variation remains unresolved.

## Why we need acquisition

Acquisition turns changing voltages into a record of voltage versus time. The oscilloscope is already acquiring in Sample mode; switching to Average changes how repeated records are combined.

We need those records to measure the current waveform and the sensor's response at the test frequency. A steady DC reading alone cannot describe their amplitudes, timing, noise, or distortion. Averaging is an optional tool for a repeating signal, not a requirement for every measurement.

The MCP6022 creates the driven current in this fixture. Its [pinout and circuit roles](mcp6022-pinout-and-fixture.md) explain where that signal originates.

## What we are trying to measure

CH1 gives the reference current through a resistor. CH2 gives the sensor's response to that current. Use these names consistently with the [project schematic](../Schematics/actuator-health/actuator-health.kicad_sch):

| Measurement | Probe tip | Probe ground | Meaning |
| --- | --- | --- | --- |
| Scope CH1 | `CH1_IREF`, R8 top / U2 IP−, J3 pin 1 | J3 pin 2, circuit GND | Voltage across the current-reference resistor |
| Scope CH2 | `CH2_SENSOR`, U2 VIOUT, J4 pin 1; physical Pololu pad marked `OUT` | J4 pin 2 / Pololu GND | Current-sensor output voltage |

U2's schematic pin numbers are project-defined module identifiers. They are different from the bare sensor IC's pin numbers. In particular, Pololu OUT must not be confused with MCP6022 pin 7, which is the reference-buffer output.

The latest annotated schematic gives measured R8 = **67 Ω**. Thus, current variation is calculated as `Ipp = CH1 fitted Vpp / 67 Ω`.

The sensor has nominal sensitivity **0.8 V/A** and nominal zero-current output **0.5 V** at a 5 V supply. For an illustrative 7 mA peak-to-peak current, the expected sensor variation is only `0.007 × 0.8 = 0.0056 V`, or **5.6 mV peak-to-peak**. This is a prediction using nominal sensitivity, not a measured gain. [Pololu #4048 specification](https://www.pololu.com/product/4048)

Our aim is to recover this small repeating component. The approximately 0.5 V DC level and the noise spikes answer different measurement questions.

## Samples, captures, and averages

A **sample** is one voltage value at one time. A **capture** is a record containing many samples. **Acquisition mode** controls how those records are formed or combined.

The supplied `data_26_017_CH1_acq.csv` and `data_26_018_CH2_acq.csv` each contain 10,000 voltage points, spaced 10 µs apart: approximately 0.1 seconds, or ten cycles at 100 Hz. These are properties of the exported data; they do not establish the instrument's internal ADC sampling rate. Record length and sample spacing jointly determine the recorded duration. [Tektronix: record length and sample rate](https://www.tek.com/en/documents/primer/evaluating-oscilloscopes)

| Mode | What it means | Why we use it here |
| --- | --- | --- |
| Sample | Shows individual acquisitions without averaging successive captures together | Observe changes between captures and retain noise or intermittent events |
| Average, count 64 | Combines successive captures using the selected averaging depth | Try to make the small repeating CH2 signal easier to distinguish |

The number **64 concerns repeated acquisitions**, not the number of points within one acquisition.

For a simple equal-weight average, each displayed time position uses:

`average[j] = (capture1[j] + … + capture64[j]) / 64`

The signal must repeat at the same position relative to the trigger. Random contributions can cancel while the aligned signal remains. Averaging also hides intermittent behavior and removes some real signal noise, so an averaged trace cannot characterize the original noise. Instruments can use different averaging algorithms; the formula is an explanatory model, not a verified DOS1102S firmware implementation. [Teledyne LeCroy: waveform averaging](https://blog.teledynelecroy.com/2016/06/just-faqs-waveform-averaging.html)

For independent, zero-mean noise with equal variance, the equal-weight model predicts noise RMS falling as `1/√N`. With 64 records, that is ideally an eightfold reduction. Correlated noise, drift, and alignment errors can prevent this improvement. No eightfold improvement has been established for our captures.

## Why the trigger matters

A trigger defines a repeatable time reference, for example: “CH1 crosses 580 mV while rising.” This lets the scope place corresponding portions of successive cycles at the same horizontal position. [Tektronix: triggering](https://www.tek.com/en/documents/primer/evaluating-oscilloscopes)

The supplied Average-64 photograph shows CH1 as the trigger source, a rising edge, and a 580 mV level. CH1 was chosen because its reference sine is much clearer than the small CH2 signal. The level must lie within the actual waveform's voltage range.

For our averaging model, combining a sine with a delayed copy can reduce the displayed amplitude. A constant phase difference between CH1 and CH2 is acceptable; varying phase relative to the trigger is the concern. This explains a possible mechanism, not the established cause of the present CH1 variation. A `Trig` indication alone does not establish sufficiently precise alignment.

## The other settings in the photograph

The user's supplied DOS1102S photograph, `image-1789305773966.jpg`, directly confirms these selected menu labels:

| Setting | Meaning |
| --- | --- |
| `Acqu Mode: Average 64` | Repeated acquisition averaging is selected |
| `Type: Vect` | Draw connecting lines between displayed points |
| `Persist: OFF` | Do not retain older traces as a persistence overlay |
| `XY Mode: OFF` | Use the usual voltage-versus-time display |
| `Counter: OFF` | Disable the additional frequency-counter feature; the ordinary channel frequency measurement can still appear |

Vectors and persistence concern presentation. They do not smooth successive captures in the way acquisition averaging does.

**Input coupling is separate.** DC coupling allows the DC level and changing component through. AC coupling blocks DC and can attenuate sufficiently low frequencies. It does not perform acquisition averaging. See [coupling and noise fundamentals](acs724-noise-bandwidth-and-fft.md).

HANMATEK's DOS1102S guide confirms the **Acquire** button accesses acquisition modes such as averaging. The exact menu selections above come from the user's instrument photograph. The full DOS1102S manual could not be retrieved from the manufacturer's linked download during this session; unverified firmware details remain unknown. [HANMATEK DOS1102S guide](https://hanmatek.com/blogs/benchtop-cluster/hanmatek-dos1102s-review-for-beginners)

## Read the correct quantity

| Quantity | What it tells us | Limitation in this experiment |
| --- | --- | --- |
| DC voltage / mean | The waveform's average level | A steady level does not establish steady AC amplitude |
| Raw Vpp | Highest voltage minus lowest voltage in the measurement interval | Noise spikes affect both extremes |
| RMS including DC | Combined contribution of the DC level and variations | A large DC level can dominate a tiny sine |
| Fitted sine Vpp | Size of the repeating component at the fitted frequency | Requires a valid, sufficiently stable record and an assessment of fit uncertainty |

A multimeter indicating steady **0.498 V between Pololu OUT and GND** means it detects no changing DC indication under that test. It cannot establish that the 100 Hz amplitude or faster noise is constant.

CSV header measurements and exported samples also need separate checks. In the acquisition pair, the header Vpp values are 368.5 mV for CH1 and 85.75 mV for CH2. Calculating maximum minus minimum from the saved samples gives 488 mV and 224 mV respectively. That mismatch is an observation. Different processing stages or capture timing are possible explanations; neither is confirmed. We cannot assume that the export represents exactly the averaged display.

For the fitting method, see [signal-analysis concepts](../docs/study/signal-analysis-concepts-for-acs724-dynamic-validation-2026-09-11.md). Its historical numerical baseline predates the present rewiring and must not be silently reused for these measurements.

## What is established and what remains open

Latest status combines the corrected 2026-09-13 observations with the 2026-09-14 follow-up:

| Item | Latest status |
| --- | --- |
| Pololu OUT-to-GND multimeter reading | Last numerical report: steady at 0.498 V on 2026-09-13 |
| Scope CH2 level | Last numerical report: steady at approximately 498 mV on 2026-09-13 |
| Scope CH1 amplitude | At 100 Hz: Sample-step reading stable at 480 mVpp; after the Average-64 instruction, rose from about 100 to 475 mVpp and then appeared stable |
| Acquisition setting verified in a photograph | Average 64 in the earlier photograph; the latest response follows the instruction to select Average 64 again |
| Controlled Sample-versus-Average comparison | Both step responses recorded: 480 mVpp in the Sample step and approximately 475 mVpp after the averaging transient |
| Suggested CH2 tip-to-ground test | Skipped after the corrected report that CH2 was already steady |
| Cause of the earlier CH1 amplitude changes | Unresolved |
| Gain accepted from the latest acquisition pair | None |

The photos and CSV filenames identify session evidence; they are not newly archived by this study note. No hardware fault, sensor failure, or firmware defect has been established.

## Sample-step result — 2026-09-14

**Purpose:** Check whether CH1's displayed Vpp continues to vary when successive captures are not averaged together.

**Requested action:** Select Acquire → Acqu Mode → Sample, keep the wiring, generator, scales, and trigger unchanged, and watch CH1 Vpp for ten seconds.

**User observation:** CH1 Vpp was **480 mV and stable**; the user reported that nothing was moving and explicitly clarified **100 Hz**. This response follows the Sample-mode instruction. There is no new settings photograph or CSV, and the user supplied one stable value rather than a separate minimum and maximum.

**Interpretation at this step:** The earlier movement was not observed in this check. A return to Average with other conditions held fixed was therefore requested; its result follows below. This Sample-step result alone does not establish the cause of the earlier variation.

Using measured R8 = 67 Ω, the reported voltage corresponds to an indicated current swing:

`Ipp = 0.480 V / 67 Ω ≈ 7.16 mA`

This conversion uses the scope's Vpp reading; it is not a fitted sine result or a calibrated uncertainty estimate. A stable reported value does not imply zero measurement uncertainty.

## Return-to-Average result — 2026-09-14

**Purpose:** Check whether the CH1 variation returns when only averaging is enabled again.

**Requested action:** At the same 100 Hz, select Acquire → Acqu Mode → Average → 64, leaving the wiring, generator amplitude/offset, scales, and trigger unchanged. Let the display settle before assessing CH1 Vpp.

**User observation:** CH1 Vpp started at approximately **100 mV**, slowly rose to **475 mV**, and then appeared stable. The elapsed settling time and a further numerical range were not supplied. This report follows the Average-64 instruction; no new screenshot or CSV was supplied.

**Comparison:** The settled indication is 5 mV below the Sample-step reading:

`(480 − 475) / 480 × 100 ≈ 1.04%`

A small Vpp reduction is compatible with reducing noise extremes. These are scope readouts from two acquisition modes, not fitted amplitudes with quantified uncertainty.

**Explanation:** The gradual rise is consistent with the average building up or adapting after a mode change. The exact DOS1102S initialization and weighting behavior have not been verified, so this is a plausible explanation rather than a confirmed firmware mechanism. Waveform averaging can combine successive records with different weighting schemes; see the [Teledyne LeCroy explanation](https://blog.teledynelecroy.com/2016/06/just-faqs-waveform-averaging.html).

For a steady repeating signal, judge the amplitude after the averaging transient has settled. The reported settled amplitude is close to the Sample result. Persistent variation was not reported after settling in this comparison; the cause of all earlier movement is not established.

## The next observation, with its purpose

**Question:** What does CH2's Vpp readout show now that the reference amplitude has settled?

**Prediction:** Using the indicated CH1 amplitude and measured R8:

`Ipp ≈ 0.475 V / 67 Ω ≈ 7.09 mA`

At the sensor's nominal 0.8 V/A sensitivity, the expected repeating sensor component is:

`CH2 sine Vpp ≈ 0.00709 A × 0.8 V/A ≈ 5.67 mV`

This is a nominal prediction based on an indicated reference amplitude. CH2's raw Vpp includes remaining noise and may be larger; it must not be treated as the sine amplitude or used directly to accept a sensor gain.

**One action:** Keep 100 Hz, Average 64, and the existing connections/settings. With the display settled, observe **CH2 Vpp** for ten seconds.

**Report:** Give CH2 Vpp and whether it stays stable; if it varies, give its lowest and highest readouts. The approximately 0.498 V DC level is a different quantity.

**Interpret before proceeding:** This CH2 observation is pending. It will describe the displayed excursion; verifying a repeatable sensor sine amplitude still requires appropriate waveform analysis.
