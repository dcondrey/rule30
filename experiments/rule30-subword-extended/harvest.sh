#!/bin/sh
# harvest.sh -- run the factor-complexity analysis over a ladder of prefix
# lengths of the generated bitstream, producing the p(n) tables and the
# L(N) / max-p(N) curve. The generator writes incrementally, so this can be
# run against a partially complete stream at any time.
#
# Usage: ./harvest.sh <bitstream.bin> <outdir>
set -e
BIN="$1"
OUT="${2:-.}"
mkdir -p "$OUT"
BITS=$(( $(wc -c < "$BIN") * 8 ))
echo "stream currently holds $BITS bits"
for N in 1000000 2000000 4000000 8000000 16000000 25000000 33000000 41000000 50000000 67000000 84000000 100000000; do
    [ "$N" -le "$BITS" ] || continue
    ./analyze "$BIN" "$N" > "$OUT/p_N${N}.json" 2>/dev/null
    printf '%s\n' "$N $(grep -o '"max_p_n": [0-9]*' "$OUT/p_N${N}.json") $(grep -o '"longest_repeated_factor_L": [0-9]*' "$OUT/p_N${N}.json") $(grep -o '"all_n_1_to_64_exceed_n": [a-z]*' "$OUT/p_N${N}.json")"
done
# full-stream run
./analyze "$BIN" > "$OUT/p_full.json" 2>/dev/null
echo "full: $(grep -o '"prefix_length": [0-9]*' "$OUT/p_full.json") $(grep -o '"max_p_n": [0-9]*' "$OUT/p_full.json") $(grep -o '"longest_repeated_factor_L": [0-9]*' "$OUT/p_full.json")"
