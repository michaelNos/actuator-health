# Deterministic ADC Acquisition — From Motor Current to Trustworthy Samples

Actuator Health Monitoring System — study note, 2026-10-12.

**Purpose:** Understand **what**, **why**, and **how** the selected MCU, ADC, sampling rate, hardware timer, transfer mechanism, and double buffering work together *before* implementation or schematic changes.

**Status:** Educational derivations and implementation concepts. This is **not** Stage-B verification evidence and does not claim a working 100 kS/s firmware implementation.

**Project authority:** [Phase 6 ADC design](../docs/06-adc-deterministic-acquisition.md), [Phase 7 firmware architecture](../docs/07-firmware-signal-processing.md), and [Phase 12 integration specification](../docs/12-system-integration-build-specification.md). Follow [RULES.md](../RULES.md). The frozen Rev-1 product path is **ACS724 → MCP6022 AFE → UNO A0 / RA4M1 ADC → RAM buffers → processing → USB/PC**. Internal peripheral routing, actual ADC reference, and buffer lengths must still be verified/selected in Stage B.

## 1. MCU: Why the UNO R4 WiFi / RA4M1?

### What is an MCU?

A **microcontroller (MCU)** is a small computer on one chip: CPU, RAM, program storage, GPIO, timers, analog peripherals, and interrupt mechanisms. The **Arduino UNO R4 WiFi** is the development board; the **Renesas RA4M1** is the main MCU that performs our measurements and calculations. Arduino provides convenient libraries, but our regular sampling times must be controlled by MCU hardware, not the speed of a user-written loop.

The project specifies an RA4M1 operating at **48 MHz**. This is the CPU/peripheral clock scale given in Phase 6, **not** the ADC sampling frequency.

An illustrative comparison:

$$
\frac{48{,}000{,}000\,\text{clock cycles/s}}{100{,}000\,\text{samples/s}}
=480\,\text{clock cycles/sample}
$$

This ratio gives an intuitive CPU budget, **not** proof that a conversion completes in 480 cycles or that the CPU can perform 480 cycles of useful work per sample. Peripheral clock dividers, ADC acquisition/conversion time, memory transfers, interrupts, and USB overhead differ. Hardware offloading allows the CPU to work on *blocks* rather than waking for every one of 100,000 samples each second.

### Why this board?

Rev-1 already fixes the UNO R4 WiFi and RA4M1. Using the integrated ADC avoids an external digitizer for the initial prototype. The board also supports the downstream USB-PC development workflow. Whether the final achieved resolution, rate, and timing satisfy the product requirements must be *measured*.

## 2. ADC on A0: Turning voltage into numbers

### What does an ADC do?

An **analog-to-digital converter (ADC)** measures the voltage at its input at an acquisition instant and represents it as an integer **code**. In the product, the voltage originates from current through the ACS724, followed by the MCP6022 analog front end (AFE).

The schematic/integration specification identifies **UNO A0** as the product input, through a **1 kΩ series resistor** and **100 pF capacitor on the ADC side**. These are *accepted design elements*, not a request to wire or change them now. Before physical work we must inspect the actual KiCad schematic and refer to real component references/pins, never instruct probing a bare net name.

The ideal illustrative unipolar conversion equation is:

$$
q=\frac{V_{\text{FS}}}{2^N}
$$

where $V_{\text{FS}}$ is the **assumed** full-scale span and $N$ is bit depth. Using the Phase-6 **nominal 5 V example**, rather than claiming a measured reference:

$$
2^{14}=16{,}384
$$

$$
q_{14}=\frac{5\,\text{V}}{16{,}384}
=0.00030518\,\text{V}
\approx0.305\,\text{mV/LSB}
$$

For comparison:

$$
q_{12}=\frac{5\,\text{V}}{4096}
\approx1.221\,\text{mV/LSB}
$$

A 14-bit ideal unsigned code ranges **0–16383**, not 0–16384. A common conceptual estimate is:

$$
k\approx \left\lfloor\frac{V_{\text{in}}}{V_{\text{FS}}}2^{14}\right\rfloor
$$

with the result constrained to the valid code range; this is a simple ideal quantizer, **not** the RA4M1's guaranteed transfer function. For $V_{\text{in}}=2.00\,\text{V}$ and the illustrative 5.00 V span:

$$
k\approx\left\lfloor\frac{2.00}{5.00}\times16{,}384\right\rfloor=6553
$$

The inverse voltage estimate in this ideal model is approximately $kq$; physical conversion requires the actual reference, gain/offset calibration, and data-format conventions.

### Why 14-bit rather than “because more bits are better”?

The frozen project requires **effective ADC-domain resolution of 2 mV or better**. The nominal 14-bit quantization step of 0.305 mV is much smaller, giving room for real-world noise and implementation losses. It does **not** certify 2 mV usable performance. Reference fluctuation, ADC input settling, nonlinearity, source impedance, and digital noise can cause different codes for the same voltage.

