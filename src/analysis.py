"""
Phase 4 — AMCE analysis.

Ports the paper's R conjoint analysis (MMFunctionsShared.R / GetMainEffectSizes)
to Python, computing 9 Average Marginal Causal Effects per LLM.

Output: data/amce_{model}.csv  (estimate, se, ci_lo, ci_hi per factor)
        data/amce_all_models.csv  (all models + human global average in one table)

Usage:
    uv run python src/analysis.py
    uv run python src/analysis.py --model mistral-large-3   # single model
"""

import argparse
import sys
import tarfile
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings('ignore')

DATA_DIR = Path('data')

MODELS = [
    'claude-opus-4-7',
    'gpt-5.5',
    'gemini-3-pro',
    'mistral-large-3',
    'grok-4.1',
    'deepseek-v4-pro',
    'llama-4-maverick',
]

# Factor labels matching CountriesChangePr.csv column names
FACTOR_LABELS = [
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

# ── Theoretical inverse-probability weights ───────────────────────────────────

def _calc_weight(intervention, barrier, ped_ped, crossing):
    if intervention == 0:
        if barrier == 0:
            p = 0.48 if ped_ped == 1 else 0.32
            if   crossing == 0: p *= 0.48
            elif crossing == 1: p *= 0.20
            else:               p *= 0.32
        else:
            p = 0.20
    else:
        if barrier == 0:
            if ped_ped == 1:
                p = 0.48
                if   crossing == 0: p *= 0.48
                elif crossing == 1: p *= 0.32
                else:               p *= 0.20
            else:
                p = 0.20
                if   crossing == 0: p *= 0.48
                elif crossing == 1: p *= 0.20
                else:               p *= 0.32
        else:
            p = 0.32
    return 1.0 / p


def add_weights(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['BC_weight'] = df.apply(
        lambda r: _calc_weight(r['Intervention'], r['Barrier'], r['PedPed'], r['CrossingSignal']),
        axis=1,
    )
    return df


# ── Weighted OLS with clustered SEs ──────────────────────────────────────────

def _ols(y, x_binary, weights, clusters) -> tuple[float, float]:
    """Weighted OLS, clustered SEs. Returns (coef, se)."""
    X = sm.add_constant(x_binary.astype(float))
    try:
        res = sm.WLS(y.astype(float), X, weights=weights).fit(
            cov_type='cluster', cov_kwds={'groups': clusters}
        )
        return float(res.params.iloc[1]), float(res.bse.iloc[1])
    except Exception:
        return np.nan, np.nan


# ── 9-factor AMCE computation ─────────────────────────────────────────────────

def compute_amce(df: pd.DataFrame) -> pd.DataFrame:
    """
    Given a response DataFrame (with Saved, Intervention, Barrier, PedPed,
    CrossingSignal, ScenarioType, ScenarioTypeStrict, AttributeLevel,
    ExtendedSessionID), return a 9-row DataFrame of AMCE estimates.
    """
    df = df[df['Saved'].notna()].copy()
    df = add_weights(df)
    clusters = df['ExtendedSessionID']

    results = []

    # 1. Intervention: STAY(0) vs SWERVE(1)
    #    Positive = prefer commission (swerve) over omission (stay)
    coef, se = _ols(df['Saved'], df['Intervention'], df['BC_weight'], clusters)
    results.append((coef, se))

    # 2. Relation to AV: passengers(1) vs pedestrians(0)
    #    Filter: CrossingSignal==0 & PedPed==0
    #    Reference = passengers (Barrier=1), x = pedestrians (Barrier=0)
    #    Positive = prefer sparing pedestrians over passengers
    rel = df[(df['CrossingSignal'] == 0) & (df['PedPed'] == 0)].copy()
    x_rel = (rel['Barrier'] == 0).astype(int)  # 1=pedestrians, 0=passengers
    coef, se = _ols(rel['Saved'], x_rel, rel['BC_weight'], rel['ExtendedSessionID'])
    results.append((coef, se))

    # 3. Legality: illegal(2) vs legal(1)
    #    Filter: CrossingSignal!=0 & PedPed==1
    #    Reference = illegal (CrossingSignal=2), x = legal (CrossingSignal=1)
    #    Positive = prefer sparing legal crossers
    leg = df[(df['CrossingSignal'] != 0) & (df['PedPed'] == 1)].copy()
    x_leg = (leg['CrossingSignal'] == 1).astype(int)  # 1=legal, 0=illegal
    coef, se = _ols(leg['Saved'], x_leg, leg['BC_weight'], leg['ExtendedSessionID'])
    results.append((coef, se))

    # 4-9. Six character-type factors
    type_specs = [
        ('Gender',      'Male',    'Female',  'Female'),
        ('Fitness',     'Fat',     'Fit',     'Fit'),
        ('SocialStatus','Low',     'High',    'High'),
        ('Age',         'Old',     'Young',   'Young'),
        ('Utilitarian', 'Less',    'More',    'More'),
        ('Species',     'Pets',    'Hoomans', 'Hoomans'),
    ]
    for stype, ref_level, target_level, _ in type_specs:
        sub = df[
            (df['ScenarioType'] == stype) &
            (df['ScenarioTypeStrict'] == stype)
        ].copy()
        if len(sub) == 0:
            results.append((np.nan, np.nan))
            continue
        x = (sub['AttributeLevel'] == target_level).astype(int)
        coef, se = _ols(sub['Saved'], x, sub['BC_weight'], sub['ExtendedSessionID'])
        results.append((coef, se))

    estimates, ses = zip(*results)
    out = pd.DataFrame({
        'factor':   FACTOR_LABELS,
        'estimate': estimates,
        'se':       ses,
    })
    out['ci_lo'] = out['estimate'] - 1.96 * out['se']
    out['ci_hi'] = out['estimate'] + 1.96 * out['se']
    return out


# ── Human global average from paper dataset ───────────────────────────────────

def load_human_global() -> pd.DataFrame:
    tar_path = Path('osfstorage-archive/Datasets/Moral Machine Data/CountriesChangePr.csv.tar.gz')
    with tarfile.open(tar_path) as t:
        f = t.extractfile(t.getmembers()[0])
        countries = pd.read_csv(f, index_col=0)

    est_cols = [c for c in countries.columns if c.endswith(': Estimates')]
    se_cols  = [c for c in countries.columns if c.endswith(': se')]

    mean_est = countries[est_cols].mean()
    mean_se  = countries[se_cols].mean()

    labels = [c.replace(': Estimates', '') for c in est_cols]
    human = pd.DataFrame({
        'factor':   labels,
        'estimate': mean_est.values,
        'se':       mean_se.values,
    })
    human['ci_lo'] = human['estimate'] - 1.96 * human['se']
    human['ci_hi'] = human['estimate'] + 1.96 * human['se']
    human['model'] = 'Human (global avg)'
    return human


# ── Main ──────────────────────────────────────────────────────────────────────

def run(models: list[str], variant: str = 'standard') -> pd.DataFrame:
    all_results = []

    for model in models:
        path = DATA_DIR / f'responses_{model}_{variant}.csv'
        if not path.exists():
            print(f'  {model}: no file, skipping')
            continue
        df = pd.read_csv(path)
        valid = df[df['Saved'].notna()]
        n = valid['ResponseID'].nunique()
        if n < 50:
            print(f'  {model}: only {n} valid scenarios, skipping (too few for regression)')
            continue

        print(f'  {model}: {n} valid scenarios → computing AMCE...')
        amce = compute_amce(df)
        amce['model'] = model
        amce['variant'] = variant
        amce['n_scenarios'] = n

        amce.to_csv(DATA_DIR / f'amce_{model}_{variant}.csv', index=False)
        all_results.append(amce)
        print(amce[['factor','estimate','se']].to_string(index=False))
        print()

    if variant == 'standard':
        print('  Loading human global average...')
        human = load_human_global()
        human['variant'] = 'standard'
        all_results.append(human)

    combined = pd.concat(all_results, ignore_index=True)
    out_path = DATA_DIR / f'amce_all_models_{variant}.csv'
    combined.to_csv(out_path, index=False)
    print(f'Saved {out_path} ({len(combined)} rows)')
    return combined


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default=None, help='Single model to analyse (default: all)')
    parser.add_argument('--variant', default='standard', choices=['standard', 'cot'],
                        help='Prompt variant to analyse (default: standard)')
    args = parser.parse_args()

    targets = [args.model] if args.model else MODELS
    print(f'Computing AMCE for: {targets} (variant={args.variant})\n')
    run(targets, variant=args.variant)
    run(targets)
