"""Reproduce the 2026-09-14 CSV integrity check; no gain is accepted.

Run from any directory with Python, NumPy, SciPy, and Matplotlib installed.
Raw files are read unchanged from ../../raw/2026-09-14/.
The largest CH1 step defines diagnostic intervals, not cleaned evidence.
"""
from pathlib import Path
import csv
import hashlib
import json
import re

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent
RAW = HERE.parent.parent / 'raw' / '2026-09-14'
NAMES = ['data_27_000_CH1_avg100Hz_2pp.csv',
         'data_27_001_CH2_avg100Hz_2pp.csv']

def read_record(name):
    raw = (RAW / name).read_bytes()
    lines = raw.decode('utf-8').splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith('index,'))
    header = {row[0].strip(' :'): row[1].strip()
              for row in csv.reader(lines[:start]) if len(row) == 2}
    step = re.fullmatch(r'([\d.]+)us', header['Time interval'])
    if step is None:
        raise ValueError('Expected time interval in microseconds')
    data = np.loadtxt(lines[start + 1:], delimiter=',')
    if not np.all(np.isfinite(data)):
        raise ValueError('Nonfinite data')
    if not np.array_equal(data[:, 0], np.arange(1, len(data) + 1)):
        raise ValueError('Nonconsecutive sample indices')
    dt = float(step.group(1)) * 1e-6
    t = np.arange(len(data)) * dt
    y = data[:, 1]  # Exported mV; do not infer physical DC from its mean.
    summary = dict(name=name, sha256=hashlib.sha256(raw).hexdigest(),
                   count=len(y), interval_s=dt, span_s=float(t[-1]),
                   header=header, exported_mean_mV=float(y.mean()),
                   raw_vpp_mV=float(np.ptp(y)),
                   smallest_level_step_mV=float(np.diff(np.unique(y)).min()))
    return t, y, summary

def fit(t, y, f):
    design = np.column_stack([np.ones(len(t)), np.sin(2*np.pi*f*t),
                              np.cos(2*np.pi*f*t)])
    coef = np.linalg.lstsq(design, y, rcond=None)[0]
    predicted = design @ coef
    residual = y - predicted
    info = dict(frequency_Hz=float(f), vpp_mV=float(2*np.hypot(*coef[1:])),
                residual_rms_mV=float(np.sqrt(np.mean(residual**2))),
                R2=float(1-np.sum(residual**2)/np.sum((y-y.mean())**2)),
                phase_deg=float(np.degrees(np.arctan2(coef[2], coef[1]))))
    return predicted, info

def best_frequency(t, y):
    grid = np.linspace(95, 105, 101)
    error = [np.mean((y-fit(t, y, f)[0])**2) for f in grid]
    center = grid[int(np.argmin(error))]
    result = minimize_scalar(lambda f: np.mean((y-fit(t, y, f)[0])**2),
                             bounds=(center-.1, center+.1), method='bounded',
                             options={'xatol': 1e-10})
    return float(result.x)

records = [read_record(name) for name in NAMES]
t, y1, meta1 = records[0]
t2, y2, meta2 = records[1]
if not np.array_equal(t, t2):
    raise ValueError('Different exported time axes')
cut = int(np.argmax(np.abs(np.diff(y1)))) + 1
regions = {}
for label, sl in [('full', slice(None)), ('before_jump', slice(0, cut)),
                  ('after_jump', slice(cut, None))]:
    f = best_frequency(t[sl], y1[sl])
    regions[label] = dict(CH1_free=fit(t[sl], y1[sl], f)[1],
                          CH1_at_100Hz=fit(t[sl], y1[sl], 100)[1],
                          CH2_at_100Hz=fit(t[sl], y2[sl], 100)[1])
result = dict(files=[meta1, meta2],
              jump=dict(from_index=cut, to_index=cut+1,
                        time_s=float(t[cut]), from_mV=float(y1[cut-1]),
                        to_mV=float(y1[cut]), step_mV=float(y1[cut]-y1[cut-1])),
              regions=regions, accepted_gain=None,
              limitation='CH1 phase discontinuity prevents a stationary whole-record gain measurement; diagnostic intervals are not accepted calibration data.')
(HERE/'metrics.json').write_text(json.dumps(result, indent=2)+'\n')

plt.rcParams.update({'font.size': 11, 'svg.fonttype': 'none', 'svg.hashsalt': 'avg100hz'})
fig, axes = plt.subplots(2, 1, figsize=(10, 6.3), layout='constrained')
fig.suptitle('CH1: the exported record contains a discontinuity', fontsize=15)
axes[0].plot(t[::4]*1000, y1[::4], color='#155e75', linewidth=1)
axes[0].axvline(t[cut]*1000, color='#b91c1c', linestyle='--', linewidth=1)
axes[0].set(title='Full 0.2 s record (displayed every fourth point)',
            xlabel='Time from first exported sample (ms)', ylabel='Exported CH1 (mV)')
axes[0].annotate(f'168 mV step at {t[cut]*1000:.2f} ms',
                 xy=(t[cut]*1000, 245), xytext=(115, 305),
                 color='#b91c1c', arrowprops=dict(arrowstyle='->',color='#b91c1c'))
axes[0].set_ylim(-285, 345)
mask = (t >= t[cut]-.002) & (t <= t[cut]+.002)
axes[1].plot(t[mask]*1000, y1[mask], '.-', color='#155e75', markersize=3,
             linewidth=.8, label='Every exported point')
axes[1].plot(t[cut-1:cut+1]*1000, y1[cut-1:cut+1], 'o-', color='#b91c1c',
             linewidth=2, markersize=5)
axes[1].set(title='Detail: sample 8520 → 8521, −104 → +64 mV',
            xlabel='Time from first exported sample (ms)', ylabel='Exported CH1 (mV)')
for ax in axes:
    ax.grid(alpha=.2)
    ax.spines[['right','top']].set_visible(False)
fig.savefig(HERE/'ch1-discontinuity.svg', metadata={'Date': None})
fig.savefig(HERE/'ch1-discontinuity-preview.png', dpi=130)
print(json.dumps(result, indent=2))
