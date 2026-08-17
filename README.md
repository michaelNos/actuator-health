# Actuator Health Monitoring System

Engineering development repository for a laboratory-scale actuator condition-monitoring system based initially on current measurement and waveform analysis of a low-voltage DC actuator.

Rev-1 is developed **design-first**: the product is specified and baselined at system and subsystem level before physical implementation begins. Implementation and verification then follow the approved engineering documentation rather than completing the design ad hoc on the bench.

## Project documentation

| Phase | Document | Status |
|---|---|---|
| 1 | [System Requirements](docs/01-system-requirements.md) | Complete / baselined |
| 2 | [System Architecture](docs/02-system-architecture.md) | Complete / baselined |
| 3 | [ACS724 Sensor Design and Verification Plan](docs/03-acs724-sensor-characterization.md) | Design complete / ready for review |

See the [documentation index](docs/README.md) for the authoritative documentation convention, design-before-implementation rule, and planned Rev-1 development stages.

## Development workflow

One engineering phase is developed on one branch and one pull request. The PR remains draft while design decisions are being developed and becomes ready for review when that phase's **design baseline and planned verification method** are complete.

Only explicitly approved engineering decisions are baselined. Values that legitimately depend on future hardware, calibration, or measurements remain `TBD` during design rather than being invented.

After the complete Rev-1 design is baselined, implementation shall proceed from the documented design. Verification then executes the planned tests, records evidence, and identifies any required deviation or redesign.

## Safety scope

Rev-1 is a low-voltage laboratory prototype. Hobby development hardware, breadboards, the Pololu ACS724 carrier, and ordinary oscilloscope probes are not to be connected directly to industrial 400 V three-phase circuits. Future industrial scaling requires appropriately rated isolated sensing and industrial installation practices.
