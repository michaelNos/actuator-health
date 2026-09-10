# ACS724 stronger positive-current 100 Hz capture — 2026-09-10

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — ACS724 dynamic/FILTER validation  
**Status:** Stronger positive-current stimulus successfully captured; CH1 reference is high quality and CH2 coherent 100 Hz response becomes more visible, but the ACS724 transfer point is still **not accepted** because CH2 block-to-block magnitude/phase remain unstable.

## 1. Test condition

The MCP6022 positive-bias fixture was used with the established formal measurement convention:

- `CH1 = voltage across RREF = 68.8 ohm`;
- `CH2 = ACS724 VIOUT`;
- AFG frequency = 100 Hz;
- AFG amplitude setting = 1.00 Vpp;
- current direction = `220-ohm side -> ACS724 IP+ -> IP- -> RREF -> GND`;
- current remained strictly positive before the synchronized capture.

Immediately before moving CH2 from MCP6022 pin 1 to ACS724 VIOUT, the driver validation showed approximately:

- MCP6022 pin 1 = 2.520 V average, 1.020 Vpp, 100 Hz;
- RREF = 672.7 mV displayed average, 284 mV displayed raw Vpp;
- pin-1 waveform clean and visibly unclipped.

After CH2 was moved to ACS724 VIOUT, the screen still showed a 100 Hz CH1 waveform and a noisy CH2 waveform around the expected ~0.52 V sensor offset.

## 2. Uploaded frozen CSV pair

Files:

- `data_25_009.csv` = CH1;
- `data_25_010.csv` = CH2.

Both contain:

- 10,000 samples;
- sample interval = 20 us;
- sample rate = 50 kSa/s;
- record duration = 0.200 s;
- approximately 20 cycles at 100 Hz.

### CH1 raw facts

CSV metadata:

- reported frequency = 100.0 Hz;
- reported PK-PK = 256.0 mV;
- probe = 1X;
- voltage per ADC value metadata = 0.250 mV.

Raw exported values:

- mean = -9.8184 mV before display-position reconstruction;
- min = -144 mV;
- max = +112 mV;
- 65 distinct exported voltage levels.

The raw mean excludes the vertical-position display offset. The coherent AC component is unaffected by that display offset.

### CH2 raw facts

CSV metadata:

- scope automatic frequency estimate = 170.0 Hz; this is not used because CH2 is noise dominated and the known excitation is 100 Hz;
- reported PK-PK = 276.0 mV;
- probe = 1X;
- voltage per ADC value metadata = 0.125 mV.

Raw exported values:

- mean = 26.1248 mV before display-position reconstruction;
- standard deviation = 31.018 mV;
- min = -90 mV;
- max = +186 mV;
- 116 distinct exported voltage levels.

The corresponding scope screen showed the physical ACS724 VIOUT around ~525 mV after accounting for the CH2 vertical-position offset.

## 3. Coherent 100 Hz least-squares fit

Both channels were fitted at exactly 100 Hz using:

`v(t) = V0 + A*sin(2*pi*100*t) + B*cos(2*pi*100*t)`

with coherent peak-to-peak amplitude:

`Vpp,100 = 2*sqrt(A^2 + B^2)`.

### CH1 result

- coherent 100 Hz amplitude = **242.443 mVpp**;
- fit phase = -28.655 deg relative to CSV time origin;
- residual RMS = **3.629 mV**;
- fit R^2 = **0.99821**.

Using `RREF = 68.8 ohm`:

`Ipp,100 = 0.242443 / 68.8 = 3.5239 mApp`.

Therefore CH1 is a high-quality current reference for this capture.

### CH2 result

- coherent 100 Hz amplitude = **3.7077 mVpp**;
- fit phase = -17.398 deg relative to CSV time origin;
- residual RMS = **30.989 mV**;
- fit R^2 = **0.001786**.

The 100 Hz component is about **9.91 dB above the median neighboring-bin amplitude in the 50–150 Hz region**. This is a clear improvement over the previous lower-stimulus capture, where the local separation was only about 3.75 dB.

## 4. Provisional transfer calculation — NOT ACCEPTED

From the full-record coherent amplitudes:

`Ipp,100 = 3.5239 mApp`

`VOUTpp,100 = 3.7077 mVpp`

therefore:

`G100,provisional = 3.7077 mV / 3.5239 mA = 1.052 V/A`.

The fitted CH2-CH1 phase difference is approximately **+11.26 deg**.

For comparison, the prior DC calibration sensitivity `0.74472 V/A` would predict:

`VOUTpp,100,predicted = 0.74472 * 3.5239 mA = 2.624 mVpp`.

The stronger stimulus therefore moves the provisional gain closer to the DC-calibration value than the previous 1.247 V/A result, but the result is still not sufficiently stable to freeze.

## 5. Repeatability check

The 0.200 s record was split into four 5-cycle blocks. The inferred gains were approximately:

- block 1: 0.935 V/A;
- block 2: 1.696 V/A;
- block 3: 1.194 V/A;
- block 4: 0.917 V/A.

Corresponding CH2-CH1 phases were approximately:

- +48.3 deg;
- -6.8 deg;
- -14.7 deg;
- +43.2 deg.

This magnitude and phase spread remains too large for an accepted ACS724 transfer point.

## 6. Comparison with previous improved-resolution capture

Previous capture:

- CH1 coherent current = 1.7367 mApp;
- CH2 coherent output = 2.165 mVpp;
- provisional gain = 1.247 V/A;
- local 100 Hz separation ≈ 3.75 dB.

Current stronger-stimulus capture:

- CH1 coherent current = 3.5239 mApp, about **2.03x** larger;
- CH2 coherent output = 3.7077 mVpp, about **1.71x** larger;
- provisional gain = 1.052 V/A;
- local 100 Hz separation ≈ **9.91 dB**.

The stronger stimulus materially improves detectability of the coherent 100 Hz component, while CH2 broadband residual noise remains near 31 mV RMS.

## 7. Engineering conclusion

### Established

- 1.00 Vpp AFG setting produces a clean MCP6022 driver waveform around 2.52 V with about 1.02 Vpp modulation.
- The positive-current condition remains satisfied.
- CH1 coherent reference quality is excellent at the stronger stimulus.
- The coherent 100 Hz CH2 component grows and becomes more spectrally distinct as stimulus is increased.

### Not established

- accepted ACS724 100 Hz gain;
- accepted ACS724 100 Hz phase;
- stock FILTER transfer point;
- any external FILTER capacitor decision.

## 8. Next action

Increase the 100 Hz stimulus by one further controlled step while first measuring MCP6022 pin 1 and RREF to prove output headroom and strictly positive current. Then return CH2 to ACS724 VIOUT and acquire another synchronized frozen CH1/CH2 pair. The purpose is to improve CH2 coherent SNR and test whether gain/phase converge toward a stable value.

No FILTER capacitor is approved from this capture.
