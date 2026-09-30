These five ideas are tightly connected, so the easiest way to understand them is as one chain.

### Two cascaded unity-gain Sallen-Key stages

A **Sallen-Key stage** is an active filter built from:

- an op-amp,
- two resistors,
- two capacitors.

One stage is a **second-order low-pass filter**. “Second-order” means its transfer function has two poles and, far above cutoff, its attenuation tends toward about:

\[
-40\ \text{dB/decade}
\]

In our design we use **two** such stages one after another:

```text id="c7debk"
ACS724
   ↓
2nd-order Sallen-Key
   ↓
2nd-order Sallen-Key
   ↓
ADC
```

“Cascaded” simply means:

> output of stage 1 feeds input of stage 2.

Two second-order stages together give:

\[
2 + 2 = 4
\]

so the complete filter is **fourth-order**.

That gives a much steeper roll-off:

\[
-80\ \text{dB/decade}
\]

far above the cutoff.

The term **unity-gain** means neither stage is intentionally amplifying the DC/passband signal. Ideally:

\[
V_{out} \approx V_{in}
\]

for low frequencies.

That is important because the ACS724 already produces roughly the voltage span we want for the ADC. We do not need extra gain.

---

### 15 kHz fourth-order Butterworth response

This describes the behavior of the **complete two-stage filter**.

“15 kHz” is the nominal cutoff frequency.

For the complete filter, at around:

\[
f_c = 15\,\text{kHz}
\]

the amplitude is approximately:

\[
-3\,\text{dB}
\]

which means the voltage amplitude is about:

\[
0.707
\]

of the low-frequency amplitude.

For example, if the input sine is:

\[
100\,\text{mV}_{pp}
\]

then around 15 kHz we expect roughly:

\[
70.7\,\text{mV}_{pp}
\]

at the complete filter output.

But our actual reason for choosing 15 kHz is not that 15 kHz itself is interesting. Our required information band is:

\[
DC \rightarrow 10\,\text{kHz}
\]

and the ADC sampling rate will be:

\[
100\,\text{kS/s}
\]

so Nyquist is:

\[
50\,\text{kHz}
\]

We therefore want:

```text id="d69y0a"
0 ───────── 10 kHz     15 kHz                50 kHz
| useful data |          |                     |
| nearly flat |       cutoff             strongly attenuated
```

Our nominal design gives approximately:

\[
-0.124\,\text{dB at 10 kHz}
\]

so the diagnostic band is almost unaffected, while around 50 kHz it gives about:

\[
-41.9\,\text{dB}
\]

which strongly suppresses frequencies that could alias into the sampled data.

“**Butterworth**” describes the shape of the response.

A Butterworth filter is designed to have a **maximally flat passband**. There is no intentional ripple before cutoff.

Conceptually:

```text id="0ur0zh"
Gain
1.0 ────────────────╮
                    │
                    ╰─────
                           ╲
                            ╲
                             ╲
frequency →
```

rather than a response that deliberately rises and falls in the passband.

That is desirable for us because we want the measured motor-current spectrum to remain as undistorted as reasonably possible inside 0–10 kHz.

---

### Low-Q

Now we need the idea of **Q**, because this is what makes the two stages different.

For a second-order filter, Q describes how strongly the stage responds around its natural frequency.

A **low-Q** stage is heavily damped.

Its response bends downward smoothly and relatively early. It does not peak.

Our first stage has approximately:

\[
Q_1 \approx 0.548
\]

Its nominal components are:

\[
R_1=R_2=9.76\,k\Omega
\]

\[
C_1=1.2\,nF
\]

\[
C_2=1.0\,nF
\]

Around 10 kHz, this stage alone is already attenuating quite noticeably:

\[
|H|\approx0.744
\]

or:

\[
-2.57\,\text{dB}
\]

That is **not a failure**.

This becomes important when we measure it on the bench. If we test only the first stage and see:

```text id="eiot25"
100 mVpp input
      ↓
~74 mVpp at 10 kHz
```

that is approximately what the design predicts.

---

### High-Q

The second stage is different.

It has:

\[
Q_2 \approx 1.304
\]

That is a **high-Q** stage.

A higher-Q second-order low-pass can have some gain near its pole frequency even though its DC gain is still 1.

So its response looks conceptually more like:

```text id="nog3mu"
Gain
             ╭──
1.0 ────────╯  ╲
               ╲
                ╲
frequency →
```

The stage is still a low-pass filter, but close to cutoff it has some **peaking**.

Our high-Q stage uses:

\[
R_1=R_2=4.07\,k\Omega
\]

\[
C_1=6.8\,nF
\]

\[
C_2=1.0\,nF
\]

At 10 kHz, for example, this stage considered by itself has a magnitude around:

\[
1.325
\]

