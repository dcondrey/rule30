# Fresh-session prompt: continue the Rule 30 period-two attack

Copy everything inside the following block into a fresh Codex session whose
working directory is `/Volumes/A/researchpapers/13-rule30`.

```text
Continue the Rule 30 research in this repository autonomously. Do concrete
mathematical and computational work, not merely a plan. The worktree contains
many unrelated user changes in sibling research-paper directories: preserve
them, scope all edits and commits to `13-rule30`, and inspect current HEAD and
status before acting.

WHAT IS AND IS NOT THE TARGET

Let F be elementary cellular automaton Rule 30,

    f(left,center,right) = left XOR (center OR right).

The immediate theorem target is only the remaining period-two rung:

    For every nonzero finite configuration y,
    Tr_0(y) != Tr_0(F^2(y)),

where Tr_0(y)_t = F^t(y)_0. Constant-zero and constant-one center traces have
already been excluded. Phase 1010... reduces after one F step to 0101..., so
the sole remaining case is an exactly alternating center trace. A proof of
this target would settle p=2 only. It would NOT prove arbitrary
nonperiodicity, randomness, normality, computational irreducibility, or the
whole Rule 30 Prize Problem 1.

CURRENT BEST UNIFORM TARGET

Prove the following statement for every m, without a tested-width parameter:

    Active-core diagonal mortality.
    Every aligned core word of length m ending in terminal symbol 3 fails a
    pin or creates 11 within m+1 macrosteps.

The bilateral reduction is already exact: for an alternating center trace,

    rho_k = s(2k,1),
    rho_(k+1) = (NOT rho_k) AND (NOT s(2k,2))
                            AND (NOT s(2k+1,2)).

Hence every actually realizable rho avoids adjacent ones. Every finite left
half reaches a finite knee represented by a core of length at most `2n` for a
seed of length `n`. A UNIFORM proof of active-core diagonal mortality would
therefore give seed mortality within `2n+1` macros and prove the period-two
theorem.

A terminal-3 core of length `m` surviving `m+1` macros would kill this
particular diagonal bound, not the period-two theorem. The weaker seed-only
`2n+2` bound and the broader alternate route remain:

    If rho has no 11 and its exact reconstructed left tail L(rho) is
    eventually zero, prove rho is eventually periodic.

Then the adjacent width-two trace is eventually periodic, contradicting the
already-recorded width-two theorem. Keep this route available if the constant
2 in the linear mortality bound is false.

CANONICAL EXACT FRONTIER DYNAMICS

Do not rederive these. Read finite words shallow-to-deep, stored as
nonnegative integers. Let inverse Gray code be

    I(X) = X XOR (X>>1) XOR (X>>2) XOR ... .

At an even macro frontier (T,A,B), the forced zero-emitting/pin-passing map is

    C = I(A OR (1 OR (B<<1))),
    D = I(C OR (A<<1)),
    pin passes iff D & 1 = 1,
    (T,A,B) -> (T+2,D,C).

The one-row shallow-to-deep recurrence is

    C_1 = v,
    C_(j+1) = C_j XOR (A_j OR B_(j-1)),
    B_0 = (T-1) mod 2.

For a forced zero phase, the new deepest output is constrained to zero, which
uniquely determines v; the next rho bit is NOT v. The next pinned phase has
v=1 and must also have zero new deepest output. In code, use
`carry_transducer.py`: `wf_step`, `parity_or`, `forced_macro`, `gray_macro`,
and `seed_state`. The forced next rho is

    forced_rho(state) = 1 XOR parity_or(state).

Reject before advancing if previous_rho = forced_rho = 1; reject the macro if
the pin is zero.

EXACT SAT FORMULATION ALREADY BUILT

`M(n,H)` in `mortality_sat.py` has n semantic seed inputs and is SAT exactly
when a no-11 seed of length n survives at least H forced post-seed macros. It
Tseitin-encodes the preceding recurrence; it is not a precomputed seed truth
table. Controls and results:

- all 95 thresholds through n=16 match independent integer enumeration;
- every SAT model was decoded and replayed;
- dropping the finite-left/deep-output constraints remains SAT;
- all Fibonacci-language seeds were enumerated through n=24, with cap 512
  and no cap hit;
- maximum survival for n=1..24 is

    2,1,1,4,3,2,2,4,3,8,7,6,5,4,5,6,6,8,8,7,10,12,11,10;

- the largest is 12 at n=22, so a small universal constant bound is dead;
- the proposed H(n)=2n+2 bound survives this finite test, but finite UNSAT is
  not a proof.

Generic proof traces did not expose an induction. Primary M(n,2n+2) DRUP
proofs were independently checked through n=11; n=12 grew to 105,998 raw
lines, 65,543 additions, maximum width 154. Shortest-death proofs
M(n,max(n)+1) were checked through n=17; at n=17 they already had 22,878
additions and maximum width 130. Treat CDCL as a falsifier/certificate
generator, not the likely final proof language. Do not enlarge SAT bounds
just to collect more finite UNSAT.

LATEST FALSIFICATIONS AND UNIFORM LEMMA

Do not resume the former constant or coefficient-seven targets:

- exact joint mortality at horizon eight is false. Right mask `0x13be`
  yields `J(82,10)` SAT. The corresponding finite row has left mask
  `0xa96bfe30260597f6e6d977d63403b1304cb232655`, support `[-164,13]`, an
  alternating center through time 184, and first failure at 185;
- `7 wt(L) >= 2n-2` is false. The length-37 hard-core word
  `0101010101010101010101010101010101000` has `wt(L)=10`, so `70<72`;
- fixed-radius label discharging is already obstructed at radius seven.
  Seed `(n,seed)=(22,0x24a28)` emits `00` while following seven forced rho
  zeros. Seed `(26,0x892512)` does the same along forced rho `01010101`.
  These give a negative self-loop and alternating two-cycle when locally
  legal factors are spliced.

One new all-width lemma is available. Every input-symbol carry action is a
permutation, so a seed append can be read shallow-to-deep starting from the
prescribed carry `(1-rho,rho)`. Composing `H` such reverse transductions gives
an exact `H`-carry cascade with at most `4^H` states that recognizes every
length-`H` emitted-label block over arbitrary frontier width. Read
`RESULTS-CORE-DISCHARGE.md` and use `core_discharge.py`. This is uniform in
width for fixed `H`, but its state grows with `H`; it is not mortality.

The local diagonal CNF `C(m,H)` in `core_mortality_sat.py` asserts survival
of an arbitrary length-`m` aligned word ending in `3`; it is stronger than
the seed CNF. All 36 thresholds through `m=7` match exhaustive word replay,
dropping no-`11` makes `C(6,7)` SAT, and `C(m,m+1)` is UNSAT through `m=34`.
These are exact finite controls only. The missing proof is a symbolic corner
induction for `C(m,m+1)` or another argument uniform in `m`.

The two weaker global balances

    2 wt(L) >= wt(rho),
    2 (wt(L)+wt(rho)) >= n

remain conjectural and together would suffice. Their radius-seven factor
approximations are killed by the preceding cycles, so a proof must retain
global seed compatibility. A corrected bound such as
`7 wt(L) >= 2n-O(1)` is also unproved; changing the additive constant after a
finite sweep is not a theorem.

NEW ROTATED-PEEL IDENTITY

Do not rederive the bridge between the inverse-terminal triangle and Peel.
For `I(e)` the inverse-terminal cut, `sigma` the one-sided shift, and

    P(x)_t = phi(x_t,x_(t+1)),

the exact all-endpoint identity is

    P(I(sigma e)) = sigma^2 I(e),
    P^j(I(sigma^j e)) = sigma^(2j) I(e).

If `I(e)` has positive finite eventual Peel rank `m`, the successive endpoint
tails have exact ranks `m,m+1,...`. A separate support-edge argument handles
rank zero: `phi(s,0)=3` for every nonzero state `s`, so Peel preserves the
rightmost nonzero coordinate of an eventually-zero cut. Combining this with
the displayed identity proves uniformly:

    An eventually periodic hard-core endpoint cannot have a finite-rank
    inverse-terminal cut.

Thus every hypothetical reachable/accepted collision now has an aperiodic
hard-core endpoint. In the positive-rank branch its tail ranks grow exactly
by one; rank zero remains possible only over an aperiodic endpoint. Read
`RESULTS-ROTATED-PEEL-IDENTITY.md` and run `rotated_peel_identity.py`.

The complete reverse-period trees are also decided for exact cut-period
constraints `p=1,2,4,8,16`: `p=1` is empty and each tested positive dyadic
period locks to endpoint `2^omega`. This is parameter-bounded, not an
all-power induction. Endpoint `(12)^omega` mapping to primitive cut period 28
is the retained non-dyadic control.

The next clean target is: rule out an aperiodic hard-core endpoint whose
inverse-terminal cut has finite Peel rank. Use actual-right restrictions as
constraints on the exact tail/rank cocycle, not as another flat
forbidden-factor filter.

NEW RANK-ZERO / CONSTANT-TAIL REDUCTION

The preceding target has now been narrowed further. Prepending endpoint state
2 lowers every positive finite Peel rank by one, so all finite ranks reduce to
rank zero: exclude a hard-core endpoint whose inverse cut is finite support.
The exact prefix grammar and halving identity are

    HC = 2 HC union 12 HC,
    I(qe) = (B(q), phi(q,I(e)_0)) . P(I(e)),
    P^n I(sigma^n e) = sigma^(2n) I(e).

At the first endpoint shift whose inverse cut becomes infinite, its Peel image
is finite. Its tail follows g_0=(0,3,2,3), so the cut is eventually constant 2
or eventually constant 3. Therefore the current proof-bearing target is:

    No cut eventually equal to 2^omega or 3^omega has a hard-core
    terminal-cone endpoint.

Read `RESULTS-RANK-ZERO-REDUCTION.md` and
`RESULTS-EVENTUAL-CONSTANT-TAIL.md`. Run `rank_zero_separator.py` and
`eventual_constant_tail.py`. Also run `constant_tail_shift.py` and
`constant_tail_doubling.py` and `constant_tail_scale.py`. The zero/2/3 tail
censuses are exhaustive through cutoff 23. OpenEvolve plus bit-level GA
controls through cutoff 96 find no
`2T+2` falsifier, but this is finite evidence only. A next evolutionary search
must emit a recursive certificate for both branches of the displayed HC
grammar with the one-symbol boundary mode retained; another numerical horizon
search cannot prove the separator.

Do not promote the observed six-node period-doubling profile to a proof.
Exhausting all primitive four-symbol driver cycles of dyadic lengths through
8 produces four profile collisions at the `8 -> 16` lift.  The exact lifted
cycle word *is* uniformly unique up to rotation whenever a doubling occurs,
because each doubling element of the 13-element monoid has a unique two-cycle.
Thus the viable target is a recursive word-level quotient; the five-component
count/return-transform profile is now a certified negative.
The exact cycle word alone is still insufficient: the prefix-independent
cycle orbit from either constant tail first branches at endpoint shift 26,603
and period 16, when its return map has two fixed points.  A corrected state
must retain the finite-prefix entry state (or a sound quotient of it), not
only the canonical periodic word.

There is now a cleaner scale-invariant finite-word target. The inverse-cut
dependency interval implies that a hypothetical constant-tail hard-core
endpoint would have, at every sufficiently large `n`, hard-core blocks

    W=e[n,2n),       R_c(W)=e[2n,4n),       c in {2,3},

where `R_c(W)` is uniquely forced and independent of all endpoint symbols
before `n`. Exact enumeration separates every `W` through length 22. Prove for
all lengths that `R_c(W)` is not a hard-core continuation. The newest-cut
boundary action has the exact affine form

    (h,l) -> (h+alpha, l+beta*h+gamma)

with only eight triples and composition
`(a,b,g)o(A,B,G)=(a+A,b+B,g+G+b*A)`. Since tails 2 and 3 have high bit one,
the forced endpoint is state `2-alpha`; hard-core becomes no consecutive
`alpha=1`. The remaining obstruction is that the next affine triple depends
on an ordered growing diagonal, so do not collapse it to the current triple
alone.

Do not attempt to prove the former charge `s_2(W)<=#2(W)`: its first exact
counterexample is `W=12212121212121212`, with survival 10 and only nine state-2
symbols. The repaired finite-census targets are

    s_2(W) <= #2(W) + indicator(22 occurs in W),
    s_3(W) <= #2(W) + 3.

