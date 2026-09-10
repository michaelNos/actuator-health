# MCP6022 channel-A unloaded dynamic validation — 2026-09-10

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — ACS724 dynamic/FILTER validation fixture  
**Status:** Channel-A DC operating point and unloaded 100 Hz level-shifting behavior demonstrated; loaded-driver validation still required before ACS724 connection.

## 1. Purpose

This record captures the first successful dynamic validation of MCP6022 channel A in the temporary positive-bias stimulus fixture.

The fixture is being developed so the zero-centered DOS1102S AFG sine can be shifted upward before driving the ACS724LLCTR-05AU primary path. The ACS724-05AU is a 0 A to 5 A unidirectional device, so the formal stimulus must remain positive for the complete cycle.

The target channel-A relation for matched resistors is:

`VOUT ~= 2*VREF_BUF - VAFG`

The expected behavior is therefore an inverted sine with approximately unity AC magnitude, but with a positive DC center near `2*VREF_BUF`.

This is a temporary Stage B test fixture, not the frozen Rev-1 anti-alias AFE.

## 2. Relevant hardware facts

MCP6022-I/P pin assignment used here:

- pin 1 = `OUTA`;
- pin 2 = `-INA`;
- pin 3 = `+INA`;
- pin 4 = `VSS`;
- pin 5 = `+INB`;
- pin 6 = `-INB`;
- pin 7 = `OUTB`;
- pin 8 = `VDD`.

Manufacturer datasheet: https://www.microchip.com/content/dam/mchp/documents/APID/ProductDocuments/DataSheets/20001685E.pdf

Verified bench supply at MCP6022 pins 8-to-4: **4.99 V**.

Channel-B buffered reference previously measured at pin 7: approximately **1.242 to 1.245 V**.

## 3. Channel-A resistor pair

Two nominal 100 kOhm resistors were selected and measured:

- `RIN = 99.1 kOhm`;
- `RF = 99.0 kOhm`.

Measured ratio:

`RF/RIN ~= 0.999`

This is sufficiently close to unity for the intended inverting level-shift relation.

## 4. Channel-A connection architecture

The successful channel-A arrangement is:

1. MCP6022 pin 3 (`+INA`) -> channel-B buffered reference, pin 7 (`VREF_BUF`).
2. MCP6022 pin 2 (`-INA`) -> junction of `RIN` and `RF`.
3. `RF = 99.0 kOhm` -> between pin 1 (`OUTA`) and pin 2 (`-INA`).
4. `RIN = 99.1 kOhm` -> between pin 2 and the signal-input node.
5. For the DC-only test, the signal-input end of `RIN` was connected to common GND.
6. For the dynamic test, the signal-input end of `RIN` was connected to DOS1102S AFG OUT.
7. AFG GND -> the same common GND as MCP6022 pin 4.
8. The ACS724 primary-current load remained disconnected from MCP6022 pin 1 during this validation.

## 5. Why the circuit produces about 2.49 V at zero signal

Negative feedback forces pin 2 to remain close to pin 3:

`V- ~= V+ ~= VREF_BUF`

With `VREF_BUF ~= 1.245 V` and the far side of `RIN` at 0 V, approximately:

`IRIN ~= 1.245 V / 99.1 kOhm ~= 12.6 uA`

Because the MCP6022 input current is tiny compared with this resistor current, nearly the same current flows through `RF`.

The output therefore rises above pin 2 by approximately another 1.24 V, giving:

`VOUT ~= 2.49 V`

This was measured directly at physical MCP6022 pin 1:

**pin 1 = 2.49 V**

Measured pin 3 was approximately:

**pin 3 = 1.24 V**

Result: **PASS for channel-A DC operating point.**

## 6. Unloaded 100 Hz dynamic measurement

The DOS1102S AFG was connected through `RIN`, with common ground maintained. The ACS724 load was still disconnected.

Oscilloscope convention for this validation:

- CH1 = actual AFG-input node at the free side of `RIN`;
- CH2 = MCP6022 pin 1 (`OUTA`);
- both probe grounds = common GND;
- both channels displayed with DC coupling.

From the photographed scope screen, the following values are directly readable:

### CH1 — AFG input

- frequency: approximately **100.0 Hz**;
- peak-to-peak amplitude: approximately **520 mVpp**;
- RMS: approximately **178.6 mV**;
- displayed mean/average value: approximately **7.4 mV**.

### CH2 — MCP6022 OUTA

- frequency: approximately **100.0 Hz**;
- peak-to-peak amplitude: approximately **504 mVpp**;
- RMS including DC component: approximately **2.486 V**;
- displayed mean/average value: approximately **2.480 V**.

The traces are visibly inverted relative to one another: when CH1 rises toward a positive peak, CH2 moves toward a negative-going peak around its 2.48 V DC center.

## 7. Comparison with prediction

Measured AC amplitude ratio from the screen values:

`|VOUT_AC / VAFG_AC| ~= 504/520 ~= 0.969`

The resistor-ratio prediction is approximately:

`RF/RIN ~= 0.999`

The photographed automatic Vpp readings therefore differ by about 3%. This is not assigned to a specific cause from one screen capture. Possible contributors include automatic Vpp extraction, trace noise, acquisition resolution, probe/channel effects, wiring/parasitics, or real circuit non-ideality. The dynamic gate is accepted qualitatively for topology and operating-point behavior, but a precise channel-A gain calibration is **not** frozen from this single screenshot.

The DC-center prediction from the previously measured buffered reference is approximately:

`2*VREF_BUF ~= 2*1.245 ~= 2.49 V`

Measured CH2 average is approximately:

`2.480 V`

This agrees closely with the intended level shift.

Using the measured CH2 value:

- approximate maximum output = `2.480 + 0.504/2 ~= 2.732 V`;
- approximate minimum output = `2.480 - 0.504/2 ~= 2.228 V`.

Therefore the unloaded driver waveform is clearly positive for the complete cycle at this test amplitude.

## 8. Engineering conclusion

Established by measurement:

- MCP6022 channel A reaches the intended approximately 2.49 V DC operating point;
- the 100 Hz AFG sine is transferred to OUTA with approximately unity AC magnitude;
- the channel-A waveform is inverted, as predicted by the inverting architecture;
- the output is shifted upward and remains positive over the observed cycle;
- the ACS724 was not connected during this validation, so no ACS724 transfer-function conclusion is drawn from this test.

**Result: unloaded channel-A dynamic level-shifter behavior is functionally validated.**

Precise AC-gain error remains to be quantified only if needed for fixture characterization. The formal ACS724 experiment will use CH1 across `RREF` as the actual current reference, so it will not depend on ideal channel-A gain.

## 9. Before loaded operation — supply bypass requirement

The MCP6022 datasheet states that the local VDD bypass should be 0.01 uF to 0.1 uF within approximately 2 mm, and that a bulk capacitor of about 1 uF or larger is also needed within approximately 100 mm for larger/slower current demand.

The local **100 nF** capacitor is already part of the fixture. Before connecting the ACS724 load and asking channel A to source several milliamps, the bulk-bypass gate must also be satisfied.

The confirmed ceramic kit contains 100 nF capacitors. If no separate capacitor of at least 1 uF is verified on the bench, ten 100 nF ceramics in parallel provide **1.0 uF nominal** for this temporary fixture.

## 10. Next controlled gate

Do not connect the ACS724 load yet.

Next:

1. satisfy the MCP6022 bulk-bypass requirement using verified available capacitance;
2. then connect the known 220 ohm current-limiting resistor as part of the loaded-driver validation path;
3. validate MCP6022 pin-1 waveform under the intended resistive load before treating it as a valid ACS724 stimulus;
4. only after the loaded output remains positive, stable and non-clipped should the ACS724 primary path be included in the first valid 100 Hz positive-current measurement.

No external ACS724 FILTER capacitor is approved by this result.