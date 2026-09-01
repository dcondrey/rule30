#!/bin/zsh
# a25: analysis pipeline for one band file.  usage: ./pipeline.sh BAND.bin TAG J
set -e
cd "$(dirname "$0")"
BAND=$1; TAG=$2; J=${3:-32}
uv run python analyze.py "$BAND" "analysis_${TAG}.json" --windows "$J"
uv run python report.py "analysis_${TAG}.json" --json "report_${TAG}.json" \
  > "report_${TAG}.txt" 2>&1
echo "wrote report_${TAG}.txt"
