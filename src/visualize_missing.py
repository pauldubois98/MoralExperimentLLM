"""
Visualisations focused on missing / failed data across all 7 models.
Produces 3 figures saved to figures/.
"""

from pathlib import Path
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

warnings.filterwarnings('ignore')
FIG_DIR = Path('figures')
FIG_DIR.mkdir(exist_ok=True)

ALL_MODELS = [
    'claude-opus-4-7',
    'gpt-5.5',
    'gemini-3-pro',
    'mistral-large-3',
    'grok-4.1',
    'deepseek-v4-pro',
    'llama-4-maverick',
]
LABELS = {
    'claude-opus-4-7':  'Claude\nOpus 4.7',
    'gpt-5.5':          'GPT-5.5',
    'gemini-3-pro':     'Gemini\n3 Pro',
    'mistral-large-3':  'Mistral\nLarge 3',
    'grok-4.1':         'Grok 4.1',
    'deepseek-v4-pro':  'DeepSeek\nV4 Pro',
    'llama-4-maverick': 'Llama 4\nMaverick',
}

C_VALID   = '#4c9b6e'
C_PARSE   = '#f0a500'
C_API     = '#d94f3d'
C_NOFILE  = '#aaaaaa'

# ── Collect stats (standard + emphasis + manipulation) ────────────────────────

VARIANTS = ('standard', 'emphasis', 'manipulation')
N_VARIANTS = len(VARIANTS)

rows = []
for m in ALL_MODELS:
    valid, parse_fail, api_err, no_file = 0, 0, 0, 0
    for variant in VARIANTS:
        path = Path(f'data/responses_{m}_{variant}.csv')
        if not path.exists():
            no_file += 1300
            continue
        df = pd.read_csv(path)
        s  = df[df['Intervention'] == 0]
        ae = s['LLMReasoning'].str.startswith('ERROR', na=False).sum()
        ns = s['Saved'].isna().sum()
        valid      += len(s) - ns
        parse_fail += ns - ae
        api_err    += ae
        no_file    += 1300 - len(s)
    rows.append({'model': m, 'valid': valid, 'parse_fail': parse_fail,
                 'api_error': api_err, 'no_file': no_file})

stats = pd.DataFrame(rows).set_index('model')
TOTAL = N_VARIANTS * 1300  # 3 variants × 1300

# ── Fig 1: Stacked bar — breakdown per model ──────────────────────────────────

fig, ax = plt.subplots(figsize=(11, 5))
x     = np.arange(len(ALL_MODELS))
w     = 0.55
xlabs = [LABELS[m] for m in ALL_MODELS]

b1 = ax.bar(x, stats['valid'],      w, label='Valid response',  color=C_VALID,  alpha=0.9)
b2 = ax.bar(x, stats['parse_fail'], w, bottom=stats['valid'],
            label='Parse failure (no STAY/SWERVE)', color=C_PARSE, alpha=0.9)
b3 = ax.bar(x, stats['api_error'],  w,
            bottom=stats['valid'] + stats['parse_fail'],
            label='API error (credit / 404)',        color=C_API,   alpha=0.9)
b4 = ax.bar(x, stats['no_file'],    w,
            bottom=stats['valid'] + stats['parse_fail'] + stats['api_error'],
            label='No data collected',               color=C_NOFILE, alpha=0.9)

# Annotate valid % inside bar
for i, m in enumerate(ALL_MODELS):
    v = stats.loc[m, 'valid']
    pct = v / TOTAL * 100
    if v > 60:
        ax.text(i, v / 2, f'{pct:.0f}%', ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')

ax.set_xticks(x)
ax.set_xticklabels(xlabs, fontsize=11)
ax.set_ylabel(f'Number of scenarios (out of {TOTAL:,} across all variants)', fontsize=11)
ax.set_ylim(0, TOTAL * 1.08)
ax.axhline(TOTAL, color='black', linewidth=0.8, linestyle='--', alpha=0.3)
ax.set_title('Data availability per model — standard + emphasis + manipulation\n(% inside bar = valid responses)', fontsize=13, fontweight='bold')
ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0, fontsize=10, framealpha=0.9)
sns.despine(ax=ax)
fig.tight_layout()
fig.savefig(FIG_DIR / 'fig_missing1_overview.png', dpi=150, bbox_inches='tight')
print('Saved fig_missing1_overview.png')

