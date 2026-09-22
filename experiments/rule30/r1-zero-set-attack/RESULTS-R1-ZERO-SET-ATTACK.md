# R1 zero-set attack: reconciling the R7 ladder's p=2 witnesses against the rotated-wedge census

Date: 2026-09-04. Directory: `experiments/rule30/r1-zero-set-attack/` (new).
All files below are new; no existing `.py`/`.md` file
anywhere in the repo was edited. `docs/rule30/PATH.md`,
`docs/rule30/RESULTS-ladder-rung0.md`, `docs/rule30/RESULTS-ladder-rung1.md`,
and everything read under `experiments/rule30/p1-period2-invariant/` were
read-only.

**Verdict up front: R1 (route "close the zero-set obligation", PATH.md
section 4, register row 1) stays OPEN. No kill condition fired. What this
document adds is not a resolution but a mechanism-level account of why two
results, produced by structurally different models, cannot be read against
each other (they were never actually in tension, only easy to mistake for
being so -- section 8 corrects that framing precisely), plus one corrected
citation and one flagged discrepancy, now with two candidate explanations,
for whoever owns the other thread.**

## 0. Task history, honestly stated

This investigation started on the general R1 attack (read `PATH.md` section 1-4 in
full, cross-checked `RESULTS-eventual-period.md`/`inverse_trace_probe.py`
provenance, built `substrate.py` -- a driven-quarter-plane simulator,
verified against the repo's ground-truth generator and against a genuine
two-sided diagram on a strip, both rules). It was then redirected to a
sharper, higher-value target: reconcile the R7
omega-automaton ladder's NONEMPTY p=2..8 witnesses (`docs/rule30/PATH.md`
section "R7", `RESULTS-ladder-rung0.md`, `RESULTS-ladder-rung1.md`) against
the independent `p1-period2-invariant` thread's exhaustive rotated-wedge
(RW/DLP) census, which reports **zero** candidates for its own specific
period-2 construction (a narrower statement than "zero period-2
configurations" -- section 8 Correction 1 makes this precise; treat this
sentence as the imprecise version being corrected, not the standing claim).
Sections 1-6 below are that reconciliation, which is where the majority of
verified, decisive content in this report lives. `substrate.py` is included for
completeness (it is correct and cross-validated) but the follow-on
experiments planned for it (a run-length structure theorem for `r` under
periodic `c`, an induced-period-vs-width sweep) were superseded by the
redirect and are listed as unfinished in section 9, not executed.

## 1. The exact objects, restated precisely (not paraphrased)

`PATH.md` section 2, in the repo's own notation: `c_t = s(t,0)`,
`l_t = s(t,-1)`, `r_t = s(t,1)`. The pin identity (an unconditional Rule 30
fact, re-verified throughout this tree, e.g. `RESULTS-ladder-rung1.md`
section 1, 80,243 antecedents / 0 violations to `T=400`):

```text
s(t,x) = 1  =>  s(t,x-1) = NOT s(t+1,x)
```

At `x=0` this gives `l_t = c_{t+1} XOR (c_t OR r_t)`, hence

```text
c_t = 1  =>  l_t = 1 XOR c_{t+1}                    (free from c alone)
c_t = 0  =>  l_t = c_{t+1} XOR r_t                  (needs r)
```

so, **assuming `c` eventually periodic**: `l` eventually periodic
`<=>` `r` restricted to `Z = {t : c_t = 0}` eventually periodic. Call this
implication **(star)**. `l` eventually periodic contradicts Jen 1990
Prop. 3 / Kopra TCS 946 (2023) 113668 Thm 3.5 (width-2 column never
eventually periodic for any nonzero finite seed), which is the whole reason
(star) matters: proving it closes P1. `PATH.md`'s stated kill condition for
route R1: exhibit a diagram (or consistent formal model of one) with `c`
eventually periodic and `r` provably aperiodic on `Z`; **or**, if the
zero-set obligation is not decidable from `c` alone, R1 dies and the
rightward cascade (R2, already independently killed) is the fallback.

## 2. What the R7 ladder actually tests (read from `ladder.py`/`rung1.py`, not summarized from prose)

`experiments/rule30/ladder/ladder.py` reads an infinite letter stream over
`{0,1,2,3}`, each letter packing `(col_{R-1}(t), col_R(t))`. **At `R=1` the
letters ARE `(c_t, r_t)` directly** -- this is not incidental, and it is
the sharpest available restatement of obstruction F (`PATH.md` 7.3.F):

