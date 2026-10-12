# Sampling, phase, spectrum, transfer, and RC fundamentals — expanded worked review

**Project:** Actuator Health Monitoring System  
**Date:** 2026-10-12  
**Purpose:** Preserve the detailed worked explanation of the 21 follow-up questions raised after ACS724 dynamic/FILTER validation.  
**Status:** Study/learning note only; not an engineering-baseline approval.

The project measurement convention used in this review is:

- **CH1** = voltage across **R8**, with $R8=67\,\Omega$, so it is the primary-current reference:

$$
  I=\frac{V_{CH1}}{67\Omega}
$$

- **CH2** = **ACS724 OUT** voltage relative to GND.
- The excitation is a **positive-biased sinusoidal current**, not a bipolar current reversing direction.

---

# 1. $\Delta t=40\,\mu s$. How do I determine it myself with the scope?

The most important distinction is:

- **$N$** = number of stored samples.
- **$f_s$** = sample rate, samples per second.
- **$\Delta t$** = time between adjacent samples.
- **$T_{record}$** = total duration stored.
- **samples/cycle** = how many samples represent one signal period.

They are related by:

$$
f_s=\frac{1}{\Delta t}
$$

and

$$
T_{record}=\frac{N}{f_s}
$$

For this project, we keep:

$$
N=10000
$$

because **Depth = 10K**.

## Start before pressing RUN

Suppose you want to measure:

$$
f_{signal}=1\,kHz
$$

First calculate its period:

$$
T_{signal}=\frac{1}{f}
$$

$$
T=\frac{1}{1000}=0.001s=1ms
$$

Now decide how many samples you want per cycle.

For amplitude + phase work, we chose about:

$$
25\text{ samples/cycle}
$$

Therefore:

$$
\Delta t=\frac{T}{25}
$$

$$
\Delta t=\frac{1ms}{25}=0.04ms=40\mu s
$$

Then sample rate:

$$
f_s=\frac{1}{40\mu s}
$$

$$
f_s=\frac{1}{40\times10^{-6}}
=25000\,Sa/s
$$

$$
\boxed{f_s=25\,kSa/s}
$$

Nyquist:

$$
f_N=\frac{f_s}{2}
$$

$$
f_N=\frac{25k}{2}=12.5\,kHz
$$

With 10K samples:

$$
T_{record}=\frac{10000}{25000}
$$

$$
T_{record}=0.4s
$$

Number of captured 1 kHz cycles:

$$
N_{cycles}=T_{record}f_{signal}
$$

$$
N_{cycles}=0.4\times1000=400
$$

So before you even run the scope, you know:

$$
\boxed{
1kHz
\rightarrow
1ms/cycle
\rightarrow
40\mu s/sample
\rightarrow
25kSa/s
\rightarrow
12.5kHz\ Nyquist
\rightarrow
0.4s\ record
\rightarrow
400\ cycles
}
$$

## How do you convert that into the actual DOS1102S setting?

This is project-specific and came from our actual CSV records.

With **Depth = 10K**, our DOS1102S approximately follows:

$$
T_{record}\approx20\times M
$$

where $M$ is the displayed main timebase.

Therefore:

$$
\Delta t\approx\frac{20M}{10000}
$$

If $M$ is in ms/div:

$$
\boxed{\Delta t[\mu s]\approx2M[ms/div]}
$$

and:

$$
\boxed{f_s[kSa/s]\approx\frac{500}{M[ms/div]}}
$$

For our 1 kHz example:

$$
M=20ms/div
$$

Then:

$$
\Delta t\approx2\times20=40\mu s
$$

$$
f_s\approx\frac{500}{20}=25kSa/s
$$

So on the scope you actually set:

**Depth = 10K**  
**M = 20 ms/div**

You do **not** directly enter “$\Delta t=40\mu s$”.

### Compare with 10 kHz

$$
f=10kHz
$$

$$
T=\frac1{10000}=100\mu s
$$

25 samples/cycle:

$$
\Delta t=\frac{100}{25}=4\mu s
$$

$$
f_s=\frac1{4\mu s}=250kSa/s
$$

$$
f_N=125kHz
$$

10K record:

$$
T_{record}=\frac{10000}{250000}=0.04s=40ms
$$

Cycles:

$$
0.04\times10000=400
$$

DOS scope setting:

