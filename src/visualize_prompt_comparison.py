"""
Prompt-variant comparison: standard vs emphasis.

Figures:
  fig6a_prompt_delta_heatmap.png  — heatmap of AMCE difference (Emphasis − standard) per model × factor
  fig6b_prompt_forest.png         — side-by-side forest plot for each model with both variants

Run: uv run python src/visualize_prompt_comparison.py
"""

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')
FIG_DIR  = Path('figures')
DATA_DIR = Path('data')
FIG_DIR.mkdir(exist_ok=True)

MODEL_STYLE = {
    'claude-opus-4-7':  {'color': '#c96442', 'label': 'Claude Opus 4.7'},
    'gpt-5.5':          {'color': '#10a37f', 'label': 'GPT-5.5'},
    'gemini-3-pro':     {'color': '#4285f4', 'label': 'Gemini 3 Pro'},
    'mistral-large-3':  {'color': '#ff7000', 'label': 'Mistral Large 3'},
    'grok-4.1':         {'color': '#9b59b6', 'label': 'Grok 4.1'},
    'deepseek-v4-pro':  {'color': '#e91e63', 'label': 'DeepSeek v4 Pro'},
}

FACTOR_SHORT = {
    '[Omission -> Commission]':       'Intervention',
    '[Passengers -> Pedestrians]':    'Relation to AV',
    'Law [Illegal -> Legal]':         'Legality',
    'Gender [Male -> Female]':        'Gender',
    'Fitness [Large -> Fit]':         'Fitness',
    'Social Status [Low -> High]':    'Social Status',
    'Age [Elderly -> Young]':         'Age',
    'No. Characters [Less -> More]':  'No. of Lives',
    'Species [Pets -> Humans]':       'Species',
}

# ── Load both variants ─────────────────────────────────────────────────────────

std_path = DATA_DIR / 'amce_all_models_standard.csv'
emphasis_path = DATA_DIR / 'amce_all_models_emphasis.csv'

if not std_path.exists():
    raise FileNotFoundError('Run: uv run python src/analysis.py first')
if not emphasis_path.exists():
    raise FileNotFoundError('Run: uv run python src/analysis.py --variant emphasis first')

std = pd.read_csv(std_path)
emphasis = pd.read_csv(emphasis_path)

# Only keep models present in both variants (exclude human baseline for delta)
std_models = set(std[std['model'] != 'Human (global avg)']['model'].unique())
emphasis_models = set(emphasis['model'].unique())
common_models = sorted(std_models & emphasis_models, key=lambda m: list(MODEL_STYLE).index(m) if m in MODEL_STYLE else 99)

if not common_models:
    raise ValueError('No models have both standard and Emphasis data yet.')

print(f'Models with both variants: {common_models}')

factors = list(FACTOR_SHORT.keys())
factor_labels = [FACTOR_SHORT[f] for f in factors]

# ── Fig 6a: Delta heatmap (Emphasis − standard) ────────────────────────────────────

delta_matrix = np.full((len(common_models), len(factors)), np.nan)

for mi, model in enumerate(common_models):
    std_sub = std[std['model'] == model].set_index('factor')
    emphasis_sub = emphasis[emphasis['model'] == model].set_index('factor')
    for fi, factor in enumerate(factors):
        if factor in std_sub.index and factor in emphasis_sub.index:
            delta_matrix[mi, fi] = emphasis_sub.loc[factor, 'estimate'] - std_sub.loc[factor, 'estimate']

model_labels = [MODEL_STYLE.get(m, {}).get('label', m) for m in common_models]

fig, ax = plt.subplots(figsize=(12, max(3, len(common_models) * 1.1 + 1.5)))
vmax = 2.0

im = ax.imshow(delta_matrix, cmap='RdBu_r', vmin=-vmax, vmax=vmax, aspect='auto')

ax.set_xticks(range(len(factors)))
ax.set_xticklabels(factor_labels, rotation=30, ha='right', fontsize=10)
ax.set_yticks(range(len(common_models)))
ax.set_yticklabels(model_labels, fontsize=11)

# Annotate cells
for mi in range(len(common_models)):
    for fi in range(len(factors)):
        val = delta_matrix[mi, fi]
        if not np.isnan(val):
            ax.text(fi, mi, f'{val:+.2f}', ha='center', va='center',
                    fontsize=8, color='white' if abs(val) > vmax * 0.5 else 'black')

plt.colorbar(im, ax=ax, label='AMCE delta (Emphasis − standard)', shrink=0.8)
ax.set_title('Effect of emphasis prompting on moral preferences')
fig.tight_layout()
fig.savefig(FIG_DIR / 'fig6a_prompt_delta_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved fig6a_prompt_delta_heatmap.png')


# ── Fig 6b: Side-by-side forest plot per model ────────────────────────────────

n_models = len(common_models)
fig, axes = plt.subplots(1, n_models, figsize=(5 * n_models, 8), sharey=True)
if n_models == 1:
    axes = [axes]

for ax, model in zip(axes, common_models):
    style = MODEL_STYLE.get(model, {'color': '#888', 'label': model})
    std_sub = std[std['model'] == model].set_index('factor')
    emphasis_sub = emphasis[emphasis['model'] == model].set_index('factor')

    for fi, factor in enumerate(factors):
        y_standard = fi + 0.15
        y_emphasis = fi - 0.15

        if factor in std_sub.index:
            row = std_sub.loc[factor]
            ax.plot([row['ci_lo'], row['ci_hi']], [y_standard, y_standard],
                    color=style['color'], linewidth=1.5, alpha=0.5)
            ax.plot(row['estimate'], y_standard, 'o', color=style['color'],
                    markersize=7, zorder=3, label='standard' if fi == 0 else '')

        if factor in emphasis_sub.index:
            row = emphasis_sub.loc[factor]
            ax.plot([row['ci_lo'], row['ci_hi']], [y_emphasis, y_emphasis],
                    color=style['color'], linewidth=1.5, alpha=0.5, linestyle='--')
            ax.plot(row['estimate'], y_emphasis, 's', color=style['color'],
                    markersize=7, zorder=3, markerfacecolor='white',
                    markeredgewidth=1.5, label='Emphasis' if fi == 0 else '')

    ax.axvline(0, color='black', linewidth=0.8, linestyle=':', alpha=0.5)
    ax.set_title(style['label'], fontsize=11, fontweight='bold', color=style['color'])
    ax.set_xlabel('AMCE', fontsize=10)
    ax.set_xlim(-0.8, 1.2)

    for fi in range(len(factors)):
        if fi % 2 == 0:
            ax.axhspan(fi - 0.5, fi + 0.5, color='#f5f5f5', zorder=0)

    legend_handles = [
        plt.Line2D([0], [0], marker='o', color=style['color'], markersize=7,
                   linewidth=1.5, label='Standard'),
        plt.Line2D([0], [0], marker='s', color=style['color'], markersize=7,
                   linewidth=1.5, linestyle='--', markerfacecolor='white',
                   markeredgewidth=1.5, label='Emphasis'),
    ]
    ax.legend(handles=legend_handles, fontsize=8, loc='lower right')
    sns.despine(ax=ax)

axes[0].set_yticks(range(len(factors)))
axes[0].set_yticklabels(factor_labels, fontsize=10)
axes[0].set_ylim(-0.7, len(factors) - 0.3)

fig.suptitle('Standard vs. emphasis prompting', y=1.01)
fig.tight_layout()
fig.savefig(FIG_DIR / 'fig6b_prompt_forest.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved fig6b_prompt_forest.png')
