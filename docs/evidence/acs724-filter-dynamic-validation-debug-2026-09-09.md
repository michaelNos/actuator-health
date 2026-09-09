# ACS724 FILTER dynamic-validation debugging and positive-bias redesign — 2026-09-09

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — implementation / sensor FILTER validation  
**Status:** Dynamic test method corrected; previous zero-centered AC stimulus is not accepted as formal ACS724-05AU validation. Positive-biased excitation is designed below and must be validated before the frequency sweep continues.

## 1. Purpose

This record captures the controlled debugging performed while preparing dynamic ACS724 FILTER verification and defines the corrected next test architecture.

The engineering objective remains unchanged:

- preserve the formal **DC–10 kHz diagnostic band**;
- quantify the signal/noise tradeoff of the ACS724 FILTER capacitor;
- compare the stock carrier with candidate external FILTER capacitors;
- do not accept any FILTER value until dynamic response is verified with a valid primary-current stimulus.

The existing design baseline already requires the ACS724LLCTR-05AU to be used within its specified **0 A to 5 A unidirectional range** and states that a periodic stimulus must remain positive (`IDC > IAC`).

## 2. Verified hardware facts used here

### Pololu #4048 / ACS724LLCTR-05AU

Manufacturer documentation establishes:

- exact device: ACS724LLCTR-05AU on Pololu #4048;
- valid primary-current range: **0 A to 5 A, unidirectional**;
- nominal sensitivity at 5 V: **0.8 V/A**;
- nominal zero-current output at 5 V: **0.5 V**;
- primary-conductor resistance: approximately **1.2 mΩ**;
- bare sensor bandwidth: approximately **120 kHz**;
- Pololu carrier stock FILTER capacitor: **1 nF**;
- stock carrier bandwidth: approximately **90 kHz**.

Reference: https://www.pololu.com/product/4048

### HANMATEK DOS1102S

Manufacturer documentation establishes for the built-in arbitrary/function generator:

- sine range: **0.1 Hz to 10 MHz**;
- amplitude specification: **0.25 Vpp to 2.5 Vpp at 50 Ω**;
- output impedance: **50 Ω**.

The oscilloscope channels are not electrically isolated and shall use a common measurement ground.

References:

- https://hanmatek.com/products/hanmatek-dos1102s-oszilloskop-wellenformgenerator
- DOS1102/DOS1102S manual / quick guide used during bench work.

### Jesverty SPS-3010V

The bench supply supports adjustable voltage/current limit and an explicit OUT control. The corrected bias procedure below therefore sets voltage and current limit before output enable.

Reference: Jesverty SPS-3010V manufacturer manual.

## 3. Existing FILTER/noise evidence

Controlled zero-primary-current tests were already completed with the same ACS724 carrier and scope method.

Measured VOUT standard deviation:

| FILTER configuration | Measured VOUT sigma |
|---|---:|
| Stock 1 nF | 32.52 mV |
| +2.2 nF external | 22.50 mV |
| +3.3 nF external | 18.66 mV |
| +4.7 nF external | 16.31 mV |
| Stock restored | 31.74 mV |

Established conclusion:

**Increasing FILTER capacitance materially reduces the measured zero-current VOUT disturbance.**

The final capacitor is not yet approved because dynamic-band preservation still requires validation.

## 4. Dynamic-test current reference

The characterized current-reference resistor is:

`RREF = 68.8 ohm`

Fixed channel convention:

- `CH1 = voltage across RREF`;
- `CH2 = ACS724 VOUT`.

Primary current is therefore derived from the measured resistor voltage, not from the generator setting:

`I(t) = VCH1(t) / 68.8 ohm`

For coherent sinusoidal analysis:

`Ipp = VCH1,pp / 68.8 ohm`

## 5. Wiring fault found and corrected

During troubleshooting, the primary loop initially showed an open circuit even though the physical cable appeared connected.

After the connection was repaired, the user verified the complete primary path with power removed:

- resistor itself: approximately **68 ohm**;
- `IP+ <-> IP-`: approximately **0 ohm / continuity**, consistent with the sensor's very low primary resistance;
- complete intended path through the reference resistor: approximately **68.8 ohm**.

