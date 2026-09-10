# MCP6022 reference-buffer bring-up and theory — 2026-09-10

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — ACS724 dynamic/FILTER validation fixture  
**Status:** MCP6022 supply and channel-B reference buffer measured; channel-A level shifter not yet built  

## 1. Purpose

This record documents the first measured bring-up of the MCP6022 positive-bias fixture and explains the reference-buffer architecture in deliberately simple terms.

The temporary fixture exists because the project uses the **ACS724LLCTR-05AU**, whose formal primary-current range is **0 A to 5 A unidirectional**. The DOS1102S AFG used directly produces a zero-centered sine in the present bench configuration, so a direct sine-current test reverses current for half of each cycle. The MCP6022 fixture will later shift that sine upward so the ACS724 primary current remains positive for the complete cycle.

This file is educational evidence and implementation documentation. It does not change the frozen Rev-1 AFE design.

---

## 2. Exact MCP6022 channel-B connections now in use

The exact device is **MCP6022-I/P, PDIP-8**. Relevant pin functions from the Microchip device definition are:

- pin 8 = `VDD`;
- pin 4 = `VSS`;
- pin 5 = `+INB`;
- pin 6 = `-INB`;
- pin 7 = `OUTB`.

Current connection list:

1. `MCP6022 pin 8 -> +5 V`.
2. `MCP6022 pin 4 -> GND`.
3. `100 nF ceramic -> between pin 8/VDD and pin 4/VSS`, physically close to the IC.
4. Four approximately 100 kOhm resistors form the reference divider from +5 V to GND.
5. The divider tap between the third and fourth resistor is `VREF_RAW`.
6. `VREF_RAW -> MCP6022 pin 5 (+INB)`.
7. `MCP6022 pin 7 (OUTB) -> MCP6022 pin 6 (-INB)`.
8. `MCP6022 pin 7 = VREF_BUF`, the buffered reference output.
9. AFG is not yet connected to channel A.
10. The ACS724 primary-current load is not yet connected to MCP6022 pin 1.

The pin-7-to-pin-6 connection is the feedback connection that makes channel B a **voltage follower / unity-gain buffer**.

---

## 3. Measured bring-up evidence

### 3.1 MCP6022 supply

Measured directly between MCP6022 pin 8 and pin 4:

`VDD - VSS = 4.99 V`

**Result: PASS for the present bring-up gate.**

Why this measurement matters: all later op-amp voltages depend on the actual voltage reaching the IC. Measuring at the pins proves the local power connection before signal-network debugging begins.

### 3.2 Reference-divider resistors

The four nominal 100 kOhm divider resistors were individually measured as:

| Resistor | Measured value |
|---|---:|
| R1 | 98.9 kOhm |
| R2 | 98.5 kOhm |
| R3 | 98.6 kOhm |
| R4 | 99.0 kOhm |

Total measured series resistance:

`RTOTAL = 98.9 + 98.5 + 98.6 + 99.0 = 394.0 kOhm`

The divider is therefore well matched for the intended approximately 3:1 upper/lower ratio.

### 3.3 Predicted unloaded raw reference

The reference tap is above R4, therefore:

`VREF_RAW,ideal = VDD * R4/(R1 + R2 + R3 + R4)`

Using the measured values:

`VREF_RAW,ideal = 4.99 V * 99.0/394.0 ~= 1.254 V`

So the resistor network itself predicts approximately **1.25 V** when it is not materially loaded.

### 3.4 Direct raw-reference measurements with the only available multimeter

The user has only one multimeter, the VC830L. Direct measurement at pin 5 / `VREF_RAW` produced approximately:

- first observation: about **1.15 V**;
- repeated observation: about **1.14 V**.

This is lower than the unloaded divider prediction. The reason is that the meter itself becomes an electrical load on this high-resistance divider.

The VC830L DC-voltage input resistance is approximately 1 MOhm. The divider, viewed from its output node, has a Thevenin source resistance of approximately:

