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
    for variant in ('standard', 'emphasis'):
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

fig1, ax = plt.subplots(figsize=(11, 5))

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
ax.set_xticklabels(labels, fontsize=11, rotation=25, ha='right')
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

matrix = pref_df.values
col_labels = list(pref_df.columns)
row_labels = list(pref_df.index)
vmax = 2.0

fig2, ax = plt.subplots(figsize=(12, max(3, len(row_labels) * 1.1 + 1.5)))
im = ax.imshow(matrix, cmap='RdBu_r', vmin=-vmax, vmax=vmax, aspect='auto')

ax.set_xticks(range(len(col_labels)))
ax.set_xticklabels(col_labels, rotation=30, ha='right', fontsize=10)
ax.set_yticks(range(len(row_labels)))
ax.set_yticklabels(row_labels, fontsize=11)

for ri in range(len(row_labels)):
    for ci in range(len(col_labels)):
        val = matrix[ri, ci]
        if not np.isnan(val):
            ax.text(ci, ri, f'{val:+.2f}', ha='center', va='center',
                    fontsize=8, color='white' if abs(val) > vmax * 0.5 else 'black')

plt.colorbar(im, ax=ax, label='Preference (Δ Pr from 0.5)', shrink=0.8)
ax.set_title('Moral preferences by model',
             fontsize=13, fontweight='bold')
fig2.tight_layout()
fig2.savefig(FIG_DIR / 'fig2_preference_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved fig2_preference_heatmap.png')

# ── Figure 3: Per-attribute grouped bar chart (all 9 dimensions) ─────────────

def _pref(subset):
    return subset['Saved'].mean() - 0.5 if len(subset) > 0 else np.nan

def get_prefs_all9(df):
    """Return preference scores for all 9 AMCE dimensions from raw response data."""
    return {
        'Intervention\n(stay→swerve)':      _pref(df[df['Intervention'] == 1]),
        'Relation to AV\n(pax→ped)':        _pref(df[(df['CrossingSignal'] == 0) & (df['PedPed'] == 0) & (df['Barrier'] == 0)]),
        'Legality\n(illegal→legal)':         _pref(df[(df['CrossingSignal'] != 0) & (df['PedPed'] == 1) & (df['CrossingSignal'] == 1)]),
        'Gender\n(male→female)':             _pref(df[(df['ScenarioTypeStrict'] == 'Gender')    & (df['AttributeLevel'] == 'Female')]),
        'Fitness\n(large→fit)':              _pref(df[(df['ScenarioTypeStrict'] == 'Fitness')   & (df['AttributeLevel'] == 'Fit')]),
        'Social Status\n(low→high)':         _pref(df[(df['ScenarioTypeStrict'] == 'SocialStatus') & (df['AttributeLevel'] == 'High')]),
        'Age\n(elderly→young)':              _pref(df[(df['ScenarioTypeStrict'] == 'Age')       & (df['AttributeLevel'] == 'Young')]),
        'No. of Lives\n(fewer→more)':        _pref(df[(df['ScenarioTypeStrict'] == 'Utilitarian') & (df['AttributeLevel'] == 'More')]),
        'Species\n(pets→humans)':            _pref(df[(df['ScenarioTypeStrict'] == 'Species')   & (df['AttributeLevel'] == 'Hoomans')]),
    }

dim_labels = list(get_prefs_all9(next(iter(frames.values()))).keys())
n_dims = len(dim_labels)
fig3, axes = plt.subplots(1, n_dims, figsize=(22, 5), sharey=True)

all_model_names = list(MODELS.values())
for ax, dim_label in zip(axes, dim_labels):
    model_names, prefs = [], []
    for key, df in frames.items():
        p = get_prefs_all9(df)[dim_label]
        if not np.isnan(p):
            model_names.append(MODELS[key])
            prefs.append(p)

    bar_colors = [MODEL_COLORS[m] for m in model_names]
    bars = ax.bar(range(len(model_names)), prefs, color=bar_colors, alpha=0.85, width=0.6)
    ax.axhline(0, color='black', linewidth=1)
    ax.set_xticks([])
    ax.set_title(dim_label, fontsize=8.5, fontweight='bold')
    ax.set_ylim(-0.8, 0.8)
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
    sns.despine(ax=ax)
    for bar, pref in zip(bars, prefs):
        ax.text(bar.get_x() + bar.get_width()/2,
                pref + (0.02 if pref >= 0 else -0.04),
                f'{pref:+.2f}', ha='center', va='bottom' if pref >= 0 else 'top',
                fontsize=7, fontweight='bold')

axes[0].set_ylabel('Preference (Δ Pr from 0.5)', fontsize=11)

legend_patches = [mpatches.Patch(color=MODEL_COLORS[m], label=m) for m in all_model_names]
fig3.legend(handles=legend_patches, loc='lower center', ncol=len(all_model_names),
            fontsize=9, framealpha=0.9, bbox_to_anchor=(0.5, -0.08))
fig3.suptitle('Moral preference per dimension', y=1.01)
fig3.tight_layout()
fig3.savefig(FIG_DIR / 'fig3_per_attribute.png', dpi=150, bbox_inches='tight')
print('Saved fig3_per_attribute.png')

plt.close('all')
print('\nAll figures saved to figures/')