or approximately:

\[
+2.44\,\text{dB}
\]

That sounds strange at first:

> Why would we make one stage attenuate and another stage amplify?

Because we do **not care about either stage independently** as the final result.

They are mathematically designed as a pair.

At 10 kHz:

\[
H_{total}=H_{lowQ}\times H_{highQ}
\]

approximately:

\[
0.744 \times 1.325 \approx 0.986
\]

So together:

\[
|H_{total}|\approx0.986
\]

which is only:

\[
-0.124\,\text{dB}
\]

That is the Butterworth magic here.

The low-Q and high-Q sections complement each other so that the **combined fourth-order response is very flat** before the cutoff.

---

### Why do we need one low-Q and one high-Q stage?

Because a fourth-order Butterworth filter mathematically contains **four poles**.

Instead of implementing one complicated fourth-order circuit directly, we split those four poles into two second-order pairs.

The two pairs need different Q values:

\[
Q_1\approx0.541
\]

and

\[
Q_2\approx1.307
\]

If we built two identical second-order stages, we would **not get a fourth-order Butterworth response**.

This is why the repository explicitly says the two stages are not just “two generic RC filters”.

---

### Unity-gain follower

Now focus only on the MCP6022 op-amp itself.

A normal op-amp has:

```text id="q43w37"
         + input
            \
             >──── output
            /
         - input
```

For the unity-gain configuration, we connect the output directly back to the negative input:

```text id="w5x0al"
            ┌─────────────┐
            │             │
Vin ─────── +             │
             \            │
              >──── Vout ─┘
             /
            -
```

So:

\[
V_- = V_{out}
\]

The op-amp tries to make:

\[
V_+ \approx V_-
\]

Therefore:

\[
V_{out}\approx V_+
\]

Hence:

\[
\frac{V_{out}}{V_{in}}\approx1
\]

That is why it is called a **unity-gain follower** or **voltage follower**.

But it does something very useful even though its voltage gain is 1.

It provides **buffering**.

The input draws almost no current, while the output can drive the next circuit much more strongly.

Conceptually:

```text id="swczoj"
weak/high-impedance signal
          ↓
      op-amp buffer
          ↓
strong/low-impedance output
```

That means stage 2 and later the ADC do not significantly load the sensitive RC network of stage 1.

---

The important distinction is this:

```text id="3z2jnz"
unity-gain follower
```

describes **how the op-amp itself is connected**.

```text id="hsgwot"
Sallen-Key filter
```

describes **the complete op-amp + R + C network**.

And:

```text id="gb2uc6"
low-Q stage + high-Q stage
```

describes the two different second-order sections.

Together they produce:

\[
\boxed{\text{4th-order, 15 kHz Butterworth low-pass filter}}
\]

That is the complete AFE filter we are building.

We picked **Sallen-Key + Butterworth** because several project requirements meet in exactly that combination. The important thing is that these are two different choices:

- **Sallen-Key** = *how we physically implement each second-order filter section.*
- **Butterworth** = *what frequency-response shape we want the complete filter to have.*

### Why do we need a low-pass filter at all?

Our useful current information is defined as:

\[
DC \rightarrow 10\,\text{kHz}
\]

and later the ADC samples at:

\[
f_s=100\,\text{kS/s}
\]

so the Nyquist frequency is:

\[
f_N=\frac{f_s}{2}=50\,\text{kHz}
\]

Anything above 50 kHz can fold back into the measured spectrum as **aliasing**.

For example, with 100 kS/s sampling, a real analog component at 90 kHz can appear in sampled data as something around:

\[
100-90=10\,\text{kHz}
\]

That is dangerous because after sampling we cannot distinguish that fake 10 kHz component from genuine motor information at 10 kHz.

So before the ADC we need analog filtering:

```text id="saitqd"
real current signal
        ↓
     ACS724
        ↓
 keep DC–10 kHz
 suppress high frequencies
        ↓
       ADC
```

This is the main reason for the AFE filter.

---

## Why Butterworth?

We have two competing requirements.

We want **almost no attenuation at 10 kHz**:

\[
A(10\,kHz)\leq1\,dB
\]

but we want **strong attenuation by 50 kHz**:

\[
A(50\,kHz)\geq20\,dB
\]

So the response needs to stay flat for quite a while and then fall rapidly.

Butterworth is especially useful for measurement because its defining characteristic is a **maximally flat magnitude response**.

Meaning there is no intentional ripple such as:

```text id="4sgvcy"
bad for our purpose:

gain
      _   _   _
1 ───/ \_/ \_/ \__
```

Instead it looks approximately:

```text id="2tqum3"
Butterworth:

gain
1 ─────────────────╮
                   ╰──
                      ╲
                       ╲
                        ╲
frequency →
```

