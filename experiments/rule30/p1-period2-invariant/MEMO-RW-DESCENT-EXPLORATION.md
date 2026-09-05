# Memo: does a minimal-counterexample descent close RW/H_r(n)?

Date: 2026-09-04. Scope: the RW-specific object `H_r(n)` from
`PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md`, not the general `BWH+`/`Delta_j`
defect (BACKLOG.md documents ~20 killed routes on that stronger object; this
memo does not retry any of them). No experiment framework was built; one
throwaway script (`scratch_peel_check.py`, not wired into the pipeline) was
run and is reported in full below.

## Verdict up front

**No natural "drop the first symbol" or "drop the last symbol of W" peel
exists for this construction.** The obstruction is structural, not a search
failure: the codebase ties the padding length to the source length itself
(`padding = 0^n` for a length-`n` word, everywhere), so shortening `W` by one
symbol necessarily also reshapes the padding, and the two changes do not
cancel. This is checked directly against the code below and confirmed
computationally: the fraction of hard-core words for which any naive
shift/truncation identity holds decays to zero as `n` grows (Fibonacci-sized
denominator, an absolute count of matches that plateaus at 7 from `n=10`
onward). `rank_zero_separator.peel_power` (the existing "Peel operator") is a
different object doing a different job and does not transplant here either,
for a distinct and more fundamental reason (see part 3).

## 1. Where a peel would have to act, read from the code

The dependency-diagonal construction used by both `literal_extension`
(`late_pull_diagonal_sat.py:254-273`) and `scale_extension`
(`constant_tail_scale.py`, just above line 205) always begins:

```python
for value in (0,) * len(word) + word:
    edge = append_dependency_edge(edge, endpoint[-1] if endpoint else None, value)
```

The comment right above this in `constant_tail_scale.py` states the reason
explicitly: *"The n inert symbols place W at absolute coordinates
n,...,2n-1. Their values are irrelevant to the forced block, but the
absolute cone orders are not."* So the padding's *length* — not its content —
is load-bearing: it is what gives `W` (and everything appended after it) its
absolute position in the diagonal recursion. This is also the origin of the
name "rotated wedge": the wedge is built symmetric, `n` zeros then `n`
source symbols, before any forced continuation begins.

`append_dependency_edge` itself (`constant_tail_scale.py:205-217`, identical
logic in `late_pull_diagonal_sat.py:append_edge` and
`peel_lift_monoid.py:append_dependency_edge`) is:

```python
following = [BOUNDARY[value]]
following.append(cone_local(previous_endpoint, following[0]))
for order in range(2, len(edge) + 1):
    following.append(cone_local(edge[order - 2], following[-1]))
```

This is causal in the fed sequence (row `k`'s edge state is a pure function
of the first `k` fed symbols and nothing later), but at each step it
recombines against the *entire* existing `edge` array, whose length equals
the whole consumed history so far. `constant_tail_scale.py`'s own docstring
states the resulting locality fact for the derived cut: *"the cut coordinate
`I(e)_t` depends only on endpoint coordinates `floor(t/2)..t`"* — a window
whose width grows linearly with `t`. There is no fixed-radius truncation
available (this matches the "Killed mechanism classes" table in
`PROOF-STATE-CAPSULE.md` section 5: fixed-radius additive energy, fixed
finite quotients, and bounded DFA rank are all killed there for the same
reason — "a growing ordered dependency diagonal stores phase in long gaps").

## 2. Why drop-first and drop-last both fail, and how each fails differently

**Drop-first.** Let `W` have length `n`. The natural length-`(n-1)` sibling
`W' = W[1:]` is fed as `0^{n-1} + W'` by the same convention. Compare this to
simply deleting the very first symbol of the *full* length-`n` feed,
`0^n + W`. These are not the same operation: deleting the first symbol of a
causal left-to-right recursion changes the *initial condition* for every
subsequent step (the first symbol of the remaining sequence now starts with
`previous_endpoint = None` instead of inheriting one), so `edge` after
`0^{n-1}+W'` is not a truncation of `edge` after `0^n+W` in general — it is a
different recursion from step 0. There is no reason to expect a shift
identity, and the check below confirms there mostly isn't one.

**Drop-last.** Here causality *does* give something for free: for the exact
same word and exact same padding, `append_dependency_edge` is a prefix
computation, so running it on `seq[:-1]` reproduces the *same* leading run of
`edge` states as running it on `seq`. But this only helps if the padding
length is held fixed. The moment you also drop a source symbol to get to a
length-`(n-1)` instance, the convention forces the padding down to `0^{n-1}`
too, which reintroduces the same first-symbol-shift problem as above (one
fewer leading zero shifts every "absolute cone order" downstream by one).
So drop-last inherits a free identity only for the wrong comparison (same
`n`, shorter feed) and loses it again once `n` itself is decremented.

## 3. Check against the throwaway script

`scratch_peel_check.py` (repo root of this directory, not part of the
pipeline) builds `edge` via `append_dependency_edge` — the real function,
unmodified — for every hard-core word of length `n` (via
`rank_zero_separator.hard_core_prefixes`, `n = 2..12`, both drop-first and
drop-last), and asks: does the shorter word's `edge` array equal an anchored
(not "found anywhere") segment of the longer word's `edge` array — trailing
segment for drop-first, leading segment for drop-last (the two positions
where a real identity would plausibly land, matching the causal argument in
part 2)? Output:

