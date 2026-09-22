# Episode continuation: boundary bounds, erased history, and a repeat-budget test

Date: 2026-09-09. Based on commit `d5c9e2a`.

The composition law now yields a stronger bound on a following zero episode.
It does **not** yield a cumulative resource spent at every switch. Exact
inverse counts and accepted-history witnesses explain two specific failures
of that proposed interpretation.

A concrete remaining candidate is the total repeat budget
`N - number_of_runs <= initial_length - 1`. It survived an exhaustive census
through initial length twelve. It is a conjecture, not a theorem. P1, P2,
and unrestricted frontier mortality remain open.

All states and examples use the legal finite Z-frontier universe defined in
[the composition report](RESULTS-variable-length-episode-composition.md) §1.
No witness is claimed to be a frontier of the original lone-seed orbit.

## 1. Uniform bound carried into a following episode

Write `(A_d,B_d)` for bits at inward depth d from the current terminal end.
A successful update with scalar q produces the boundary pattern

```
(A_0,B_0)=(1,1 XOR q),    (A_1,B_1)=(q,q).             (1)
```

**Theorem.** A legal frontier of length R>=3 satisfying (1), for either q,
admits at most `R-3` consecutive scalar-zero updates. In particular this
holds for every one-step image, and at every episode onset after at least
one successful update. The previous bound was `R-1`.

**Proof.** The backward-depth equations are the exact identities proved in
the composition report §5:

```
A_d(t) = A_(d-1)(t) XOR (B_(d-1)(t) OR A_(d-2)(t-1)),
B_d(t) = B_(d-1)(t) XOR (A_(d-1)(t-1) OR B_(d-2)(t-1)). (2)
```

After the first successful zero update, the new boundary has `A_1=B_1=0`.
Equation (1) and (2) give

```
A_2 = 0 XOR (0 OR 1) = 1,
B_2 = 0 XOR (q OR (1 XOR q)) = 1,
A_3 = 1 XOR (1 OR q) = 0.
```

After t>=1 consecutive zeros, induction therefore gives

```
A_d(t) = (d-1) mod 2,  1<=d<=2t+1,
B_d(t) = (d-1) mod 2,  1<=d<=2t.                     (3)
```

Only existing physical sites are asserted. To advance the induction, use
(2) in increasing d. The previous-time terms needed at the two new depths
are inside the old ranges; consecutive alternating values make their OR
equal one. This extends both ranges by two. At `t=R-2`, site zero has
depth `R+t-1=2t+1`. Equation (3) forces its high bit to zero, contradicting
the invariant `a_0=1`. Thus that many zeros cannot survive.

The small-length exception matters: the one-symbol frontier `3` emits `10`,
so its length-two image really admits one zero. At R=4 the new bound is
attained: frontier `201` emits `00`, and its first image admits one zero.

Consequently a successful two-run tape `1^a 0^b` begun at length r satisfies

```
b <= r+a-3,    provided r+a>=3.                       (4)
```

This is a genuine consequence of retaining the preceding update's boundary
data. It is not specific to a switch: (1) works for both values of q.

There is also a stronger **arbitrary-frontier scalar-one bound**:
`L<=r-2` for r>=2, with the r=1 exception `L=1`. A first successful one
already forces `A_1=1,A_2=0,B_1=1`. The same induction gives the constant-one
pattern `1 XOR ((d-1) mod 2)` through A-depth 2t and B-depth 2t-1.
At `t=r-1`, site zero has even depth `2r-2`, forcing its high bit to zero.
This strengthens the composition report's valid but weaker `L<=r` bound.

## 2. The boundary credit does not accumulate with switches

The preceding bound uses two cells that every successful update recreates.
Counting switches does not let the proved constant-pattern range extend
indefinitely farther into the frontier.

For example, legal frontier `200110` emits `10111`, reaching
`21320303032`. There have been two switches and the current one-run has
length three. In that state the constant-one pattern holds through A-depth
7 and B-depth 6. Immediately beyond those ranges,

```
A_8=1, while the constant-one pattern predicts 0;
B_7=0, while the constant-one pattern predicts 1.
```

Thus simply adding these two-depth credits across switches is false. This
witness refutes that particular propagation invariant; it does not refute
every possible cumulative quantity.

## 3. Exact inverse fibers: preserving continuation does not retain a unique past

The earlier composition theorem preserves continuation of a specified
frontier and accepts a prescribed tape only when every guard passes. It
does not claim that the endpoint encodes that tape injectively.

Here is an explicit inverse formula for its suffix map R_s. Let the output
T consist of m pre-append pairs `(u_i,v_i)`, followed by the appended symbol,
where m>=1. Reject unless its last pre-append pair is `(s,s)` and its last
symbol is `3-s`. Define

```
E_0 = {0,1},
E_i = {a in {0,1}: v_i OR a = u_i XOR u_(i-1)}, i>=1.
```

Then the exact number of predecessor suffixes is

```
|R_s^(-1)(T)| = 2 * |E_(m-1)|
  * PRODUCT_(i=0..m-2)
      #{(a,b): a in E_i, b in {0,1}, a OR b = v_(i+1) XOR v_i}. (5)
```

**Proof.** Rearranging the two scan equations separately constrains a_i by
E_i and constrains the disjoint block `(a_i,b_(i+1))` by the displayed OR
equation. The last high bit is chosen separately; b_0 is unused by R_s and
has two choices. These choices partition all input variables, so their
counts multiply. Each nonzero count is a product of powers of two and three.

For a fixed prefix exit memory `(U,V,alpha)`, impose the exact compatibility
guard by replacing the leading factor two with

```
#{b in {0,1}: alpha OR b = V XOR v_0}
```