$$
M=\frac{\Delta t[\mu s]}2
=\frac42
=2ms/div
$$

So:

**1 kHz → M = 20 ms/div**  
**10 kHz → M = 2 ms/div**

That is the procedure you should be able to do completely without ChatGPT.

After stopping the acquisition, you can independently verify $\Delta t$ by deeply zooming into stored points and measuring the time between adjacent samples, or later from CSV timestamps.

---

# 2. Does ACS724 OUT minus IP− give residual noise? Should they ideally be equal?

No. This is a very important correction.

They represent **different physical quantities**.

At R8:

$$
V_{CH1}=I_{primary}\times67\Omega
$$

At ACS724 OUT:

$$
V_{OUT}\approx V_{ZERO}+S(f)I_{primary}
$$

where approximately:

- $V_{ZERO}$ is around the sensor's zero-current offset;
- $S$ is sensor sensitivity in V/A.

Suppose current variation is:

$$
I_{pp}=7mA
$$

Across R8:

$$
V_{CH1,pp}=0.007\times67
$$

$$
V_{CH1,pp}=0.469V
$$

But with sensor sensitivity around $0.8V/A$:

$$
V_{OUT,pp}=0.007\times0.8
$$

$$
V_{OUT,pp}=0.0056V
$$

$$
=5.6mV
$$

So one signal can be roughly:

$$
469mVpp
$$

while the other is only:

$$
5.6mVpp
$$

They absolutely should **not** be equal in volts.

What should ideally match is the **information about current**, after scaling.

From CH1:

$$
I=\frac{V_{CH1}}{67}
$$

Then predicted sensor output would be something like:

$$
V_{predicted}=V_{ZERO}+S I
$$

Only after making the quantities comparable does subtraction make sense:

$$
e(t)=V_{OUT,measured}-V_{OUT,predicted}
$$

That residual should approach zero for a perfect model, perfect sensor and perfect measurement.

## Why does phase differ?

There are two separate causes.

### Physical phase

The ACS724 and FILTER network have dynamics.

Current changes first.

The Hall element, amplifier and filtering respond afterward.

Therefore CH2 can lag CH1.

### Measurement-system phase

Our same-node test showed that even when both probes measured the same electrical signal, exported CH2 appeared approximately **one stored sample behind CH1**.

At 10 kHz:

$$
T=100\mu s
$$

with:

$$
\Delta t=4\mu s
$$

One sample corresponds to:

$$
360^\circ\frac{4}{100}
=14.4^\circ
$$

So approximately $14.4^\circ$ of apparent phase could come from the measurement system rather than the ACS724.

Therefore measured CH1→CH2 phase can contain:

$$
\boxed{
\text{real sensor/filter phase}
+
\text{scope/channel timing artifact}
}
$$

---

# 3. What is “apparent transfer”? Is it some kind of power?

No.

You may be thinking of **apparent power**, measured in VA. That is completely different.

Our **apparent transfer** is:

$$
H_{apparent}(f)=\frac{V_{OUT}(f)}{I_{primary}(f)}
$$

Units:

$$
\frac{V}{A}
$$

So it is basically frequency-dependent sensor sensitivity.

Example:

$$
I_{pp}=6.8mA
$$

$$
V_{OUT,pp}=5.8mV
$$

Then:

$$
H=\frac{5.8mV}{6.8mA}
$$

$$
H=0.853V/A
$$

Meaning:

> For every 1 A of current variation at that frequency, the complete measured system appears to produce about 0.85 V of output variation.

Why **apparent**?

Because we have not proven that all of this response comes only from the ACS724.

The measured result may include:

- ACS724 itself;
- FILTER network;
- probe response;
- scope response;
- channel timing skew;
- noise;
- finite-record effects.

So:

$$
H_{measured}
=
H_{sensor}
\times
H_{filter}
\times
H_{measurement}
$$

conceptually.

It is definitely **not power**.

---

# 4. How do I determine phase manually?

For two periodic signals of equal frequency:

$$
\boxed{\phi=360^\circ\frac{\Delta t_{phase}}{T}}
$$

where:

- $T$ = signal period;
- $\Delta t_{phase}$ = horizontal time difference.

For a lagging CH2, we use negative phase.

Example at 10 kHz:

$$
T=\frac1{10000}=100\mu s
$$

Suppose CH2 reaches the equivalent point $16\mu s$ after CH1.