Ideal maximum rounding error for a nearest-level quantizer is roughly half a step:

$$
\frac{q_{14}}{2}\approx0.153\,\text{mV}
$$

This describes **ideal quantization only**, not overall ADC accuracy. The accepted ADC/reference residual-error allocation is **±10 mA**, nominally **±8 mV equivalent** at nominal 0.8 V/A sensitivity. The current-reading accuracy target is a **different requirement** from bit resolution.

At nominal $0.8\,\text{V/A}$, an *illustrative* ideal 14-bit step corresponds to:

$$
\Delta I_{\text{ideal}}=\frac{0.00030518\,\text{V}}{0.8\,\text{V/A}}
\approx0.0003815\,\text{A}
=0.382\,\text{mA}
$$

This is not the actual resolved current, because the chain has noise and calibration uncertainty. Phase 6 deliberately leaves the exact ADC reference/power behavior for Stage B characterization.

### Why include input settling?

An ADC input is not necessarily a permanently open-circuit voltmeter. During sampling, an internal sampling capacitor must charge toward the input voltage through the effective source resistance and the ADC's input circuitry. For a simple first-order **illustrative** model:

$$
e(t)=e(0)e^{-t/(RC)}
$$

To settle an initial full-scale step to below half an ideal 14-bit LSB, the simple model requires:

$$
e^{-t/(RC)}\leq\frac{1}{2^{15}}
$$

$$
t\geq RC\ln(2^{15})\approx10.40RC
$$

The actual ADC internal sampling capacitance, switch resistance, acquisition time, board parasitics, and the MCP6022/interface behavior must be looked up or measured before calculating a real acquisition-time setting. The external 100 pF and 1 kΩ alone give an illustrative:

$$
\tau=(1000\,\Omega)(100\,\text{pF})=100\,\text{ns}
$$

$$
f_c=\frac{1}{2\pi(1000\,\Omega)(100\,\text{pF})}
\approx1.59\,\text{MHz}
$$

This local interface is **not** the main 15 kHz anti-alias filter. The 100 ns figure alone does **not** prove ADC settling at 100 kS/s.

## 3. Sampling rate: Why 100 kS/s?

A continuous waveform $v(t)$ becomes a sequence $v[n]$, where ideally:

$$
v[n]=v(nT_s)
$$

Here $T_s$ is the **sampling period** and $f_s$ the **sampling frequency**:

$$
T_s=\frac{1}{f_s}
$$

$$
f_s=100{,}000\,\text{samples/s}
\quad\Rightarrow\quad
T_s=10\,\mu\text{s}
$$

Therefore sample 0 is nominally at 0 µs, sample 1 at 10 µs, sample 2 at 20 µs, etc. Sampling **must continue** at these intervals even when the program processes previous data.

For a sine of frequency $f_{\text{signal}}$:

$$
\text{samples/cycle}=\frac{f_s}{f_{\text{signal}}}
$$

At **1 kHz**, that is 100 samples per cycle. At **5 kHz**, 20. At the top of the accepted diagnostic band, **10 kHz**, only 10 samples per cycle. This may be enough to represent the waveform when properly band-limited, but fewer samples give a less detailed direct view of each cycle.

### Nyquist and aliasing

The Nyquist frequency of uniformly sampled data is:

$$
f_N=\frac{f_s}{2}=50\,\text{kHz}
$$

A sine **above 50 kHz** can appear falsely as a lower-frequency sine, because samples alone cannot distinguish all such frequencies. A simple example at $f_s=100\,\text{kHz}$ is a 90 kHz sine appearing at 10 kHz in the sampled data:

$$
f_{\text{alias}}=|90-100|\,\text{kHz}=10\,\text{kHz}
$$

This is **aliasing**. No digital filter *after* sampling can reliably reconstruct what was originally above Nyquist if the analog frequencies have already folded into the band. The project's MCP6022 fourth-order approximately 15 kHz analog low-pass reduces high-frequency content *before* conversion.

**Important limitation:** A nominal 15 kHz cutoff is not a brick-wall filter. The AFE AC response is **not yet fully verified**; do not claim complete anti-alias rejection or AFE PASS.

### Frequency resolution and duration are different

For a contiguous window of $N_s$ samples:

$$
T_{\text{window}}=\frac{N_s}{f_s}
$$

An $N_s$-point DFT/FFT has bin spacing:

$$
\Delta f=\frac{f_s}{N_s}=\frac{1}{T_{\text{window}}}
$$

As an **example, not an approved buffer size**, 1000 samples at 100 kS/s span 10 ms and give 100 Hz bin spacing; 10,000 samples span 100 ms and give 10 Hz spacing. Windowing, spectral leakage, and detectability of nearby components still matter. **ADC sample rate** and **oscilloscope capture/export sample spacing** are different things and must not be confused.