Each would suffice for its tail mode and both are exact through length 22, but
neither is proved. The incremental newest-dependency diagonal in
`constant_tail_scale.py` computes each scale block in quadratic time and is
the current order-sensitive coordinate. Prefix/suffix deletion does not
preserve either budget, so seek a path/contact invariant inside that diagonal,
not a flat induction on the word grammar.

The same adaptive formula now has an exact growing-word form.  If `D_m` is
the newest dependency diagonal and `R` its reversal, a constant tail
`c in {2,3}` gives the partial queue update

    S_0=c,  S_i=g_(S_(i-1))(R_i),
    R'=S . B(next endpoint).

The final scan state uniquely decodes the next endpoint and hard-core
legality.  Hence it is sufficient to prove mortality for every finite word
beginning in `c` and ending in `{1,2}`; the middle word may be arbitrary.  The
identity `g_s(1)=g_s(3)` gives an exact `3 -> 1` quotient in every nonleading
coordinate, so ternary representatives cover the full four-symbol language.
The complete determinized scan graph also proves that every normalized
successor avoids exactly the factors `20`, `22`, and `011`; the hard-core
boundary append preserves them.  Restrict any induction to this invariant
SFT after the first update.
The candidate bound `lifetime(R)<=|R|` holds exhaustively through length 15,
but is not proved.  Read `RESULTS-CONSTANT-TAIL-QUEUE.md` and run
`constant_tail_queue.py`.  This coordinate retains the full ordered diagonal
and the prefix-entry information whose loss caused the period-16 branch, so
it is the preferred form for a genuine morphing-formula induction.

