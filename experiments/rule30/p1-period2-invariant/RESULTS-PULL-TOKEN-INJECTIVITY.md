# Pull-token nonreusability: the §4 bridge fails, and the D8 decoration is a near-chain-invariant

Date: 2026-09-06. Preregistered in `PREREG-PULL-TOKEN-INJECTIVITY.md` (frozen
before any run). Script `pull_token_injectivity.py`; stored witness
`PULL_TOKEN_COUNTEREXAMPLE.txt`.

Status: **THE TOKEN INJECTION PROPOSED IN `RESULTS-HARD-CORE-PULL-DEPTH.md` §4
DOES NOT EXIST IN THE FORM STATED: ALL TWELVE CANDIDATES COLLIDE ON THE
HARD-CORE-DERIVED POPULATION. THE `D8` DECORATION IS REAL BUT NEARLY USELESS —
THE ACTION TAKES 4 VALUES GLOBALLY YET IS CONSTANT ALONG 2,689 OF 2,709 CHAINS.
`(HCD)`, `(SEP)`, TP2 AND PERIOD TWO ARE UNTOUCHED; NOTHING HERE BEARS ON
THEM.**

Evidence level: exhaustive over the stated finite corpora plus one stored
infinite-family witness; no proof.

## 0. Why this is not `RESULTS-QUEUE-WINDOW-PHASE-NO-GO.md` rebuilt

That document kills every state class of the form *fixed-radius two-ended queue
window + length + endpoint/event data + exact total `D8` action*, by placing
neutral blocks in the queue interior where no fixed window can see them.

Nothing here is a bounded quotient. The tokens below are computed on the
complete ordered queue `Q_t`, and the claim tested is per-chain injectivity of a
map on pull edges, not closure of a transition system. The no-go's own §5 names
this continuation verbatim: "A continuation should use the complete queue to
prove pull-token nonreusability, a scale-aware gap descent, or the actual
syndetic pull-ray exclusion." So this is the recommended next step, run.

The result below nevertheless lands in the same direction as the no-go, and for
a reason the no-go did not supply: see §3.1, where the `D8` action turns out to
be constant along 99.3% of ancestry chains — a per-chain statement the no-go's
transition-congruence argument does not make.

## 1. Controls

**Q3 negative control (reported first, as preregistered).** `c_root` is
chain-constant by construction and must collide on every depth-`>=2` chain. It
does, on 2,709/2,709 chains in population A and 22,816/22,816 in population B.
PASS. Had it not, nothing else in this run would be reportable.

**`c_pivot` is tautological and its survival means nothing.** The chain is built
by walking `node -> parent(node)`, and the parent IS the pivot, so the pivots
along a chain are strictly decreasing node indices and `c_pivot` is injective by
construction. Asserted directly: 894,178 chains verified to have strictly
decreasing pivots, zero exceptions. It also fails Q2 outright — the pivot ranges
over the appended region, whose size is the orbit length, so bounding `h` by it
is circular. `c_pivot` is excluded from the survivor list; it was carried only
because the prereg listed it, and it is recorded here as a test that had its
answer by construction.

**Corpus.** Population A (hard-core-endpoint-derived queues): all endpoints
exhaustively to length 20, plus 2,000 random endpoints at each of lengths
64, 96, 128, 192, 256, 384, 512 — 30,214 queues, 4,959 pulls, 12,513 chains
carrying a pull, 2,709 of depth `>=2`, max depth 3, zero orbit-cap hits.
Population B (general invariant queues, holding the abstract counterexamples):
2,416,659 queues, 564,536 pulls, 894,178 chains, 22,816 of depth `>=2`, max
depth 4, zero cap hits.

## 2. Result table (colliding chains / max distinct tokens on one chain)

Population A has 2,709 chains of depth `>=2`; population B has 22,816.

