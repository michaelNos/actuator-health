# MCP6022 Rev-1 AFE DC bring-up — 2026-09-30

**Project:** Actuator Health Monitoring System  
**Stage:** Stage B — independent AFE bring-up  
**Status:** Initial DC continuity/supply/unity-path check completed

## Purpose

Validate the newly built Rev-1 MCP6022 analog front end at DC before applying an AC stimulus.

## Measured supply

Measured directly across the MCP6022 supply pins:

- pin 8 (VDD) relative to pin 4 (VSS): **4.92 V**

Result: **PASS** for the present 5 V measurement-domain bring-up check.

## DC signal-path measurements

Observed DC voltages:

- `TP_SENSOR`: **0.49 V**
- MCP6022 pin 3 (+IN A): **0.48 V**
- MCP6022 pin 1 / OUTA: **0.49 V**
- MCP6022 pin 5 (+IN B): **0.49 V**
- MCP6022 pin 7 / TP_AFE: **0.49 V**
- `ADC_IN`: **0.49 V**

Interpretation:

The two unity-gain Sallen-Key sections pass the present DC level essentially unchanged through the complete AFE path. The approximately 10 mV difference observed at pin 3 is not assigned to a specific cause from this one measurement.

No AC transfer conclusion is made from this test.

## Continuity note

The user reported continuity checks as beeping. Because the AFE includes supply capacitors across `5V_MEAS` and `GND_MEAS`, a continuity meter may beep transiently while charging those capacitors. A sustained low-resistance short between the supply rails would be a fault; the powered 4.92 V measurement is consistent with the rails not being hard-shorted.

## Next step

Perform independent low-frequency AC validation with a known AFG stimulus, ensuring only one active source drives `TP_SENSOR` at a time.
