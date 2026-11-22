#!/usr/bin/env bash
# Run the PaperOrchestra pipeline on one paper built from this repo.
#   paperorchestra/run.sh [paper_id] [extra paper_writing_cli.py args...]
# Output goes to paperorchestra/output/<paper_id>_<timestamp>/ (final_paper.pdf at the top).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PAPER_ID="${1:-symmetry-convergence}"; shift || true
PO="$HERE/paper-orchestra"
MAT="$HERE/raw_materials/$PAPER_ID"

python3 "$HERE/build_materials.py" "$PAPER_ID"   # always rebuild from program/data

TEMPLATE="$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('template','iclr2025'))" "$MAT/paper.json")"

if [ -f "$HERE/.env" ]; then set -a; . "$HERE/.env"; set +a; fi
if [ -z "${GEMINI_API_KEY:-}" ] && [ -z "${VERTEX_AI_PROJECT:-}" ] && [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "No LLM credentials: set GEMINI_API_KEY (or VERTEX_AI_PROJECT/LOCATION, or OPENAI_API_KEY) in $HERE/.env" >&2
  exit 1
fi

OUT="$HERE/output/${PAPER_ID}_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"
cd "$PO"   # the pipeline imports methods/ and utils/ relative to its own root
PYTHONUNBUFFERED=1 "$HERE/.venv/bin/python" paper_writing_cli.py \
  --raw_materials_dir "$MAT" \
  --latex_template_dir "$PO/templates/$TEMPLATE" \
  --output_dir "$OUT" \
  --idea_filename idea_dense.md \
  --experimental_log_filename experimental_log.md \
  --research_cutoff "${RESEARCH_CUTOFF:-$(date +%Y-%m)}" \
  --use_plotting false \
  "$@" 2>&1 | tee "$OUT/run.log"
echo "Output: $OUT"
