# P3: exact bulk query jumps, and the cost still inside them

Date: 2026-09-13. **There is now an implemented arbitrary-k core jump,
with an all-length correctness proof. There is no proved exact sublinear
Rule 30 center algorithm.** This extends the
[contextual rewriting investigation](RESULTS-p3-contextual-query-rewriting.md)
from local cancellations to a complete bulk operation. The main new
limitation is also precise: its explicit boundary construction costs
quadratic bit work when used as one giant jump on the actual query.
That is an implementation-specific result, not a general P3 lower bound.

The scope remains the [uniform singleton query model](P3-SCOPE-AUDIT.md):
input n in binary, fixed seed, and all construction, preprocessing, and
bit work charged. No P1 or P2 exclusion follows from this investigation.

## The constructive result

Use chronological words in the three exact section generators A,B,C,
where A(x)=x XOR((x<<1) OR(x<<2)). The current core update Q takes two
zero sections, removes their first A, and appends the letter determined
by the actual two-bit output of the preceding word. The new theorem is

\[
 (UA^k)|_{0^{2k}}=A^kQ^k(U)
\]

as **literal ordered words**, for every nonempty U and every k>=0.
Two entering bits overwrite a single generator's initial memory; an
induction uses that synchronization while retaining the intermediate
bits at every word junction. Both even and odd center queries can use Q:

\[
 c_{2h}=\operatorname{bit}_1(Q^{h-1}(C^{h+1})(0)),\qquad
 c_{2h+1}=\operatorname{bit}_0(Q^h(C^{h+1})(0)).
\]

The first formula has h>=1, the second h>=0, and c_0=1.
The [bulk theorem and proof](RESULTS-p3-bulk-core-formula.md) also give
the exact integer action H(x)=(x>>2) XOR((x>>1) OR x), with
Q^k(U)(0)=H^k(U(0)). These are all-length identities, not extrapolations
from the saved small cases.

The [fused compiler](RESULTS-p3-fused-section-blocks.md) executes the
formula on a shared word expression without a loop over k core updates.
It transports the complete ordered block between concatenated children.
Its huge fixed-family control computes Q^k(A^L)=A^L at
L=2^40+3 and k=2^36+7 using86 grammar nodes, without an expanded word or
large zero buffer. This checks real compressed execution on that known
fixed family; it does not demonstrate a shortcut for the singleton query.

## What blocks the tested acceleration

The exact compiler explicitly materializes its boundary integers.
For a C-headed input, its first k required leaf actions have distinct
contexts of increasing bit length. Their total size is Omega(k^2).
The same protocol evaluates A^n(1) in one width-(n+1) block with
Omega(n^2) bit work. Fewer outer calls or grammar nodes therefore do not
establish an asymptotic speedup. The proof excludes neither an implicit
boundary representation nor a different algorithm.

There is also a full-output restriction: a C-headed word of length L
sends zero to an integer with highest one2L-1. Any positive A/B/C word
with the same zero output must have exactly L letters after its leading
A-run, and that remainder must begin with C. Thus positive rewrites
preserving the full zero output cannot shorten this core. This leaves
shared graphs and query-only rewrites open.

Three other exact tests clarify which information cannot simply be lost:

| Attempt | Established result | Limit of the conclusion |
|---|---|---|
| Let the G/H boundary error decay | At the actual core Q(C^4)(0)=222, a closed four-cycle preserves a bit1 discrepancy forever | Refutes automatic error decay under further H steps; other contexts may cancel it |
| Replace each fine-core letter pair by one coarse letter | An actual terminal-core conflict and an all-fixed-seam commuting obstruction for phase moduli1,2,4,8 | Does not exclude a stateful decoder, other phases, or an observable-only recursion |
| Collect conjugated boundary corrections in the original small group | Two levels fail to commute; a complete seven-bit permutation has order16 | Refutes those collection rules, not all structured correction representations |

The first result is in the bulk proof. The other two have separate
[pair-decimation](RESULTS-p3-core-decimation-pairs.md) and
[ordered-defect](RESULTS-p3-conjugated-defects.md) reports and verifiers.
The defect factorization also identifies
bit_n(Ad_A^n(tau)(0))=c_n: evaluating a single compressed conjugate can
already contain the original P3 query. Its short notation is not a cost
bound.

## Exact outcome and remaining obligation

The new result is a correct bulk construction, accompanied by a proved
cost obstruction for its explicit-context implementation. It is useful
structural progress, but does not establish improved asymptotic query
time or a general impossibility theorem.

The next concrete obligation for this route is an **implicit boundary
action and section algorithm**: it must compose the actual ordered block
through the shared expression, recover the demanded bit, and prove that
the total construction and evaluation costs are o(n). It cannot assume
the boundary is available for free, replace its ordered state by the
failed static pair code, or drop errors using automatic decay. No such
algorithm or complexity bound is supplied here.

Each linked report retains its exact verifier and artifact. The bulk
identity and compiler received an independent mathematical audit; the
persistent-cycle edges were also recomputed independently. The compiler's
local section tests use the raw section recurrence, and its15 directed
singleton query variants agree with independent row evolution. Finite
checks validate implementations; the universal statements above use the
displayed induction, support arguments, or complete closed cycles.
No old frontier census, long-prefix regeneration, GPU, or paid compute
was used.

**Continuation.** The
[implicit-boundary investigation](RESULTS-p3-implicit-boundary-investigation.md)
proves an all-length finite-core period bound and a safe transient-aware
powering rule. Actual center queries at n=11 and n=18 reject dropping or
extrapolating the transient. A sublinear singleton algorithm is still missing.