$$
\phi=-360^\circ\frac{16}{100}
$$

$$
\boxed{\phi=-57.6^\circ}
$$

On the scope:

1. STOP the waveform.
2. Choose the same feature on both traces.
3. Prefer a rising midline crossing.
4. Measure horizontal $\Delta t$ with cursors.
5. Measure $T$.
6. Use the formula.

For a positively biased sine, “zero crossing” means crossing the waveform's **own mean/midline**, not necessarily 0 V.

At 1 kHz:

$$
T=1ms
$$

If CH2 lags by $50\mu s$:

$$
\phi=-360\frac{50}{1000}
$$

$$
\boxed{-18^\circ}
$$

For noisy signals, measure several cycles and average because one cursor crossing may be noisy.

---

# 5. At 1 kHz/10 kHz are we sending AC current? Why can current change fast or slowly?

First: we are not sending an **impulse**.

An impulse is a short transient.

We are applying a **sinusoidal periodic stimulus**.

Our current is approximately:

$$
i(t)=I_{DC}+I_{AC}\sin(2\pi ft)
$$

So there is:

- positive DC bias;
- AC ripple.

The current generally remains positive.

## Why 10 kHz changes faster than 1 kHz

At:

$$
1kHz
$$

one cycle lasts:

$$
T=1ms
$$

At:

$$
10kHz
$$

one cycle lasts:

$$
T=100\mu s
$$

So 10 kHz completes ten times as many oscillations in the same time.

Mathematically:

$$
i(t)=I_{pk}\sin(2\pi ft)
$$

Differentiate:

$$
\frac{di}{dt}
=
2\pi fI_{pk}\cos(2\pi ft)
$$

Maximum rate of current change:

$$
\left|\frac{di}{dt}\right|_{max}
=
2\pi fI_{pk}
$$

Therefore if amplitude stays identical, a 10 kHz sine requires ten times larger maximum $di/dt$ than a 1 kHz sine.

For example with:

$$
I_{pk}=1mA
$$

at 1 kHz:

$$
2\pi(1000)(0.001)
=6.28A/s
$$

At 10 kHz:

$$
2\pi(10000)(0.001)
=62.8A/s
$$

Ten times faster.

In a resistor, current can follow voltage almost immediately:

$$
i=\frac{v}{R}
$$

In an inductor:

$$
v=L\frac{di}{dt}
$$

so an inductor actively resists fast current change. Therefore high-frequency current becomes harder to create through an inductive load.

---

# 6. How can I analyze spectrum and harmonics manually?

A spectrum asks:

> How much of each frequency exists in my waveform?

Suppose you have samples:

$$
x_0,x_1,\ldots,x_{N-1}
$$

taken every:

$$
\Delta t
$$

First calculate sample times:

$$
t_n=n\Delta t
$$

## Step 1 — calculate DC

$$
V_{DC}
=
\frac1N\sum_{n=0}^{N-1}x_n
$$

Remove it:

$$
y_n=x_n-V_{DC}
$$

## Step 2 — choose a frequency

Suppose your fundamental is:

$$
f_0=1kHz
$$

To test the fundamental:

$$
f=1kHz
$$

For each sample calculate:

$$
\theta_n=2\pi ft_n
$$

Then sine projection:

$$
S_f
=
\frac2N
\sum y_n\sin(\theta_n)
$$

Cosine projection:

$$
C_f
=
\frac2N
\sum y_n\cos(\theta_n)
$$

Amplitude:

$$
A_{pk}
=
\sqrt{S_f^2+C_f^2}
$$

Peak-to-peak:

$$
A_{pp}=2A_{pk}
$$

Phase in our project convention:

$$
\phi=\operatorname{atan2}(C_f,S_f)
$$

## Harmonics

Second harmonic:

$$
f_2=2f_0
$$

Third:

$$
f_3=3f_0
$$

Fourth:

$$
f_4=4f_0
$$

etc.

If:

$$
f_0=1kHz
$$

then:

- fundamental = 1 kHz
- 2nd = 2 kHz
- 3rd = 3 kHz
- 4th = 4 kHz
- 5th = 5 kHz.

Run exactly the same sine/cosine calculation for each.

## Frequency resolution

For a DFT:

$$
\Delta f=\frac{f_s}{N}
$$

Because:

$$
T_{record}=\frac{N}{f_s}
$$

also:

