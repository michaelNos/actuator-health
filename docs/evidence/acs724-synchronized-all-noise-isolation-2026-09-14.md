# ACS724 synchronized ALL-export and VIOUT noise-isolation study — 2026-09-14

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — ACS724 dynamic/FILTER validation  
**Status:** Experimental diagnostic evidence; high-frequency transfer magnitude remains unaccepted.

## 1. Purpose

This record continues the 4.7 nF ACS724 FILTER investigation after the initial 10 kHz open-primary experiment.

The immediate goals were to:

1. verify whether the DOS1102S `Utility -> Source = ALL` export provides synchronized CH1/CH2 samples in one CSV;
2. re-establish the closed-primary schematic state after the earlier open-primary control;
3. test whether the apparent 10 kHz VIOUT component with the primary path open is a stable coherent feedthrough phasor;
4. determine whether the approximately 15-17 mV RMS VIOUT residual is explained primarily by ACS724 VCC noise, ground movement, oscilloscope-channel noise, or real electrical variation present at the VIOUT node.

This record does not freeze the 4.7 nF FILTER value and does not establish an accepted 10 kHz ACS724 transfer magnitude.

---

## 2. Common acquisition conditions

For the synchronized 10 kHz work, the DOS1102S ALL export contains both channels in one CSV:

- `CH1_Voltage(mV)`;
- `CH2_Voltage(mV)`.

The valid records use:

- 10,000 samples;
- `dt = 0.20000 us`;
- `fs = 5 MSa/s`;
- 500 samples per commanded 10 kHz cycle.

This is important because CH1 and CH2 then share the same sample index and time base. Relative phase within one ALL file is therefore much better defined than phase inferred from separately exported channel files.

Commanded-frequency amplitude is obtained from the coherent least-squares model:

`v(t) = V0 + A*sin(2*pi*f*t) + B*cos(2*pi*f*t)`.

Coherent peak-to-peak amplitude is:

`Vpp,f = 2*sqrt(A^2 + B^2)`.

Residual RMS is calculated after removal of the fitted DC and commanded-frequency term.

---

## 3. File 030 — returned-to-schematic current-on state

File:

`data_27_030_ALL_10kHz_filter4.7_100us.csv`

Configuration:

- primary path CLOSED;
- `MCP6022 pin 1 -> 220 Ohm -> ACS724 IP+ -> ACS724 IP- -> R8 -> GND`;
- `R8 = 67 Ohm`;
- external 4.7 nF FILTER capacitor still installed;
- CH1 across R8;
- CH2 on ACS724 VIOUT;
- AFG commanded at 10 kHz.

Fixed-10-kHz coherent fit:

- CH1 coherent: `475.733 mVpp`;
- CH1 residual RMS: `4.026 mV`;
- inferred primary current: `475.733 mVpp / 67 Ohm = 7.1005 mApp`;
- CH2 coherent: `7.794 mVpp`;
- CH2 residual RMS: `17.595 mV`.

The CH1 amplitude agrees with the previous valid current-on 10 kHz captures near 471-476 mVpp. This supports that the physical primary-current path had been successfully restored to the documented schematic state.

The CH2 coherent component remains small relative to its residual, so it is not accepted as Hall-current transfer response.

---

## 4. File 031 — closed primary with CH1 moved to MCP6022 pin 1

File:

`data_27_031_All_CH1-pin1_10kHz.csv`

Configuration:

- primary path CLOSED;
- no circuit wiring change from the restored state;
- CH1 probe tip moved from R8 to MCP6022 pin 1;
- CH2 remained on ACS724 VIOUT;
- AFG remained at 10 kHz.

Fixed-10-kHz coherent fit:

- CH1 coherent: `2.00152 Vpp`;
- CH1 residual RMS: `19.857 mV`;
- CH1 phase relative to the common CSV time origin: `95.13 deg`;
- CH2 coherent: `5.720 mVpp`;
- CH2 residual RMS: `16.612 mV`;
- CH2 phase relative to the common CSV time origin: `2.49 deg`.

Relative CH2-to-CH1 phase within this capture is approximately:

`2.49 - 95.13 = -92.63 deg`.

This file established a synchronized closed-primary driver-reference measurement.

---

## 5. Files 032 and 033 — synchronized open-primary repeatability test

For both captures:

- the primary path was OPEN between the 220-Ohm resistor and ACS724 `IP+`;
- CH1 remained on MCP6022 pin 1;
- CH2 remained on ACS724 VIOUT;
- AFG remained commanded at 10 kHz;
- 4.7 nF FILTER remained installed;
- export source was ALL.

### File 032

