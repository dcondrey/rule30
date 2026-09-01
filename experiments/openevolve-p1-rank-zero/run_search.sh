#!/usr/bin/env bash
set -euo pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
VENDOR="$HERE/../openevolve-p3/vendor/openevolve"
PY="$VENDOR/.venv/bin/python"
OUT=${OUT:-openevolve_output_search}

"$PY" "$VENDOR/openevolve-run.py" \
  "$HERE/initial_program.py" \
  "$HERE/evaluator.py" \
  --config "$HERE/config_search.yaml" \
  --output "$HERE/$OUT" \
  --iterations 18