This established that the later measurements were performed with a physically continuous primary-current path.

## 6. Scope-channel scaling cross-check

Before interpreting the sensor gain anomaly, both scope probes were placed on the same resistor node.

Measured coherent 1 kHz amplitudes:

- CH1: approximately **1.97118 Vpp**;
- CH2: approximately **1.97355 Vpp**.

Amplitude ratio:

`CH2 / CH1 ~= 1.0012`

Conclusion:

**CH1/CH2 amplitude scaling agrees to about 0.12%. Scope-channel gain mismatch does not explain the later ACS724 VOUT anomaly.**

## 7. Corrected closed-loop 1 kHz measurement

Files:

- `stock_1k_fixed_CH1.txt`
- `stock_1k_fixed_CH2.txt`

Acquisition facts:

- 10,000 samples;
- 2 us sample interval;
- 20 ms record;
- coherent least-squares fit evaluated exactly at 1 kHz.

### CH1 current reference

Coherent 1 kHz:

`VCH1,pp = 1.1271978 V`

Therefore:

`Ipp = 1.1271978 / 68.8 = 16.3837 mApp`

### CH2 sensor output

Coherent 1 kHz:

`VOUT,pp = 40.4492 mVpp`

Mean:

`VOUT,mean ~= 0.50205 V`

Residual broadband variation:

`~24.47 mV RMS`

Using the previously measured DC sensitivity:

`Smeas = 0.74472 V/A`

Expected coherent VOUT amplitude would be:

`16.3837 mA x 0.74472 V/A = 12.201 mVpp`

Observed apparent AC gain would be:

`40.449 mV / 16.3837 mA = 2.469 V/A`

This is inconsistent with the measured DC sensitivity and shall **not** be accepted as ACS724 frequency-response evidence.

## 8. Controlled checks of possible measurement error

### 8.1 Open-primary-loop control

File:

`fixed_openloop_1k_CH2.csv`

With the corrected circuit otherwise unchanged, the primary loop was opened so no intended primary current flowed.

Coherent 1 kHz VOUT component:

`2.534 mVpp`

Relative reduction from the corrected closed-loop 1 kHz result:

`1 - 2.534 / 40.449 ~= 93.7%`

Conclusion:

**The large coherent 1 kHz VOUT component is strongly associated with closure of the primary-current loop; it is not explained by simple open-loop generator pickup.**

### 8.2 Local-ground movement check

File:

`groundcheck_1k_CH2.txt`

CH2 measured ACS724 local GND relative to the common measurement ground.

Coherent 1 kHz component:

`~1.962 mVpp`

Conclusion:

Local ground movement is present at a small level but is far too small to explain the approximately 40.45 mVpp VOUT component.

### 8.3 VCC-ripple check

File:

`vcccheck_1k_CH2.txt`

CH2 measured ACS724 VCC ripple with AC coupling.

Coherent 1 kHz VCC component:

`~18.081 mVpp`

The 05AU zero point is nominally `VCC / 10`, so the corresponding first-order zero-point contribution is approximately:

`18.081 mVpp / 10 = 1.808 mVpp`

Conclusion:

Supply ripple can contribute to VOUT but is far too small to explain the approximately 40.45 mVpp coherent VOUT result.

## 9. Corrected 100 Hz trial and validity problem

Files:

- `stock_100Hz_CH1last.csv`
- `stock_100Hz_CH2last.csv`

The earlier 100 kHz selection error was corrected; these files are from the intended **100 Hz** trial.

### CH1

Coherent 100 Hz:

`VCH1,pp = 1.1508919 V`

Therefore:

`Ipp = 1.1508919 / 68.8 = 16.7281 mApp`

### CH2

Coherent 100 Hz:

`VOUT,pp = 90.2917 mVpp`

The CH2 exported mean is near 0 V, consistent with CH2 still being AC-coupled from the preceding supply-ripple check. This prevents use of the file's DC level, but it does not by itself justify the very large coherent 100 Hz amplitude.

