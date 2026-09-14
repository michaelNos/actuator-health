# ACS724 VIOUT node isolation and FILTER repeatability controls 038-044 — 2026-09-14

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — ACS724 dynamic/FILTER validation  
**Status:** Experimental diagnostic evidence; no high-frequency transfer magnitude accepted; no FILTER value frozen.

## 1. Purpose

This record continues the synchronized ACS724 noise-isolation study after files 030-037 and extends it through the controlled FILTER-capacitance sequence 041-044.

The immediate objectives were to determine whether the tens-of-millivolts RMS variation observed on ACS724 VIOUT was caused primarily by:

1. common oscilloscope/probe pickup;
2. loading caused by two scope probes attached simultaneously to VIOUT;
3. the powered MCP6022 stimulus fixture;
4. or electrical variation genuinely associated with the ACS724 VIOUT node or its local carrier/fixture environment.

A second objective was then to test whether the remaining VIOUT variation changed reproducibly with ACS724 FILTER capacitance.

These are temporary diagnostic test configurations. They do not represent a frozen product design change.

Project workflow clarification established during this sequence:

- permanent or intended design/circuit changes must be reflected in the schematic before physical implementation;
- temporary diagnostic test configurations such as probe moves, opening a path, disconnecting a block, temporarily powering a block down, or temporarily substituting FILTER capacitors for comparison do not require a schematic revision first, but their exact configuration and results must be documented.

---

## 2. Common acquisition conditions

All captures used DOS1102S `Utility -> Source = ALL`, with synchronized CH1 and CH2 samples.

Common acquisition characteristics for the zero-current isolation/FILTER captures:

- 10,000 samples;
- `dt = 0.20000 us`;
- `fs = 5 MSa/s`;
- Sample acquisition mode;
- AFG OFF unless otherwise stated;
- ACS724 primary current path open or primary terminals unattached as stated;
- CH1 on ACS724 VIOUT and CH2 on ACS724 GND for the single-output controls unless otherwise stated.

For these no-commanded-signal controls, the primary quantities of interest are:

- AC standard deviation/RMS about the mean;
- raw peak-to-peak amplitude;
- CH1/CH2 correlation coefficient;
- when useful, zero-mean channel-difference RMS.

Finite fitted amplitudes or oscilloscope auto-frequency readings are not treated as physical tones unless independently supported.

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

Removing the second scope probe from VIOUT did not suppress the variation. The GND reference remained quiet and essentially uncorrelated with VIOUT.

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

Powering down the MCP6022 did not eliminate the VIOUT variation. This single capture must not be interpreted as evidence that the powered MCP6022 reduces ACS724 noise because an unpowered op-amp remaining electrically connected can alter impedances and current paths.

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

The approximately `32.96 mV RMS` value from the preceding MCP-OFF capture did not reproduce under stronger isolation. Instead, VIOUT measured approximately `16.79 mV RMS` while GND remained quiet.

This made the active MCP6022/current-generation fixture unlikely to be the sole explanation of the observed VIOUT variation, but this `16.79 mV RMS` result is **not accepted as a stable +4.7 nF baseline** because the later controlled repeat in file 044 measured approximately `32.09 mV RMS` under the same intended strong-isolation condition.

The file remains valid evidence of what was measured in that capture; its earlier interpretation as a stable FILTER-noise baseline is superseded by the repeatability sequence below.

---

## 7. File 041 — stock FILTER configuration under strong isolation

File:

`data_28_041_ALL_CH1-OUT_CH2-GND_open_AFGOFF_MCPoff_IPopen_FILTERstock.csv.csv`

Configuration:

- primary current path open;
- ACS724 `IP+` and `IP-` unattached from the temporary stimulus loop;
- AFG OFF;
- MCP6022 OFF;
- ACS724 remained powered;
- CH1 on ACS724 VIOUT;
- CH2 on ACS724 GND;
- external 4.7 nF FILTER capacitor removed;
- Pololu carrier returned to its stock FILTER configuration.

Measured statistics calculated directly from the exported samples:

- CH1 VIOUT mean scope coordinate: `226.946 mV`;
- CH1 VIOUT AC standard deviation: `30.126 mV RMS`;
- CH1 raw data Vpp: `196 mV`;
- CH2 GND mean scope coordinate: `3.795 mV`;
- CH2 GND AC standard deviation: `1.646 mV RMS`;
- CH2 raw data Vpp: `52 mV`;
- VIOUT/GND correlation coefficient: `0.01358`;
- zero-mean CH1-CH2 difference RMS: `30.148 mV`.

### Superseded comparison note

When file 041 was first compared only against the preceding `16.79 mV RMS` +4.7 nF capture, the stock condition appeared to be approximately `1.79x` higher in RMS variation. That comparison was provisionally interpreted as evidence that the additional 4.7 nF capacitance materially reduced VIOUT noise.

