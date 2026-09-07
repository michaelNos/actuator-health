# ACS724 zero-current noise isolation — 2026-09-07

**Status:** Stage B bench evidence  
**Sensor:** Pololu #4048 ACS724LLCTR-05AU  
**Purpose:** isolate the source of the unexpectedly large zero-current ACS724 OUT disturbance before changing the sensor FILTER network or proceeding with further motor diagnostics.

## 1. Measurement configuration

Unless explicitly stated otherwise, the raw waveform captures used here were acquired with:

- physical oscilloscope probe: 1X
- CH1 probe setting: 1X
- horizontal scale: 50 ms/div
- memory depth: 10k
- 10,000 samples per CSV
- sample interval: 100 us
- sample rate: 10 kS/s
- record duration: 1.000 s
- motor physically removed during the supply/noise-isolation tests
- no additional ACS724 FILTER capacitance added

The 10 kS/s export has a 5 kHz Nyquist frequency and therefore does **not** validate the project's complete DC–10 kHz diagnostic band.

Primary broadband comparison metric is standard deviation after mean removal (`sigma`). Vpp is retained as a secondary metric because it is strongly affected by isolated excursions.

## 2. Authoritative file mapping

The following labels are authoritative for this experiment:

| File | Signal | Condition |
|---|---|---|
| `data_21_005.csv` | OUT | A1 — bench supply |
| `data_21_006.csv` | OUT | B1 — Arduino supply |
| `data_21_007.csv` | OUT | A2 — bench supply |
| `data_21_008.csv` | VCC | A1 — bench supply |
| `data_21_009.csv` | VCC | B1 — Arduino supply |
| `data_21_010.csv` | VCC | A2 — bench supply |
| `data_21_011.csv` | VCC | oscilloscope bandwidth limit OFF |
| `data_21_012.csv` | VCC | bandwidth limit OFF |
| `data_21_013.csv` | VCC | 20 MHz bandwidth limit ON |
| `data_21_014.csv` | VCC | bandwidth limit OFF |
| `data_21_015.csv` | OUT | 20 MHz bandwidth limit ON |
| `data_21_016.csv` | OUT | 20 MHz bandwidth limit ON |
| `data_21_017.csv` | OUT | 20 MHz bandwidth limit ON |

This mapping must not be inferred from file sequence; it records the actual bench signal for each capture.

## 3. Same-ground measurement floor

A control capture was made with both probe tip and probe ground connected to the same ACS724 GND node.

Result:

- `sigma_GND ≈ 1.43 mV`

This is substantially below the ACS724 OUT disturbance observed later. Therefore the approximately 30 mV OUT standard deviation cannot be attributed primarily to the oscilloscope/probe measurement floor under the tested configuration.

## 4. Supply-source A-B-A experiment

The sensor supply was changed while the motor was physically removed:

`bench 5 V (A1) -> Arduino 5 V (B1) -> bench 5 V (A2)`

Multimeter observations during this sequence were approximately:

- A1: VCC ≈ 5.00 V; OUT ≈ 0.49–0.50 V
- B1: VCC ≈ 4.66–4.67 V; OUT ≈ 0.469–0.470 V
- A2: VCC ≈ 5.00 V; OUT ≈ 0.50 V

The lower zero-current OUT under Arduino power is qualitatively consistent with the ACS724's ratiometric zero-output behavior and the lower measured VCC. These readings are raw bench observations, not a precision calibration.

### OUT noise

| Condition | File | sigma | sample Vpp |
|---|---|---:|---:|
| A1 bench | `005` | 30.13 mV | 242 mV |
| B1 Arduino | `006` | 29.97 mV | 374 mV |
| A2 bench | `007` | 31.08 mV | 500 mV |

The OUT standard deviation remained essentially unchanged:

`30.13 -> 29.97 -> 31.08 mV`

### VCC noise

| Condition | File | sigma | sample Vpp |
|---|---|---:|---:|
| A1 bench | `008` | 4.28 mV | 74 mV |
| B1 Arduino | `009` | 8.25 mV | 130 mV |
| A2 bench | `010` | 3.86 mV | 68 mV |

The Arduino rail was measurably noisier in this test:

`4.28 -> 8.25 -> 3.86 mV`

The A-B-A return to approximately 4 mV on the bench supply supports repeatability of the supply-source effect.

## 5. Interpretation of supply-source experiment

Changing from the bench supply to the Arduino approximately doubled measured VCC noise, but ACS724 OUT remained near 30 mV in all three conditions.

Therefore:

**The sensor power source is not the dominant cause of the approximately 30 mV zero-current OUT disturbance under this bench configuration.**