More importantly, the excitation architecture itself is invalid for formal 05AU verification:

- the DOS1102S generator has no usable DC-offset control in the actual instrument configuration used on the bench;
- the generator sine was centered around zero;
- the resulting primary current therefore changed sign every half-cycle;
- the ACS724LLCTR-05AU is specified for **0 A to 5 A unidirectional current**.

For approximately 16.7 mApp sinusoidal current centered at zero, the primary-current extrema are approximately:

`-8.36 mA to +8.36 mA`

The negative half-cycle is outside the sensor's specified valid range.

## 10. Engineering decision

The zero-centered AFG dynamic test is **stopped**.

The 100 Hz and 1 kHz closed-loop observations are retained as troubleshooting evidence, but their apparent V/A gain values are **not accepted as sensor transfer-function measurements** and shall not be used to approve or reject a FILTER capacitor.

Before the frequency sweep continues, the primary stimulus shall be redesigned so that:

`IDC > IAC,peak`

and the current remains positive for the entire waveform.

A bench PSU and AFG output shall **not** be directly paralleled.

## 11. Positive-biased excitation — pre-build design

### 11.1 Proposed parts

Existing characterized part:

- `RREF = 68.8 ohm`.

Proposed new parts:

- `RBIAS = 180 ohm`, >= 0.25 W;
- `RINJ = 100 ohm`, >= 0.25 W;
- `CCOUPLE = 100 uF` electrolytic, rated >= 10 V.

Do not substitute different values without recalculation.

### 11.2 Proposed topology

Common ground:

`PSU- = AFG GND = RREF low side = CH1 ground = CH2 ground = ACS724 GND`

Sensor supply:

`PSU +5 V -> ACS724 VCC`

DC primary-current bias:

`PSU +5 V -> RBIAS 180 ohm -> IP+ -> IP- -> RREF 68.8 ohm -> common GND`

AC injection:

`AFG OUT -> RINJ 100 ohm -> CCOUPLE 100 uF -> IP+`

For the polarized coupling capacitor:

- capacitor **positive** terminal -> IP+ side;
- capacitor **negative** terminal -> AFG / RINJ side.

Reason: with the designed DC bias, IP+ sits at a positive DC voltage while the AFG side has approximately zero DC offset.

Oscilloscope:

- CH1 tip -> `IP- / top of RREF`;
- CH1 ground -> common GND;
- CH2 tip -> `ACS724 VOUT`;
- CH2 ground -> common GND;
- CH1 coupling -> **DC**;
- CH2 coupling -> **DC**.

### 11.3 DC prediction

Ignoring the approximately 1.2 mOhm primary resistance relative to the resistor values:

`IDC ~= 5.00 V / (180 + 68.8) ohm`

`IDC ~= 20.10 mA`

Predicted DC voltage across RREF:

`VREF,DC = 20.10 mA x 68.8 ohm ~= 1.383 V`

Using the measured calibration model:

`VOUT = 0.46910 + 0.74472 x I`

predicted sensor output near the DC-bias point is:

`VOUT,DC ~= 0.4841 V`

Predicted resistor dissipation:

- `PRBIAS ~= 73 mW`;
- `PRREF,DC ~= 28 mW`.

0.25 W resistors therefore provide substantial margin for this low-current test.

### 11.4 AC target

Target coherent AC primary current:

`IAC,pp ~= 16 mApp`

Equivalent CH1 target:

`VCH1,pp = 68.8 ohm x 16 mA ~= 1.10 Vpp`

This corresponds to approximately:

`IAC,peak ~= 8 mA`

With the predicted 20.10 mA DC bias:

- minimum current ~= `20.10 - 8 = 12.10 mA`;
- maximum current ~= `20.10 + 8 = 28.10 mA`.

The complete stimulus therefore remains positive and comfortably inside the 0–5 A specified range.

Predicted RREF voltage extrema:

- minimum ~= `12.10 mA x 68.8 ohm = 0.832 V`;
- maximum ~= `28.10 mA x 68.8 ohm = 1.933 V`.

### 11.5 Coupling-network prediction

