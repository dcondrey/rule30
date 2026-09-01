# OpenEvolve rank-zero witness search

This experiment evolves a uniform generator for hard-core endpoint prefixes.
It is a counterexample and structure-discovery probe for the remaining
rank-zero separator, not a proof search by finite exhaustion.

For every generated prefix of length `T`, the evaluator independently:

1. computes its unique inverse-terminal cut prefix;
2. appends an exact zero ray;
3. applies the exact terminal cone; and
4. records the first hard-core failure and the literal endpoint/cut witness.

The known exhaustive maxima through `T=23` calibrate the small-cutoff score.
Cutoffs `24..96` test extrapolation without enumerating the Fibonacci-sized
endpoint language.  A survival length at least `2T+2` would rigorously falsify
the proposed linear bound for that `T`; it would not establish infinite
survival or disprove the rank-zero separator.

Run with:

```bash
./run_search.sh
```

The complementary bit-level GA searches phase-slip locations directly while
using the same exact reconstruction boundary:

```bash
uv run python ga_witness_search.py --cutoffs 23 32 48 64 \
  --json ga_witness_results.json
```

Pass `--tail 2` or `--tail 3` to stress-test the two fibers isolated by the
first-infinite-tail reduction.  Its output remains finite falsifier data.  If
it finds a reusable family, the next OpenEvolve pass should search for a short
generator of that family rather than treating a width-indexed genome table as
an invariant.

Replay every retained witness independently with:

```bash
uv run python verify_results.py
```
