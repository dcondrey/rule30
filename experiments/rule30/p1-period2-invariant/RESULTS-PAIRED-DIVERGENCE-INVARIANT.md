# Paired/relative divergence invariant across the queue-window-phase no-go

Date: 2026-09-06

Status: **NEGATIVE FOR BOTH TESTED CONSTRUCTIONS.  FOR TAIL 3, THE
DIVERGENCE BETWEEN THE NO-GO DOC'S OWN COUNTEREXAMPLE PAIR GROWS TO A
FIXED FRACTION OF THE WHOLE WORD ONE ROUND AFTER IT FIRST APPEARS, AND
GROWS WITHOUT SATURATION AS THE FAMILY PARAMETER `k` GROWS.  FOR TAIL 2,
COMBINING TWO INDEPENDENT NEUTRAL-BLOCK SWAP SITES PRODUCES A DIVERGENCE
WIDTH THAT GROWS LINEARLY IN THE SEPARATION BETWEEN THE TWO SITES, EVEN
THOUGH EACH SITE ALONE PRODUCES ONLY A WIDTH-1 DEFECT.  NEITHER
CONSTRUCTION EVER RE-MERGES.  NO FINITE-STATE PAIRED LAW SURVIVES EITHER
KILL CONDITION AS REGISTERED.**

Evidence level: `K` (exact finite computation on the doc's own real scan,
no summarization).

The checker is `paired_divergence_invariant.py`.

## 1. What this does and does not touch

`RESULTS-QUEUE-WINDOW-PHASE-NO-GO.md` proves that for every finite radius
`r`, no fixed end-window plus queue length plus endpoint/event data plus
exact total `D8` word action is a transition congruence on a SINGLE legal
invariant queue (its section 4, `Sigma_r`). The counterexample there pairs
two words differing in one interior neutral block (`00` vs `11`, both
identity in `D8`) and shows their successors still agree on every fixed
window but disagree in total action.

That theorem says nothing about a PAIRED construction: a product state
built from the two queues' real, unsummarized per-symbol scan states, run
forward together. This experiment asks whether such a paired state obeys a
finite law -- specifically, whether the region where the two normalized
queues differ (its position and width) stays confined to boundedly many
patterns of bounded width as the run continues and as the family parameter
grows, or whether it is forced to grow without bound. It does not attempt
to repair `Sigma_r` itself, and it does not touch queue mortality directly
except as an observed side effect.

## 2. Exact scan semantics reused unmodified

Everything numeric here reuses, unmodified, the real sequential scan and
counterexample families already checked by `constant_tail_queue.py` and
`constant_tail_queue_window_phase_no_go.py`:

- `queue_step` / `normalize_queue` from `constant_tail_queue.py` -- the
  actual per-symbol scan and the collapse of `1`/`3` on non-leading
  symbols, not a rederivation.
- `tail_two_pair` / `tail_three_pair` / `word_action` from
  `constant_tail_queue_window_phase_no_go.py` -- the exact `R^0_k`/`R^1_k`
  and `S^0_k`/`S^1_k` families of the no-go doc's section 3.

`h_a(state) == LIFT_GENERATORS[state][a]`, used by `queue_step`'s real scan,
is algebraically identical to `QUEUE_INPUT_ACTIONS[a][state]`, used by the
no-go checker's `word_action`/`scan` (`peel_lift_monoid.py` builds
`QUEUE_INPUT_ACTIONS[right][output] = LIFT_GENERATORS[output][right]`).
So the no-go doc's "total `D8` action" already IS the real sequential scan
composed symbol by symbol, not an approximate summary of it; the paired
construction below differs from the no-go's own argument only in running
the actual scan forward through MANY further rounds of the deterministic
queue-growth cocycle, rather than stopping after the one update the no-go
theorem needs.

## 3. Pre-registration

