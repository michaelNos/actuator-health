# MCP6022 channel-A resistor network and supply-bypass theory — 2026-09-10

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — ACS724 dynamic/FILTER validation fixture  
**Status:** Theory/study record based on the measured MCP6022 bring-up; no new ACS724 FILTER decision

## 1. Purpose

This record explains two concepts that are required before the temporary MCP6022 positive-bias fixture is loaded by the ACS724 primary-current path:

1. the complete resistor/feedback architecture around MCP6022 channel A and why it implements a level shifter;
2. the purpose of the local and bulk supply-bypass capacitors and why the bulk capacitor is added before loaded dynamic operation.

The explanations below deliberately separate **what sets a voltage**, **what carries current**, and **what negative feedback forces the op-amp to do**.

This file is educational implementation evidence. It does not alter the frozen Rev-1 AFE design.

---

## 2. Measured context already established

The temporary fixture has already produced the following measured results:

- MCP6022 supply between pins 8 and 4: approximately **4.99 V**;
- buffered reference on channel B: approximately **1.242–1.245 V**;
- channel-A resistors:
  - `RIN = 99.1 kOhm`;
  - `RF = 99.0 kOhm`;
- channel-A pin-1 DC output with zero external input: approximately **2.49 V**;
- unloaded 100 Hz dynamic test:
  - AFG/input CH1: approximately **520 mVpp**;
  - MCP6022 pin-1 output CH2: approximately **504 mVpp**;
  - output DC centre: approximately **2.480 V**;
  - output visibly inverted relative to input.

These observations are consistent with the intended level-shifter relation derived below.

---

# Part I — Channel-A resistor and feedback architecture

## 3. Exact channel-A connection list

Relevant MCP6022 channel-A pins:

- pin 1 = `OUTA`;
- pin 2 = `-INA`;
- pin 3 = `+INA`.

Connections used for the temporary level shifter:

1. `pin 3 (+INA) -> VREF_BUF`, the buffered approximately 1.245 V reference produced by channel B.
2. `RIN = 99.1 kOhm` connects between the AFG output node and pin 2.
3. `RF = 99.0 kOhm` connects between pin 1 and pin 2.
4. Pin 2 is therefore the junction of `RIN` and `RF`.
5. Pin 1 is the driven output node; it is **not** the resistor junction.
6. The AFG ground is common with MCP6022 VSS/GND.
7. During the earlier DC-only validation, the AFG side of `RIN` was temporarily connected to GND so that `VIN = 0 V` was known exactly.

The resistor network is therefore an **inverting amplifier referenced to a non-zero voltage** rather than to ground.

---

## 4. The three voltages that must not be confused

Define:

- `VIN` = voltage on the AFG side of `RIN`;
- `VREF` = voltage on pin 3, approximately 1.245 V;
- `VOUT` = voltage on pin 1.

Pin 2 is the inverting-input node. Call it `VX`.

Because the op-amp is operated with negative feedback, the closed-loop circuit drives its output so that, to a very good approximation:

`VX ~= VREF`

This does **not** mean pin 2 and pin 3 are physically connected. They are separate pins. The equality is an operating result created by the feedback loop.

The phrase often used in op-amp analysis is **virtual short** or **virtual equality**:

- the voltages are almost equal;
- there is no actual short circuit between them;
- essentially no signal current needs to flow from pin 3 to pin 2.

For this fixture:

`pin 3 ~= 1.245 V`

therefore negative feedback keeps:

`pin 2 ~= 1.245 V`.

---

## 5. Why pin 2 stays near the reference voltage

The MCP6022 has very large open-loop gain. Conceptually:

`VOUT = AOL * (V+ - V-)`

For channel A:

- `V+ = pin 3 = VREF`;
- `V- = pin 2 = VX`.

If `VX` falls slightly below `VREF`, then `V+ > V-` and the output stage drives pin 1 upward.

Because pin 1 is connected back to pin 2 through `RF`, raising pin 1 sends corrective current through `RF` and raises the pin-2 node.

If `VX` rises slightly above `VREF`, the opposite happens: the output moves downward and the feedback current changes direction until pin 2 returns close to the reference.

Thus the feedback loop continuously acts to make:

`pin 2 ~= pin 3`.

This is the fundamental condition that allows the resistor equations below to determine the output voltage.

---

## 6. Why current through RIN must also flow through RF

At pin 2 there are three possible current paths:

1. through `RIN` toward the input source;
2. through `RF` toward the output;
3. into the MCP6022 inverting input itself.

