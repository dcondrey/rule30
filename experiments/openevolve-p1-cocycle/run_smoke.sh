#!/usr/bin/env bash
set -euo pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
VENDOR="$HERE/../openevolve-p3/vendor/openevolve"
PY="$VENDOR/.venv/bin/python"
OUT=${OUT:-openevolve_output_smoke}

"$PY" "$HERE/build_dataset.py"
"$PY" "$VENDOR/openevolve-run.py" \
  "$HERE/initial_program.py" \
  "$HERE/evaluator.py" \
  --config "$HERE/config_smoke.yaml" \
  --output "$HERE/$OUT" \
  --iterations 8