At small signal, the approximate load seen from IP+ is:

`RLOAD ~= 180 ohm || 68.8 ohm ~= 49.7 ohm`

Using the documented 50 ohm AFG output impedance and the proposed 100 ohm series injection resistor, the total resistance relevant to the coupling-capacitor high-pass corner is approximately:

`50 + 100 + 49.7 ~= 199.7 ohm`

For `CCOUPLE = 100 uF`:

`fc ~= 1 / (2*pi*199.7*100 uF) ~= 8.0 Hz`

Therefore the coupling network should be essentially settled by 100 Hz and above. Exact primary-current amplitude is still measured from CH1 at every test frequency, so the test does not depend on ideal PSU or generator source models.

## 12. Exact next execution sequence

### Gate A — component verification with all outputs OFF

1. Keep Jesverty **OUT OFF**.
2. Keep AFG **output OFF**.
3. Disconnect power before resistance checks.
4. Measure and record the actual `RBIAS` resistor value; target approximately 180 ohm.
5. Measure and record the actual `RINJ` resistor value; target approximately 100 ohm.
6. Reconfirm `RREF`; current characterized value is 68.8 ohm.
7. Confirm coupling-capacitor value **100 uF or larger** and voltage rating **>= 10 V**.
8. Confirm capacitor polarity before installation.

If the available values differ materially, stop and recalculate before power is applied.

### Gate B — build the DC-bias path only

With AFG still disconnected from the injection branch:

1. Connect PSU- to common GND.
2. Connect PSU +5 V to ACS724 VCC.
3. Connect ACS724 GND to common GND.
4. Connect PSU +5 V -> `RBIAS` -> `IP+`.
5. Connect `IP-` -> `RREF` -> common GND.
6. Connect CH1 tip to `IP- / RREF-high`.
7. Connect CH1 ground to common GND.
8. Connect CH2 tip to ACS724 VOUT.
9. Connect CH2 ground to common GND.
10. Set both scope channels to **DC coupling**.

### Gate C — power the DC bias

1. On the SPS-3010V, with OUT still OFF, set **5.00 V**.
2. Set current limit to **0.10 A**.
3. Enable PSU OUT.
4. Confirm the supply remains in normal CV operation and no unexpected current draw occurs.
5. Measure CH1 DC level.
6. Calculate actual bias current:

   `IDC = VCH1,DC / 68.8 ohm`

7. Expected result for 180 ohm RBIAS is approximately **20 mA**.
8. Confirm CH1 is approximately **1.38 V DC**.
9. Confirm CH2 DC baseline is physically plausible, approximately **0.48–0.50 V** under this low positive current.
10. If CH1 is near 0 V, unexpectedly high, or the PSU enters current limiting, disable OUT and troubleshoot before continuing.

### Gate D — add the AC injection branch

With PSU OUT OFF and AFG output OFF:

1. Connect AFG ground to common GND.
2. Connect AFG OUT -> `RINJ 100 ohm`.
3. Connect RINJ -> negative terminal of `CCOUPLE`.
4. Connect positive terminal of `CCOUPLE` -> `IP+`.
5. Recheck polarity: **capacitor + toward IP+**, **capacitor - toward AFG**.
6. Re-enable PSU OUT and reconfirm the DC-bias measurements before enabling AFG.

### Gate E — establish a valid 100 Hz biased sine

1. Set AFG waveform to **sine**.
2. Set frequency to **100 Hz**.
3. Start at the DOS1102S documented minimum amplitude, **0.25 Vpp**.
4. Enable AFG output.
5. Observe CH1.
6. Increase AFG amplitude gradually while monitoring the actual CH1 waveform.
7. Target CH1 AC peak-to-peak amplitude approximately **1.10 Vpp**.
8. Keep the CH1 DC baseline near the previously measured approximately 1.38 V.
9. Verify the full CH1 waveform remains above 0 V for the complete cycle.
10. Record actual CH1 minimum and maximum voltage and derive:

   `Imin = VCH1,min / 68.8 ohm`

   `Imax = VCH1,max / 68.8 ohm`

