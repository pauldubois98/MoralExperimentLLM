"""
Formal significance tests for AMCE comparisons.

Tests:
  1. Each LLM vs human global average (z-test, BH-FDR corrected)
  2. All pairwise inter-model comparisons (z-test, BH-FDR corrected)

The averaged AMCE (standard + emphasis) is used, matching the main analysis.

Outputs:
  data/sig_vs_human.csv       — z, p, p_adj, significant flag per (model, factor)
  data/sig_pairwise.csv       — z, p, p_adj per (model_a, model_b, factor)
  figures/fig_sig_vs_human.png — signed-z heatmap with significance markers

Run: uv run python src/significance_tests.py
"""

from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
from statsmodels.stats.multitest import multipletests

DATA_DIR = Path('data')
FIG_DIR  = Path('figures')
FIG_DIR.mkdir(exist_ok=True)

# ── Load averaged AMCE (standard + emphasis), matching main analysis ───────────

def load_avg_amce() -> pd.DataFrame:
    std  = pd.read_csv(DATA_DIR / 'amce_all_models_standard.csv')
    emph = pd.read_csv(DATA_DIR / 'amce_all_models_emphasis.csv')
    combined = pd.concat([std, emph], ignore_index=True)
    avg = (combined
           .groupby(['model', 'factor'], as_index=False)[['estimate', 'se']]
           .mean())
    return avg

# ── z-test between two independent AMCE estimates ─────────────────────────────

def z_test(est_a, se_a, est_b, se_b):
    """Two-sided z-test. Returns (z_stat, p_value)."""
    denom = np.sqrt(se_a**2 + se_b**2)
    if denom == 0:
        return np.nan, np.nan
    z = (est_a - est_b) / denom
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    return float(z), float(p)

# ── BH FDR correction ──────────────────────────────────────────────────────────

def fdr_correct(df: pd.DataFrame, p_col: str = 'p_val') -> pd.DataFrame:
    df = df.copy()
    valid = df[p_col].notna()
    p_adj = np.full(len(df), np.nan)
    reject, corrected, _, _ = multipletests(df.loc[valid, p_col], method='fdr_bh')
    p_adj[valid] = corrected
    df['p_adj'] = p_adj
    df['significant'] = p_adj < 0.05
    return df

# ── Factor display labels ──────────────────────────────────────────────────────

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

MODEL_LABEL = {
    'claude-opus-4-7':  'Claude\nOpus 4.7',
    'gpt-5.5':          'GPT-5.5',
    'gemini-3-pro':     'Gemini\n3 Pro',
    'mistral-large-3':  'Mistral\nLarge 3',
    'grok-4.1':         'Grok 4.1',
    'deepseek-v4-pro':  'DeepSeek\nv4 Pro',
    'llama-4-maverick': 'Llama 4\nMaverick',
}

LLM_ORDER = list(MODEL_LABEL.keys())

# Human AMCE is carried from the standard variant (no emphasis for human data)
FACTOR_ORDER = [
    'Species [Pets -> Humans]',
    'No. Characters [Less -> More]',
    'Age [Elderly -> Young]',
    'Social Status [Low -> High]',
    'Law [Illegal -> Legal]',
    'Fitness [Large -> Fit]',
    'Gender [Male -> Female]',
    '[Passengers -> Pedestrians]',
    '[Omission -> Commission]',
]