The later controlled FILTER sweep and +4.7 nF repeat in files 042-044 do **not** reproduce that effect. Therefore the earlier `1.79x` comparison is retained only as historical traceability and must **not** be used as an accepted engineering conclusion.

---

## 8. File 042 — external +2.2 nF FILTER candidate

File:

`data_28_042_ALL_CH1-OUT_CH2-GND_open_AFGOFF_MCPoff_IPopen_FILTERplus2p2nF.csv`

Configuration:

- same strong-isolation test concept as file 041;
- primary open / `IP+` and `IP-` unattached from the temporary stimulus loop;
- AFG OFF;
- MCP6022 OFF;
- ACS724 powered;
- CH1 on VIOUT;
- CH2 on GND;
- stock carrier FILTER retained;
- external `2.2 nF` added from FILTER to GND;
- approximate total FILTER capacitance: `3.2 nF`;
- predicted first-order corner using `RF ~= 1.8 kOhm`: approximately `27.6 kHz`.

Acquisition:

- 10,000 samples;
- `dt = 0.20000 us`;
- `fs = 5 MSa/s`.

Measured statistics calculated directly from the exported samples:

- CH1 VIOUT mean scope coordinate: `226.209 mV`;
- CH1 VIOUT AC RMS: `30.461 mV`;
- CH1 raw data Vpp: `196 mV`;
- CH2 GND mean scope coordinate: `3.958 mV`;
- CH2 GND AC RMS: `1.029 mV`;
- CH2 raw data Vpp: `28 mV`;
- VIOUT/GND correlation coefficient: `0.02001`;
- zero-mean CH1-CH2 difference RMS: `30.458 mV`.

### Interpretation

The +2.2 nF condition did not show a meaningful reduction in broadband VIOUT RMS relative to the stock file 041 (`30.126 mV` versus `30.461 mV`).

---

## 9. File 043 — external +3.3 nF FILTER candidate

File:

`data_28_043_ALL_CH1-OUT_CH2-GND_open_AFGOFF_MCPoff_IPopen_FILTERplus3p3nF.csv`

Configuration:

- same strong-isolation test concept;
- primary open / `IP+` and `IP-` unattached;
- AFG OFF;
- MCP6022 OFF;
- ACS724 powered;
- CH1 on VIOUT;
- CH2 on GND;
- stock carrier FILTER retained;
- external `3.3 nF` added from FILTER to GND;
- approximate total FILTER capacitance: `4.3 nF`;
- predicted first-order corner using `RF ~= 1.8 kOhm`: approximately `20.6 kHz`.

Measured statistics calculated directly from the exported samples:

- CH1 VIOUT mean scope coordinate: `223.048 mV`;
- CH1 VIOUT AC RMS: `31.488 mV`;
- CH1 raw data Vpp: `216 mV`;
- CH2 GND mean scope coordinate: `3.905 mV`;
- CH2 GND AC RMS: `1.105 mV`;
- CH2 raw data Vpp: `32 mV`;
- VIOUT/GND correlation coefficient: `0.02182`;
- zero-mean CH1-CH2 difference RMS: `31.483 mV`.

### Interpretation

The +3.3 nF condition also did not show a broadband VIOUT RMS reduction. Its measured RMS was slightly higher than stock, but this single-capture difference is not interpreted as a physical noise increase caused by the capacitor.

---

## 10. File 044 — external +4.7 nF repeat under the controlled sweep configuration

File:

`data_28_044_ALL_CH1-OUT_CH2-GND_open_AFGOFF_MCPoff_IPopen_FILTERplus4p7nF_REPEAT.csv`

Configuration:

- same strong-isolation test concept;
- primary open / `IP+` and `IP-` unattached;
- AFG OFF;
- MCP6022 OFF;
- ACS724 powered;
- CH1 on VIOUT;
- CH2 on GND;
- stock carrier FILTER retained;
- external `4.7 nF` added from FILTER to GND;
- approximate total FILTER capacitance: `5.7 nF`;
- predicted first-order corner using `RF ~= 1.8 kOhm`: approximately `15.5 kHz`.

Measured statistics calculated directly from the exported samples:

- CH1 VIOUT mean scope coordinate: `225.962 mV`;
- CH1 VIOUT AC RMS: `32.095 mV`;
- CH1 raw data Vpp: `216 mV`;
- CH2 GND mean scope coordinate: `3.969 mV`;
- CH2 GND AC RMS: `0.385 mV`;
- CH2 raw data Vpp: `8 mV`;
- VIOUT/GND correlation coefficient: `0.02162`;
- zero-mean CH1-CH2 difference RMS: `32.089 mV`.

### Interpretation

This repeat is the critical result of the FILTER sweep.

The earlier strong-isolation +4.7 nF capture measured `16.79 mV RMS`. Under the later controlled sweep configuration, the +4.7 nF repeat measured `32.095 mV RMS`.

