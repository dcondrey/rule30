# RESULTS — arm "anf": algebraic degree of the iterated Rule 30 center-bit function

STATUS: PROVED — for every t >= 3, deg f_t = 2t-1 exactly, and the unique monomial of that
degree is M_t = prod_{i=-t+2}^{t} y_i. The upper bound and top-monomial confinement are proved
by induction (below); the surviving-coefficient claim C1, which was the arm's open obligation
through most of this run, was proved tonight via a self-similarity recursion and is recorded in
full below. No published theorem gives deg f_t for general t (triage sweep); ARM4 measured the
law to t = 10 without proof.

Pre-registration: PREREG-anf.md (+ Addendum 1, written before any run beyond the substrate
selftest). Triage: TRIAGE.md row 9. Prior art anchors: ARM4-frequency-domain.md SS3 (measured
the degree law to t = 10; no proof), Meier-Staffelbach EUROCRYPT '91 (exploited low-order
structure of the same function family; no degree theorem). Per the triage literature sweep, no
published theorem gives deg f_t for general t.

## Objects

f_t : {0,1}^(2t+1) -> {0,1}, the center bit s(t,0) as a Boolean function of the time-0 cells
y_{-t}..y_t (radius-1 light cone). Rule: s(u+1,x) = s(u,x-1) XOR (s(u,x) OR s(u,x+1)),
i.e. l + c + r + cr over GF(2). M_t denotes the monomial prod_{i=-t+2}^{t} y_i (degree 2t-1,
missing exactly the two leftmost light-cone cells).

## Theorem (PROVED, unconditional)

For every t >= 3:
  (i)  deg f_t <= 2t-1;
  (ii) the only monomial of degree 2t-1 that can occur in f_t is M_t;
  (iii) every monomial of f_t containing y_{-t} is the linear monomial y_{-t} itself.

With the parity input C1 (below): coeff(M_t) = 1, hence deg f_t = 2t-1 exactly, with unique
top monomial M_t.

### Lemma 1 (iterated left-permutivity; classical, cf. repo Lemma-1 usage)

s(u,x) = y_{x-u} XOR g_{u,x}(y_{x-u+1}, ..., y_{x+u}). Induction on u: the OR-term of the
update involves only s(u,·) at cells x, x+1, whose light cones exclude y_{x-u-1}; the linear
term s(u,x-1) contributes y_{x-u-1} linearly. By uniqueness of ANF this proves (iii) at
every level, and every s(u,x) is balanced.

### Inductive step (t -> t+1)

Write f_{t+1} = A + B + C + BC over GF(2), where A = s(t,-1), B = s(t,0), C = s(t,1) as
functions on cells -t-1..t+1. By Lemma 1, B = y_{-t} + g_B with g_B = f_t|_{y_{-t}=0} on
cells -t+1..t, and C is y_{-t}-free on cells -t+1..t+1.

(a) Monomials containing y_{-t-1}: only A involves y_{-t-1}; by Lemma 1 only linearly.

(b) Monomials containing y_{-t} but not y_{-t-1}, of degree >= 2t: A's y_{-t-1}-free part has
degree <= 2t-1 (induction (i), shifted), so its monomials have degree <= 2t-1; B contributes
y_{-t} linearly; BC = y_{-t}*C + g_B*C, and the coefficient of a y_{-t}-containing monomial m
in y_{-t}*C equals the coefficient of m \ y_{-t} in C. For deg m >= 2t+1 this needs a
C-monomial of degree >= 2t, impossible by (i) at t. For deg m = 2t it needs a C-monomial of
degree 2t-1, which by (ii) at t can only be C's top M_t shifted right by one; so at most one
degree-2t monomial contains y_{-t}, namely Q = y_{-t} * prod_{i=-t+3}^{t+1} y_i, present iff
coeff(M_t) = 1, and in any case BELOW the top layer. (Q misses cells {-t-1, -t+1, -t+2}, i.e.
variable indices {0,2,3} — exactly the persistent [0,2,3] outlier observed in the measured
second layer at every t <= 13, an independent consistency check of this analysis against
runs/overnight/anf/sweep.json.)