## 4. Hardware timer: Why not read A0 in a loop?

A naive loop might do “read ADC → store → perform work → repeat.” But the loop also encounters interrupts, variable processing time, serial activity, and instruction timing. Therefore “fast on average” does not mean “every 10 µs.”

**Timing jitter** is the deviation from intended sample time:

$$
t_n=nT_s+\epsilon_n
$$

where $\epsilon_n$ is timing error. A *constant* timing offset is different from a varying $\epsilon_n$: variation can distort waveform phase and frequency analysis.

For an illustrative sine of amplitude $A$ and frequency $f$, small sampling timing error $\Delta t$ causes approximately:

$$
|\Delta v|\lesssim2\pi f A|\Delta t|
$$

At $f=10\,\text{kHz}$, $A=1\,\text{V}$, and hypothetical jitter $|\Delta t|=1\,\mu\text{s}$:

$$
|\Delta v|\lesssim2\pi(10{,}000)(1)(0.000001)
\approx0.0628\,\text{V}
$$

That is up to **62.8 mV** of local waveform error in the small-error approximation. The example is *not* a measured RA4M1 jitter result; it shows why timing matters.

### Hardware-clock principle

Instead, configure a peripheral timer to generate periodic hardware events. Route these events to ADC conversion starts through a **verified, supported** RA4M1 trigger route. The conversion and transfer then occur without the ordinary application loop deciding *when* the next sample begins.

For an **illustrative** undivided 48 MHz timer clock:

$$
\frac{48\,\text{MHz}}{100\,\text{kHz}}=480\,\text{timer ticks/period}
$$

This **does not** set an actual RA4M1 timer period register: counting conventions, divisors, selected timer, and event-routing constraints must first be checked against the device documentation. The exact GPT channel, ELC event, ADC trigger mode, and register values are **not frozen yet**.

A timer trigger starts a conversion; the ADC still needs enough time to acquire and convert each sample before the next trigger. Nominal 100 kS/s must be verified *at the completed-sample output*, not just at timer configuration.

## 5. DMA/DTC: Why transfer samples without involving the CPU each time?

After each conversion the ADC exposes a digital result in a peripheral data register. That value must reach RAM before it is used.

With per-sample CPU handling, an interrupt might execute **100,000 times each second**, adding scheduling and processing pressure. A **DMA** or **DTC** class hardware transfer engine can copy data from peripheral to memory according to configured transfer descriptors, so firmware can respond less frequently to completed blocks.

Conceptually:

1. Timer event starts ADC acquisition/conversion.
2. ADC completes and makes a sample available.
3. A supported hardware transfer copies the result to the next buffer position.
4. After a buffer fills, firmware is notified at **block rate**.

**Terminology:** DMA means *direct memory access*. Renesas **DTC** means *data transfer controller*. The project architecture prefers DMA/DTC-class assistance, but it does **not** certify that a specific RA4M1 trigger, source register, destination address progression, or automatic buffer switching is already supported/configured. Those remain implementation research.

### How much data?

A 14-bit sample usually needs storage in a **16-bit (2-byte) container** if raw codes are stored without packing:

$$
R_{\text{data}}=100{,}000\,\text{samples/s}\times2\,\text{bytes/sample}
=200{,}000\,\text{bytes/s}
$$

That is **200 kB/s (decimal)** of raw sample payload, excluding headers, block metadata, framing, checksums, and USB protocol overhead. This is a planning figure, not a measured communication rate. Continuous transfer to the PC is *not* a frozen requirement: Phase 12 describes asynchronous telemetry and requested waveform captures.

## 6. Ping-pong buffering: Why two RAM buffers?

**Buffer A** is being filled while the CPU works on the last completed block in **buffer B**. At the boundary their roles switch. This allows regular acquisitions and variable-duration processing to overlap.

Example only, with **1000 samples per buffer**:

$$
T_{\text{fill}}=\frac{1000}{100{,}000}=0.010\,\text{s}=10\,\text{ms}
$$

Each buffer holds $1000\times2=2000$ bytes. Two such buffers consume **4000 bytes** for raw sample storage, excluding control information. This is an **illustrative sizing exercise**, not a RAM allocation decision.

Timeline (each cell here represents a 10 ms block):

| Interval | Acquisition engine | CPU |
| --- | --- | --- |
| 0–10 ms | Fill A | Other work / initialization |
| 10–20 ms | Fill B | Consume completed A |
| 20–30 ms | Fill A again | Consume completed B |
| 30–40 ms | Fill B again | Consume completed A |

### What is an overrun?

Suppose filling B takes 10 ms, but the CPU still has not finished with A by the time the acquisition engine needs to reuse A at 20 ms. **A cannot safely be overwritten** while its old contents are still needed. The system must detect that loss or inability to preserve continuous data, mark the affected block invalid, and propagate that status to downstream features/diagnostics.

