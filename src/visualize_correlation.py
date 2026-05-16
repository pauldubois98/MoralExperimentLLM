"""
Correlation between moral preference strength (|AMCE|) and response length.

Figures:
  fig8_amce_length_correlation.png  — per-model Spearman r bar chart + scatter

Run: uv run python src/visualize_correlation.py
"""

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats

warnings.filterwarnings('ignore')
FIG_DIR  = Path('figures')
DATA_DIR = Path('data')
FIG_DIR.mkdir(exist_ok=True)

MODEL_STYLE = {
    'claude-opus-4-7':  {'color': '#c96442', 'label': 'Claude Opus 4.7'},
    'gpt-5.5':          {'color': '#10a37f', 'label': 'GPT-5.5'},
    'gemini-3-pro':     {'color': '#4285f4', 'label': 'Gemini 3 Pro*'},
    'mistral-large-3':  {'color': '#ff7000', 'label': 'Mistral Large 3'},
    'grok-4.1':         {'color': '#9b59b6', 'label': 'Grok 4.1'},
    'deepseek-v4-pro':  {'color': '#e91e63', 'label': 'DeepSeek v4 Pro'},
    'llama-4-maverick': {'color': '#607d8b', 'label': 'Llama 4 Maverick'},
}

FACTOR_SHORT = {
    '[Omission -> Commission]':      'Intervention',
    '[Passengers -> Pedestrians]':   'Relation to AV',
    'Law [Illegal -> Legal]':        'Legality',
    'Gender [Male -> Female]':       'Gender',
    'Fitness [Large -> Fit]':        'Fitness',
    'Social Status [Low -> High]':   'Social Status',
    'Age [Elderly -> Young]':        'Age',
    'No. Characters [Less -> More]': 'No. of Lives',
    'Species [Pets -> Humans]':      'Species',
}

DIM_FILTERS = {
    'Intervention':   lambda df: df,
    'Relation to AV': lambda df: df[df['PedPed'] == 0],
    'Legality':       lambda df: df[(df['PedPed'] == 1) & (df['CrossingSignal'].isin([1, 2]))],
    'Gender':         lambda df: df[df['ScenarioTypeStrict'] == 'Gender'],
    'Fitness':        lambda df: df[df['ScenarioTypeStrict'] == 'Fitness'],
    'Social Status':  lambda df: df[df['ScenarioTypeStrict'] == 'SocialStatus'],
    'Age':            lambda df: df[df['ScenarioTypeStrict'] == 'Age'],
    'No. of Lives':   lambda df: df[df['ScenarioTypeStrict'] == 'Utilitarian'],
    'Species':        lambda df: df[df['ScenarioTypeStrict'] == 'Species'],
}

# ── Load AMCE (averaged across variants) ─────────────────────────────────────

amce_std = pd.read_csv(DATA_DIR / 'amce_all_models_standard.csv')
emphasis_path = DATA_DIR / 'amce_all_models_emphasis.csv'
if emphasis_path.exists():
    amce_all = pd.concat([amce_std, pd.read_csv(emphasis_path)], ignore_index=True)
    amce = amce_all.groupby(['model', 'factor'], as_index=False)[['estimate']].mean()
else:
    amce = amce_std
amce['dim'] = amce['factor'].map(FACTOR_SHORT)

# ── Load response files (Intervention==0 rows, both variants) ─────────────────

rows = []
for model_key, style in MODEL_STYLE.items():
    dfs = []
    for variant in ('standard', 'emphasis'):
        path = DATA_DIR / f'responses_{model_key}_{variant}.csv'
        if path.exists():
            df = pd.read_csv(path)
            dfs.append(df[df['Intervention'] == 0])
    if not dfs:
        continue
    df = pd.concat(dfs, ignore_index=True)
    for dim, filt in DIM_FILTERS.items():
        tok = filt(df)['OutputTokens'].dropna().median()
        sub = amce[(amce['model'] == model_key) & (amce['dim'] == dim)]
        if len(sub) == 0:
            continue
        rows.append({
            'model_key':   model_key,
            'model_label': style['label'],
            'color':       style['color'],
            'dim':         dim,
            'tokens':      tok,
            'abs_amce':    abs(sub['estimate'].iloc[0]),
        })

