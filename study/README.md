# Study Notes

This directory is the learning notebook for the Actuator Health Monitoring System project.

It is intentionally separate from `docs/`, which remains the authoritative professional engineering record.

## LEARN-001 — Separation of engineering baseline and study notes

**Status:** Accepted

Purchased devices, ICs, relevant modules, and laboratory instruments shall be studied as they become relevant to project development.

Broader educational material shall be maintained separately from the formal engineering phase documentation.

- `docs/` contains approved requirements, design decisions, calculations, tests, results, limitations, verification evidence, and next actions that belong to the engineering baseline.
- `study/` contains deeper device theory, operating principles, datasheet interpretation, terminology, practical lessons, experiments for learning, and Anki-style review material.

Knowledge from `study/` shall enter the formal engineering documentation only when it becomes relevant to an accepted project decision, calculation, test, result, or limitation.

Study notes are therefore educational support material and are not themselves an engineering approval mechanism.

## Study workflow

When a device becomes relevant to the project, study it before relying on it in the design:

`Identify → Read primary documentation → Understand operating principle → Understand important limits/parameters → Perform useful learning experiments → Apply relevant knowledge to the engineering design`

Important terminology may be captured in compact Anki-style form:

**Front:** What is the term or engineering question?  
**Back:** Concise technically correct explanation.

Unknown values remain unknown until verified from primary documentation, calculated, or measured.

## Initial study queue

The current project hardware provides the initial learning queue. Notes should be added when each item becomes relevant rather than attempting to study everything at once.

- Allegro ACS724 / Pololu #4048 current-sensor carrier
- Arduino UNO R4 WiFi
- Renesas RA4M1 microcontroller
- MCP6022 operational amplifier
- MAX485 RS-485 modules
- MCP2551 CAN transceiver modules
- HANMATEK DOS1102S oscilloscope and function generator
- Jesverty SPS-3010V bench power supply
- relevant passive components, protection parts, wiring, connectors, and measurement techniques as they enter the design

## Relationship to engineering phases

The engineering phase workflow does not change because of this directory.

A study note may contain explanations, examples, or experiments that are useful for learning but are not yet accepted project decisions. Formal phase documents continue to baseline only explicitly approved engineering work.
