**Adjacent research targets: scope and remaining obligations — 2026-09-11**

This audit checks the proposed connections against the primary papers and the
current reconstruction archive. It does not establish a prize conclusion or a
reduction from a Rule 30 conjecture to an arithmetic conjecture. No claim of
novelty is made for the elementary observations below.

**1. The all-budget period-two target is correctly quantified.**

For alternating phase a, let m_a(D) be the minimum initial-left support among
admissible reconstruction prefixes reaching depth D. The sufficient target is

    for each phase a and each K, there exists D such that m_a(D) > K.

Equivalently, every frontier reachable from a finite admissible prefix has a
finite legal lifetime under the partial zero-cost successor Z. The lifetime
may depend on the complete frontier; no uniform constant lifetime is required.
An infinite bounded-cost branch eventually takes only zero-cost edges, since
the costs are nonnegative integers. Conversely, finite branching and König's
lemma turn arbitrarily deep bounded-cost prefixes into an infinite branch.
This equivalence was already proved in
[RESULTS-alt-trace-fiber.md](RESULTS-alt-trace-fiber.md), in the discussion
beginning “Every state has at most one zero-cost successor.”

The no-11 source model is a relaxation of actual-right compatibility. Mortality
in that larger model suffices. An immortal relaxed trajectory would invalidate
that proof route, but need not give a Rule 30 seed counterexample.

There is a further proved restriction already in
[the p1.4 archive](../../experiments/rule30/panel/runs/p1.4.md): an immortal
zero-cost continuation cannot have an ultimately periodic source sequence.
If the samples have period p after index n_0, put T = 2n_0 and P = 2p. The
inverse recurrence gives every reconstructed left column the same eventual
temporal period P and onset T. An initial zero interval of length 2(T+P)
would force two adjacent columns to vanish for a full eventual period; the
local rule then propagates that vanishing toward the alternating center, a
contradiction. Thus a prefix of support at most K has length at most

    2(T+P)(K+1) - 1 = 4(n_0+p)(K+1) - 1.

The remaining mortality question concerns aperiodic source tails. The bound
does not control n_0 or p in terms of K, so it supplies no all-budget theorem.

**2. The recorded budget-26 result needs a provenance qualification.**

The results document records H_01(26) = 191 and H_10(26) = 119 as an external
continuation; it reports independent reproduction of phase 01 through budget
23. No separate budget-26 machine-readable certificate was located in this
audit. The existing slow regression test called support_H with its default
cap of 140, which cannot certify a maximum of 191, and ignored the cap flag.

The test now sets explicit caps of 194 and 122 and requires hit_cap to be false
before checking the two maxima. This repairs the verification procedure; it
does not independently reproduce the recorded maxima. Six relevant small
support/control tests passed. Both slow cases collect successfully, but the
budget-26 enumeration was not run.

**3. Gravner–Griffeath: create branches, rather than preserve existing ones.**

