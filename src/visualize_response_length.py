"""
Response length analysis across LLMs.

Figures:
  fig7a_token_distribution.png  — violin + box plot of output token counts per model
  fig7b_length_by_choice.png    — token count split by STAY vs SWERVE choice
  fig7c_length_by_factor.png    — median token count per scenario type (factor)
  fig7d_latency.png             — latency distribution per model

Run: uv run python src/visualize_response_length.py
"""

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
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
    'llama-4-maverick': {'color': '#607d8b', 'label': 'Llama 4 Maverick'},
}

FACTOR_LABELS = {
    'Gender':      'Gender',
    'Fitness':     'Fitness',
    'SocialStatus':'Social Status',
    'Age':         'Age',
    'Utilitarian': 'No. of Lives',
    'Species':     'Species',
    'Random':      'Random',
}

# ── Load all response files (standard + CoT combined) ─────────────────────────

dfs = []
for model, style in MODEL_STYLE.items():
    for variant in ('standard', 'cot'):
        path = DATA_DIR / f'responses_{model}_{variant}.csv'
        if not path.exists():
            continue
        df = pd.read_csv(path)
        # Keep one row per scenario (Intervention==0) to avoid double-counting
        df = df[df['Intervention'] == 0].copy()
        df = df[df['OutputTokens'].notna() & (df['OutputTokens'] > 0)]
        df['model_label'] = style['label']
        df['model_key']   = model
        df['color']       = style['color']
        df['char_count']  = df['LLMReasoning'].fillna('').str.len()
        dfs.append(df)

if not dfs:
    raise FileNotFoundError('No response files found.')

all_df = pd.concat(dfs, ignore_index=True)

model_order  = [MODEL_STYLE[m]['label'] for m in MODEL_STYLE if m in all_df['model_key'].unique()]
model_colors = [MODEL_STYLE[m]['color'] for m in MODEL_STYLE if m in all_df['model_key'].unique()]

# ── Fig 7a: Token distribution (violin + box) ─────────────────────────────────

fig, ax = plt.subplots(figsize=(12, 6))

data_by_model = [all_df[all_df['model_label'] == m]['OutputTokens'].dropna().values
                 for m in model_order]

parts = ax.violinplot(data_by_model, positions=range(len(model_order)),
                      showmedians=False, showextrema=False, widths=0.7)
for pc, color in zip(parts['bodies'], model_colors):
    pc.set_facecolor(color)
    pc.set_alpha(0.4)

bp = ax.boxplot(data_by_model, positions=range(len(model_order)),
                widths=0.25, patch_artist=True,
                medianprops=dict(color='black', linewidth=2),
                whiskerprops=dict(linewidth=1.2),
                capprops=dict(linewidth=1.2),
                flierprops=dict(marker='.', markersize=2, alpha=0.3))
