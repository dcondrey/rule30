# The actual syntactic-monoid quotient, not the assumed D8 one

Date: 2026-09-06. Script: `syntactic_monoid_quotient.py`.

Status: **NO COMPRESSION OBSERVED AT ANY TESTED LENGTH (`L=1..18`, UP TO
3,015,168 LEGAL WORDS, EXHAUSTIVE). THE RIGHT MYHILL-NERODE CONGRUENCE FOR
ONE QUEUE_STEP IS STRICTLY FINER THAN THE TOTAL D8 ACTION AND, ON THIS
EVIDENCE, EMPIRICALLY INJECTIVE. THIS GENERALIZES RESULTS-QUEUE-WINDOW-PHASE-
NO-GO.MD FROM "D8-BASED QUOTIENTS FAIL" TO "NO CANDIDATE OF THIS SHAPE
COMPRESSES AT ALL", BUT IT IS NOT A PROOF FOR ALL L.**

**SUPERSEDED 2026-09-06 on the "for all L" question:
`RESULTS-SYNTACTIC-MONOID-INJECTIVITY-PROOF.md` proves `sig_A` injective at
every length from two finite checks on `QUEUE_INPUT_ACTIONS`. The measurements
below stand and were the right first move; the open gap named in sections 5 and
7 is closed, section 6's conditional is now unconditional, and the
re-synchronization argument section 5 names as the missing ingredient turns out
not to be needed. Section 4's legal-word counts also hold on the full product
alphabet — legality plays no role.**

Evidence level: `K` (exact exhaustive enumeration to `L=18` and a matching
regression check against the no-go doc's own worked instance; not a
closed-form proof for arbitrary `L`).

## 1. Why D8 is not the right object, and what is

`RESULTS-QUEUE-WINDOW-PHASE-NO-GO.md` proves every fixed end-window plus
total D8 action fails, using one exact instance: interior blocks `00` and
`11` both act as the identity permutation of the 4-state scan (`h_0` and
`h_1` are involutions), yet substituting one for the other changes the
successor queue.

The mechanism the no-go doc does not need to name: `queue_step`
(`constant_tail_queue.py`) does not summarize a scanned block down to its
final state. It re-emits the **entire intermediate scan trace**, position by
position, as literal entries of the successor queue:

```text
QueueStep.queue = tuple(scan) + (BOUNDARY[endpoint],)
```

A common prefix before the block and a common suffix after it are scanned
identically whenever the entering/exit states already agree, so two
successor queues can only differ inside the block's own window. That makes
the correct right-congruence for "these two blocks are interchangeable in
every legal context, forever" not

```text
sig_B(w) = (final state reached from entering state q, for q in 0..3)   -- the D8 element
```

but the strictly finer

```text
sig_A(w) = (full trace of intermediate states from entering state q, for q in 0..3).
```

`sig_A` refines `sig_B` by construction (equal traces imply equal final
states). No enumeration of literal prefix/suffix contexts is required: since
prefixes and suffixes external to the block only interact with it through the
entering state they hand it, the map `q -> full_trace(q, w)` already decides
whether `w` and `w'` are interchangeable in every context.

## 2. Pre-registration

- Alphabet: `{0,1,2}` (queue entries are collapsed `3->1` before scanning by
  `SYMBOL_QUOTIENT` in `constant_tail_queue.py`; interior blocks are drawn
  from the post-normalization alphabet, matching the no-go doc's own example
  words).
- Legal words: length-`L` tuples avoiding the invariant-SFT forbidden factors
  `NORMALIZED_FORBIDDEN = (20, 22, 011)` as internal factors.
- `sig_A`, `sig_B` as defined above (4 entering states `{0,1,2,3}`, exact,
  no sampling).
- **Stabilization** means `#classes(sig_A, L)` is strictly less than the
  legal-word count at some tested `L`, and the class count stops growing
  (repeats, or grows sublinearly against exponential word growth) for three
  consecutive `L`.
- **Kill condition for "a bounded quotient of this shape exists"**: fires the
  moment `#classes(sig_A, L)` is observed strictly below the word count at
  any tested `L` and that gap persists/stabilizes. A single counterexample
  (one non-injective `L`) is not itself a plateau, but it would falsify the
  "always injective" reading below and reopen the search.
- **Kill condition for "sig_A never compresses, full stop"**: a single
  observed merge (two distinct legal words with equal `sig_A`) at any tested
  `L` falsifies it outright. This condition COULD fire — nothing about the
  construction forces `sig_A` to be injective a priori (see the local
  collision noted in Section 4), it is checked exhaustively, not assumed.
- `sig_B` is run purely as a validation baseline: it must reproduce the known
  D8 collapse (plateau at a small constant, `00`/`11` merged at `L=2`) or the
  harness is broken.