```
n= 2 hard-core-words=    3 anchored-trailing-match(drop-first)=    0 anchored-leading-match(drop-last)=    0
n= 3 hard-core-words=    5 anchored-trailing-match(drop-first)=    1 anchored-leading-match(drop-last)=    1
n= 4 hard-core-words=    8 anchored-trailing-match(drop-first)=    1 anchored-leading-match(drop-last)=    1
n= 5 hard-core-words=   13 anchored-trailing-match(drop-first)=    2 anchored-leading-match(drop-last)=    1
n= 6 hard-core-words=   21 anchored-trailing-match(drop-first)=    3 anchored-leading-match(drop-last)=    3
n= 7 hard-core-words=   34 anchored-trailing-match(drop-first)=    3 anchored-leading-match(drop-last)=    3
n= 8 hard-core-words=   55 anchored-trailing-match(drop-first)=    4 anchored-leading-match(drop-last)=    3
n= 9 hard-core-words=   89 anchored-trailing-match(drop-first)=    7 anchored-leading-match(drop-last)=    4
n=10 hard-core-words=  144 anchored-trailing-match(drop-first)=    7 anchored-leading-match(drop-last)=    7
n=11 hard-core-words=  233 anchored-trailing-match(drop-first)=    7 anchored-leading-match(drop-last)=    7
n=12 hard-core-words=  377 anchored-trailing-match(drop-first)=    7 anchored-leading-match(drop-last)=    7
```

The hard-core population grows like Fibonacci (matches the known count in
`rank_zero_separator.hard_core_prefixes`, also cited in BACKLOG.md's
L10-FIB-TRANSFER row), but the absolute count of words for which either
naive shift identity holds *stops growing* at `n=10` (plateaus at 7 for both
directions through `n=12`). So the fraction with any such identity is
already heading to zero, exactly as the structural argument in part 2
predicts: the identity is not false everywhere (a handful of exceptional,
presumably highly-structured words satisfy it by coincidence — plausibly the
same near-constant/checkerboard-like words flagged elsewhere in the archive
as exceptional, e.g. BACKLOG.md's "source-bit-haar-coefficient-decay" and
"periodic-source-defect-oscillation" rows), but it is not a law usable for
induction on generic `W`.

## 4. Why `rank_zero_separator.peel_power` does not transfer either

`rank_zero_separator.peel` (`rank_zero_separator.py:24-27`) is:

```python
def peel(values):
    return tuple(cone_local(values[index], values[index + 1]) for index in range(len(values) - 1))
```

This is a *spatial* contraction of an already-fixed endpoint snapshot
(`values`), shrinking a length-`L` row to length-`L-1` by combining adjacent
pairs — it is literally one step of the forward inverse-cone triangle
(matches `PROOF-STATE-CAPSULE.md`'s "Rotated Peel identity" `P(I(sigma
e))=sigma^2 I(e)`). It operates on the *time/rank* axis of an endpoint
sequence that is already given in full, and is used (per the capsule,
section 1 and section 4's "Rank descent" row) to reduce an *infinite*
endpoint's dependency rank down to rank zero — a different reduction on a
different object (the endpoint tail's asymptotic structure), not a
reduction on the *length of the finite source word* `W` that indexes
`H_r(n)`. There is no step in `H_r(n)`'s definition that hands you a
pre-built endpoint snapshot to peel spatially; the object under induction
here is `n` itself, entering through the padding-coupling described in part
1, which `peel`/`peel_power` never touches. Applying it would require first
solving exactly the open problem this memo is about (an `n`-to-`n-1`
reduction) to get an endpoint snapshot in the right shape to peel — it
cannot substitute for that step.

Additionally, `PROOF-STATE-CAPSULE.md` section 5 records, under "One
backward source defect": *"single-coordinate four-state relaxations usually
remain UNSAT; the obstruction is branched/global,"* and under "Actual-right
constraints only after finite prefixes": *"Rank descent prepends artificial
endpoint 2s, so conditioning the entire endpoint on actual-right
realizability is unsound."* Both are direct, already-recorded warnings
against exactly the move this memo tested (treat a shortened/modified
endpoint prefix as validly representing a shorter real instance) — this
memo's finding is a source-word-level, RW-specific instance of that same
already-diagnosed unsoundness, not a new failure mode.

## 5. Bottom line for the descent program

A minimal-counterexample argument of the classic shape (assume shortest `W`
survives, produce a shorter survivor, contradict minimality via the known
empty base cases through `n=13`/`n=29`) needs a *reduction lemma*: some map
`W -> W'` with `|W'| < |W|` that provably preserves membership in the
relevant survivor set. This memo's finding is that the two most obvious
candidate maps — dropping the first symbol, dropping the last symbol —
are not such reductions for this construction, because the codebase's own
`n`-vs-padding coupling makes both maps change the recursion's absolute
frame of reference, not just truncate it. This was verified against the
actual `append_dependency_edge`/`literal_extension` code (not a
reimplementation) and against a direct computation (part 3), and is
independently consistent with two already-recorded warnings in
`PROOF-STATE-CAPSULE.md` section 5. It is a negative finding specific to the
"drop a boundary symbol of W" reduction shape; it does not rule out a
different reduction (e.g. one that also re-derives a compensating padding
change, or one phrased on the endpoint/cut coordinate `e` rather than on
`W`), which would be a different, unexplored proposal, not a retry of this
one under a new name.
