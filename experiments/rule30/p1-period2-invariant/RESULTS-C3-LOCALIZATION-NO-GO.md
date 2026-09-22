# The C3 localization no-go: five relocations, no seam

Date: 2026-09-07. Scripts: `zero_prefix_greedy_invariant_probe.py`,
`c3_abelianization_probe.py`, `rule90_control_on_c3.py`.

Status: **A MECHANISM CLASS IS CLOSED, NOT A LEMMA. `(1)` (`s_2 <= n`,
`s_3 <= n+1`) is still open and returns to being the target, exactly as in
`RESULTS-SCALE-TELESCOPING.md` sec. 5. What is dead is the strategy of proving
it by localizing the zero-prefix sensitivity claim: C3, its strengthening C3ab,
and the reachability restatement of C3ab all hold as far as measured, and none
of them localizes into a fact about a bounded object.**

Evidence level: `K` for the mechanism-class closure (each shape is refuted by an
explicit witness, listed below); `R` for the reductions, which are proved and
stand.

This belongs beside `RESULTS-QUEUE-WINDOW-PHASE-NO-GO.md` and
`RESULTS-SYNTACTIC-MONOID-INJECTIVITY-PROOF.md`: a third family of tools that
cannot compress the remaining gap.

## 1. The chain of relocations

Each step is a proved implication or a measured fact. None of them is a proof
of `(1)`.

```text
greedy lemma            supported to length 22, certificate to 23
   |  implies (drops the frontier and all cross-row induction)
C3:  max S_j >= j       0 failures, 44,205 legal rows to n=20
   |  implied by (drops gamma; phi is a homomorphism)
C3ab: max S_j^ab >= j   0 failures, 72,351 legal rows to n=21
   |  restated (K is nonempty, so this is not "f never freezes")
reachability:  no legal row realizes a freeze triple (V, j, c)
   |  restated
prefix-class bound:  max_P s_c(P.V) < legality threshold(j, c)
   |
   X  no quantity shared between the two processes
```

`C3ab ==> C3 ==> (1)` is two lines plus a homomorphism and is not retracted.

## 2. What each relocation bought, and what it cost

**C3 (from the greedy lemma).** Bought: no frontier, no cross-row induction, a
per-row statement. Cost: nothing. This one is a genuine simplification and
stands on its own (`RESULTS-ZERO-PREFIX-GREEDY-REDUCTION.md`).

**C3ab (from C3).** Bought: the object shrinks from an 8-element non-abelian
group to two GF(2) bits, which turn out to be the project's existing
`(alpha, beta)`, with `gamma` exactly the kernel. Neither bit suffices alone, so
two is the exact size. Cost: a strictly stronger claim, hence more exposure.

**Reachability (from C3ab).** Bought: the target becomes a statement about a
sparse, computable set of freeze triples rather than about all words. Cost: the
required bound on that subclass (`s < j = n - L`) is *stricter* than `(1)`
itself. Vocabulary shrank; difficulty did not.

## 3. Every local shape, with its witness

| Shape | Refuted by |
|---|---|
| `f` is never constant | `K` is nonempty: 20 triples at `L <= 5`, `j <= 14` |
| `K` is a suffix-closed language over `V` | `f` depends on `(V, j, c)`, not on `V` |
| freeze implies at most one more emission | `s - j` is not a window |
| immediate fatality, `s = 0` | `max s` reaches 10 (`V=2122`, `c=2`, `j=12`) |
| a first-symbol identity | 16 of 20 triples take all four first symbols |
| a chasing gap, `s` tracking `j` | `max s` is 3 and 5 at `j=11`, 6 at `j=9` |
| a finite poison list | `max L` wanders 0-5 over `j <= 14`; inconclusive |
| non-commutativity of `D8` as the lever | C3 holds after quotienting by `[G,G]` |
| one bit (activity-parity flux) | `alpha` fails 4, `beta` fails 14, to `n=14` |
| a Mersenne / dyadic escape | no slack dip at `n = 7, 15`; `n=9` beats `n=7` |
| any bound routed through `s <= n` | that is `(1)` assuming itself |

## 4. The structural reason, which is what forbids retries

> The freeze is `P`-independent. Every scenario in the chain has `k >= j`, so all
> of `P` is zeroed and the frozen `(alpha, beta)` cannot see it. The survival
> `s_c(P.V)` is `P`-dependent, and its first forced symbol is almost entirely a
> function of `P`.

The reachability statement therefore asks a `P`-independent abelian fact to
bound a `P`-dependent lifetime. The two quantities are computed by different
machines over different inputs, and no quantity living in both has been found.
Everything tried — the first symbol, `s = 0`, a bounded emission window, a `D8`
word, `gamma`, a single bit, `s <= n` — fails for that reason and not by
accident.

This is the same shape as the missing-seam obstruction elsewhere in the project:
there is no composition law for `s`. Induction on shorter prefixes fails in the
usual way, since `(1)` on `P` gives `s(P) <= j` while the goal needs
`s(P.V) <= j-1` or less, i.e. concatenation would have to *drop* survival.

## 5. What stands as fact

- C3ab holds on 72,351 legal rows through `n = 21`, C3 on 44,205 through
  `n = 20`; the tight set is exactly `W = 121` and `W = 221`, tail 3, row 2, and
  has not grown with `n`.
- The abelianization of the newest-cut group is exactly the existing
  `(alpha, beta)`; `gamma` is the kernel and is never needed for C3.
- `K` is nonempty, sparse (at most 3 triples per row depth), `P`-independent,
  and never legal on the dump: 20 triples, 1,465 realizing words, 0 legal.
- Route 1 is closed on both sides: extremal source periods grow with `n`, and
  extremal continuations include aperiodic cases.
- The Rule 90 control remains ill-posed, so `C3ab ==> PT2` is not claimed.

## 6. Scope

`(1)` is open. C3 and C3ab are true-so-far restatements of it that did not
localize, and are best read as structural findings about the coordinates rather
than as live proof routes. `C3ab ==> (1)` on this queue does not need the Rule
90 control; `C3ab ==> PT2` does, and that control has not been made well posed.
PT2 is one rung of P1. P2 and P3 are untouched.

Anyone resuming this branch should name a quantity shared between the nested
zero-prefix chain of `V` and the lifetime of `P.V` **before** writing code. The
absence of such a quantity is the content of this file.