The Arduino rail is measurably noisier, but the OUT disturbance does not track that change.

For bench power, the observed OUT standard deviation is approximately seven times the approximately 4.1 mV VCC standard deviation. Even the Arduino VCC result of 8.25 mV remains far below the approximately 30 mV OUT result.

This comparison is evidence against a simple interpretation in which OUT is merely reproducing supply ripple.

## 6. Oscilloscope 20 MHz bandwidth-limit control on VCC

A VCC A-B-A bandwidth-limit test was performed while holding the rest of the configuration fixed:

- `012`: limit OFF — sigma ≈ 5.41 mV, sample Vpp ≈ 104 mV
- `013`: 20 MHz limit ON — sigma ≈ 3.89 mV, sample Vpp ≈ 94 mV
- `014`: limit OFF — sigma ≈ 5.26 mV, sample Vpp ≈ 98 mV

This gives:

`OFF 5.41 -> ON 3.89 -> OFF 5.26 mV`

The result is physically consistent with the bandwidth limiter reducing measured high-frequency noise. It also demonstrates repeatable A-B-A behavior.

The bench VCC captures contain a noticeable approximately 50 Hz component, consistent with environmental/mains pickup, but this component is much smaller than the total approximately 30 mV OUT standard deviation.

## 7. Repeated OUT captures with 20 MHz limit

Three repeated OUT captures were then taken with the 20 MHz bandwidth limit enabled:

| File | sigma | sample Vpp |
|---|---:|---:|
| `015` | 29.85 mV | 250 mV |
| `016` | 29.11 mV | 220 mV |
| `017` | 29.68 mV | 256 mV |

Mean standard deviation across these three records:

`mean sigma_OUT ≈ 29.55 mV`

This independently confirms that the approximately 29–31 mV OUT disturbance is repeatable in the present setup.

The strongest individual low-frequency FFT components in these OUT records are only of order approximately 1–1.3 mVrms and are not a single stable dominant 50 Hz tone. The observed disturbance is therefore largely broadband within the recorded spectrum rather than being explained by one large mains-frequency component.

## 8. Established findings

The experiment establishes the following Stage B evidence:

1. The same-ground scope/probe floor is approximately **1.43 mV sigma** under the tested acquisition configuration.
2. ACS724 zero-current OUT repeatedly measures approximately **29–31 mV sigma**.
3. The motor and its current-path wiring were physically absent during these isolation measurements, so the observed OUT disturbance is not caused by motor operation or pickup through connected motor wiring in this test.
4. Arduino VCC is noisier than bench VCC in the A-B-A test, approximately **8.25 mV versus about 4 mV sigma**.
5. Despite that VCC change, OUT remains approximately **30 mV sigma**.
6. Therefore the sensor supply source is **not the dominant cause** of the observed OUT disturbance.
7. Enabling the oscilloscope 20 MHz bandwidth limit reduces measured VCC noise as expected.
8. Repeated OUT captures with the 20 MHz limit enabled remain approximately **29–30 mV sigma**, confirming that the large OUT disturbance persists under the standard measurement configuration.

## 9. What has NOT been established

These measurements do not yet establish:

- the intrinsic noise of the ACS724 IC itself
- whether the stock carrier FILTER network is behaving exactly as intended
- the quantitative effect of adding FILTER capacitance
- the complete analog transfer function of the sensor/output chain
- the full DC–10 kHz project-band noise performance
- production-level noise or current resolution
- whether all observed broadband disturbance originates inside the sensor rather than through output-node coupling or the physical bench implementation

No fault/health diagnostic claim should be based on this noise-isolation experiment alone.

## 10. Next engineering task

The next controlled investigation is the **ACS724 output bandwidth / FILTER behavior**.

The purpose is to determine whether deliberately reducing the sensor output bandwidth produces the expected reduction in zero-current OUT noise and to quantify the trade-off between noise and usable diagnostic bandwidth.

The FILTER network must not be changed arbitrarily. Before adding capacitance:

1. confirm the stock Pololu #4048 FILTER implementation and present effective bandwidth from authoritative hardware documentation
2. calculate candidate FILTER capacitances and predicted bandwidths
3. select one controlled test value that preserves a justified diagnostic bandwidth
4. record a baseline OUT capture immediately before modification
5. add the selected capacitance using a controlled, documented connection
6. repeat the identical zero-current OUT capture
7. compare sigma, Vpp, and Hamming-window spectrum
8. remove/restore the baseline configuration if practical and repeat to establish A-B-A evidence

The formal project diagnostic band remains **DC–10 kHz**. Any filter experiment must therefore be interpreted against that requirement rather than optimizing noise alone.