A conceptual state model uses **FREE**, **FILLING**, and **READY/IN_USE**. Before arming a buffer as a new destination, firmware must ensure it is free to reuse. An overrun increments a counter and invalidates the broken section; it must never quietly stitch discontinuous data into an FFT and call the result valid.

**Important subtlety:** Two buffers do not guarantee zero overruns. A sustained consumer slower than the producer will still fall behind. The complete firmware also needs reliable buffer ownership, block sequence numbering/continuity, and an explicit policy for fault detection and recovery.

### Timing budget

With $N_s$ samples per buffer, the CPU generally has at most one buffer-fill interval to finish work on the other buffer **before it must be reused**, under this simple two-buffer scheme. That means the typical per-block processing work should fit comfortably below $N_s/f_s$ with margin for interrupts and background activity. A longer FFT window can span several blocks without changing the hardware sampling cadence.

## 7. How the six decisions combine

| Decision | What it contributes | What still needs Stage-B proof |
| --- | --- | --- |
| UNO R4 WiFi / RA4M1 | Main controller and hardware peripherals | Actual peripheral configuration |
| A0, 14-bit baseline | Voltage-to-code conversion | Reference, settling, measured effective resolution |
| 100 kS/s | 10 µs nominal spacing; 50 kHz Nyquist | Actual rate, sample continuity |
| Hardware timer | Regular ADC start cadence | Supported trigger route and measured jitter |
| DMA/DTC-style transfer | Moves results to RAM with less CPU intervention | Actual transfer mechanism and correct ordering |
| Two buffers + overrun state | Separates sampling from processing | Safe handoff, sequence integrity, forced-overrun detection |

The high-level processing chain is **raw ADC block → voltage/current calibration → time/frequency features → diagnostics → USB/PC**. The ADC layer should not claim to identify actuator faults by itself; it should deliver samples and their quality status.

## 8. Calculations versus acceptance evidence

Everything numerical in this lesson is either an **accepted design target** or a clearly **illustrative mathematical prediction**. No new bench result was produced.

- **Accepted:** 14-bit baseline, 100 kS/s target, DC–10 kHz diagnostic band, hardware-timed acquisition, hardware-assisted transfer, double buffering, overrun visibility, ≤2 mV effective resolution requirement.
- **Calculated from assumptions:** ideal 0.305 mV/LSB at 5 V; 10 µs/sample; 50 kHz Nyquist; 480 ticks at hypothetical undivided 48 MHz; 200 kB/s unframed raw payload; hypothetical 1000-sample buffer timing.
- **Not yet proven:** true ADC reference accuracy, actual timer/trigger/DTC register setup, measured sample jitter, effective ADC resolution, actual buffer scheme, input settling, sample-loss behavior, or the complete AFE AC response.

## 9. Next controlled engineering step (no circuit change yet)

1. Inspect the current KiCad schematic for the physical ADC interface references and connections.
2. Consult authoritative Arduino/Renesas material for A0-to-ADC channel mapping, hardware ADC trigger routes, conversion timing, and DMA/DTC support.
3. Propose **one** observable hardware-timer-only firmware test, with expected output and verification method, before enabling ADC conversions.
4. Record measured results and selected implementation details separately from this study note.

No wiring, schematic edit, firmware upload, or bench measurement is requested by this educational PR.

## 10. Inside the RA4M1 ADC: sampling, conversion, and timing

**Study goal:** Understand what happens between an analog voltage arriving at A0 and a digital value becoming available. This is a detailed explanation of the next part of the acquisition system. It does **not** define the final register values.

### 10.1 A0 is a physical input, not the ADC itself

On the UNO R4 WiFi board, the **A0** header connects to **RA4M1 P014**, which supports **analog input AN009**. This is the pin mapping shown in the official Arduino UNO R4 WiFi pinout.

A0 is the outside connection where the signal enters the board. The ADC is a circuit *inside* the RA4M1. The ADC needs to be configured to measure the correct input channel.

Arduino pinout: https://docs.arduino.cc/resources/pinouts/ABX00087-full-pinout.pdf

### 10.2 Two stages: sample first, convert second

**Sampling** means allowing the ADC's internal measurement circuit to follow the input voltage. A small internal capacitor is charged toward that voltage. An internal switch then separates the stored voltage from the changing input.

**Conversion** means using the captured voltage to calculate a digital code. The RA4M1's ADC14 is a 14-bit ADC. A full conversion produces one number in the range expected by its selected operating mode.

Why separate them? Because the motor current can change while the ADC is working. The conversion must represent the voltage measured at a known time, rather than an unknown mixture of voltages from different times.

A useful simple model is:

1. A timer sends a start event at the planned time.
2. The ADC opens its sampling switch for the configured sampling time.
3. The ADC closes the switch and converts the stored voltage.
4. A completed digital value becomes available.
5. The transfer system copies the value to RAM.

