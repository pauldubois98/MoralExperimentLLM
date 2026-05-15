#!/usr/bin/env bash
# Run full analysis (Phase 3) and all visualizations (Phase 4) for both variants.
# Assumes LLM responses are already collected in data/responses_*.csv.

set -e
cd "$(dirname "$0")"

echo "=== Phase 3: AMCE analysis ==="
uv run python src/analysis.py
uv run python src/analysis.py --variant emphasis

echo ""
echo "=== Phase 4: Visualizations ==="
uv run python src/visualize_amce.py
uv run python src/visualize_basic.py
uv run python src/visualize_missing.py
uv run python src/visualize_response_length.py
uv run python src/visualize_prompt_comparison.py

echo ""
echo "Done. Figures saved to figures/"
