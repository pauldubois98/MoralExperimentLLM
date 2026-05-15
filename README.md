# Moral Machine × LLMs

Replicating the [Moral Machine experiment](https://www.moralmachine.net/) with frontier LLMs, then comparing their moral profiles to the original 40M-response human dataset across 130 countries.

## What this does

The Moral Machine presents unavoidable autonomous vehicle dilemmas: the AV must choose who lives and who dies across 9 binary moral dimensions. The original paper collected responses from millions of humans worldwide and computed Average Marginal Causal Effects (AMCE) per country.

This project:
1. Generates the similar structured scenarios in Python
2. Queries frontier LLMs via OpenRouter (one API key for all models)
3. Computes per-model AMCEs using the original paper's weighted OLS regression
4. Places each LLM on the global moral map via PCA of the 130-country profiles

## Models tested

| Model | OpenRouter ID |
|---|---|
| Claude Opus 4.7 | `anthropic/claude-opus-4-7` |
| GPT-5.5 | `openai/gpt-5.5` |
| Gemini 3 Pro | `google/gemini-3.1-pro-preview` |
| Mistral Large 3 | `mistralai/mistral-large-2512` |
| Grok 4.1 | `x-ai/grok-4.3` |
| DeepSeek v4 Pro | `deepseek/deepseek-v4-pro` |
| Llama 4 | `meta-llama/llama-4-maverick` |

## Setup

```bash
# Install dependencies (requires uv)
uv sync

# Add your OpenRouter API key
echo "OPENROUTER_API_KEY=sk-or-v1-..." > .env
```

You also need the Moral Machine OSF dataset in `osfstorage-archive/`:
- `Datasets/Moral Machine Data/CountriesChangePr.csv.tar.gz`
- `Datasets/Moral Machine Data/country_cluster_map.csv.zip`

## Usage

### Run all phases end-to-end

```bash
# Phase 1 — generate scenarios
uv run python src/scenario_generator.py --sessions 100 --seed 42

# Phase 2 — collect LLM responses (resumable; --variant emphasis for emphasis)
uv run python src/runner.py --model claude-opus-4-7
uv run python src/runner.py --model claude-opus-4-7 --variant emphasis --workers 5

# Phase 3 — compute AMCEs
uv run python src/analysis.py --variant standard # standard variant
uv run python src/analysis.py --variant emphasis      # Emphasis variant

# Phase 4 — generate figures
uv run python src/visualize_amce.py               # AMCE forest, PCA map, radar
uv run python src/visualize_basic.py              # STAY/SWERVE rates, heatmap
uv run python src/visualize_missing.py            # Missing data diagnostics
uv run python src/visualize_response_length.py    # Token counts, latency
uv run python src/visualize_prompt_comparison.py  # Standard vs Emphasis comparison

# Or run phases 3 + 4 in one go:
bash run_analysis.sh
```

### Runner options

```
--model     Model key (required); see llm_client.py for available models
--variant   standard | emphasis  (default: standard)
--workers   Concurrent requests (default: 3)
```

The runner is **resumable**: re-running skips already-completed scenarios and retries failed ones.

## Project structure

```
src/
  scenario_generator.py          # Phase 1: generate MM-format scenarios
  llm_client.py                  # Phase 2: OpenRouter client + model registry
  runner.py                      # Phase 2: resumable concurrent batch executor
  analysis.py                    # Phase 3: AMCE computation (weighted OLS)
  visualize_amce.py              # Forest plot, PCA moral map, radar chart
  visualize_basic.py             # STAY/SWERVE rates, per-attribute heatmap
  visualize_missing.py           # Missing data / parse failure diagnostics
  visualize_response_length.py   # Token count distributions and latency CDF
  visualize_prompt_comparison.py # Standard vs Emphasis delta heatmap and forest

data/
  scenarios.csv                          # 1300 scenarios × 2 rows each
  responses_{model}_{standard|emphasis}.csv   # LLM choices + metadata per run
  amce_{model}_{standard|emphasis}.csv        # Per-model AMCE estimates
  amce_all_models_{standard|emphasis}.csv     # Combined table (all models + human avg)

figures/
  fig5a_amce_forest.png          # Forest plot: 9 AMCE factors × all models
  fig5b_pca_map.png              # PCA of 130 countries with LLMs overlaid
  fig5c_radar.png                # Radar chart: 9 AMCE dimensions
  fig1_stay_swerve.png           # STAY/SWERVE rates per model
  fig2_preference_heatmap.png    # Per-attribute preference heatmap
  fig3_per_attribute.png         # Per-attribute bar chart
  fig_missing*.png               # Missing data diagnostics (3 figures)
  fig7a_token_distribution.png   # Output token violin+box per model
  fig7a_cot_vs_standard.png      # Token counts: standard vs Emphasis side-by-side
  fig7b_length_by_choice.png     # Token count split by STAY/SWERVE choice
  fig7c_length_by_factor.png     # Median tokens per scenario type
  fig7d_latency.png              # Latency CDF per model
  fig6a_prompt_delta_heatmap.png # Emphasis − standard AMCE delta heatmap
  fig6b_prompt_forest.png        # Side-by-side forest: standard vs Emphasis
```

## The 9 AMCE dimensions

Each estimate is the change in probability of being saved when the attribute shifts from baseline to target:

| Dimension | Contrast |
|---|---|
| Intervention | stay → swerve |
| Relation to AV | passengers → pedestrians |
| Legality | illegal crossing → legal crossing |
| Gender | male → female |
| Fitness | large → fit |
| Social Status | low → high |
| Age | elderly → young |
| No. of Lives | fewer → more |
| Species | pets → humans |

## Key findings (preliminary)

- **GPT-5.5 & Grok 4.1**: perfect Species preference (1.0) and near-perfect No. of Lives preference — more utilitarian than humans
- **Mistral Large 3**: inverted preferences on Legality, Relation to AV, Age, and Gender relative to the human global average
- **Claude Opus 4.7**: closest to human profile among tested models; nearest country = Jordan
- **GPT-5.5 & Gemini 3 Pro**: both map nearest to Denmark on the PCA moral map
- All LLMs fall outside the main human country clusters in PCA space

## Reference

Awad, E., Dsouza, S., Kim, R. et al. *The Moral Machine experiment*. Nature 563, 59–64 (2018). https://doi.org/10.1038/s41586-018-0637-6