This is attractive for the actuator project because when MATLAB later sees, for example:

- 500 Hz component,
- 2 kHz component,
- 5 kHz component,
- 8 kHz component,

we don't want the analog filter itself deliberately boosting and reducing alternating portions of that spectrum.

A **Chebyshev** filter could give a sharper transition, but does so partly by accepting passband ripple.

A **Bessel** filter gives better time-domain/phase behavior, but rolls off more slowly.

Butterworth is therefore a good compromise here:

\[
\boxed{\text{flat useful band + strong enough attenuation above it}}
\]

It is not “the universally best filter”. It is appropriate for the particular measurement requirements we established.

---

# Why 15 kHz?

Our useful band finishes at:

\[
10\,\text{kHz}
\]

If we put the filter cutoff at 10 kHz, the highest useful frequency would already be strongly attenuated.

So we put the overall Butterworth cutoff somewhat above it:

\[
f_c\approx15\,\text{kHz}
\]

That allows 10 kHz through almost unchanged.

For our fourth-order design:

\[
|H(10\,kHz)|\approx-0.124\,dB
\]

which corresponds to approximately:

\[
10^{-0.124/20}\approx0.986
\]

So a 100 mV signal at 10 kHz becomes approximately:

\[
98.6\,mV
\]

Very little is lost.

But at 50 kHz:

\[
|H(50\,kHz)|\approx-41.9\,dB
\]

or only about:

\[
0.8\%
\]

of the voltage amplitude.

So:

```text id="dp0z3o"
10 kHz:  ████████████████████   ~98.6%
50 kHz:  ▏                      ~0.8%
```

That's exactly the kind of separation we want.

---

# Why fourth-order?

Every filter “order” gives us more slope after the cutoff.

Roughly:

\[
1^\text{st}\text{ order} \rightarrow -20\,dB/decade
\]

\[
2^\text{nd}\text{ order} \rightarrow -40\,dB/decade
\]

\[
4^\text{th}\text{ order} \rightarrow -80\,dB/decade
\]

A first-order RC filter would force an unpleasant compromise: either preserve 10 kHz well or suppress 50 kHz strongly, but not both particularly well.

A second-order filter could get much closer, but the fourth-order solution gives us considerably more attenuation margin.

And there was another practical reason:

We already selected a **MCP6022**.

The “2” is significant: it contains **two op-amps**.

Each op-amp can implement one second-order Sallen-Key section:

```text id="slxb9j"
MCP6022

Op-amp A → 2nd-order filter
Op-amp B → 2nd-order filter
                  ↓
            4th order total
```

So the available component fits the architecture naturally.

---

# Why Sallen-Key?

There are several ways to build an active second-order filter.

Sallen-Key is particularly convenient for our case because we want approximately:

\[
\text{gain}=1
\]

and we don't want to level-shift the ACS724 output.

The ACS724 already gives approximately:

\[
0.5\rightarrow4.5\,V
\]

which fits nicely inside our approximately 0–5 V ADC domain.

So there's little point doing:

```text id="ayu11f"
sensor → amplify → attenuate → ADC
```

We want:

```text id="ocdamp"
sensor → filter/buffer → ADC
```

Sallen-Key lets the MCP6022 act essentially as a **voltage follower** while the surrounding R and C components create the desired frequency response.

It is also:

- non-inverting;
- relatively simple;
- low component count;
- easy to cascade;
- well suited to a dual op-amp;
- able to realize different Q values without requiring intentional signal gain.

That last point is important.

---

# Now: what exactly is “natural frequency”?

This is one of the concepts worth understanding properly.

For a generic second-order low-pass filter, we often write:

\[
H(s)=
\frac{\omega_0^2}
{s^2+\frac{\omega_0}{Q}s+\omega_0^2}
\]

Two important parameters appear:

\[
\omega_0
\]

and:

\[
Q
\]

The first is the **natural angular frequency**.

Usually we express it in ordinary frequency:

\[
f_0=\frac{\omega_0}{2\pi}
\]

For our Sallen-Key stages, \(f_0\) is approximately:

\[
15\,kHz
\]

---

## Physical intuition first

Think about a mechanical spring and mass.

If you pull the mass and let it go, the system has a frequency at which it naturally wants to oscillate:

```text id="kyu703"
wall ─ spring ─ mass

       ←→ ←→ ←→
```

That frequency depends on things like:

- spring stiffness;
- mass.

Electrical second-order systems have mathematically equivalent behavior.

Instead of mass and spring, we have energy-storage elements—in our case capacitors plus an active circuit.

So a second-order circuit has a characteristic frequency built into its component values.

That is its **natural frequency**.

It doesn't mean our low-pass circuit must literally sit there continuously oscillating at 15 kHz.

It means:

