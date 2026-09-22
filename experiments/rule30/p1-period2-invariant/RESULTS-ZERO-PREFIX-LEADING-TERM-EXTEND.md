# Zero-prefix greedy lemma: extended empirical horizon, no proof

Date: 2026-09-06

Status: **THE ZERO-PREFIX GREEDY LEMMA (RESULTS-SCALE-TELESCOPING.md sec.5)
REMAINS UNPROVED.  NO COUNTEREXAMPLE WAS FOUND.  THE EXHAUSTIVE HORIZON
MOVES FROM LENGTH 22 TO LENGTH 23, AND STRUCTURED-ADVERSARIAL PLUS RANDOM
SAMPLING NOW COVER WORDS UP TO LENGTH 2000 WITH ZERO FAILURES.  THIS
STRENGTHENS CONFIDENCE IN THE LEMMA; IT DOES NOT PROVE IT, AND THE PROOF
GAP IDENTIFIED IN SECTION 6 OF RESULTS-SCALE-TELESCOPING.MD IS UNTOUCHED.**

Evidence level: `K` (finite census, now broader; no new proof machinery).

**Follow-up 2026-09-06:** the proof target has since been weakened. The greedy
statement is not what `(1)` needs; the per-row claim `max S_j >= j` suffices and
is strictly implied by it (`RESULTS-ZERO-PREFIX-GREEDY-REDUCTION.md`). Section 5
below is still accurate about the greedy lemma itself. That doc also records
why the large-`n` random axis used here is weak evidence: at `n >= 100` the
hard-core continuation dies within a row or two, so those words never approach
the bound.

## 1. Preregistration (recorded before running)

- Task: does the deterministic zero-prefix greedy frontier (RESULTS-SCALE-
  TELESCOPING.md eq. 6) miss any nonfinal hard-core survival row, for tail
  `c in {2,3}`? Does it miss the final row for tail 2? (Tail 3 may miss only
  its own final row, per `PREREGISTRATION-ZERO-PREFIX-FINAL-MISS.md`.)
- Metric: `greedy_failures` (greedy total < survival length) and
  `nonfinal_miss_failures`, computed with the same, unmodified
  `zero_prefix_bitsliced_graph` / `greedy_matching` functions already
  verified in `constant_tail_zero_prefix_bitsliced.py` — no new graph
  definition is introduced, since a new graph would be a new, unverified
  claim rather than an extension of the frozen one.
- Kill condition: any word `W` with `greedy_failures>0` for tail 2, or any
  nonfinal miss for either tail. A hit would name the word, tail, survival
  length, and missed row(s).
- Disconfirming result would print a `FAIL`/`KILL CONDITION FIRED` line
  naming a concrete word.
- This was **not** guaranteed to pass: the closely related pointwise
  derivative certificate broke at length 21 after holding through length 16
  (RESULTS-SCALE-TELESCOPING.md sec.2), so a break in the greedy
  construction at a length beyond 22, or at a much larger random/adversarial
  length, was a live possibility, not a foregone conclusion.
- Growth rate noted in advance: hard-core words (alphabet `{1,2}`, no `11`)
  of length `n` number `Fib(n+2)`, so exhaustive cost grows like
  `1.6^n`, and the per-word bit-sliced cost is empirically `~O(n^2)`
  (measured: `n=100` -> 0.02s, `n=300` -> 0.22s, `n=1000` -> 3.1s per
  tail). This bounds how far pure exhaustion and how large a random `n`
  can go in a reasonable session, and was used to size the sweeps below
  (a first attempt at `scaled-max-run=500` / uniform 300 trials up to
  `n=5000` was killed after nearly an hour with no result — recorded as a
  dead end in section 4).

## 2. What ran

Reused, unmodified: `zero_prefix_bitsliced_graph`, `greedy_matching`,
`correction` from `constant_tail_zero_prefix_bitsliced.py` /
`constant_tail_zero_prefix_matching.py`. New driver:
`zero_prefix_leading_term_extend.py`, three independent probes.

**(1) Exhaustive continuation.** Time-boxed re-derivation from length 1
(as a control replicating the documented length-1..22 census) through as
far as a fixed time budget allowed.

**(2) Scaled structured adversarial families.** The three known
sharp/adversary words from `RESULTS-SCALE-TELESCOPING.md` (`121` for tail
3; the tail-2 repair word `12212121212121212`; the length-21 derivative
adversary `122212222222221212122`) are scaled by extending exactly the run
that made each one sharp — these are the patterns that broke *other*
certificates (pointwise derivative, fixed selector) at small length, so
they are the structurally motivated place to look for a greedy failure,
per the project's discipline of testing structure titled to catch the
effect rather than generic words.

