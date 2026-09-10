# ACS724 positive-biased dynamic-test fixture using MCP6022 — 2026-09-10

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — ACS724 dynamic/FILTER validation  
**Status:** Active pre-build fixture design and controlled bring-up procedure  

## 1. Purpose

The previous DOS1102S zero-centered sine-current experiment is not valid for formal ACS724LLCTR-05AU transfer verification because the 05AU variant has a specified **0 A to 5 A unidirectional** primary-current range. A zero-centered sine reverses current for half of every cycle.

The purpose of this temporary laboratory fixture is therefore to create a **frequency-variable primary current that remains positive for the complete cycle**, while preserving an independent current reference on oscilloscope CH1 and the ACS724 output measurement on CH2.

This fixture is **not** the frozen Rev-1 MCP6022 anti-alias AFE. It is a temporary Stage B stimulus/verification circuit assembled from hardware already available in the project.

The measurement principle remains:

`AFG sine -> MCP6022 level shift -> positive primary current -> ACS724 -> VOUT`

while simultaneously:

`RREF -> CH1 -> actual primary-current reference`

and:

`ACS724 VOUT -> CH2 -> sensor response`

The fixture is only accepted for dynamic testing after each bring-up gate below is measured and passes.

---

## 2. Verified hardware facts used by the fixture

### ACS724 carrier

The project uses the Pololu #4048 carrier with ACS724LLCTR-05AU. Relevant verified facts already established in the project are:

- specified current range: **0 A to 5 A, unidirectional**;
- nominal zero-current output at 5 V: approximately **0.5 V**;
- nominal sensitivity at 5 V: approximately **0.8 V/A**;
- project bench calibration: `VOUT = 0.46910 + 0.74472 * I`;
- characterized current-reference resistance: `RREF = 68.8 ohm`;
- stock carrier FILTER capacitance: 1 nF.

### MCP6022

The available op-amp is MCP6022-I/P, dual 10 MHz rail-to-rail input/output op-amp.

For the PDIP-8 package, Microchip defines:

| Pin | Function |
|---:|---|
| 1 | OUTA |
| 2 | -INA |
| 3 | +INA |
| 4 | VSS |
| 5 | +INB |
| 6 | -INB |
| 7 | OUTB |
| 8 | VDD |

The device operates from 2.5 V to 5.5 V. For this fixture it is operated from a single nominal 5 V supply with `VSS = GND`.

Microchip specifies a local supply bypass capacitor of approximately **0.01 uF to 0.1 uF** close to VDD for good high-frequency performance, and also recommends a bulk capacitor of approximately **1 uF or larger** within about 100 mm for slower current demand.

The exact DNGH ceramic-capacitor kit physically available on the bench contains 30 pieces of each value from 10 pF through 100 nF, including **100 nF**. Therefore:

- one 100 nF ceramic is used as the local MCP6022 VDD-VSS bypass;
- if no separate >=1 uF capacitor is verified elsewhere in the bench stock, **ten 100 nF ceramics in parallel = 1.0 uF nominal** may be used as the bulk bypass for this temporary fixture.

No electrolytic capacitor is assumed to exist.

### DOS1102S

The built-in generator is used only as the AC command signal. The project has already verified that the actual bench instrument does not provide the usable DC-offset control needed for the earlier direct-drive approach.

The oscilloscope channels share a common ground, so CH1 and CH2 probe grounds remain on the same common-GND node.

---

## 3. Why an active level-shifting fixture is needed

A zero-centered AFG sine can be written conceptually as:

`VAFG(t) = A sin(2*pi*f*t)`

so it takes both positive and negative values.

Directly converting this voltage into primary current would create positive and negative current. That violates the 05AU formal measurement-range condition.

The MCP6022 fixture changes the voltage domain before the current is produced. It generates an output approximately centered at +2.5 V:

`VDRV(t) = 2*VREF - VAFG(t)`

with:

`VREF ~= 1.25 V`

therefore:

`VDRV(t) ~= 2.5 V - VAFG(t)`

