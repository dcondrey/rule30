# Pull ancestry depth and temporal branching

Date: 2026-09-01

Status: **THE TEMPORAL DEPTH RECURRENCE IS PROVED FOR QUEUES OF EVERY
LENGTH.  THE WEAKER ONE-CHAIN FEATURE BOUND PASSES ITS FROZEN HELD-OUT
CORPUS BUT IS NOT PROVED.  PERIOD TWO REMAINS OPEN.**

## 1. The parent forest

Give every initial coordinate its own root.  At a successful update, the
newly appended boundary coordinate is made a child of the rightmost colex
pivot.  Inherited coordinates keep their nodes.  Count a parent edge only
when its update is a pull (`C`).  The resulting pull-depth is an ordered
ancestry statistic, not an additive weight on the current queue.

The three proved suffix rewrites make the parent coordinate exact:

```text
A or B at time t: parent is the old terminal coordinate;
stabilized C at t: parent is the old third-last coordinate.       (1)
```

If appended nodes are indexed by their update times, (1) means that `A/B`
copies the node at `t-1`, while `C` points to the node at `t-3`.

## 2. All-length temporal theorem

Let pull times and depths be `(t_i,h_i)`, indexed from zero, and interpret a
missing earlier depth as zero.  Pull gaps are at least two.  Between two
pulls every update is `A` or `B`, hence copies the current parent depth.

If `t_i-t_(i-1)>=3`, the node at `t_i-3` descends from the preceding pull,
so

```text
h_i=h_(i-1)+1.                                          (2)
```

If the gap is two, the node at `t_i-3=t_(i-1)-1` lies immediately before
the preceding pull.  That pull is preceded by `A`, and no pull lies between
it and pull `i-2`; therefore

```text
h_i=h_(i-2)+1.                                          (3)
```

Induction in (2)--(3) gives

```text
h_i >= floor(i/2)+1,
number of pulls <= 2 max_i h_i.                         (4)
```

This is a proof for arbitrary event-word length.  The script checks the
coordinate/node identities on every audited literal orbit, but (4) does not
depend on the audit.

The conceptual consequence is important: infinitely many pulls cannot hide
in infinitely many shallow branches.  They force one ancestry chain of
unbounded pull-depth.

## 3. Frozen held-out result for the remaining chain lemma

For initial queue `R`, put

```text
F_R(r) = # {initial 1 cells and maximal-zero-run starts at positions <=r}.
```

The frozen claim is

> Every pull node rooted at initial coordinate `r` has depth at most
> `F_R(r)`.

Its unchanged held-out run produced

```text
all invariant queues of length 19:        3,015,168
new random queues at lengths 24--96:         500,000
new sparse queues at lengths 24--128:        600,000
TOTAL queues:                              4,115,168
successful updates:                        2,660,215
pull events:                                 725,282
maximum observed pull-depth:                       4
feature-depth failures:                            0
temporal-recurrence failures:                      0
orbit-cap hits:                                    0
minimum feature slack:                             0.
```

The zero slack makes the one-chain bound sharp on the held-out corpus.  This
is finite evidence only.

## 3a. Strengthened raw-reserve invariant

Write the remaining reserve of a current coordinate as

```text
k = F_R(root) - pull-depth.
```

After the first held-out result, a raw-state annotation suggested the
strictly stronger invariant

```text
root>0  =>  k >= [raw state = 3].                     (5)
```

Equivalently, an exhausted positive-root coordinate never has raw state `3`.
This is exactly the strict slack needed at a stabilized pull: its pivot has
raw state `3`, so (5) permits the new `C` edge to consume one reserve unit.
An initial off-ray pull pivots at an initial normalized `1`, which is itself
a feature.

The strengthened claim was frozen after discovery through length 16.  Its
new held-out run contains

```text
all invariant queues of length 17:          597,191
new random queues at lengths 24--96:        500,000
new sparse queues at lengths 24--128:       600,000
TOTAL queues:                             1,697,191
successful updates:                       1,079,301
pull events:                                311,450
maximum observed pull-depth:                      4
raw-reserve failures:                             0
feature-depth failures:                           0
temporal-recurrence failures:                     0
orbit-cap hits:                                   0
minimum reserve slack:                            0.
```