`RTH = R4 || (R1 + R2 + R3)`

`RTH ~= 99 kOhm || 296 kOhm ~= 74.2 kOhm`

Connecting a 1 MOhm meter therefore forms an additional divider and lowers the voltage being measured. Using the nominal 1 MOhm input resistance predicts roughly 1.16 V, which is close to the measured 1.14–1.15 V.

This is a useful measurement lesson:

**A voltmeter is not always a passive observer. If the source impedance is high enough, the meter changes the circuit while measuring it.**

### 3.5 Buffered-reference measurement

Channel B was then wired as a voltage follower:

- pin 5 = raw reference input;
- pin 6 = inverting input;
- pin 7 = output;
- pin 7 wired directly back to pin 6.

Measured pin 7 relative to GND:

- first observation: **1.242 V**;
- repeated observation: **1.245 V**.

This is close to the approximately 1.254 V value predicted from the measured resistor divider and 4.99 V supply.

**Result: channel-B buffer behavior is consistent with the intended architecture.**

The small remaining difference is not assigned to one cause without further evidence; possible contributors include actual local supply/reference values, meter accuracy, resistor tolerances, breadboard/contact effects, and op-amp non-idealities.

---

## 4. Buffer architecture — simplest possible explanation

### 4.1 What problem are we solving?

The four-resistor divider can create the voltage we want, approximately 1.25 V, but it is a **weak source** because its source resistance is high.

The divider is good at saying:

`"the desired voltage is about 1.25 V"`

but it is not good at supplying current to another circuit while holding that voltage unchanged.

Without a buffer, the next circuit connected to the divider can pull current from the divider and change the reference voltage.

### 4.2 What does the buffer do?

The MCP6022 buffer separates two jobs:

**Job 1 — the resistor divider defines the desired voltage.**

`divider -> about 1.25 V`

**Job 2 — the op-amp output supplies current to whatever uses that voltage.**

`MCP6022 output -> about 1.25 V, but with much stronger drive capability`

The divider therefore no longer needs to power the next circuit directly.

In one sentence:

**The buffer copies the voltage without making the original divider supply the load current.**

### 4.3 Why can the op-amp read the divider without disturbing it much?

The MCP6022 uses CMOS input circuitry. Its input current is extremely small compared with the current in the 100 kOhm divider.

Therefore pin 5 behaves approximately like a very light electrical load. The divider stays close to its natural approximately 1.25 V value when only the op-amp input is connected.

This is described as **high input impedance**.

### 4.4 Where does the output current come from?

The output current does **not** come through pin 5.

Pin 5 tells the op-amp what voltage is desired.

The energy needed to drive pin 7 comes from the op-amp supply:

- pin 8 provides the positive supply;
- pin 4 provides the return/GND;
- pin 7 delivers the resulting output voltage/current.

Therefore the functional roles are:

- `pin 5 = sense/command voltage`;
- `pins 8 and 4 = energy supply`;
- `pin 7 = driven output`.

### 4.5 Why is pin 7 connected back to pin 6?

The op-amp continuously compares its two inputs:

- pin 5 = non-inverting input `V+`;
- pin 6 = inverting input `V-`.

Because pin 6 is wired directly to pin 7:

`V- = VOUT`

If the output is too low compared with pin 5:

`V+ > V-`

and the internal amplifier/output stage drives pin 7 upward.

If the output is too high:

`V+ < V-`

and the output stage drives pin 7 downward.

As pin 7 moves, pin 6 moves with it because they are physically connected. This reduces the difference between the two op-amp inputs.

The stable state is approximately:

`V7 ~= V6 ~= V5`

This self-correcting connection is **negative feedback**.

### 4.6 The buffer does not "calculate" in steps

There is no digital sequence inside the op-amp such as measure -> calculate -> move -> stop.

The MCP6022 contains analog transistor stages. A voltage difference between the inputs changes transistor currents continuously. Internal high-gain stages amplify that imbalance, and the output stage sources or sinks current. Feedback continuously changes the input difference as the output changes.