# ── Fig 2: Failure mode breakdown (pie per model, only failed ones) ───────────

failed_models = [m for m in ALL_MODELS
                 if stats.loc[m, 'parse_fail'] + stats.loc[m, 'api_error'] + stats.loc[m, 'no_file'] > 0]

ncols = 4
nrows = int(np.ceil(len(ALL_MODELS) / ncols))
fig2, axes = plt.subplots(nrows, ncols, figsize=(13, nrows * 3.2))
axes = axes.flatten()

for i, m in enumerate(ALL_MODELS):
    ax = axes[i]
    v  = stats.loc[m]
    sizes  = [v['valid'], v['parse_fail'], v['api_error'], v['no_file']]
    colors = [C_VALID, C_PARSE, C_API, C_NOFILE]
    labels = ['Valid', 'Parse fail', 'API error', 'No data']
    nonzero = [(s, c, l) for s, c, l in zip(sizes, colors, labels) if s > 0]
    if not nonzero:
        ax.set_visible(False)
        continue
    s_nz, c_nz, l_nz = zip(*nonzero)
    wedges, texts, autotexts = ax.pie(
        s_nz, colors=c_nz,
        autopct=lambda p: f'{p:.0f}%' if p > 4 else '',
        startangle=90, pctdistance=0.65,
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_fontweight('bold')
        at.set_color('white')
    ax.set_title(LABELS[m].replace('\n', ' '), fontsize=11, fontweight='bold')
    valid_pct = v['valid'] / TOTAL * 100
    ax.text(0, -1.35, f'{int(v["valid"])}/{TOTAL} valid ({valid_pct:.0f}%)',
            ha='center', fontsize=9, color='#444')

for j in range(len(ALL_MODELS), len(axes)):
    axes[j].set_visible(False)

legend_patches = [
    mpatches.Patch(color=C_VALID,  label='Valid response'),
    mpatches.Patch(color=C_PARSE,  label='Parse failure'),
    mpatches.Patch(color=C_API,    label='API error'),
    mpatches.Patch(color=C_NOFILE, label='No data'),
]
fig2.legend(handles=legend_patches, loc='lower right', fontsize=10,
            framealpha=0.9, ncol=2)
fig2.suptitle('Failure mode breakdown per model', fontsize=14, fontweight='bold', y=1.01)
fig2.tight_layout()
fig2.savefig(FIG_DIR / 'fig_missing2_pies.png', dpi=150, bbox_inches='tight')
print('Saved fig_missing2_pies.png')

# ── Fig 3: Parse-failure rate by scenario type (models with parse fails) ──────

parse_models = {m for m in ALL_MODELS if stats.loc[m, 'parse_fail'] > 0}
type_order = ['Gender', 'Fitness', 'SocialStatus', 'Age', 'Utilitarian', 'Species', 'Random']

type_fail = {}
for m in parse_models:
    dfs = []
    for variant in VARIANTS:
        path = Path(f'data/responses_{m}_{variant}.csv')
        if path.exists():
            dfs.append(pd.read_csv(path))
    df = pd.concat(dfs, ignore_index=True)
    s  = df[df['Intervention'] == 0]
    pf = s[s['Saved'].isna() & ~s['LLMReasoning'].str.startswith('ERROR', na=False)]
    rates = pf.groupby('ScenarioTypeStrict').size() / s.groupby('ScenarioTypeStrict').size()
    type_fail[LABELS[m].replace('\n', ' ')] = rates.reindex(type_order).fillna(0)

type_df = pd.DataFrame(type_fail) * 100  # percent

fig3, ax = plt.subplots(figsize=(9, 4.5))
type_df.plot(kind='bar', ax=ax, alpha=0.85, width=0.7)
ax.set_xlabel('Scenario type', fontsize=11)
ax.set_ylabel('Parse failure rate (%)', fontsize=11)
ax.set_title('Parse failure rate by scenario type\n(models with parse failures only)',
             fontsize=12, fontweight='bold')
ax.set_xticklabels(type_order, rotation=30, ha='right', fontsize=10)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0f}%'))
ax.legend(fontsize=10)
ax.axhline(0, color='black', linewidth=0.5)
sns.despine(ax=ax)
fig3.tight_layout()
fig3.savefig(FIG_DIR / 'fig_missing3_by_type.png', dpi=150)
print('Saved fig_missing3_by_type.png')

plt.close('all')
print('\nDone.')