`data_27_032_All_CH1-pin1_10kHz_open.csv`

- CH1 coherent: `1.99948 Vpp`;
- CH1 residual RMS: `19.992 mV`;
- CH2 coherent: `5.850 mVpp`;
- CH2 residual RMS: `16.926 mV`;
- CH2-to-CH1 relative phase: approximately `-171.88 deg`.

### File 033 repeat

`data_27_033_All_CH1-pin1_10kHz_open_repeat.csv`

- CH1 coherent: `2.00010 Vpp`;
- CH1 residual RMS: `19.657 mV`;
- CH2 coherent: `3.144 mVpp`;
- CH2 residual RMS: `16.149 mV`;
- CH2-to-CH1 relative phase: approximately `+139.44 deg`.

### Interpretation

CH1 repeated extremely closely, so the commanded 10 kHz drive was stable.

CH2 did not repeat as a stable coherent phasor:

- coherent amplitude changed from approximately `5.85 mVpp` to `3.14 mVpp`;
- relative phase changed materially.

Therefore the open-primary component cannot be treated as a stable correction phasor under the present test conditions.

A vector subtraction performed using only one closed/open pair may be mathematically defined for those two individual records, but the repeat demonstrates that the assumed feedthrough phasor is not sufficiently repeatable to support a trustworthy corrected Hall-response result.

**Consequence:** no 10 kHz phasor correction or corrected sensitivity is accepted.

---

## 6. File 034 — open primary, AFG OFF

File:

`data_27_034_All_CH1-pin1_10kHz_open_AFGOFF.csv`

Configuration:

- primary path OPEN;
- AFG output OFF;
- CH1 on MCP6022 pin 1;
- CH2 on ACS724 VIOUT;
- same scope acquisition settings.

With no commanded 10 kHz stimulus, a forced mathematical 10 kHz fit still returns finite projections:

- CH1 forced 10 kHz component: `0.868 mVpp`;
- CH1 residual RMS: `17.731 mV`;
- CH2 forced 10 kHz component: `3.248 mVpp`;
- CH2 residual RMS: `16.606 mV`.

Because the AFG is OFF, the finite 10 kHz fit must not be interpreted as evidence of a commanded 10 kHz transfer or feedthrough tone. A forced sine fit to structured/broadband noise can always produce a non-zero projection.

The oscilloscope automatic frequency estimate on CH2 was approximately 8.969 kHz, but this is not treated as an accepted physical tone because the full spectrum contains multiple components rather than one dominant stable line.

---

## 7. File 035 — ACS724 VCC versus VIOUT

File:

`data_27_035_All_CH1-pin1_open_AFGOFF.csv`

The filename was copied from the previous capture and is misleading. The bench configuration was confirmed as:

- primary path OPEN;
- AFG OFF;
- CH1 physically on ACS724 VCC;
- CH2 on ACS724 VIOUT.

Measured AC statistics:

- CH1 VCC residual RMS: approximately `17.53 mV`;
- CH2 VIOUT residual RMS: approximately `16.53 mV`;
- CH1/CH2 raw waveform correlation coefficient: `-0.0011`.

The near-zero correlation and non-matching dominant spectral structure provide no evidence that the observed VIOUT variation is simply a direct copy of the measured VCC variation in this configuration.

The CSV DC coordinate on CH1 must not be used as a physical VCC DC measurement because the scope export includes channel vertical offset/coordinate effects. This experiment is interpreted only for AC/noise behavior.

---

## 8. File 036 — ACS724 GND versus VIOUT

File:

`data_27_036_ALL_CH1-GND_CH2-OUT_open_AFGOFF.csv`

Configuration:

- primary path OPEN;
- AFG OFF;
- CH1 probe tip on ACS724 GND;
- CH2 on ACS724 VIOUT.

Measured AC statistics:

- CH1 GND AC standard deviation: `13.779 mV`;
- CH2 VIOUT AC standard deviation: `15.645 mV`;
- CH1/CH2 raw waveform correlation coefficient: `0.0285`.

The near-zero correlation and non-matching spectral structure provide no evidence that the observed VIOUT variation is simply common-ground movement in this configuration.

The exported CH1 mean was approximately `-2.995 V` even though the probe tip was physically on the common ground node. This demonstrates that exported DC coordinates can include scope vertical-position/offset information and must not be interpreted as physical node DC voltage without an appropriate reference check.

---

## 9. File 037 — same-node oscilloscope control

File:

`data_27_037_ALL_CH1-OUT_CH2-OUT_open_AFGOFF.csv`

Configuration:

- primary path OPEN;
- AFG OFF;
- both CH1 and CH2 probe tips on the same ACS724 VIOUT node;
- both probe grounds referenced to the common ground;
- 4.7 nF FILTER still installed.