The physical loop is therefore continuous:

`input-voltage difference -> transistor-current imbalance -> internal amplification -> output current -> output voltage change -> feedback -> smaller input difference`

### 4.7 Why does the output follow the input so closely?

An op-amp has very large **open-loop gain**. Conceptually:

`VOUT = AOL * (V+ - V-)`

Because `AOL` is very large, only a tiny input difference is needed to create an ordinary output voltage. With negative feedback, the circuit therefore settles with `V+` and `V-` extremely close to one another.

The common engineering approximation is:

`V+ ~= V-`

It is an approximation, not an assertion that the two voltages are mathematically identical.

### 4.8 Why is the input impedance so high physically?

The MCP6022 is a CMOS op-amp. MOS transistor gates are insulated from their conductive channels by a dielectric layer. The gate voltage controls the channel primarily through an electric field rather than through a normal DC conduction path into the gate.

Therefore only tiny leakage/bias currents flow into the op-amp input under normal conditions.

That is the physical reason a CMOS input can have extremely high DC input impedance.

### 4.9 Why is the output impedance much lower?

The output stage is designed to source or sink current. Negative feedback also helps hold the commanded voltage: if a load pulls the output slightly away from the desired voltage, the op-amp senses the resulting input error and changes its output current to correct it.

The output is therefore much better at driving a load than the raw high-resistance divider.

The MCP6022 is still not a power amplifier; its output-current/headroom limits must be respected. That is why the later ACS724 stimulus path includes a dedicated series resistor and a separate loaded-driver validation gate.

---

## 5. Why the one-meter measurements look contradictory but are not

The user has only one multimeter, so pin 5 and pin 7 are measured **sequentially**, not simultaneously.

This distinction is essential.

### Case A — meter connected directly to pin 5

The meter is connected to the raw high-impedance divider node.

Its approximately 1 MOhm input resistance loads the divider, so the voltage falls to about 1.14–1.15 V.

During this measurement, the buffer would follow the now-loaded reference downward as well.

### Case B — meter moved from pin 5 to pin 7

Removing the meter from pin 5 removes the large measurement load from the raw divider.

Pin 5 is then loaded mainly by the extremely high-impedance MCP6022 input, so the raw reference recovers toward approximately 1.25 V.

The buffer follows that recovered voltage.

The meter is now connected to pin 7. Its current is supplied mainly by the low-impedance op-amp output instead of by the raw divider, so the output remains near 1.25 V. The measured result was approximately 1.242–1.245 V.

Therefore the two readings do **not** mean that the follower is simultaneously receiving 1.14 V and producing 1.245 V.

They mean that moving the one available meter changes which node is being loaded.

This is the clearest experimental demonstration so far of why the buffer is required.

---

## 6. Why the 100 nF capacitor is between VDD and VSS

The 100 nF ceramic connected between pin 8 and pin 4 is a **supply-decoupling/bypass capacitor**.

It is not the ACS724 FILTER capacitor.

The op-amp draws time-varying current while its internal transistors and output stage respond to signals. Breadboard wires and supply leads have nonzero resistance and inductance. Fast current changes can therefore create local supply-voltage movement.

The 100 nF capacitor provides a short local path for fast transient current close to the IC:

- at DC it does not short the 5 V rail to GND;
- at higher frequency its impedance decreases;
- it can locally source/sink brief high-frequency current;
- this helps keep the voltage across VDD-VSS stable.

The reason it is physically placed close to the IC is that long wires would add impedance and reduce the benefit of the local current loop.

---

## 7. Why later frequency-response gain is expressed in dB

The ACS724/FILTER test will measure gain at different frequencies.

First the sensor gain is calculated in ordinary units:

`G(f) = VOUT_AC(f) / I_AC(f)`

This has units of V/A.

For FILTER response, each frequency is then normalized to a low-frequency reference, planned at 100 Hz:

`H(f) = G(f) / G(100 Hz)`

`H` is dimensionless.

