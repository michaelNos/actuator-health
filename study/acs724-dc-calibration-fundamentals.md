# ACS724 DC Calibration Fundamentals

This note explains the learning behind the Stage B ACS724 resistive-load calibration. The formal engineering result is recorded in `docs/16-acs724-dc-calibration.md`.

## Why use resistors instead of the motor first?

A motor is a dynamic electromechanical load. Its current depends on winding resistance, back-EMF, speed, mechanical load, commutation, startup state, and PSU behavior.

A resistor is much simpler:

`I = V / R`

If voltage and resistance are known, current can be predicted before the circuit is powered. This makes a resistor load useful for checking whether the current sensor behaves correctly.

## Why three 56 Ω resistors in parallel?

One 56 Ω resistor at 3 V draws approximately:

`I = 3 / 56 = 53.6 mA`

Three identical resistors in parallel have:

`R_eq = 56 / 3 = 18.67 Ω`

so total current becomes approximately:

`I = 3 / 18.67 = 161 mA`

The sensor output shift becomes easier to observe because the ACS724 output change is approximately proportional to current.

The important idea is:

**More parallel branches reduce equivalent resistance, therefore the source supplies more total current.**

This is different from series connection, where equivalent resistance increases.

## Why not use one low-value resistor?

A single low-value resistor may dissipate too much power.

For a resistor:

`P = V² / R`

For 15 Ω at 3 V:

`P = 9 / 15 = 0.6 W`

A 1/4 W resistor would be overloaded.

Using several higher-value resistors in parallel shares the total power among branches.

For each 56 Ω resistor at 3 V:

`P = 9 / 56 = 0.161 W`

which is below the 0.25 W resistor rating.

## Why does each parallel resistor see the full 3 V?

All three resistor left ends are connected to one common node and all three right ends are connected to the other common node.

Therefore each resistor is connected across the same two electrical potentials.

That means every branch sees the same voltage:

`V1 = V2 = V3 = 3 V`

The branch currents add:

`I_total = I1 + I2 + I3`

For identical resistors the currents are approximately equal.

## Why did the measured resistance equal 18.8 Ω?

Three ideal 56 Ω resistors in parallel give:

`56 / 3 = 18.67 Ω`

The measured network resistance was 18.8 Ω.

The difference can come from resistor tolerance, multimeter accuracy, probe/contact resistance, and rounding. The measured result is very close to expectation and confirmed that all three resistors were actually connected in parallel.

## Understanding the ACS724 transfer

A simplified current-sensor model is:

`VOUT = V0 + S·I`

where:

- `V0` = zero-current output voltage
- `S` = sensitivity in volts per ampere
- `I` = measured current

If current increases and the sensor is used in its intended direction, `VOUT` should increase approximately linearly.

For this calibration the measured fit was:

`VOUT = 0.46910 + 0.74472·I`

Therefore:

- measured zero-current intercept ≈ 0.469 V
- measured sensitivity ≈ 0.745 V/A

To convert voltage back to current:

`I = (VOUT - 0.46910) / 0.74472`

## What does sensitivity mean?

Sensitivity tells us how much sensor output voltage changes for each ampere of current.

For example:

`S = 0.745 V/A`

means that an increase of 1 A would ideally increase the sensor output by about 0.745 V under the same calibration condition.

For 0.1 A:

`ΔV ≈ 0.745 × 0.1 = 0.0745 V`

or about 74.5 mV.

## What does R² mean here?

The measured calibration gave:

`R² ≈ 0.999997`

R² describes how closely the measured data follow the fitted straight-line model.

A value very close to 1 means the five measured points lie extremely close to a straight line over the tested current range.

It does **not** mean the sensor is 99.9997% accurate.

Linearity and absolute accuracy are different concepts.

The entire line could, for example, have the wrong slope but still have an R² extremely close to 1.

## Why was the measured sensitivity lower than the nominal 0.8 V/A?

The nominal value was used as a design prediction, but the bench fit gave approximately 0.745 V/A.

That difference can come from several sources:

- supply voltage not exactly 5 V
- sensor gain tolerance
- sensor temperature
- PSU current indication uncertainty
- multimeter voltage indication uncertainty
- resistor tolerance and heating
- contact/wiring effects

One calibration run cannot identify the contribution of each source.

## Why did OUT-to-VCC show about -4.07 V?

A voltmeter measures:

`V_red - V_black`

It does not measure an absolute voltage at one point.

When red was on `OUT` and black was accidentally on `VCC`:

`V_meter = VOUT - VCC`

With approximately 0.58 V at OUT and 4.65 V at VCC:

`0.58 - 4.65 ≈ -4.07 V`

The meter was therefore behaving correctly; the reference node was wrong for the intended measurement.

This is why measurements should always state both nodes, e.g.:

`VOUT-to-GND = 0.586 V`

## What does the PSU current limit do?

In normal constant-voltage operation the PSU tries to maintain the configured voltage.

If the load attempts to draw more current than the configured current limit, the PSU should reduce its output voltage to keep current near the limit.

This protects the circuit, but it is not perfect protection against every wiring mistake.

Correct connection, component ratings, and unpowered continuity checks remain necessary.

## Human electrical safety versus component safety

At the 3–5 V DC levels used in this experiment, electric-shock risk through normal intact skin is very low.

The more relevant bench hazards are:

- short-circuit current
- overheated components
- overheated wires or clips
- damaged USB ports
- accidental connection of the sensor high-current path to logic power

The safe-current question for components therefore depends on the ratings of each component and wire, not on one universal current number.

## Review questions

**Q:** What happens to equivalent resistance when identical resistors are added in parallel?  
**A:** It decreases; for N identical resistors, `R_eq = R/N`.

**Q:** Why did three 56 Ω resistors draw about three times the current of one 56 Ω resistor at the same supply voltage?  
**A:** Each resistor receives the full supply voltage and contributes its own branch current; the branch currents add.

**Q:** Why was resistor power checked before applying voltage?  
**A:** To verify that the selected resistor would not exceed its power rating.

**Q:** What is the simplified ACS724 DC transfer equation?  
**A:** `VOUT = V0 + S·I`.

**Q:** Does R² close to 1 prove absolute accuracy?  
**A:** No. It demonstrates linearity relative to the fitted model, not absolute accuracy.

**Q:** Why must a voltage measurement name its reference node?  
**A:** A voltmeter always measures potential difference between two points.

**Q:** What is the practical calibration equation obtained in this experiment?  
**A:** `I = (VOUT - 0.46910) / 0.74472`, with voltage in volts and current in amperes, valid as the present low-current bench calibration.