**Candidate paired state.** At round `t`, the two normalized queues
`W_t`, `R_t` have equal length. Let `first_t`, `last_t` be the first and
last index where they differ (`None` if identical), and
`width_t = last_t - first_t + 1` (0 if identical). The candidate finite law
under test: is there a bound `B`, independent of the family parameter and
of `t`, such that `width_t <= B` for every reachable `t`, together with
finitely many distinct local content-patterns realized inside that window?

**Strong outcome.** `width_t` stays at or returns to a small bound (e.g.
1-4) across all tested `t` and all tested family parameters, with the
distinct interior patterns observed forming a finite, small set -- evidence
that a bounded local "defect automaton" could serve as the missing paired
transition congruence the single-copy no-go rules out.

**Kill condition (must be able to fire on a plausible negative, and does
apply here).** Stop and record negative if, for a fixed construction, the
maximum observed `width_t` grows without saturating as the family
parameter grows (e.g. scales with `k` or with inter-site separation) rather
than converging to a constant, OR if mortality becomes a substitute for
healing (the pair simply dies before any candidate bound could be tested,
which would make "bounded width" true only vacuously).

**Controls.** Every constructed word is checked, not assumed, for: avoiding
the three normalized forbidden factors (`20`, `22`, `011`); ending in a
hard-core-eligible symbol; and, for the double-swap construction, that the
second swap site's entering scan state is genuinely 1 or 3 (the only two
states where eq. 3 of the no-go doc makes `00`/`11` exit-invariant) --
`site2_entering_state` and `find_valid_double_swap_triples` compute this
rather than assert a hand-derived parity.

**Resource limits.** Local CPU only, exact integer/tuple arithmetic, no
floating point, no external solver. Word lengths tested up to ~230 symbols,
up to 200 forward rounds per pair, all completing in well under a second.

## 4. Single-swap pairs, forward-evolved

For tail 2 (`R^0_k`/`R^1_k`, `k` odd, tested `k = 1, 5, ..., 101`): the
successor queues differ at exactly one interior position (`width = 1`,
matching eq. 3's row `enter 1: scan(00)=(1,1), scan(11)=(2,1)`, which
differs only in its first emitted symbol), and BOTH copies die
(`queue_step` returns `None` on both sides simultaneously) on the very next
round, for every tested `k` with no exception. The pair never gets a
chance to test growth: mortality intervenes immediately, one round after
the divergence appears. Concretely, for `k=9` (length-22 queues):

```text
round 0: width=1 at position 10, left_window=(1,) right_window=(2,)
round 1: both queues mortal (queue_step -> None on both sides)
```

For tail 3 (`S^0_k`/`S^1_k`, `k = 2 (mod 4)`, tested `k = 2, 6, ..., 98`):
`width = 1` at round 0 exactly as the no-go doc's own theorem certifies,
but at round 1 the divergence explodes to a large fraction of the entire
queue and keeps growing as `k` grows, with no sign of saturation over the
tested range:

```text
k=2:  max_width=7      k=18: max_width=39     k=34: max_width=71
k=6:  max_width=16      k=22: max_width=48     k=38: max_width=80
k=10: max_width=23      k=26: max_width=55     k=42: max_width=87
k=14: max_width=33      k=30: max_width=65
```

`max_width` is monotone increasing in `k` throughout, consistent with
`width` scaling with the word length rather than staying bounded. This is
the kill condition firing directly: the paired state's natural width
statistic is not bounded, for a family constructed straight from the no-go
doc's own counterexample.

The pair also does not survive long past this explosion (death at round 2
or, occasionally, round 3), and mortality is sometimes ASYMMETRIC: of the
25 values of `k` tested in `2..98`, 9 produce a pair where `S^1_k`'s copy
(the `11` variant) dies strictly before `S^0_k`'s copy, and in every one of
those 9 cases it is always `S^1_k` that dies first -- never the reverse.
A representative full trace, `k=10` (length-31 queues):

```text
round 0: width=1  at position 11  (endpoints agree: both emit 2)
round 1: width=23 at positions 12..34,
         endpoints now DISAGREE (left emits 2, right emits 1)
round 2: left survives, right is mortal (queue_step -> None)
```

