# Actuator Health Monitoring System

Engineering development repository for a laboratory-scale actuator condition-monitoring system based initially on current measurement and waveform analysis of a low-voltage DC actuator.

The project is developed phase by phase. Accepted engineering decisions are documented in Markdown and merged through pull requests so Git history remains the durable project record.

## Project documentation

| Phase | Document | Status |
|---|---|---|
| 1 | [System Requirements](docs/01-system-requirements.md) | Complete / baselined |
| 2 | [System Architecture](docs/02-system-architecture.md) | Complete / baselined |
| 3 | ACS724 Sensor Theory and Characterization | Next |

See the [documentation index](docs/README.md) for the repository documentation convention and planned phases.

## Development workflow

One engineering phase is developed on one branch and one pull request. The PR stays draft while decisions are being discussed and becomes ready for review only after the phase is complete. Accepted decisions are committed as they are approved; implementation details that have not yet been derived or measured remain explicitly TBD.

## Safety scope

Rev-1 is a low-voltage laboratory prototype. Hobby development hardware, breadboards, the Pololu ACS724 carrier, and ordinary oscilloscope probes are not to be connected directly to industrial 400 V three-phase circuits. Future industrial scaling requires appropriately rated isolated sensing and industrial installation practices.