$$
\boxed{\Delta f=\frac1{T_{record}}}
$$

Example:

$$
T_{record}=40ms
$$

$$
\Delta f=\frac1{0.04}=25Hz
$$

So spectrum bins occur at:

$$
0,\ 25,\ 50,\ 75,\ldots
$$

10 kHz is bin:

$$
k=\frac{10000}{25}=400
$$

The FFT simply performs this type of Fourier calculation extremely efficiently for many frequencies.

For learning manually, use **8 or 16 samples**, not 10000.

---

# 7. Fundamental highest, harmonics much lower: are harmonics just unwanted noise?

No.

For our **transfer measurement**, yes:

the fundamental at the commanded frequency is the wanted quantity.

If AFG is at 1 kHz, then for:

$$
H(1kHz)
$$

use the coherent **1 kHz component**.

But a harmonic is not automatically noise.

Harmonics are:

$$
2f_0,\ 3f_0,\ 4f_0,\ldots
$$

They can indicate:

- distortion;
- clipping;
- nonlinearity;
- asymmetry;
- generator distortion;
- circuit behavior.

Random noise is different.

For example:

$$
A_1=100mV
$$

$$
A_3=5mV
$$

Third harmonic relative to fundamental:

$$
\frac{5}{100}=0.05
$$

$$
=0.05
$$

That is deterministic distortion at 3$f_0$, not necessarily noise.

For transfer:

$$
H(f_0)
$$

use only the $f_0$ component.

But keep the harmonics because they tell us about waveform quality and may eventually be useful for actuator-health diagnostics.

---

# 8. Why does filtering increase phase lag?

For a first-order RC low-pass:

$$
H(j\omega)=\frac{1}{1+j\omega RC}
$$

Its magnitude is:

$$
|H|=
\frac1{\sqrt{1+(\omega RC)^2}}
$$

and its phase:

$$
\boxed{\phi=-\tan^{-1}(\omega RC)}
$$

Using:

$$
\omega RC=\frac f{f_c}
$$

we get:

$$
\phi=-\tan^{-1}\left(\frac f{f_c}\right)
$$

At:

$$
f=0.1f_c
$$

$$
\phi=-\tan^{-1}(0.1)
=-5.71^\circ
$$

At:

$$
f=f_c
$$

$$
\phi=-\tan^{-1}(1)
=-45^\circ
$$

At:

$$
f=10f_c
$$

$$
\phi=-\tan^{-1}(10)
=-84.3^\circ
$$

Physically, the capacitor stores and releases charge.

It cannot reproduce rapid voltage changes instantaneously.

The faster the input changes, the more the capacitor's behavior causes the output waveform to trail behind the input.

Important nuance: an RC filter does **not** simply add one fixed time delay. Its phase depends on frequency.

---

# 9. What does “close to Nyquist” mean?

Nyquist:

$$
f_N=\frac{f_s}{2}
$$

Our old case:

$$
f_s=25kSa/s
$$

Therefore:

$$
f_N=12.5kHz
$$

We were measuring:

$$
f=10kHz
$$

So:

$$
\frac f{f_N}
=
\frac{10}{12.5}
=0.8
$$

The signal was at **80% of Nyquist**.

Samples per cycle:

$$
\frac{25k}{10k}=2.5
$$

Only 2.5 samples/cycle.

Angle between neighboring samples:

$$
\frac{360^\circ}{2.5}=144^\circ
$$

That is terrible for accurate waveform/phase interpretation.

Compare 25 samples/cycle:

$$
\frac{360^\circ}{25}=14.4^\circ
$$

Much better.

## Aliasing problem

Suppose the 10 kHz waveform contains a second harmonic:

$$
2f=20kHz
$$

But Nyquist is only:

$$
12.5kHz
$$

So 20 kHz cannot be represented correctly.

At:

$$
f_s=25kHz
$$

20 kHz aliases to:

$$
|25-20|=5kHz
$$

The scope/data could therefore show an apparent 5 kHz component that was actually 20 kHz.

So “below Nyquist” does not automatically mean “good measurement”.

Nyquist is the theoretical minimum boundary, not a recommended operating point.

---

# 10. Are we measuring OUT and IP− to calculate residual noise?

No.

We measure them together to calculate **transfer**.

CH1 gives current:

$$
I(f)=\frac{V_{CH1}(f)}{67\Omega}
$$

CH2 gives sensor output:

