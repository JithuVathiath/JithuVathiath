#!/usr/bin/env python3
"""Redraw the public aggregate results; never reads participant-level data.

Source: human-ai-loan-collaboration-analysis/README.md#headline-findings
Retrieved 2026-10-29. Chart generation requires matplotlib.
"""
import os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', '/tmp/jithu-profile-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'path'})
fig, ax = plt.subplots(figsize=(8, 3.5), facecolor='#F1F6FC')
ax.set_facecolor('#F1F6FC')
labels = ['Initial human', 'AI recommendation', 'Final human–AI']
values = [65.42, 60.73, 66.61]
colors = ['#647F9D', '#2695BE', '#2563EB']
ax.barh([2, 1, 0], values, height=.5, color=colors)
for y, value in zip([2, 1, 0], values):
    ax.text(value+2, y, f'{value:.2f}%', va='center', fontsize=17, weight='bold', color='#142D4E')
ax.set_yticks([2, 1, 0], labels, fontsize=15, color='#142D4E')
ax.set_xlim(0, 100)
ax.set_xticks([0, 25, 50, 75, 100], ['0%', '25%', '50%', '75%', '100%'], fontsize=12, color='#496480')
ax.set_axisbelow(True)
ax.grid(axis='x', color='#D3DFEF', linewidth=.8)
ax.tick_params(axis='both', length=0, pad=10)
for spine in ax.spines.values():
    spine.set_visible(False)
fig.suptitle('Accuracy across decision stages', x=.035, ha='left', fontsize=20, weight='bold', color='#142D4E')
fig.text(.035, .035, 'Reported study results · small, uncertain gain over initial judgement', fontsize=12, color='#496480')
fig.subplots_adjust(left=.31, right=.96, top=.78, bottom=.2)
fig.savefig(ROOT/'assets/research/accuracy-comparison.svg', metadata={'Title':'Human–AI decision accuracy', 'Description':'Reported aggregate accuracy: initial human 65.42%; AI recommendation 60.73%; final human–AI 66.61%. The gain over initial judgement is small and uncertain.', 'Date':None})
fig.savefig(ROOT/'assets/research/accuracy-comparison.png', dpi=160)