and replacing E_0 with `{a: v_0 OR a = U XOR u_0}`. This is an exact guarded
inverse count. With entering memory zero and E_0 additionally restricted to
a=1, it counts every legal whole-frontier predecessor under Z. Empty suffixes
are handled separately by the original terminal test.

The guarded fiber can be singleton even when the ambient fiber has four
members: prefix `20`, scalar zero, output suffix `03` accepts only the
one-symbol predecessor suffix `1`. Ambient information loss is therefore
not a guaranteed collision within a specified frontier's accepted histories.

Erasure also occurs on actual accepted trajectories:

```
20000013 --1110--> 212103210303
20000111 --0110--> 212103210303.
```

Both tapes pass every compatibility guard and the frozen direct update.
Their full endpoints coincide. Even the common prefix `20000` can be retained
as the cut in the composition law.

Nor is one-step inverse multiplicity monotone at repeated scalars. Seed
`302` emits `00`, with legal predecessor counts increasing from 2 to 12.
Seed `20001` emits `0010100`; its final repeat decreases the count from
648 to 216. These count all legal predecessors, not a history-conditioned
reachable set. They exclude this simple multiplicity charge in either
direction, without excluding a more refined lineage argument.

## 4. The repeat budget remains a concrete unproved target

For N successful emissions grouped into m maximal constant runs, put

```
D = N-m = #{j: 1<=j<N and s_j=s_(j-1)}.
```

The candidate is `D<=r-1`, where r is the initial length, for every successful
prefix of the same frontier. A uniform proof would bound the total number
of repeated neighboring scalars in an infinite tape, forcing that tape to
be eventually alternating. That is a specific target beyond the composition
identity. No such proof is supplied here.

The exhaustive census covers **11,184,810 legal starts of lengths 1–12**,
evolved completely to death with a cap that raises an inconclusive error.
No repeat-budget violation occurred. Because D is nondecreasing as a tape
is extended, checking the complete tape covers all its prefixes. Maximum D
at each starting length was

```
r: 1 2 3 4 5 6 7 8 9 10 11 12
D: 0 0 1 1 2 3 4 3 6  7  6  7.
```

The separate candidate `a+b<=r+1` survived **2,763,985 episode pairs** in
the same census, with r measured at each pair's onset. These are finite
observations. Neither the new boundary bound nor (5) proves either candidate.
The depth-credit and multiplicity witnesses above explain why two immediate
attempts to turn those observations into a resource fail.

## 5. An exact next tool was executed: prescribed-tape preimage languages

For a regular language L of legal frontiers define

```
Pre_s(L) = {w legal: Z(w) survives with scalar s and Z(w) belongs to L}.
```

This is computed exactly by a product of L's DFA state q, the eight scan
memories h, and an initial-symbol legality flag. Reading a symbol emits y
and advances q by y. Acceptance requires terminal memory `(s,s,alpha)` and
acceptance of q after the appended symbol `3-s`. This proves exactness for
every starting length. For chronological tapes,

```
Pre_(alpha gamma)(L) = Pre_alpha(Pre_gamma(L)).         (6)
```

Unlike enumerating frontier states at a fixed length, each resulting DFA
recognizes all starting lengths. Breadth-first search therefore certifies
the globally shortest frontier that realizes that particular finite tape.
The full chronological tape is imposed; no episode boundary is reset.

The implementation completed **44 constant and two-run languages**, with
7,480 membership comparisons against direct evolution on all legal starts
of lengths 1–4, plus independent replay of all 44 shortest witnesses.
For constant tapes of lengths 1–7 the exact minimum starting lengths are

```
zero: 2, 3, 7, 9, 10, 15, 18
one:  1, 4, 8, 10, 11, 16, 19.
```

Every completed tape of length n had minimized DFA size
`10,34,130,514,2050,8194,32770` for n=1–7. No states merged during
minimization in those cases. The observed formula `2*4^n+2` is not claimed
as a uniform theorem. The two constant length-eight tapes and both
four-plus-four episode tapes hit the 100,000 raw-state cap before completion.
No minimum length or minimized size is inferred for those four cases.

Thus this is an executable exact language method, but the current experiment
provides no compact automaton induction for arbitrary episode lengths.

## 6. Reproduction and scope

From the project root:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python experiments/rule30/episode-composition/verify_resources.py
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python experiments/rule30/episode-composition/preimage_languages.py
```

The first command writes `resources-verification.json`. It checks 816
ambient fibers, 1,120 guarded fibers, 816 legal-origin fibers, and all 2,728
candidate outputs through predecessor length four, including outputs with
no predecessor. It independently replays the displayed witnesses and checks
the proved bounds on 1,736,604 zero runs with the birth pattern and 4,172,082
one runs. The second writes `preimage-languages.json`. Both record source
hashes; the original scan, macro, and direct engines remain unchanged.

The all-length results are the boundary-pattern bound, the scalar-one bound,
the inverse product formula, and exactness of the regular-language operation.
The repeat and pair budgets are unproved; computed minima are for specified
finite tapes. The missing mortality argument is still a uniform bound on
what successive episodes can collectively sustain.

## Follow-up, 2026-09-09: exact phase resets and rank obstructions

A static first-defect height now gives a nonlinear rank that decreases at
every repeat. Switches reset that height exactly to one or two, and the
rank increases by elapsed time across same-phase returns; its refill can
be arbitrarily large. Exact rational certificates rule out phase-aware
additive scan ranks even on actual second images, separately by sector.
An all-length pumping family also rules out unit-drop ranks depending only
on inverse crossing counts, phase, sector and actual length on third images.
These results do not refute the repeat budget. See
[RESULTS-repeat-budget-phase-reset.md](RESULTS-repeat-budget-phase-reset.md).
