# Characterization: Natal & Al-saadi, "Fast Simulation of Cellular Automata by Self-Composition"

Date: 2026-09-13

Primary source: Joseph Natal, Oleksiy Al-saadi, arXiv:2409.07065v2 (submitted
2024-09-11, revised 2025-06-22), cs.CC, CC BY 4.0. Full text and HTML retrieved
directly; not a self-published or unreviewed target — normal arXiv revision
history, standard theorem/lemma structure.

This is a characterization, not a refutation. The construction and its proofs
are checked and found correct (with one minor, non-load-bearing indexing slip
in Lemma 5, isolated in §6). The question this audit answers is what the
result actually establishes and how it relates to P3, not whether it is wrong.

**Correction from the subsequent P3 investigation, 2026-09-13.** The earlier
version called this bound a generic simulation "ceiling." That was not
justified. [Two-dimensional macroblock tabulation](RESULTS-p3-macroblocks.md)
gives `O(n²/log² n)` word-RAM time, including table construction; the
tabulation principle already appears in Grandjean and Jachiet,
[arXiv:2206.13851v2, §8.2 and Appendix 11](https://arxiv.org/pdf/2206.13851v2).
The claims of a generic ceiling are corrected below. This does not refute
Natal and Al-saadi's upper bound or supply a sublinear P3 algorithm.

## Verdict

The paper proves a genuine, correct **logarithmic-factor time
speedup** for computing an entire generation-`n` configuration of *any*
one-dimensional 2-color CA, at the cost of asymptotically **more** space than
naive simulation, not less. It does not claim to touch any Rule 30 prize
problem, and does not: the P3 connection is entirely external framing, absent
from the paper's own introduction, contributions, and discussion. Under the
paper's own declared model of computation, the same O(n²/log n) time bound is
already implied by standard bit-parallel word-RAM simulation — the technique
already implemented in this repository's own `center_column.py` — at
asymptotically less space. Its self-composition construction is a valid
alternative way to obtain that upper bound. The theorem does not prove
optimality, and a generic block-table construction improves the bound as
explained in the correction above. Neither construction supplies a Rule 30
center-query algorithm with sublinear charged work.

## 1. The construction, exactly

Rule 30 is written (Eq. 5) as `x_i^{n+1} = x_{i-1}^n XOR (x_i^n OR
x_{i+1}^n)`, radius `r=1`. Definition 2 composes two local rules `f_2`, `f_1`
into a single rule of radius `r_1+r_2` by running `f_1` everywhere, then `f_2`
everywhere, in one step. Lemma 3 proves the `k=2` self-composition case
directly by substitution (Eq. 6-9): `X_{n+1}^G` built from `g=h∘h` equals
`X_{n+2}^H`, so one step of the radius-`2r` composite automaton `G`
reproduces two steps of `H`. Lemma 5 generalizes to `k`-fold self-composition
`h^{(k)}`, radius `kr`.

Lemma 6 is the algorithmic core: `h^{(k)}`, as a lookup table over all
`2^{2kr+1}` possible radius-`kr` neighborhoods, can be *built* in
`O(k²·2^{2kr})` time (each entry costs `O(k²)`: `k` nested applications of `h`
to a shrinking window, total window-length work `Σ_{j<k} O(kr-2j) = O(k²r)`,
`r` constant — this reproduces to the stated bound). The De Bruijn graph
`B^F` of the composite rule (Definition 1; Fig. 5-7) is a byproduct of the
same table, "with no additional run-time complexity." Lemma 7 then says: given
`B^F` already built, walking it to advance *any* configuration of `F` by one
generation costs `O(n)` — one table lookup per output cell.

Theorem 8 balances the one-time table-build cost against the per-generation
walk cost. Building `h^{(k)}` costs `O(k²2^{2kr})`; running the resulting
radius-`kr` automaton for the `~n/k` composite steps needed to reach
generation `n` costs `O(n²/k)` (Eq. 11: `n²/k = k²2^{2kr}`, solved by the
Lambert W branch `k(n) = 3/(2r ln 2) · W_0(2r ln(2)/3 · n^{2/3}) ~ log n`,
Eq. 12). Substituting `k ~ log n` gives the headline `O(n²/log n)` time.
Corollary 9 rearranges the *same* balance equation for the table size:
`2^{2kr+1} ~ n²/k³ ~ n²/(log n)³` — this is the paper's `O(n²/(log n)³)`
space bound, and it is the size of the precomputed rule table / De Bruijn
graph, not the size of the row being simulated (that stays `Θ(n)` throughout,
as in naive simulation).

## 2. What the complexity claim actually says about space

The abstract calls this "a time-memory tradeoff," which is accurate but reads
as if both bounds improve on the naive `O(n²)`-time algorithm. They do not.
Naive row-by-row simulation is `O(n²)` time and `O(n)` space (one row,
overwritten in place — this is exactly what `run_simulation()` does in the
paper's own Appendix C++ code, and what `center_column.py`'s `center_column`
does). This construction trades that `O(n)` space for `O(n²/(log n)³)` space
— a blow-up by a factor of `~n/(log n)³` — to buy a `Θ(log n)` reduction in
time. The direction of the tradeoff is space-for-time, not a joint
improvement, and the paper's own experimental section concedes this is not
merely asymptotic pedantry:

> "the bitwise optimizations described by Wolfram [8] are several times
> faster than this method for any reasonable number of generations because
> computers parallelize packed bitwise operations and are efficient at
> reading memory linearly along an array" (§4).

> "The 27-fold composition (4.5 petabytes) will overtake the
> bitwise-optimized implementation in about ~60 years on an Intel(R) Xeon(R)
> Gold CPU. This takes the principle of delayed gratification to its
> extreme." (Fig. 4 caption.)

Both are the authors' own words, not this audit's inference.

## 3. Does the log-factor improvement hold up, and against what baseline

The proof is sound (§1, §6) and the asymptotic is real *relative to
element-by-element naive simulation*. But it does not hold up as a novel
asymptotic once the model of computation is made explicit, which the paper
itself does honestly in §5:

> "it relies on a model of computation that treats accessing memory with an
> address of size O(log n) as taking a single unit of time — the canonical
> RAM model."

Under exactly that model (word size `w = Θ(log n)` bits), the standard
bit-parallel technique for any 2-color, bitwise-expressible local rule
already achieves `O(n²/log n)` time at `O(n)` space. This repository's own
ground-truth generator is that technique:

```python
# experiments/rule30/center_column.py
row = (row << 1) ^ (row | (row >> 1))
```

One call advances the *entire* row by one generation; on an `n`-bit integer,
each of the shift/OR/XOR operations costs `O(n/w) = O(n/log n)` word
operations under the same transdichotomous RAM model the paper invokes. `n`
generations therefore cost `O(n²/log n)` time — the identical exponent-of-`n`
bound Theorem 8 proves — using `O(n)` bits of state, not `O(n²/(log n)³)`.
This is folklore (it is exactly Wolfram's cited optimization, ref. [8] in the
paper), not a novel result, and the paper does not make this comparison
anywhere; §4 only benchmarks wall-clock practicality, never asymptotic
equivalence.

This does **not** refute Theorem 8. Its self-composition construction is
rule-agnostic. The earlier version of this audit overstated a distinction
between that construction and bit-packing for larger fixed alphabets.
Every fixed finite alphabet and fixed-radius rule can be encoded by a fixed
Boolean circuit on finitely many input bits. Evaluating that circuit on
packed bit planes also permits word parallelism; its constants can depend
strongly on the alphabet and rule, but not on `n`. An alphabet supplied as
part of the input would require a separate complexity analysis.

Separately from the bit-parallel comparison: a `Θ(log n)` factor is real
progress in a fine-grained-complexity sense, but it is not a polynomial
exponent reduction and not polylogarithmic overall — the algorithm is still
`Θ(n²)` up to that single log factor. This project's own `SEARCH-ARCH.md`
already sets the bar for what counts as a real reduction on this exact
question: `alpha_hat = 1.9676`, measured for a 64-bit bit-parallel candidate
that is "plain forward simulation with a 40x constant factor and no
reducibility whatsoever," is explicitly rejected by the pre-registered
`alpha_hat < 1.9` gate. A `log n` divisor shifts a fitted power-law exponent
over any practically measurable range of octaves by far less than that
constant-factor case already rejected; this construction would not pass this
project's own acceptance bar for a P3 candidate, and there is no reason to
benchmark it to confirm that.

## 4. Do the authors claim P3 relevance

No. The words "prize," "center column," "conjecture," "periodic," "density,"
and "P1/P2/P3" do not occur anywhere in the paper (introduction, discussion,
or conclusion — checked against the full text). Rule 30 is chosen purely as
a stress test:

> "Our focus on Rule 30 in this paper stems from its notoriously chaotic
> nature and perceived lack of structure." (§1)

The paper's own point of comparison is not the Wolfram prize problems but
Culik & Dube's fractal point-query result for Rule 90/150:

> "CAs with nested patterns such as the well-studied Rule 90 or Rule 150
> contain a fractal structure which allows for a given space-time coordinate
> to be determined in O(log n) [6]." (§1)

This is the paper's own taxonomy, and it draws exactly the line this audit
needs: Rule 90/150 admit a **point query** — one output coordinate in
`O(log n)`, no other cells touched — because of linear/affine structure.
Natal & Al-saadi's algorithm computes the **entire** generation-`n`
configuration (all `~2n+1` cells); there is no asymmetry between "get the
center bit" and "get the whole row" in their construction, because advancing
the composite automaton by Lemma 7 requires materializing every cell of the
growing row regardless of which one you ultimately read. Getting only the
center column costs exactly the same `O(n²/log n)`, `O(n²/(log n)³)`-space
bound as getting the whole triangle. §5's discussion of open questions
("There may exist faster machines to compute certain cellular automata...")
is deliberately general and never narrows to the center column or to Rule
30's prize status.

The P3 connection is therefore entirely this project's (or this audit
round's) own framing, not the authors'.

## 5. Small-scale verification

Checked against `experiments/rule30/center_column.py`, this project's ground
truth (OEIS A051023 generator):

- Reconstructed the `k`-fold table exactly as Lemma 6/Definition 4 specify
  (iterated raw Rule 30 application `k` times per table entry) for
  `k=1..5`.
- Ran the resulting composite automaton from a simple seed and compared its
  center cell against `center_column.py`'s ground truth at the generation
  Lemma 3/5 predict it should reproduce.
- Result: **45/45 trials match** using the corrected generation-alignment
  formula (§6 below); **24/45 match, 21/45 mismatch** using the paper's
  literally printed Lemma 5 formula, confirming the printed formula is
  general-`k` incorrect and the corrected one is what the construction
  actually computes.
- This confirms Lemma 3/6/7 and Theorem 8's underlying mechanism (table-build
  correctness and De Bruijn-walk correctness) are sound; no discrepancy found
  in the core construction itself.

