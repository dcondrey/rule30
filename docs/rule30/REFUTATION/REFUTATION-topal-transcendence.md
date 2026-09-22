# Refutation: Topal 2026, transcendence of the centre-column generating function

**Verdict: REFUTED for P1. P2 not attempted. P3 circular.**

Assessed 2026-08-31. Tolga Topal, "Transcendence of the Center Column Generating
Function of Rule 30 and the Resolution of the Prize Problems", Zenodo preprint,
2026-08-02. Version DOI 10.5281/zenodo.21780750, concept DOI
10.5281/zenodo.21780749, OpenAlex W7172247817 / W7172315126, CC-BY, ~14pp. Not
on arXiv, not peer reviewed.

Retrieval note for anyone repeating this: Zenodo's own `api/records/?q=` search
does not find it; OpenAlex `title.search` does. WebFetch lands Zenodo PDFs as an
unreadable `.bin`, so the text came through an `r.jina.ai` proxy. Section 2's
equations are **not validatable through that proxy** (dropped subscripts are a
known extraction artifact) and no claim below rests on them. Theorem 2 carries
no such caveat.

## The strategy is sound. The one computation it rests on is wrong.

Credit where due: the outline is correct and the field is unambiguous. The paper
works over `F_2(y)`, states Christol's theorem correctly, and does not equivocate
with `Q(x)`. The chain

> not 2-automatic ==> not algebraic over `F_2(y)` ==> not rational ==> not
> eventually periodic ==> P1

is valid. If the transcendence proof worked, P1 would fall.

Everything rests on **Theorem 2** ("the subsequences `S_k = (c_{2^k t})` are
pairwise distinct"). Theorem 1's Fibonacci degree growth is never invoked in it.
Theorem 2's proof uses only `c_0 = 1` and `c_2 = 0`, and its first line is:

> "The series `C(y^{2^k})` is precisely the generating function of the
> subsequence `(c_{2^k t})_{t>=0}`."

**This is backwards.** `C(y^{2^k})` is the **dilation**, which inserts zeros. The
generating function of the **decimation** `(c_{2^k t})` is given by the
**Cartier / section operator**, the adjoint of Frobenius. Christol's 2-kernel is
built from sections, never from Frobenius. The words "Cartier", "section
operator" and "decimation" appear nowhere in the paper.

**Verified locally on the actual Rule 30 column** (`experiments/rule30/center_column.py`,
bit-exact against OEIS A051023):

```
decimation (c_2t)  first 16 = 1010100010011111
dilation   C(y^2)  first 16 = 1010001010100000
identical?                  = False
```

## Why it is fatal rather than fixable

`C(y)^2 = C(y^2)` holds for **every** power series over `F_2`. It is the free
identity. Strip the mislabel and what Theorem 2 proves is:

> for `C` in `F_2[[y]]` with `C` not in `{0,1}`, the powers `C^{2^k}` are
> pairwise distinct.

True, and empty. It says nothing about any particular sequence, which is exactly
the diagnostic: **Rule 30's nonlinearity enters nowhere in the load-bearing
step.** The tower recurrence `L_{k+1} = L_k + L_{k-1} + L_k L_{k-1}` is where the
nonlinearity genuinely lives (Rule 90 would give the linear
`L_{k+1} = L_k + L_{k-1}`), and Theorem 1 appears correct, but it is decorative.

## The argument refutes itself on known inputs

- `C(y) = sum_{j>=0} y^(2^j - 1)` is 2-automatic, hence **algebraic** over
  `F_2(y)` by Christol, and is not in `{0,1}`. The paper's argument concludes its
  2-kernel is infinite and the series transcendental. Contradiction.
- `C(y) = 1/(1+y)`, the all-ones sequence, is eventually periodic. The same
  argument "proves" it non-periodic.

**Rule 90 is the wrong control here and passes vacuously**, which is worth
recording as a trap for future assessments. Rule 90's lone-seed centre column is
`(1,0,0,0,...)`: cell 0 at time `2m` is `C(2m,m) mod 2`, which is 0 for every
`m >= 1` by Kummer, since `m+m` always carries. So `C = 1`, precisely the
degenerate escape case the paper's own proof lands on. The argument never fires.
Use a non-constant 2-automatic series instead.

*(Correction to an internal brief: the centre column of Rule 90 is **not** the
indicator of `t = 2^j - 1`. `PATH.md` section 9.3 row 1 is unaffected, since the
`r_t = 1 iff t = 2^j - 1` there is R1's `r` column, not the centre column.)*

## A second, independent error in the same theorem

The kernel is defined as `K = { (c_{mt+r}) | m >= 1, 0 <= r < m }`, the set of
**all** arithmetic subsequences. The 2-kernel requires `m = 2^k`, `r < 2^k`.
Christol does not apply to the set as defined. Only `r = 0` is ever considered.

Diagnosis common to both errors: the paper conflates a coefficientwise operation
with a ring operation. Hadamard versus product in section 2, Cartier versus
Frobenius in Theorem 2. One mistake, two symptoms.

## Neither empirical number reproduces

Both checked here against the repo's verified generator.

| claim | paper | measured | note |
|---|---|---|---|
| ones in first 50,000 terms | 25,001 | **25,095** | invariant across offset conventions (offset 0 or 1, `N` = 49,999 / 50,000 / 50,001) |
| Berlekamp-Massey linear complexity `L(50,000)` over `F_2` | 25,001 | **24,999** | BM implementation validated on a degree-5 LFSR (5), all-zeros (0), all-ones (1), alternating (2) |

**The same value 25,001 is reported for two different quantities, and it is
exactly `N/2 + 1`.** That is the idealised value, not a measured one. Whether
this is transcription error or fabrication cannot be determined from the
document, and neither should be asserted; what is established is that the
empirical section does not reproduce.

## P2 and P3

**P2 is not attempted.** `N = 50,000` empirics plus "beyond any reasonable
doubt", and the paper itself concedes "a formal limit proof remains open".

**P3 is circular.** Theorem 3 assumes the column is a `(T(n), eps)`-secure PRG
with `T(n) = Omega(n)` and concludes an `Omega(n)` lower bound; the hypothesis is
strictly stronger than the conclusion. Its supporting side-claim is also false:
"any sub-linear time algorithm would provide a finite-state description,
contradicting non-automaticity". Automaticity means a DFA on the base-2 digits of
`n`, i.e. about `O(log n)`. Non-automaticity forbids nothing at `O(sqrt n)` or
`O(n / log n)`.

## Literature engagement

Four references: Christol 1979 (TCS 9:141-145, correctly cited), Massey 1969,
NKS 2002, the prize page. **No** Cobham, Allouche-Shallit,
Christol-Kamae-Mendes France-Rauzy 1980, Rowland, Bridy, Kopra, or Jen. Christol
is cited, and the operator Christol's theorem is about is the one the paper gets
wrong.

## What this repo should take from it

1. The `F_2(y)` transcendence route to P1 is **not** discredited by this paper's
   failure. The strategy remains valid and unattempted; only this execution of it
   is refuted. That is worth stating in any survey.
2. The Cartier-versus-Frobenius confusion is a reusable check: any future
   automaticity argument reaching this repo should be tested on
   `sum_j y^(2^j - 1)` before anything else.
3. Rule 90 is a **vacuous** control for arguments of this shape. Record it.