So two queues that the no-go theorem certifies as indistinguishable under
every fixed end-window, total phase, and endpoint/event datum can, one
round later, emit different endpoints and have unequal survival -- the
"neutral" swap is not neutral to the pair's future at all, exactly as the
no-go doc's own section 4 already argues for the single-copy case, now
shown to widen catastrophically rather than stay local.

## 5. Double-swap pairs (two interior sites, tail 2 only)

To test whether the neutral-block trick composes when applied at two
independent interior positions, `double_swap_word(k1, k2, k3, flip1,
flip2)` builds `2 1^k1 <b1> 2 1^k2 <b2> 2 1^k3` with `k1` odd (site 1
enters at scan state 1, as in the doc's own tail-2 family) and `k2` chosen,
via `site2_entering_state`, so site 2 genuinely enters at scan state 1 or
3 -- not assumed, checked. `find_valid_double_swap_triples` additionally
requires the base (`00,00`) word to survive one further `queue_step`
before a triple is used. This is the doc's single-site shape reused twice,
not a new independent family.

Flipping only one site at a time (`flip=(True,False)` or `(False,True)`)
reproduces the tail-2 single-swap result exactly: `width = 1`, death on the
next round, for every tested `(k1, k2, k3)`. This is a consistency check on
the construction, not a new finding.

Flipping BOTH sites simultaneously (`flip=(True,True)`) does not simply
combine two independent width-1 defects. It produces a divergence spanning
the ENTIRE region between the two sites, growing linearly with the
separation `k2`:

```text
k1=1,3,5 (all give the same slope):
  k2= 2 -> max_width= 6      k2=10 -> max_width=14
  k2= 4 -> max_width= 8      k2=12 -> max_width=16
  k2= 6 -> max_width=10      k2=14 -> max_width=18
  k2= 8 -> max_width=12      k2=16 -> max_width=20
```

`max_width = k2 + 4` exactly, for every `(k1, k2)` pair tested. A witness
(`k1=3, k2=8, k3=2`, comparing the all-`00` word to the all-`11` word):

```text
round 0: width=12, positions 4..15
  left_window  (base, 00/00)  = (1,1,1,0,1,0,1,0,1,0,1,2)
  right_window (flipped,11/11)= (2,1,1,0,1,0,1,0,1,0,1,0)
```

The two isolated single-site defects therefore do not compose additively
or locally into a bounded joint state; combining them opens an interior
region whose width tracks the site separation, i.e. is unbounded as that
separation is allowed to grow. This directly rules out the natural hope
that a paired automaton could track "one defect per swap site" as
independent, boundedly-many local states.

## 6. Consequence

Both tested paths to a finite paired/relative transition congruence over
the no-go doc's own construction fail the pre-registered kill condition:

- the tail-3 single-swap family's divergence width is not bounded as `k`
  grows, and reaches near-catastrophic size one round after the divergence
  first appears, while the tail-2 family instead escapes the question by
  dying immediately;
- the tail-2 double-swap family shows that combining two individually
  bounded (width-1) interior defects is not itself bounded: the composed
  divergence grows with the sites' separation.

Neither construction ever re-merges (`ever_remerged=False` throughout).
This does not prove no paired/relative invariant of any shape exists --
only that the two natural constructions tried here (the doc's own
single-swap families run forward, and two chained copies of the same
site) both blow up rather than close. It extends the no-go's conclusion
(no fixed single-copy end-window state works) to these two paired
constructions without asserting anything about the general paired-state
question, which remains open.

## 7. Independent verification

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/paired_divergence_invariant.py \
  --max-k 41 --k-step 4 --rounds 80
```

Every constructed word is checked in-line for legality (the three
normalized forbidden factors), hard-core extendability, and (for the
double-swap construction) genuine entering-state 1/3 at the second site,
before being used; nothing is asserted by hand-derivation alone.