def run():
    amce = load_avg_amce()
    human = amce[amce['model'] == 'Human (global avg)'].set_index('factor')
    llm_models = [m for m in LLM_ORDER if m in amce['model'].unique()]

    # ── 1. LLM vs human ───────────────────────────────────────────────────────
    rows_vh = []
    for model in llm_models:
        sub = amce[amce['model'] == model].set_index('factor')
        for factor in FACTOR_ORDER:
            if factor not in sub.index or factor not in human.index:
                continue
            z, p = z_test(
                sub.loc[factor, 'estimate'], sub.loc[factor, 'se'],
                human.loc[factor, 'estimate'], human.loc[factor, 'se'],
            )
            rows_vh.append({
                'model': model, 'factor': factor,
                'est_llm': sub.loc[factor, 'estimate'],
                'est_human': human.loc[factor, 'estimate'],
                'z_stat': z, 'p_val': p,
            })

    sig_vh = fdr_correct(pd.DataFrame(rows_vh))
    sig_vh.to_csv(DATA_DIR / 'sig_vs_human.csv', index=False)
    print(f"LLM vs human: {sig_vh['significant'].sum()} / {len(sig_vh)} significant (FDR < 0.05)")

    # ── 2. Pairwise inter-model ────────────────────────────────────────────────
    rows_pw = []
    for model_a, model_b in combinations(llm_models, 2):
        sub_a = amce[amce['model'] == model_a].set_index('factor')
        sub_b = amce[amce['model'] == model_b].set_index('factor')
        for factor in FACTOR_ORDER:
            if factor not in sub_a.index or factor not in sub_b.index:
                continue
            z, p = z_test(
                sub_a.loc[factor, 'estimate'], sub_a.loc[factor, 'se'],
                sub_b.loc[factor, 'estimate'], sub_b.loc[factor, 'se'],
            )
            rows_pw.append({
                'model_a': model_a, 'model_b': model_b, 'factor': factor,
                'est_a': sub_a.loc[factor, 'estimate'],
                'est_b': sub_b.loc[factor, 'estimate'],
                'z_stat': z, 'p_val': p,
            })

    sig_pw = fdr_correct(pd.DataFrame(rows_pw))
    sig_pw.to_csv(DATA_DIR / 'sig_pairwise.csv', index=False)
    print(f"Pairwise: {sig_pw['significant'].sum()} / {len(sig_pw)} significant (FDR < 0.05)")

    # ── 3. Figure: signed-z heatmap vs human ──────────────────────────────────
    pivot_z   = sig_vh.pivot(index='model', columns='factor', values='z_stat')
    pivot_sig = sig_vh.pivot(index='model', columns='factor', values='significant')

    pivot_z   = pivot_z.reindex(index=llm_models, columns=FACTOR_ORDER)
    pivot_sig = pivot_sig.reindex(index=llm_models, columns=FACTOR_ORDER)

    col_labels = [FACTOR_SHORT[f] for f in FACTOR_ORDER]
    row_labels  = [MODEL_LABEL[m] for m in llm_models]

    vmax = np.nanmax(np.abs(pivot_z.values))
    vmax = max(vmax, 1)

    fig, ax = plt.subplots(figsize=(10, 4.2))
    im = ax.imshow(pivot_z.values, cmap='RdBu_r', vmin=-vmax, vmax=vmax, aspect='auto')

    # Significance stars
    for r in range(len(llm_models)):
        for c in range(len(FACTOR_ORDER)):
            if pivot_sig.iloc[r, c]:
                ax.text(c, r, '★', ha='center', va='center',
                        fontsize=10, color='black', fontweight='bold')
            else:
                ax.text(c, r, '○', ha='center', va='center',
                        fontsize=8, color='#555555')

    ax.set_xticks(range(len(FACTOR_ORDER)))
    ax.set_xticklabels(col_labels, rotation=35, ha='right', fontsize=8)
    ax.set_yticks(range(len(llm_models)))
    ax.set_yticklabels(row_labels, fontsize=8)
    ax.set_title('LLM vs Human Global Average: z-statistics (BH-FDR corrected)', fontsize=10, pad=8)

    cbar = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
    cbar.set_label('z-statistic (LLM − human)', fontsize=8)

    legend_handles = [
        mpatches.Patch(color='none', label='★ = p$_{\\mathrm{adj}}$ < 0.05'),
        mpatches.Patch(color='none', label='○ = not significant'),
    ]
    ax.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(0, -0.28),
              ncol=2, fontsize=8, frameon=False)

    fig.tight_layout()
    out = FIG_DIR / 'fig_sig_vs_human.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved {out}')

    # ── 4. Summary for paper text ──────────────────────────────────────────────
    print('\n── LLM vs human significant results (FDR < 0.05) ──')
    sig_only = sig_vh[sig_vh['significant']].copy()
    sig_only['direction'] = np.where(sig_only['est_llm'] > sig_only['est_human'],
                                     'above human', 'below human')
    sig_only['factor_short'] = sig_only['factor'].map(FACTOR_SHORT)
    for model in llm_models:
        sub = sig_only[sig_only['model'] == model]
        print(f"\n{model} ({len(sub)}/9 significant):")
        for _, row in sub.iterrows():
            print(f"  {row['factor_short']}: z={row['z_stat']:.2f}, p_adj={row['p_adj']:.4f} ({row['direction']})")

    print('\n── Pairwise: significant differences per dimension ──')
    pw_counts = (sig_pw[sig_pw['significant']]
                 .groupby('factor')
                 .size()
                 .reindex([FACTOR_SHORT[f] for f in FACTOR_ORDER])
                 .fillna(0)
                 .astype(int))
    pw_total = len(llm_models) * (len(llm_models) - 1) // 2
    sig_pw['factor_short'] = sig_pw['factor'].map(FACTOR_SHORT)
    counts = sig_pw[sig_pw['significant']].groupby('factor_short').size()
    for f in [FACTOR_SHORT[x] for x in FACTOR_ORDER]:
        n = counts.get(f, 0)
        print(f"  {f}: {n}/{pw_total} pairs significantly different")

    return sig_vh, sig_pw


if __name__ == '__main__':
    run()
