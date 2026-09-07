# ACS724 Noise, Bandwidth and FFT — Study Notes

These notes capture the learning from the first oscilloscope noise investigation around the ACS724 current-sensor output.

They are educational support material. Formal accepted bench results are recorded separately under `docs/`.

## 1. Why the multimeter looked clean while the oscilloscope looked noisy

A multimeter mainly reports a slowly varying or averaged voltage. It rejects or averages much of the fast variation that an oscilloscope can display.

So both observations can be true at the same time:

- multimeter: `VOUT ≈ 0.49 V`
- oscilloscope: `0.49 V + fast fluctuations`

The multimeter is useful for the DC operating point. The oscilloscope is required to see time-dependent behavior.

## 2. Bandwidth controls how much noise we observe

Every measurement system has bandwidth.

A wider bandwidth admits a wider range of frequency components, including useful signal and noise.

Conceptually:

`measured signal = useful signal within bandwidth + admitted noise within bandwidth`

Reducing bandwidth can reduce observed noise, but it can also remove real signal content.

Therefore filtering is not simply "make the trace prettier". The filter bandwidth must be selected from the signal band that the system is required to preserve.

For this project the formal diagnostic band is DC to 10 kHz. Any analog filtering decision must preserve that requirement.

## 3. Oscilloscope 20 MHz bandwidth limit experiment

The DOS1102S channel bandwidth limit was enabled while observing ACS724 OUT.

The displayed disturbance changed very little.

Interpretation:

The dominant disturbance was not primarily in the 20–110 MHz portion removed by the bandwidth limit.

This does not identify the source. It only rules out one simple hypothesis.

## 4. Why control measurements matter

Before assigning noise to the sensor, measure the instrument/setup floor.

A useful sequence is:

1. probe tip shorted to probe ground / same reference node
2. sensor VCC ripple
3. sensor OUT at zero current
4. sensor OUT with motor running

The principle is:

**change one thing at a time and keep the acquisition settings identical wherever the results are to be compared quantitatively.**

If settings change, the result can remain useful as a learning observation but should not be treated as a strict numerical comparison.

## 5. RMS versus peak-to-peak noise

Peak-to-peak is:

`Vpp = Vmax - Vmin`

It is strongly affected by rare spikes.

RMS-type noise better reflects the average energy of a varying signal, although the exact statistical meaning depends on how the instrument calculates it and whether the DC mean has been removed.

For noise analysis, a preferred exported-data quantity is standard deviation after removing the mean:

`σV = std(V - mean(V))`

If the current-sensor sensitivity is known:

`σI = σV / S`

For the measured low-current calibration:

`S ≈ 0.74472 V/A`

This converts voltage-domain noise to equivalent current-domain noise.

## 6. AC coupling versus DC coupling

### DC coupling

DC coupling preserves both the DC operating point and AC variation.

Use it when the absolute sensor voltage matters.

Example:

`VOUT ≈ 0.469 V + noise`

### AC coupling

AC coupling blocks the large DC component at the oscilloscope input and displays mainly the changing part.

This is useful when a small ripple is riding on a much larger DC level.

Example:

`4.63 V supply + small ripple`

can be displayed as approximately:

`small ripple around 0 V`

AC coupling changes the measurement path inside the oscilloscope; it does not change the circuit under test.

## 7. Vertical scale versus vertical position

Vertical scale answers:

**How many volts does one grid division represent?**

Example:

`20 mV/div`

Vertical position/offset answers:

**Which part of the voltage range is placed on the visible screen?**

Changing position does not amplify the signal and does not change the circuit voltage. It only moves the viewing window.

## 8. Signal-path sanity check

A major practical lesson occurred when the probe BNC was accidentally connected to the DOS1102S AFG output instead of CH1.

The multimeter correctly measured the ACS724 output while CH1 appeared near zero because CH1 was not actually connected to the probe.

