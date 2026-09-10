# ACS724 first positive-current 100 Hz coherent capture — 2026-09-10

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — ACS724 dynamic/FILTER validation  
**Status:** First synchronized CH1/CH2 positive-current capture obtained; stimulus validity established, but sensor transfer magnitude is **not yet accepted** because measurement SNR/resolution is insufficient.

## 1. Purpose

This record documents the first synchronized CSV capture acquired after the MCP6022 positive-bias fixture was proven to keep the ACS724LLCTR-05AU primary current strictly positive.

The measurement convention is:

- `CH1 = voltage across RREF = 68.8 ohm`, therefore primary-current reference;
- `CH2 = ACS724 VIOUT`;
- frequency = 100 Hz;
- AFG drives MCP6022 channel A through `RIN = 99.1 kOhm`;
- MCP6022 channel-A feedback resistor `RF = 99.0 kOhm`;
- MCP6022 pin 1 drives `220 ohm -> ACS724 IP+ -> IP- -> RREF 68.8 ohm -> GND`;
- current direction was physically checked against the carrier `+i` arrow and is `220-ohm side -> RREF side`.

Immediately before this capture, scope measurements showed approximately:

- MCP6022 pin 1: 2.483 V average, 512 mVpp, 100 Hz;
- RREF: approximately 582.7 mV average and 160 mVpp;
- therefore the primary current remained positive throughout the cycle with substantial margin.

## 2. Uploaded CSV facts

Two CSV files from the same frozen acquisition were analyzed:

- `Ch1.csv`;
- `Ch2.csv`.

Both files contain:

- 10,000 samples;
- sample interval = 20 us;
- sample rate = 50 kSa/s;
- total record duration = 0.200 s;
- therefore exactly about 20 cycles of a 100 Hz signal.

### CH1 metadata / raw record

CSV metadata:

- channel = CH1;
- scope PK-PK metadata = 240 mV;
- probe attenuation = 1X;
- time interval = 20 us.

Raw-data statistics:

- mean = 577.032 mV;
- minimum = 400 mV;
- maximum = 640 mV;
- raw full-range span = 240 mV.

Important limitation: the exported CH1 record contains only four distinct voltage values:

- 400 mV;
- 480 mV;
- 560 mV;
- 640 mV.

This means the saved CH1 waveform is far too coarsely resolved for precision transfer-gain work. The screen was using a much larger vertical scale than needed for the approximately 0.58 V RREF signal. This is an acquisition-resolution limitation, not evidence that the current itself has only four physical levels.

### CH2 metadata / raw record

CSV metadata:

- channel = CH2;
- scope PK-PK metadata = 398 mV;
- probe attenuation = 1X;
- time interval = 20 us.

Raw CSV statistics before reconstructing the display offset:

- mean = 19.424 mV;
- standard deviation = 33.706 mV;
- minimum = -192 mV;
- maximum = 244 mV.

The scope screen for this capture showed CH2 at 50 mV/div with a -10.00-div vertical-position setting and an automatic average around 519.8 mV. The CSV mean of 19.424 mV is therefore consistent with approximately 519.4 mV physical VIOUT after accounting for the displayed 500 mV vertical-position displacement. This reconstruction is an inference from the screen plus CSV, not a separately documented CSV-format guarantee.

## 3. Coherent 100 Hz least-squares fit

Each channel was fitted at exactly 100 Hz using:

`v(t) = V0 + A*sin(2*pi*100*t) + B*cos(2*pi*100*t)`

The coherent peak amplitude is:

`Vpk = sqrt(A^2 + B^2)`

and coherent peak-to-peak amplitude is:

`Vpp,100 = 2*Vpk`.

### CH1 result

Coherent 100 Hz fit:

- mean/intercept = 577.032 mV;
- coherent 100 Hz amplitude = **167.807 mVpp**;
- fitted phase = approximately 88.17 deg relative to the CSV time origin;
- residual RMS after removing DC and 100 Hz fit = approximately 27.01 mV;
- fit R^2 = approximately 0.828.

Using `RREF = 68.8 ohm`:

`Iavg = 0.577032 / 68.8 = 8.387 mA`

`Ipp,100 = 0.167807 / 68.8 = 2.439 mApp`

The positive-current operating point is therefore consistent with the preceding scope observations. However, because the CH1 export has only four discrete voltage levels, the 167.8 mVpp coherent estimate is not accepted as a precision current-amplitude reference.

### CH2 result

Coherent 100 Hz fit of the raw AC record:

- coherent 100 Hz amplitude = **2.792 mVpp**;
- fitted phase = approximately 74.37 deg relative to the CSV time origin;
- residual RMS = approximately **33.69 mV**;
- fit R^2 = approximately **0.00086**.

The coherent 100 Hz component therefore explains only a tiny fraction of the total CH2 variation.

The 100 Hz component is also not strongly separated from nearby spectral noise. In the 50–150 Hz region, the 100 Hz component is about 2.79 mVpp while the median neighboring-bin amplitude is about 1.52 mVpp. This is only about 5.3 dB above that local median noise floor.

Five-cycle sub-block fits were not stable: the inferred CH2 magnitude and phase varied strongly between blocks. This prevents treating the present 100 Hz CH2 fit as a repeatable sensor response.

## 4. Provisional transfer calculation — NOT ACCEPTED

If the two coherent amplitudes are divided directly:

`Ipp,100 = 2.439 mApp`

`VOUTpp,100 = 2.792 mVpp`

then:

`G100,provisional = 2.792 mV / 2.439 mA = 1.145 V/A`.

The fitted CH2-CH1 phase difference is approximately -13.8 deg.

These numbers are **not accepted as ACS724 transfer evidence** because:

1. CH1 is severely coarsely quantized in the saved record;
2. CH2 residual noise is much larger than the coherent 100 Hz component;
3. the 100 Hz CH2 spectral component is only modestly above neighboring noise;
4. short-block magnitude/phase estimates are unstable;
5. the provisional 1.145 V/A result is far from the previously measured DC sensitivity of 0.74472 V/A and cannot presently be distinguished from measurement noise/bias.

For comparison only, the previous DC sensitivity would predict from the fitted CH1 current:

`0.74472 V/A * 2.439 mApp = 1.816 mVpp`

while nominal 0.8 V/A would predict approximately 1.951 mVpp.

The observed coherent CH2 value of 2.792 mVpp is therefore too uncertain to freeze as a gain measurement.

## 5. Engineering conclusion

### Established

- The MCP6022 positive-bias fixture can drive the ACS724 primary path with a positive DC-biased 100 Hz current.
- The first synchronized CH1/CH2 CSV pair was successfully captured from the same frozen acquisition.
- The primary-current mean remains about 8.4 mA.
- A coherent 100 Hz component is strong and obvious in CH1.
- A numerical 100 Hz component can be extracted from CH2, but it is not yet sufficiently dominant or repeatable for transfer-function acceptance.

### Not established

- accepted 100 Hz ACS724 AC gain;
- accepted 100 Hz phase;
- stock FILTER transfer point;
- any external FILTER capacitor decision.

## 6. Required next measurement improvement

The next capture should improve the measurement itself before any FILTER conclusion is attempted.

First priority: improve CH1 vertical resolution. The previous CH1 screen scale was 2 V/div while the signal of interest was only around 0.58 V DC with roughly 0.1–0.2 Vpp modulation. The next CH1 acquisition should use a substantially finer vertical sensitivity and use vertical position to keep the DC-biased waveform visible. This should produce many more resolved ADC/output levels in the exported CSV.

Second priority: increase the 100 Hz primary-current modulation in controlled steps while preserving a clearly positive current minimum and verifying that MCP6022 pin 1 remains undistorted and within output headroom. The purpose is to raise the ACS724 coherent 100 Hz component above the approximately tens-of-millivolts broadband/noise environment.

After the stronger stimulus is validated, capture CH1 and CH2 again from one frozen acquisition and repeat the coherent fit. Acceptance requires repeatable magnitude/phase and a transfer gain physically consistent with the independently established sensor behavior.

No FILTER capacitor is approved from this capture.