The sine is inverted but shifted upward. Inversion is acceptable because transfer magnitude is calculated from the independently measured current on CH1. The essential requirement is that `VDRV` remains positive, and therefore the primary current remains positive.

---

## 4. Functional architecture

The temporary fixture is divided into six blocks.

### Block A — 5 V supply and local bypass

`+5 V -> MCP6022 pin 8 (VDD)`

`GND -> MCP6022 pin 4 (VSS)`

`100 nF ceramic -> directly between VDD and VSS, physically close to the IC`

**Why:** the op-amp draws time-varying current while responding to signals. Breadboard wiring has nonzero impedance, so a local capacitor provides a short high-frequency current path close to the IC and prevents fast supply disturbances from appearing as VDD movement.

This capacitor is a **power-supply decoupling capacitor**, not an ACS724 FILTER capacitor and not part of the test-signal transfer function.

### Block B — 1.25 V reference generator

A resistor divider creates approximately 1.25 V from the nominal 5 V rail.

The simplest bench realization uses four equal resistors:

`+5 V -> R -> R -> R -> VREF_RAW -> R -> GND`

For equal resistor values:

`VREF_RAW = 5 V * R/(4R) = 1.25 V`

The exact resistor value is not yet frozen. The next bench step is to select four equal available resistors and measure them before wiring. Matching/ratio is more important than the exact nominal resistance.

A 100 nF ceramic is placed from `VREF_RAW` to GND.

**Why:** the fixture requires a stable DC reference from which the AFG sine can be level-shifted. The capacitor suppresses reference-node noise and fast movement.

### Block C — MCP6022 channel B reference buffer

Channel B is configured as a voltage follower:

- pin 5 (`+INB`) -> `VREF_RAW`;
- pin 6 (`-INB`) -> pin 7;
- pin 7 (`OUTB`) -> `VREF_BUF`.

Expected:

`VREF_BUF ~= VREF_RAW ~= 1.25 V`

**Why:** a bare resistor divider has finite source impedance. The voltage follower isolates the divider from the level-shifting amplifier and produces a low-impedance 1.25 V reference.

### Block D — MCP6022 channel A level shifter

Channel A is configured as an inverting amplifier around the buffered 1.25 V reference:

- pin 3 (`+INA`) -> `VREF_BUF`;
- AFG OUT -> `RIN` -> pin 2 (`-INA`);
- pin 1 (`OUTA`) -> `RF` -> pin 2;
- choose `RF = RIN`.

For equal `RF` and `RIN`:

`VDRV = 2*VREF_BUF - VAFG`

With `VREF_BUF ~= 1.25 V`:

`VDRV ~= 2.5 V - VAFG`

**Why:** this converts a bipolar/zero-centered AFG sine into a positive voltage waveform without directly paralleling the AFG with the bench PSU.

The exact equal resistor value for `RIN` and `RF` remains to be selected from the verified resistor inventory. It shall be measured before power is applied.

### Block E — positive primary-current path

After the MCP6022 driver is validated unloaded, its output may drive the ACS724 primary path through a current-limiting resistor:

`MCP6022 pin 1 -> 220 ohm -> ACS724 IP+ -> ACS724 IP- -> RREF 68.8 ohm -> GND`

The 220 ohm resistor is confirmed available in the user's resistor kit.

`RREF = 68.8 ohm` remains the characterized current-reference resistor and is **not replaced by 220 ohm**.

Approximate total resistive load, ignoring the ACS724 primary resistance:

`RTOTAL ~= 220 + 68.8 = 288.8 ohm`

Primary current is approximately:

`I(t) ~= VDRV(t) / 288.8 ohm`

**Why the 220 ohm resistor is needed:** it limits current demanded from the MCP6022 output. The op-amp is not a power amplifier. The load must be deliberately limited and its real output waveform verified before the ACS724 measurement is accepted.

Microchip gives output-current/headroom performance and a +/-30 mA absolute-maximum current at output/supply pins; these figures are **not** treated as a normal operating target. The fixture therefore includes an explicit loaded-output validation gate before formal sensor testing.

### Block F — independent measurements

Fixed scope convention remains:

- `CH1 tip -> ACS724 IP- / top of RREF`;
- `CH1 ground -> common GND`;
- `CH2 tip -> ACS724 VOUT`;
- `CH2 ground -> common GND`.

Thus:

`I(t) = VCH1(t) / 68.8 ohm`

and the coherent AC gain at frequency `f` is:

`G(f) = VOUT_AC(f) / I_AC(f)`

**Why:** the experiment must not infer primary current from AFG amplitude or ideal op-amp equations. CH1 measures the actual current through the characterized resistor, so source amplitude error, small driver gain error and frequency-dependent driver variation are included in the measured denominator rather than silently assumed away.

---

## 5. Current breadboard state / connection status

The MCP6022 has been physically placed across the breadboard center trench with the package orientation identified from the top-view notch/dot convention.

The active power-pin definition is:

- pin 8 = `VDD` -> +5 V;
- pin 4 = `VSS` -> GND.

The user explicitly confirmed understanding of `5 V -> pin 8` and `GND -> pin 4`.

The next required hardware connection is the local **100 nF ceramic bypass directly between the VDD and VSS supply nodes near the MCP6022**. Installation of this capacitor is not recorded as measured/completed until the user confirms it physically.

No AFG, ACS724 primary path, reference divider or feedback network is yet treated as validated in this new fixture.

---

## 6. Exact controlled bring-up sequence

The fixture shall be built progressively. A later gate is not entered until the previous gate behaves as predicted.

### Gate 1 — MCP6022 supply and decoupling only

With PSU output OFF:

1. Verify MCP6022 orientation and that it straddles the center trench.
2. Verify pin 8 is the VDD side and pin 4 is VSS.
3. Connect +5 V rail to pin 8.
4. Connect GND rail to pin 4.
5. Place one **100 nF ceramic** directly between the pin-8 VDD node and pin-4/GND node as close to the IC as practical.
6. Verify that the 100 nF capacitor is ceramic and therefore non-polarized.
7. Do not connect AFG, ACS724 primary path or op-amp feedback yet.

**Reason for this gate:** first prove that the IC has a correct and stable power domain. This prevents later signal-network faults from being confused with basic power-wiring errors.

### Gate 2 — supply sanity measurement

After visual continuity inspection:

1. Keep AFG disconnected/OFF.
2. Keep the ACS724 primary path disconnected from the MCP6022 output.
3. Set the bench supply to nominal 5.00 V with an appropriately low current limit before enabling output.
4. Enable the supply.
5. Measure MCP6022 pin 8 relative to pin 4/GND.
6. Expected result: approximately the applied 5 V supply.
7. If pin 8 is near 0 V, the PSU enters current limit, the IC becomes warm, or the supply is otherwise abnormal, disable output immediately and troubleshoot before continuing.

**Reason:** later op-amp measurements are meaningless until the actual local supply has been verified at the IC pins.

### Gate 3 — bulk bypass requirement

Before loaded dynamic operation, satisfy the MCP6022 bulk-bypass recommendation.

Preferred route: use a verified capacitor of at least 1 uF if one is confirmed elsewhere in the project stock.

Fallback using the confirmed DNGH kit only:

`10 x 100 nF in parallel = 1.0 uF nominal`

Connect this parallel bank between the local +5 V and GND rails within approximately 100 mm of the MCP6022.

**Reason:** the single 100 nF local capacitor is optimized for fast/high-frequency current loops. The larger effective capacitance supplies slower transient current demand and reduces movement of the local 5 V rail during output loading.

### Gate 4 — choose and measure reference-divider resistors

With power OFF:

1. Select four resistors of the same nominal value from the available resistor kit.
2. Prefer a moderate/high value that does not unnecessarily load the 5 V rail; the exact value is secondary to having a well-matched 3:1 divider ratio.
3. Measure and record all four actual resistance values.
4. Do not proceed if one resistor is clearly from a different value group.

Then wire:

`+5 V -> R1 -> R2 -> R3 -> VREF_RAW -> R4 -> GND`

with all four nominally equal.

Add one 100 nF ceramic from `VREF_RAW` to GND.

