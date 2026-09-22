# Trying combinatorial rewriting of the exact center query

Date: 2026-09-13. **Sound contextual rewrites were found and implemented.
They have not produced an exact sublinear algorithm.** This continues the
[section-based query investigation](RESULTS-p3-exact-shortcut-investigation.md)
by simplifying only the actual seed computation or the requested finite
precision. It does not require a rewrite to preserve every complete
transformation on every arbitrary input.

## 1. The constructive results

| Rewrite | Exact permission to apply it | Implementation |
|---|---|---|
| Delete a leading A-run | The chronological entering value is zero; A(0)=0 | Metadata-guided cuts of the shared expression |
| Replace the last t letters by A^t | The requested output bit m satisfies m>=2t | Keep a homogeneous suffix and a shorter active core |
| BC -> AA, and other two-letter cancellations | The actual incoming residue satisfies the complete boundary table; BC=AA for x=1 mod4 | One 32-state transducer pass over the compressed expression |
| Reduce a repeated expression's exponent | Only h output bits are needed; exponent is reduced modulo 2^(h-floor(h/4)) | A paid finite-precision rewrite, including an early exit avoiding huge moduli |

These identities have different scopes. Prefix deletion preserves the full
zero-input output. Suffix replacement preserves the specified bit and
higher bits, but may change lower ones. Conditional pair rules preserve
the full output on their retained input residue class. Power reduction is
equality at a finite precision for every input. Their conditions must not
be interchanged.

The proofs and independent controls are in the
[zero-prefix](RESULTS-p3-query-pruning-zero-prefix.md),
[query-cone](RESULTS-p3-query-cone-rewrite.md),
[conditional-pair](RESULTS-p3-observable-rewrite-pairs.md), and
[finite-precision](RESULTS-p3-precision-filtration.md) reports.

## 2. A genuine cancellation inside an actual query

Let A,B,C be the three ordered binary section states. After consuming the
seed prefix1000, the n=8 query contains

```
ABCCABCC.
```

The new contextual pass rewrites this directly to

```
ABAAABCB.
```

Both send the zero tail to6428. The first CC is reached after AB has
produced an input congruent to1 mod4, where CC=AA. Thus the pass creates
a reusable A-run inside the computation. This is not an unguarded
exchange of generator symbols.

The normalizer propagates a residue mod8 and a pending pair letter through
the grammar. A node is memoized together with this complete context. It
has at most32 distinct boundary states per input node, so a single pass
can operate on a highly compressed expression without expanding its word.
The bound counts graph operations; arithmetic on identifiers and lengths
is still charged. No convergence to a small normal form is assumed.

## 3. The query can be represented with half as many active letters

The suffix theorem proves that changing t late generator labels cannot
affect bit m>=2t. Its threshold is sharp: C A^(t-1) and A^t differ on zero
at bit2t-1. Combining this with exact leading-A deletion gives a closed
query core of length floor(n/2)+1.

The resulting two-step updates are explicit. If U begins with C, set
a=p(U), b=p(U|_0), where p is the root toggle. Delete the leading A of
U|_00 and append C if b=1. If b=0, the even-n update appends A, while the
odd-n update appends B when a=1 and A otherwise. Calling these updates R
and Q respectively,

```
c_(2h)   = bit_1(R^(h-1)(C^(h+1))(0)),
c_(2h+1) = bit_0(Q^h(C^(h+1))(0)).
```

The [evaluator](../../experiments/rule30/p3_query_cone_rewrite.py) constructs
and applies these updates with their actual boundary bits. The proof
retains the homogeneous suffix's influence on the answer. Simply deleting
that suffix, or treating R/Q as constant-cost oracles, would be invalid.

This representation still makes n-1 one-bit section advances, grouped in
pairs. Its active width stays approximately n/2 during those advances;
the same pruning does not repeatedly halve it. This is an exact
observational simplification, not a sublinear-time theorem.

## 4. Cost was measured including the rewrites

At the directed control n=32:

| Evaluator | Constructed grammar nodes | Distinct section + pair-transduction subqueries |
|---|---:|---:|
| Original section evaluator | 205 | 246 |
| Pair pass after every original section | 401 | 646 |
| Half-width core | 437 | 317 |
| Half-width core plus pair pass | 385 | 431 |

The pair rules perform real cancellations but their naive schedules cost
more than the work they avoid. Smaller expanded words also need not have
smaller shared graphs. The artifacts separately record cuts, concatenations,
and the normalizer's own work; none of these costs is hidden.

To test whether the core's regression was just parenthesization overhead,
a [canonical balanced grammar](../../experiments/rule30/p3_query_balanced_slp.py)
was implemented without flattening. It reduces the n=32 core from437 to244
nodes, still above the original205. All recursive reshaping costs are
recorded. The three controls n=8,17,32 discriminate the implementations;
they are not a scaling fit or an asymptotic lower bound.

The power-reduction theorem also supplies a real rewrite, but its modulus
at the initial precision n+1 is too large to shorten A^n. It can help at
small residual precision; it does not remove the earlier sequence of
section advances.

## 5. What this attempt establishes

There are useful nonlinear, context-dependent cancellations in the exact
singleton query, and they can be implemented on a compressed graph while
retaining the boundary conditions. The stronger full-map obstructions did
not prevent these rewrites.

What remains missing is a composition or scheduling theorem that reduces
the total cost of constructing and advancing the core to o(n). Neither
normalizing every step nor canonical tree balancing supplies it. The saved
implementation gives concrete rules and costs against which a proposed
bulk rewrite can now be checked; no successful bulk rewrite is claimed.

Each report links its verifier and saved JSON certificate. Checks cover
the complete small pair-boundary table, exact conditional higher tails,
query-preserving suffix thresholds, independent singleton queries, finite
group quotients, and guarded failures such as the incorrect removal of an
interior A at n=4. Source hashes are retained. No paid compute, GPU work,
old census rerun, or long-prefix generation was used.

Problem 3 remains open. No new period exclusion follows from this work.

**Continuation (2026-09-13).** The
[bulk-jump investigation](RESULTS-p3-bulk-query-jumps.md) now proves a
literal arbitrary-k core identity and implements its block section.
This supersedes the absence of a bulk construction noted above, but
does not supply a sublinear cost bound: the explicit boundary compiler
has a proved quadratic giant-block cost on the actual query.