## 6. Erratum: Lemma 5's general-`k` formula is off by a `k`-dependent constant

Lemma 5 states, for `F` a `k`-fold composition of `H` with `X_1^F = X_1^H`:
`X_{kn-1}^H = X_n^F`. Take `k=1`: `F=H` trivially, so the claim reduces to
`X_{n-1}^H = X_n^H`, which is false for evolving `H`. The correct relation,
matching the paper's own generation convention ("`X_n` denotes the
configuration after `n-1` applications... beyond the initial configuration,"
§2) and its own worked `k=2` proof (Eq. 9: `X_3^H = X_2^G`), is

```
X_{k(n-1)+1}^H = X_n^F
```

This coincides with the printed `kn-1` exactly at `k=2` (`k(n-1)+1 = 2n-1 =
kn-1` only when `k=2`), which is the case Lemma 3 derives it from; the
general-`k` statement in Lemma 5 appears to carry that special case forward
without adjusting the additive constant. The §3 numerical check (45 trials,
`k=1..5`) confirms the corrected formula and refutes the printed one for
`k≠2`.

This is cosmetic. Theorem 8 and Corollary 9 do not depend on the exact
alignment constant — they only need *some* fixed offset, bounded by `k`, to
translate `H`'s target generation into a count of `F`-steps, and reaching a
generation not exactly on that offset costs at most `k-1` extra naive `O(n)`
steps, i.e. `O(n log n)`, absorbed into the `O(n²/log n)` bound. The
complexity results are unaffected.

## 7. Relationship to this project's P3 program

`SEARCH-ARCH.md`'s grammar (§1.2) deliberately excludes "`Iterate` over a term
containing `Eval`" specifically because that is forward simulation:
"stepping a *concrete* configuration repeatedly." Natal & Al-saadi's
construction is structurally in that excluded family — it is still iterated
concrete simulation, just batched into a larger-radius single step via a
precomputed table. It is rule-agnostic: it uses no property of Rule 30's
nonlinear term (`x_i^n x_{i+1}^n` in Eq. 4) and would apply identically to
Rule 90, Rule 150, or any other radius-1 ECA. It supplies no analogue of the
`InvertLeft` backward-solving primitive (§1.3 of `SEARCH-ARCH.md`) that this
project has identified as the only demonstrated reducibility specific to
Rule 30.

It is citable prior art for an upper-bound construction, not a ceiling on
generic algorithms. In the same word-RAM model, packing both the output
block and the time jump gives the stronger bound recorded above. A lower
bound can be proved for an explicitly exhaustive fixed-macrotable tiling
architecture; it must not be extended to every compression method or every
uniform center-query algorithm. No result here shows that every improvement
over quadratic simulation requires Rule 30-specific algebra.

No prize problem is addressed by this paper or by this audit.