The formula morph itself is now implemented exactly.  For `L_h(c)`, the
regular language of invariant queues surviving `h` more updates,

    L_(h+1)(c)=L_0(c) intersect Q_c^(-1)(L_h(c)).

The minimized DFA rank expands as `4^(h+1)+1` through horizon seven; accepting
states have Fibonacci counts.  Therefore strict DFA-rank contraction is a
certified failure, not the missing invariant.  The shortest accepted length
does jump `1/2 -> 3 -> 5 -> 10` with plateaus.  Prove that this minimum tends
to infinity, using an amortized structural argument rather than expecting a
decrease at every morph.  Read `RESULTS-CONSTANT-TAIL-LANGUAGE-COCYCLE.md` and
run `constant_tail_language_cocycle.py`.

The shortest-word metric has an exact frontier graph.  At horizon `h`, stack
the `h+1` queue rows over one input column.  Reading normalized symbol `a`
updates the vertical frontier by

    w_0=a,  w_j=g_(v_j)(w_(j-1)).

Starting from `(c,...,c)`, a path is accepted exactly when it reaches the
inverse-cone diagonal of a hard-core endpoint word of length `h+1`.  There are
provably `F_(h+3)` such targets, and the shortest arbitrary surviving queue is
one plus the directed distance to this set.  This bare distance allows every
ternary queue; taking the product with the `20,22,011` suffix DFA gives the
invariant
language-cocycle minimum.  The two divergence statements are equivalent,
because an immortal arbitrary queue has an immortal SFT successor.  Both
sequences are nondecreasing by nesting but have plateaus.  Exact values
through `h=12` are

    arbitrary tail 2: 1,3,5,5,5,10,10,10,10,16,16,18
    arbitrary tail 3: 2,3,5,5,5,10,10,10,12,12,15,16
    invariant tail 2: 1,3,5,5,5,10,10,10,10,17,18,18
    invariant tail 3: 2,3,5,5,5,10,10,10,13,14,15,16.