- Cheapest version first: `L=1..4` by hand-checkable brute force (matches the
  no-go doc's own worked numbers exactly, see regression check below), then
  scaled to `L=18` while the legal-word count stayed enumerable (`L=18` took
  ~13.5 minutes of CPU time for ~3M words x 4 entering-state traces).

## 3. Regression check against the no-go doc

`full_trace(1, (0,0)) == (1,1)`, `full_trace(1, (1,1)) == (2,1)` — these are
literally the no-go doc's `enter 1: scan(00)=11, scan(11)=21` (section 2).

`full_trace(3, (0,0)) == (2,3)`, `full_trace(3, (1,1)) == (0,3)` — the raw
values; the doc's displayed `scan(00)=21, scan(11)=01` at `enter 3` apply the
doc's own **display** normalization `q(3)=1` (stated explicitly in the doc,
"Writing `q(3)=1` ... leaving `0,1,2` fixed") to the trailing `3`, which the
script also verifies (`normalize_display[s] for s in trace == (2,1)` /
`(0,1)`).

`sig_B((0,0)) == sig_B((1,1))` (the known D8 collision) and
`sig_A((0,0)) != sig_A((1,1))` (the trace congruence separates them) both
hold, as required.

## 4. Exhaustive class counts, `L=1..16`

```text
  L   #legal  #classes_A  #classes_B
  1        3           3           3
  2        7           7           6
  3       16          16           8
  4       36          36           8
  5       81          81           8
  6      182         182           8
  7      409         409           8
  8      919         919           8
  9     2065        2065           8
 10     4640        4640           8
 11    10426       10426           8
 12    23427       23427           8
 13    52640       52640           8
 14   118281      118281           8
 15   265775      265775           8
 16   597191      597191           8
 17  1341876     1341876           8
 18  3015168     3015168           8
```

`sig_B` plateaus at exactly 8 from `L=3` on — the D8 group order, confirming
the methodology reproduces the already-established collapse (`sig_B` carries
exactly the information the no-go doc already ruled out as too coarse).

`sig_A` shows **zero merges at every tested length**: `#classes_A == #legal`
at every `L` from 1 through 18 inclusive (word count growing by a factor of
roughly the alphabet's Perron eigenvalue for the `{20,22,011}`-avoiding
language, about 2.24x per step, reaching just over 3x10^6 legal words at
`L=18`, in roughly 13.5 minutes of CPU time). The "kill condition for a
bounded quotient of this shape" has not fired; the "sig_A never compresses"
reading is what the data shows, holding exhaustively across six orders of
magnitude of word count (3 to 3x10^6).

## 5. Why this is not a surprise, and what it does and does not prove

Structural remark (not itself a proof of injectivity for all `L`): the local
table `QUEUE_INPUT_ACTIONS = ((0,1,3,2),(3,2,1,0),(2,3,1,0),(3,2,1,0))`
happens to have `QUEUE_INPUT_ACTIONS[1][2] == QUEUE_INPUT_ACTIONS[2][2] == 1`
— i.e. symbols `1` and `2`, entering scan state `2`, land on the same next
state. So a first point of difference between two words does NOT
automatically produce a different trace value at every entering state; it
can coincide for the *specific* entering value that happens to arrive at
that position under *one* global entering state. What the exhaustive search
shows is that this local coincidence never simultaneously holds for all four
independent global entering states `{0,1,2,3}` at once, for any tested `L`
— so no observed pair of distinct legal words is interchangeable in every
context. That is an empirical fact up to `L=16-18`, not a closed-form
argument for all `L`; a proof would need to show the four trajectories
(images of the four entering states through a shared word) can never
simultaneously re-synchronize, which this script does not attempt.

## 6. Consequence for the no-go family

This generalizes, but does not replace, `RESULTS-QUEUE-WINDOW-PHASE-NO-GO.md`.
That doc rules out fixed end-window + queue length + endpoint/event data +
total D8 action, for every finite radius, via one exact counterexample family.
This result independently shows that the *actual* right congruence for one
`queue_step` — the one thing whose invariance would make ANY bounded local
summary safe to use as a transition congruence — has not merged two distinct
legal blocks at any tested length. If that holds at every `L` (not proved
here), it says no finite-state summary of an interior block, of ANY shape
(not just D8-based ones), can serve as a lossless transition congruence for
this queue dynamics: the queue_step map genuinely needs to remember the
literal block, not a bounded function of it. This would close the entire
bounded-quotient family in one shot, matching the ambition stated in the task
that motivated this file, but the present evidence is exhaustive-computation
support up to `L~18`, not a proof for unbounded `L`.

## 7. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/syntactic_monoid_quotient.py \
  --max-length 18
```

Raise `--max-length` at the cost of exponential legal-word growth (roughly
2.24x per unit of `L`); `L=18` already reaches ~3x10^6 words (~13.5 minutes
of CPU time in this run) and both signature maps are computed by brute force
with no sampling.