$$
V_{OUT}(f)
$$

Then:

$$
H(f)=
\frac{V_{OUT}(f)}
{V_{CH1}(f)/67}
$$

Residual is calculated separately.

For CH2:

$$
e_{CH2}(t)
=
V_{CH2}(t)
-
[V_{DC}+V_{target}(t)]
$$

Similarly CH1 can have its own residual.

Do not calculate:

$$
CH2-CH1
$$

because they do not represent the same scaled physical quantity.

---

# 11. How do I determine $V_{DC}$ manually from an AC-varying signal?

For:

$$
v(t)=V_{DC}+A\sin(\omega t)
$$

the sine's average over a complete number of cycles is zero.

Therefore:

$$
V_{DC}
=
\frac1T\int_0^Tv(t)\,dt
$$

because:

$$
\frac1T\int_0^T A\sin(\omega t)\,dt=0
$$

For sampled data:

$$
\boxed{
V_{DC}
=
\frac1N\sum_{n=0}^{N-1}v[n]
}
$$

So simply add all voltage samples and divide by the number of samples.

On the scope, the **Mean** measurement does this for you.

For a clean symmetric sine, approximately:

$$
V_{DC}=
\frac{V_{max}+V_{min}}2
$$

Example:

$$
V_{max}=0.506V
$$

$$
V_{min}=0.494V
$$

Then:

$$
V_{DC}
=
\frac{0.506+0.494}{2}
$$

$$
=\frac{1.000}{2}
$$

$$
\boxed{0.500V}
$$

For noisy signals, use Mean, because one noise spike can corrupt $V_{max}$ or $V_{min}$.

Very important:

If the scope channel is **AC coupled**, the scope intentionally removes the original DC component.

So to measure $V_{DC}$:

$$
\boxed{\text{use DC coupling}}
$$

---

# 12. How do I understand sine and cosine from the AFG?

The AFG normally produces one sinusoid.

For example:

$$
v(t)=A\sin(\omega t)
$$

Cosine is not a different kind of periodic signal.

It is the same waveform shifted by $90^\circ$:

$$
\cos(\omega t)
=
\sin(\omega t+90^\circ)
$$

Our analysis uses both because any phase-shifted sine can be written as:

$$
A\sin(\omega t)+B\cos(\omega t)
$$

Using:

$$
C\sin(\omega t+\phi)
$$

expand:

$$
C[\sin(\omega t)\cos\phi+
\cos(\omega t)\sin\phi]
$$

Therefore:

$$
A=C\cos\phi
$$

$$
B=C\sin\phi
$$

So:

$$
C=\sqrt{A^2+B^2}
$$

and:

$$
\phi=\operatorname{atan2}(B,A)
$$

The sine/cosine pair is therefore like an **x-y coordinate system for sinusoidal signals**.

The AFG still generates only one sine.

---

# 13. What does $-0.49\,dB$ represent?

For amplitude:

$$
dB=20\log_{10}\left(\frac{A_2}{A_1}\right)
$$

If:

$$
dB=-0.49
$$

then:

$$
\frac{A_2}{A_1}
=
10^{-0.49/20}
$$

$$
=10^{-0.0245}
$$

$$
\approx0.945
$$

So:

$$
\boxed{A_2\approx0.945\,A_1}
$$

Amplitude reduction:

$$
1-0.945=0.055
$$

So $-0.49dB$ means approximately **5.5% lower amplitude than the chosen reference**.

It does **not** mean $-0.49V$.

It does not directly mean power either.

For power we use:

$$
dB=10\log_{10}\left(\frac{P_2}{P_1}\right)
$$

Why 20 for amplitude?

Because:

$$
P\propto A^2
$$

Therefore:

$$
10\log(A_2^2/A_1^2)
=
20\log(A_2/A_1)
$$

In our project that $-0.49dB$ was an earlier 10 kHz versus 1 kHz amplitude-transfer estimate. The later complex-average estimate was around $-0.70dB$.

---

# 14. What is a complex transfer phasor?

A sinusoid has two important properties:

- magnitude;
- phase.

A phasor stores both.

Instead of constantly writing:

$$
v(t)=A\sin(\omega t+\phi)
$$

we can represent that sinusoid at one frequency as:

$$
\tilde V=A\angle\phi
$$

Input current:

$$
\tilde I=I\angle\phi_I
$$

