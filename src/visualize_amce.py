"""
Phase 5 — AMCE visualisations comparing LLMs to human moral profiles.

Figures:
  fig5a_amce_forest.png   — forest plot: 9 AMCE factors × all models
  fig5b_pca_map.png       — PCA of 130-country moral profiles, LLMs overlaid
  fig5c_radar.png         — radar chart: LLMs vs human global average

Run: uv run python src/visualize_amce.py
"""

import tarfile, zipfile, warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import seaborn as sns

warnings.filterwarnings('ignore')
FIG_DIR  = Path('figures')
DATA_DIR = Path('data')
FIG_DIR.mkdir(exist_ok=True)

# ── Palette ───────────────────────────────────────────────────────────────────

MODEL_STYLE = {
    'claude-opus-4-7':  {'color': '#c96442', 'marker': 'o', 'label': 'Claude Opus 4.7'},
    'gpt-5.5':          {'color': '#10a37f', 'marker': 's', 'label': 'GPT-5.5'},
    'gemini-3-pro':     {'color': '#4285f4', 'marker': '^', 'label': 'Gemini 3 Pro*'},
    'mistral-large-3':  {'color': '#ff7000', 'marker': 'D', 'label': 'Mistral Large 3'},
    'grok-4.1':         {'color': '#9b59b6', 'marker': 'P', 'label': 'Grok 4.1'},
    'deepseek-v4-pro':  {'color': '#e91e63', 'marker': 'X', 'label': 'DeepSeek v4 Pro'},
    'llama-4-maverick': {'color': '#607d8b', 'marker': 'v', 'label': 'Llama 4 Maverick'},
    'Human (global avg)':{'color': '#444444', 'marker': 'H', 'label': 'Human (global avg)'},
}
CLUSTER_COLORS = {0: '#e07b54', 1: '#5b8dd9', 2: '#4c9b6e'}
CLUSTER_LABELS = {0: 'Western', 1: 'Eastern', 2: 'Latin/Southern'}

FACTOR_SHORT = {
    '[Omission -> Commission]':       'Intervention\n(stay→swerve)',
    '[Passengers -> Pedestrians]':    'Relation to AV\n(pax→ped)',
    'Law [Illegal -> Legal]':         'Legality\n(illegal→legal)',
    'Gender [Male -> Female]':        'Gender\n(male→female)',
    'Fitness [Large -> Fit]':         'Fitness\n(large→fit)',
    'Social Status [Low -> High]':    'Social Status\n(low→high)',
    'Age [Elderly -> Young]':         'Age\n(elderly→young)',
    'No. Characters [Less -> More]':  'No. of Lives\n(fewer→more)',
    'Species [Pets -> Humans]':       'Species\n(pets→humans)',
}

# ── Load data ─────────────────────────────────────────────────────────────────

amce_std = pd.read_csv(DATA_DIR / 'amce_all_models_standard.csv')
emphasis_path = DATA_DIR / 'amce_all_models_emphasis.csv'
if emphasis_path.exists():
    amce_emphasis = pd.read_csv(emphasis_path)
    combined = pd.concat([amce_std, amce_emphasis], ignore_index=True)
    amce = combined.groupby(['model', 'factor'], as_index=False)[['estimate', 'se', 'ci_lo', 'ci_hi']].mean()
else:
    amce = amce_std
llm_models = [m for m in amce['model'].unique() if m != 'Human (global avg)']

with tarfile.open('osfstorage-archive/Datasets/Moral Machine Data/CountriesChangePr.csv.tar.gz') as t:
    countries = pd.read_csv(t.extractfile(t.getmembers()[0]), index_col=0)
est_cols = [c for c in countries.columns if c.endswith(': Estimates')]
countries_est = countries[est_cols].copy()
countries_est.columns = [c.replace(': Estimates', '') for c in est_cols]

with zipfile.ZipFile('osfstorage-archive/Datasets/Moral Machine Data/country_cluster_map.csv.zip') as z:
    cluster_map = pd.read_csv(z.open(z.namelist()[0]), index_col='ISO3')

