# Raw DOS1102S evidence inventory — 2026-09-07

Original files captured during the ACS724 USB-export and motor-spectrum experiment:

## Native screenshots
- `bmp_20_002.bmp`
- `bmp_20_003.bmp`
- `bmp_20_004.bmp`

## Native BIN exports
- `data_20_001.bin`
- `data_20_002.bin`
- `data_20_003.bin`
- `data_20_004.bin`
- `data_20_005.bin`

## CSV exports
- `data_20_006.csv` — first CSV; invalid voltage scaling because scope metadata was 10X while physical probe was 1X
- `data_20_007.csv` — corrected 1X exploratory capture; motor state unknown
- `data_20_008.csv` — corrected 1X exploratory capture; motor state unknown
- `data_20_009off.csv` — controlled motor OFF
- `data_20_010on.csv` — controlled motor ON
- `data_20_011off.csv` — repeatability sequence OFF
- `data_20_012on.csv` — repeatability sequence ON
- `data_20_013off.csv` — repeatability sequence OFF
- `data_20_014on.csv` — repeatability sequence ON
- `data_20_015-4v.csv` — motor ON, 4 V, PSU 34 mA / 0.135 W
- `data_20_016-5v.csv` — motor ON, 5 V, PSU 35 mA / 0.175 W
- `data_20_017-6v.csv` — motor ON, 6 V, PSU 36 mA / 0.216 W

005 = A1 OUT, bench
006 = B1 OUT, Arduino
007 = A2 OUT, bench
008 = A1 VCC, bench
009 = B1 VCC, Arduino
010 = A2 VCC, bench
011 = VCC, bandwidth limit OFF
012 = VCC, limit OFF
013 = VCC, 20 MHz limit ON
014 = VCC, limit OFF
015 = OUT, limit 20MHz
016 = OUT, limit 20MHz
017 = OUT, limit 20MHz

The exact original files were also bundled during the documentation session as `acs724_scope_raw_2026-09-07.zip`. Binary/raw file bytes are intentionally not reconstructed from screenshots or derived analysis.

See `docs/evidence/acs724-raw-waveform-and-speed-dependent-spectrum-2026-09-07.md` for validity classification and results, and `analysis/acs724_raw_csv_fft.py` for the reproducible CSV analysis method.