Therefore the earlier approximately `16.79 mV RMS` result did **not** reproduce. It must not be used as evidence that +4.7 nF reliably halves the measured broadband VIOUT RMS.

---

## 11. Controlled FILTER sweep summary

Using the directly calculated AC RMS values from files 041-044:

| External FILTER capacitor | Approx. total FILTER C | Predicted first-order corner | VIOUT AC RMS |
|---|---:|---:|---:|
| none; stock carrier only | ~1.0 nF | ~88.4 kHz | `30.126 mV` |
| +2.2 nF | ~3.2 nF | ~27.6 kHz | `30.461 mV` |
| +3.3 nF | ~4.3 nF | ~20.6 kHz | `31.488 mV` |
| +4.7 nF repeat | ~5.7 nF | ~15.5 kHz | `32.095 mV` |

The measured sequence is therefore approximately:

`30.13 -> 30.46 -> 31.49 -> 32.09 mV RMS`.

Within these single captures, there is **no demonstrated monotonic broadband-noise reduction with increasing FILTER capacitance**.

The values instead remain in the same approximately `30-32 mV RMS` region. The small upward progression must not be interpreted as proof that increasing FILTER capacitance increases ACS724 noise; repeat statistics and spectral characterization would be required before making such a claim.

The key accepted conclusion is only that the previously observed `16.79 mV RMS` +4.7 nF result is not repeatable enough to support a FILTER-noise-reduction conclusion.

---

## 12. Combined interpretation of files 037-044

The control chain supports the following observations:

1. **037 — VIOUT/VIOUT:** both channels on the same VIOUT node showed approximately 15 mV RMS each with correlation about `0.981`, demonstrating that the dominant waveform in that capture was common to the physical VIOUT node measurement rather than independent channel noise.
2. **038 — GND/GND:** both channels on the same GND node were much quieter, approximately 1-2 mV RMS, with very low correlation. Generic same-node probe pickup is therefore insufficient to explain the VIOUT waveform.
3. **039 — VIOUT/GND:** one probe on VIOUT still measured approximately `17.13 mV RMS` while GND measured approximately `0.89 mV RMS`. Removing the second VIOUT probe did not suppress the variation.
4. **040 MCP-OFF:** disabling the MCP6022 did not remove VIOUT variation. One capture increased to approximately 33 mV RMS, but a stronger-isolation repeat returned approximately 16.79 mV RMS, so the MCP-OFF level was not stable across configurations.
5. **Stronger isolation:** with the MCP6022 OFF and ACS724 primary terminals disconnected from the stimulus loop, VIOUT variation remained present while GND stayed quiet. This weakens the temporary current-stimulus fixture as the dominant source.
6. **041-044 FILTER sweep:** stock, +2.2 nF, +3.3 nF and the controlled +4.7 nF repeat all measured approximately `30-32 mV RMS` on VIOUT. The earlier `16.79 mV RMS` +4.7 nF result did not reproduce.

The strongest current conclusion is:

**A substantial electrical variation is associated with the ACS724 VIOUT measurement path and is not explained primarily by independent oscilloscope-channel noise, generic same-node probe pickup, two-probe loading, simple GND movement, or the active MCP6022 stimulus fixture. However, the current evidence does not establish a reproducible broadband-noise reduction from the tested external FILTER capacitors.**

This does **not** prove that the ACS724 silicon itself is the sole source. Remaining mechanisms include:

- ACS724 output-stage behavior/noise;
- the Pololu carrier implementation;
- FILTER-node behavior;
- local breadboard/wiring pickup specifically coupled into VIOUT;
- other local electromagnetic or fixture coupling mechanisms;
- capture-to-capture variation not yet fully characterized.

---

## 13. Engineering consequence and next action

The previous statement that the external +4.7 nF capacitor had demonstrated a material, reproducible broadband-noise reduction is **withdrawn/superseded** by files 042-044.

The 4.7 nF value remains an experimental Stage-B candidate and is not frozen. No FILTER value is accepted from the current broadband-RMS data alone.

No accepted 10 kHz ACS724 current-to-voltage transfer magnitude is established by these controls.

Before selecting a FILTER value, the next work must distinguish repeatability/capture variation from real frequency-dependent behavior. A suitable next experiment is to repeat the zero-current captures for each FILTER candidate multiple times under unchanged geometry and acquisition settings, and/or compare their spectra in defined frequency bands rather than relying only on one full-band RMS number.

After repeatability is established, candidate selection must still be checked against the frozen Rev-1 DC-10 kHz diagnostic-band requirement.

Until then:

- do not freeze the 4.7 nF value;
- do not claim that +4.7 nF halves broadband VIOUT RMS;
- do not infer monotonic FILTER-noise behavior from files 041-044;
- do not accept high-frequency CH2/current ratios as ACS724 transfer data.