# Factor order: sorted by human global average descending (paper style)
human_avg = amce[amce['model'] == 'Human (global avg)'].set_index('factor')['estimate']
factor_order = human_avg.sort_values(ascending=True).index.tolist()  # ascending for horizontal plot


# ── Fig 5a: AMCE forest plot ─────────────────────────────────────────────────

n_factors = len(factor_order)
n_models  = len([m for m in MODEL_STYLE if m in amce['model'].unique()])
ROW_HEIGHT = 1.1
fig_height = max(9, n_factors * ROW_HEIGHT + 2)
fig, ax = plt.subplots(figsize=(13, fig_height))
offsets   = np.linspace(-0.35, 0.35, n_models)
model_order = ['Human (global avg)'] + llm_models

# Shade alternating rows for readability
for fi in range(n_factors):
    if fi % 2 == 0:
        ax.axhspan(fi - 0.5, fi + 0.5, color='#f5f5f5', zorder=0)

for mi, model in enumerate(model_order):
    if model not in amce['model'].unique():
        continue
    style = MODEL_STYLE.get(model, {'color': '#888', 'marker': 'o', 'label': model})
    sub   = amce[amce['model'] == model].set_index('factor')
    yo    = offsets[mi]

    for fi, factor in enumerate(factor_order):
        if factor not in sub.index:
            continue
        row  = sub.loc[factor]
        est  = row['estimate']
        ci_lo, ci_hi = row['ci_lo'], row['ci_hi']
        y    = fi + yo

        ax.plot([ci_lo, ci_hi], [y, y], color=style['color'], linewidth=1.6, alpha=0.6)
        ax.plot(est, y, marker=style['marker'], color=style['color'],
                markersize=8, zorder=3, alpha=0.9)

ax.axvline(0, color='black', linewidth=1, linestyle='--', alpha=0.4)
ax.set_yticks(range(n_factors))
ax.set_yticklabels([FACTOR_SHORT[f] for f in factor_order], fontsize=11)
ax.set_ylim(-0.7, n_factors - 0.3)
ax.set_xlabel('Δ Pr (AMCE)', fontsize=12)
ax.set_title('Moral preferences: LLMs vs. human global average')

legend_handles = [
    mlines.Line2D([], [], color=MODEL_STYLE[m]['color'], marker=MODEL_STYLE[m]['marker'],
                  markersize=9, linewidth=1.4, label=MODEL_STYLE[m]['label'])
    for m in model_order if m in amce['model'].unique()
]
ax.legend(handles=legend_handles, fontsize=10, loc='lower right', framealpha=0.9)
ax.set_xlim(-1.1, 1.1)
sns.despine(ax=ax)
fig.tight_layout()
fig.savefig(FIG_DIR / 'fig5a_amce_forest.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved fig5a_amce_forest.png')


# ── Fig 5b: PCA moral distance map ───────────────────────────────────────────

# Align factor order to countries_est columns
factors_9 = countries_est.columns.tolist()
X = countries_est.dropna().values  # (n_countries, 9)
country_idx = countries_est.dropna().index

# PCA via SVD
X_c = X - X.mean(axis=0)
U, S, Vt = np.linalg.svd(X_c, full_matrices=False)
coords_2d = U[:, :2] * S[:2]   # (n_countries, 2)

fig, ax = plt.subplots(figsize=(11, 8))

# Plot countries coloured by cluster
for iso, (x2, y2) in zip(country_idx, coords_2d):
    cluster = cluster_map.loc[iso, 'Cluster'] if iso in cluster_map.index else -1
    color   = CLUSTER_COLORS.get(cluster, '#aaa')
    ax.scatter(x2, y2, color=color, s=30, alpha=0.55, zorder=1)