The normalized amplitude ratio is converted to decibels:

`HdB(f) = 20*log10(|H(f)|)`

Important reference values:

- amplitude ratio 1.000 -> 0 dB;
- amplitude ratio approximately 0.707 -> approximately -3.01 dB;
- amplitude ratio 0.5 -> approximately -6.02 dB;
- amplitude ratio 0.1 -> -20 dB.

Why dB is useful:

1. frequency responses can span large amplitude ranges, and logarithms compress them into a readable scale;
2. multiplication of stage gains becomes addition in dB;
3. standard filter landmarks such as the first-order cutoff at approximately -3.01 dB become easy to compare;
4. Bode plots conventionally use logarithmic frequency and dB magnitude, making poles/slopes easier to identify.

The factor is `20 log10` for voltage/current amplitude ratios because electrical power at fixed impedance is proportional to the square of voltage or current. The original decibel power relation uses `10 log10(P2/P1)`; substituting a squared amplitude ratio produces the factor 20.

---

## 8. Current engineering interpretation

Established by measurement:

- MCP6022 supply across pins 8–4 = **4.99 V**;
- four divider resistors = **98.9, 98.5, 98.6, 99.0 kOhm**;
- ideal unloaded divider reference from measured values = approximately **1.254 V**;
- direct raw-reference measurement with the single VC830L = approximately **1.14–1.15 V**;
- buffered pin-7 measurement = approximately **1.242–1.245 V**;
- the results are consistent with significant loading of the raw high-impedance divider by the multimeter and much smaller loading through the MCP6022 buffer architecture.

Not yet established:

- exact simultaneous `VREF_RAW` and `VREF_BUF` values, because only one multimeter is available;
- channel-A `RIN/RF` values;
- channel-A zero-input output;
- channel-A response to the AFG;
- MCP6022 loaded-driver behavior;
- valid positive ACS724 primary-current waveform.

No claim requiring simultaneous pin-5/pin-7 measurement is made from the sequential one-meter observations.

---

## 9. Next controlled step — select the channel-A resistor pair

The next stage is **not yet to connect the AFG or ACS724**.

With the PSU output OFF, select **two resistors of the same nominal value** for channel A and measure them individually. Record them as:

- `RIN`;
- `RF`.

The critical design requirement for the initial level shifter is:

`RF/RIN ~= 1`

Why: channel A will use the buffered reference at pin 3 and the two resistors around pin 2/pin 1 to implement approximately:

`VDRV = (1 + RF/RIN)*VREF_BUF - (RF/RIN)*VAFG`

When `RF = RIN` this simplifies to:

`VDRV = 2*VREF_BUF - VAFG`

With `VREF_BUF ~= 1.245 V`, the zero-input driver target will be approximately:

`VDRV,zero ~= 2*1.245 ~= 2.49 V`

This places the future sine waveform around the middle of the 0–5 V supply instead of around 0 V.

### After the resistor pair is measured

Only after `RIN` and `RF` are known and sufficiently matched will the next wiring gate be entered. The planned channel-A connections, based on the MCP6022 pinout, are:

- `pin 3 (+INA) -> pin 7 / VREF_BUF`;
- `AFG OUT -> RIN -> pin 2 (-INA)`;
- `pin 1 (OUTA) -> RF -> pin 2 (-INA)`;
- ACS724 primary-current load remains disconnected during the first channel-A voltage test.

The first channel-A test will be performed with no ACS724 load and initially with AFG output disabled. The predicted pin-1 DC output will then be approximately twice the buffered reference. Only after that passes will a small 100 Hz AFG sine be introduced.

This order isolates one function at a time:

`power -> reference divider -> buffer -> level shifter unloaded -> level shifter with AFG -> driver under load -> ACS724 positive-current validation`.

---

## 10. Immediate next action

**Power OFF. Select two equal nominal resistors for `RIN` and `RF`, measure each individually with the multimeter, and record the two resistance values. Do not connect the AFG or ACS724 to channel A yet.**
