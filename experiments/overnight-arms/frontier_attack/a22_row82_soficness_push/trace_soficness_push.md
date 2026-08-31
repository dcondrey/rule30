# NO TRACTION (killed over budget before producing new data)

Arm a22, `experiments/overnight-arms/frontier_attack/a22_row82_soficness_push/`.
Follow-on to a10 (`../a10_trace_soficness/trace_soficness.md`), targeting Lemma U
(section 7 there): either an explicit family proving `Sigma_2(W30)` non-sofic
(U-neg) or a fixed point proving it sofic (U-pos).

## What was attempted

a10 section 6 left ten explicit pumped candidate families for (U-neg) — words
`x y^j`, `y` of length 3 — each verified to have pairwise-distinct truncated
follower sets only for `j = 1,2,3`, capped there by the exact-language window
`N = 14` (`|x| + 3j + m <= 14`). a10's own text names the next step: extend the
window to `N = 16` to reach `j = 4` for the strongest candidate
(`x=[0], y=[0,1,3], m=3`, follower sizes `20, 12, 8` at `j=1,2,3`), and separately
suggests trying to prove separation by induction on `j` via the section-3
rightward-extendability game rather than searching wider.

Two scripts were copied unmodified into this directory as `follower_table_push.py`
and `pump_search_push.py` (from a10's `follower_table.py` / `pump_search.py`,
which already contain the `N`-window logic needed; no code changes were made).
A microbenchmark of the inner `step()` loop at `N=16` (window width 32 bits,
`2^32` candidate cell-windows, chunked at `2^23`) estimated ~5-10 minutes for the
language enumeration alone. `pump_search_push.py --N 16 --rule 30 --m 3 --ylens 3
--maxj 4 --minmembers 4` was launched in the background to compute exact `L_16`
and re-run the pumping search including `j=4`.

**This run was killed on coordinator instruction before completion** (PID 47313,
~80s CPU time observed, no output yet — `language_words(16, "30")` had not
finished the full `2^32`-window enumeration). `out/pump_search_N16_y3_m3.log` is
empty (0 bytes); no JSON was written. So the benchmark estimate was optimistic
or the real cost (extraction + per-chunk `np.unique` + Python-level follower
lookups afterward, none of which the microbenchmark included) is larger than
the raw `step()` cost alone suggested. Either way: **no new numeric data was
produced.**

## Verdict

**No traction — partial setup only, no result.** Nothing in this directory
supersedes or extends a10's findings. The 492-follower-set lower bound and the
ten `j<=3`-verified pumped candidates from a10 stand unchanged.

## What would actually be needed (unchanged from a10 section 7 / obstruction H)

1. **Computational route (part a):** `L_16` (or beyond) exactly, to push the
   pumping check to `j=4` and further. Feasibility is genuinely uncertain from
   this run — the `step()`-only microbenchmark suggested ~5-10 min, but the real
   script did not finish in the time available before being killed, and the true
   per-`N` cost includes chunked deduplication and `O(4^m)` Python-level follower
   set construction per candidate family that the benchmark did not model. Even
   if `N=16` completes, it buys only `j=4` (one more family member) for the
   `|y|=3` families; `j=5` needs `N=19`, an order of magnitude more compute per
   a10's own scaling note (`2^{2N}` growth). This is a genuine "more compute"
   requirement, and moreover a finite `j` bound of any size is still not a proof
   (obstruction H): no window buys the "for all `j`" step of Lemma U-neg.
2. **Structural route (part b):** a10 section 7's real ask — prove separation of
   one of the ten candidate families by induction on `j`, using the section-3
   rightward-extendability recursion (the `Phi` operator / OR-latch pin
   structure) as the inductive engine instead of brute-force windows. This was
   not attempted here beyond reading; it requires an analytic argument (e.g. an
   explicit invariant of the automaton state reached after reading `y^j`,
   analogous to PATH.md's boundary-pin analysis for the P1 orbit problem row 55,
   but generalized from a single position to the whole rightward chain) that no
   tool call in this session produced. This is genuine unsolved-math work, not
   a compute-bound task, and is the only route that could turn any of the ten
   candidates into a real (U-neg) proof.

Nothing here rules out either candidate route; both remain exactly as open as
a10 left them, and this arm adds no evidence in either direction.

## Files

| file | status |
|---|---|
| `follower_table_push.py` | unmodified copy of a10's `follower_table.py`; never run |
| `pump_search_push.py` | unmodified copy of a10's `pump_search.py`; launched for `--N 16`, killed before completion, produced no output |
| `out/pump_search_N16_y3_m3.log` | 0 bytes |
