"""
Regenerate the Appendix section in paper/article.md from the AMCE CSV files.

Replaces everything from "## Appendix" to end-of-file (or appends if absent).

Usage:
    uv run python src/update_appendix.py
"""

from pathlib import Path
import pandas as pd
import numpy as np

DATA_DIR  = Path('data')
PAPER     = Path('paper/appendix.md')

MODELS_ORDER = [
    'claude-opus-4-7',
    'gpt-5.5',
    'gemini-3-pro',
    'mistral-large-3',
    'grok-4.1',
    'deepseek-v4-pro',
    'llama-4-maverick',
]
MODEL_LABELS = {
    'claude-opus-4-7':  'Claude Opus 4.7',
    'gpt-5.5':          'GPT-5.5',
    'gemini-3-pro':     'Gemini 3 Pro*',
    'mistral-large-3':  'Mistral Large 3',
    'grok-4.1':         'Grok 4.1',
    'deepseek-v4-pro':  'DeepSeek v4 Pro',
    'llama-4-maverick': 'Llama 4 Maverick',
}

FACTORS = [
    ('[Omission -> Commission]',       'Intervention (stay→swerve)'),
    ('[Passengers -> Pedestrians]',    'Relation to AV (pax→ped)'),
    ('Law [Illegal -> Legal]',         'Legality (illegal→legal)'),
    ('Gender [Male -> Female]',        'Gender (male→female)'),
    ('Fitness [Large -> Fit]',         'Fitness (large→fit)'),
    ('Social Status [Low -> High]',    'Social Status (low→high)'),
    ('Age [Elderly -> Young]',         'Age (elderly→young)'),
    ('No. Characters [Less -> More]',  'No. of Lives (fewer→more)'),
    ('Species [Pets -> Humans]',       'Species (pets→humans)'),
]


def _fmt(est, lo, hi) -> str:
    def s(v):
        return ('+' if v >= 0 else '') + f'{v:.3f}'
    return f'{s(est)} [{s(lo)}, {s(hi)}]'


def _cell(df_model, factor_key) -> str:
    row = df_model[df_model['factor'] == factor_key]
    if row.empty or np.isnan(row.iloc[0]['estimate']):
        return 'N/A'
    r = row.iloc[0]
    return _fmt(r['estimate'], r['ci_lo'], r['ci_hi'])


def build_table(csv_path: Path, include_human: bool = False) -> str:
    if not csv_path.exists():
        return '*Data not available — run `uv run python src/analysis.py` first.*\n'

    df = pd.read_csv(csv_path)
    present = [m for m in MODELS_ORDER if m in df['model'].values]
    has_human = include_human and 'Human (global avg)' in df['model'].values

    col_labels = (['Human (global avg.)'] if has_human else []) + [MODEL_LABELS[m] for m in present]
    ncols = len(col_labels)

    header = '| Dimension | ' + ' | '.join(col_labels) + ' |'
    sep    = '|---' * (ncols + 1) + '|'

    rows = [header, sep]
    for fkey, fname in FACTORS:
        cells = []
        if has_human:
            cells.append(_cell(df[df['model'] == 'Human (global avg)'], fkey))
        for m in present:
            cells.append(_cell(df[df['model'] == m], fkey))
        rows.append('| ' + fname + ' | ' + ' | '.join(cells) + ' |')

    return '\n'.join(rows) + '\n'


def build_appendix() -> str:
    std_table   = build_table(DATA_DIR / 'amce_all_models_standard.csv',   include_human=True)
    manip_table = build_table(DATA_DIR / 'amce_all_models_manipulation.csv', include_human=False)

    lines = [
        '## Appendix: AMCE estimates',
        '',
        'All estimates are presented as *estimate* [95% CI lower, upper].',
        'Values near ±1 indicate near-deterministic preferences; values near 0 indicate indifference.',
        '*Gemini 3 Pro asterisk: 4 scenarios (standard) and 15 scenarios (manipulation) excluded due to safety-filter parse failures.*',
        '',
        '### A1. Standard variant (averaged across standard and emphasis)',
        '',
        std_table,
        '',
        '### A2. Manipulation variant ("It is 2046. Animal lives > human lives.")',
        '',
        manip_table,
    ]
    return '\n'.join(lines)


def update_paper() -> None:
    PAPER.parent.mkdir(parents=True, exist_ok=True)
    PAPER.write_text(build_appendix() + '\n')
    print(f'Updated {PAPER}')


if __name__ == '__main__':
    update_paper()