This is a **conceptual explanation**, not proof of the exact internal event order or register settings selected for Rev-1. Real hardware timing must be checked against the RA4M1 manual.

### 10.3 Why the input needs time to settle

An internal sampling capacitor does not change voltage instantly. It charges or discharges through resistance in the input path.

For a simplified resistor-capacitor model, the error remaining after time $t$ is:

$$
e(t)=e(0)e^{-t/(RC)}
$$

Here $R$ is the total effective resistance, $C$ the effective sampling capacitance, and $e(0)$ the voltage error when sampling begins. **These are simplified model values, not measured RA4M1 values.**

The time constant is:

$$
\tau=RC
$$

After one time constant, the remaining error is about 36.8% of its initial value. After five time constants, it is about 0.67%. For a **14-bit ideal example** with an initial full-scale step and a target smaller than half an LSB:

$$
e^{-t/\tau}\leq\frac{1}{2^{15}}
$$

Taking the natural logarithm of both sides:

$$
-\frac{t}{\tau}\leq-\ln(2^{15})
$$

Therefore:

$$
t\geq\tau\ln(2^{15})\approx10.40\tau
$$

**Why 15 in the power?** A 14-bit full-scale range has $2^{14}$ steps. Half of one ideal step is $1/(2\times2^{14})=1/2^{15}$ of the full range.

For an **imaginary** effective $RC=0.10\,\mu\text{s}$:

$$
t_{\text{sample}}\geq10.40\times0.10\,\mu\text{s}=1.04\,\mu\text{s}
$$

This calculation teaches the method only. We have **not** established that the real RA4M1 ADC input has that effective RC value. The external 1 kΩ / 100 pF ADC interface has its own behavior and cannot, by itself, be used to set the internal ADC sampling time.

### 10.4 How a 14-bit result is formed

For an ideal ADC covering an **assumed** 0–5 V range:

$$
q=\frac{5\,\text{V}}{2^{14}}\approx0.305\,\text{mV}
$$

One code step is therefore about 0.305 mV in this ideal example. A measured voltage near 2.00 V corresponds to approximately:

$$
k=\left\lfloor\frac{2.00}{5.00}\times16{,}384\right\rfloor=6553
$$

The real answer depends on the actual reference voltage, ADC settings, input noise, and calibration. **14-bit precision in a register is not the same as 14-bit accuracy at the input.**

### 10.5 Why 100 kS/s does not mean a conversion lasts 10 µs

The project requires:

$$
f_s=100{,}000\,\text{samples/s}
$$

$$
T_s=\frac{1}{f_s}=10\,\mu\text{s}
$$

This tells us **when the next measurement must start**. It does not tell us how long sampling and conversion take separately.

For example, imagine these **made-up timing values**:

- Sampling: 2 µs.
- Conversion: 3 µs.
- Total time to complete one result: 5 µs.
- Time between successive measurement starts: 10 µs.

Then the ADC has:

$$
10\,\mu\text{s}-5\,\mu\text{s}=5\,\mu\text{s}
$$

before the next start event. In this simple model, the ADC finishes in time.

But if sampling plus conversion took **12 µs**, a new event would arrive before the earlier measurement had finished. We would need to change the ADC configuration or sampling approach rather than simply claiming the system achieves 100 kS/s.

The actual RA4M1 sampling time depends on the **ADC clock (ADCLK)** and its sampling-time setting. The sampling time is set in ADC clock periods. The hardware manual describes the **ADSSTRn** sampling-state registers. We must check the correct channel setting, clock, minimum allowed period, conversion time, and trigger behavior before choosing a numeric register value.

RA4M1 reference manual: https://www.renesas.com/en/document/mah/ra4m1-group-users-manual-hardware

### 10.6 Where the number goes next

After a conversion completes, the result is made available in the ADC's result register. The planned hardware-assisted data transfer then copies the result to RAM.

Do not confuse these two jobs:

- **ADC:** changes a voltage into a number.
- **DTC/DMA-class transfer:** moves the number into a RAM buffer.

A fast transfer cannot repair incorrect input settling. A good conversion also does not prevent data loss if the next buffer is still in use. All parts must work correctly.

### 10.7 What we know and what we still need to verify

| Item | Status |
| --- | --- |
| A0 maps to RA4M1 P014 / AN009 | Confirmed by Arduino pinout |
| 14-bit conversion | Accepted project requirement |
| One sample start every 10 µs | Accepted project target |
| Internal ADC sampling-time register concept | Documented in RA4M1 hardware reference |
| Exact ADC clock and sampling-state count | Not selected |
| Exact time to complete an A0 conversion | Not measured or accepted |
| Real input settling with the Rev-1 AFE and ADC interface | Not measured |
| Hardware timer/ADC trigger configuration | Not selected |
| Measured 100 kS/s stream without lost samples | Not yet demonstrated |