Before debugging trigger, offset, or scaling, check:

- probe tip node
- probe ground node
- physical BNC input
- selected channel
- probe 1X/10X switch
- scope probe factor
- AC/DC coupling
- bandwidth limit

A wrong physical signal path cannot be repaired with software/menu settings.

## 9. What FFT does

The oscilloscope time-domain view shows:

`voltage versus time`

FFT transforms a sampled record into an estimate of:

`amplitude versus frequency`

It is useful for asking whether a waveform contains repeatable periodic components.

For a motor-current signal, possible repeatable components could be associated with rotation, commutation, load periodicity, or electrical switching.

A real useful motor-related component would ideally appear as a repeatable peak that increases or appears in the motor-ON spectrum compared with motor OFF.

## 10. FFT center frequency and span

Two controls must not be confused:

- **Hz/div** = horizontal frequency scale
- **center frequency** = frequency at the middle of the FFT display

Example:

`125 Hz/div` with center `625 Hz`

across about 10 divisions gives approximately:

`0 to 1.25 kHz`

Changing only Hz/div while leaving the center at 6.25 kHz would instead zoom into a narrow region around 6.25 kHz, not the low-frequency region.

## 11. Window functions

An FFT uses a finite record. Cutting a non-periodic signal at the record boundaries can spread spectral energy into neighboring frequency bins. This is spectral leakage.

A window function reduces the edge discontinuity before the FFT.

A Hanning window is a useful general-purpose choice for exploratory spectrum inspection.

Window choice affects spectral amplitude and resolution, so it should be documented for quantitative analysis.

## 12. Why the exploratory OFF/ON FFT was inconclusive

The motor-OFF and motor-ON spectra looked broadly similar in the inspected 0–1.25 kHz and 0–12.5 kHz views.

This means only:

**no obvious stable motor-related line was resolved above the existing background with the present setup.**

It does not prove that the motor has no spectral signature.

Reasons include:

- low current amplitude
- large sensor/output-chain noise
- breadboard/probe pickup
- limited FFT record quality
- no averaging
- screenshots rather than exported data
- insufficient frequency resolution or SNR

## 13. Why exported waveform data are better

A screenshot is excellent for documenting instrument state and a qualitative waveform.

For quantitative work, exported samples are much better because MATLAB can calculate:

- mean
- standard deviation
- RMS
- peak-to-peak
- FFT with controlled windowing
- averaged spectra
- exact peak frequencies
- equivalent current noise

The original scope export should be preserved unchanged before analysis.

## 14. Review questions

**Q:** Why can a multimeter show a stable 0.49 V while the scope shows a noisy waveform around the same level?  
**A:** The multimeter largely averages fast variation; the oscilloscope resolves time-dependent components over a much wider bandwidth.

**Q:** Why does reducing measurement bandwidth often reduce noise?  
**A:** Less frequency range is admitted, so less noise power is included, provided the removed band does not contain required signal information.

**Q:** Does a 20 MHz bandwidth limit test the project's final anti-alias filter?  
**A:** No. It only removes the scope channel content above approximately 20 MHz. The project diagnostic band and AFE anti-alias design operate at much lower frequencies.

**Q:** Why is peak-to-peak not enough to characterize random noise?  
**A:** It is dominated by the largest positive and negative excursions and is sensitive to rare spikes and observation time.

**Q:** What is the difference between FFT scale and FFT center frequency?  
**A:** Scale defines frequency per division; center defines which frequency lies at the middle of the display.

**Q:** What would constitute convincing motor spectral evidence?  
**A:** A repeatable component at a stable frequency/amplitude relationship that appears or changes consistently with motor operation under controlled identical acquisition conditions.

**Q:** Why should we not add arbitrary filtering immediately?  
**A:** Filtering can also remove useful diagnostic content. The required DC–10 kHz band and the designed AFE must be respected, and the noise source should first be measured reproducibly.