The MCP6022 uses CMOS inputs and its input bias current is extremely small compared with the microampere-scale resistor currents in this fixture. For first-order circuit analysis, the current into pin 2 is therefore approximated as zero:

`Ipin2 ~= 0`.

Kirchhoff's Current Law at pin 2 then requires the resistor currents to balance.

Using currents leaving pin 2 as positive:

`(VX - VIN)/RIN + (VX - VOUT)/RF ~= 0`

and because negative feedback gives:

`VX ~= VREF`,

the equation becomes:

`(VREF - VIN)/RIN + (VREF - VOUT)/RF = 0`.

This single node equation explains the whole level shifter.

---

## 7. Derivation of the general level-shifter equation

Starting from:

`(VREF - VIN)/RIN + (VREF - VOUT)/RF = 0`

move the second term to the other side:

`(VREF - VOUT)/RF = -(VREF - VIN)/RIN`

multiply by `RF`:

`VREF - VOUT = -(RF/RIN)*(VREF - VIN)`

expand the right-hand side:

`VREF - VOUT = -(RF/RIN)*VREF + (RF/RIN)*VIN`

solve for `VOUT`:

`VOUT = VREF + (RF/RIN)*VREF - (RF/RIN)*VIN`

therefore:

`VOUT = (1 + RF/RIN)*VREF - (RF/RIN)*VIN`.

This is the general equation for the present resistor arrangement.

---

## 8. Why equal resistors are useful

The measured resistor ratio is:

`RF/RIN = 99.0/99.1 ~= 0.99899`.

This is very close to one.

If `RF = RIN` exactly, the equation simplifies to:

`VOUT = 2*VREF - VIN`.

With the measured buffered reference around 1.245 V:

`2*VREF ~= 2.49 V`.

So the practical working relation is:

`VOUT ~= 2.49 V - VIN`.

This expression has two separate effects:

1. `2.49 V` sets the positive DC centre;
2. `-VIN` reproduces the input with approximately unity amplitude but inverted polarity.

The circuit therefore performs both **level shifting** and **inversion**.

---

## 9. DC example: VIN = 0 V

During the controlled DC validation, the AFG side of `RIN` was connected to ground.

Therefore:

`VIN = 0 V`.

Pin 2 is held by feedback near:

`VX ~= 1.245 V`.

Current through `RIN` is approximately:

`IRIN = (1.245 - 0)/99.1 kOhm ~= 12.6 uA`.

Because essentially no current enters the op-amp input, approximately the same magnitude must be supplied through `RF`.

For about 12.6 uA through approximately 99 kOhm, the voltage difference across `RF` is approximately:

`VRF ~= 12.6 uA * 99 kOhm ~= 1.24 V`.

The output therefore must be about 1.24 V above the pin-2 node:

`VOUT ~= 1.245 + 1.24 ~= 2.49 V`.

The measured pin-1 result was approximately **2.49 V**, matching this prediction.

---

## 10. Positive-input example

Suppose the AFG instantaneously produces:

`VIN = +0.25 V`.

The pin-2 node is still maintained near 1.245 V by feedback.

The difference across `RIN` becomes smaller than in the zero-input case:

`1.245 - 0.25 = 0.995 V`.

Less current therefore leaves pin 2 through `RIN`.

Because the current through `RF` must balance it, a smaller voltage difference is needed across `RF`.

The output falls.

Using the ideal equal-resistor equation:

`VOUT ~= 2.49 - 0.25 = 2.24 V`.

Thus a positive movement at the input creates a negative movement at the output.

---

## 11. Negative-input example

Suppose instead:

`VIN = -0.25 V`.

The voltage difference across `RIN` is now larger:

`1.245 - (-0.25) = 1.495 V`.

More current flows through `RIN`.

The op-amp must raise pin 1 so that enough current can flow through `RF` to maintain the pin-2 node near the 1.245 V reference.

Using the ideal equal-resistor equation:

`VOUT ~= 2.49 - (-0.25) = 2.74 V`.

Thus the zero-centered input swing of about `-0.25 V to +0.25 V` becomes approximately:

`2.74 V to 2.24 V`.

The order is reversed because the stage is inverting, but the complete output remains positive.

This is exactly the behavior observed in the unloaded 100 Hz oscilloscope measurement.

---

## 12. Why the resistors matter individually

`RIN` and `RF` are not arbitrary series resistors. Their ratio defines the AC signal gain:

`signal gain = -RF/RIN`.

The same ratio also determines how strongly the reference contributes to the output:

`reference gain = 1 + RF/RIN`.

With a 1:1 ratio:

- signal gain is approximately `-1`;
- reference gain is approximately `+2`.

Therefore:

