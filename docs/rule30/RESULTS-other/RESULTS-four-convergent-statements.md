# The four "same zero-set question" statements are four different statements

Date: 2026-09-09. Reading and formalization only; no code was written and no
measurement was taken. Every statement below is transcribed from its own
primary source with a file:line citation, then compared.

**Deliverable: a correction, not a result.** Four lines in this repo are
asserted in prose to bottom out on "the same zero-set question". They do not.
They share one *object* — column 1 sampled on the centre column's zero set —
and, for three of them, one *target* (`P1`). They differ in the universe they
quantify over and, for one pair, in polarity. The single most consequential
consequence is (A) below: **R1 is not a reduction of `P1` to anything weaker;
it is logically equivalent to `P1`.**

| # | Finding | Evidence |
|---|---|---|
| A | S1 (route R1) is **equivalent to P1**, not a subgoal of it | `U`, from the proved pin biconditional plus Kopra Thm 3.5 (inherited citation, see §5) |
| B | S2 (a7's i.o. lemma) is **closed** — proved 2026-09-09 — and is logically independent of the periodicity question, with a concrete separating object | `U` for the proof (rung 3); `C` for the separator (the `N=7,T=4` torus) |
| C | S3 (R7's `q=420` residual) is the **negation of the ladder relaxation** of S1's conclusion. `¬S3 ⟹ S1(p=2)`; the converse is **false unless `P1(2)` is false**, and a witness in this repo proves the relaxed statement false at `q=1` | `C`, the extracted `R=1,k=2` witness |
| D | S4 (alt-trace uniformity gap) `⟹ S1(p=2)` by an explicit map; converse unproved | `U` for the implication; `R` for the converse |
| E | S3 and S4 are **unresolved** against each other; their universes are provably incomparable | `C`, two-way |
| F | The four share exactly one thing: the object `rho`. Two prose lines need correction notes | `R` |

## 0. Common notation

Rule 30, in the repo's own orientation (`PATH.md` §1, `ladder.FWD[30]`):

```text
s(t+1,x) = s(t,x-1) XOR ( s(t,x) OR s(t,x+1) )
c_t = s(t,0)      r_t = s(t,1)      l_t = s(t,-1)
```

The pin at `x = 0` (`PATH.md` §2, restated verbatim at
`experiments/rule30/r1-zero-set-attack/RESULTS-R1-ZERO-SET-ATTACK.md:52-59`
and `docs/rule30/RESULTS-r1-general-period.md:56-62`):

```text
l_t = c_(t+1) XOR ( c_t OR r_t )
c_t = 1  =>  l_t = 1 XOR c_(t+1)          (free from the trace alone)
c_t = 0  =>  l_t = c_(t+1) XOR r_t        (needs column 1)
```

Write `Z(c) = { t : c_t = 0 }` and let `rho` be `(r_t)` for `t in Z(c)` taken
in increasing time order. For `c` exactly `(01)`-alternating this is
`RESULTS-alt-trace-fiber.md:38-39`'s `rho_k = r_(2k)`; the general-`p`
version is `RESULTS-r1-general-period.md:63-70`.

**Proved biconditional** (`R1-general-period` §0, general `p`; not
period-2-specific): *assuming `c` eventually periodic*,

```text
l eventually periodic   <=>   rho eventually periodic
```

**Universes.** These are what the four statements actually differ in.

| symbol | universe |
|---|---|
| `D_seed` | the lone-seed diagram, one object |
| `D_fin` | diagrams whose initial row has finite support |
| `D_lfin` | diagrams whose initial row vanishes left of some `-d`; right half arbitrary, finite or not |
| `D_all` | all diagrams on `Z` |
| `L(R,k)` | the R7 ladder's ω-regular constraint language at depth `R`, window `k` — a **sound over-approximation**: every real diagram's letter word lies in it, not conversely (`PATH.md` 7.3.F; `R1-ZERO-SET-ATTACK` §2) |

`D_seed ⊂ D_fin ⊂ D_lfin ⊂ D_all`. `L(R,k)` is not a set of diagrams at all;
it contains letter words with no realizing configuration.

### 0.1 One ambiguity, recorded rather than resolved

`PATH.md:239` phrases the conclusion as "`r` eventually periodic on
`{c_t = 0}`" — a statement about `r` as a partial function of `t`.
`R1-general-period` §0 phrases it as `rho`, the *sampled* sequence.
Under the hypothesis that `c` is eventually `p`-periodic, `Z(c)` is
eventually a union of residues mod `p`, and the two readings coincide up to
multiplying the period by at most `p`. **The readings are not equivalent
without that hypothesis**, and both sources always carry it, so nothing below
turns on the choice. Degenerate case: if `c` is eventually constant 1 then
`Z(c)` is finite and both readings are vacuous — that is the `p=1, w=1`
checkerboard case, settled separately in `RESULTS-eventual-period.md`.

## 1. The four statements, formalized from their primary sources

### S1 — route R1

Source: `docs/rule30/PATH.md:239-243`; sharpened to a biconditional and to
arbitrary period at `docs/rule30/RESULTS-r1-general-period.md:56-70`;
independently restated as "(star)" at
`experiments/rule30/r1-zero-set-attack/RESULTS-R1-ZERO-SET-ATTACK.md:60-62`.

> **S1.** In `D_seed`: if `c` is eventually periodic, then `rho` is eventually
> periodic.

Universe: one object. Polarity: we want it **true**.

*Staleness check.* `PATH.md` §4 predates commit `aac9085`
(`RESULTS-r1-general-period.md`). No drift: `PATH.md:242` already carries the
explicit `<=>`, and `R1-general-period` §1 confirms the reduction "never
assumes `p=2`". The newer file adds the general-`p` `rho` definition and the
finding that the five-zero bound does **not** generalize; neither changes S1.

### S2 — a7's i.o. lemma

Source: `experiments/overnight-arms/frontier_attack/a7_ladder_realizability/ladder_realizability.md:236`;
restated at `RESULTS-ladder-rung2-periodic-realizability.md:69-70`.

> **S2.** In the single diagram `X(k,01)`: `col_1(t) = 1` for infinitely many
> `t` with `col_0(t) = 0`. Equivalently, `rho` contains infinitely many ones.

Universe: the singleton `{X(k,01)}`, one per `k`. `X(k,01)` is the diagram
built at `ladder_realizability.md:38-50` — right wedge zero, seed cell, lone-seed
match on `-2k..-1`, and the cells at `x <= -(2k+1)` chosen greedily by left
permutivity to drive `col_0` onto the target word from `T0 = 2k+1`. It is
**not** the lone seed and **not** finite: its own §5 states "`X(k,w)` has
infinite support to the left", so `X(k,01) ∈ D_all \ D_lfin`.

**S2 is PROVED.** `RESULTS-ladder-rung3-io-and-aperiodicity-audit.md:52-57`:
prior theorem R5 says every actual alternating-centre right trace avoids
`00000`, so every five consecutive `rho` samples contain a one; applied at
every time after the onset this gives the literal i.o. lemma for every `k`,
and a7's odd-`q` Theorem B becomes unconditional.

### S3 — R7's residual `q = 420` branch

Source: the gap is `RESULTS-ladder-rung2-periodic-realizability.md:58-61`
(quoting rung 1 §6); the residual is `rung2:317-322` and `PATH.md:461-463`;
the `rho` form is
`RESULTS-ladder-rung3-io-and-aperiodicity-audit.md:59-65`.

> **S3.** For `q ≡ 0 (mod 420)` and every `R`: there is a letter word in
> `L(R,k)` whose derived `col_0` is eventually `01`-periodic and whose
> `col_{-1}` is **not** eventually `q`-periodic. In `rho` coordinates
> (rung 3): `rho_n ≠ rho_(n-210)` infinitely often.

Universe: `L(R,k)`, the over-approximation. Polarity: **inverted**. S3 true
means ladder mode (ii) can never return EMPTY, i.e. the method is dead
(`rung2:46-52`: "a limitation theorem kills a *method*"). S3 false at some
`(R,k,q)` proves `Thm(2)`.

### S4 — the alt-trace uniformity gap

Source: `docs/rule30/RESULTS-alt-trace-fiber.md:10-11` (the status line),
`:53-56` (Claim(d)), `:951-954` (the exact restatement).

> **S4.** No diagram in `D_lfin` has `c` exactly `(01)^∞` (resp. `(10)^∞`).
> Equivalently: no finite seed — a frontier pair of a finite `rho`-prefix
> triangle — follows the forced map with every pin parity equal to 1 forever.
> Equivalently: Claim(`d`) holds for every `d`.

Universe: `D_lfin`, all of it, with the right half arbitrary. Note "exactly",
not "eventually"; the eventual version follows by shifting the onset to time 0.
Verified instances: `d <= 24` by depth certificate, and separately every
instance of left support `<= 26` ones in both phases (`alt-trace-fiber:5-9`).

## 2. Relationships, one pair at a time

Each implication below names the map that carries a witness across. Where
there is no map, the verdict is *unresolved*, not *independent*, unless a
separating object is exhibited.

### 2.1 S1 is equivalent to P1

`P1` is "the lone seed's `c` is not eventually periodic".

*`S1 ⟹ P1`.* Suppose S1 and suppose `c` eventually `p`-periodic. S1 gives
`rho` eventually periodic; the proved biconditional (§0) gives `l` eventually
periodic. Then `c` and `l` are two adjacent eventually periodic columns of a
nonzero finite-seed diagram, contradicting Kopra TCS 946 (2023) 113668
Thm 3.5 (see §5 on this citation). Hence `c` is not eventually periodic. The
witness map is explicit: an eventual period of `c` maps, through the pin, to
an eventual period of `l`.

*`P1 ⟹ S1`.* Vacuously: `P1` falsifies S1's antecedent.

*The `p=1` case does not use the citation.* If `c` is eventually constant then
`Z(c)` is finite or cofinite and §0.1's vacuity applies, but the conclusion is
available directly: `PATH.md` register rows 25 and 26 exclude every eventually
constant lone-seed centre outright, PROVED in repo (row 26: the all-one trace
forces `L_k = 1` for every positive even `k`, an infinite left support, so no
finite row has a constant-one trace; Jen 1986 Thm 7a independently). So the
Kopra dependency of §5 is confined to `p >= 2`.

**Therefore S1 ⟺ P1.** R1's value is real but it is not what the register
implies. R1 *localizes* the obligation — it identifies `rho` as the entire
residual freedom, and `R1-general-period` quantifies exactly how that freedom
grows with `p` — but it does not *reduce* `P1` to anything easier. Any plan of
the form "close R1 first, then P1 follows" is circular. `PATH.md:240` already
says closing R1 closes the problem; what has not been recorded anywhere in
this repo is the converse, which is what makes it an equivalence.

### 2.2 S2 is closed, and independent of all three others

S2 is proved (§1). It is a statement about *recurrence of ones* in `rho`, not
about periodicity, and the two are independent in both directions:

* **Periodic and satisfies S2.** The `N=7, T=4` torus, on record at
  `rung3:70-75`: `col_0 = (0101)^ω`, `col_1 = (1100)^ω`, `rho = (10)^ω`,
  `col_-1 = (0111)^ω`. Ones infinitely often, and every period. rung 3 cites
  it for exactly this purpose: "It satisfies i.o., but fails both `Diff_4` and
  `Diff_420`."
* **The proof route confirms it.** S2 follows from R5 alone (no `00000`), a
  constraint every eventually periodic `rho` with positive one-density also
  satisfies. Nothing in the proof touches periodicity.

Moreover, even proved, S2 does not deliver what the ladder wanted from it:
`ladder_realizability.md` §5 records that the Jen/Kopra finisher **may not be
invoked** on `X(k,01)`, because that diagram is infinite to the left and the
finisher needs a finite seed. Listing S2 among the open convergent statements
is stale as of `RESULTS-ladder-rung3-io-and-aperiodicity-audit.md`.

### 2.3 S3 is the negation of the *relaxation* of S1, and the relaxation is already false

Ladder mode (ii) returning EMPTY at `(R,k,q)` says: *every* word in `L(R,k)`
with eventually `01`-periodic `col_0` has `col_{-1}` eventually `q`-periodic.
That is S1's conclusion with `D_seed` replaced by `L(R,k)`. So:

```text
S1  =  [ forced periodicity of rho, over D_seed ]
¬S3 =  [ forced periodicity of col_-1, over L(R,k) ]     with L(R,k) ⊋ D_seed's words
```

*`¬S3 ⟹ S1(p=2)`.* `¬S3` at any `(R,k,q)` proves `Thm(2)`, hence `P1(2)`,
which falsifies S1(2)'s antecedent. Map: the EMPTY certificate.

*Converse fails.* `P1(2)` says nothing about `L(R,k)`, which contains
non-realizable words. **Separating object, already in this repo:**
`experiments/rule30/r1-zero-set-attack/RESULTS-R1-ZERO-SET-ATTACK.md` §3
extracts, from the unmodified `rung1.decide_pin` at `R=1, k=2, w=(0,1), q=1`,
a word with onset 5, prefix `[2,3,0,2,2,0,2]`, cycle `[1,3,0,2,0,2]`, whose
`c` is eventually `01`-periodic and whose `l` is not eventually 1-periodic.
So the relaxed statement is **false at `q=1`** while S1(2) is open. The two
are not equivalent unless `P1(2)` is false.

A second, stronger separation is proved in `rung2` §4: the four tori
`(N,T) = (7,4), (84,6), (155,10), (728,14)` are **genuine Rule 30 diagrams**
with `col_0` exactly `01`-alternating. Unrolled to `Z` they are spatially
periodic elements of `D_all \ D_lfin`. So a Rule 30 diagram with an exactly
alternating centre column *exists*; S1's and S4's finite/left-finite
hypotheses are load-bearing, and any argument that does not use them cannot
prove either. This is the Rule 90 filter's lesson in a second register.

**The conflation, named.** `PATH.md:463` and `rung2:322` both say the residual
is "the same zero-set question as R1". As *questions* — "is `rho` forced
periodic?" — they are the same question asked of two different universes. As
*statements* they are not the same, and the difference is not cosmetic:
finding a ladder witness (S3 true) bears on R1 not at all, and the `q ≠ 420`
witnesses already found are the demonstration of that pattern. Only the
`¬S3` direction transfers.

### 2.4 S4 implies S1(p=2)

*Map.* Suppose S4, and suppose the lone seed's `c` is eventually alternating
with onset `T0`. The row `s(T0, ·)` has support in `[-T0, T0]`, hence lies in
`D_lfin`, and its centre trace is exactly `(01)^∞` or `(10)^∞`. That
contradicts S4. So `c` is not eventually alternating — `P1(2)` — which
falsifies S1(2)'s antecedent. The map is `T0 ↦ s(T0, ·)`.

*Converse: unproved.* S4 quantifies over every left-finite row and every right
half; S1(2) is one orbit. No separating object is available, so the verdict is
**unresolved**, not "strictly stronger".

*What the wallpaper does and does not separate.* `alt-trace-fiber:968-988`
records the right-half-`{1,4}` member: forced left half spatially 7-periodic
(`0110010` from depth 1, verified to depth 1024), `rho` locked alternating to
`t = 20000`. Its own status line says the infinite member is **not proved**
and the lock is empirical. It separates `D_all` from `D_lfin`, showing S4's
left-finiteness hypothesis is necessary — but so do the four tori of §2.3,
*and those are proved*. **The tori supersede the wallpaper for this purpose.**
Neither separates S4 from S1(2).

### 2.5 S3 versus S4: unresolved, universes incomparable

No implication is available in either direction, and both are provable in
neither. Their universes are incomparable, in both directions and concretely:

* `L(R,k) ⊄ D_lfin`: the tori of §2.3 splice into accepted letter words
  (`rung2` metric M3: 0 rejections over 192 `(R,k)` cases) and are not
  left-finite.
* `D_lfin ⊄ L(R,k)`: S4 admits an arbitrary right half, while every ladder
  word satisfies the right wedge `s(0,x) = 0` for `x >= 1`
  (`ladder_realizability.md:40`). The `{1,4}` member is the recorded instance
  of a right half that violates it (`ladder_realizability.md` §5).

Verdict: **unresolved**. Both imply `P1(2)`; neither is known to imply the
other.

## 3. Summary table

`P1(2)` = "the lone seed's centre column is not eventually `(01)`-alternating".

| | universe | polarity | status | relation to `P1` |
|---|---|---|---|---|
| **S1** (R1) | `D_seed` | want true | **open** | **equivalent to `P1`** |
| **S2** (a7 i.o.) | `{X(k,01)} ⊂ D_all` | want true | **PROVED** (rung 3) | none; independent of periodicity |
| **S3** (R7 `q=420`) | `L(R,k)`, an over-approximation | want **false** | open at `q ≡ 0 mod 420`; **true** for every other `q` | `¬S3 ⟹ P1(2)`; `S3` implies nothing |
| **S4** (alt-trace gap) | `D_lfin` | want true | open; certified `d <= 24`, support `<= 26` | `S4 ⟹ P1(2)`; converse unproved |

Proved implications, all one-directional except the first:

```text
S1  <=>  P1
¬S3  ==>  Thm(2)  ==>  P1(2)  ==>  S1(2)      (last step vacuous)
S4         ==================>  P1(2)  ==>  S1(2)
S2   independent of all three (separator: the N=7,T=4 torus)
```

## 4. What this changes

1. **Do not treat R1 as a subgoal.** S1 ⟺ P1. "Concentrate on R1 because one
   proof closes several lines" is not available: closing R1 *is* closing P1.
   What R1 legitimately provides is a change of coordinates — the whole
   residual freedom is `rho` — and `RESULTS-r1-general-period.md` is the
   measurement of how that freedom behaves as `p` grows.
2. **The only genuine convergence is on the object, not the statement.** All
   four are about `rho`. Nothing else is shared.
3. **Two lines need correction notes**, appended rather than edited:
   `docs/rule30/PATH.md:461-463` and
   `docs/rule30/RESULTS-ladder-rung2-periodic-realizability.md:317-322`.
   Both say the `q=420` residual is "the same zero-set question as R1". The
   accurate statement is: the `¬S3` direction implies S1(2) and is strictly a
   statement about the relaxation; the `S3` direction implies nothing about
   R1, and the relaxed form of R1's conclusion is already **false at `q=1`**
   by the witness in `r1-zero-set-attack` §3.
4. **S2 should be moved out of the open column** wherever it is still listed
   as the unproved i.o. lemma. rung 3 proved it on 2026-09-09.
5. **The four tori are a proved replacement for the empirical wallpaper**
   as the witness that some Rule 30 diagram has an exactly alternating centre
   column. Any future argument for S1 or S4 must use finiteness of the seed,
   and now has a proved object saying so rather than an empirical one.

## 5. One load-bearing citation, not re-verified here

`S1 ⟹ P1` uses the **eventual** form: no nonzero finite seed has two adjacent
eventually periodic columns. This repo attributes that to Kopra, TCS 946
(2023) 113668, Thm 3.5 (`r1-zero-set-attack:61-64`;
`LITCHECK-p2-density.md` §7 records the arXiv version as 2202.13809 and
Jen 1990 Prop. 3 as the lone-seed, non-eventual predecessor).

**Jen's form is weaker.** If only Jen's "not periodic" were available, `S1`
would yield only "`c` is not periodic", not `P1`. The equivalence in §2.1
therefore rests on Kopra's eventual strengthening. That is an inherited
citation. It was **not** re-verified against the paper this session; the two
in-repo restatements of it agree with each other, which is not independent
confirmation. Anyone building on §2.1 should read Kopra Thm 3.5 directly first.

**Scope of the dependency:** `p >= 2` only. The `p = 1` case is closed
independently by `PATH.md` register rows 25 and 26 (see §2.1). Everything at
`p >= 2` rests on the citation, including the headline equivalence.

## 6. Scope

Reading and formalization only. No new mathematics, no computation, no code.
Every formal statement is transcribed from the cited file and line. The
implications in §2 are elementary given the proved pin biconditional and the
Kopra citation of §5; the separating objects are all pre-existing repo
artifacts, cited but not re-run this session. `P1`, `P2` and `P3` remain open,
and nothing here moves any of them.

## 7. Primary-source follow-up, 2026-09-09

The dependency in §5 is now verified against Kopra's journal text:
Theorem 3.5 (p. 5) and Corollary 3.7 (p. 6) explicitly exclude
**eventually** periodic width-two traces. Definition 2.4 requires a nonzero
left-finite configuration and permits an arbitrary right tail. Thus the
S1/P1 equivalence survives at p>=2. See
[RESULTS-kopra-eventual-verification.md](RESULTS-kopra-eventual-verification.md)
for source links, hypotheses and the period/onset map. The earlier
unverified-citation caveat is historical. The phrase "needs a finite seed"
in §2.2 should read "needs a nonzero left-finite configuration"; X(k,01)
still fails that hypothesis. No claim about a historical strengthening over
Jen follows from this verification.

## 8. Logical-seam correction, 2026-09-09

The subsequent [Task 6 audit](RESULTS-load-bearing-seam-audit.md) §4 found
overstatements in this report. The following supersedes them:

* The q=1 witness refutes one parameter-specific relaxation. It does not
  decide the existential q=420-multiple certificate or establish that
  `S1(2) => not-S3` is false. That converse is **unproved**; the wording
  "false unless P1(2) is false" is withdrawn.
* The last sentence of §2.5 needs **not-S3**, not S3, as the statement
  implying P1(2) alongside S4.
* Letter-word and diagram universes require explicit encoding/projection
  maps before set-inclusion comparisons. The spliced torus tail and the
  `{1,4}` right half do not establish the two claimed inclusions' failure
  as written. The asserted two-way universe separation is withdrawn;
  S3 versus S4 remains unresolved.
* The T=4 torus shows that recurrence of ones does not force aperiodicity.
  It does not establish two-way logical independence of the four fixed
  statements. S2 is proved and supplies no aperiodicity conclusion by
  that recurrence property alone.

The S1/P1 equivalence, the proof of S2, and S4=>P1(2) stand. These
corrections narrow claimed separations; they resolve no open Rule 30 problem.