Read `RESULTS-CONSTANT-TAIL-FRONTIER-GRAPH.md` and run
`constant_tail_frontier_graph.py`.  The graph equivalence and Fibonacci target
count are uniform; the displayed distances remain only finite evidence.
Height deletion commutes with every labeled graph edge and terminal set.  In
the inverse limit, the theorem is exactly

    {T_u(c^omega): finite ternary u} intersect I(HC_omega) = empty

for `c=2,3`.  Also `P(T_a(v))=sigma(v)`, so a collision reached by a word of
length `d` has `P^d(x)=c^omega` and `P^(d+1)(x)=0^omega`.  This is the same
finite-Peel-rank aperiodic collision isolated by the rank reductions, now as
a precise topological orbit-separation problem.

Height extension is an exact four-sheeted permutation cover.  Writing a
frontier as `(v,z)`, a projected edge ending in symbol `t` sends the fiber to
`K_t(z)`, where

    K_0=(0,1,3,2), K_1=K_3=(3,2,1,0), K_2=(2,3,1,0).

These permutations generate `D8`.  Thus the extra coordinate is transported
reversibly rather than contracted.  A useful next proof must control the
monodromy accumulated by source-to-terminal paths across all cover levels.
This is exactly the eight-map affine boundary group from the scale route.  Its
fiber generators have coordinates

    K_0=(0,1,0), K_1=K_3=(1,0,1), K_2=(1,1,0)