This is again finite evidence, not induction.  It improves the proof target:
instead of constructing a global matching, prove preservation of one marked
raw-state exclusion under the exact scan and boundary append.

### The exact inductive reduction

Most of that preservation is already uniform.  Initially every positive
root has depth zero and the normalized row has no raw state `3`.  An `A` or
`B` update gives its new boundary child the parent's unchanged depth and raw
boundary state `1` or `2`.  At a time-zero `C` update, the pivot is an
initial symbol `1`, hence its root prefix already contains a feature.  Every
later `C` is the proved post-retreat pull and its pivot has raw state `3`.
Thus (5) gives one unit of reserve, precisely the unit consumed by the new
`C` edge.  New children therefore preserve (5).

Inherited coordinates keep the same root and depth.  Consequently the sole
remaining inductive clause is

> **Inherited zero-reserve lemma.** If a legal marked row satisfies (5) and
> its queue update succeeds, no inherited coordinate of reserve zero scans
> to raw state `3`.

The four-state table reduces a first failure to exactly three local cases:

```text
(incoming scan state, normalized input) = (0,1), (1,2), or (2,0).       (5a)
```

It also locates the failure strictly left of the rightmost colex pivot.  At
the pivot the raw output is `0` or `2`; to its right, the all-length accepted
equality suffix is empty or `0*2` after raw output `0`, and its raw outputs
are only `0` and `2`.  The constant-table part of this reduction is checked
by `inherited_raw_three_reduction_control()`.

This is a genuine reduction, not the missing proof.  To the left of the
pivot, positive-reserve blocks transport the incoming state by the full
`D8` action.  Contracting those blocks to arbitrary phases is too coarse;
their reserve hierarchy must be retained recursively.  The remaining lemma
is therefore a finite-phase, unbounded-depth block induction, rather than a
fixed-window statement.

## 4. Why this target is strictly weaker

Origin-prefix Hall sorts all pull origins and demands enough initial
features for every prefix of that global multiset.  Bottom-feature crossing
injects all visits to the stabilized ray simultaneously.  The new statement
does neither: two different branches may reuse the same feature prefix.  It
only prevents one nested parent chain from consuming that prefix more times
than it contains features.

Nevertheless (4) turns the one-chain claim into

```text
#pulls <= 2 max_r F_R(r) <= 2|R|.                      (6)
```

That constant-two bound is fully sufficient for `d(r)->infinity`; the
previous sharp mixed budget is not needed.  The proved retreat--pull pairing
then makes retreats finite.  The existing eventual-`2` separator excludes
an immortal remainder, closing constant-tail mortality, rank zero, and the
nonconstant period-two case.

For the actual Rule 30 application there is another weakening: the proved
right trace forbids `00000`, so a counterexample would have eventually
syndetic pull gaps in `{2,3,4,5}`.  A proof may exploit that restriction
without establishing (5) for every abstract invariant queue.

Actual-right realizability does not impose a fixed depth cap.  The literal
hard-core endpoint of length 64

```text
2222121212122121221221221212212221212121221222121222122221212122
```

contains neither `11` nor `22222`.  Its exact reversed inverse diagonal has
tail `3`, survives 13 queue updates, and makes six pulls at times

```text
1,3,5,8,10,12
```

with maximum ancestry depth four.  Thus the exact-length-26 observation that
actual endpoints had depth at most two is a finite artifact.  The witness is
still consistent with the syndetic-chain target and then dies; it is not a
period-two counterexample.

## 5. Exact remaining lemma

It now suffices to prove either:

1. **single-chain feature descent:** each nested pull edge must cross a new
   initial feature start before returning to the same root; or
2. **actual syndetic-chain exclusion:** no finite-root ancestry chain can
   have unbounded depth when the ambient pull gaps are eventually in
   `{2,3,4,5}`.

The local scalar searches do not address these statements.  They collapse
the parent forest, and their exact all-word systems are already
unsatisfiable through factor width five.

The raw-reserve formulation supplies a concrete inductive version of item 1:
show that every exhausted positive-root coordinate avoids raw state `3`.
On the discovery rows, filtering out every positive-reserve coordinate left
only `empty`, `0`, `2`, `02`, or an alternating `{1,2}` word ending in `1`.
That tiny projection suggests a recursive block-action proof, but the grammar
has not yet been established for all rows.

## 6. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_pull_ancestry_depth.py
```