| candidate | A: colliding chains | A: max tokens on a chain | B: colliding chains |
|---|---|---|---|
| `c_root` (neg. control) | 2709 | 1 | 22816 |
| `c_pivot` (tautological) | 0 | 3 | 0 |
| `c_feat` | 2709 | 1 | 22816 |
| `c_count` | **2** | 3 | 302 |
| `c_zrun` | 2709 | 1 | 22816 |
| `c_phase` | 2709 | 1 | 22816 |
| `c_feat_phase` | 2709 | 1 | 22816 |
| `c_count_phase` | **2** | 3 | 302 |
| `c_zrun_phase` | 2709 | 1 | 22816 |
| `c_d8` | 2689 | 2 | 12419 |
| `c_root_d8` | 2689 | 2 | 12419 |
| `c_count_d8` | **2** | 3 | 107 |

**Q1: KILL FIRED.** No candidate is injective on population A. Q3 (fixed
operation `o1`/`o2` at the anchor) is not part of this prereg; the analogous
codomain question is Q2, reported in §3.3.

`c_root_d8` matching `c_d8` exactly, in both populations, is the expected
consequence of §3.2: the root component is chain-constant, so pairing with it
adds nothing and the pair collides precisely when the `D8` component does.

## 3. The two findings that make this more than a kill

### 3.1 Two different "phases", and only one of them is constant

There are two distinct objects in this codebase that the word "phase" can name
at a pull pivot, and they behave oppositely. Keeping them apart is necessary to
read §4 correctly.

**The scan state at the pivot is the constant 0.** This is `raw_scan[pivot]`,
the 4-valued lifted scan state, and it is 0 at every pull measured, with zero
exceptions. Consequently the `c_feat_phase`, `c_count_phase` and `c_zrun_phase`
rows of the table are identical to their undecorated partners: that decoration
multiplies the codomain by one.

**The eight-element `D8` word action at the pivot is NOT constant, but it is
almost constant along a chain.** This is `word_action(Q_t[1:pivot+1])` from
`constant_tail_queue_window_phase_no_go.py`, and it is the object
`RESULTS-HARD-CORE-PULL-DEPTH.md` §4 means by "the absolute eight-state `D8`
phase". Globally it takes 4 distinct values at pull pivots — and only 4 of the 8
group elements ever occur there, all of the form `(2,3,*,*)` or `(3,2,*,*)`:

```text
population A (4,959 pulls):   (2,3,1,0) 2,991  (2,3,0,1) 1,002
                              (3,2,1,0)   396  (3,2,0,1)   570
population B (564,536 pulls): (2,3,1,0) 330,404 (3,2,1,0) 187,215
                              (3,2,0,1) 25,557  (2,3,0,1)  21,360
```

So the decoration is not information-free. But the quantity that matters is
whether it varies ALONG A CHAIN, and it barely does: `c_d8` collides on
**2,689 of 2,709** chains in population A, and its maximum distinct-token count
on any one chain is **2**, never 3 or 4. The decoration separates 20 chains out
of 2,709 — 0.7%.

This is the honest form of the conclusion. §4's `h <= 8N` fallback is a genuine
weakening of `h <= N`, not a vacuous one; it simply does not help, because the
`D8` phase at a pull pivot is a near-invariant of the ancestry chain rather than
a coordinate that advances along it. Anyone proposing to recover the bridge by
enlarging the phase alphabet should note that the enlargement is already
measured to be worth a factor of 2 at best, on the chains where it does
anything at all.

**Correction recorded.** An earlier draft of this file claimed the `D8`
decoration was exactly information-free, on the strength of the 4-valued scan
state being constant. That conflated the two objects above; the scan state is
not what §4 names. The claim was withdrawn and the true `D8` action measured
before this file was finalized.

### 3.2 The literal reading of "projected zero-prefix token" collapses to the root

`c_feat` — the feature start at or below the pivot, projected through `roots` —
equals `c_root` at all 569,495 pulls, both populations, zero exceptions. The
same holds for `c_zrun`, whose token also collapses to one value per chain.

So the most literal reading of §4's "coordinate map from a pull edge to a
projected zero-prefix change" lands on the root, which is chain-constant by
construction. That is precisely why these three candidates all show *one*
distinct token per chain rather than merely colliding: they are not weak
injections, they are constant maps. The bridge as literally stated cannot work,
and this identifies the reason rather than just recording the failure.