Output voltage:

$$
\tilde V=V\angle\phi_V
$$

Transfer:

$$
H=
\frac{\tilde V}{\tilde I}
$$

Therefore:

$$
|H|=\frac{V}{I}
$$

and:

$$
\phi_H=\phi_V-\phi_I
$$

Example:

$$
H(10kHz)
=
0.784\angle-59.9^\circ\,V/A
$$

Meaning:

- magnitude $=0.784V/A$;
- output lags current reference by $59.9^\circ$.

A phasor can also be written:

$$
H=a+jb
$$

Using approximately:

$$
0.784\angle-60^\circ
$$

$$
a=0.784\cos(-60^\circ)
\approx0.392
$$

$$
b=0.784\sin(-60^\circ)
\approx-0.679
$$

so approximately:

$$
H\approx0.392-j0.679
$$

These two forms contain the same information.

---

# 15. Does the ACS724 internal filter allow only signals below 15.5 kHz?

No.

There are two misconceptions here.

First, **15.5 kHz was not the entire ACS724 internal bandwidth**.

It came from our FILTER-pin RC approximation with:

$$
R_F\approx1.8k\Omega
$$

stock capacitor:

$$
1nF
$$

plus external:

$$
4.7nF
$$

Total:

$$
C=5.7nF
$$

Then:

$$
f_c=
\frac1{2\pi RC}
$$

$$
=
\frac1{
2\pi(1800)(5.7\times10^{-9})
}
$$

$$
\approx15.5kHz
$$

Second, a low-pass is not a brick wall.

At:

$$
f=f_c
$$

the output is:

$$
|H|=
\frac1{\sqrt2}
=0.707
$$

So 70.7% amplitude still passes.

At 10 kHz with $f_c=15.5kHz$:

$$
\frac f{f_c}
=
\frac{10}{15.5}
=0.645
$$

$$
|H|=
\frac1{\sqrt{1+0.645^2}}
$$

$$
=
\frac1{\sqrt{1.416}}
$$

$$
\approx0.840
$$

So about:

$$
\boxed{0.84}
$$

still passes.

At $10f_c$:

$$
|H|=
\frac1{\sqrt{1+100}}
\approx0.0995
$$

Even there it is not mathematically zero.

The stock 1 nF carrier gives a simple RC prediction around:

$$
88kHz
$$

and the device's broader analog bandwidth is around 120 kHz.

---

# 16. Can CH1 and CH2 show different phase when measuring the same node?

Electrically:

$$
\boxed{\text{same node + same ground + same instant → phase } \approx0^\circ}
$$

Therefore if they show nonzero phase on the same physical signal, it is a measurement-system effect.

Our same-node control showed approximately:

$$
CH1[n]\approx CH2[n+1]
$$

That means exported CH2 appeared about one stored sample later.

At 10 kHz:

$$
\Delta t=4\mu s
$$

$$
T=100\mu s
$$

Phase:

$$
360^\circ\frac4{100}
=14.4^\circ
$$

At 1 kHz we deliberately used:

$$
\Delta t=40\mu s
$$

$$
T=1000\mu s
$$

Again:

$$
360^\circ\frac{40}{1000}
=14.4^\circ
$$

So the one-sample alignment artifact corresponded to approximately the same phase because we deliberately kept **25 samples/cycle**.

We do **not** know the exact internal reason in the DOS1102S.

It could involve acquisition, processing, alignment or export, but that was not proven.

What is proven is the same-node experimental observation.

---

# 17. What does $H(10k)/H(1k)$ tell us?

A ratio answers:

> How large is one quantity relative to another?

If:

$$
R=\frac{A_2}{A_1}
$$

then:

- $R=1$: equal
- $R<1$: numerator is smaller
- $R>1$: numerator is larger.

For transfer:

$$
H_{norm}
=
\frac{H(10kHz)}{H(1kHz)}
$$

Using project values:

$$
|H_1|\approx0.850V/A
$$

$$
|H_{10}|\approx0.784V/A
$$

Magnitude ratio:

$$
\frac{0.784}{0.850}
=0.922
$$

Therefore:

$$
\boxed{|H_{10}/H_1|\approx0.922}
$$

Meaning:

10 kHz transfer magnitude is approximately **92.2% of the 1 kHz transfer magnitude**.

Loss:

$$
1-0.922=0.078
$$

$$
=0.078
$$