Measured statistics:

- CH1 raw data Vpp: `88 mV`;
- CH2 raw data Vpp: `88 mV`;
- CH1 AC standard deviation: `15.071 mV`;
- CH2 AC standard deviation: `15.388 mV`;
- CH1/CH2 correlation coefficient: `0.9812`;
- RMS of the zero-mean channel-to-channel difference: `2.973 mV`.

The very high same-node correlation is the strongest isolation result in this sequence.

If independent oscilloscope-channel noise were responsible for most of the approximately 15 mV RMS VIOUT variation, two probes on the same physical node would not be expected to reproduce nearly the same instantaneous waveform. Instead the two channels track each other closely.

Therefore the dominant measured variation is common to the physical VIOUT node measurement, rather than being predominantly independent CH1/CH2 oscilloscope-channel noise.

This does **not** prove that the ACS724 IC itself generates the variation. Common pickup at the VIOUT node, breadboard/wiring coupling, sensor-output behavior, grounding geometry, probe pickup, or other fixture mechanisms remain possible.

---

## 10. Accepted observations from files 030-037

The following observations are accepted:

1. DOS1102S `Utility -> Source = ALL` produces CH1 and CH2 data in one CSV with a common sample index/time base and is the preferred export mode for synchronized two-channel analysis.
2. File 030 demonstrates that the primary-current path was successfully restored to the schematic state after the earlier open-primary test; its CH1 current-reference amplitude is consistent with previous valid 10 kHz current-on captures.
3. The MCP6022 10 kHz drive is highly repeatable in the synchronized open-primary repeats 032/033.
4. The apparent open-primary 10 kHz VIOUT component is **not** a sufficiently stable phasor for quantitative subtraction: amplitude and relative phase changed materially between repeated captures.
5. A forced 10 kHz fit returns a finite VIOUT projection even with the AFG OFF. Therefore small 10 kHz fit results in this noise environment must not automatically be interpreted as a physical 10 kHz tone.
6. The VCC/VIOUT control showed essentially zero raw waveform correlation (`-0.0011`); the present data do not support VCC ripple as a simple direct explanation of VIOUT noise.
7. The GND/VIOUT control showed essentially zero raw waveform correlation (`0.0285`); the present data do not support common-ground movement as a simple direct explanation of VIOUT noise.
8. The same-node VIOUT/VIOUT control produced very high correlation (`0.9812`) with only about `2.97 mV RMS` zero-mean channel difference while each channel contained about `15 mV RMS` AC variation. This demonstrates that most of the measured VIOUT variation is common to the node measurement rather than independent oscilloscope-channel noise.
9. No accepted 10 kHz ACS724 current-to-voltage transfer magnitude has yet been established.
10. The external 4.7 nF FILTER capacitor remains an experimental Stage-B candidate, not a frozen product value.

---

## 11. Correction/refinement to the earlier 4.7 nF evidence record

The earlier evidence record documented an open-primary 10 kHz component of approximately 7.114 mVpp and described coherent fixture/environment coupling as demonstrated.

The synchronized ALL-export repeats in this record refine that interpretation:

- an open-primary VIOUT component at or near the commanded 10 kHz frequency can be observed;
- however its fitted amplitude and phase are not repeatable enough under the present conditions to support a stable feedthrough-phasor model;
- finite forced 10 kHz projections also remain with the AFG OFF.

Therefore the prior observation must **not** be used as a fixed scalar or phasor correction for current-on data.

The robust conclusion is narrower:

**The present high-frequency VIOUT measurement is noise/coupling limited, and the small coherent component cannot yet be separated reliably into Hall response and fixture/environment contributions.**

The original record is retained as historical evidence; this document adds the repeatability controls and updated interpretation rather than silently rewriting the earlier measurement.

---

## 12. Engineering consequence and next action

The diagnostic sequence has isolated several possibilities without changing the circuit topology:

- commanded current generation is stable;
- simple VCC-copy behavior is not supported;
- simple ground-copy behavior is not supported;
- independent oscilloscope-channel noise is not the dominant explanation for the approximately 15 mV RMS VIOUT variation;
- substantial common electrical variation is present at the VIOUT measurement node or enters both probes through a common physical pickup mechanism there.

The next work should isolate the physical source of this VIOUT-node variation before attempting another high-frequency transfer measurement.

Candidate next investigations must preserve the project rule:

**before any physical circuit modification, update the schematic first.**

Until that isolation is complete, do not accept high-frequency CH2/current ratios or phasor-subtracted values as ACS724 sensitivity/transfer data.