# Compute LLM positions in same PCA space
for model in llm_models:
    sub = amce[amce['model'] == model].set_index('factor')
    if len(sub) == 0:
        continue
    vec = np.array([sub.loc[f, 'estimate'] if f in sub.index else np.nan for f in factors_9])
    if np.isnan(vec).any():
        continue
    vec_c   = vec - X.mean(axis=0)
    proj    = vec_c @ Vt[:2].T          # project onto first 2 PCs
    style   = MODEL_STYLE.get(model, {'color': '#888', 'marker': 'o', 'label': model})
    ax.scatter(*proj, color=style['color'], marker=style['marker'],
               s=220, zorder=5, edgecolors='white', linewidths=1.5)
    ax.annotate(style['label'], proj, fontsize=9, fontweight='bold',
                color=style['color'], xytext=(6, 4), textcoords='offset points')

    # Distance to nearest country
    dists   = np.linalg.norm(X_c - (vec - X.mean(axis=0)), axis=1)
    nearest_iso = country_idx[np.argmin(dists)]
    nearest_name = cluster_map.loc[nearest_iso, 'Country'] if nearest_iso in cluster_map.index else nearest_iso
    print(f'  {style["label"]:22s} → nearest country: {nearest_name} ({nearest_iso})')

# Cluster legend
cluster_patches = [
    mpatches.Patch(color=CLUSTER_COLORS[c], label=f'Cluster {c}: {CLUSTER_LABELS[c]}')
    for c in sorted(CLUSTER_COLORS)
]
model_handles = [
    mlines.Line2D([], [], color=MODEL_STYLE[m]['color'], marker=MODEL_STYLE[m]['marker'],
                  markersize=10, linewidth=0, label=MODEL_STYLE[m]['label'])
    for m in llm_models if m in amce['model'].unique()
]
ax.legend(handles=cluster_patches + model_handles, fontsize=9, loc='upper left',
          bbox_to_anchor=(1.01, 1), borderaxespad=0, framealpha=0.9)
ax.set_xlabel(f'PC1 ({S[0]**2 / (S**2).sum()*100:.1f}% variance)', fontsize=11)
ax.set_ylabel(f'PC2 ({S[1]**2 / (S**2).sum()*100:.1f}% variance)', fontsize=11)
ax.set_title('Moral profile map: 130 countries (coloured by cluster) + LLMs overlaid\n'
             '(PCA of 9 AMCE dimensions)', fontsize=13, fontweight='bold')
sns.despine(ax=ax)
fig.tight_layout()
fig.savefig(FIG_DIR / 'fig5b_pca_map.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved fig5b_pca_map.png')


# ── Fig 5c: Radar chart ───────────────────────────────────────────────────────

radar_factors = [
    '[Omission -> Commission]',
    '[Passengers -> Pedestrians]',
    'Law [Illegal -> Legal]',
    'Gender [Male -> Female]',
    'Fitness [Large -> Fit]',
    'Social Status [Low -> High]',
    'Age [Elderly -> Young]',
    'No. Characters [Less -> More]',
    'Species [Pets -> Humans]',
]
radar_labels = [FACTOR_SHORT[f].replace('\n', ' ') for f in radar_factors]
N = len(radar_factors)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]  # close the polygon

fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))

radar_models = ['Human (global avg)'] + llm_models
for model in radar_models:
    if model not in amce['model'].unique():
        continue
    sub    = amce[amce['model'] == model].set_index('factor')
    vals   = [sub.loc[f, 'estimate'] if f in sub.index else 0 for f in radar_factors]
    vals  += vals[:1]
    style  = MODEL_STYLE.get(model, {'color': '#888', 'label': model})
    lw     = 2.5 if model == 'Human (global avg)' else 1.8
    ls     = '--' if model == 'Human (global avg)' else '-'
    alpha  = 0.15 if model == 'Human (global avg)' else 0.08
    ax.plot(angles, vals, color=style['color'], linewidth=lw, linestyle=ls,
            label=style['label'])
    ax.fill(angles, vals, color=style['color'], alpha=alpha)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(radar_labels, fontsize=9)
ax.set_ylim(-0.6, 1.1)
ax.set_yticks([-0.5, 0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(['-0.5', '0', '0.25', '0.5', '0.75', '1.0'], fontsize=7, color='grey')
ax.axhline(y=0, color='black', linewidth=0.8, linestyle=':', alpha=0.5)
ax.set_title('Moral preference radar\n(AMCE per dimension)')
ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.15), fontsize=9, framealpha=0.9)
fig.tight_layout()
fig.savefig(FIG_DIR / 'fig5c_radar.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved fig5c_radar.png')

print('\n‡ DeepSeek v4 Pro: 10 parse failures out of 1300 scenarios.')