- For `R=1`, the model's *only* free input is the `(c,r)` pair itself, and
  the boundary pin (`rung1.py`'s `pin_ok`, exactly Lemma 1 of
  `RESULTS-ladder-rung1.md`: `col_R(t)=1 => col_{R-1}(t) = NOT col_R(t+1)`)
  binds **directly on `r`** -- it is exactly the real pin identity from
  section 1 above, applied at `x=1`.
- For `R>=2`, the letters are `(col_{R-1}, col_R)`, i.e. the free pair
  moves one column further right, and the *single* pin constraint the model
  imposes binds at that new outermost pair -- **not** at `r` again. Larger
  `R` does not add cumulative structure at `r`; it relocates the one
  constraint outward and leaves `r` at least as free as before.

This is a sharper reading of `RESULTS-ladder-rung1.md` Corollary 2/3
(`plain(R+1) subset pin(R) subset plain(R)`, "the pin buys strictly less
than one column of depth") than "the outermost column is free": it pins
down *which* column carries the model's one real constraint at each `R`,
and explains from the encoding itself -- not only from the measured
`~R^2.75` vs `4^R` growth -- why rung 0/1 found the verdict uniform in `R`
and `k`.

Everything beyond column `R` (in particular, for `R=1`, all of column 2 and
beyond) is **entirely unmodelled**. That is obstruction F, `PATH.md` 7.3.F,
already named and proved (`plain(R+1) subset pin(R) subset plain(R)`); this
document's contribution is pinning it to the specific column at `R=1` and
then measuring exactly how much freedom that leaves, in section 3.

## 3. An explicit p=2 witness, extracted and independently re-verified

`extract_r7_witness.py` imports `experiments/rule30/ladder/{ladder,rung1}.py`
**read-only** (`importlib`, no edits, matching how `a21`/`a7` cross-imported
`overnight-arms/common`) and calls the existing, unmodified
`rung1.decide_pin` at rung 1's own smallest documented pin-NONEMPTY case:
`R=1, k=2, w=(0,1), q=1, pin=True` (`RESULTS-ladder-rung1.md` section 3,
table row `R=1`, pin states 224).

```text
states=224, verdict=NONEMPTY, witness independently re-verified by
  ladder.verify_witness: onset=5
prefix = [2, 3, 0, 2, 2, 0, 2]
cycle  = [1, 3, 0, 2, 0, 2]           (length 6)
c (col 0): 1101101010101010101010101...
r (col 1): 0100000110000110000110000...
l (col -1): 0110111011111011111011111...
```

(Letters decode as `(c,r) = (letter>>1, letter&1)`; e.g. prefix letter `2 =
0b10` is `(c,r)=(1,0)`, matching the printed arrays.)

**`witness_column2_uniqueness.py`** then asks, from scratch, using nothing
but the raw local rule `r_{t+1} = c_t XOR (r_t OR s(t,2))` at `x=1` (no
reuse of `ladder.py`'s own verification logic beyond generating the
witness):

- At every `t` in the cyclic tail with `r_t = 1`: does **both**
  `s(t,2) = 0` and `s(t,2) = 1` reproduce the witness's actual `r_{t+1}`?
- At every `t` with `r_t = 0`: does **exactly one** value of `s(t,2)`
  reproduce it?

```text
witness R=1 k=2 w=(0,1) q=1: verified=True (onset=5)
cells with r_t=1 (claimed FREE at column 2): 16, violations: 0
cells with r_t=0 (claimed FORCED at column 2): 31, violations: 0
CONCLUSION: confirmed -- genuine 2-way freedom at every r_t=1 cell,
genuine forcing at every r_t=0 cell
```

So in this one concrete, ladder-verified, pin-satisfying witness, **34% of
the cells in the cyclic tail require column 2 to be a genuinely free,
two-valued choice** for the witness's own `(c,r)` pattern to be achievable
at all via the real Rule 30 rule (this is forced by the OR saturating at
`r_t=1`, not an artifact of the bookkeeping here -- both values of `s(t,2)`
algebraically give the same `r_{t+1}`). `extract_r7_witness.py` repeats the
same accounting at `R=2` (letters `(r, col 2)`, so the free pair moves out
by one column as predicted in section 2): 24 of 47 cells free over the
cyclic tail. (`extract_r7_witness.py`'s own default `reps=6` prints this as
12/35 at `R=1` -- the same ~34% steady-state density, just fewer repeats of
the length-6 cycle than `witness_column2_uniqueness.py`'s `reps=8`, which is
what the 16/47 figure above is; both scripts' numbers are reproducible
exactly as printed and agree in ratio.) The freedom does not shrink when the
model is pushed one column deeper, consistent with rung 0/1's own "depth
does not tighten" finding, now located at the specific cells responsible
for it.

**This is not yet a claim that the witness is unrealizable.** It is a
quantified demonstration of exactly what freedom the witness's own
construction requires and where. Whether that freedom can be sustained
forever under full recursive Rule 30 consistency (i.e. whether the witness
is *realizable* by an actual configuration extending arbitrarily far right)
is precisely rung 1's own named open gap ("realizability... is not [in
hand]. That is the next target.") and is not resolved here either.