Predicted reference for ideal equal resistors:

`VREF_RAW ~= 1.25 V`.

**Reason:** 1.25 V is chosen because the later equal-resistor inverting stage produces `2*VREF = 2.5 V` of DC level shift, centering the driver waveform around mid-supply.

### Gate 5 — measure the raw 1.25 V reference

With power ON and AFG still disconnected:

1. Measure `VREF_RAW` relative to GND.
2. Expected result: approximately 1.25 V.
3. Record the measured value.
4. If it is materially different, disable power and check resistor order, breadboard rows and resistor values.

**Reason:** the level shifter depends directly on this reference. A wrong VREF would shift the output to the wrong DC level and could reintroduce negative primary current or op-amp clipping.

### Gate 6 — configure channel B as reference buffer

With power OFF:

1. Connect pin 5 (`+INB`) to `VREF_RAW`.
2. Connect pin 6 (`-INB`) directly to pin 7 (`OUTB`).
3. Treat pin 7 as `VREF_BUF`.

Power ON and measure pin 7 relative to GND.

Expected:

`VREF_BUF ~= VREF_RAW ~= 1.25 V`.

Record both values.

**Reason:** channel B isolates the divider from channel A so the 1.25 V reference remains stiff when channel A processes the AFG signal.

### Gate 7 — choose equal RIN and RF for channel A

With power OFF:

1. Select two equal nominal resistors from the available kit.
2. Measure both values.
3. Record them as `RIN` and `RF`.
4. Their ratio should be close to 1:1; exact resistance is less important than matching for this unity-magnitude inverting stage.

Wire:

- pin 3 (`+INA`) -> `VREF_BUF` / pin 7;
- `RIN` between AFG OUT connection node and pin 2 (`-INA`);
- `RF` between pin 1 (`OUTA`) and pin 2 (`-INA`).

Do **not** connect the ACS724 primary-current load yet.

**Reason:** channel A must first be validated as a voltage-processing stage without the extra complication of output loading.

### Gate 8 — validate level shifting without ACS724 load

1. Keep ACS724 primary path disconnected from pin 1.
2. Apply 5 V power to MCP6022.
3. With AFG output OFF/zero input, measure pin 1.
4. Expected zero-input driver level:

   `VDRV ~= 2*VREF_BUF ~= 2.5 V`.

5. If the zero-input output is not physically plausible, stop before connecting the AFG or load.
6. Configure the DOS1102S AFG to a 100 Hz sine at a small initial amplitude.
7. Measure the actual AFG waveform rather than relying solely on the front-panel amplitude number.
8. Enable AFG and observe pin 1.
9. Confirm the driver waveform is sinusoidal, inverted relative to AFG, centered near 2.5 V, and remains inside the 0-5 V supply range.
10. Increase amplitude only after the small-signal result is correct.

**Reason:** this independently proves the mathematical relation `VDRV ~= 2*VREF - VAFG` before the op-amp is asked to source load current.

### Gate 9 — loaded driver validation before sensor interpretation

With power OFF, add the intended positive-current path:

`pin 1 -> 220 ohm -> ACS724 IP+ -> ACS724 IP- -> RREF 68.8 ohm -> common GND`.

Then restore power with AFG initially OFF.

Measure:

- pin-1 DC output;
- CH1 voltage across RREF;
- local MCP6022 VDD;
- whether the output waveform clips or shifts unexpectedly under load.

For an ideal 2.5 V zero-input driver level:

`IDC ~= 2.5 V / 288.8 ohm ~= 8.66 mA`

and:

`VCH1,DC ~= 8.66 mA * 68.8 ohm ~= 0.596 V`.

These are predictions, not acceptance by themselves.

**Reason:** the MCP6022 output-current capability and voltage headroom are finite. The loaded waveform must be measured before the circuit is trusted as a test stimulus.

### Gate 10 — establish positive AC current at 100 Hz

1. Keep both scope channels DC-coupled.
2. Set AFG to 100 Hz sine.
3. Start at low measured amplitude.
4. Increase amplitude gradually while observing CH1.
5. The entire CH1 waveform must remain above 0 V.
6. Derive:

   `Imin = VCH1,min / 68.8 ohm`

   `Imax = VCH1,max / 68.8 ohm`