for patch, color in zip(bp['boxes'], model_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Annotate with median + mean
for i, (m, data) in enumerate(zip(model_order, data_by_model)):
    median = np.median(data)
    mean   = np.mean(data)
    ax.text(i, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else max(d.max() for d in data_by_model if len(d)),
            f'med={median:.0f}\nmean={mean:.0f}',
            ha='center', va='bottom', fontsize=7.5, color='#333')

ax.set_xticks(range(len(model_order)))
ax.set_xticklabels(model_order, fontsize=11)
ax.set_ylabel('Output tokens', fontsize=12)
ax.set_title('Response length distribution by model\n(standard + CoT combined)',
             fontsize=13, fontweight='bold')
ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
sns.despine(ax=ax)
fig.tight_layout()
fig.savefig(FIG_DIR / 'fig7a_token_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved fig7a_token_distribution.png')


# ── Fig 7b: Token count by choice (STAY vs SWERVE) ───────────────────────────

fig, axes = plt.subplots(1, len(model_order), figsize=(3.2 * len(model_order), 5), sharey=False)
if len(model_order) == 1:
    axes = [axes]

for ax, model_label in zip(axes, model_order):
    sub = all_df[all_df['model_label'] == model_label]
    color = sub['color'].iloc[0]

    stay   = sub[sub['LLMChoice'] == 'STAY']['OutputTokens'].dropna()
    swerve = sub[sub['LLMChoice'] == 'SWERVE']['OutputTokens'].dropna()

    data   = [stay.values, swerve.values]
    labels = ['STAY', 'SWERVE']
    colors = [color, '#aaaaaa']

    bp = ax.boxplot(data, patch_artist=True, widths=0.5,
                    medianprops=dict(color='black', linewidth=2),
                    flierprops=dict(marker='.', markersize=2, alpha=0.3))
    for patch, c in zip(bp['boxes'], colors):
        patch.set_facecolor(c)
        patch.set_alpha(0.75)

    for i, (d, lbl) in enumerate(zip(data, labels), 1):
        ax.text(i, ax.get_ylim()[1] if ax.get_ylim()[1] > 1 else max(max(stay) if len(stay) else 0, max(swerve) if len(swerve) else 0),
                f'n={len(d)}\nmed={np.median(d):.0f}',
                ha='center', va='bottom', fontsize=8)

    ax.set_xticklabels(labels, fontsize=11)
    ax.set_title(model_label, fontsize=10, fontweight='bold', color=color)
    ax.set_ylabel('Output tokens' if ax == axes[0] else '', fontsize=10)
    sns.despine(ax=ax)

fig.suptitle('Response length by choice (STAY vs SWERVE)',
             fontsize=13, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(FIG_DIR / 'fig7b_length_by_choice.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved fig7b_length_by_choice.png')


# ── Fig 7c: Median token count per scenario type ─────────────────────────────

scenario_col = 'ScenarioType'
if scenario_col not in all_df.columns:
    scenario_col = 'ScenarioTypeStrict'

scenario_types = [s for s in FACTOR_LABELS if s in all_df[scenario_col].unique()]
scenario_labels = [FACTOR_LABELS[s] for s in scenario_types]

medians = pd.DataFrame(index=model_order, columns=scenario_labels, dtype=float)
for model_label in model_order:
    sub = all_df[all_df['model_label'] == model_label]
    for stype, slabel in zip(scenario_types, scenario_labels):
        vals = sub[sub[scenario_col] == stype]['OutputTokens'].dropna()
        medians.loc[model_label, slabel] = vals.median() if len(vals) else np.nan

fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(len(scenario_labels))
width = 0.8 / len(model_order)

for i, (model_label, color) in enumerate(zip(model_order, model_colors)):
    vals = medians.loc[model_label].values.astype(float)
    offset = (i - len(model_order) / 2 + 0.5) * width
    bars = ax.bar(x + offset, vals, width=width * 0.9,
                  color=color, alpha=0.8, label=model_label)

ax.set_xticks(x)
ax.set_xticklabels(scenario_labels, fontsize=11)
ax.set_ylabel('Median output tokens', fontsize=12)
ax.set_title('Response length by scenario type', fontsize=13, fontweight='bold')
ax.legend(fontsize=9, loc='upper right', framealpha=0.9)
sns.despine(ax=ax)
fig.tight_layout()
fig.savefig(FIG_DIR / 'fig7c_length_by_factor.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved fig7c_length_by_factor.png')


# ── Fig 7d: Latency distribution ──────────────────────────────────────────────

lat_df = all_df[all_df['LatencyMs'] > 0].copy()
lat_df['LatencySec'] = lat_df['LatencyMs'] / 1000

fig, ax = plt.subplots(figsize=(12, 5))

for i, (model_label, color) in enumerate(zip(model_order, model_colors)):
    sub = lat_df[lat_df['model_label'] == model_label]['LatencySec'].dropna()
    if len(sub) == 0:
        continue
    ax.ecdf(sub, color=color, linewidth=2, label=f'{model_label} (med={sub.median():.1f}s)')

ax.set_xlabel('Latency (seconds)', fontsize=12)
ax.set_ylabel('Cumulative proportion', fontsize=12)
ax.set_title('Response latency CDF by model', fontsize=13, fontweight='bold')
ax.legend(fontsize=9, loc='lower right', framealpha=0.9)
ax.set_xlim(left=0)
ax.grid(axis='y', alpha=0.3)
sns.despine(ax=ax)
fig.tight_layout()
fig.savefig(FIG_DIR / 'fig7d_latency.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved fig7d_latency.png')

# ── Summary stats ─────────────────────────────────────────────────────────────
print('\nSummary (output tokens):')
print(all_df.groupby('model_label')['OutputTokens'].agg(['median','mean','std','min','max'])
      .round(1).to_string())
