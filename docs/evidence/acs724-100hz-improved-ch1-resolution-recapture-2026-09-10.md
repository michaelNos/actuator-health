# ACS724 100 Hz improved-CH1-resolution recapture — 2026-09-10

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — ACS724 dynamic/FILTER validation  
**Status:** CH1 current-reference resolution successfully improved; CH2 ACS724 response remains below acceptance SNR/repeatability.

## 1. Purpose

This record documents the next synchronized 100 Hz CH1/CH2 frozen capture after the first positive-current measurement showed inadequate CH1 vertical resolution.

The circuit and measurement convention remain:

- `CH1 = voltage across RREF = 68.8 ohm`;
- `CH2 = ACS724 VIOUT`;
- frequency = 100 Hz;
- MCP6022 positive-bias fixture drives `220 ohm -> ACS724 IP+ -> IP- -> RREF -> GND`;
- primary current direction and positive-current margin had already been established before this capture;
- both CSVs were exported from one frozen acquisition.

Uploaded files analyzed:

- `data_25_005CH1frozen.csv`;
- `data_25_006CH2frozen.csv`.

## 2. CSV facts

Both files contain:

- 10,000 samples;
- sample interval = 20 us;
- sample rate = 50 kSa/s;
- record duration = 0.200 s;
- approximately 20 cycles at 100 Hz.

### CH1 metadata and resolution

CSV header:

- scope frequency = 100.0 Hz;
- scope PK-PK metadata = 140.0 mV;
- probe attenuation = 1X;
- reported `Voltage per ADC value` = 0.250000 mV;
- sample interval = 20 us.

The exported CH1 data contains **36 distinct voltage levels**, versus only four distinct levels in the previous coarse-scale capture. The observed exported-value spacing is mainly 4 mV.

Raw exported-data statistics (relative to the scope's vertical-position/export reference, not treated as the physical DC RREF level):

- mean = -11.868 mV;
- minimum = -72 mV;
- maximum = +72 mV;
- raw span = 144 mV.

The physical RREF DC operating point had already been measured on the scope at approximately 0.58 V before export; the CSV offset is therefore not used as a physical current mean.

### CH2 metadata

CSV header:

- scope-detected frequency = 26.32 Hz, which is not trusted because CH2 is noise dominated;
- scope PK-PK metadata = 406.0 mV;
- probe attenuation = 1X;
- reported `Voltage per ADC value` = 0.125000 mV;
- sample interval = 20 us.

Raw exported-data statistics:

- mean = +18.493 mV relative to the export/vertical-position reference;
- standard deviation = 33.289 mV;
- minimum = -192 mV;
- maximum = +250 mV;
- raw span = 442 mV;
- 145 distinct exported voltage values.

## 3. Exact 100 Hz coherent fit

Each channel was fitted at exactly 100 Hz using:

`v(t) = V0 + A*sin(2*pi*100*t) + B*cos(2*pi*100*t)`

with coherent peak-to-peak amplitude:

`Vpp,100 = 2*sqrt(A^2 + B^2)`.

### CH1 — current reference

Results:

- coherent 100 Hz component = **119.488 mVpp**;
- fitted phase = **+39.20 deg** relative to CSV time origin;
- residual RMS after removing DC and 100 Hz = **2.613 mV**;
- fit `R^2 = 0.9962`;
- 100 Hz spectral amplitude is about **60 dB above** the median neighboring spectral bins in the 50–150 Hz region.

This is a major improvement over the previous four-level CH1 export. CH1 is now a clean and well-resolved current reference for AC-amplitude work.

Using `RREF = 68.8 ohm`:

`Ipp,100 = 0.119488 / 68.8 = 1.7367 mApp`.

The physical positive-current margin remains governed by the independently measured ~0.58 V DC bias across RREF, not by the CSV's vertically shifted mean.

### CH2 — ACS724 output

Results:

- coherent 100 Hz component = **2.165 mVpp**;
- fitted phase = **+35.62 deg** relative to CSV time origin;
- residual RMS = **33.280 mV**;
- fit `R^2 = 0.000529`;
- 100 Hz spectral amplitude is only about **3.75 dB above** the median neighboring spectral bins in the 50–150 Hz region.

The full-record CH2 coherent component is therefore numerically extractable, but it remains much smaller than the broadband/noise disturbance.

## 4. Provisional direct transfer ratio — NOT ACCEPTED

From the full-record coherent amplitudes:

`Ipp,100 = 1.7367 mApp`

`VOUTpp,100 = 2.165 mVpp`

therefore:

`G100,provisional = 2.165 mV / 1.7367 mA = 1.247 V/A`.

Full-record fitted phase difference:

`phi_CH2 - phi_CH1 = -3.59 deg`.

These values are **not accepted** as ACS724 transfer evidence.

Reason: CH2 short-block behavior is unstable. Five-cycle block fits produced provisional gain values of approximately 2.15, 1.92, 0.69 and 1.06 V/A, with phase differences spanning roughly -37 deg to +59 deg. Two ten-cycle halves produced approximately 1.83 V/A and 0.75 V/A. This variation is much larger than an acceptable repeatability band.

The CH2 noise limitation therefore remains dominant even though CH1 has now been fixed.

For comparison only, the established DC sensitivity `0.74472 V/A` would predict:

`0.74472 * 1.7367 mApp = 1.293 mVpp`

at CH2 for this current modulation. The present 2.165 mVpp full-record fit cannot be distinguished confidently from noise/interference bias.

## 5. Engineering conclusion

### Established by this recapture

- The CH1 vertical-resolution problem from the first capture has been substantially corrected.
- CH1 now contains 36 distinct levels and a very clean coherent 100 Hz component.
- The coherent primary-current modulation is approximately **1.737 mApp** for this capture.
- A full-record 100 Hz component is still visible numerically in CH2.

### Not established

- accepted ACS724 100 Hz gain;
- accepted 100 Hz phase;
- stock FILTER transfer point;
- any external FILTER capacitor decision.

### Decision

Do not repeat the same low-amplitude capture again. The dominant limitation is now CH2 signal-to-noise ratio, not CH1 current-reference resolution.

The next experiment shall increase the 100 Hz stimulus in a controlled step, then re-prove:

1. MCP6022 pin-1 output remains clean and within headroom;
2. RREF waveform remains entirely above zero, proving positive primary current;
3. only after those checks, reconnect CH2 to ACS724 VIOUT and freeze/export a synchronized pair.

No ACS724 FILTER capacitor is approved from this recapture.