In dB:

$$
20\log_{10}(0.922)
\approx-0.70dB
$$

Now phase.

Suppose:

$$
\phi_1=-18.18^\circ
$$

$$
\phi_{10}=-59.87^\circ
$$

Complex division subtracts phases:

$$
\phi_{norm}
=
-59.87-(-18.18)
$$

$$
=-41.69^\circ
$$

So:

$$
\boxed{
\frac{H(10k)}{H(1k)}
\approx
0.922\angle-41.7^\circ
}
$$

Interpretation:

> Compared with 1 kHz, the system passes about 92.2% as much magnitude at 10 kHz and introduces about 41.7° additional phase lag.

This normalization is useful because constant gain/sensitivity errors tend to cancel.

---

# 18. How do I calculate propagation delay, response time and rise time?

Normally from a **step response**.

They are different quantities.

## Propagation delay $t_{pd}$

For the ACS724 definition:

Measure:

- time when input reaches 20%;
- time when output reaches 20%.

Then:

$$
\boxed{
t_{pd}
=
t_{OUT,20}
-
t_{IN,20}
}
$$

Example:

$$
t_{IN,20}=3\mu s
$$

$$
t_{OUT,20}=5\mu s
$$

Then:

$$
t_{pd}=5-3
=2\mu s
$$

## Response time

Using 90%:

$$
\boxed{
t_{response}
=
t_{OUT,90}
-
t_{IN,90}
}
$$

Example:

$$
t_{IN,90}=8\mu s
$$

$$
t_{OUT,90}=14\mu s
$$

Then:

$$
t_{response}=14-8
=6\mu s
$$

## Rise time

Rise time belongs to the **output itself**:

$$
\boxed{
t_r=t_{OUT,90}-t_{OUT,10}
}
$$

Example:

$$
t_{OUT,10}=4\mu s
$$

$$
t_{OUT,90}=14\mu s
$$

$$
t_r=10\mu s
$$

For an ideal first-order RC:

$$
V(t)=1-e^{-t/\tau}
$$

At 10%:

$$
0.1=1-e^{-t_{10}/\tau}
$$

$$
e^{-t_{10}/\tau}=0.9
$$

$$
t_{10}=-\tau\ln(0.9)
$$

$$
t_{10}=0.1053\tau
$$

At 90%:

$$
0.9=1-e^{-t_{90}/\tau}
$$

$$
e^{-t_{90}/\tau}=0.1
$$

$$
t_{90}=-\tau\ln(0.1)
$$

$$
t_{90}=2.3026\tau
$$

Therefore:

$$
t_r
=
2.3026\tau-0.1053\tau
$$

$$
\boxed{t_r=2.1973\tau}
$$

Since:

$$
f_c=\frac1{2\pi\tau}
$$

then:

$$
\tau=\frac{t_r}{2.197}
$$

so:

$$
f_c=
\frac{2.197}{2\pi t_r}
$$

$$
\boxed{f_c\approx\frac{0.35}{t_r}}
$$

But this relationship is for an approximate first-order system. The complete ACS724 is more complex, so actual step measurements are preferable.

---

# 19. Why does $RC=f/f_c$?

It does **not**.

The correct expression is:

$$
\boxed{\omega RC=\frac f{f_c}}
$$

Start with:

$$
f_c=\frac1{2\pi RC}
$$

and:

$$
\omega=2\pi f
$$

Then:

$$
\omega RC
=
(2\pi f)RC
$$

From:

$$
f_c=\frac1{2\pi RC}
$$

rearrange:

$$
2\pi RC=\frac1{f_c}
$$

Therefore:

$$
\omega RC
=
f\frac1{f_c}
$$

$$
\boxed{\omega RC=\frac f{f_c}}
$$

Units confirm this.

$RC$:

$$
\Omega F=s
$$

so RC has units of **seconds**.

But:

$$
\frac f{f_c}
$$

has:

$$
\frac{Hz}{Hz}=1
$$

dimensionless.

So $RC$ alone could never equal $f/f_c$.

But $\omega RC$ is dimensionless because:

$$
\omega[1/s]\times RC[s]=1
$$

---

# 20. Why does delay contribute to phase shift?

Suppose input is:

$$
x(t)=\sin(2\pi ft)
$$

Now delay it by $t_d$:

$$
y(t)=x(t-t_d)
$$

Therefore:

$$
y(t)
=
\sin[2\pi f(t-t_d)]
$$

Expand:

$$
y(t)
=
\sin(2\pi ft-2\pi ft_d)
$$

So delay creates phase:

$$
\boxed{
\phi=-2\pi ft_d
}
$$

in radians.

In degrees:

$$
\boxed{
\phi=-360^\circ ft_d
}
$$

Example:

$$
t_d=2\mu s
$$

At 1 kHz:

$$
\phi=
-360(1000)(2\times10^{-6})
$$

$$
=-0.72^\circ
$$

At 10 kHz:

$$
\phi=
-360(10000)(2\times10^{-6})
$$

$$
=-7.2^\circ
$$

Same physical delay.

But ten times the phase at ten times the frequency.

Why?

Because 2 µs occupies a larger percentage of a short 10 kHz period than of a long 1 kHz period.

For 1 kHz:

$$
T=1000\mu s
$$

$$
\frac{2}{1000}=0.002
$$

For 10 kHz:

$$
T=100\mu s
$$

$$
\frac2{100}=0.02
$$

Ten times larger fraction of a cycle.

---

# 21. What is RC corner frequency?

For a first-order RC low-pass:

$$
\boxed{
f_c=\frac1{2\pi RC}
}
$$

The corner frequency is the frequency where the filter begins transitioning significantly from “mostly pass” toward “increasing attenuation”.

It is not a hard cutoff.

At the corner several very useful things happen simultaneously.

## Capacitor reactance equals resistor resistance

Capacitor reactance magnitude:

$$
|X_C|=
\frac1{2\pi fC}
$$

At $f=f_c$:

$$
|X_C|
=
\frac1{2\pi f_cC}
$$

Substitute:

$$
f_c=\frac1{2\pi RC}
$$

Then:

$$
|X_C|
=
\frac1{
2\pi
\left(\frac1{2\pi RC}\right)
C
}
$$

The denominator simplifies to:

$$
\frac C{RC}
=
\frac1R
$$

Therefore:

$$
\boxed{|X_C|=R}
$$

So at the corner, resistor and capacitor impedance magnitudes are equal.

## Magnitude becomes $1/\sqrt2$

RC low-pass:

$$
|H|=
\frac1{\sqrt{1+(f/f_c)^2}}
$$

At:

$$
f=f_c
$$

$$
|H|=
\frac1{\sqrt{1+1}}
$$

$$
=
\frac1{\sqrt2}
$$

$$
=0.707
$$

So output amplitude is:

$$
\boxed{0.707}
$$

of the low-frequency value.

In dB:

$$
20\log_{10}(0.707)
$$

$$
\boxed{-3.01dB}
$$

## Phase is $-45^\circ$

$$
\phi
=
-\tan^{-1}\left(\frac f{f_c}\right)
$$

At $f=f_c$:

$$
\phi=-\tan^{-1}(1)
$$

$$
\boxed{-45^\circ}
$$

## Relation to time constant

$$
\tau=RC
$$

and:

$$
\boxed{
f_c=\frac1{2\pi\tau}
}
$$

So larger $RC$:

$$
RC\uparrow
\Rightarrow
f_c\downarrow
$$

slower filter.

Smaller $RC$:

$$
RC\downarrow
\Rightarrow
f_c\uparrow
$$

faster filter.

### Example from our ACS724 4.7 nF candidate

$$
R=1.8k\Omega
$$

$$
C_{total}=5.7nF
$$

Time constant:

$$
\tau=RC
$$

$$
=1800\times5.7\times10^{-9}
$$

$$
=10.26\times10^{-6}s
$$

$$
\boxed{\tau=10.26\mu s}
$$

Corner:

$$
f_c=
\frac1{2\pi(10.26\mu s)}
$$

$$
\boxed{f_c\approx15.5kHz}
$$

That does **not** mean 15.5 kHz is the last frequency allowed through.

It means that at 15.5 kHz:

$$
|H|=0.707
$$

and:

$$
\phi=-45^\circ
$$

for that simple first-order RC model.

One final distinction is important for this project: this first-order RC reasoning applies nicely to the **ACS724 FILTER approximation**. Our later MCP6022 AFE is a multi-pole Sallen-Key filter, so you should not blindly apply the simple $f_c=1/(2\pi RC)$, $-45^\circ$ rule to the entire fourth-order AFE.