**(3) Random hard-core words at large `n`.** Non-uniform but valid
hard-core generator (forbids `11`), many trials per length, `n` up to
2000.

## 3. Results

Exhaustive (new territory only; lengths 1-22 replicate the documented
242,783-case census exactly and are not re-claimed as new):

```text
length=23  cases=150,050  failures=0   (154.22s at that length; cumulative 555.65s)
time budget (420s) exceeded after length 23 -> sweep stopped there
```

Scaled adversarial families (`--scaled-max-run 60`, run lengths growing to
135):

```text
families: cases=480  max_length_seen=135  failures=0
```

Random sampling (both tails, per length):

```text
n=   50  trials=300  failures=0
n=  100  trials=300  failures=0
n=  200  trials=300  failures=0
n=  500  trials= 40  failures=0
n= 1000  trials= 15  failures=0
n= 2000  trials= 15  failures=0
```

Total new cases checked beyond the documented length-22 horizon:
150,050 (exhaustive, length 23) + 480 (families, up to length 135) +
1,940 (random, up to length 2000) = **152,470 new cases, 0 failures**.

No `greedy_failures`, no `nonfinal_miss_failures`, in any probe.

## 4. A dead end worth recording

The first attempt used `--scaled-max-run 500` and a uniform 300 trials
per length including `n=5000`. Since the bit-sliced check cost is
`~O(n^2)` at the Python-loop level (not just bigint width), this pushed
total cost past `~10^9` word-checks worth of work; the run was still stuck
in the families phase after 57 minutes of CPU time and was killed. The
corrected run split the random sweep by length with trial counts scaled
down as `n` grows (300 trials at `n<=200`, 40 at `n=500`, 15 at
`n in {1000,2000}`) and capped the adversarial-family run length at 135.
Anyone extending this further should budget `~O(n^2)` per word, not assume
the exhaustive script's per-word cost is `O(n)`.

## 5. Reading the evidence honestly

This is a horizon extension, not a proof, and only a modest one on the
exhaustive axis (22 -> 23, limited by the same combinatorial explosion that
stopped prior sessions, not by anything new). Its actual value is the two
new axes: structured scaling of the exact words known to break related
(but distinct) certificates, and random sampling three orders of magnitude
past the exhaustive horizon. Neither found a counterexample. That is
consistent with — but does not establish — the truth of the lemma; a
monotone counting bound of this kind can hold on every sampled/adversarial
instance up to some length and still fail on a rare structured word this
sweep did not construct (the pointwise-derivative certificate's own history,
passing 13,526 registered cases through length 16 before breaking at length
21, is the concrete precedent for exactly this failure mode, cited in
RESULTS-SCALE-TELESCOPING.md sec.2).

No progress was made on option (a), the ordered finite-difference / Peel-
leading-term proof direction named in RESULTS-SCALE-TELESCOPING.md sec.6.
That gap is untouched: this work only ran probes (b)/(c) — extend
verification and hunt for a counterexample — per the pre-registered,
cheapest-first plan. The lemma is neither more nor less alive on the proof
axis than before; it is more empirically supported on the counterexample
axis.

## 6. Reproduction

From `13-rule30/`:

```bash
# exhaustive continuation from length 1, time-boxed at 420s (reaches ~length 23)
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/zero_prefix_leading_term_extend.py \
  --exhaustive-first 1 --exhaustive-last 40 --exhaustive-time-budget 420 \
  --skip-families --skip-random

# scaled adversarial families up to run length 60 (word length ~135)
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/zero_prefix_leading_term_extend.py \
  --skip-exhaustive --skip-random --scaled-max-run 60

# random sampling, small/medium n
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/zero_prefix_leading_term_extend.py \
  --skip-exhaustive --skip-families \
  --random-lengths 50 100 200 --random-trials-per-length 300

# random sampling, large n (scale trials down as n grows -- see sec.4)
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/zero_prefix_leading_term_extend.py \
  --skip-exhaustive --skip-families --random-lengths 500 --random-trials-per-length 40

PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/zero_prefix_leading_term_extend.py \
  --skip-exhaustive --skip-families --random-lengths 1000 2000 --random-trials-per-length 15
```

Each invocation prints a `=== SUMMARY ===` block; `KILL CONDITION FIRED`
would name the failing word if the lemma broke. None did.