11. Do **not** continue unless `Imin > 0 A`.
12. Confirm CH2 is still **DC-coupled** and its mean remains near the expected approximately 0.48–0.50 V operating point rather than near 0 V.

### Gate F — first valid synchronized acquisition

At valid 100 Hz positive-biased operation:

1. Allow the waveform to stabilize.
2. Capture approximately 10–20 cycles.
3. Press **Run/Stop** before export.
4. Export CH1.
5. Without resuming acquisition, switch export source and export CH2.
6. Use filenames:

   - `bias_stock_100Hz_CH1.csv`
   - `bias_stock_100Hz_CH2.csv`

7. Resume only after both files are saved.
8. Verify CSV headers before analysis.

### Gate G — analysis of the first valid point

From the same stopped record:

1. Fit CH1 coherently at exactly 100 Hz.
2. Calculate:

   `IAC,pp = VCH1,AC,pp / 68.8 ohm`

3. Fit CH2 coherently at exactly 100 Hz.
4. Calculate sensor AC gain:

   `G100 = VOUT,AC,pp / IAC,pp`

5. Compare `G100` with the measured DC sensitivity `0.74472 V/A`.
6. Do not require exact equality, but the result must be physically plausible and repeatable before proceeding.
7. Repeat the same 100 Hz capture once to establish repeatability.

## 13. Frequency-sweep sequence after Gate G passes

Only after the biased 100 Hz result is trustworthy:

### Formal diagnostic-band points

Use the same positive-biased topology at:

- 100 Hz;
- 1 kHz;
- 2 kHz;
- 5 kHz;
- 10 kHz.

At every point:

- CH1 remains the actual current reference;
- CH2 remains VOUT;
- both channels remain DC-coupled unless a deliberate documented exception is made;
- current must remain positive for the whole cycle;
- save CH1 and CH2 from the same stopped acquisition;
- calculate coherent gain from actual measured current.

Normalize each configuration to its own low-frequency reference:

`Hnorm(f) = G(f) / G(100 Hz)`

`HdB(f) = 20 log10(Hnorm(f))`

### Candidate FILTER comparison

After the stock configuration is established, repeat the formal points for the selected external candidates, beginning with **+3.3 nF**, because the pre-build analysis identified it as the strongest current compromise candidate.

Existing prediction for +3.3 nF external FILTER:

- total FILTER capacitance approximately 4.3 nF;
- ideal first-order cutoff approximately 20.56 kHz;
- predicted 10 kHz magnitude approximately 0.899;
- predicted 10 kHz attenuation approximately -0.92 dB.

The zero-current noise result for +3.3 nF was approximately 18.66 mV sigma versus approximately 32 mV stock.

The capacitor is approved only if the measured dynamic response confirms acceptable preservation of the DC–10 kHz diagnostic band.

### Educational extended sweep

After formal 10 kHz verification, optional points may extend toward the stock carrier bandwidth, for example:

- 15 kHz;
- 20 kHz;
- 30 kHz;
- 50 kHz;
- 80 kHz;
- 100 kHz.

This extended sweep is educational/characterization evidence and is not required for the formal 10 kHz system acceptance band.

## 14. Current engineering status

Established:

- zero-current FILTER capacitance reduces measured VOUT noise;
- RREF is characterized at 68.8 ohm;
- scope-channel amplitude scaling is matched;
- primary-path wiring fault was found and corrected;
- local ground bounce and VCC ripple are too small to explain the anomalous zero-centered AC VOUT gain;
- open-primary-loop control removes most of the coherent 1 kHz VOUT component;
- the zero-centered AC stimulus violates the 05AU unidirectional validity requirement and is therefore retired.

Not established:

- valid ACS724 AC gain at 100 Hz or 1 kHz;
- valid stock FILTER transfer curve;
- measured -3 dB point;
- final external FILTER capacitor;
- final explanation for the anomalous zero-centered-sine response.

Immediate next task:

**Build and validate the positive-biased AC current excitation above, starting with the DC-only bias gate and then one valid synchronized 100 Hz measurement.**
