# Temporary AFE biased-source test fixture

This folder documents the **temporary bench-only source fixture** used to drive the MCP6022 AFE from the DOS1102S AFG.

It is not part of the product-level actuator-health signal chain.

## Exact electrical connections

```text
5V_MEAS
   |
  10 kΩ
   |
   +---------------- BIAS_NODE ---------------- R1 / AFE input
   |                     |
   1 kΩ                  |
   |                     |
GND_MEAS          1 µF coupling bank
                         |
                      AFG OUT

AFG GND -------------------------------------- GND_MEAS
```

The 1 µF coupling bank is the physical bank of **ten 100 nF ceramic capacitors marked 104 in parallel**.

## Bench rule

During independent AFE testing:

- AFG OUT connects to the coupling-capacitor-bank input.
- AFG GND connects to GND_MEAS.
- The capacitor-bank output, bottom of the 10 kΩ resistor, top of the 1 kΩ resistor, and the AFE R1 input are the **same BIAS_NODE**.
- The 10 kΩ resistor top connects to 5V_MEAS.
- The 1 kΩ resistor bottom connects to GND_MEAS.
- ACS724 VOUT must be disconnected from the AFE input while the AFG fixture is active.

With about 4.8 V supply, the unloaded expected bias is approximately:

`VBIAS = 4.8 V * 1k / (10k + 1k) ≈ 0.436 V`.

The measured bench value near 0.44 V is consistent with this.

## Physical verification before continuing AC measurements

With power OFF:

1. BIAS_NODE continuity: bottom of 10 kΩ ↔ top of 1 kΩ ↔ coupling-bank output ↔ AFE R1 input.
2. 10 kΩ top ↔ 5V_MEAS.
3. 1 kΩ bottom ↔ GND_MEAS.
4. AFG GND ↔ GND_MEAS.
5. AFG OUT ↔ coupling-bank input.
6. Coupling-bank input must **not** have DC continuity to BIAS_NODE through the capacitors after any transient meter response settles.
7. ACS724 VOUT must not be connected to BIAS_NODE during AFG-driven AFE tests.

With power ON:

1. Measure BIAS_NODE DC before enabling the AFG; expect about 0.4–0.45 V.
2. Enable AFG and confirm the mean remains near the same bias.
3. Confirm the full sine remains above 0 V.