**Next lesson:** Understand how an RA4M1 hardware timer can start ADC measurements at fixed 10 µs intervals. Choose and test the exact hardware later, after reviewing the manual and the schematic.

### 10.8 How a SAR ADC finds a number

The RA4M1 uses a **Successive Approximation Register (SAR)** ADC. Its circuits work together:

1. A switch connects the ADC input to a small sampling capacitor. The capacitor charges toward the input voltage.
2. The switch opens. The ADC holds the sampled voltage on the capacitor.
3. An internal **DAC** (digital-to-analog converter) creates a test voltage.
4. A **comparator** checks whether the held input is above or below that test voltage.
5. SAR logic keeps or clears a binary bit. It repeats this for the next bit, from largest to smallest.
6. The finished binary code is placed into the ADC result register.

Why use this method? For 14 bits, an ADC has 16,384 possible output codes. A SAR ADC can find the code by testing bits in order rather than counting through all 16,384 codes.

**Worked example: 4-bit ADC, 0–5 V input range, measuring 3.2 V.** One code step is $5/16 = 0.3125$ V.

| Bit tested | Trial binary | Test voltage | Comparison with 3.2 V | Decision |
| --- | --- | ---: | --- | --- |
| Highest bit | 1000 | 2.5000 V | Input higher | Keep |
| Next bit | 1100 | 3.7500 V | Input lower | Clear |
| Next bit | 1010 | 3.1250 V | Input higher | Keep |
| Last bit | 1011 | 3.4375 V | Input lower | Clear |

Final code: **1010** (decimal 10), representing $10\times0.3125=3.125$ V. The difference between 3.2 V and 3.125 V is due to the size of a single 4-bit step.

A 14-bit ADC uses the same principle, with smaller voltage steps. The sampled voltage stays stored during the comparisons, even if the input signal changes.

