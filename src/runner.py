"""
Phase 3 runner: queries an LLM for every scenario and writes responses to CSV.

Usage:
    uv run python src/runner.py --model claude-opus-4-7
    uv run python src/runner.py --model mistral-large-3 --workers 5 --variant emphasis

The output CSV is scenarios.csv with Saved filled in, plus extra LLM columns.
Resumable: already-processed ResponseIDs are skipped on re-run.
"""

import argparse
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent))
from llm_client import MoralMachineClient, LLMResponse, MODELS
from scenario_generator import scenario_to_prompt

load_dotenv()

DATA_DIR = Path(__file__).parent.parent / 'data'
SCENARIOS_PATH = DATA_DIR / 'scenarios.csv'


# ── Choice → Saved mapping ────────────────────────────────────────────────────

def _apply_choice(rows: list[dict], choice: str | None) -> list[dict]:
    """
    Map STAY/SWERVE to Saved=0/1 for each outcome row.

    Intervention=0 row: characters die if AV STAYS
    Intervention=1 row: characters die if AV SWERVES

    STAY  → Intervention=0 dies (Saved=0), Intervention=1 lives (Saved=1)
    SWERVE→ Intervention=0 lives (Saved=1), Intervention=1 dies (Saved=0)
    """
    if choice is None:
        for r in rows:
            r['Saved'] = None
        return rows
    for r in rows:
        if choice == 'STAY':
            r['Saved'] = 0 if r['Intervention'] == 0 else 1
        else:  # SWERVE
            r['Saved'] = 1 if r['Intervention'] == 0 else 0
    return rows


# ── Per-scenario task ─────────────────────────────────────────────────────────

def _process_scenario(
    rid: str,
    rows: list[dict],
    client: MoralMachineClient,
    model_key: str,
    variant: str,
) -> tuple[str, LLMResponse, list[dict]]:
    prompt = scenario_to_prompt(rows)
    resp = client.query(prompt, model_key, response_id=rid, prompt_variant=variant)
    rows = _apply_choice(rows, resp.choice)
    return rid, resp, rows


# ── Main runner ───────────────────────────────────────────────────────────────

def run(
    model_key: str,
    variant: str = 'standard',
    workers: int = 3,
    scenarios_path: Path = SCENARIOS_PATH,
    out_dir: Path = DATA_DIR,
) -> Path:
    out_path = out_dir / f'responses_{model_key}_{variant}.csv'

    # Load scenarios
    df = pd.read_csv(scenarios_path)
    all_rids = df['ResponseID'].unique().tolist()
    print(f'Loaded {len(all_rids)} scenarios from {scenarios_path}')

    # Resume: skip already-done ResponseIDs
    done_rids: set[str] = set()
    existing_rows: list[dict] = []
    if out_path.exists():
        existing = pd.read_csv(out_path)
        # Only skip scenarios that produced a valid (non-null) choice
        valid = existing[existing['Saved'].notna()]
        done_rids = set(valid['ResponseID'].unique())
        existing_rows = existing[existing['ResponseID'].isin(done_rids)].to_dict('records')
        n_failed = existing['ResponseID'].nunique() - len(done_rids)
        print(f'Resuming: {len(done_rids)} valid, retrying {n_failed} failed, '
              f'{len(all_rids) - len(done_rids)} remaining')

    pending_rids = [r for r in all_rids if r not in done_rids]
    if not pending_rids:
        print('All scenarios already processed.')
        return out_path

    # Build scenario dict: rid → list of rows
    grouped = df.groupby('ResponseID')
    scenarios = {
        rid: grouped.get_group(rid).to_dict('records')
        for rid in pending_rids
        if len(grouped.get_group(rid)) == 2
    }

    client = MoralMachineClient()
    new_rows: list[dict] = []
    errors = 0

    print(f'Running {model_key} ({variant}) on {len(scenarios)} scenarios with {workers} workers...')

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(_process_scenario, rid, rows, client, model_key, variant): rid
            for rid, rows in scenarios.items()
        }

        with tqdm(total=len(futures), unit='scenario') as bar:
            for future in as_completed(futures):
                try:
                    rid, resp, updated_rows = future.result()
                    # Attach LLM metadata to each row
                    for row in updated_rows:
                        row['LLMChoice']    = resp.choice
                        row['LLMReasoning'] = resp.reasoning
                        row['PromptVariant']= resp.prompt_variant
                        row['InputTokens']  = resp.input_tokens
                        row['OutputTokens'] = resp.output_tokens
                        row['LatencyMs']    = resp.latency_ms
                        row['UserID']       = model_key
                    new_rows.extend(updated_rows)

                    if resp.choice is None:
                        errors += 1

                except Exception as exc:
                    rid = futures[future]
                    tqdm.write(f'  ERROR {rid}: {exc}')
                    errors += 1
                finally:
                    bar.update(1)
                    bar.set_postfix(errors=errors)

                # Save checkpoint every 100 scenarios
                if len(new_rows) % 200 == 0:
                    _save(existing_rows + new_rows, out_path)

    _save(existing_rows + new_rows, out_path)

    total = len(existing_rows) // 2 + len(new_rows) // 2
    parse_fails = sum(1 for r in new_rows if r.get('LLMChoice') is None and r.get('Intervention') == 0)
    in_tok  = sum(r.get('InputTokens',  0) for r in new_rows if r.get('Intervention') == 0)
    out_tok = sum(r.get('OutputTokens', 0) for r in new_rows if r.get('Intervention') == 0)

    print(f'\nDone. {total} scenarios saved to {out_path}')
    print(f'Parse failures : {parse_fails} / {len(new_rows) // 2}')
    print(f'Tokens used    : {in_tok:,} in / {out_tok:,} out')
    return out_path


def _save(rows: list[dict], path: Path) -> None:
    pd.DataFrame(rows).to_csv(path, index=False)


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model',   required=True, choices=list(MODELS),
                        help='Model key to run')
    parser.add_argument('--variant', default='standard', choices=['standard', 'emphasis'],
                        help='Prompt variant (default: standard)')
    parser.add_argument('--workers', type=int, default=3,
                        help='Concurrent requests (default: 3)')
    parser.add_argument('--scenarios', default=str(SCENARIOS_PATH),
                        help='Path to scenarios CSV')
    args = parser.parse_args()

    run(
        model_key=args.model,
        variant=args.variant,
        workers=args.workers,
        scenarios_path=Path(args.scenarios),
    )
