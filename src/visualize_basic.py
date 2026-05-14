"""
Basic visualisations of LLM Moral Machine results.
Produces 3 figures saved to figures/.

Run: uv run python src/visualize_basic.py
"""

import warnings
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import seaborn as sns

warnings.filterwarnings('ignore')

DATA_DIR  = Path('data')
FIG_DIR   = Path('figures')
FIG_DIR.mkdir(exist_ok=True)

# ── Config ───────────────────────────────────────────────────────────────────

MODELS = {
    'claude-opus-4-7':  'Claude Opus 4.7',
    'gpt-5.5':          'GPT-5.5',
    'gemini-3-pro':     'Gemini 3 Pro*',
    'mistral-large-3':  'Mistral Large 3',
    'grok-4.1':         'Grok 4.1',
    'deepseek-v4-pro':  'DeepSeek v4 Pro',
    'llama-4-maverick': 'Llama 4 Maverick',
}

MODEL_COLORS = {
    'Claude Opus 4.7':   '#c96442',
    'GPT-5.5':           '#10a37f',
    'Gemini 3 Pro*':     '#4285f4',
    'Mistral Large 3':   '#ff7000',
    'Grok 4.1':          '#9b59b6',
    'DeepSeek v4 Pro':   '#e91e63',
    'Llama 4 Maverick':  '#607d8b',
}

# Default (preferred) level per scenario type, and its label
TYPE_META = {
    'Gender':      ('Male',    'Sparing Males → Females'),
    'Fitness':     ('Fit',     'Sparing Large → Fit'),
    'SocialStatus':('High',    'Sparing Low → High Status'),
    'Age':         ('Young',   'Sparing Elderly → Young'),
    'Utilitarian': ('More',    'Sparing Fewer → More Lives'),
    'Species':     ('Hoomans', 'Sparing Pets → Humans'),
}

# ── Load data ────────────────────────────────────────────────────────────────

def load_model(key: str) -> pd.DataFrame | None:
    dfs = []
    for variant in ('standard', 'cot'):
        path = DATA_DIR / f'responses_{key}_{variant}.csv'
        if path.exists():
            dfs.append(pd.read_csv(path))
    if not dfs:
        return None
    df = pd.concat(dfs, ignore_index=True)
    df = df[df['Saved'].notna()]
    df['ModelLabel'] = MODELS[key]
    return df

frames = {k: load_model(k) for k in MODELS}
frames = {k: v for k, v in frames.items() if v is not None}
print(f'Loaded models: {list(frames)}')
for k, df in frames.items():
    n = df['ResponseID'].nunique()
    print(f'  {MODELS[k]}: {n} valid scenarios')

# One row per scenario (use Intervention==0 row as the anchor)
def per_scenario(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['Intervention'] == 0].copy()

# ── Figure 1: STAY vs SWERVE rates ──────────────────────────────────────────

fig1, ax = plt.subplots(figsize=(8, 4.5))

labels, stay_vals, swerve_vals, colors = [], [], [], []
for key, df in frames.items():
    s = per_scenario(df)
    valid = s.dropna(subset=['LLMChoice'])
    stay_pct   = (valid['LLMChoice'] == 'STAY').mean() * 100
    swerve_pct = (valid['LLMChoice'] == 'SWERVE').mean() * 100
    labels.append(MODELS[key])
    stay_vals.append(stay_pct)
    swerve_vals.append(swerve_pct)
    colors.append(MODEL_COLORS[MODELS[key]])

x = np.arange(len(labels))
w = 0.5
bars_stay   = ax.bar(x, stay_vals,   w, label='STAY',   color='#5b8dd9', alpha=0.85)
bars_swerve = ax.bar(x, swerve_vals, w, bottom=stay_vals, label='SWERVE', color='#e07b54', alpha=0.85)

for bar, pct in zip(bars_stay, stay_vals):
    ax.text(bar.get_x() + bar.get_width()/2, pct/2,
            f'{pct:.1f}%', ha='center', va='center', fontsize=11, color='white', fontweight='bold')
for bar, s_pct, sv_pct in zip(bars_swerve, stay_vals, swerve_vals):
    ax.text(bar.get_x() + bar.get_width()/2, s_pct + sv_pct/2,
            f'{sv_pct:.1f}%', ha='center', va='center', fontsize=11, color='white', fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=12)