`VOUT ~= 2*VREF - VIN`.

If `RF` were twice `RIN`, the signal would be inverted with magnitude gain about 2 and the reference term would be multiplied by about 3. If `RF` were half `RIN`, the signal magnitude gain would be about 0.5 and the reference term would be multiplied by about 1.5.

So resistor **ratio** determines the transfer law.

---

## 13. Why approximately 100 kOhm was acceptable for this temporary test

The present pair was chosen primarily because two well-matched nominal 100 kOhm resistors were physically available and could be measured.

High resistance keeps the signal-network current small. At roughly a 1.25 V difference, a 100 kOhm resistor carries only about 12.5 uA.

However, resistance cannot be increased indefinitely. High resistor values interact more strongly with input/parasitic capacitances and can increase thermal-noise contribution. Microchip specifically discusses gain peaking and the interaction of feedback resistance with capacitance at the inverting node for this high-speed op-amp family.

Therefore the 99 kOhm pair is acceptable as a **temporary Stage B stimulus-network value only after measured dynamic validation**. It is not being promoted to a final precision/high-frequency design choice by this study.

For the actual ACS724 test, the primary current is measured independently on CH1. The experiment therefore does not rely on the resistor-network equation being perfectly ideal at every frequency.

---

# Part II — Local and bulk supply-bypass capacitors

## 14. What problem supply bypass solves

An op-amp is powered through real wires, breadboard contacts, leads and a bench supply. These are not ideal conductors.

They have non-zero:

- resistance;
- inductance;
- contact impedance.

When the op-amp output current changes, its internal current demand from VDD also changes. If that changing current must travel through the entire supply path before it reaches the IC, the finite impedance of the path creates a changing voltage drop.

Conceptually:

`Vsupply_at_IC = Vsupply_source - I(t)*Zsupply`.

Therefore a changing current can make the voltage actually present at the MCP6022 pins move even if the bench supply display remains fixed.

Supply-bypass capacitors reduce this local supply movement by storing charge close to the IC.

---

## 15. Capacitor as a local charge reservoir

The fundamental charge relation is:

`Q = C*V`.

A larger capacitance stores more charge for the same voltage.

The current-voltage relation is:

`i = C*dV/dt`.

Rearranged:

`dV/dt = i/C`.

This shows directly why a larger capacitor reduces supply-voltage movement for a given temporary current demand: for the same current, increasing `C` reduces the rate at which the capacitor voltage changes.

For a current pulse lasting `dt`, the approximate voltage change is:

`DeltaV ~= I*dt/C`.

This is the simplest quantitative picture of a bypass capacitor.

The capacitor does not create energy. It is charged from the supply beforehand, releases some stored charge during a transient, and is then replenished by the supply.

---

## 16. Why the local 100 nF capacitor is very close to the IC

Microchip Section 4.7, **Supply Bypass**, states that this op-amp family should have a local bypass capacitor of approximately **0.01 uF to 0.1 uF within 2 mm** for good high-frequency performance.

The present fixture therefore uses one **100 nF ceramic** directly between:

- MCP6022 pin 8 / VDD;
- MCP6022 pin 4 / VSS-GND.

The local capacitor is physically close because high-frequency current changes are strongly affected by wiring inductance. A capacitor several centimetres away may have sufficient capacitance but the long connection path can add enough inductive impedance that it cannot supply a very fast current pulse effectively.

Thus the local 100 nF capacitor is mainly about making the **high-frequency current loop short**.

---

## 17. Why a separate bulk capacitor is also recommended

The same Microchip Section 4.7 states that the device also needs a **bulk capacitor of about 1 uF or larger within 100 mm** to provide **large, slow currents**. The datasheet explicitly distinguishes this from the small local high-frequency bypass.

The two capacitors therefore have complementary jobs:

- local ~100 nF: small, physically very close, optimized for fast/high-frequency current transients;
- bulk >=1 uF: larger stored charge, allowed to be farther away, supports slower/larger current changes and reduces lower-frequency supply movement.

This is not because one capacitor works only at one exact frequency. Real capacitors and interconnections have distributed resistance and inductance. The practical reason for using both is to obtain low supply impedance over a wider frequency range.

---

## 18. Why bulk bypass becomes important before loading channel A

The unloaded channel-A test required almost no external output current. The op-amp only had to drive the oscilloscope input and its own feedback network.

The next stage will connect a substantially lower-resistance external path. The planned primary-current drive path contains the confirmed 220 Ohm current-limiting resistor plus the characterized 68.8 Ohm reference resistor, with the ACS724 primary conductor between them.

