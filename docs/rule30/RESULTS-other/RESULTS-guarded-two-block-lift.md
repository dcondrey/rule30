# Exact guarded lifts of a two-parameter capacity-18 family

Date: 2026-09-13. Status: all-depth lifting and local guard lemmas proved;
three completed layers independently certified; mortality still open.

The family is the full second endpoint

```text
213(13)^a1213(13)^b03,        a,b >= 0,        initial scalar tape 00.
```

Its exact two-step original-ancestor capacity is 18 by the
[all-length counted-language classification](RESULTS-capacity18-joint-mortality.md#1-complete-language-coverage-and-the-new-finite-bound).
The present computation preserves the correlation between both parameters.
It classifies every parameter pair's guarded history through 15 further
updates, and some survive.
The attempted next layer stopped at its explicit route-cache cap. It proves
neither uniform mortality of this family nor period-two exclusion.

The useful distinction exposed here is that the next guard removes exactly
two of four *ambient new-pair choices*, while the reachable choices depend
on a spatial return permutation. Some return cycles force all four choices
to be reachable, and therefore reproduce two surviving choices at each old
survivor. Other components lose all their choices. Controlling this mixture
across temporal depths remains the missing step.

## 1. Exact columns and the four-sheet extension

A depth-n spatial column is

```text
q = (A_0, (A_1,B_1), ..., (A_n,B_n)),
integer encoding = A_0 + sum_j (2*A_j+B_j)*2^(2*j-1).
```

Reading a quaternary input symbol updates the full column by the stated Z
scan, without evaluating a terminal guard prematurely. Reading a fixed word
is its composition. The original endpoint's fixed suffix is read only after
both starred blocks. The complete chronological guard test then reconstructs
every growing birth suffix.

**Triangular extension lemma.** If F_n is the column map for a fixed word,
then its depth-(n+1) extension has the form

```text
(q,x) -> (F_n(q), g_q(x)),       x = (a,b) in F_2^2,
g_q(a,b) = (a + t*b + e, b + c),    t,e,c in F_2.
```

Proof: for one scanned symbol, all lower-layer information is fixed. If its
incoming constants are p,A,B, put c=p OR B. The new pair satisfies

```text
v = b + c,
u = a + (v OR A)
  = a + (1+A)*b + A + (1+A)*c.
```

This is the displayed affine form. Those eight forms are closed under
composition. Writing the later map as (t',e',c'), the composed coefficients
are

```text
t_total = t+t',       c_total = c+c',
e_total = e+e'+t'*c.
```

They form the eight-element dihedral permutation group on the four pairs;
their orders are 1,2,4. Consequently a pure depth-n block orbit lifts to a
pure depth-(n+1) orbit with period ratio 1,2,or4. Inductively the order of a
block on its fixed-A_0 slice divides 4^n. Here the slice is fixed by the high
bit of the block's last symbol. The prefix and seam both enter the required
slices. The present specialized lift checks this hypothesis; it does not
silently discard a preperiod.

The affine coefficients also give an exact ordered transport recurrence.
For consecutive local maps (t_i,e_i,c_i), the total e includes the ordered
cross-term sum_{i<j} t_j*c_i. Arbitrarily reordering maps is invalid. More
seriously, the resulting three coefficients describe only ONE extra pair.
They do not specify the return's action on another temporal layer. The
actual ordered block word must still be retained for subsequent lifts.

## 2. What the compressed graph retains

At depth n retain:

1. the complete first-star orbit, with its exact parameter phases;
2. every reachable joint column G_n whose endpoint passes all n guards;
3. the first-return permutation on G_n, labeling each edge by the positive
   integer L meaning the actual spatial word `(13)^L`;
4. for every first-star phase, the first visit of its seam column to G_n,
   with its exact b-offset, or a certified cycle having no such visit.

Both block maps are bijections on the fixed-A_0 slices. Thus a finite closed
reachable graph is a union of cycles, and deleting unmarked vertices gives
an exact weighted first-return permutation. A deleted vertex is not assumed
to die for every larger b; its next surviving vertex and exact distance are
retained. Only entire cycles with no marked vertex are discarded.

**Guarded lift lemma.** From this data, one obtains exactly all reachable
depth-(n+1) columns whose lower projection belongs to G_n as follows:

1. Close the complete lifted first-star orbit. Its old phase is the new
   phase modulo the old period.
2. Transport every lifted seam column along its old first-entry word. Keep
   its resulting full column and a representative pair (a,b).
3. Close the union of all these entries under the lifted old first-return
   edges. Call this cover H_(n+1). It has at most 4|G_n| states.
4. Read the fixed suffix and test the complete chronological guard history.
   Keep exactly G_(n+1), and contract its weighted return cycles again.

Proof: every a has a phase in the complete lifted first orbit. For that a,
its second-star trajectory is a cycle in a permutation graph. Its visits
to the old guard-surviving set consist precisely of its first entry followed
by the successive old first-return words. Step 3 closes all and only those
visits, including every reachable new pair. A failed lower guard cannot be
repaired by adding a higher pair, so no excluded column can pass the new
full history. Step 4 is therefore an exact filter. Tracking the actual word
lengths and parameter labels proves reachability as well as closure. This
argument applies at every n; it is not limited to the saved depths.

An empty G_n would prove a uniform temporal cutoff for this family. A cap,
a nonempty set, or a projected closure without the actual return words does
not have that implication.

## 3. The next guard and the spatial return action

**Balanced guard lemma.** For any q in G_n, exactly two of the four ambient
depth-(n+1) lifts pass the new guard. In pair labels 0,1,2,3, its accepted
set A_n(q) is one of

```text
{0,1}, {0,3}, {1,2}, {2,3}.
```

Proof: the fixed suffix acts on the new pair by the same eight-element
affine group. All earlier guards and birth symbols depend only on q.
Scanning that now-fixed birth suffix again composes invertible maps
`v <- v XOR constant; u <- u XOR (v OR constant)`. The final condition
u=v pulls back to either a=constant or a+b=constant. Each selects exactly
two pairs, one for either value of b.

Let R_n(q) be the new pairs actually reachable by the joint two-star action.
Then the exact count recurrence is

```text
|G_(n+1)| = sum_(q in G_n) |R_n(q) intersect A_n(q)|.
```

In particular |G_(n+1)| <= 2|G_n|. This is a conditional statement about
ambient column extensions. These columns are not original ancestors, and
their number is not |C_r(alpha)|. The lemma does not charge an independent
bit to a chronological repeat. The previously recorded
[unchanged original-fiber plateau](RESULTS-aperiodic-mortality-audit.md)
is compatible with it.

Along an old first-return cycle, the R_n(q) are carried bijectively by its
edge permutations. After a full cycle the resulting permutation, called
the cycle monodromy here, preserves the reachable set. If it has order4,
it is a four-cycle. Every nonempty invariant reachable set is then all four
pairs. Such a cycle gives exactly two new survivors per old survivor.
This proves a local reproduction mechanism, not its persistence at the next
depth: the new return cycles have new ordered transports and new guards.

## 4. Saved complete layers and the stopped continuation

The complete depth-12 base joint graph has 441,088 states and 125 survivors.
The new algorithm did not construct the full joint graphs at higher depths.
It constructed the smaller all-parameter covers and certified the skipped
paths explicitly.

| Further depth | First-star period | Guarded cover | Survivors | Cached ordered-path states |
|---:|---:|---:|---:|---:|
| 13 | 512 | 425 | 216 | 107,008 |
| 14 | 1,024 | 703 | 351 | 340,480 |
| 15 | 2,048 | 1,088 | 545 | 1,003,008 |

The attempted depth16 stopped when its route cache reached the declared
2,000,000-state cap. Its partial work is not a completed layer. The complete
run took 2.59 seconds and 3,450,496 actual repeated-block steps, including
the capped attempt. No cap was raised.

The exact saved covers distinguish survival from transitivity:

| New depth | Old states with 2/3/4 reachable pairs | Old states with 0/1/2 successful pairs | Old cycles of monodromy order 1/2/4 |
|---:|---:|---:|---:|
| 13 | 23 / 29 / 73 | 3 / 28 / 94 | 14 / 27 / 4 |
| 14 | 67 / 27 / 122 | 18 / 45 / 153 | 21 / 53 / 8 |
| 15 | 129 / 58 / 164 | 30 / 97 / 224 | 37 / 84 / 13 |

All eight possible first-return pair permutations and all four possible
guard acceptance sets occur at each saved layer. The order4 cycles account
for 13,11,20 old survivors respectively, and exactly 26,22,40 new survivors.
Thus neither universal loss of descendants nor a single fixed guard line
describes these layers. Finite growth of the surviving set is not an
all-depth branching theorem, an infinite finite-parameter trajectory, or
unbounded repeat count at fixed capacity.

For example a=1248,b=260 gives the successful total scalar prefix
`00110011111111111`, of length17 and repeat count13, and remains alive at
the recorded depth. This is an exact finite prefix, not its complete tape or
a mortality bound. The first two scalars and original ancestry are supplied
by the counted-language theorem; the lift itself acts on second endpoints.

## 5. Exact route certificates and independent checking

A cached route row contains

```text
(state, target_state, distance, packed_permutation, next_state, local_map).
```

At an old survivor the route has distance0, target=self, and identity map.
It still records the actual next block step and its one-pair map. Every
nonterminal row has the actual next state, distance one greater than the
next row, the same target, and

```text
route_map(q) = route_map(next(q)) composed with local_map(q).
```

Strictly decreasing distance certifies the entire finite path. A positive
first-return edge first takes the actual unit step out of the old survivor,
then follows this certified route. The checker verifies that its total
distance equals the stored exponent L; it does not substitute an earlier
depth's permutation for `(13)^L`.

The independent Python checker validates all four actual extended-column
transitions for every cached row, all initial first-star phases, every seam
entry, closure and reachable representatives of the lifted cover, weighted
cycle contraction, and every chronological guard and birth symbol. It also
validates source, base-manifest, and sidecar hashes. The completed layers
passed; seven copied-data corruption controls were rejected. The final
independent artifact explicitly retains the unresolved depth16 status.

This is an exact computational certificate with a finite mathematical
closure argument, not a proof-assistant formalization.

## 6. What remains unresolved

The induced guard-surviving graph is small, but its discarded return paths
are not. The current certificate explicitly traverses and shares their
unit steps, so its route storage still grows much faster than its survivor
cover. A three-bit affine summary suffices for the current lift and loses
the ordered information needed by the next one.

The concrete further obligation is an exact representation of those return
words that can be lifted repeatedly while controlling their survivor/guard
intersection. For example a reusable section or word-composition certificate
would have to retain the action on every subsequent pair, not merely a
single four-point permutation. The saved data supply exact edge words,
guard sets, and transitive versus restricted components against which such
a proposal can be checked. No such bounded representation or descending
quantity is proved here. Extending this family alone would also leave the
other unresolved capacity-18 families and arbitrary capacity untreated.

## 7. Four-sheet propagation and the lift of a four-cycle

Date: 2026-09-19. Status: a pre-registered inductive invariant is refuted on
the saved layers, and a lift lemma is proved at every depth. Neither decides
mortality.

**Pre-registered test.** The order4 mechanism of section 3 is local. The
simplest inductive candidate is that every old survivor with all four sheets
reachable has a child with all four sheets reachable. If that held at every
depth, the survivor tree would be infinite and this family would not be
uniformly mortal. The
[pre-registration](../../../experiments/rule30/PREREGISTRATION-cap18-four-sheet-propagation.md)
was committed before its script existed. Two generations are measurable:
parents in G_12, whose children's sheets come from layer 14, and parents in
G_13, whose children's sheets come from layer 15. A child in G_15 would need
the capped depth16 cover.

| Parents | With four sheets | No four-sheet child | Expected if independent |
|---|---:|---:|---:|
| G_12 | 73 | 17 | 13.8 |
| G_13 | 122 | 54 | 34.6 |

The kill fired in both generations. The last column assumes each child has
four sheets at its layer's base rate, 122/216 and 164/351. Both failure counts
exceed it, so the property is not inherited. The weaker invariant with at
least three sheets fails too, for 18 of 102 and 31 of 149 parents. Before any
outcome was read, the script checked the manifest hashes, that each layer's
live cover states are exactly the next layer's old survivors (216 and 351),
that liveness equals the chronological guard evaluated from scratch, that
every four-sheet parent has exactly two children, and that every saved
histogram reproduces.

The exploratory order4 version failed completely: no child of the 13 and 11
old survivors on order4 cycles lies on an order4 cycle. The lemma below
forces that.

**Lift lemma.** Let C be a cycle of G_n with total word W, let M be its
monodromy on the new pair, and let O be an M-orbit, so the survivors over O
lie on one lifted cycle that traverses C |O| times. Let z be the central
translation `(a,b) -> (a+1,b)`, the square of either four-cycle.

1. If |O| = 4, that is M is a four-cycle, the lifted monodromy on the next
   pair is a translation, never a four-cycle. If |W| is even, it is the
   identity or z.
2. If |O| = 2 and O is closed under adding (1,0), the lifted monodromy is a
   translation when |W| is even.

Case 2 covers both orbits of M = z and the two-point orbit of a reflection
with two fixed points. Here W = (13)^L, so |W| is always even.

Proof: at a fixed symbol of W the |O| traversals hold depth-(n+1) pairs that
form one transported copy of O. The linear part of every group element fixes
(1,0), so this copy is closed under adding (1,0) whenever O is, and so is its
image after the symbol. The next layer's incoming constants at that symbol are
the old high bit U and the new bits U',V' of the depth-(n+1) pair, so by the
triangular extension lemma its coefficients there are `t = 1+U'` and
`c = U OR V'`. A pair `{y, y+(1,0)}` contributes 1 to the sum of U' after the
symbol, and 1+V' to the sum of c, because its members share V' and differ in
U. Summed over O at one symbol, t therefore adds to |O| + |O|/2, which is 0
mod 2 for |O| = 4 and 1 for |O| = 2. For |O| = 4 the two pairs carry V' and
V'+1, so c adds to 1. By the composition rule of section 1, t and c of the
lifted cycle are the sums of these over the |W| symbols: t = 0 in case 1 and
t = |W| in case 2, while c = |W| in case 1. A group element with t = 0 is a
translation, and one with t = c = 0 is the identity or z.

So the children of an order4 cycle lie on a cycle whose monodromy is the
identity or z, which forces nothing beyond the pairs the seam entries supply.
The reproduction mechanism of section 3 never acts at two consecutive depths
of one lineage, so an infinite lineage, if one exists, needs the entries to
supply its sheets at least every other depth.

Checks: all 82 and 134 child cycles of the two generations were matched to
the parent cycle they lift. The 4 and 8 order4 cycles lift to identity or z
monodromy, and all 25 and 37 lifts the lemma covers have t = 0, with no
violation. The lemma also holds on every column of the pure (13) block through
depth 8. The algebra excludes nothing else: with arbitrary incoming constants
from the layer below, an exhaustive two-layer enumeration at even word length
realizes every other combination of monodromy class, orbit size and lifted
class, including four-cycles over fixed points of the identity or of a fixing
reflection and over free-reflection orbits. At odd word length the same
enumeration confirms the parity-free part of case 1, every four-point orbit
lifting to a free reflection since c = |W| = 1, and shows that case 2 needs
even length: there every two-point orbit closed under (1,0) lifts with t = 1.
The saved lifts show no four-cycle
over a free-reflection orbit (0 of 75), but the (13) block lifts 4.9 percent
of the free-reflection orbits over depth-8 columns to four-cycles, so that
absence is not an identity.

The refutation covers two finite generations of this family. The lemma holds
at every depth, but it only says where four-cycles cannot occur.

## 8. Seam-entry supply and the first-star schedule

Date: 2026-09-19. Status: an entry-supply lemma is proved at every depth and
validated on layers 5-16, of which 5-12 and 16 were not used to find it; a
pre-registered inheritance invariant is refuted; depth 16 is completed. None of
this decides mortality.

By construction (section 2) a cycle's reachable pairs are the monodromy closure
of its seam entries, so what is left from section 7 is which entries arrive. The
answer does not depend on the cycle.

**Entry-supply lemma.** Let P_n be the first-star period at depth n, h_d the
action of `(13)^(P_(d-1))` on the depth-d pair over the prefix column, and O_d
the h_d-orbit of that column's own pair, so P_d = |O_d| P_(d-1). The |O_d| new
phases over an old phase with an entry all enter G_(d-1) at one vertex, with
pairs g(O_d) for a single group element g.

Proof: `(13)^(k P_(d-1))` fixes the depth-(d-1) prefix column and moves its pair
by h_d^k. Reading `(13)^a`, the seam and the old entry route then acts on the
new pair by group elements that depend only on the shared lower column, by the
triangular extension lemma.

Call {x, x+(1,0)} a z-pair, and each accepted set {0,1}, {2,3}, {0,3}, {1,2}
of section 3 a guard line. Every group element has linear part fixing (1,0),
so it maps a point, a z-pair, a guard line or the fibre to one of the same kind.
Each layer therefore has one entry type, and a z-pair meets every guard line in
exactly one pair. At every depth:

1. Every cycle of G_(d-1) receives an entry. Each cycle of the cover, or of the
   base joint graph, contains a generator of its closure, and that phase's next
   entry is the first survivor after it.
2. At a z-pair layer every old survivor has a child; at a fibre layer, exactly
   two.
3. A survivor dies exactly when its reachable set lies in the guard line
   disjoint from its accepted line. Monodromy z closes every entry type to a set
   containing a z-pair, and a four-cycle closes it to the fibre, so no survivor
   on a z or order4 cycle ever dies. A fixing reflection closes a guard line to
   three pairs and a moved point to a z-pair, so its cycles lose survivors only
   at point layers.

The prefix orbit alone fixes the schedule. One pass over the depth-24 prefix
orbit gives the periods for d = 1..24: 1, 4, 8, 16, 32, 32, 32, 128, 128, 128,
128, 256, 512, 1024, 2048, 2048, 4096, 8192, 16384, 32768, 65536, 131072,
131072, 262144. The analysis script checks them against every lifted layer and
against the first periods of the exhaustive joint closures at depths 4, 8, 12
and 16, a separate program.

| Entry type | Layers 2 <= d <= 24 |
|---|---|
| fibre | 2, 8 |
| z-pair | 3, 12, 17, 18, 24 |
| guard line | 4, 5, 13-15, 19-22 |
| point | 6, 7, 9-11, 16, 23 |

At the lifted layers 5-16, h_d is a four-cycle at 8, z at 12, a free reflection
at 5 and 13-15, the identity at 6, 9, 10 and 16, and a fixing reflection at 7
and 11. The saved layers 13-15 are all guard-line layers, which is why no entry
pair there differs by (1,0).

**Out-of-sample validation.** A
[pre-registered](../../../experiments/rule30/PREREGISTRATION-cap18-entry-supply.md)
run of the unmodified lift from the exhaustive depth-4 base (8 survivors)
completed layers 5-15. It reproduces the exhaustive G_8 and G_12 as sets, its
layers 13-15 are byte-identical to the committed ones, and the independent
checker of section 5 passes on every layer. Every live old phase entered as the
lemma says, at every layer. The fibre layer 8 predicted |G_7| = 31 before the
run, which holds; the z-pair layer 12 killed no survivor; no survivor on a z or
order4 cycle died; fixing-reflection cycles lost survivors only at point layers.

**Depth 16.** Raising only the route cap from 2,000,000 to 8,000,000 states
completes depth 16 from the depth-12 base: 2,915,328 route records, 7.6 seconds,
460 MB resident, and the independent checker passes. Depth 17 would need about
three times the records, so this is one layer, not a new ladder.

| Layer | Type | G_(d-1) | G_d | Offspring mean | Deaths |
|---:|---|---:|---:|---:|---:|
| 5 | guard line | 8 | 14 | 1.750 | 1 |
| 6 | point | 14 | 24 | 1.714 | 0 |
| 7 | point | 24 | 31 | 1.292 | 2 |
| 8 | fibre | 31 | 62 | 2.000 | 0 |
| 9 | point | 62 | 90 | 1.452 | 7 |
| 10 | point | 90 | 95 | 1.056 | 10 |
| 11 | point | 95 | 85 | 0.895 | 26 |
| 12 | z-pair | 85 | 125 | 1.471 | 0 |
| 13 | guard line | 125 | 216 | 1.728 | 3 |
| 14 | guard line | 216 | 351 | 1.625 | 18 |
| 15 | guard line | 351 | 545 | 1.553 | 30 |
| 16 | point | 545 | 673 | 1.235 | 88 |

The pre-registered H2, that each point-layer mean at 9, 10 and 11 is below
1.553, the smallest guard-line mean at 13-15, survives. H3, the same bound for
depth 16 registered before it ran, survives too. H2 had little power: the
product of the means at 9-12 was known to be 125/62 and mu_12 lies in [1,2],
so it could only locate the slowdown. The point layers are not uniformly low:
layer 6, excluded in advance for its 14 parents, reaches 1.714, above every
guard-line mean from 14 on. The entry type sets where deaths can occur, not
the ordering of the means. The tree shrank once, at layer 11, the third point
layer in a row. The decline 1.73, 1.63, 1.55 at layers 13-15 happens within one
entry type.

**Self-sufficient supply is not inherited.** By corollary 3, survivors on z and
order4 cycles never die. The pre-registered candidate H1 was that each such
survivor has a child on such a cycle, which at every depth would make the tree
infinite. It fails in 9 of the 10 registered generations, G_4 to G_5 through
G_13 to G_14: 143 of 205 parents fail, 88 of them out of sample, against 104
expected under the registered independence floor and 126 under the corrected
one. The one clean generation, G_7 to G_8, has 6 parents. Of the 218 children
of z-cycle survivors, 95 lie on identity cycles, 85 on free reflections and 38
on z cycles. The pre-registration said the lift lemma puts a z cycle's children
on identity or z cycles. It only makes them translations, and the free
reflections are the translations by (0,1) and (1,1), so both floors are
reported.

**What is left.** By corollary 3 a layer can empty the tree only if no survivor
of the previous layer lies on a z or order4 cycle, nor, away from point layers,
on a fixing-reflection cycle. Every computed layer has survivors on z or order4
cycles: at least 3 (G_4), and 219 of the 545 in G_15. If every G_n has one,
the survivor tree is infinite and index 15 is not uniformly mortal. The open
step is that existence statement at every depth, not inheritance along one
lineage.

## 9. Survivor mass and exact halving

Date: 2026-09-19. Status: a mass lemma is proved at every depth and checked on
every old phase of layers 5-16; the lift's survivor mass equals the lifetime
census exactly through depth 16; the first-star schedule runs to depth 38; the
lemma's predictions at layers 17 and 18 hold in a pre-registered census; three
further pre-registered censuses measure the first five layers the lemma leaves
open, mu_19 = 10137/2^32, mu_20 = 20239/2^34, mu_21 = 20457/2^35,
mu_22 = 81869/2^38 and mu_23 = 10173/2^36, with kept fractions 0.5042, 0.4991,
0.5054, 0.5003 and 0.4970, and reach lifetime 46. None of this decides
mortality.

A survivor count weights every column equally. Weight each column instead by
the parameter pairs that reach it: a uniform modulo P_n, then b uniform modulo
the length of that phase's body2 orbit. Both are powers of two, so the mass
mu_n of G_n is the limiting fraction of pairs a < 2^i, b < 2^j that survive n
guards. The family is uniformly mortal exactly when mu_n = 0 for some n. For a
column q of G_n, write nu_q for the mass on its four lifts.

**Survivor-mass lemma.** If layer n+1 has z-pair or fibre entries, or the cycle
of q has monodromy z or a rotation, then nu_q is invariant under adding (1,0),
and exactly half of the mass of q survives layer n+1. In particular
mu_(n+1) = mu_n/2 at every z-pair and fibre layer.

Proof: a new phase entering the cycle at pair y visits q once for each point of
the monodromy orbit of the transported y, so its mass at q is uniform on that
orbit. By the entry-supply lemma the new phases over one old phase enter at one
vertex with pairs g(O_(n+1)). Every group element commutes with adding (1,0).
So the sum is invariant when O_(n+1) is a z-pair or the fibre, and also when every
monodromy orbit is closed under adding (1,0), as for z and the rotations. That
translation maps each guard line to the parallel one, which is its complement,
so an invariant measure puts half its mass on the accepted line.

The same argument gives each old phase's kept fraction at a column exactly:

| Monodromy | z-pair or fibre layer | Guard-line layer | Point layer |
|---|---|---|---|
| z, rotation | 1/2 | 1/2 | 1/2 |
| fixing reflection | 1/2 | 1/4 or 3/4 | 1/2, or 0 or 1 |
| free reflection | 1/2 | 1/2 unless the entry line is one of its orbits, then 0, 1/2 or 1 | 0, 1/2 or 1 |
| identity | 1/2 | 0, 1/2 or 1 | 0 or 1 |

At a guard-line layer the transported entry line meets each z-pair once. A
fixing reflection fixes both points of one z-pair and swaps the points of the
other, which gives 1/4 plus 0 or 1/2. A column's kept fraction is the
mass-weighted mean over the old phases entering its cycle. Mass can vanish only at guard-line and point layers, only
on identity and free-reflection columns, and at point layers also on fixing
reflections.

Write s_n for the share of the depth-n mass on z and rotation columns. Those
columns keep exactly half at every layer type, so mu_(n+1) >= s_n mu_n/2. The
lemma does bound the mass below, but only through a quantity it does not
control. Over the guard-line and point layers of 5-16, s_n ran 0.207 to 0.500,
a floor of 0.103 to 0.250 against kept fractions of 0.481 to 0.586. Uniform
mortality therefore needs s_n = 0 at some layer: no survivor mass at all on a z
or rotation cycle.

A cycle's monodromy is that of the whole body2 orbit through it, because its
return words add up to one period. Which orbits are z or rotations therefore
does not depend on the guards; only which of them carry survivors does.

**Checks.** `cap18_survivor_mass.py` recomputes nu_q from the saved entries and
cycles and asserts every entry of the table on every old phase at every column
of layers 5-16. It also asserts that the support of nu_q is the lift's reachable
set, that its accepted part is the lift's children, and that each layer's kept
mass is the next layer's mass. Through depth 16 the census box a < 2^11,
b < 2^16 covers every period that carries survivors (P_16 = 2^11, longest orbit
2^16). Its surviving fraction is therefore mu_n exactly, and the two independent
programs agree as exact rationals at every depth 4-16:

| n | 1-3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2^n mu_n | 1 | 0.875 | 0.875 | 0.906 | 1.063 | 1.063 | 1.047 | 1.188 | 1.242 | 1.242 | 1.301 | 1.289 | 1.275 | 1.227 |

At guard-line and point layers the kept fraction ran from 0.481 (layer 16) to
0.586 (layer 7). The deviation comes from the old phases that keep 0 or 1 at a
column, or 1/4 or 3/4 at guard-line fixing reflections. At every such layer the
two members of each pair occur about equally often: 205 zeros against 186 ones
at layer 16, and 39 quarters against 36 three-quarters at layer 15, while 465
(layer 16) and 319 (layer 15) keep exactly 1/2. The 942 deviating cases over
layers 5-16 are the script's control that its halving checks are not vacuous.
Columns on z or rotation cycles held 18 to 50 percent of the mass. The census's
"roughly halving" count is therefore exact halving at z-pair and fibre layers
with small drift elsewhere. A box of 2^k pairs covering the periods at depth n
holds exactly 2^k mu_n pairs that survive n guards, so a record near k, rising
one step per doubling of the box, is 2^n mu_n staying near 1. The per-layer
sums of the cycle coefficients t and c of section 7 are not forced: both
parities occur.

**Schedule to depth 38.** `first_star_schedule.cpp` streams the prefix orbit
with 128-bit columns and reproduces the Python schedule through 24. P_38 = 2^31.
Layers 25-38 are guard lines at 25, 26 and 28, z-pairs at 27, 29, 30, 33, 36
and 37, fibres at 32 and 35, and points at 31, 34 and 38. The mass halves exactly
at 15 of the layers 2-38, so mu_17 = 2513/2^28 and mu_18 = 2513/2^29 without
computing those lifts. After layer 16 the point layers are 23, 31, 34 and 38.

**Out-of-sample test.** A
[pre-registered](../../../experiments/rule30/PREREGISTRATION-cap18-survivor-mass-census.md)
census of a < 2^13 against the nested ranges b < 2^18 and b < 2^19 (8192 rows,
110 s) reproduces mu_n for every n <= 16 in both boxes, and both give
mu_17 = 2513/2^28 and mu_18 = 2513/2^29, the predicted values: 20104 and 40208
pairs survive 17 guards, 10052 and 20104 survive 18. No program had computed
either layer. Two boxes agreeing is the evidence that neither undersamples.
Past depth 18 the boxes miss phases, since P_19 = 2^14 exceeds their a range,
and their fractions, which are then not the mass, stay between 1.18 and 1.75
times 2^-n through depth 27, and between 1.18 and 1.56 in the larger box. The deepest pair in the box is (742, 109338) with
lifetime 34, confirmed by the frozen `panel/cert33.py` replay and by the
chronological column guard. So G_34 is nonempty and a common-depth certificate
for index 15 needs depth at least 35, against the 32 that the witness at
(1534, 15247338) gave. The next census raises both again.

**Layers 19 and 20.** A second
[pre-registered](../../../experiments/rule30/PREREGISTRATION-cap18-mass-census-depth20.md)
census, `cap18_mass_census_grid.py`, takes a nested grid a < 2^13, 2^14, 2^15
against b < 2^19, 2^20, 2^21, one sweep per a, 2^36 pairs in the largest box in
about 27 minutes. All nine boxes reproduce mu_n for every n <= 18. Layer 19 is
the first the halving lemma does not determine, and all six boxes covering
P_19 = 2^14 agree: mu_19 = 10137/2^32, a kept fraction of
10137/20104 = 0.5042 and 2^19 mu_19 = 1.2374. That is (Y) on the pre-registered
band [0.44, 0.54]. At layer 20 the pre-registered verdict is (I), since b < 2^19
undersamples there and the covering boxes disagree. The two that saturate,
a < 2^15 with b < 2^20 and b < 2^21, agree post hoc on mu_20 = 20239/2^34, a
kept fraction of 20239/40548 = 0.4991.

The half-sample prediction failed, as pre-registered (K). The a < 2^13 boxes
carry half the depth-19 phase classes and put k_19 at 0.4906 and 0.4894 against
the true 0.5042, missing by 0.0136 and 0.0149 where the pre-registration allowed
0.01. Their exploratory fractions past depth 18 are therefore not a guide to the
mass at that precision. The covered box replaces them: 2^n times the fraction in
a < 2^15, b < 2^21 stays between 1.230 and 1.295 at every depth 19 to 30,
against the 1.18 to 1.75 the half-sampled boxes drifted through.

The record rose to lifetime 36 at (31051, 1202824), pre-registered (Y) against a
floor of 35 and confirmed independently by the frozen `panel/cert33.py` replay
on the explicit 2467759-symbol word. It appears only in the largest box, since
its a exceeds 2^14 and its b exceeds 2^20. So G_36 is nonempty and a
common-depth certificate for index 15 needs depth at least 37.

**Where the self-sufficient mass comes from.** `cap18_class_flow.py` follows the
kept mass from every depth-n column onto its children and classifies both ends,
depths 4 to 15. It is exploratory and not pre-registered. Two controls hold
exactly: the children of center and rotation columns stay inside the section 7
lift lemma at every depth, and the flow into a depth reproduces that depth's own
column masses as exact rationals, so s_(n+1) is computed twice by different
routes. What changes with depth is how many classes supply it and how evenly:
one class at depths 4 and 5, then two to four through 12, and all five present
classes at 13 and 14, where the weakest still sends 0.156 and 0.299 of its kept
mass to a z or rotation child and no single class supplies more than 0.478 or
0.333 of the total. Depth 12 is the sharp case the other way: the fixing
reflections sent nothing at all, and s_13 was still 0.2387, so losing a whole
class did not empty the z and rotation columns. Two depths with all five feeding
is not a trend, but this is the first measurement of the quantity the lemma's
floor depends on. The ambient two-layer enumeration of section 7 bears on it
permissively: read forward rather than as an exclusion, its transition table
lets every parent class but a four-traversal rotation at odd word length have a
center or rotation child, over arbitrary incoming constants rather than over
this family's survivors.

**Layer 21, and layer 20 without the post hoc mark.** A third
[pre-registered](../../../experiments/rule30/PREREGISTRATION-cap18-mass-census-depth21.md)
census, `cap18-mass-census-21.json`, takes a < 2^15, 2^16 against b < 2^21,
2^22, 2^38 pairs in the largest box in 1.82 hours. All four boxes reproduce
mu_n for every n <= 18 and no member reaches the step cap. All five predictions
hold. mu_19 = 10137/2^32 reproduces under the new a < 2^16 and b < 2^22 ranges,
so the layer-19 value does not depend on its box. All four covering boxes now
agree on mu_20 = 20239/2^34, which the previous census could only give post hoc
with a pre-registered verdict of (I), so layer 20 loses that mark; the kept
fraction is 20239/40548 = 0.4991. Layer 21 is new: mu_21 = 20457/2^35 from the
two boxes covering P_21 = 2^16, a kept fraction of 20457/40478 = 0.5054 and
2^21 mu_21 = 1.2486, inside both the [0.44, 0.54] band the earlier open layers
were judged by and the tighter [0.49, 0.53] registered as the riskier claim.
The record rose to further lifetime 37 at (21781, 2338078), so G_37 is nonempty
and a common-depth certificate for index 15 needs depth at least 38.

The record's growth law is not the one the two census pre-registrations
assumed. Over the dyadic maxima of every box measured, 2^0 to 2^27 in the
lifetime census and 2^32 to 2^38 in the two grid censuses, 18 of the 33 single
doublings add nothing, and the plateaus run to three doublings: max_ell 19 from
2^15 through 2^18, and 34 from 2^32 through 2^35. The largest box here is one
of them, a < 2^16, b < 2^22 finding the same 37 at the same pair as the half
the size a < 2^15, b < 2^22. The average slope is 0.91 steps per doubling from
2^27 to 2^38 and 0.92 from 2^0 to 2^38, the exponents 28 to 31 being
unmeasured. So one step per doubling
is a trend and not a per-doubling fact, and the rationales in both
pre-registrations that called a non-rising doubling the first stall were wrong
about the sequence they appealed to, though each prediction resolved Y on the
floor it actually stated.

**Layers 22 and 23.** A fourth
[pre-registered](../../../experiments/rule30/PREREGISTRATION-cap18-mass-census-depth23.md)
census, `cap18-mass-census-23.json`, runs the same unmodified program over
a < 2^16, 2^17 against b < 2^23, 2^24, 2^41 pairs in the largest box in 15.4
hours on six workers. `resolve_cap18_depth23.py`, committed before the artifact
existed, reads its nine predictions by rule; all nine hold and all fifteen of
its self-checks pass. mu_19, mu_20 and mu_21 reproduce exactly under the new a
and b ranges. Layer 22 is a guard line at P_22 = 2^17: mu_22 = 81869/2^38, a kept
fraction of 81869/163656 = 0.5003 and 2^22 mu_22 = 1.2492, inside both
[0.44, 0.54] and [0.49, 0.53]. Layer 23 is the first point layer past 16, at the
same period: mu_23 = 10173/2^36, a kept fraction of 40692/81869 = 0.4970 and
2^23 mu_23 = 1.2418, inside the point-layer band [0.48, 0.59] and the guard-line
band [0.44, 0.54]. Only the two a < 2^17 boxes cover P_22 and P_23, and at depth
22 both b ranges already saturate, so their agreement there is guaranteed in
advance and tests nothing; the a < 2^16 boxes, which do not cover P_22, read
81849 rather than 81869 there. Depth 23 is the one live cross-check: b < 2^23 and
b < 2^24 agree through depth 23 and first part at 24, in both a ranges, so the b
saturation law extends one threshold. The census carries no column classes, so
it does not measure s_n, and neither form of mortality is decided by it. Layer 24
is a z-pair layer, so mu_24 = mu_23/2 by the lemma. Layer 25 needs a < 2^19 and
b < 2^25, 2^44 pairs, which puts it past this program at practical cost.

The dyadic maxima are 37 at 2^39, 39 and 40 at the two 2^40 boxes, and 46 at
2^41, at (81664, 16385540). So G_46 is nonempty and a common-depth certificate
for index 15 needs depth at least 47. The frozen `panel/cert33.py` replay on the
explicit 32934417-symbol word confirms 46. The step from 40 to 46 over one doubling, after
a plateau at 37 from 2^38 to 2^39, makes the record's growth lumpier in both
directions than the trend of the previous paragraph.

**What this changes.** Uniform mortality now needs the kept fraction, between
0.48 and 0.59 at every computed guard-line or point layer of 5 to 16, 0.5042 at
19, 0.4991 at 20, 0.5054 at 21, 0.5003 at 22 and 0.4970 at 23, to reach 0 at one such
layer. All of that layer's mass would then sit on identity, free-reflection or
(at a point layer) fixing-reflection columns, with every entry off the accepted
line. Unbounded lifetimes would follow from any positive lower bound on the kept
fraction at those layers. The lemma bounds it below only by s_n/2, so what it
proves is positive exactly when some survivor mass sits on a z or rotation
cycle, and nothing here says it must. What remains is an equidistribution
statement: where the transported entries fall relative to the guard lines.

## 10. Files and reproduction

- [Primary guarded lift](../../../experiments/rule30/two_block_guarded_lift.cpp)
- [Hashed completed-layer manifest](../../../experiments/rule30/capacity18-guarded-15.json)
- [Independent verifier](../../../experiments/rule30/verify_guarded_two_block_lift.py)
- [Independent certificate](../../../experiments/rule30/capacity18-guarded-15-independent.json)
- [Saved-cocycle statistics program](../../../experiments/rule30/guarded_two_block_lift_statistics.py)
- [Saved-cocycle statistics](../../../experiments/rule30/capacity18-guarded-15.statistics.json)
- [Four-sheet propagation and lift-lemma checks](../../../experiments/rule30/cap18_four_sheet_propagation.py)
  and [their artifact](../../../experiments/rule30/cap18-four-sheet-propagation.json)
- [Entry-supply checks and tests](../../../experiments/rule30/cap18_entry_supply.py), with artifacts for
  [layers 5-15](../../../experiments/rule30/cap18-entry-supply.json) and
  [layers 13-16](../../../experiments/rule30/cap18-entry-supply-16.json)
- Section 8 runs: [from depth 4](../../../experiments/rule30/capacity18-guarded-base4.json) and
  [to depth 16](../../../experiments/rule30/capacity18-guarded-16.json), with independent certificates
  [here](../../../experiments/rule30/capacity18-guarded-base4-independent.json) and
  [here](../../../experiments/rule30/capacity18-guarded-16-independent.json)
- Section 9: [survivor-mass checks](../../../experiments/rule30/cap18_survivor_mass.py) and
  [their artifact](../../../experiments/rule30/cap18-survivor-mass.json), which embeds the
  [first-star schedule](../../../experiments/rule30/cap18-first-star-schedule.txt) written by
  [its streaming program](../../../experiments/rule30/first_star_schedule.cpp) (depth 38 in about 4 minutes)
- Section 9's out-of-sample test: [its pre-registration](../../../experiments/rule30/PREREGISTRATION-cap18-survivor-mass-census.md),
  [the census](../../../experiments/rule30/cap18_mass_census.py) and
  [its artifact](../../../experiments/rule30/cap18-mass-census.json) (about 2 minutes on six workers)
- Section 9's layers 19 and 20: [its pre-registration](../../../experiments/rule30/PREREGISTRATION-cap18-mass-census-depth20.md),
  [the nested-grid census](../../../experiments/rule30/cap18_mass_census_grid.py) and
  [its artifact](../../../experiments/rule30/cap18-mass-census-20.json) (about 27 minutes on six workers)
- Section 9's layer 21: [its pre-registration](../../../experiments/rule30/PREREGISTRATION-cap18-mass-census-depth21.md)
  and [its artifact](../../../experiments/rule30/cap18-mass-census-21.json) (about 1.8 hours on six workers)
- Section 9's layers 22 and 23: [its pre-registration](../../../experiments/rule30/PREREGISTRATION-cap18-mass-census-depth23.md),
  [its artifact](../../../experiments/rule30/cap18-mass-census-23.json) (about 15.4 hours on six workers) and
  [its resolver](../../../experiments/rule30/resolve_cap18_depth23.py)
- Section 9's class flow: [the program](../../../experiments/rule30/cap18_class_flow.py) and
  [its artifact](../../../experiments/rule30/cap18-class-flow.json) (about 8 seconds, exploratory)

The manifest names the complete binary sidecars. To recheck existing data
without repeating the orbit computation:

```sh
uv run --offline --no-project --with numpy python experiments/rule30/verify_guarded_two_block_lift.py experiments/rule30/capacity18-guarded-15.json --allow-incomplete --output /tmp/rule30-guarded-lift-check.json
uv run --offline --no-project --with numpy python experiments/rule30/guarded_two_block_lift_statistics.py --primary experiments/rule30/capacity18-guarded-15.json --output /tmp/rule30-guarded-lift-statistics.json
uv run --offline --no-project --with numpy python experiments/rule30/cap18_four_sheet_propagation.py   # about 7 s
```

The section 8 sidecars are not committed. The two lift commands in the
docstring of `cap18_entry_supply.py` regenerate them in about 10 seconds, the
depth-16 one with 460 MB resident. Then run
`cap18_entry_supply.py`, and again with
`--primary capacity18-guarded-16.json --output cap18-entry-supply-16.json`.
`cap18_survivor_mass.py` reads the same sidecars and the committed census and
schedule, and runs in about 4 seconds.

## 11. Depth 19, and two families whose answer is already known

Date: 2026-09-21. Status: the depth cap of section 8 was a command-line flag,
not a wall; layers 17, 18 and 19 are complete and independently checked, which
makes `s_16`, `s_17` and `s_18` measurable for the first time. The same
unmodified lift reproduces the uniform mortality certificates of the two closed
seams that have one, index 5 and index 27, and those controls show that no
finite prefix of `s_n` distinguishes a mortal family from an immortal one.
Pre-registered in
[PREREGISTRATION-cap18-self-sufficient-share-depth19.md](../../../experiments/rule30/PREREGISTRATION-cap18-self-sufficient-share-depth19.md).
None of this decides mortality for any open seam.

**The depth-17 estimate was wrong, and it was load-bearing.** Section 8 says
"Depth 17 would need about three times the records, so this is one layer, not a
new ladder", and route `p1-cap18` carried that forward as the reason `s_n` stops
at 15. Run from the same exhaustive depth-12 base with the three budget flags
raised and nothing else changed -- `--max-states` 8,000,000 to 40,000,000,
`--max-block-steps` 50,000,000 to 400,000,000 and `--seconds` 300 to 5,400 --
depth 17 costs 6,158,336 route records, 2.11 times depth 16's 2,915,328, and
layers 13 to 17 complete in 21.0 s. A second run to depth 19, at 120,000,000
states, 4,000,000,000 block steps and 7,200 s, completes in 560.8 s and
71,548,416 ordered block steps; at depth 19 the section-8 run's block-step and
wall-clock limits would each have bound as well, so the state cap was not the
only one that had to move. Peak resident memory was about 918 MB and 6.05 GB,
observed at the console and recorded in no artifact. Layers 13, 14 and 15 are
byte-identical to the previously saved `capacity18-guarded-15` cover and entry
sidecars in both runs, as `cap18-entry-supply-19.json`'s
`committed_layers_byte_identical` block records, and layer 16 reproduces 673
survivors, so the new layers sit on a reproduction of the saved ones rather than
beside them. Those sidecars are gitignored `*.bin`, so the byte-identity check
is reproducible only where they already exist.

| Layer | Type | G_(d-1) | G_d | Offspring mean | Deaths |
|---:|---|---:|---:|---:|---:|
| 17 | z-pair | 673 | 946 | 1.406 | none |
| 18 | z-pair | 946 | 1487 | 1.572 | none |
| 19 | guard line | 1487 | 2560 | 1.722 | 39 free reflection, 34 identity |

Layers 17 and 18 are z-pair layers, where the entry-supply lemma forces every
old survivor to have a child, and both have zero deaths as it requires. Layer 19
is the first guard-line layer past 15 and kills only on identity and
free-reflection cycles, as corollary 3 requires. `cap18_entry_supply.py`, run
unmodified on the depth-19 manifest, passes every validation through layer 19:
`lift_lemma_violations` 0, `no_death_on_z_or_rotation_cycles` true, every live
old phase entering as the entry-supply lemma says, and the layer types matching
the independently computed first-star schedule.
`verify_guarded_two_block_lift.py`, also unmodified, reports
`all_saved_layers_verified` true with 2560 surviving columns and mortality
false.

**Self-sufficient survivors past depth 15.** The survivor counts on z and
four-cycle cycles, the set corollary 3 says never dies, are 37, 45, 71, 219,
221, 388 and 499 of 125, 216, 351, 545, 673, 946 and 1487 at depths 12 to 18.
The mass-weighted share `s_n` that the survivor-mass floor
`mu_(n+1) >= s_n mu_n / 2` actually needs is

| n | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---:|---:|---:|---:|---:|---:|---:|
| s_n | 0.3113 | 0.2387 | 0.2917 | 0.4089 | 0.4274 | 0.4194 | 0.3623 |
| kept at layer n+1 | 0.5236 | 0.4955 | 0.4947 | 0.4810 | 0.5000 | 0.5000 | 0.5042 |

computed by `cap18_self_sufficient_share.py`, a companion that imports
`cap18_survivor_mass.py`'s `load`, `column_masses` and `layer_record` unchanged
and differs only in accepting a manifest whose first-star period exceeds the
`a < 2^11` lifetime-census box and in applying the census cross-check to exactly
the layers where that box provably covers. Depths 12 to 15 reproduce the
committed `cap18-survivor-mass.json` values exactly, and layers 13 to 16 are
still checked against the lifetime census. The survivor-mass lemma is asserted
on every old phase at every column of every layer reported here, and layers 17
and 18, both z-pair layers, keep exactly half as it requires. The registered
prediction was `s_16, s_17, s_18 >= 0.10`; all three hold, and no measured `s_n`
at any depth 4 to 18 is 0.

**Two known-answer controls.** The guarded lift had never been run on a family
whose answer is known. Of the three closed two-parameter seams, index 12 closes
at depth 4 and is degenerate; the other two do not.

| Index | Word | Base | Last layer | Stop reason | Survivors | Wall clock |
|---:|---|---:|---:|---|---:|---:|
| 5 | `21213(13)^a031(31)^b303` | depth 4 | 23 | closed empty guarded cover | 0 | 58.7 s |
| 27 | `3031(31)^a3031(31)^b303` | depth 4 | 16 | closed empty guarded cover | 0 | 0.03 s |

Both reach zero survivors at exactly the depth section 3 of
[the joint-mortality report](RESULTS-capacity18-joint-mortality.md) records as
the first failed further guard, 23 for index 5 and 16 for index 27, and
`verify_guarded_two_block_lift.py` returns
`uniform_family_mortality_verified` true with
`remaining_surviving_columns` 0 on both. What is independent is the
construction, not the guard predicate: `verify_guarded_two_block_lift.py`
imports `decode_guards` and the `panel/cert33.py` oracle from
`verify_two_block_family.py`, the joint-column engine's own checker, and both
lifts start from that engine's depth-4 base manifest. Within that, it is a
reproduction of two certificates whose only previous source was the separate
joint-column engine `two_block_column_orbit.cpp`, by a construction that stores
first-return words
and transported entries instead of whole joint columns.

**What the controls say about `s_n`, and it is not good news for the
instrument.** Route `p1-cap18` records `s_n` past depth 15 as "the instrument
that would" decide the route. Both control profiles are now available in full.

| Index | s_n = 0 at | s_n = 1 at | Empty layer at |
|---:|---|---|---:|
| 5 | 4, 7, 9, 11, 12, 13, 16, 20, 21, 22 | 5, 6, 8, 10, 14, 15, 17, 18, 19 | 23 |
| 27 | 4, 5, 6, 7, 8, 9, 10, 14, 15 | 11, 12, 13 | 16 |

`s_n = 0` is necessary for layer `n+1` to empty, by the survivor-mass lemma and
corollary 3, and it occurs nineteen times across the two families whose answer
is known. Seventeen of those nineteen are false alarms. Index 27 carries `s_n =
0` through seven consecutive depths, 4 to 10, and survives all seven. In the
other direction index 5 has `s_n` at its maximum value 1 at depth 19 and is
empty at 23, so the strongest possible positive reading of the quantity is
compatible with death four layers later. No prefix of `s_n` measured on either
family whose answer is known announces the layer that kills it, so measuring
more layers of it for index 15 is not evidence for unbounded lifetimes. It is
still evidence the other way if it ever reaches 0, which is necessary for the
next layer to empty; what goes is the reading of a positive `s_n` as support.

Two limits on how far that carries. Both controls are among the three families
the [seam-intertwining identities](RESULTS-column-seam-intertwining.md) reduce
to one parameter, so their joint state count equals their first-orbit count and
their survivor sets stay between 1 and 8 columns. At every depth of both, the
whole survivor mass sits in a single monodromy class, so `s_n` there is not a
share at all but an indicator of which class the family's one surviving orbit is
in, and it takes only 0 and 1, against 0.2387 to 0.4274 for index 15 over depths
12 to 18 and 0.2089 to 0.5000 for index 8. No immortal family is in the control
set either, because none is known, and no mortal non-intertwined two-parameter
capacity-18 family is known, so no control without these defects exists to run.
What the controls establish is that the presumption behind measuring `s_n`
deeper -- that a mortal family announces itself in the quantity before the layer
that kills it -- is false where it can be tested at all.

**The first-star schedule does not determine the outcome, and a controlled pair
shows it.** `first_star_schedule` depends only on the prefix and `body1`. Index
5 is `21213(13)^a031(31)^b303` and index 8 is `21213(13)^a1213(13)^b03`: same
prefix, same `body1`, different seam and `body2`. Their schedules are therefore
identical, and the computed ones agree at every layer through 20, both in
period and in entry type. Index 5 empties at depth 23; index 8 has 7140
survivors at 18 and has grown at every layer. Held against that fixed schedule,
the two families' survivor ratios are

| Layer | Type | index 5 | index 8 |
|---:|---|---:|---:|
| 10 | point | 0.875 | 1.556 |
| 11 | z-pair | 1.000 | 1.679 |
| 12 | guard line | 0.571 | 1.687 |
| 13 | guard line | 1.000 | 1.708 |
| 14 | point | 0.500 | 1.246 |
| 15 | z-pair | 1.000 | 1.439 |
| 16 | z-pair | 1.000 | 1.628 |
| 17 | point | 0.500 | 1.291 |
| 18 | fibre | 2.000 | 2.000 |

They agree exactly at every z-pair and fibre layer, 1 and 2, which is what the
entry-supply lemma forces, and they differ at every guard-line and point layer,
which is exactly where the lemmas leave the outcome free. So the schedule, the
entry types, and the layers at which mass can be lost are all shared by a family
that dies and a family that does not: whatever separates them is the seam and
the `body2` transport, not the first-star orbit. Any argument for `s_n > 0`
whose only index-5 discriminator is the schedule proves index 8 mortal, which is
false. Both known extinctions, index 5 at 23 and index 27 at 16, occur at point
layers.

**An open seam other than 15, lifted for the first time.** Nothing in the
catalog had run this construction on indices 8, 23 or 34; the joint-column
engine reached its 2,000,000-state cap at depth 12 for index 8 and 34 and at
depth 16 for index 23, and those caps are what the open-seam rows of section 4
of the joint-mortality report record. Indices 8 and 34 are run here; 23 is not.

| Index | Word | Base | Layers | Last G_d | Stop reason |
|---:|---|---:|---|---:|---|
| 8 | `21213(13)^a1213(13)^b03` | depth 8 | 9-18 | 7140 | route cache state cap at 60,000,000 |
| 34 | `30322(2)^a100(0)^b32` | depth 8 | 9-17 | 14098 | route cache state cap at 60,000,000 |

`verify_guarded_two_block_lift.py` verifies every saved layer of the index-8 run
and leaves mortality false with 7140 surviving columns. Its survivor counts at
depths 8 to 18 are 63, 126, 196, 329, 555, 948, 1181, 1699, 2766, 3570 and 7140:
growing, like index 15 and unlike either control. Its `s_n` at depths 8 to 17 is
0.5000, 0.3867, 0.4885, 0.2981, 0.2089, 0.3905, 0.3606, 0.2937, 0.3246 and
0.3694, never 0 and in the same band as index 15's, and its `2^n mu_n` stays
between 2.0000 and 2.2148, so the survivor-mass lemma holds on a third family
and the second open seam behaves like the first. The index-34 run is verified the
same way, with 14098 surviving columns at depth 17 and mortality false, and its
counts grow fastest of the four, 161, 312, 602, 845, 1690, 3042, 4482, 5406,
8562, 14098 for depths 8 to 17. Neither this nor any count here is a mortality
argument; a common-depth certificate for index 8 still needs depth at least 34
and one for index 34 at least 29, since (753, 12291) has further lifetime 33 and
(20, 8964344) has 28, and a certificate needs depth strictly greater than every
member's lifetime. Neither run was pre-registered: the registration covers
indices 15 and 5 only, and these two are exploratory add-ons. All four open
seams grow; both closed ones do not.

## 12. Files added by section 11

- [Pre-registration](../../../experiments/rule30/PREREGISTRATION-cap18-self-sufficient-share-depth19.md)
- [The self-sufficient share companion](../../../experiments/rule30/cap18_self_sufficient_share.py) and
  [its artifact](../../../experiments/rule30/cap18-self-sufficient-share.json)
- Index-15 depth-19 run: [manifest](../../../experiments/rule30/capacity18-guarded-19.json),
  [entry-supply artifact](../../../experiments/rule30/cap18-entry-supply-19.json) and
  [independent certificate](../../../experiments/rule30/capacity18-guarded-19-independent.json)
- Index-5 control: [manifest](../../../experiments/rule30/capacity18-guarded-i05b4.json) and
  [independent certificate](../../../experiments/rule30/capacity18-guarded-i05b4-independent.json)
- Index-27 control: [manifest](../../../experiments/rule30/capacity18-guarded-i27.json) and
  [independent certificate](../../../experiments/rule30/capacity18-guarded-i27-independent.json)
- Index-8 run: [manifest](../../../experiments/rule30/capacity18-guarded-i08.json) and
  [independent certificate](../../../experiments/rule30/capacity18-guarded-i08-independent.json)
- Index-34 run: [manifest](../../../experiments/rule30/capacity18-guarded-i34.json) and
  [independent certificate](../../../experiments/rule30/capacity18-guarded-i34-independent.json)
- Index-15 depth-17 run, which carries the depth-17 cost measurement on its own:
  [manifest](../../../experiments/rule30/capacity18-guarded-17.json)

The binary sidecars are not committed. Every run in section 11 is one
invocation of the unmodified `two_block_guarded_lift.cpp`; the four commands are
in the docstring of `cap18_self_sufficient_share.py` and in the manifests' own
`config` blocks.

## 13. The last open seam lifted, and a guard-independent survival count

Date: 2026-09-21. Status: all four open seams now have guarded lifts, and the
assertion set the programs carry passes on all six two-parameter capacity-18
families. A registered band for `s_n` was too narrow and its kill fired, on the
high side. A guard-independent count `SAFE_n` of columns that cannot die is
derived, checked against both known answers, and is 1.4 to 2.6 times the GOOD
count on the open seams. None of this decides mortality. Pre-registered in
[PREREGISTRATION-cap18-safe-set-and-seam-23.md](../../../experiments/rule30/PREREGISTRATION-cap18-safe-set-and-seam-23.md).

**All four open seams are lifted, and the assertions pass on all six families.**
Index 23, `3031(31)^a213(13)^b03`, was the last open seam with no guarded lift.
From its exhaustive depth-12 base at a 60,000,000-state cap it completes layers
13 to 19 in 2655.3 s and stops on `route_cache_state_cap`, with
`|G_d|` = 116, 185, 261, 303, 507, 1014, 1724 for d = 13..19;
`verify_guarded_two_block_lift.py`, unmodified, verifies every saved layer in
25.7 s and leaves mortality false at 1724 surviving columns.

Every assertion the existing programs carry holds on it: every column's accepted
set is one of the four guard lines, so the balanced guard lemma is intact; every
layer's entry type matches the independently computed first-star schedule; the
mass halves exactly at all four z-pair and fibre layers, 13, 14, 18 and 19 in
the lift's own numbering; each layer's kept mass equals the next layer's mass;
the survivor-mass lemma's per-class kept fractions hold on every old phase at
every column; `lift_lemma` reports zero violations; and no survivor on a z or
four-cycle cycle dies. The same set passes on all six families.

A correction to how an earlier draft of this section framed that. It said index
23 was the first family checked whose two block words differ. It is not, and the
manifests say so: `body1`/`body2` are `13`/`31` for index 5, `2`/`0` for index
34 and `31`/`13` for index 23, against `13`/`13` for indices 15 and 8 and
`31`/`31` for index 27. Three of the six have unequal block words, and two of
those three, indices 5 and 34, were already lifted and checked in section 11.
What index 23 adds is coverage, not a first: the assertion set now passes on
every one of the six, including all three with unequal block words, and on the
only open seam that had never been lifted at all.

**`s_n` on the last two open seams, and a registered band that was too narrow.**

| n | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---:|---:|---:|---:|---:|---:|---:|
| index 23 | 0.2668 | 0.4111 | **0.6214** | 0.4701 | 0.3446 | 0.2786 | 0.4343 |

| n | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| index 34 | 0.2797 | 0.3546 | 0.3684 | 0.3285 | 0.3070 | 0.3436 | 0.3699 | 0.3602 | 0.3549 |

`2^n mu_n` stays between 1.6162 and 1.7090 for index 23 and between 1.7734 and
1.8521 for index 34. The registration predicted `s_n` in `[0.15, 0.55]` with a
kill outside `[0.10, 0.60]`. **The kill fired**: index 23's `s_14` is 0.6214.
It fired on the high side, which is the opposite of what the kill was written to
catch -- the registration's stated worry was an `s_n` of 0, which "would be the
first one ever seen and would put a common-depth certificate for that seam back
in play". 0.6214 is instead the largest `s_n` ever measured on an open seam, and
it is outside index 15's whole measured range. The band was set from the two
families then available and was simply too tight above; that is a defect in the
registration, not a finding, and it is recorded as a fired kill rather than
rescoped after the fact.

Across all four open seams `s_n` is never 0 at any computed depth, over `n` =
4..18 for index 15, 8..17 for index 8, 12..18 for index 23 and 8..16 for index
34, with the whole range `[0.1765, 0.6214]`. Both closed seams take only the
values 0 and 1. By section 11 that split is not evidence: index 5 and 27 keep
`s_n` at 1 within four and three layers of the layer that empties them.

**A guard-independent sufficient condition.** A column dies at layer `n+1`
exactly when its reachable set `R` misses its accepted set `A`, and by the
balanced guard lemma `A` is one of `{0,1}`, `{2,3}`, `{0,3}`, `{1,2}`. Each of
those is the complement of another, so `R` misses `A` exactly when `R` lies
inside a guard line. The two sets `{0,2}` and `{1,3}` are not among the four, so
a column whose `R` lies inside no guard line has a child whatever its own guard
turns out to be, and

```text
SAFE_n = #{ q in G_n : |R(q)| >= 3, or R(q) in {{0,2},{1,3}} }
```

satisfies: `SAFE_n > 0` forces `G_(n+1)` nonempty. A `z`-pair is exactly `{0,2}`
or `{1,3}`, and corollary 3 closes a `z` or four-cycle cycle's entries to a set
containing one, so GOOD is contained in SAFE; that containment is asserted at
every layer of every family below and never fails. Note the direction: `SAFE_n >
0` is *sufficient* for `G_(n+1)` to be nonempty and is not necessary, so it is a
weaker hypothesis than the GOOD condition but a stronger statement than the
conclusion it gives.

`SAFE_n` equals `|G_n|` at every z-pair and fibre layer, with no counterexample
across all six families, because every entry is then a `z`-pair or the whole
fibre. So the count is forced except at guard-line and point layers, and only
those are informative. Restricted to them:

| Family | informative layers | SAFE/GOOD mean | min | SAFE range |
|---|---:|---:|---:|---|
| index 15 | 5 | 2.58 | 1.32 | 102-1194 |
| index 8 | 5 | 2.14 | 1.63 | 92-1617 |
| index 23 | 3 | 1.40 | 1.24 | 127-200 |
| index 34 | 6 | 2.07 | 1.56 | 294-6084 |
| index 5 (closed) | 10 | -- | -- | 0-0 |
| index 27 (closed) | 8 | -- | -- | 0-0 |

Both forced control values hold: `SAFE_22 = 0` for index 5 and `SAFE_15 = 0` for
index 27, the depths whose successor layer is empty. `SAFE_n > 0` at every layer
the six manifests carry, which for the open seams is `n` = 12-18, 8-17, 12-18
and 8-16. The registered ratio prediction, index 15's mean at least 1.5 with a
kill below 1.2, holds at 2.58. Index 23's 1.40 is the weakest and sits not far
above that floor.

The closed rows have no ratio because at every informative layer of both closed
families `GOOD_n = SAFE_n = 0`: the quotient is `0/0`. That is the whole content
of the earlier draft's claim that SAFE "adds nothing" on the closed families --
it adds nothing because both counts vanish wherever a difference could have
shown, not because the two sets were compared and found equal.

**The split is exceptionless, and it lives entirely at the destructive layers.**
Call a layer destructive when it is a guard line or a point, the two types at
which anything can die. Over all six families and every layer computed:

- on both closed seams, `SAFE_n = 0` at **every one of their 18 destructive
  layers** and `SAFE_n = |G_n|` at every non-destructive one, so `SAFE_n` is a
  function of the layer type alone and carries no information about the family;
- on all four open seams, `SAFE_n` lies **strictly between 0 and `|G_n|` at
  every one of their 19 destructive layers**, and is never 0.

That 18-for-18 against 19-for-19 is a cleaner separation than `s_n` gives, and
it sharpens what a proof would have to do. Since `SAFE_n` is restored to `|G_n|`
at every z-pair and fibre layer, and index 15's first-star schedule has one at
13 of the layers 2 to 38 with no run of destructive layers longer than five, the
open question is exactly whether a run of at most five destructive layers can
take `SAFE` from the whole survivor set to nothing. On the two families where it
does, it takes one layer, every time. Neither observation is a proof, and the
controls' own behaviour is consistent with their survivor sets never exceeding
eight columns: `SAFE_n = 0` is not extinction either, since index 5 has it at
ten depths and `G_(n+1)` is nonempty at nine of them.

One limit on the derivation. That `{0,2}` and `{1,3}` are never accepted sets is
enforced here by the assertion in `cap18_entry_supply.py` that every accepted
set is a guard line, checked on the layers actually run; it is the balanced
guard lemma that makes it a statement about every layer, and that lemma is taken
as given rather than re-derived.

## 14. The bridge from column counts to survivor mass, measured

Date: 2026-09-21. Status: exploratory, not pre-registered; the quantity had
never been computed and several of its inputs had already been read this
session, so a registration would have been theatre. It is a finite observation
over 45 layers and bounds nothing uniformly.

Every structural fact the lift proves is about COLUMNS -- the entry-supply
lemma, the lift lemma, corollary 3, the SAFE count of section 13 all count
columns. The quantity the survivor-mass floor `mu_(n+1) >= s_n mu_n / 2` needs
is `s_n`, a MASS share. Nothing in this report relates the two, so a counting
argument about columns has never been known to imply anything about the mass.

For the GOOD set, the two are now computed side by side on every layer of all
six families: `s_n` from `cap18_self_sufficient_share.py` and the column
fraction `GOOD_n / |G_n|` from `cap18_safe_set.py`.

| Family | layers | ratio range |
|---|---:|---|
| index 15 | 12-18 | 1.02 - 1.44 |
| index 8 | 8-17 | 0.79 - 1.43 |
| index 23 | 12-18 | 0.68 - 1.26 |
| index 34 | 8-16 | 1.00 - 1.25 |
| index 5, 27 (closed) | 12 layers | 1.00 exactly |

Over all 45 layers the ratio of mass share to column share runs from 0.6809,
index 23 at `n = 12`, to 1.4419, index 15 at `n = 14`. So on everything computed

```text
GOOD mass share  >=  GOOD column share / 1.47,
```

and the distortion does not grow with the survivor set: index 34's ratio runs
1.25, 1.05, 1.01, 1.03, 1.00, 1.09, 1.05, 1.05, 1.01 as `|G_n|` goes from 161 to
8562, and index 8's tightens the same way. If anything it shrinks.

Two limits, and the second is the one that matters. The closed families'
exact 1.00 is degenerate for the third time in this report: there `s_n` and the
column share are both 0 or both 1, so the ratio is 1 by construction and the
rows carry no information. And 45 layers of a bounded ratio is not a bounded
ratio; what a counting argument would need is a distortion bound holding at
every depth, which is a statement about how the parameter mass spreads over the
columns of one layer and is not proved here. What the measurement does settle is
that the bridge is not obviously absent: the mass share does track the column
share closely, on four families with no known answer, over the whole computed
range, so a proof that the GOOD column fraction is bounded below is worth having
rather than being known in advance to say nothing about `mu_n`.

**The per-column distortion grows geometrically, so the aggregate ratio above is
not uniformity.** The ratio of section 14 compares two AGGREGATE shares. It says
nothing about how the mass spreads over the columns of one layer, and the two
behave in opposite directions. Computing `nu_q` per column with the imported
`column_masses`:

| n | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---:|---:|---:|---:|---:|---:|---:|
| index 15, `max nu_q / min nu_q` | 16 | 16 | 32 | 32 | 32 | 64 | 64 |
| index 23, `max nu_q / min nu_q` | 16 | 32 | 64 | 64 | 128 | 128 | 128 |

every value an exact power of two, with `mean/min` rising 2.54 to 6.76 for index
15 and 5.62 to 13.48 for index 23 over the same layers. Index 23's spread
doubles about every two layers, index 15's about every three. So the survivor
mass is concentrating, not equalising, as `|G_n|` grows.

Two consequences, and the second is a kill. The aggregate ratio staying inside
`[0.68, 1.45]` while the per-column spread quadruples means only that column
weight is roughly UNCORRELATED with GOOD membership; it is not a statement that
the columns carry comparable mass, and it must not be read as one. And the
natural way to make the bridge uniform -- bound `max nu_q / min nu_q` and push a
column bound through it -- **is dead**: no such bound exists on this data, the
quantity is geometric in the depth. A usable bridge has to come from the
decorrelation itself, which is not proved and has no candidate mechanism here.