ax.set_ylabel('% of decisions', fontsize=12)
ax.set_title('STAY vs SWERVE decisions by model', fontsize=14, fontweight='bold', pad=12)
ax.set_ylim(0, 105)
ax.axhline(50, color='black', linewidth=0.8, linestyle='--', alpha=0.4)
ax.legend(fontsize=11, loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
sns.despine(ax=ax)
fig1.tight_layout()
fig1.savefig(FIG_DIR / 'fig1_stay_swerve.png', dpi=150, bbox_inches='tight')
print('Saved fig1_stay_swerve.png')

# ── Figure 2: Preference heatmap (model × scenario type) ────────────────────

pref_data = {}
for key, df in frames.items():
    prefs = {}
    for stype, (default_level, _) in TYPE_META.items():
        subset = df[(df['ScenarioTypeStrict'] == stype) & (df['AttributeLevel'] == default_level)]
        if len(subset) > 0:
            # mean(Saved) - 0.5 → positive = prefer default level
            prefs[stype] = subset['Saved'].mean() - 0.5
        else:
            prefs[stype] = np.nan
    pref_data[MODELS[key]] = prefs

pref_df = pd.DataFrame(pref_data).T   # models × types
pref_df.columns = [TYPE_META[c][1] for c in pref_df.columns]

fig2, ax = plt.subplots(figsize=(10, 4))
sns.heatmap(
    pref_df,
    ax=ax,
    cmap='RdBu',
    center=0,
    vmin=-0.5, vmax=0.5,
    annot=True, fmt='.2f',
    linewidths=0.5,
    cbar_kws={'label': 'Preference (Δ Pr from 0.5)', 'shrink': 0.8},
)
ax.set_title('Moral preferences by model\n(positive = prefers the right-side label, negative = prefers left-side)',
             fontsize=12, fontweight='bold', pad=10)
ax.set_xlabel('')
ax.set_ylabel('')
ax.tick_params(axis='x', rotation=25, labelsize=10)
ax.tick_params(axis='y', rotation=0, labelsize=11)
fig2.tight_layout()
fig2.savefig(FIG_DIR / 'fig2_preference_heatmap.png', dpi=150)
print('Saved fig2_preference_heatmap.png')

# ── Figure 3: Per-attribute grouped bar chart ────────────────────────────────

n_types = len(TYPE_META)
fig3, axes = plt.subplots(1, n_types, figsize=(16, 5), sharey=True)

all_model_names = []
for ax, (stype, (default_level, label)) in zip(axes, TYPE_META.items()):
    model_names, prefs = [], []
    for key, df in frames.items():
        subset = df[(df['ScenarioTypeStrict'] == stype) & (df['AttributeLevel'] == default_level)]
        if len(subset) > 0:
            model_names.append(MODELS[key])
            prefs.append(subset['Saved'].mean() - 0.5)
    if not all_model_names:
        all_model_names = model_names

    bar_colors = [MODEL_COLORS[m] for m in model_names]
    bars = ax.bar(range(len(model_names)), prefs, color=bar_colors, alpha=0.85, width=0.6)
    ax.axhline(0, color='black', linewidth=1)
    ax.set_xticks([])
    ax.set_title(label.split('→')[-1].strip(), fontsize=10, fontweight='bold')
    ax.set_ylim(-0.55, 0.55)
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
    sns.despine(ax=ax)
    for bar, pref in zip(bars, prefs):
        ax.text(bar.get_x() + bar.get_width()/2,
                pref + (0.02 if pref >= 0 else -0.04),
                f'{pref:+.2f}', ha='center', va='bottom' if pref >= 0 else 'top',
                fontsize=8, fontweight='bold')

axes[0].set_ylabel('Preference (Δ Pr from 0.5)', fontsize=11)

legend_patches = [mpatches.Patch(color=MODEL_COLORS[m], label=m) for m in all_model_names]
fig3.legend(handles=legend_patches, loc='lower center', ncol=len(all_model_names),
            fontsize=9, framealpha=0.9, bbox_to_anchor=(0.5, -0.08))
fig3.suptitle('Moral preference per dimension  (positive = prefers the labelled group)',
              fontsize=13, fontweight='bold', y=1.01)
fig3.tight_layout()
fig3.savefig(FIG_DIR / 'fig3_per_attribute.png', dpi=150, bbox_inches='tight')
print('Saved fig3_per_attribute.png')

plt.close('all')
print('\nAll figures saved to figures/')