7. Do not accept the test unless `Imin > 0 A` with visible margin.
8. Also verify the pin-1 driver waveform remains undistorted and the MCP6022 local 5 V rail remains stable.

Example only, for an actual measured AFG input of approximately 2.0 Vpp and ideal unity ratio:

- `VDRV ~= 1.5 V to 3.5 V`;
- predicted current ~= 5.19 mA to 12.12 mA;
- predicted CH1 ~= 0.357 V to 0.834 V.

These values shall be replaced by the actual measured amplitudes in the test record.

**Reason:** this is the decisive validity gate. CH1 directly proves that primary current never reverses direction.

### Gate 11 — connect CH2 and perform first valid sensor capture

After Gate 10 passes:

1. CH1 remains across RREF.
2. CH2 tip -> ACS724 VOUT.
3. CH2 ground -> common GND.
4. CH1 and CH2 remain DC-coupled.
5. Verify CH2 mean is near the expected ACS724 operating level rather than near 0 V.
6. Allow the 100 Hz waveforms to stabilize.
7. Press Run/Stop to freeze the acquisition.
8. Export CH1.
9. Without resuming acquisition, switch export source and export CH2.
10. Use explicit filenames identifying the MCP6022 biased fixture and frequency.
11. Resume acquisition only after both files are saved.

Calculate:

`IAC,pp = VCH1,AC,pp / 68.8 ohm`

`G100 = VCH2,AC,pp / IAC,pp`

Compare the result with the bench DC sensitivity `0.74472 V/A` for plausibility and repeatability.

**Reason:** only after the primary-current waveform is proven valid may CH2 be interpreted as formal ACS724 dynamic-response evidence.

### Gate 12 — frequency sweep and FILTER comparison

Only after one valid repeatable 100 Hz result:

- stock FILTER: 100 Hz, 1 kHz, 2 kHz, 5 kHz, 10 kHz;
- then repeat with selected external FILTER candidates, beginning with +3.3 nF if still retained as the leading candidate;
- at every point derive actual current from CH1 rather than generator settings;
- normalize each filter configuration to its own low-frequency gain.

This completes the missing dynamic-band validation needed before approving an external ACS724 FILTER capacitor.

---

## 7. Current engineering boundary

Established:

- the direct zero-centered sine architecture is invalid for formal 05AU validation;
- an active level-shifting approach avoids the need for an unavailable 100 uF/470 uF coupling capacitor;
- the MCP6022 and confirmed ceramic capacitor kit can implement the required reference, buffering, local bypass and level shifting;
- pin 8 is VDD and pin 4 is VSS/GND;
- 100 nF is a valid local bypass value for the MCP6022;
- RREF remains 68.8 ohm;
- a 220 ohm current-limiting resistor is available.

Not yet established by measurement:

- actual four-resistor VREF divider values;
- actual equal RIN/RF values;
- measured VREF_RAW and VREF_BUF;
- unloaded level-shifter transfer;
- loaded MCP6022 output headroom/distortion;
- final positive-current amplitude;
- valid 100 Hz ACS724 AC gain;
- valid stock/candidate FILTER transfer curves.

## Immediate next action

**Complete Gate 1 only:** install the 100 nF ceramic bypass between MCP6022 pin 8/VDD and pin 4/VSS-GND, physically close to the IC. Then verify the connection before proceeding to the 1.25 V reference divider.

Do not connect the AFG or ACS724 primary-current load to the MCP6022 yet.

## References

- Microchip MCP6021/1R/2/3/4 datasheet, DS20001685E — MCP6022 pinout, 2.5-5.5 V operation, 10 MHz GBWP, output-current/headroom data, and supply-bypass guidance.
- Pololu #4048 ACS724 carrier documentation — ACS724LLCTR-05AU range, transfer characteristics, primary resistance and carrier FILTER configuration.
- HANMATEK DOS1102S documentation — AFG operating range/output impedance and oscilloscope common-ground constraints.