This is consistent with, and explains the mechanism behind, the already-false
per-root Hall bound `h <= feature_counts[root]`
(`constant_tail_pull_coordinate_depth.py`, `FEATURE_COUNTEREXAMPLE`).

### 3.3 The one candidate with content, and its single witness

`c_count` — the number of zero-prefix tokens strictly below the pivot in the
COMPLETE ordered queue `Q_t` — is the only candidate that is neither
chain-constant, near-chain-constant, nor tautological. It nearly survives: 2 colliding chains out of 2,709 in
population A (and those two are the same collision seen from two nodes whose
chains share the edges, so there is exactly ONE distinct collision event).

The witness is stored in `PULL_TOKEN_COUNTEREXAMPLE.txt`: a genuine hard-core
endpoint of length 512 (verified by `rank_zero_separator.hard_core`), tail 2,
queue length `N=512`, on which a depth-2 chain has

```text
pull at time 2, pivot 511, c_count=342, root=511, depth 1
pull at time 5, pivot 514, c_count=342, root=511, depth 2
```

The appended cells 512-514 contribute no new feature start, so the count below
the pivot is unchanged across the two pulls. This is inside population A, so
the root-localization escape of §1 of `RESULTS-HARD-CORE-PULL-DEPTH.md` (which
disposes of `3001 0^382 2` by the `200 != 203` three-cell control) does NOT
apply to it. The candidate is dead in the live subcase, not merely in the
abstract one.

Decorating it with the `D8` action does not rescue it: `c_count_d8` collides on
exactly the same 2 chains, because the two pulls in the witness happen to carry
the same `D8` value `(2,3,0,1)` as well as the same count.

Q2, for the record: `c_count` does satisfy the codomain bound on A
(`max c_count / N = 0.889 < 1`), so it failed on injectivity alone, not on size.
On population B it does not (`max c_count / N = 1.143`), which is a second,
independent reason it could not have delivered `h <= N` there.

## 4. What this does and does not close

Closed: the token injection of `RESULTS-HARD-CORE-PULL-DEPTH.md` §4 in the form
stated, over the nine candidates enumerated in the prereg plus the three `D8`
candidates added once the prereg's "eight-state `D8` phase" was traced to
`word_action` rather than to the scan state.

Not closed, and not touched: `(HCD)` itself, which remains exactly as
`RESULTS-HARD-CORE-PULL-DEPTH.md` §3 left it (no failure through all endpoints
of length 27, no failure in the long random corpus, not proved). Root
localization (§2 there) is a theorem and is unaffected. `(SEP)`, TP2, PP1-PP3
and period two are all untouched; nothing here bears on them.

Honest scope: the nine candidates are the ones the archive's own vocabulary
suggests (root, pivot, feature start, feature count, zero run, scan phase, and
the phase-decorated pairs). A token built from data outside that vocabulary —
in particular one that distinguishes the interior neutral blocks the no-go uses,
which §4 of that document explicitly leaves open — is not ruled out by anything
here.

## 5. Consequence for the remaining proof search

`RESULTS-HARD-CORE-PULL-DEPTH.md` §4 lists three routes and this run removes the
first, in both its plain and its `D8`-decorated form. The two it names as
alternatives stand untouched:

* the actual syndetic-chain exclusion;
* the projected diagonal-support / halving lemma.

A continuation that wants to revive a counting bridge must first exhibit a
pull-edge statistic that actually varies along an ancestry chain. Measured here,
root, feature start, zero run and scan phase are exactly constant along a chain;
the `D8` action is constant on 99.3% of chains; and the one statistic that does
vary, `c_count`, has a stored counterexample. That is a concrete precondition
any new candidate should be checked against before anything is built on it, and
it costs one `CANDIDATES` entry in `pull_token_injectivity.py`.

## 6. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/pull_token_injectivity.py
```

Defaults reproduce both populations and the table above; `--a-exact-length`,
`--a-random-per-length`, `--b-exact-length`, `--b-sparse-max-length` and
`--seed` control the corpus. The stored witness is regenerated by the same seed
(730921), lengths 64..512, at random index 845 of length 512.