> Around this characteristic frequency, the two-pole dynamics of the circuit become dominant.

---

# Natural frequency is NOT always the same as cutoff frequency

This distinction is important.

For a first-order filter, we usually talk about one obvious corner frequency.

For a second-order system, behavior around \(f_0\) depends strongly on **Q**.

Two filters can have exactly:

\[
f_0=15\,kHz
\]

but behave completely differently around 15 kHz.

For example:

```text id="1juwsh"
same f0:

low Q:
──────────╲
           ╲
            ╲

high Q:
────────────╮
            ╰╮
             ╲
```

Why?

Because \(f_0\) tells us **where the pole pair sits in frequency**.

Q tells us **how strongly damped that pole pair is**.

---

# Our low-Q stage

For the first stage:

\[
f_0\approx14.89\,kHz
\]

and:

\[
Q\approx0.548
\]

The relatively low Q means strong damping.

So as we approach its natural frequency, its magnitude has already fallen considerably.

That's why our low-Q stage by itself around 15 kHz is much lower than −3 dB.

---

# Our high-Q stage

The second section has:

\[
f_0\approx15.00\,kHz
\]

but:

\[
Q\approx1.304
\]

Same approximate **natural frequency**.

Very different **Q**.

Because it is less damped, its response rises near \(f_0\).

So:

```text id="ismxki"
Low-Q stage:
                     \
                      \
                       \

High-Q stage:
                    /\
                   /  \
──────────────────     \

combined:
───────────────────╮
                   ╰──
```

The interesting part is that the two are deliberately designed to compensate each other.

Their combined response gives the flat fourth-order Butterworth shape.

---

# Where does the natural frequency come from in our components?

For the particular unity-gain Sallen-Key topology we're using, with equal resistors:

\[
R_1=R_2=R
\]

the natural frequency is:

\[
\boxed{
f_0=
\frac{1}
{2\pi R\sqrt{C_1C_2}}
}
\]

Look at our low-Q section:

\[
R=9.76\,k\Omega
\]

\[
C_1=1.2\,nF
\]

\[
C_2=1.0\,nF
\]

Then:

\[
f_0=
\frac{1}
{2\pi(9760)\sqrt{1.2\times10^{-9}\cdot1.0\times10^{-9}}}
\]

which gives approximately:

\[
\boxed{14.9\,kHz}
\]

So **we don't tell the op-amp “work at 15 kHz.”**

The resistor and capacitor values physically establish that characteristic frequency.

That's why we're being so careful about the component values.

---

And this gives us the next important conceptual connection:

\[
\boxed{R,C\rightarrow f_0}
\]

while the **ratio** of those component values also determines:

\[
\boxed{Q}
\]

So next, before we continue drawing the schematic, I think it is worth showing **exactly how our 1.2 nF versus 1.0 nF produces the low-Q value, and how 6.8 nF versus 1.0 nF produces the high-Q value**. That's the key to understanding why the two Sallen-Key stages look almost identical but behave so differently.


---

## Low-Q stage bring-up: first capacitor from N2A to GND_MEAS

Good. Removing the temporary capacitor bank is actually cleaner. Your schematic now matches the direction we want much better.

I checked the screenshot carefully:

- `R1 = 9.76k` is correct.
- `R2 = 9.76k` is correct.
- `TP_SENSOR → R1 → N1A → R2 → N2A → U1A pin 3` is correct.
- U1A **pin 1 → pin 2** feedback is correct.
- `5V_MEAS/GND_MEAS` and C1 decoupling are correct.
- ACS724 C12 = 4.7 nF and its updated note are consistent.
- The title block is now correctly changed to **Stage B – MCP6022 AFE bring-up**.

Now we add the first capacitor.

## Step 6A — add the capacitor from N2A to ground

Place:

```text id="uydude"
C13 = 1.0 nF
```

from:

```text id="e3707j"
N2A
 │
C13 1.0 nF
 │
GND_MEAS
```

So this part becomes:

```text id="0aug3d"
TP_SENSOR ─ R1 ─ N1A ─ R2 ─ N2A ── pin 3 (+)
                                   │
                                 C13
                                 1.0nF
                                   │
                               GND_MEAS
```

Do **not add the 1.2 nF capacitor yet**.

### Why does this capacitor go to ground?

A capacitor's impedance is:

\[
Z_C=\frac{1}{j\omega C}
\]

At very low frequency:

\[
\omega\rightarrow0
\]

therefore:

\[
|Z_C|\rightarrow\infty
\]

So C13 behaves almost like an open circuit.

At DC:

```text id="3ed3j6"
N2A ── C13 ── GND
        ↑
   effectively open
```

Almost no current flows through it.

Therefore the DC sensor voltage passes through R1/R2 with almost no drop:

\[
V_{N2A}\approx V_{TP\_SENSOR}
\]

which is exactly what we want.

---

As frequency increases:

\[
|Z_C|=\frac{1}{2\pi fC}
\]

gets smaller.

For `C = 1 nF`:

At 1 kHz:

\[
|Z_C|\approx159\,k\Omega
\]

At 10 kHz:

\[
|Z_C|\approx15.9\,k\Omega
\]

At 50 kHz:

\[
|Z_C|\approx3.18\,k\Omega
\]

Compare that with our resistors:

\[
R_1=R_2=9.76\,k\Omega
\]

Now you can see what starts happening.

At low frequency, C13 looks enormous compared with 9.76 kΩ, so almost nothing is diverted to ground.

At high frequency its impedance becomes comparable to — and eventually much lower than — the resistors.

So high-frequency current increasingly finds a path:

```text id="2jo2w2"
signal
  ↓
R1 → R2 → N2A
             │
            C13
             │
         GND_MEAS
```

That starts pulling the high-frequency voltage at `N2A` downward.

This is the fundamental low-pass behavior.

### But isn't that just an RC filter?

At this moment, **yes — partly**.

With only this capacitor installed, we do not yet have the complete Sallen-Key second-order behavior.

The important second capacitor will connect:

```text id="3o4k0g"
N1A → capacitor → OUTA
```

That creates the frequency-dependent feedback interaction which gives us the second pole and the required Q.

So think of today's first capacitor as:

> the obvious low-pass path.

The next capacitor is the less intuitive one that turns the network into the full Sallen-Key stage.

### One important naming detail

In the design equations/documentation this capacitor is called the low-Q section's:

\[
C_2=1.0\,nF
\]

But in KiCad it will be **C13**, because `C1–C12` have already been used historically.

So:

```text id="bothra"
mathematical C2 = KiCad C13 = 1.0 nF
```

That distinction will save us confusion later.

Add only **C13 = 1.0 nF from N2A to GND_MEAS**, then send me the screenshot.

Next we add the much more interesting **1.2 nF capacitor from N1A to U1A output**, and I'll derive why that connection determines Q instead of merely adding another ordinary RC pole.


---

## Completing the low-Q Sallen-Key section: why the second capacitor goes to OUTA

At this stage of the schematic, the low-Q section has:

\`\`\`text
TP_SENSOR ─ R1 9.76k ─ N1A ─ R2 9.76k ─ N2A ─ U1A pin 3 (+)

U1A pin 1 (OUTA) ─────────────── U1A pin 2 (−)
\`\`\`

The capacitor from \`N2A\` to \`GND_MEAS\` is the first energy-storage element:

\`\`\`text
N2A
 │
1.0 nF
 │
GND_MEAS
\`\`\`

The second capacitor must **not** also go to ground. It must connect:

\`\`\`text
N1A → 1.2 nF → OUTA
\`\`\`

This difference is what turns the network from a pair of simple RC sections into the intended unity-gain Sallen-Key second-order filter.

### Why not put both capacitors to ground?

If both capacitors were simply shunt capacitors to ground, the network would behave like two passive RC low-pass sections interacting through the resistor chain.

That is not the accepted Sallen-Key topology and it would not realize the required pole quality factor \(Q\).

The Sallen-Key topology deliberately makes the first capacitor see the **op-amp output** rather than ground.

The complete low-Q section is:

\`\`\`text
TP_SENSOR ── R1 ── N1A ── R2 ── N2A ───── pin 3 (+)
                       │          │
                     1.2 nF     1.0 nF
                       │          │
                       │       GND_MEAS
                       │
                       └──────── OUTA pin 1

OUTA pin 1 ───────────── pin 2 (−)
\`\`\`

### What does the capacitor from N1A to OUTA actually do?

At low frequency the 1.2 nF capacitor has very high impedance, so almost no current flows through it.

The op-amp behaves as a voltage follower and:

\[
V_{OUTA}\approx V_{N2A}\approx V_{TP\_SENSOR}
\]

As frequency increases, the capacitor impedance decreases:

\[
|Z_C|=\frac{1}{2\pi fC}
\]

Now current can flow between \`N1A\` and \`OUTA\`.

But \`OUTA\` is not ground. It is an actively driven voltage that follows \`N2A\`.

Therefore the current through this capacitor depends on:

\[
V_{N1A}-V_{OUTA}
\]

rather than simply:

\[
V_{N1A}-0
\]

That creates a frequency-dependent interaction between the resistor chain and the op-amp output.

This interaction changes the **damping** of the two-pole system. In other words, it sets the section's \(Q\).

### Transfer-function connection

For the unity-gain topology used here:

\[
H(s)=
\frac{1}
{1+sC_2(R_1+R_2)+s^2R_1R_2C_1C_2}
\]

where:

- \(C_1\) is the capacitor from \`N1A\` to \`OUTA\`;
- \(C_2\) is the capacitor from \`N2A\` to \`GND_MEAS\`.

Comparing this with the standard second-order denominator:

\[
1+\frac{s}{Q\omega_0}+\frac{s^2}{\omega_0^2}
\]

gives:

\[
\omega_0=
\frac{1}{\sqrt{R_1R_2C_1C_2}}
\]

and therefore:

\[
f_0=
\frac{1}
{2\pi\sqrt{R_1R_2C_1C_2}}
\]

The quality factor is:

\[
Q=
\frac{\sqrt{R_1R_2C_1C_2}}
{C_2(R_1+R_2)}
\]

For equal resistors \(R_1=R_2=R\):

\[
Q=
\frac{1}{2}\sqrt{\frac{C_1}{C_2}}
\]

This is the key relationship.

For the low-Q section:

\[
C_1=1.2\,nF
\]

\[
C_2=1.0\,nF
\]

so:

\[
Q=
\frac{1}{2}\sqrt{\frac{1.2}{1.0}}
\approx0.548
\]

That is the required low-Q behavior.

The resistor values then place the natural frequency near 15 kHz:

\[
f_0=
\frac{1}
{2\pi(9.76\,k\Omega)\sqrt{1.2\,nF\cdot1.0\,nF}}
\approx14.9\,kHz
\]

So the two capacitor connections have different jobs:

\`\`\`text
N2A → 1.0 nF → GND_MEAS
    establishes the direct frequency-dependent shunt path

N1A → 1.2 nF → OUTA
    creates the output-dependent interaction that sets the required Q
\`\`\`

Together with the two 9.76 kΩ resistors and unity-gain follower they form one complete second-order Sallen-Key low-pass section.


---

## Complete low-Q Sallen-Key stage: what the finished first section now does

The low-Q section is now:

\`\`\`text
TP_SENSOR ─ R1 9.76k ─ N1A ─ R2 9.76k ─ N2A ─ U1A pin 3 (+)
                         │          │
                       C3 1.2nF   C2 1.0nF
                         │          │
                         │       GND_MEAS
                         │
                         └──────── OUTA pin 1

OUTA pin 1 ───────────── U1A pin 2 (−)
\`\`\`

This is one complete second-order unity-gain Sallen-Key low-pass section.

### DC behavior

At DC, both capacitors behave approximately as open circuits.

Therefore almost no current flows through R1 and R2, so there is essentially no resistor voltage drop:

\[
V_{TP\_SENSOR}\approx V_{N1A}\approx V_{N2A}
\]

The op-amp is configured as a voltage follower:

\[
V_{OUTA}\approx V_{N2A}
\]

Therefore:

\[
V_{OUTA}\approx V_{TP\_SENSOR}
\]

The section preserves the sensor's DC level, which is essential because current is encoded in the ACS724 output's DC voltage.

### Frequency-dependent behavior

As frequency increases, both capacitor impedances decrease:

\[
|Z_C|=\frac{1}{2\pi fC}
\]

The capacitor from N2A to GND_MEAS increasingly shunts high-frequency current toward ground.

The capacitor from N1A to OUTA does something different: because OUTA follows N2A, current through this capacitor depends on the difference between N1A and the actively driven output voltage.

That active interaction determines the damping and therefore the quality factor Q.

### Natural frequency and Q

For this topology:

\[
f_0=
\frac{1}
{2\pi\sqrt{R_1R_2C_1C_2}}
\]

and:

\[
Q=
\frac{\sqrt{R_1R_2C_1C_2}}
{C_2(R_1+R_2)}
\]

For equal resistors:

\[
R_1=R_2=R
\]

the expressions simplify to:

\[
f_0=
\frac{1}
{2\pi R\sqrt{C_1C_2}}
\]

and:

\[
Q=
\frac12\sqrt{\frac{C_1}{C_2}}
\]

Using the low-Q values:

\[
R=9.76\,k\Omega
\]

\[
C_1=1.2\,nF
\]

\[
C_2=1.0\,nF
\]

gives:

\[
f_0\approx14.886\,kHz
\]

and:

\[
Q\approx0.548
\]

### Important: natural frequency is not the -3 dB frequency of this individual stage

For a unity-DC-gain second-order low-pass section, at its natural frequency:

\[
|H(f_0)|=Q
\]

For this low-Q section:

\[
|H(f_0)|\approx0.548
\]

which is about:

\[
20\log_{10}(0.548)\approx-5.23\,dB
\]

So seeing roughly -5.2 dB around 14.9 kHz from this first stage alone is expected.

The approximately -3 dB at 15 kHz requirement applies to the complete fourth-order Butterworth filter after the low-Q and high-Q sections are cascaded.

### Nominal low-Q transfer predictions

Using the accepted component values, the ideal stage response is approximately:

| Frequency | Magnitude | Gain | Phase |
|---:|---:|---:|---:|
| DC | 1.000 | 0 dB | 0° |
| 1 kHz | 0.997 | -0.026 dB | -7.0° |
| 5 kHz | 0.927 | -0.656 dB | -34.7° |
| 10 kHz | 0.744 | -2.566 dB | -65.9° |
| 15 kHz | 0.544 | -5.295 dB | -90.5° |
| 50 kHz | 0.0835 | -21.56 dB | -149.2° |

For a 100 mVpp sinusoidal input, this predicts approximately:

\`\`\`text
1 kHz  → 99.7 mVpp
5 kHz  → 92.7 mVpp
10 kHz → 74.4 mVpp
15 kHz → 54.4 mVpp
50 kHz → 8.35 mVpp
\`\`\`

These are prediction values for later bench comparison, not measured values.

### Why this first stage is intentionally low-Q

The first section is deliberately strongly damped. It begins attenuating before 15 kHz and does not peak.

The second, high-Q section will have the opposite tendency near its natural frequency. When the two stages are cascaded, their responses multiply and produce the intended flat fourth-order Butterworth response.

So the first stage should not be judged against the complete-filter response by itself.


---

## High-Q Sallen-Key stage: same natural frequency, different damping

The second MCP6022 section uses the same unity-gain Sallen-Key topology as the first section, but with different component ratios.

Accepted values:

\[
R_3=R_4=4.07\,k\Omega
\]

\[
C_4=6.8\,nF
\]

\[
C_5=1.0\,nF
\]

For equal resistors, the natural frequency is:

\[
f_0=
\frac{1}
{2\pi R\sqrt{C_1C_2}}
\]

and the quality factor is:

\[
Q=
\frac12\sqrt{\frac{C_1}{C_2}}
\]

Using \(R=4.07\,k\Omega\), \(C_1=6.8\,nF\), and \(C_2=1.0\,nF\):

\[
f_0\approx14.996\,kHz
\]

and:

\[
Q\approx1.304
\]

So the low-Q and high-Q sections have almost the same natural frequency, but very different damping.

The low-Q section uses:

\[
Q\approx0.548
\]

and therefore attenuates smoothly as frequency approaches \(f_0\).

The high-Q section uses:

\[
Q\approx1.304
\]

and therefore has resonant peaking around the natural-frequency region.

At exactly \(f_0\), a unity-DC-gain second-order low-pass has:

\[
|H(f_0)|=Q
\]

so the high-Q section has approximately:

\[
|H(f_0)|\approx1.304
\]

or about:

\[
+2.30\,dB
\]

The maximum peak is slightly below \(f_0\), around 12.6 kHz for this section, and is about:

\[
|H|_{max}\approx1.412
\]

or roughly:

\[
+3.0\,dB
\]

This peaking is intentional. It compensates the stronger attenuation of the low-Q first stage so the two cascaded sections together form the flat fourth-order Butterworth response.

The high-Q topology is:

\`\`\`text
OUTA ─ R3 4.07k ─ N1B ─ R4 4.07k ─ N2B ─ U1B pin 5 (+)
                     │          │
                   C4 6.8nF   C5 1.0nF
                     │          │
                     │       GND_MEAS
                     │
                     └──────── OUTB pin 7

OUTB pin 7 ───────── U1B pin 6 (−)
\`\`\`

As with the low-Q stage:

- the capacitor from N2B to GND_MEAS provides the direct high-frequency shunt path;
- the capacitor from N1B to OUTB creates the output-dependent Sallen-Key interaction that sets Q;
- the op-amp itself is a unity-gain follower.

The key design idea is:

\`\`\`text
same approximate f0
        +
different Q values
        ↓
two complementary second-order responses
        ↓
fourth-order Butterworth response
\`\`\`


---

## High-Q stage construction: resistor order and capacitor connections

The high-Q section must follow the accepted net order:

\`\`\`text
OUTA → R3 4.07k → N1B → R4 4.07k → N2B → U1B pin 5 (+)
\`\`\`

Because R3 and R4 have the same value, reversing their physical positions does not change the ideal electrical transfer function. However, keeping the reference designators aligned with the accepted net-level definition matters for traceability, troubleshooting, and later comparison between schematic, documentation, measurements, and BOM.

The unity-gain feedback is:

\`\`\`text
U1B pin 7 OUTB → U1B pin 6 (−)
\`\`\`

The high-Q capacitors are then connected as:

\`\`\`text
N1B → 6.8 nF → OUTB
N2B → 1.0 nF → GND_MEAS
\`\`\`

This is the same Sallen-Key topology as the low-Q stage, but with a much larger ratio between the feedback-side capacitor and the ground-side capacitor.

For equal resistors:

\[
Q=\frac12\sqrt{\frac{C_1}{C_2}}
\]

Using:

\[
C_1=6.8\,nF
\]

and:

\[
C_2=1.0\,nF
\]

gives:

\[
Q=\frac12\sqrt{6.8}\approx1.304
\]

The larger feedback-side capacitor means its impedance becomes lower than in the low-Q stage for the same frequency:

\[
|Z_C|=\frac{1}{2\pi fC}
\]

At 10 kHz:

\[
|Z_{6.8nF}|\approx2.34\,k\Omega
\]

while:

\[
|Z_{1.0nF}|\approx15.9\,k\Omega
\]

Therefore the N1B-to-OUTB feedback interaction is much stronger near the 10–15 kHz region than it was in the low-Q section.

That stronger frequency-dependent feedback produces much less damping and therefore the higher Q.

The natural frequency nevertheless remains close to 15 kHz because the resistor values are reduced to 4.07 kΩ:

\[
f_0=
\frac{1}
{2\pi(4.07\,k\Omega)\sqrt{6.8\,nF\cdot1.0\,nF}}
\approx15.0\,kHz
\]

The design therefore changes Q strongly while keeping the pole pair in approximately the same frequency region.

The completed high-Q section is:

\`\`\`text
OUTA ─ R3 4.07k ─ N1B ─ R4 4.07k ─ N2B ─ U1B pin 5 (+)
                     │          │
                   6.8 nF     1.0 nF
                     │          │
                     │       GND_MEAS
                     │
                     └──────── OUTB pin 7

OUTB pin 7 ───────── U1B pin 6 (−)
\`\`\`


---

## Cascading the completed low-Q and high-Q sections

After the high-Q capacitors are added, both MCP6022 channels implement complete second-order unity-gain Sallen-Key sections.

The signal path is:

\`\`\`text
TP_SENSOR
    ↓
low-Q section U1A
    ↓
OUTA
    ↓
high-Q section U1B
    ↓
OUTB / TP_AFE
\`\`\`

The low-Q output is the high-Q input. In an ideal linear cascade, the complete transfer function is the product of the two individual transfer functions:

\[
H_{total}(s)=H_{lowQ}(s)\,H_{highQ}(s)
\]

This multiplication is why the two sections can have very different individual responses but still form the desired fourth-order Butterworth response together.

The first section is strongly damped and attenuates near 15 kHz. The second section has higher Q and intentionally peaks in the same frequency region. Their combined magnitude response is approximately flat through the useful band and then rolls off rapidly above the cutoff.

For schematic clarity, the interstage node should be named explicitly as \`OUTA\` (or an equivalent unambiguous name) and the final AFE output should be named \`TP_AFE\`.

The required system-level signal nodes are therefore:

\`\`\`text
ACS724 VIOUT → TP_SENSOR
TP_SENSOR → low-Q stage
low-Q OUTA → high-Q stage
high-Q OUTB → TP_AFE
\`\`\`

These labels do not create additional electronics. They identify electrically common nodes and make the schematic, bench procedure, measurements, and documentation use the same vocabulary.

During independent Stage-B AFE bring-up, a clean test source may be injected at TP_SENSOR while the ACS724 output is physically disconnected. That is a temporary test configuration; it does not change the accepted product-level signal path shown in the schematic.


---

## MCP6022 supply conditioning: 100 nF bypass versus 10 µF reservoir

The AFE supply uses two capacitors with different jobs:

\`\`\`text
5V_MEAS
  │
  ├── 100 nF local bypass
  │
  └── 10 µF reservoir
  │
GND_MEAS
\`\`\`

The 100 nF capacitor should be physically very close to MCP6022 pins 8 and 4. Its small capacitance and low parasitic inductance make it effective for fast, high-frequency supply-current transients.

The 10 µF capacitor is a local energy reservoir. It is intended to support slower and larger supply variations caused by wiring impedance, breadboard connections, load changes, or other low-frequency disturbances on the measurement rail.

The two are therefore complementary rather than redundant.

A useful mental model is:

\`\`\`text
100 nF → fast disturbances
10 µF  → slower / larger disturbances
\`\`\`

Both capacitors connect directly between the same two supply nets:

\`\`\`text
5V_MEAS
   │
 capacitor
   │
GND_MEAS
\`\`\`

If the 10 µF part is polarized, its positive terminal must connect to 5V_MEAS and its negative terminal to GND_MEAS.

The reservoir capacitor is not part of the Sallen-Key transfer function. It conditions the op-amp power rail and should not be confused with the filter capacitors connected to N1A/N2A or N1B/N2B.