## 4. What the rotated-wedge (RW/DLP) census enforces that the ladder does not

`experiments/rule30/p1-period2-invariant/late_pull_diagonal_sat.py`
(`literal_extension`) and `constant_tail_scale.py`
(`append_dependency_edge`), read read-only:

```python
# literal_extension, late_pull_diagonal_sat.py:254-273 (abridged)
for _ in range(rows):
    candidates = []
    for value in range(4):
        following = append_dependency_edge(edge, endpoint[-1], value)
        if following[-1] == tail:
            candidates.append((value, following))
    assert len(candidates) == 1          # <-- zero freedom, every step
    value, edge = candidates[0]
```

```python
# append_dependency_edge, constant_tail_scale.py:205-218 (abridged)
following = [BOUNDARY[value]]
following.append(cone_local(previous_endpoint, following[0]))
for order in range(2, len(edge) + 1):
    following.append(cone_local(edge[order - 2], following[-1]))
return tuple(following)                  # edge GROWS by one entry per call
```

Two facts, both checked directly rather than taken from the surrounding
prose:

1. **`assert len(candidates) == 1` is not an incidental property of this
   particular search -- it is guaranteed by construction.**
   `cone_local(left, right) = INVERSE[swap(left)][right]`, and `INVERSE` is
   the functional inverse of `FORWARD`, which is built from
   `carry_action(symbol, state)`. Checked directly (not merely read) that
   `carry_action(symbol, .)` is a bijection on `{0,1,2,3}` for every fixed
   `symbol in 0..3`:

   ```text
   symbol=0: [0,1,3,2]  bijection
   symbol=1: [2,3,1,0]  bijection
   symbol=2: [3,2,1,0]  bijection
   symbol=3: [3,2,1,0]  bijection
   ```

   Composing bijections stays a bijection, so requiring the far end of the
   (arbitrarily long, growing) `edge` to hit a prescribed `tail` value picks
   out a unique new input symbol at every single step, all the way out.
   There is no point in this recursion where a fresh, uncorrelated bit is
   introduced.
2. **`edge` has no fixed width.** It grows by exactly one entry every time
   `append_dependency_edge` is called (`len(edge)+1` iterations of the
   inner loop), so it is tracking the *entire* accumulated dependency
   frontier, not a small fixed window like the ladder's `[x_min, R]`.

## 5. The reconciliation

The two searches are answering different, non-contradictory questions,
and the difference is exactly located, not merely asserted:

| | R7 ladder (mode ii) | RW/DLP census (`literal_extension`) |
|---|---|---|
| object | fixed-width window `[x_min, R]`, `R,k` small (<=9, state-count wall) | growing frontier `edge`, width = symbols processed so far, unbounded |
| freedom | outermost letter pair chosen **freely at every future time step**, forever (one real pin constraint applied once, at whichever column is currently outermost) | **zero** free bits anywhere (`assert len(candidates)==1` at every step, guaranteed by `carry_action`'s per-symbol bijectivity) |
| verified numerically here | 16/47 (`R=1`) and 24/47 (`R=2`) cells of the p=2 witness's own cyclic tail require genuine two-valued freedom at the next unmodelled column | N/A by construction -- there is no cell where two continuations are both consistent |
| finding | NONEMPTY at every checked `p in 2..8`, `R<=7..9` (rung 0/1) | `|H_r(n)|=0` exhaustively `n=1..16`; RW UNSAT by complete SAT `n=21..28`, `r=0`, both `c` (`BACKLOG.md` section 12) |

**So the results do not conflict.** The R7 witnesses are constructions that
*use* a freedom (an unconstrained column immediately beyond the modelled
window) that the census's construction structurally cannot contain, by the
census's own design: every one of its continuation symbols is the unique
value forced by the *entire* history so far, with no window truncation
anywhere. A witness built by injecting fresh unconstrained information at a
fixed, finite distance from the centre is not the kind of object the census
searches over at all, so its absence from the census is not evidence
against the witness, and the witness's existence is not evidence against
the census's exhaustive zero. Obstruction F (`PATH.md` 7.3.F) already
predicted this in general terms ("any fixed-depth strip leaves its
outermost column under-constrained"); sections 2-4 above pin it to (a) the
specific column at each `R`, (b) an explicit, ladder-verified, from-scratch
re-verified numeric instance of the freedom (16/47, 24/47 cells), and (c) an
explicit, code-level proof of why the census's own construction cannot
contain the analogous freedom (per-symbol bijectivity of `carry_action`,
checked directly).

**What this does NOT establish**, stated as plainly as the tree's own
convention requires:

- It does **not** show the R7 p=2 witnesses are unrealizable by any actual
  Rule 30 configuration. That is exactly rung 1's open "realizability"
  question, and it is exactly as open now as before this analysis.
  Showing a construction *requires* freedom the census forecloses is not
  the same as showing that freedom can never be filled in consistently to
  infinity.
- It does **not** extend the census's own `n<=28` (SAT) / `n<=16`
  (exhaustive `H_r`) horizons, and does not attempt to, per the redirect's
  instruction to reconcile rather than to re-run either side's compute.
- It is specific to **period 2** on the census side: the RW/DLP machinery
  (`rotated_wedge_population`'s `12a`-terminal / hard-core checks) is built
  around the alternating-phase target (`PROOF-STATE-CAPSULE.md`: "the
  opposite alternating phase shifts to `0101...`, so only that phase
  remains"), i.e. it is PT2-specific, not a general-`p` construction the
  way the ladder's `period_word` parameter is. This reconciliation says
  nothing about whether the same free-column mechanism is or is not present
  in the `p=3..8` witnesses relative to *some* equally strict finite
  construction for those periods -- none is known to exist in this repo.

## 6. One correction and one flagged discrepancy

**Correction (an earlier brief cited `n=24`; the source says otherwise,
re-verified against the actual files rather than repeated):**

- `experiments/rule30/p1-period2-invariant/BACKLOG.md` section 12: RW by
  complete SAT is **UNSAT for `n = 21..28`**, `r=0`, both `c`, solve times 14s
  to 27 min ("The RW census therefore stands at `n = 28` for `r = 0`").
- `RESULTS-RW-TERMINAL-DEFECT-H-POPULATION.md`: the *exhaustive* (not SAT)
  population check `|H_r(n)| = 0` for every `n = 1..16`, `r in {0,1,2}`, both
  `c` -- a necessary-only, weaker-but-exhaustive statement, explicitly not
  yet extended past 16 (extension to `n=18` costed at ~2 hours, not run as
  of that document).
- Both are explicitly flagged by their own authors as bounded-horizon
  results (obstruction H, `PATH.md` 7.3.A/H): not all-`n` proofs.

**Discrepancy, flagged for whoever owns `p1-period2-invariant/uc/r1-r1zero/`,
not resolved here:** `RESULTS-R1-ZERO-SET-INVENTORY.md` (dated today,
2026-09-04, in the directory treated as read-only here) reports,
for the *driven right-half-plane* model (`driven_halfplane.py`,
`drive01_deep.py` -- a direct forward simulation with `c` clamped to a
periodic word, a different model from the ladder's omega-automaton, see
below): `r|Z` eventually periodic in 10/44 (word, prefix) drives, but `l`
(column -1) eventually periodic in **0/44**. By the exact identity in
section 1 (`l_t` is a pointwise XOR/complement of `c_{t+1}` and `r_t`), `l`
should inherit eventual periodicity whenever both `c` and `r|Z` have it, so
naively 10/44 and 0/44 look inconsistent. Two candidate explanations, neither
verified here, and this report resolves neither:

1. A period-bound accounting mismatch: a period found for `r` in
   zero-set-rank-space, or with a generous search bound, need not fall
   within whatever bound was separately searched for `l` in literal-time
   space.
2. An onset-detection artifact of exactly the kind independently
   found in section 8's sibling analysis: `sampler_validity.py`
   reports Rule 30 `w=01` committing at "onset 298" on a 300-letter word,
   which that analysis calls explicitly "the trivial end-of-word artifact,
   i.e. no onset -- as it must be." A harness that can mistake
   end-of-search-window for a found onset in one direction is a plausible
   candidate for reporting a spurious "periodic" verdict for `r|Z` while
   correctly reporting "not periodic" for `l` under a stricter or
   differently-windowed check -- i.e. the 10/44 figure may itself be
   partly this artifact, independent of any rank-vs-literal-time accounting
   issue in explanation 1.

Both are named rather than adjudicated: **this is not verified here** -- it
costs one short script against `driven_halfplane.py`/`r1zero_lib.py`, and
since those files belong to a directory not written to here, it is
reported as an open flag rather than chased. Do not read this report as
having resolved it either way.

## 7. Convergent, independent evidence (not a scoop, not duplicated work)

`RESULTS-R1-ZERO-SET-INVENTORY.md` (same directory, same day, a different
model: direct forward simulation of the driven right half-plane, not an
omega-automaton) reaches an independently-derived version of the same
qualitative conclusion reached here by a different method: **"a periodic `c`
does not force `r|Z` periodic [...] a proof of R1 therefore cannot run
through a forcing argument on the driven right half-plane alone; it must use
global consistency (a real diagram constrains `c`, `r` and the LHP
simultaneously, and the driven model does not)."** That is the same
diagnosis as section 5 above, reached from simulation rather than from
automaton-construction and census-construction internals. Two structurally
different local/relaxed models (a driven forward simulation with an
arbitrary clamp, and a fixed-width omega-automaton with a free outermost
letter) both fail to force (star) for exactly the reason obstruction F
predicts -- neither model can see far enough right to know whether its
freedom is genuine. This is convergent evidence for one diagnosis from two
independent, structurally different sources, not a duplicate result: this
analysis did not know that inventory existed until after extracting and
verifying the witness in sections 2-3, and the two analyses touch no common
file.

Their own "what remains open" list (R1-a: does the pin-consistent horizon
`H(p,w)` grow linearly in `w`, currently blocked on system load; R1-b: does
diagram-global consistency restore the forcing the driven model lacks --
explicitly named "the real R1 question"; R1-c: an unaudited log) was
**not** picked up here: R1-a is flagged as another thread's next action on
a directory not written to here, and duplicating it under load contention
would be exactly the kind of collision worth avoiding. R1-b is the
same open question this section's reconciliation bears on but does not
close.

## 8. A concurrent sibling analysis in this same directory, and two corrections it earns

While section 3-6 above were being written, a parallel investigation working
the same redirected target independently produced
`RESULTS-R7-WITNESS-EXTENSION.md`, `extend_probe.py`, `left_sweep.py`, and
`sampler_validity.py` in this same new directory (files this report did not
create; discovered only when re-checking `git status` before finalizing).
Per this repo's own concurrency practice (`PATH.md` prior-work convention:
do not interfere with another thread's in-flight files), those
files are left exactly as written. Reading them changes two
things about how sections 5-7 above should be read, and one thing is added
that neither analysis had alone.

**Correction 1 -- `H_r(n) = 0` is a necessary-only pre-filter for RW/DLP,
not RW/DLP itself, and RW/DLP is period-2-specific.** Section 5-6 above
cites `H_r(n)=0` (`n<=16`) and the separate complete-SAT RW result
(UNSAT, `n=21..28`, `BACKLOG.md` section 12) side by side with the ladder's
NONEMPTY verdict, as two searches over related-but-differently-shaped
objects. The sibling analysis sharpens this: `H_r(n)` is explicitly, in its
own source document's words, "strictly weaker/necessary-only" relative to
the full RW/DLP predicate (it omits RW's own required constancy check), and
RW/DLP itself is a period-2-specific reduction built from a particular
combinatorial encoding (`PROOF-STATE-CAPSULE.md`'s Peel-rank / hard-core /
`12a`-terminal endpoint machinery) that has no established analogue for
`p=3..8`. So neither `H_r(n)=0` nor RW-UNSAT-to-28 should be read as a
general-purpose census that an arbitrary p=2 ladder witness could be checked
against; they are specific, narrow, bounded-depth statements about one
specific proof route for period 2 alone. This does not undermine section 5's
mechanism-level reconciliation (the free-vs-forced-bit account of section
4-5 is independent of this scope point, and still correctly explains why a
*fully forced* construction of any kind cannot contain the freedom the
ladder's witness uses) but it means section 5's table should not be read as
"two searches over the same space with different freedom budgets" quite as
literally as stated there -- they differ in shape as well as in freedom.

**Correction 2 -- a decisive negative result on witness-sampling as an
instrument, with a control this report's own section 3 did not run.** The
sibling analysis tried exactly the next step this report's section 3
stopped short of: sample many accepting lassos (not just `ladder.py`'s own
canonical shortest-BFS witness, which is what section 3 above examines) and
check how far each extends, left and right. The left extension is fully
deterministic and decidable (`RESULTS-ladder-rung1.md` Lemma 1's leftward
analogue is just the wedge check applied past `x_min`); sampled Rule 30
`p=2` witnesses fail it almost immediately (depth 1-7 over `k=1..5`). Taken
alone that would look like evidence the escape is spurious. **Their control
kills that reading**: run the identical sampler on Rule 90's `w=0` case,
where a genuine witness is known to exist (the true Rule 90 lone-seed word
itself, onset 1, extending to at least the probe limit of 24). The sampler
never finds anything past depth 5-6 in that case either -- it misses a
witness that is *known to be present, onset 1, in the language*. So
"sampled witnesses die early" is a fact about the sampler, not about
whether a genuine long-transient Rule 30 `p=2` witness exists. This
directly bears on section 3 above: this report's single extracted
witness is `ladder.py`'s own canonical BFS-shortest lasso, a different
(non-random) selection, but the sibling's control is a warning against
over-reading *any* single extracted witness's properties -- including the
16/47 and 24/47 free-cell counts in section 3 -- as representative of "the"
p=2 witness in general, rather than of that one specific, shortest-available
member of a language that (per rung 1) is known to contain much longer,
unsampled members too.

**What is added, reading both analyses together, that neither had alone.**
Section 4-5 above answer *why* a fully-forced construction (of the kind the
census actually builds) structurally cannot contain the freedom the
ladder's witnesses use -- a mechanism, verified down to the bijectivity of
`carry_action`. The sibling analysis's section 5 independently converges on
the identical structural diagnosis stated in fully general terms and
without reference to the RW/DLP internals at all: *"The ladder
existentially quantifies over an infinite-dimensional family of boundary
continuations in both directions; a finite census quantifies over nothing,
because a finite seed determines its entire diagram... truncating the strip
in either direction discards the fact that a lone-seed diagram has no free
parameters at all."* That is section 5 above's conclusion, reached by a
different method (sampling plus a Rule 90 control, rather than
code-level proof of `literal_extension`'s uniqueness), independently, in
parallel, the same night, touching no common file until this cross-read.
Both analyses also independently arrive at "do not re-run the ladder
deeper" and "R1 stays OPEN, no theorem, no kill condition fired." Given
their explicit, controlled demonstration that naive witness-sampling cannot
distinguish a genuine long-transient witness from an artifact, this report
downgrades its own section 3 finding accordingly: the 16/47 and 24/47 counts
are a real, correctly-verified property of one specific, canonical,
shortest witness, worth recording as a lower bound on how much freedom
*that* witness needs -- not as a claim about the freedom every witness in
the NONEMPTY language needs, and not as progress toward the realizability
question either analysis leaves open.

## 9. What was built but not carried to a result (honestly listed, not padded)

`substrate.py`: a driven-quarter-plane simulator (columns `1..W` under the
standard local rule, column 0 supplied externally as a clamp, column `W+1`
supplied externally as an adjustable free boundary), cross-validated against
the repo's ground-truth generator and against a genuine two-sided diagram on
a strip for both rules (150+100 random trials, 0 mismatches), plus a
linearity check confirming rule 90's driven stepper is linear and rule 30's
is not. This was built to run two experiments -- (1) a run-length structure
theorem (`c` eventually `p`-periodic and nonconstant forces every 1-run of
`r` to length `<=p`, since a nonconstant `p`-periodic word has a `1` in
every length-`p` window, combined with the unconditional pin facts
`r_t=1,c_t=0 => r_{t+1}=1` and `r_t=1,c_t=1 => r_{t+1}=0`), and (2) an exact
induced-period-vs-strip-width sweep with a periodic (not free) right
boundary, using cycle detection on the finite joint state space. Neither was
run: the redirected target took priority, and section 3-5's witness
extraction turned out to be more decisive for the actual question asked.
The run-length claim above is a straightforward, believed-correct
consequence of already-verified identities (not a new risk), but it is
reported here as **unverified** rather than claimed. It
would be a cheap next step and does not depend on anything in
`p1-period2-invariant/`.

## 10. Status of route R1

**OPEN. No kill condition fired in either direction.** What changed:

- A sharper, code-verified statement of obstruction F: at `R=1` the ladder's
  one real constraint binds directly on `r`; at `R>=2` it relocates outward
  and `r` is at least as free as before -- explaining "depth does not
  tighten" from the encoding, not only from measured state growth.
- An explicit, independently re-verified numeric instance (16/47 and 24/47
  cells of one p=2 witness's cyclic tail) of exactly how much freedom the
  ladder's witnesses require at the first unmodelled column.
- A code-level (not prose-level) proof of why the census's `literal_extension`
  construction cannot contain that freedom (per-symbol bijectivity of
  `carry_action`, checked directly against all 4 symbols).
- A citation correction (`n=28` SAT / `n<=16` exhaustive, not `n=24`) and one
  flagged, unresolved discrepancy for the directory that owns it.
- Independent convergent evidence (a different model, a different session,
  same day) for the same underlying diagnosis, from
  `RESULTS-R1-ZERO-SET-INVENTORY.md` (driven-RHP simulation).
- A second, concurrently-produced independent convergence
  (`RESULTS-R7-WITNESS-EXTENSION.md`, this same directory): the identical
  free/forced-parameter diagnosis reached by witness-sampling plus a Rule 90
  control, which additionally proves witness-sampling cannot be trusted as
  an instrument (it misses a *known-to-exist* long-transient Rule 90
  witness by a wide margin) and sharpens the scope of the census citation
  (`H_r(n)` is a necessary-only pre-filter for a period-2-specific
  reduction, not a general finite-configuration census). Section 8 folds
  this in and downgrades this report's own section 3 numbers accordingly.

**What remains the live question, matching both this document's finding and
the concurrent inventory's own R1-b:** whether *global* consistency (an
actual configuration extending arbitrarily far in both directions, not a
fixed-width automaton window or a driven simulation with an arbitrary
clamp) restores the forcing that every local/relaxed model tried so far
lacks. No route in this repo currently attacks that question directly; it
is not the same as, and is not addressed by, re-running either the ladder
or the census deeper.

## Reproduction

```sh
cd experiments/rule30/r1-zero-set-attack
uv run python substrate.py                    # ~1 s, cross-validation only
uv run python extract_r7_witness.py            # ~1 s, witness + column-2 forcing counts
uv run python witness_column2_uniqueness.py    # ~1 s, from-scratch freedom/forcing check
```

All three import `experiments/rule30/ladder/{ladder,rung1}.py` and
`experiments/overnight-arms/common/rule30.py` **read-only** via
`importlib.util.spec_from_file_location`; no file outside this directory was
written. `experiments/rule30/p1-period2-invariant/*.py` was read (not
imported, not executed) for sections 4 and 6-7.

`extend_probe.py`, `left_sweep.py`, `sampler_validity.py`,
`RESULTS-R7-WITNESS-EXTENSION.md`, and their `.json` outputs, also in this
directory, are **not products of this report** -- see section 8. Their own
file lists reproduction commands for that work.

## Files (this report's own; section 8's sibling files are listed there)

- `substrate.py` -- driven quarter-plane simulator, cross-validated, unused
  beyond validation (section 9).
- `extract_r7_witness.py` -- extracts and dumps an explicit R7 mode-(ii) p=2
  witness at `R=1` and `R=2`, with the column-2 forced/free cell count.
- `witness_column2_uniqueness.py` -- from-scratch (not reusing
  `ladder.verify_witness`) confirmation of genuine two-way freedom at every
  `r_t=1` cell and genuine forcing at every `r_t=0` cell, via the raw local
  rule.
- This file.