(c) Monomials free of both y_{-t-1} and y_{-t} live on the remaining 2t+1 cells, so degree
<= 2t+1. With (a) and (b): deg f_{t+1} <= 2t+1. This is (i) at t+1.

(d) A degree-(2t+1) monomial must be the full product over cells -t+1..t+1, i.e. M_{t+1}:
(a) kills y_{-t-1}-containing candidates, (b) allows y_{-t}-containing ones only at degree
<= 2t, and on 2t+1 cells the only degree-(2t+1) monomial is the full one. This is (ii) at t+1.

(e) coeff(M_{t+1}) = parity of #{y : g_B(y) = 1 and C(y) = 1} over the 2t+1-cell cube
(A, B, C are too low-degree to contribute; y_{-t}*C cannot produce a y_{-t}-free monomial;
for the product g_B*C the full-monomial coefficient is the mod-2 count of joint ones).

Base t = 3: exact ANF (anf_probe.py): deg = 5, top layer = {M_3}, coeff(M_3) = 1.

### The former obligation: C1 (now proved, two subsections below)

C1(t): with cell -t fixed to 0 and cells -t+1..t+1 free (2t+1 variables),
    N(t) = #{ y : s(t,0) = 1 AND s(t,1) = 1 }  is ODD.

By (e), coeff(M_{t+1}) = N(t) mod 2. First VERIFIED N(t) odd for t = 2..12 (parity_probe.py),
then reduced (R2'-R5) and PROVED for all t (see "C1 PROVED" below), which is what closes the
theorem. Also PROVED en route: the UNRESTRICTED pair count (cell -t free too) is even for
every t (pair on y_{-t}, which flips s(t,0) and fixes s(t,1); balancedness of s(t,1) does the
rest) — so C1 is genuinely about the restricted half-cube.

### Reduction chain on C1 (each link VERIFIED numerically; derivations elementary)

A first three-prover adversarial workflow on C1 died on a session quota limit; the chain below
was then derived and checked directly, and it is what made the eventual proof tractable by
turning C1 into a statement about t variables instead of 2t+1.

- (R1) VERIFIED t = 2..7, exhaustively over the full cube:
  d f_t / d y_{-t+1} = t + sum_{u=0}^{t-1} s(u, u-t+2)  (mod 2).
  A closed form for the left derivative in terms of one antidiagonal. Not used below; recorded
  because it is exact and independently checkable.
- (R2') PROVED and VERIFIED t = 2..8: N(t) mod 2 = parity over the 2t-cube (cells -t+1..t) of
  g_B * D_R, where D_R = d s(t,1) / d y_{t+1}. Proof: split the (2t+1)-cube on the last cell;
  the integer count collapses mod 2 to the derivative in that cell.
- (R3) PROVED and VERIFIED t = 2..9: D_R = AND_{u=0}^{t-1} (1 XOR s(u, t-u)).
  Proof: flipping y_{t+1} propagates only along the antidiagonal chain; at each step it passes
  the OR iff the c-cell s(u,t-u) is 0, and those c-cells have light cones excluding y_{t+1}.
- (R4) Hence C1(t) <=> M(t) := #{ w on cells -t+1..t : s(t,0) = 1 and s(u,t-u) = 0 for
  u = 0..t-1 } is ODD. VERIFIED by brute force: M = 1, 5, 5, 15, 33, 65, 117, 253 for t = 2..9,
  all odd.
- (R5) The t wedge conditions s(u,t-u) = 0 are left-permutive in y_{t-2u}, so they determine
  the t cells y_t, y_{t-2}, ..., y_{-t+2} triangularly from the t free cells y_{t-1}, y_{t-3},
  ..., y_{-t+1}. So M(t) is a weight over a 2^t cube, not 2^(2t+1): C1 becomes "the restricted
  function h_t on t variables has odd weight", equivalently "h_t contains its full degree-t
  monomial". This is the same shape as the original claim on exponentially fewer variables,
  and it is what makes verification far past t = 13 cheap (wedge_reduction.py).

### C1 PROVED (self-similarity recursion)

Notation: v_k = y_{t+1-2k} are the t free wedge cells (v_1 = y_{t-1}, ..., v_t = y_{-t+1});
h_t(v) = s(t,0) restricted to the wedge variety, so M(t) = weight(h_t); h_0 := 0, h_1 = v_1.

- (S1) Pointwise self-similarity. Fix u >= 1 and cells z_0..z_{2u} at consecutive positions
  p..p+2u at any time tau. If s(tau+j, p+2u-j) = 0 for j = 0..u-1, then
      s(tau+u, p+u) = z_0 XOR h_u(z_{2u-1}, z_{2u-3}, ..., z_1).
  By L1 none of the constraints involve z_0 except as a bare leading term; processing
  j = 0..u-1 determines z_{2u}, z_{2u-2}, ..., z_2 triangularly from the odd cells, so the
  constraint set is a graph of size 2^(u+1); setting z_0 = 0 reproduces the parameter-u wedge
  problem verbatim, whose apex is h_u by definition. CA homogeneity gives the general (tau,p).
- (S2) The wedge solved. Applying S1 to the block y_{t-2u}..y_t, condition W_u reads
  0 = y_{t-2u} XOR h_u(v_1..v_u), so the determined cells are y_{t-2u} = h_u(v_1..v_u),
  independent of t. The variety is exactly the graph
  R(v) = (0, v_t, h_{t-1}, v_{t-1}, h_{t-2}, ..., v_2, h_1, v_1, 0).
- (S3) Recursion. Evolving R(v) one step gives leftmost cell v_t OR H (H := h_{t-1}(v')) and
  s(1, t-2k) = w_k := v_{k+1} XOR (h_k(v_1..v_k) OR v_k) for k = 1..t-1, with s(1,t-1) = 0.
  Row 1 satisfies S1's hypotheses with u = t-1 (they are exactly W_1..W_{t-1}), so
      h_t(v) = (v_t OR h_{t-1}(v')) XOR h_{t-1}(w_1, ..., w_{t-1}).
- (S4) Parity. Summing over v in {0,1}^t: the first term contributes
  sum_{v'} h_{t-1}(v') + 2^(t-1) = M(t-1) + 2^(t-1) = M(t-1) mod 2. For the second, with v'
  fixed the map v_t -> w_{t-1} is a bijection of {0,1} while w_1..w_{t-2} are unchanged, and
  the map v' -> (w_1..w_{t-2}) is triangular in v_2..v_{t-1} with v_1 never an output
  coordinate, hence exactly 2-to-1 onto {0,1}^(t-2); so that sum is even.
  Therefore M(t) = M(t-1) mod 2, and with M(1) = M(2) = 1, M(t) is odd for every t. QED.

Verification status of the proof itself. The argument was produced by one of three independent
prover agents, passed its adversarial verifier (which re-derived everything with its own code
and indexing and tested each general claim at t = 7, 8, 9, finding only a cosmetic notation
issue in S4 where an integer inner sum is written with XOR — harmless, the argument is mod 2),
and was then re-checked here by a third independent implementation
(verify_c1_proof.py, which rebuilds h_t from the wedge definition rather than reusing any prover
code): S2, S3 and the exact 2-to-1 property of the w-map all hold pointwise for t = 2..11, and
M(t) = 1, 5, 5, 15, 33, 65, 117, 253, 505, 1117 reproduces the earlier independent counts.

Integer-level check, and why the result is a parity result only. Writing h_t = A XOR B with
A = (v_t OR h_{t-1}(v')) and B = h_{t-1}(w), the two structural lemmas of S4 give exact integer
identities, both VERIFIED for t = 2..12: |A| = M(t-1) + 2^(t-1) (the OR sum) and |B| = 2*M(t-1)
(the w-map being exactly 2-to-1). Hence M(t) = 3*M(t-1) + 2^(t-1) - 2*I(t) with
I(t) = |A AND B|, also verified exactly. This is a stronger confirmation of S4's two lemmas than
the mod-2 argument needs. But I(t)/2^t does not converge or follow any evident law over
t = 2..12 (0.500, 0.125, 0.563, 0.250, 0.344, 0.383, 0.402, 0.346, 0.374, 0.347, 0.428), so no
closed form for M(t) itself is claimed: the -2*I(t) term vanishes mod 2 and that is precisely
why the parity is tractable while the count is not.

A second prover independently reported a proof by a different route (an involution flipping the
one free cell appearing in no wedge condition, using a left-edge mirror of R3); it is not relied
on here and is not reproduced, but its agreement is corroborating.

OEIS status: M(t) is NOT in OEIS. Searched as the full 21 terms, several prefixes and suffixes
(ruling out an offset mismatch), first differences, and both halved forms; all return no
results. The only entry sharing the prefix 1,5,5,15 is A255304 (odd-rule CA "OddRule 117"),
which diverges at the fifth term (5 vs 33) and is unrelated. A151929 surfaces on a combined
query but is a false positive (a "-5,-5,15" substring deep in its data). So M(t) is a new
integer sequence arising from Rule 30, with the parity theorem below attached to it.

M(t) for t = 2..22 (wedge_reduction.py; t = 2..9 gated against the independent brute force):
1, 5, 5, 15, 33, 65, 117, 253, 505, 1117, 1895, 4415, 7821, 16851, 31829, 65675, 130797,
266065, 515597, 1064045, 2077175 — all odd. So C1, hence deg f_t = 2t-1 with unique top
monomial M_t, is now EXACT COMPUTATION for t <= 22 (previously t <= 13 via the direct ANF).
M(t)/2^t sits at 0.495 at t = 22: h_t is close to balanced, which is why odd weight is a
delicate claim rather than a counting triviality.

## Measurements (VERIFIED, exact; what they do and do not control for)

Exact ANF of f_t, t = 3..13 (134M inputs at t = 13), via bit-sliced truth tables + packed
Mobius transform; pipeline validated by exact match against ARM4 SS3's independent
measurements at t = 1,3,5,7 and by the Rule 90 control (degree 1 at every t, as forced by
additivity). Numbers below are exact integers, no sampling, no seeds needed.

| t | deg f_t | ANF terms | max abs Walsh | max correlation (/2^(2t+1)) |
|---|---|---|---|---|
| 3 | 5 | 30 | 56 | 0.4375 |
| 4 | 7 | 122 | 208 | 0.4063 |
| 5 | 9 | 346 | 456 | 0.2227 |
| 6 | 11 | 1360 | 1536 | 0.1875 |
| 7 | 13 | 4852 | 5696 | 0.1738 |
| 8 | 15 | 23094 | 21568 | 0.1646 |
| 9 | 17 | 79192 | 47304 | 0.0902 |
| 10 | 19 | 324572 | 175240 | 0.0836 |
| 11 | 21 | 1244124 | 397712 | 0.0474 |
| 12 | 23 | 5529024 | 1303744 | 0.0389 |
| 13 | 25 | 20440778 | 3550832 | 0.0265 |

- Degree = 2t-1 and top layer = {M_t} at every t <= 13: EXACT COMPUTATION (t=2 is the known
  small exception: two top monomials). This is finite evidence for the conditional part of the
  theorem, and proves it outright for t <= 13; it establishes nothing for t > 13 on its own.
- Max Walsh correlation decays from 0.44 to 0.026 (H3): measured only; the decay is irregular
  (drops cluster at odd t); NO law is claimed. Controls for nothing beyond what it states:
  it is the exact maximum over all 2^(2t+1) linear functions, so no sampling bias exists.
- ANF density (terms / 2^(2t+1)) sits at 0.152 at t = 13, consistent with ARM4's ~0.15 plateau
  (H2: no convergence claim made).
- Second-layer missing-triples fluctuate irregularly (chaotic-flavored) EXCEPT the invariant
  outlier {0,2,3}, which the proof above derives exactly. The fluctuation is why the theorem's
  induction was designed to avoid ever needing the second layer.

## Proof-relevance (honest scope)

This is a structural theorem about the ARBITRARY-INPUT function family f_t — the object ARM4
measured and the Meier-Staffelbach line attacked — not about the one-seed center column. It
implies NOTHING for P1 or P2, and the reason is structural rather than a gap in effort: a
statement about a function's degree says nothing about its value at the single point of its
domain that P1/P2 concern. For P3 it is model-restricted: any algorithm family whose t-th
output is forced to have algebraic degree < 2t-1 in the initial window cannot compute f_t.
That is now unconditional for all t, but it bounds computation of the FUNCTION, not of the
single-seed column, so it is not progress on P3 as posed. Claimed novelty is confined to: the
degree law with proof, and the self-similarity recursion h_t = (v_t OR h_{t-1}(v')) XOR
h_{t-1}(w) that drives it.

### Addendum 2 — exactly what the degree theorem buys for P3 (dedicated follow-up, verified)

Correct consequences, both standard and near-immediate (deg_2 <= D is textbook; see Buhrman &
de Wolf, TCS 288 (2002) 21-43):
- D(f_t) >= 2t-1 for deterministic decision-tree depth;
- D_xor(f_t) >= 2t-1 for parity decision trees (adaptive GF(2)-linear queries).
Both sit within 2 of the trivial ceiling 2t+1, and D(f_t) = 2t+1 exactly was measured for
t <= 5. The one genuine gain is the parity-decision-tree separation from Rule 90 (2t-1 vs 1).

REFUTED, and this matters because it is the tempting move: "deg_2(f_t) = 2t-1, hence by
Smolensky f_t needs super-polynomial AC^0[p] size" is FALSE. Smolensky's method requires
INAPPROXIMABILITY by low-degree polynomials over F_p, not high exact degree. The counterexample
proposed here was confirmed by the follow-up and stands: AND_n has deg_2 = n, is a single AC^0
gate, and is approximable over F_3 to within 25% by a degree-<= 4 polynomial. Two further false
inferences recorded: high exact degree does NOT imply high approximate degree (AND_n: n vs
Theta(sqrt n), Nisan-Szegedy 1994 / Paturi 1992; and directly for our family, deg_2(f_4) = 7
while the 1/3-approximate degree is 5), and low exact degree does not imply easy (PARITY has
deg_2 = 1 and is not in AC^0). Its verifier marked the blanket phrasing "exact degree gives NO
approximate-degree lower bound" as overstated; the counterexamples stand, the blanket claim is
withdrawn.

Sharpest statement of why this is inert for P3, worth keeping: P3's input is the INDEX t, of
length about log2(t) bits, whereas f_t is a function of 2t+1 unknown bits, and the seed column
is the single point evaluation a(t) = f_t(delta) at one fixed known input. Lower bounds on the
cost of computing f_t over its whole domain therefore carry no implication for the cost of
that one evaluation. On P3 the degree theorem is not merely unproved-to-help; it is provably
inert.

## Reproduction

- uv run python experiments/overnight-arms/common/rule30.py            (substrate selftest)
- uv run --with numpy python experiments/overnight-arms/anf/anf_probe.py   (t<=8 + ARM4 gate)
- uv run --with numpy python experiments/overnight-arms/anf/anf_sweep.py   (t=3..13 -> runs/overnight/anf/sweep.json)
- uv run --with numpy python experiments/overnight-arms/anf/parity_probe.py (C1/C2 + hierarchy -> runs/overnight/anf/parity.json)
- uv run python experiments/overnight-arms/anf/wedge_reduction.py 22 (M(t), t=2..22 -> runs/overnight/anf/wedge.json)
- uv run python experiments/overnight-arms/anf/verify_c1_proof.py 11 (independent check of C1 proof steps S2/S3/S4)

## Spending

Local CPU only. Modal $0.
