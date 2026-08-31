#!/bin/zsh
# One sealed-commitment tournament per n-point; fuel is the effort proxy and the
# exponent is fitted across points, so a single point is never the decision.
set -e
LAB=/Volumes/C/rust-target/debug/crosstalk-lab
for N in "$@"; do
  HI=$((N + 64))
  uv run python make_band.py $N $HI 30 64 >/dev/null
  C=$($LAB commitment --hidden-tests hidden-$N-$HI.json)
  uv run python -c "
import json; p='challenge-$N-$HI.json'; d=json.load(open(p)); d['hidden_test_commitment_sha256']='$C'.strip(); json.dump(d,open(p,'w'),indent=2)"
  rm -f report-$N-$HI.json
  $LAB run --challenge challenge-$N-$HI.json --hidden-tests hidden-$N-$HI.json \
    --baseline naive.wasm --candidate bitparallel=bitparallel.wasm \
    --fuel 100000000000 --timeout-secs 1800 --output report-$N-$HI.json
  echo "done $N"
done