under `(h,l)->(h+alpha,l+beta*h+gamma)`, with the established three-bit
composition law.  For a fixed suffix `u`, the last frontier coordinate at
height `H` is `M_H(u)(c)`.  The live theorem is that no finite `u` can make
`M_H(u)(c)=I(e)_(H-1)` for every `H` and one infinite hard-core `e`.
For fixed `u` of length `d`, the height driver is the exact `4^d`-state map

    s_0=c, s_k=g_(s_(k-1))(r_k), D_c(r)=(s_1,...,s_d).

The rightmost coordinate of `D_c^j(u)` is the infinite frontier output.  Its
eventual period is dyadic, but the driver dimension grows with `d`; the proof
must use the stronger finite-Peel ancestry, since dyadic periodicity alone is
defeated by the accepted `(12)^omega` cut.

The invariant-SFT minimum has now been extended by an exact local PySAT
encoding.  Every model is decoded and replayed by the literal queue map.  For
`h=0,...,20` the values are

    tail 2: 1,1,3,5,5,5,10,10,10,10,17,18,18,18,22,23,23,26,26,30,33
    tail 3: 2,2,3,5,5,5,10,10,10,13,14,15,16,16,24,24,26,26,31,31,32.

Thus `m_h(c)>=h` and the sufficient bound `lifetime(R)<=|R|` survive the
displayed instances, but neither is proved.  Run
`constant_tail_queue_sat.py` in the `experiments/sygus-p3` environment.
Ordinary local additive energies, even with endpoint terms, did not explain
these minima in small exact probes; seek a noncrossing ancestry, recursive
grammar, or stack rank.

The Fibonacci numbers here have one exact source: endpoint words over
`{1,2}` avoiding `11`, hence `|A_h|=F_(h+3)`.  Cardinality alone cannot prove
orbit separation.  A scalar first-illegal-position induction also fails
structurally.  For any hard-core endpoint prefix beginning in state 1, put
`y=I(e)` and choose `v` with `sigma(v)=P(y)`; the unique inverse lift with
initial symbol `y_0=2` recovers `y`.  Therefore one inverse-Peel lift can
replace an immediately invalid predecessor endpoint by an arbitrarily long
hard-core endpoint prefix.  Any Fibonacci/Zeckendorf attempt must retain the
complete prefix grammar or equivalent ancestry, not just terminal counts or
the first defect.

For the original period-two application there is a useful weaker target.
The endpoint before rank descent is the genuine even-time right trace.  Rank
descent and the first-infinite shift change only a finite prefix, so at every
sufficiently large scale `W R_c(W)` is a factor of that actual right trace.
It is enough to prove that no actual-right factor `W` has `R_c(W)` as an
actual-right continuation.  Exact right-light-cone SAT membership gives

    scale:  10 15 20 24 27
    tail 2:  4  4  4  4  5
    tail 3:  5  3  4  5  5.

At scale 27 the current finite-factor relaxation permits 7 and 9, while the
full right language lowers both to 5.  This is finite evidence, not a
universal constant-five theorem.  See `constant_tail_right_filter.py` and
`RESULTS-EVENTUAL-CONSTANT-TAIL.md`.

The complete actual-right terminal frontier product has also been audited.
For

    A_h^right={I(e): bits(e) is a complete length-(h+1) actual-right trace},