corr_df = pd.DataFrame(rows).dropna()

# ── Compute per-model correlations ────────────────────────────────────────────

results = []
for model_key, style in MODEL_STYLE.items():
    sub = corr_df[corr_df['model_key'] == model_key]
    if len(sub) < 3:
        continue
    r, p = stats.spearmanr(sub['abs_amce'], sub['tokens'])
    results.append({
        'model_key':   model_key,
        'model_label': style['label'],
        'color':       style['color'],
        'r':           r,
        'p':           p,
        'sig':         p < 0.05,
    })
    print(f'{style["label"]:22s}  r={r:+.3f}  p={p:.3f}{"  *" if p < 0.05 else ""}')

res_df = pd.DataFrame(results).sort_values('r')

pooled_r, pooled_p = stats.spearmanr(corr_df['abs_amce'], corr_df['tokens'])
print(f'\nPooled  r={pooled_r:+.3f}  p={pooled_p:.4f}  N={len(corr_df)}')

# ── Fig 8: two-panel figure ───────────────────────────────────────────────────

fig, (ax_bar, ax_scat) = plt.subplots(1, 2, figsize=(13, 5))

# Left panel: bar chart of Spearman r per model
bar_colors = [('#888888' if not row['sig'] else row['color']) for _, row in res_df.iterrows()]
bars = ax_bar.barh(res_df['model_label'], res_df['r'], color=bar_colors, alpha=0.85, height=0.55)
ax_bar.axvline(0, color='black', linewidth=1)
ax_bar.set_xlabel('Spearman r  (|AMCE| vs. median tokens)', fontsize=11)
ax_bar.set_title('Preference strength vs. response length', fontsize=11, fontweight='bold')
ax_bar.set_xlim(-1.1, 0.4)
for bar, (_, row) in zip(bars, res_df.iterrows()):
    x = row['r'] - 0.03 if row['r'] < 0 else row['r'] + 0.03
    ha = 'right' if row['r'] < 0 else 'left'
    label = f"{row['r']:+.2f}{'*' if row['sig'] else ''}"
    ax_bar.text(x, bar.get_y() + bar.get_height() / 2,
                label, va='center', ha=ha, fontsize=9, fontweight='bold',
                color=row['color'] if row['sig'] else '#555555')
sig_patch   = mpatches.Patch(color='#555555', label='p ≥ 0.05 (n.s.)')
insig_patch = mpatches.Patch(color='#aaaaaa', label='p < 0.05')
sns.despine(ax=ax_bar)

# Right panel: scatter + per-model fit lines
for model_key, style in MODEL_STYLE.items():
    sub = corr_df[corr_df['model_key'] == model_key]
    if len(sub) < 2:
        continue
    r_val = res_df.loc[res_df['model_key'] == model_key, 'r'].values
    r_str = f' (r={r_val[0]:+.2f})' if len(r_val) else ''
    ax_scat.scatter(sub['abs_amce'], sub['tokens'],
                    color=style['color'], s=60, alpha=0.75, zorder=3)
    m, b = np.polyfit(sub['abs_amce'], sub['tokens'], 1)
    xr = np.linspace(sub['abs_amce'].min(), sub['abs_amce'].max(), 100)
    ax_scat.plot(xr, m * xr + b, color=style['color'], linewidth=1.4,
                 linestyle='--', alpha=0.7, label=style['label'] + r_str)

ax_scat.set_xlabel('|AMCE|  (preference strength)', fontsize=11)
ax_scat.set_ylabel('Median output tokens', fontsize=11)
ax_scat.set_title('Preference strength vs. response length\n(per-model fit lines)', fontsize=11, fontweight='bold')
ax_scat.legend(fontsize=8, loc='upper right', framealpha=0.9)
sns.despine(ax=ax_scat)

fig.tight_layout()
fig.savefig(FIG_DIR / 'fig8_amce_length_correlation.png', dpi=150, bbox_inches='tight')
plt.close()
print('\nSaved fig8_amce_length_correlation.png')
