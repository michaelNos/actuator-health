# Phase 9 — Communication Interface Design

**Status:** Design complete  
**Project:** Actuator Health Monitoring System

## Purpose

Phase 9 defines how Rev-1 communicates measurement, diagnostic and system-health information to a PC/MATLAB/controller without disturbing deterministic acquisition.

This phase selects the Rev-1 physical/logical communication strategy and the product-level data interface. Exact packet encoding, host software implementation, connector wiring and debugging remain deferred to Stage B unless required to make the architecture buildable.

## Accepted design inputs

- deterministic 100 kS/s acquisition must remain independent of communication workload;
- calibrated current data, signal features, diagnostic states and measurement-pipeline health are available from Phases 7–8;
- PC/MATLAB analysis and logging are required;
- Arduino UNO R4 WiFi is the Rev-1 MCU platform;
- MAX485 and MCP2551 modules are available but shall not be selected merely because they are on hand;
- Rev-1 is a low-voltage laboratory system; industrial scalability remains architectural rather than direct reuse of hobby hardware.

## 9.1 — Primary Rev-1 communication interface

### COM-001 — USB serial for laboratory PC/MATLAB integration

**Status:** Accepted

Rev-1 shall use the Arduino UNO R4 WiFi's **USB serial connection** as the primary communication interface to the laboratory PC/MATLAB environment.

USB is selected because Rev-1 is a low-voltage laboratory prototype and already provides the required direct PC connection without an additional external physical-layer transceiver. It supports development, logging, analysis and diagnostic interaction while keeping the hardware build simple.

Communication remains downstream of the deterministic acquisition path:

`ADC → RAM buffering → processing/diagnostics → USB communication`

USB activity, host latency or temporary communication congestion shall not control or perturb the hardware-timed 100 kS/s ADC sampling cadence. Where communication cannot keep pace with generated data, the firmware shall manage that condition explicitly rather than allowing transmission work to block deterministic acquisition.

Available MAX485 and MCP2551 hardware is not made mandatory for Rev-1 merely because it is available. RS-485 and CAN remain candidate future industrial communication layers where longer cables, noisy environments, differential signaling or networked nodes justify them.

### Rationale

USB provides the simplest appropriate Rev-1 path to the required PC/MATLAB environment. Separating the application data model from the physical transport preserves future scalability without adding industrial communication hardware before the laboratory monitoring concept is validated.

## 9.2 — Telemetry and waveform-transfer strategy

### COM-002 — Continuous low-rate telemetry plus on-demand waveform capture

**Status:** Accepted

Rev-1 communication shall distinguish between routine monitoring information and high-rate waveform data rather than requiring continuous transmission of every 100 kS/s ADC sample.

The **normal telemetry** data product shall provide the information needed for live monitoring, including as applicable:

- mean/RMS/peak current and other selected current features;
- current-signature/spectral feature outputs;
- operating state;
- diagnostic condition and retained event information;
- measurement-pipeline/system-health state.

A separate **waveform-capture** data product shall make raw and/or calibrated high-rate current samples available on demand for MATLAB analysis, characterization, calibration and debugging.

At 100 kS/s, representing each ADC sample in a 16-bit storage word already produces approximately:

`100,000 samples/s × 2 bytes/sample = 200 kB/s`

before framing and metadata. Continuous full-rate transmission is therefore not required for normal condition monitoring and shall not be allowed to become an architectural dependency.

Waveform capture shall preserve acquisition integrity. If communication is slower than the generated sample stream, capture/buffering and transfer shall be arranged so that USB transmission does not alter the deterministic sample cadence. Exact capture length, buffering implementation and transfer scheduling are Stage B details constrained by MCU memory and measured USB throughput.

### Rationale

Routine health monitoring requires compact features and diagnostic states, while development and detailed analysis sometimes require the original waveform. Separating these data products keeps ordinary communication lightweight without sacrificing access to high-resolution evidence when it is actually needed.

## 9.3 — Communication data model

### COM-003 — Versioned, sequenced, integrity-aware transport-independent messages

**Status:** Accepted

Rev-1 shall define telemetry and waveform-capture messages using an application-level data model that is not inherently tied to USB as a physical transport.

Each message or data block shall contain, as applicable to its type:

- a message/type identifier;
- protocol/data-format version identity;
- a monotonically interpretable sequence number or equivalent continuity identifier;
- timing and/or sample-rate information required to interpret the payload;
- the payload itself;
- measurement/data-validity and system-health flags relevant to that payload;
- an integrity check appropriate to the selected framing/encoding.

Sequence information shall allow the receiving PC/controller to detect missing or discontinuous transmitted data rather than silently assuming message continuity.

The application data model shall remain conceptually separable from its physical transport so that future interfaces can carry equivalent logical information through another appropriate link, for example:

`application data model → USB / future RS-485 / future CAN`

This does not require Rev-1 to implement all of those transports. USB remains the accepted Rev-1 interface under COM-001.

Exact binary/text encoding, field widths, byte order, framing markers, CRC/checksum algorithm, command set and host parser implementation are deferred to Stage B. They shall be selected consistently with measured throughput, debugging needs and the chosen transport while preserving the product-level requirements above.

### Rationale

Versioning prevents later format changes from being interpreted incorrectly, sequence information exposes communication loss, and explicit validity information preserves the measurement-pipeline trust model across the PC interface. Keeping the logical data model independent of USB also supports future industrial communication without prematurely implementing an industrial protocol in Rev-1.

## Phase 9 design status

COM-001 through COM-003 define the Rev-1 product-level communication architecture:

`validated measurement/diagnostic products → telemetry or waveform-capture messages → USB serial → PC/MATLAB`

The logical message model remains transport-independent so future industrial communication can be added without redefining the measurement and diagnostic data products.

## Verification handoff

Implementation/verification shall demonstrate that:

- communication workload does not disturb deterministic 100 kS/s acquisition;
- normal telemetry conveys the selected measurement, diagnostic and health information correctly;
- requested waveform captures preserve sample ordering, timing identity and validity information;
- missing/discontinuous messages or captured data can be detected rather than silently accepted;
- the PC/MATLAB side can identify the data-format version and reject or handle incompatible data appropriately;
- integrity errors in framed communication are detectable by the selected implementation mechanism.

## Planned output

Phase 9 closes with a communication architecture that supports practical Rev-1 logging/analysis while preserving deterministic acquisition and leaving a clean path toward later industrial interfaces.