height deletion satisfies the uniform equality

    pi_h(A_h^right)=A_(h-1)^right.

Counts through h=12 are

    3,5,8,12,17,25,36,50,68,91,119,156

instead of the hard-core Fibonacci counts ending at 610. The tail-2 arbitrary
minimum at h=12 rises from 18 to 23. Augmenting paths by the exact D8 action
shows all eight phases by h=7, but phase-conditioned costs separate strongly
by h=10. Read `RESULTS-ACTUAL-RIGHT-FRONTIER.md` and run
`constant_tail_actual_frontier.py` in the `experiments/sygus-p3` environment.

Do not use whole-prefix actual-right conditioning as a period-two proof.
Rank descent replaces an actual endpoint e by `2^m e`, and the first-infinite
shift may retain part of that artificial state-2 prefix. The relevant endpoint
is only eventually actual-right. Since arbitrary finite hard-core prefixes
can precede an actual-right tail, the raw finite terminal language then
collapses back to the hard-core one. Actual-right information is valid only
beyond a prefix bound carried by the source/Peel ancestry, or in the scale
block chosen beyond both finite prefixes. This scope correction is
load-bearing.

The exact moving-formula update is also now known. If endpoint coordinate k is
changed from 1 to 2, the inverse cut changes only on [k,2k+1], and it changes
at k. Flipping hard-core 1s left-to-right therefore gives a sequence of finite
cut formulas with compact, position-dependent rewrite zones. An eventually
zero or constant-3 cut requires these zones to cover the late cut axis; a
constant-2 cut requires them to cover every late even coordinate. In all three
cases consecutive defect positions obey k_(i+1)<=2k_i+2, while hard-core gives
k_(i+1)>=k_i+2. This is not a contradiction: supports can escape while each
formula remains finite. Read `RESULTS-ENDPOINT-FLIP-COCYCLE.md` and run
`endpoint_flip_cocycle.py`. The next certificate must control exact overlaps
of these ordered rewrite intervals, not merely their count or outer support.

EXACT TRIANGULAR CORRELATION LEMMA

Let P_w be suffix XOR on width-w vectors:

    (P_w x)_k = XOR_(j>=k) x_j.

Then over F_2,

    <P_w x,P_w y> = x^T K_w y,
    (K_w)_(i,j) = (min(i,j)+1) mod 2,
    rank(K_w) = w.

The even- and odd-output pieces have ranks ceil(w/2) and floor(w/2).
Therefore inverse-Gray correlation is structured and triangular, but its
separable bilinear rank grows unboundedly. A 37-bit summary containing
T mod 16, split parities/endpoints of A,V,C,S, and every pairwise split
inverse-Gray correlation has an equal-depth reachable closure collision at

    T=32, previous rho=0,
    seed 0x200 length 15 follow 1:
        (32,1431655765,984962389)
    seed 0xa20 length 15 follow 1:
        (32,1431655765,716879189).

Both force rho=1, pass the pin, preserve no-11, and have equal current
summaries but different successor summaries. Do not retry bounded quadratic
summaries by merely adding a few more parity bits.

An immediate endpoint identity worth exploiting (verify it in the retained
checker before using it) is: when w is even and e_i=(i+1) mod 2,

    K_(w+2) = [ K_w   e   e ]
              [ e^T   1   1 ]
              [ e^T   1   0 ].

Likewise, appending deep bits a,b gives

    (P_(w+2)(x,a,b))_k = (P_w x)_k XOR a XOR b,  k<w,
    output_w = a XOR b,
    output_(w+1) = b.

The forced recurrence makes the new deepest outputs zero. The best current
hope is to turn this moving-endpoint block recurrence into a well-founded
statement tied to those zero outputs, rather than compressing K_w to a fixed
finite summary.

ORDERED-BOUNDARY OPERATOR ATTEMPT ALREADY KILLED

The exact four carry states, the eight D8 prefix actions, and D8 x carry were
tested as deterministic weighted observers. Small exact Farkas-style
multisets prove that no bounded-below additive regular edge cost on these
controls strictly decreases on every surviving macro. D8 x carry is not a
real refinement: from zero carry, carry is the current D8 action applied to
zero. The D8 x depth-parity observer was solver-inconclusive, not positive.
Do not extend it by more runtime or seed length without a new exact strategy.
Non-additive/reset/stack-like ordered certificates and a full moving-endpoint
triangular argument remain open.

