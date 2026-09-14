# ACS724 VIOUT node isolation controls 038-040 — 2026-09-14

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — ACS724 dynamic/FILTER validation  
**Status:** Experimental diagnostic evidence; no high-frequency transfer magnitude accepted.

## 1. Purpose

This record continues the synchronized ACS724 noise-isolation study after files 030-037.

The immediate objective was to determine whether the approximately 15-17 mV RMS variation previously observed on ACS724 VIOUT was caused primarily by:

1. common oscilloscope/probe pickup;
2. loading caused by two scope probes attached simultaneously to VIOUT;
3. the powered MCP6022 stimulus fixture;
4. or electrical variation genuinely associated with the ACS724 VIOUT node or its local carrier/fixture environment.

These are temporary diagnostic test configurations. They do not represent product design changes.

Project workflow clarification established during this sequence:

- permanent or intended design/circuit changes must be reflected in the schematic before physical implementation;
- temporary diagnostic test configurations such as probe moves, opening a path, disconnecting a block, or temporarily powering a block down do not require a schematic revision first, but their exact configuration and results must be documented.

The external 4.7 nF FILTER capacitor remained installed throughout the tests below.

---

## 2. Common acquisition conditions

All captures used DOS1102S `Utility -> Source = ALL`, with synchronized CH1 and CH2 samples.

Common acquisition characteristics:

- 10,000 samples;
- `dt = 0.20000 us`;
- `fs = 5 MSa/s`;
- Sample acquisition mode;
- AFG OFF unless otherwise stated;
- ACS724 primary current path open;
- 4.7 nF external FILTER capacitor installed.

For these no-commanded-signal controls, the primary quantities of interest are:

- AC standard deviation/RMS about the mean;
- raw peak-to-peak amplitude;
- CH1/CH2 correlation coefficient;
- when useful, zero-mean channel-difference RMS.

Finite fitted amplitudes at arbitrary frequencies are not treated as physical tones unless independently supported.

---

## 3. File 038 — same-node GND/GND control

File:

`data_27_038_ALL_CH1-GND_CH2-GND_open_AFGOFF.csv`

Configuration:

- primary OPEN;
- AFG OFF;
- CH1 probe tip on ACS724 GND;
- CH2 probe tip on the same ACS724 GND point;
- both probe grounds referenced to common GND;
- MCP6022 fixture otherwise unchanged;
- 4.7 nF FILTER installed.

Measured statistics:

- CH1 GND AC standard deviation: approximately `1.78 mV RMS`;
- CH2 GND AC standard deviation: approximately `1.16 mV RMS`;
- CH1 raw data Vpp: approximately `36 mV`;
- CH2 raw data Vpp: approximately `28 mV`;
- CH1/CH2 correlation coefficient: approximately `0.037`;
- zero-mean CH1-CH2 difference RMS: approximately `2.09 mV`.

### Interpretation

This same-node GND/GND control is much quieter than the earlier same-node VIOUT/VIOUT control in file 037, where each channel showed approximately 15 mV RMS and the two channels were highly correlated.

Therefore the approximately 15 mV RMS waveform seen on VIOUT cannot be explained primarily as generic same-node common pickup produced by the two scope probes or channels.

The oscilloscope and probes are capable of producing a substantially quieter same-node measurement in the same general bench environment.

---

## 4. File 039 — single-probe VIOUT versus GND reference

File:

`data_27_039_ALL_CH1-OUT_CH2-GND_open_AFGOFF.csv`

Configuration:

- primary OPEN;
- AFG OFF;
- CH1 probe tip on ACS724 VIOUT;
- CH2 probe tip on ACS724 GND;
- only CH1 was attached to VIOUT;
- 4.7 nF FILTER installed.

Measured statistics:

- CH1 VIOUT AC standard deviation: approximately `17.13 mV RMS`;
- CH1 raw data Vpp: approximately `100 mV`;
- CH2 GND AC standard deviation: approximately `0.89 mV RMS`;
- CH2 raw data Vpp: approximately `16 mV`;
- VIOUT/GND correlation coefficient: approximately `0.0022`.

### Interpretation

The VIOUT variation remained in the same approximately 15-17 mV RMS range even after removing the second scope probe from VIOUT.

Therefore the high VIOUT variation observed in file 037 was not caused primarily by having two scope inputs simultaneously connected to the ACS724 output node.

At the same time, the GND reference remained quiet and essentially uncorrelated with VIOUT.

This strengthens the conclusion that the observed variation is associated specifically with the VIOUT node measurement rather than ordinary common-ground or probe-channel noise.

---

## 5. File 040 — MCP6022 powered down, primary still open

File:

`data_27_040_ALL_CH1-OUT_CH2-GND_open_AFGOFF_MCPoff.csv`

Configuration:

- primary OPEN;
- AFG OFF;
- MCP6022 stimulus block powered down;
- ACS724 remained powered;
- CH1 on ACS724 VIOUT;
- CH2 on ACS724 GND;
- 4.7 nF FILTER installed.

Measured statistics:

- CH1 VIOUT AC standard deviation: approximately `32.96 mV RMS`;
- CH1 raw data Vpp: approximately `220 mV`;
- CH2 GND AC standard deviation: approximately `1.83 mV RMS`;
- CH2 raw data Vpp: approximately `16 mV`;
- VIOUT/GND correlation coefficient: approximately `0.0315`.

### Interpretation

Powering down the MCP6022 did not eliminate the VIOUT variation. In this particular capture the VIOUT variation increased substantially.

This single result must not be interpreted as evidence that the powered MCP6022 reduces ACS724 noise. An unpowered op-amp that remains electrically connected can change impedances and current paths, so powering a block down is not necessarily an electrically neutral operation.

The valid conclusion is narrower:

**The approximately 15-17 mV RMS VIOUT variation was not eliminated by disabling the active MCP6022 stimulus source.**

A stronger isolation control was therefore required.

---

## 6. Stronger isolation — MCP6022 OFF and ACS724 primary terminals unattached

File:

`data_28_040_ALL_CH1-OUT_CH2-GND_open_AFGOFF_MCPoff_IP-IPplus unatached.csv`

The filename is retained exactly as captured, including its spelling.

Configuration:

- primary current path open;
- ACS724 `IP+` and `IP-` not connected into the temporary stimulus loop;
- AFG OFF;
- MCP6022 OFF;
- ACS724 remained powered;
- CH1 on ACS724 VIOUT;
- CH2 on ACS724 GND;
- 4.7 nF FILTER installed.

Measured statistics:

- CH1 VIOUT AC standard deviation: approximately `16.79 mV RMS`;
- CH1 raw data Vpp: approximately `116 mV`;
- CH2 GND AC standard deviation: approximately `1.49 mV RMS`;
- CH2 raw data Vpp: approximately `36 mV`;
- VIOUT/GND correlation coefficient: approximately `0.0027`.

### Interpretation

The approximately `32.96 mV RMS` value from the preceding MCP-OFF capture did not reproduce under stronger isolation.

Instead, VIOUT returned to approximately:

`16.79 mV RMS`,

which is very close to file 039:

`17.13 mV RMS`.

Therefore the earlier approximately 33 mV RMS observation is treated as a configuration-dependent or transient result and is not used as an accepted baseline.

More importantly, even with:

- zero primary current;
- AFG OFF;
- MCP6022 OFF;
- ACS724 primary terminals disconnected from the temporary stimulus loop;

VIOUT still showed approximately 17 mV RMS variation while the GND reference remained near 1.5 mV RMS and essentially uncorrelated.

This makes the active MCP6022/current-generation fixture an unlikely dominant source of the persistent approximately 15-17 mV RMS VIOUT baseline.

---

## 7. Combined interpretation of files 037-040

The control chain now supports the following observations:

1. **037 — VIOUT/VIOUT:** both channels on the same VIOUT node showed approximately 15 mV RMS each with correlation about `0.981`, proving that the dominant waveform was common to the measured node rather than independent channel noise.
2. **038 — GND/GND:** both channels on the same GND node were much quieter, approximately 1-2 mV RMS, with very low correlation. Therefore generic same-node probe pickup is not sufficient to explain the VIOUT waveform.
3. **039 — VIOUT/GND:** one probe on VIOUT still measured approximately `17.13 mV RMS` while the GND reference measured approximately `0.89 mV RMS`. Removing the second probe from VIOUT did not suppress the variation.
4. **040 MCP-OFF:** disabling the MCP6022 did not remove VIOUT variation; one capture increased to approximately 33 mV RMS, but this did not reproduce and is not accepted as a stable condition.
5. **Stronger isolation:** with the MCP6022 OFF and ACS724 primary terminals disconnected from the stimulus loop, VIOUT remained approximately `16.79 mV RMS` while GND remained quiet.

The strongest current conclusion is:

**The persistent approximately 15-17 mV RMS variation is genuinely associated with the ACS724 VIOUT node measurement and is not explained primarily by independent scope-channel noise, generic probe pickup, two-probe loading of VIOUT, simple GND movement, or the active MCP6022 stimulus fixture.**

This still does **not** prove that the ACS724 silicon itself is the sole source. Remaining mechanisms include:

- ACS724 output-stage behavior/noise;
- the Pololu carrier implementation;
- FILTER-node behavior;
- local breadboard/wiring pickup specifically coupled into VIOUT;
- other local electromagnetic or fixture coupling mechanisms.

---

## 8. Engineering consequence

The temporary stimulus fixture has now been sufficiently isolated to justify shifting attention toward the ACS724 carrier/output/filter behavior rather than continuing arbitrary disconnection tests.

No accepted 10 kHz ACS724 transfer magnitude is established by these controls.

The external 4.7 nF FILTER value remains an experimental Stage-B candidate and is not frozen.

A controlled FILTER-value experiment is a reasonable next investigation because earlier measurements showed that FILTER capacitance materially changes observed VIOUT residual noise. Any physical component-value change intended as a circuit-design experiment must be reflected in the schematic before implementation.

Temporary diagnostic probe moves, open circuits, block isolation, and power-down configurations remain exempt from the schematic-first requirement, provided the exact configuration is documented.