In [Edge cellular automata, revised September 15, 2012](https://www.math.ucdavis.edu/~gravner/edge/rpsrev2.pdf),
Problem 8 asks whether the number of cycles seen on growing boundary strips
is unbounded. Unbounded periods are already established. The preceding
analysis also controls repeated labels modulo rotation: distinct genuine
branches retain their ancestry distinctions; period-doubling siblings account
for the relevant duplicate labels.

Therefore the proposed branch-preservation theorem does not reach the main
gap. A useful new theorem must force infinitely many genuine branching events.
For the E1D0 labels in their construction, the distinction is between labels
using only 0 and 2 with an even number of 2s (genuine branching) and those with
an odd number (period doubling). A finite branch census or a random-label
heuristic is not an infinitude proof. A precise translation from our reachable
frontiers to these labels remains to be supplied.

**4. Rowland: retain the finite-seed restriction explicitly.**

[Local Nested Structure in Rule 30](https://ericrowland.github.io/papers/Local_nested_structure_in_rule_30.pdf)
uses the reflected, shifted map

    (fR)(m) = R(m) XOR (R(m-1) OR R(m-2)),

with R(m) = 0 for m <= 0 and R(1) = 1. Its recurrence signature is
a_R(n) = lambda_R(2^n), where lambda records the first disagreement of R with
f^t R. Conjecture 1 explicitly restricts to central rows with white tails.
The printed statement of Conjecture 2 does not repeat a finite-tail qualifier;
the surrounding discussion also admits rows with infinite right tails.

There is an exact obstruction to uniqueness up to *integer* time shift on the
unrestricted one-sided space. Let I be the singleton and define

    r_k = (4^k - 1)/3,       S = lim_k f^(r_k) I.

Here convergence means agreement on each finite prefix. This limit exists:
the first m coordinates form a triangular permutation whose order is a power
of two, and r_k tends to -1/3 in the 2-adic integers. The power-of-two assertion
follows inductively: after a period of the first m-1 coordinates, the last
coordinate is either fixed or flipped, so doubling that period suffices.

The map f preserves the first position at which two rows disagree, as does its
inverse. Hence lambda_(f^r I)(t) = lambda_I(t) for every integer r. For each
fixed t = 2^n the singleton has a finite first disagreement with f^t I, so
passing to the finite-prefix limit gives a_S(n) = a_I(n).

Nevertheless S is not f^r I for any integer r. Let p_m be the least period of
the singleton's first m coordinates. These powers of two are unbounded:
otherwise a common finite period would give f^P I = I, whereas a finite row's
rightmost occupied position advances two places with every f step. If
S = f^r I, prefix periodicity would force r = -1/3 modulo every p_m, which is
impossible for an ordinary integer r.

This proves failure of the unrestricted extension. It does **not** establish
that S has finite support, and is not a finite-seed counterexample. A restricted
reconstruction theorem must use the finite-origin hypothesis, rather than
silently replacing it with membership in the one-sided compact completion.

**5. The 4/3 problem gives an exact arithmetic control, not an easier theorem.**

For the stated stopping map, a legal step is

    n_(j+1) = (4 n_j + e_j)/3,   e_j in {0,1},

where e_j is 0 on residue 0 and 1 on residue 2; residue 1 stops. After D steps,

    3^D n_D = 4^D n_0 + sum_(j=0)^(D-1) 4^(D-1-j) 3^j e_j.

Each binary word (e_0,...,e_(D-1)) specifies exactly one starting residue class
modulo 3^D: 4^D is invertible modulo 3^D, and the congruence successively
enforces integrality of all intermediate steps. Distinct words give distinct
classes, since the first differing digit would contradict the uniquely forced
residue at that step. Thus precisely 2^D of the 3^D classes survive D updates.
An exhaustive check through D = 8 agrees with this proof.

Consequently any set of positive integers that never stop has natural density
zero: its upper density is at most (2/3)^D for every D. This does not prove the
set is empty. Every finite legal word has positive integer realizations, but
an infinite compatible word generally specifies a 3-adic starting value;
compactness does not ensure an ordinary positive integer. Every legal positive
step strictly increases the value, so any infinite positive orbit diverges.

This is a useful transfer test: a proposed termination argument must distinguish
ordinary positive starts from infinite compatible histories. Counting surviving
classes or proving a measure-zero exception set does not settle universal
termination. See [Dubickas–Mossinghoff, Lower bounds for Z-numbers](https://doi.org/10.1090/S0025-5718-09-02211-X).

**6. The common CA framework needs an additional hypothesis.**

[Kopra's rapidly left expansive framework](https://arxiv.org/pdf/2202.13809)
includes Rule 30 and fractional multiplication automata, but also Rule 90.
The latter has an eventually periodic singleton center trace. Thus the common
class cannot by itself imply nonperiodicity of a single column. Kopra explicitly
separates his multi-column result from the single-column problem. Similarly,
infinitely many fractional-part limit points do not exclude confinement to
[0,1/2). A transferable theorem needs a verifiable additional condition that
rejects these controls.

The rational-base normality conjecture is accurately stated in
[Andrieu–Eliahou–Vivion](https://arxiv.org/html/2510.11723v2): every positive
integer orbit of ceil(px/q) should be equidistributed modulo every q^k.
The paper proves implications to Mahler-type and generalized stopping problems.
For the particular 4/3 stopping problem, merely hitting residue 1 once from
every positive integer already suffices; full equidistribution is much stronger.
No corresponding implication from a Rule 30 prize conclusion is established.

**Research decision.** The most immediate reuse of the existing proof machinery
is the aperiodic zero-cost mortality question. A worthwhile outside control is
the exact 4/3 survivor calculation above. A published boundary target requires
either a finite-origin signature theorem or a theorem creating infinitely many
genuine branches. These are narrower obligations than the original general
transfer proposal, but none has been shown easier than the outstanding P2
seed-specific cancellation bound. Choosing the period-two route as the main
project would be a strategic change from the earlier P2 priority.