OTHER RETIRED CLASSES — DO NOT REPACKAGE THEM

- fixed-local additive rankings: exact Farkas obstructions;
- finite modular/count/endpoint summaries: same-summary/different-future
  collisions;
- every fixed Hasse order: H_k(I(X))=H_k(X) XOR H_(k+1)(X), so it needs the
  next order; rich reachable equal-depth collisions also exist;
- carry contraction: all four-symbol actions are permutations generating D8;
- bounded D8 lookahead/action summaries: closure collisions;
- bounded run-length/gap projections: collisions; the full ordered gap list
  is lossless but unbounded;
- natural signed/contact/boundary counts: exact oscillating transition
  multisets;
- odd-row complement/toggle: two phases compose back to exactly F^2;
- hard-core plus fixed D8 action: closure collision;
- the 37-bit split triangular-correlation summary described above.
- the joint constant-eight/sixteen-zero-gap theorem;
- the exact coefficient-seven bound `7 wt(L)>=2n-2`;
- radius-seven emitted-label factor discharging for either weaker balance.

Do not "improve" these merely by increasing locality, moment order, endpoint
window, lookahead, seed bound, or runtime. A genuinely new attempt must
retain an unbounded ordered object with an exact proof mechanism, or give a
symbolic induction that removes n.

LOAD-BEARING CONTROLS

- Rule 30 finite row {-8,-1,6} alternates through t=14 and first fails at
  t=15. Never reject it earlier.
- The finite Rule 30 row with right mask `0x13be` and left mask
  `0xa96bfe30260597f6e6d977d63403b1304cb232655` alternates through t=184 and
  first fails at t=185. This supersedes the shallow control as the strongest
  known prefix trap.
- Rule 90 finite row {-1,1} has zero center forever. Any generic argument
  that also excludes this is invalid. Rule 30's no-11 lemma uses OR and must
  not be transferred to Rule 90's XOR.
- An infinite-left spatial-period-7 wallpaper with finite right part {1,4}
  survives the alternating fiber. Therefore finite-left support is
  essential; any invariant excluding the wallpaper has silently discarded a
  valid infinite-left control.
- Forward support expansion is not a contradiction. Any "escape" must map
  exactly to distinct nonzero cells of the fixed reconstructed initial tail
  L(rho), or prove mortality.
- Finite data can falsify a universal claim but cannot prove it.

ASSESSMENT OF THE FOUR EXOTIC FRAMEWORKS

The non-Hermitian, trans-adic, sheaf, and hyperbolic-thermodynamic proposals
were assessed. Their broad ingredients already exist in literature; their
specific Rule 30 mappings have not been established as novel. As stated:

- non-Hermitian skin-effect mapping has low merit: a state-dependent,
  changing Hilbert space is not a fixed linear operator with comparable
  spectral winding, an exceptional point is a parameter-space singularity,
  and periodicity of one observed column does not imply closure of the global
  operator orbit;
- a trajectory-dependent trans-adic metric is circular, Poincare recurrence
  does not apply without a finite invariant measure, and negative curvature
  does not forbid closed geodesics;
- hyperbolic thermodynamics lacks a proved bridge from embedding-dependent
  surface tension/conductivity to central-column periodicity or algorithmic
  complexity;
- sheaf local-to-global language has the most merit only after conversion to
  an exact constraint system. The mortality CNF is already a concrete
  version. Ordinary sheaf cohomology also needs abelian/linear stalk data,
  and nonzero H^1 does not automatically preclude H^0 global sections.

Do not pursue an exotic reformulation unless every map is canonical and the
claimed implication back to Rule 30 is proved independently; decorative
geometry is not progress.

FILES TO READ FIRST — DO NOT LOAD THE WHOLE ARCHIVE

