# Lab Measurement and Breadboard Notes

This note collects learning material that is useful for understanding the project bench work but is broader than the formal engineering baseline.

## Breadboard connectivity

A standard solderless breadboard does **not** connect every nearby hole together.

For the board currently used in this project:

- holes `a–e` on one numbered row form one connected node
- holes `f–j` on the same numbered row form a second connected node
- the center trench isolates those two groups
- row `5` is electrically separate from row `6`
- the red/blue power rails are separate conductors and must be connected explicitly to the circuit

Example:

`f5, g5, h5, i5, j5` are connected together.

But:

`e5` is not connected to `f5`, and `j5` is not connected to `j6`.

### Practical rule

When connecting a module with several adjacent pins:

1. identify the exact module pin label
2. identify the exact breadboard coordinate containing that pin
3. connect only one new wire
4. verify the node
5. only then add the next wire
6. apply power only after checking that supply and ground are not accidentally on the same node

This is slower than guessing from wire colors, but much safer and more repeatable.

---

## Why a square PCB pad may appear on GND

PCB pad shape can be used as an orientation/reference convention. A square pad does not automatically imply a different electrical behavior.

On the ACS724 carrier, the printed labels `OUT`, `VCC`, and `GND` define the signal functions. The square shape of a pad is an assembly/orientation aid rather than an additional electrical function.

---

## Raw measurement vs corrected value

A very important measurement rule is:

**record what the instrument actually displayed before applying any correction.**

Example from the current bench work:

- bench PSU set/display: `5.00 V`
- VC830L multimeter indication across the PSU output: approximately `4.8–4.9 V`

This does **not** prove that the multimeter has a fixed −0.1 to −0.2 V error.

Possible contributors include:

- multimeter accuracy and resolution
- PSU display accuracy
- probe/contact resistance or unstable probe contact
- instrument calibration state
- supply/load conditions

Therefore the correct notation is:

`PSU displayed 5.00 V; multimeter indicated 4.8–4.9 V under the stated test condition.`

It is not yet justified to write:

`multimeter error = −0.15 V`

unless a trusted reference or formal calibration establishes that.

---

## Instrument cross-checking

When a measurement seems suspicious, isolate the measurement chain.

The useful reasoning pattern is:

1. measure the unknown system
2. observe unexpected result
3. remove possible causes one at a time
4. measure a simpler/reference condition
5. compare

This was used twice in the project already:

### PSU transient example

A slow motor-terminal voltage rise was observed during PSU switch-on. Repeating the same capture with the motor disconnected showed a similar rise.

Therefore the observed ramp was attributed primarily to PSU output turn-on behavior rather than directly to motor acceleration.

### Arduino 5 V measurement example

The ACS724 supply appeared low. Measurement was moved from the ACS724/breadboard back to the Arduino `5V` and `GND` pins. The reading remained approximately 4.5 V, showing that the breadboard alone could not explain the observation.

A further comparison against a bench PSU set to 5.00 V produced a multimeter indication of approximately 4.8–4.9 V, showing that instrument/reference uncertainty must also be considered.

---

## Current sensor offset and sensitivity

For a current sensor with nominal transfer relation

`V_OUT = V_ZERO + S·I`

where:

- `V_ZERO` is zero-current output
- `S` is sensitivity in volts per ampere
- `I` is measured current

current can be estimated from:

`I = (V_OUT - V_ZERO) / S`

For the Pololu #4048 ACS724LLCTR-05AU at nominal 5 V operation:

- nominal `V_ZERO ≈ 0.5 V`
- nominal `S ≈ 0.8 V/A`

For an expected 35 mA motor current:

`ΔV ≈ 0.8 × 0.035 = 0.028 V = 28 mV`

This demonstrates why stable contacts, instrument resolution, noise characterization, and proper analog acquisition matter: the useful DC change in the first low-current motor test is only a few tens of millivolts.

---

## Measurement lesson: display value is not always transient truth

The bench PSU displayed roughly 60–75 mA during motor startup and approximately 35–36 mA during steady running.

The steady value is useful as a low-bandwidth reference. The startup indication is not a reliable instantaneous peak measurement because the display update rate is much slower than the underlying electrical transient.

This is why the ACS724 plus oscilloscope is required for startup-current waveform characterization.

---

## Review questions

**Front:** Why are `f5` and `j5` connected on the breadboard but `e5` and `f5` are not?  
**Back:** Each numbered row is split by the center trench into two independent five-hole nodes: `a–e` and `f–j`.

**Front:** Why should raw instrument readings be stored before applying corrections?  
**Back:** Because any correction depends on assumptions about instrument/reference error. Preserving the raw result allows later reinterpretation when calibration or uncertainty becomes known.

**Front:** If the ACS724 sensitivity is 0.8 V/A, what output change corresponds to 35 mA?  
**Back:** `0.8 × 0.035 = 0.028 V`, or 28 mV.

**Front:** Why is a PSU current display insufficient for measuring motor startup peak current?  
**Back:** The display is updated much more slowly than the electrical transient and can average or miss the true peak.

**Front:** What is the general troubleshooting pattern when a measurement looks wrong?  
**Back:** Isolate the chain, remove possible causes one at a time, measure a simpler/reference condition, and compare results.
