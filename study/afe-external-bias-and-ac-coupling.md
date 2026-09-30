# External bias and AC coupling for AFE bench validation

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — Rev-1 AFE bring-up  
**Purpose:** Explain why the DOS1102S sine cannot be injected directly into the single-supply AFE and how a temporary external bias fixture solves that measurement problem.

## 1. The problem: the AFG sine is centered around 0 V

The DOS1102S AFG was used at 100 Hz and its minimum practical amplitude setting of 0.5 Vpp.

A measured input waveform was approximately:

- 520 mVpp;
- 176 mV RMS;
- mean close to 0 V.

A 520 mVpp sine has a peak amplitude of about 260 mV. If it is centered near 0 V, it asks the circuit to see approximately:

```text
-0.26 V ... 0 V ... +0.26 V
```

The Rev-1 MCP6022 AFE is powered from approximately 0 V and 5 V. A negative input is therefore outside the intended sensor-signal operating region.

This is why the first direct 100 Hz test produced a bottom-clipped output instead of a clean sine.

## 2. What "bias" means

Bias is a DC operating level intentionally added to an AC signal.

The sine's size can stay the same while its center moves:

```text
before:
-0.26 V ... 0 ... +0.26 V

after adding about +0.44 V bias:
+0.18 V ... +0.44 V ... +0.70 V
```

The AC amplitude has not intentionally changed. Only the DC center has moved upward.

That keeps the complete sine above ground so the single-supply AFE can process it normally.

## 3. Why a resistor divider makes the DC bias

For a divider:

```text
5V_MEAS -- Rtop --+-- Vbias
                  |
                Rbottom
                  |
               GND_MEAS
```

the unloaded bias is:

`Vbias = Vsupply × Rbottom / (Rtop + Rbottom)`.

For 10 kΩ on top and 1 kΩ on the bottom with 4.8 V measured supply:

`Vbias ≈ 4.8 × 1 / 11 ≈ 0.436 V`.

The bench measurement was 0.44 V, which agrees with the prediction.

## 4. Why the AFG is connected through a capacitor

If the AFG were connected directly to the bias node, its low output impedance would fight the resistor divider and pull the node toward the AFG's own DC level.

A series coupling capacitor prevents that DC fight.

At DC, after charging, an ideal capacitor is open: the divider can establish the node's DC voltage.

For changing signals, capacitor current can flow, so the AFG's AC component is transferred to the biased node.

Conceptually:

```text
AFG AC ---- coupling capacitor ----+---- R1 / AFE
                                   |
                                Vbias divider
```

The result is intended to be:

`biased input = DC bias + AC sine`.

## 5. Why capacitor value matters

The coupling capacitor and the resistance seen around it form a high-pass network.

If its corner frequency is too close to the test frequency, the temporary fixture itself attenuates and phase-shifts the sine. Then the measured result would be a mixture of:

1. temporary coupling-fixture response;
2. actual AFE response.

That is undesirable because the goal is to characterize the AFE.

The user's available coupling parts are ten 100 nF capacitors.

In parallel:

`Ctotal = 100 nF + ... + 100 nF = 1000 nF = 1 µF`.

With a 10 kΩ / 1 kΩ divider:

`Rth = 10k || 1k ≈ 909 Ω`

and the approximate coupling corner is:

`fc ≈ 1 / (2π × 909 Ω × 1 µF) ≈ 175 Hz`.

That is too high for a clean 100 Hz baseline because the test fixture would significantly attenuate 100 Hz.

If the divider resistances are scaled by 10 while preserving their 10:1 ratio, e.g. 100 kΩ / 10 kΩ, the DC bias remains about the same but:

`Rth ≈ 9.09 kΩ`

and with 1 µF:

`fc ≈ 17.5 Hz`.

That is much farther below 100 Hz. This is a design candidate, not yet an accepted bench configuration; actual resistor availability and measured behavior must be verified first.

## 6. What "ten capacitors in parallel" physically means

Every capacitor must connect between the exact same two electrical nodes:

```text
Node A ----||---- Node B
       ----||----
       ----||----
          ...
       ----||----   ten total
```

All Node-A legs are electrically common.

All Node-B legs are electrically common.

For the 100 nF ceramic capacitors used here, there is no polarity.

The total capacitance is the sum of the individual capacitances.

## 7. Measurement sequence

A valid temporary source must be proven before connecting it to the AFE:

1. Verify divider alone: expected bias near 0.44 V.
2. Add the coupling-capacitor bank and AFG.
3. Measure only the resulting biased source at the R1 input.
4. Confirm:
   - mean remains positive near the intended bias;
   - full waveform stays above ground;
   - frequency is 100 Hz;
   - waveform remains sinusoidal;
   - actual Vpp is known.
5. Only then connect/measure TP_AFE and calculate AFE gain/phase.

This prevents a source-fixture problem from being misinterpreted as filter behavior.

## 8. Source-contention rule

Only one active voltage source may directly drive the R1/TP_SENSOR input node at a time.

Do not connect ACS724 VOUT and AFG OUT directly to that same node simultaneously.

When the AFG is used for independent AFE validation, the ACS724 output path must be disconnected from the R1 input.