1. `experiments/rule30/p1-period2-invariant/README.md`
2. `experiments/rule30/p1-period2-invariant/RESULTS-JOINT-MORTALITY.md`
3. `experiments/rule30/p1-period2-invariant/RESULTS-TAIL-DENSITY.md`
4. `experiments/rule30/p1-period2-invariant/RESULTS-CORE-DISCHARGE.md`
5. `experiments/rule30/p1-period2-invariant/carry_transducer.py`
6. `experiments/rule30/p1-period2-invariant/core_discharge.py`
7. `experiments/rule30/p1-period2-invariant/RESULTS-CORE-MORTALITY-SAT.md`
8. `experiments/rule30/p1-period2-invariant/RESULTS-CORE-INTERPOLANT.md`
9. `experiments/rule30/p1-period2-invariant/core_mortality_sat.py`
10. `experiments/rule30/p1-period2-invariant/core_interpolant_probe.py`
11. `experiments/rule30/p1-period2-invariant/mortality_sat.py`

The matching preregistrations are the audit trail. Read another historical
result only if the compact README routes you to it.

LATEST SCALE-TELESCOPING RESULT

The old pointwise source-2 intervention program is killed at length 21.
`W=122212222222221212122`, tail 2, has survival 12 but the full affine
intervention graph plus its contact credit matches only 11 rows; the full
derivative rank is 10 against target 11. Do not revive pointwise sensitivity,
scalar selectors, or affine-rank certificates.

The live target is the zero-prefix chain `W^(k)=0^k W[k:]`. Let `A_(j,k)` be
the newest affine boundary permutation at forced scale row `j`. Starting after
the previous token, greedily choose the least `k` with
`A_(j,k)!=A_(j,k+1)`. Exact bit-sliced/slow audits through length 22 give zero
failures in 242,783 cases: tail 2 matches every survival row; tail 3 matches
every nonfinal survival row and may miss only the final row. Hence the uniform
lemma would prove `s_2(W)<=|W|`, `s_3(W)<=|W|+1`, both constant-tail
separators, and the alternating-center exclusion. This is not proved. The
next task is a leading-term/Peel induction on the ordered zero-prefix finite
differences. Read `RESULTS-SCALE-TELESCOPING.md` first.

REPRODUCTION COMMANDS

    uv run --project experiments/sygus-p3 python \
      experiments/rule30/p1-period2-invariant/mortality_sat.py \
      --validate --max-validate 16

    uv run --project experiments/sygus-p3 python \
      experiments/rule30/p1-period2-invariant/quadratic_probe.py \
      --max-width 8 --max-seed 16 --max-follow 32

    python3 experiments/rule30/p1-period2-oboc/verify_oboc_negative.py

    python3 \
      experiments/rule30/p1-period2-invariant/core_discharge.py

    uv run --project experiments/sygus-p3 python \
      experiments/rule30/p1-period2-invariant/core_interpolant_probe.py

WORKING METHOD FOR THIS SESSION

1. Inspect current HEAD/status and read the eleven routed files above.
2. Reproduce the lightweight controls before relying on them.
3. Before any substantive new search, write a dated preregistration fixing
   the candidate certificate, success criterion, controls, resource limits,
   and kill conditions.
4. Prefer a symbolic derivation. Computation should seek counterexamples,
   exact identities, or a parameterized proof schema—not a larger finite
   horizon.
5. The recommended first attack is a symbolic induction on the full
   seed-generated compatibility object. Viable forms are an unbounded
   interval grammar with a well-founded stack/multiset rank, or an
   `n`-to-`n+1` interpolant whose closure is checked independently. Use the
   reverse cascade to make fixed-horizon obligations exact, but do not promote
   another bounded factor graph: radius seven is already false. If the
   induction fails, find the smallest exact reachable collision/cycle and
   record the whole certificate class that it kills.
6. Do not claim success unless the argument quantifies over all n and the
   reduction to the alternating finite-support fiber is explicit.
7. Update the compact README and write a result report. Preserve failures as
   useful exact negatives. Run independent controls, then commit only scoped
   Rule 30 artifacts.

At the end, tell me plainly whether we proved the period-two theorem, found a
uniform intermediate lemma, or only obtained a finite/negative result. If a
uniform period-two theorem is proved, also state clearly that it is still only
the p=2 rung and not yet a full solution of Rule 30 unpredictability.
```