When the output is loaded, pin 1 must source a time-varying milliampere-scale current. This is a more demanding operating condition than the unloaded voltage test.

Adding the recommended bulk bypass before that test gives the local 5 V domain a reserve of charge for these slower/larger current variations and helps prevent supply movement from being mistaken for op-amp gain error or ACS724 behavior.

The engineering sequence is therefore deliberately:

1. validate the op-amp unloaded;
2. establish the manufacturer's recommended supply bypassing;
3. validate the driver under load;
4. only then use the fixture as a sensor stimulus.

---

## 19. Why capacitors in parallel add

For capacitors connected between the same two nodes, each capacitor experiences the same voltage.

Total stored charge is the sum of the individual charges:

`Qtotal = Q1 + Q2 + ...`.

Since `Q = C*V` and `V` is common:

`Qtotal = (C1 + C2 + ...)*V`.

Therefore:

`Ctotal = C1 + C2 + ...`.

The confirmed ceramic kit contains 100 nF capacitors but no verified 1 uF part. Ten 100 nF capacitors in parallel therefore give a nominal total capacitance:

`10 * 100 nF = 1000 nF = 1.0 uF`.

This is a practical temporary bench implementation of the nominal capacitance requirement.

It should not be interpreted as saying that ten distributed 100 nF capacitors are physically identical to one ideal 1 uF capacitor. Their lead lengths, ESR, ESL and breadboard layout differ. For this temporary fixture, the parallel bank is a documented fallback using verified available parts.

---

## 20. The three capacitor functions in this fixture must not be confused

There are currently three different capacitor roles in the Stage B work:

### A. MCP6022 local supply bypass

- about 100 nF;
- between VDD and VSS;
- physically close to the IC;
- purpose: fast local supply-current support / high-frequency supply stability.

### B. MCP6022 bulk supply bypass

- about 1 uF or larger;
- also between VDD and VSS;
- within about 100 mm according to Microchip;
- purpose: larger/slower supply-current support.

### C. ACS724 FILTER capacitor

- connected to the ACS724 FILTER node according to the sensor/carrier architecture;
- purpose: deliberately changes the sensor-output bandwidth/noise behavior;
- this is the component being experimentally optimized in the project.

The supply-bypass capacitors are **not** part of the intended signal transfer function. The ACS724 FILTER capacitor deliberately is.

A separate 100 nF capacitor may also be used on the raw 1.25 V reference node to reduce reference-node noise; that is yet another function and should not be confused with the VDD-VSS bypass components.

---

## 21. Current theory conclusions

### Channel-A resistor network

- pin 3 defines the reference voltage;
- negative feedback drives pin 2 close to that reference;
- the op-amp input draws negligible current compared with the resistor currents;
- KCL at pin 2 forces the `RIN` and `RF` currents to balance;
- resistor ratio sets the transfer equation;
- with `RF ~= RIN`, the circuit implements approximately:

`VOUT ~= 2*VREF - VIN`;

- this converts the zero-centered AFG sine into an inverted sine centered near +2.49 V.

### Supply bypass

- real supply wiring has impedance;
- dynamic op-amp current produces dynamic voltage drop in that impedance;
- bypass capacitors provide local stored charge;
- the local 100 nF capacitor handles fast/high-frequency current loops;
- the >=1 uF bulk capacitor supports larger/slower current demand;
- Microchip explicitly recommends both roles for this op-amp family;
- the bulk bypass is added before loaded-driver validation so supply movement is not confused with signal-path behavior.

---

## 22. References

- Microchip, **MCP6021/1R/2/3/4 — Rail-to-Rail Input/Output, 10 MHz Op Amps**, DS20001685F. Relevant sections: electrical characteristics, input current/impedance, gain peaking, and Section 4.7 Supply Bypass.  
  https://ww1.microchip.com/downloads/aemDocuments/documents/MSLD/ProductDocuments/DataSheets/MCP6021-Data-Sheet-DS20001685.pdf
- Microchip MCP6022 product page:  
  https://www.microchip.com/en-us/product/mcp6022

---

## 23. Next controlled action

No ACS724 load is connected yet.

After this theory gate is understood/accepted, the next physical action is to complete the MCP6022 bulk supply bypass before loaded-driver validation.

Using only the confirmed capacitor kit, the provisional fallback is a nominal 1.0 uF bank made from ten 100 nF ceramics in parallel between the local +5 V and GND rails, while retaining the existing dedicated 100 nF capacitor immediately at MCP6022 VDD-VSS.

After installation, the local supply and channel-A DC operating point are rechecked before the 220 Ohm / ACS724 load is introduced.