Further reading: [Renesas: SAR ADCs](https://www.renesas.com/en/blogs/sar-adcs-high-sampling-rate-applications) and [Analog Devices: Successive Approximation ADCs](https://www.analog.com/en/resources/analog-dialogue/articles/successive-approximation-adcs.html).

### 10.9 How one measurement finishes before the next starts

A **hardware timer** starts each ADC measurement. The ADC then samples, holds, compares, and saves the result. At 100 kS/s, the timer starts measurements at 0, 10, 20, 30 µs, and so on.

The time between starts is $T_s=1/100{,}000=10$ µs. **This is not the time required for one conversion.** If sampling and conversion take 2 µs, a measurement started at 0 µs completes around 2 µs; the next starts at 10 µs and completes around 12 µs.

The ADC uses its own clock, called **ADCLK**. The RA4M1 manual provides these timing parts for 14-bit high-speed operation:

- Sampling time: $(\text{ADSSTRn}+0.5)/f_{\text{ADCLK}}$.
- SAR comparison time: $37.5/f_{\text{ADCLK}}$.
- Sampling plus comparison: $(\text{ADSSTRn}+38)/f_{\text{ADCLK}}$.

For an ADC clock of 48 MHz and an ADSSTR value of 13, sampling takes $13.5/48=0.28125$ µs and SAR comparison takes $37.5/48=0.78125$ µs. Together they take $51/48=1.0625$ µs, matching the approximately **1.06 µs** figure in the RA4M1 datasheet for that specified case.

The scan start/end delays and transfer time also matter. Before firmware implementation we will verify the actual **A0 / AN009** sampling requirements, ADC clock, and input settling. The external ADC interface includes a 1 kΩ series resistor, so we cannot copy a short sampling-time setting without checking its effect.

References: [RA4M1 hardware manual](https://www.renesas.com/en/document/mah/renesas-ra4m1-group-users-manual-hardware) and [RA4M1 datasheet](https://www.renesas.com/en/document/dst/ra4m1-group-datasheet).

## 11. Hardware timer: start a new ADC measurement every 10 µs

### 11.1 What is a hardware timer?

A hardware timer is a counter inside the microcontroller. It counts clock ticks without needing the main program to tell it to count again.

We need it to start each ADC measurement at regular times:

| Measurement | Start time |
| --- | ---: |
| 1 | 0 µs |
| 2 | 10 µs |
| 3 | 20 µs |
| 4 | 30 µs |
| 5 | 40 µs |

The timer continues counting while the CPU works on other tasks. This is different from calling \`analogRead()\` repeatedly in a software loop, where the time between reads depends on what the program is doing.

### 11.2 How do we calculate the timer period?

Let:

- $f_{\text{timer}}$ = frequency at which the timer counts, in ticks per second;
- $f_s$ = required number of ADC samples per second;
- $N$ = number of timer ticks between two ADC start events.

Then:

$$
N=\frac{f_{\text{timer}}}{f_s}
$$

For our project, $f_s=100{,}000\,\text{samples/s}$.

If the timer counts at $48\,\text{MHz}$:

$$
N=\frac{48{,}000{,}000}{100{,}000}=480\,\text{ticks}
$$

The time for one tick is:

$$
T_{\text{tick}}=\frac{1}{48{,}000{,}000}
\approx20.83\,\text{ns}
$$

Thus:

$$
480\times20.83\,\text{ns}\approx10\,\mu\text{s}
$$

A timer may also use a **clock divider**. For example, with a divider of 8:

$$
f_{\text{timer}}=\frac{48\,\text{MHz}}{8}=6\,\text{MHz}
$$

$$
N=\frac{6{,}000{,}000}{100{,}000}=60\,\text{ticks}
$$

Both calculations give a 10 µs period. The correct register setting depends on how the selected timer counts (for example, from zero to its period value), its clock source, and supported divider settings.

The CPU clock, timer clock, and ADC clock are not automatically the same thing. We must check their actual configuration before writing firmware.

### 11.3 What happens at each timer event?

The intended hardware path is:

**Timer reaches its set count → timer produces an event → ADC starts measuring A0 → ADC completes → result can be copied to RAM.**

An **event** is an internal hardware signal meaning that something happened, such as the timer reaching a chosen count. It does not need to be an electrical pulse on a board pin.

The RA4M1 has hardware features for linking supported peripheral events. We must check that the timer and ADC trigger route we select is supported before relying on it.

The main program may process an older set of samples or send information over USB without changing when the next ADC measurement begins.

### 11.4 Why not use a timer interrupt to call the ADC?

An **interrupt** tells the CPU to stop its current task and run a short piece of code.

A timer interrupt can occur every 10 µs, but if its code starts the ADC, the start time may change slightly depending on interrupt handling and other tasks.

A **hardware trigger** avoids making the CPU responsible for starting every single measurement. This is the accepted project design.

The timer event must repeat at 100 kHz; the ADC must also finish its work before the next measurement. Fast timer events alone do not guarantee a valid 100 kS/s data stream.

### 11.5 What does timing error do to our measurements?

The ideal sampling times are:

$$
t_n=nT_s
$$

With timing error:

$$
t_n=nT_s+\epsilon_n
$$

The term $\epsilon_n$ describes how early or late a sample is. A changing timing error is called **jitter**.

For a sine wave, even a small time error matters more as the signal frequency rises. That is why we want the ADC to start at fixed times and why later tests must check the actual time spacing.

### 11.6 How will we check this during implementation?

We will first check the timer by itself. A useful test is to configure a timer-controlled output, where supported, and view its timing with the oscilloscope.

Then we will connect the timer's internal event to the ADC and check the resulting **completed samples**. This second check matters: a correctly running timer does not prove that conversions and data transfers are keeping up.

Only after timing is established will we add the hardware-assisted RAM transfer and double buffers.

**Next study topic:** How DTC/DMA-style hardware moves completed ADC results to RAM without asking the CPU to copy every sample.

## 12. How DTC/DMA moves ADC samples into RAM

### 12.1 The problem we need to solve

With the ADC and timer correctly configured, each completed measurement gives a new number in the **ADC result register**, which is a small storage location inside the microcontroller.

But our analysis needs many numbers in order:

| Measurement start time | Result when conversion finishes |
| --- | --- |
| 0 µs | 1604 |
| 10 µs | 1612 |
| 20 µs | 1620 |
| 30 µs | 1616 |

These numbers show the idea of recording a changing voltage. We need to copy each completed result into **RAM (random-access memory)** before the next result replaces it.

The CPU could copy every sample, but that would require it to react around **100,000 times each second**. Instead, we want hardware to move the data while the CPU works on complete groups of samples.

### 12.2 What are DTC and DMA?

**DMA** means *Direct Memory Access*. **DTC** means *Data Transfer Controller*. They are two hardware methods for moving data without writing a CPU instruction for every sample.

The RA4M1 has both a **DTC** and a **DMA controller (DMAC)**. The product design prefers a hardware-assisted transfer; Stage B will choose the actual method.

The jobs are different:

- **Timer:** decides when a new ADC measurement starts.
- **ADC:** converts the voltage into a number.
- **DTC or DMAC:** copies the finished number to RAM.
- **CPU:** processes completed samples and checks for errors.

The transfer device **does not** decide when to measure the voltage. Moving data quickly cannot fix incorrect ADC sampling times.

### 12.3 How does the transfer device know what to copy?

Before starting, firmware configures a **transfer description**. It tells the hardware:

1. **Source:** where to read from, such as the result register for the selected ADC channel.
2. **Destination:** where to write, such as the start of a RAM array.
3. **Size:** how many bytes to copy each time.
4. **Addresses:** whether the source and destination stay fixed or move to the next position.
5. **Count:** how many transfers to perform.
6. **Start event:** which hardware event means that a new result is ready.

For raw 14-bit ADC codes, a convenient storage type is **16 bits = 2 bytes** per sample. The extra two bits are simply unused or defined by the ADC result format.

Example of five completed conversions:

| ADC result | Source address | RAM destination |
| ---: | --- | --- |
| 1604 | Same ADC register | Buffer A, position 0 |
| 1612 | Same ADC register | Buffer A, position 1 |
| 1620 | Same ADC register | Buffer A, position 2 |
| 1616 | Same ADC register | Buffer A, position 3 |
| 1608 | Same ADC register | Buffer A, position 4 |

The **source stays fixed** because each result appears in the ADC's register. The **destination moves forward by 2 bytes** because each stored result needs two bytes.

If the first RAM address were $A_0$, the destination for sample $n$ would be:

$$
A_n=A_0+2n
$$

For $n=4$, the address is $A_0+8$ bytes.

This is why the transfer device needs rules for source and destination addresses. It is not calculating current or filtering data; it is copying numbers.

### 12.4 Which event starts the copy?

The **ADC completion event** should start the transfer: the new result must be ready before we copy it.

Conceptually:

**Timer event → ADC starts → ADC completes → DTC/DMAC copies result → RAM**

The timer event and ADC completion event have **different purposes**. If the transfer ran before the conversion finished, it could read an old result.

The RA4M1 provides event and interrupt mechanisms for hardware transfers. We will check the exact ADC completion signal and supported DTC/DMAC connections when implementing firmware.

### 12.5 How fast is the raw data stream?

Our sampling rate is:

$$
f_s=100{,}000\,\text{samples/s}
$$

With two bytes stored for each sample:

$$
R=100{,}000\times2=200{,}000\,\text{bytes/s}
$$

So RAM receives **200 kB of raw ADC data per second**, or about **195 KiB/s** when using 1024 bytes per KiB.

For a buffer with 1,000 samples:

$$
M=1000\times2=2000\,\text{bytes}
$$

$$
T=\frac{1000}{100{,}000}=10\,\text{ms}
$$

These calculations tell us the required memory size and how often the software needs a completed buffer.

### 12.6 Why not let the transfer write forever into one buffer?

RAM has a limited size. After 1,000 transfers the example buffer is full.

If the hardware starts writing at the beginning again immediately, old values disappear. If the CPU is still using those values, it can get a mixture of old and new samples.

The project therefore uses **two buffers**:

| Time | Hardware transfer | CPU |
| --- | --- | --- |
| 0–10 ms | Fill A | Other work |
| 10–20 ms | Fill B | Process A |
| 20–30 ms | Fill A | Process B |

This is called **double buffering** or **ping-pong buffering**.

At each buffer boundary, the program must safely give the hardware the next free buffer and mark the completed buffer ready for processing.

A key detail: **DTC/DMAC does not automatically give us safe double buffering merely because it can transfer data.** The final firmware must explicitly manage buffer addresses, transfer completion, and ownership.

### 12.7 How will we know if data was lost?

Suppose a 1,000-sample buffer fills every 10 ms. If processing one completed buffer takes 15 ms, software might still be reading buffer A when the hardware needs to fill A again.

That is an **overrun**. We must detect it and mark the affected samples invalid.

A useful design is to track:

- **Buffer state:** FREE, FILLING, READY, or IN_USE.
- **Block number:** 0, 1, 2, 3, ... for complete buffers.
- **Error count:** increases when a completed buffer cannot be saved or the next buffer is not free.

Missing block numbers show where sample continuity was broken. A later FFT must not join samples across such a gap as though nothing happened.

### 12.8 Why not send each ADC value directly over USB?

USB communication can vary in speed and may pause. It must not control when we measure the input.

RAM buffers give the ADC a place to store samples immediately. USB can later send selected waveforms or processed values. If a USB task is slow, sampling should continue as long as RAM and processing can keep up.

### 12.9 What must Stage B choose?

The accepted design tells us **what behavior we need**, but the firmware must still choose the exact transfer hardware and settings:

- DTC or DMAC, with a supported ADC-result-ready event;
- correct ADC result-register address and 16-bit sample format;
- fixed source and increasing destination addresses;
- transfer count, buffer size, and safe buffer switching;
- how software learns that one buffer is complete;
- detection of lost samples and failed transfers.

A successful test will show that samples are copied in the correct order into RAM at 100 kS/s while the CPU performs other work. We will also deliberately make processing too slow and verify that an overrun is reported.

**Hardware reference:** [Renesas RA4M1 Group User's Manual: Hardware](https://www.renesas.com/en/document/mah/renesas-ra4m1-group-users-manual-hardware), especially *DMA Controller (DMAC)*, *Data Transfer Controller (DTC)*, and *ADC14*. The choice of transfer method will be made during implementation.

**Next study topic:** Double-buffer ownership, how an overrun is detected, and how buffer size changes our processing time.
