# Frozen inequality survives an exhaustive finite test: applied to BWH+ (P1)

Date: 2026-09-19

Target: `M_c(n) <= n+1` for every `n >= 7` and `c in {2,3}` (BWH+), the
repaired binary-wedge horizon of
`experiments/rule30/p1-period2-invariant/RESULTS-BINARY-WEDGE-HORIZON.md`.

## STATUS

**Method applies; it cannot deliver the target.** BWH+ is computed true for
every `7 <= n <= 30` by exhaustive enumeration and is **unproved** for all
larger `n`. P1 and period two are unchanged.

## 1. The premise "nobody has applied this method to this statement" is false

Checked by reading `PREREGISTRATION-BINARY-WEDGE-HORIZON.md` and
`RESULTS-BINARY-WEDGE-HORIZON.md` under `experiments/rule30/p1-period2-invariant/`,
and by grepping `data/research-metadata/rule30_research_db.jsonl` for `BWH+`.
The existing work already meets every clause of "how to tell it applies":

| clause | where it is met |
|---|---|
| named pre-registration | `PREREGISTRATION-BINARY-WEDGE-HORIZON.md`, frozen 2026-09-02 after `n<=10`, before the held-out `11<=n<=20` |
| kill condition | "any exact source with `b_c(W)>n` at `n>=7`"; for BWH+, `M_c(n) >= n+2`, coded as exit 1 in `binary_wedge_census_exhaustive.py` |
| kill did not fire, with slack | BWH+: zero failures through `n=29` (source doc; `n=30` added here), slack table §4a |
| disclaims general `n` | "A finite pass is evidence only"; "unproved" |

The catalog is behind the source on range, which is probably why the premise
was generated: its BWH+ records say "checked exhaustively through n=20", while
the results doc extends to `n=29` (2026-09-17). Not edited here, per the
constraints.

## 2. Preconditions: split between two inequalities

The method is *frozen* inequality survives. Here the freeze and the survival
attach to different inequalities.

* **BWH** (`M_c(n) <= n`) was genuinely frozen before held-out data. It was
  **falsified** at `n=15` (`M_3(15)=16`). The frozen inequality did not
  survive.
* **BWH+** (`M_c(n) <= n+1`) is a post-hoc repair fitted after the `n<=20`
  data was seen; the source says so. It was fixed before the 2026-09-17
  extension, so `21 <= n <= 29` was prospective for that extension and is
  reproduced here. Only `n=30` is prospective for this run, pre-registered in
  `PREREG-n30.md` before its log was read.

So the preconditions hold for BWH+ in the only sense the method has: a fixed
inequality, a decidable finite instance at each `n`, a kill that can fire. In
sample `7..20`, out of sample `21..30`.

The precondition that **fails** is the one the target needs: the method
produces a finite range, and the target quantifies over all `n >= 7`. Per the
instructions, the method is not adapted past this point.

## 3. Kill tests

**Proposed state quotient is not a congruence: does not bear on this method.**
An exhaustive census proposes no quotient and needs no congruence. The
obstruction lives on the route that would turn the census into a proof (the
non-canonical, drifting source-assumption cores and degree `~n` ANF residuals
of the source doc §5); it is not a finding of this run and was not reproduced
here.

**Finite computation cannot certify an all-length statement: FIRES.** Each
`n` is a separate instance; no length covers the next. Largest parameter
reached: `n = 30`. Cost doubles per unit `n`. This is what caps the status
at *computed*, not *proved*.

**Claim generalised from one instance fails at another: fired on BWH, not on
BWH+.** BWH held for `7 <= n <= 14` and failed at `n=15`; that is why BWH+
exists. The unrestricted bound also fails below the threshold (`M_3(5)=8 >= 7`,
`M_2(6)=9 >= 8`), which is why BWH+ starts at `n=7`. BWH+ has no failing
instance in `7..30`.

## 4. Reproduction (this session)

Unmodified `experiments/rule30/p1-period2-invariant/binary_wedge_census_exhaustive.py`.

* `census-n7-n25.log`: control replay of the published `n=7..20` table,
  14/14 match, then `n=7..25`, zero BWH+ failures, rc 0.
* `census-n26.log` .. `census-n30.log`: one process per length,
  `--histogram --skip-control`, same working tree as the control.

| `n` | `M_2` | `M_3` | `max - n` | matches published |
|---:|---:|---:|---:|:---|
| 7 | 7 | 6 | 0 | yes |
| 8 | 6 | 7 | -1 | yes |
| 9 | 5 | 8 | -1 | yes |
| 10 | 9 | 9 | -1 | yes |
| 11 | 9 | 8 | -2 | yes |
| 12 | 9 | 11 | -1 | yes |
| 13 | 10 | 10 | -3 | yes |
| 14 | 11 | 11 | -3 | yes |
| 15 | 11 | 16 | **+1** | yes |
| 16 | 14 | 14 | -2 | yes |
| 17 | 13 | 13 | -4 | yes |
| 18 | 17 | 18 | 0 | yes |
| 19 | 18 | 16 | -1 | yes |
| 20 | 16 | 17 | -3 | yes |
| 21 | 16 | 21 | 0 | yes |
| 22 | 18 | 19 | -3 | yes |
| 23 | 19 | 17 | -4 | yes |
| 24 | 21 | 23 | -1 | yes |
| 25 | 20 | 21 | -4 | yes |
| 26 | 21 | 21 | -5 | yes |
| 27 | 22 | 22 | -5 | yes |
| 28 | 22 | 25 | -3 | yes |
| 29 | 27 | 24 | -2 | yes |
| 30 | 25 | 24 | -5 | **new, held out** |

Maximiser counts from the histograms at `n=26..29` (`c=2`: 4, 12, 29, 4;
`c=3`: 24, 50, 48, 48) match the source doc's §4a degeneracy table.

**Control that fails when the claim is false.** Below the threshold the
BWH+ inequality itself is false, and the same detector says so:
`census-n1-n6.log` gives `M_3(5)=8` and `M_2(6)=9`, both `>= n+2`, i.e. `max - n
= +3`. The kill is gated to `n >= 7` by definition, which is why that run
exits 0. So the census does report violations of exactly this inequality
where they exist. It also reports `max - n = +1` at `n=15`, recovering the
published BWH falsifier. The `n=7..20` replay aborts on any mismatch and
passed.

The `n=28` and `n=29` rows in the source doc came from a `--skip-control` run
attested by a sibling control. They are now recomputed independently, with
the control in this session's sibling run from the same tree.

## 5. What is proved, refuted, open

* **Proved (exhaustive certificate, with control):** `M_c(n) <= n+1` for
  `c in {2,3}` and every `7 <= n <= 30`. A finite statement only.
* **Refuted:** nothing new. BWH (`<= n`) stays refuted at `n=15`, reproduced.
* **Open:** BWH+ for `n > 30`, hence DLP, both constant-tail separators,
  the rank-zero separator and period two by this route. The live proof route
  is the one the source doc §4a names: a lossy asymptotic bound
  `max_c M_c(n) <= n+1` for `n >= N_0` plus this census below `N_0`. This work
  supplies only the finite half.
* **§4b converse, one new trial, passed (computed):** `M_2(29)=27 ->
  M_2(30)=25` drops by exactly two, the first qualifying step since
  `n=24->25` for the source doc §4b statement "every step with
  `M(n+1,c)=M(n,c)-2` has `Q(n+1,c)=Q(n,c)[2:]`". Pre-registered in
  `PREREG-continuation-n29-n30.md`, with the predicted word written down
  before the `n=30` line printed. Result (`continuations-n29.log`,
  `continuations-n30.log`; both `M` values match the census, and the maximiser
  counts 4 and 134 match the histograms):

  ```text
  Q(29,2)         = 121121121111122121212211221   (1 distinct, 4 maximisers)
  Q(29,2)[2:]     =   1121121111122121212211221
  Q(30,2) word 1  =   1121121111122121212211221   = Q(29,2)[2:]
  Q(30,2) word 2  =   1211211222121222221212221   fresh
  ```

  Under the pre-registered reading for multiple words (some `Q(30,2)` equals
  some `Q(29,2)[2:]`), the kill did not fire. The record goes from 5 of 5 to
  6 of 6. As at the prior `18->19` and `22->23` (`c=3`) steps, whose targets
  also have two distinct maximal words in the §4b table, the second word here
  is not inherited: the statement is only about existence, and a strong form
  ("every maximal `Q(n+1)` is inherited") was already false at those steps.
  Six trials is not a law. The `n=30`, `c=3` sweep was stopped after the `c=2` line (rc 143); it is
  not part of the trial.

**The n=30 row against the source doc's §4a watch item.** §4a warned that
each new length had raised the fitted slope of `g(n)=max_c M_c(n)` (0.842,
0.851, 0.871) and that the margin below 0.95 was shrinking. `n=30` reverses
that for one step (`slope_fit.py`, `slope_fit.log`, recomputed from this
session's logs; the 7..29 fits reproduce §4a exactly):

| range | fit | resid sd |
|---|---|---:|
| 7..29 | `0.871 n + 0.24` | 1.40 |
| 7..30 | `0.857 n + 0.44` | 1.39 |
| 18..29 | `0.724 n + 3.91` | 1.41 |
| 18..30 | `0.703 n + 4.35` | 1.37 |

One length is not a trend, and the slack has swung between `-5` and `-2` on
consecutive lengths. It is recorded, not interpreted. Maximisers at `n=30`:
134 sources for `c=2`, 8 for `c=3`, out of `2^30`.

## 6. Ladder statement changed

None changed in kind. BWH+ stays **conjectured** for all `n >= 7`. Its
exhaustively certified range moves from `7 <= n <= 29` to `7 <= n <= 30`, so
the finite base any asymptotic argument must reach is now `N_0 <= 31`. The
catalog's BWH+ records still say "through n=20" and lag both the source doc
(29) and this run (30); not edited here, per the constraints.

## 7. Reproduce

```bash
S=experiments/rule30/p1-period2-invariant/binary_wedge_census_exhaustive.py
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python $S --first-n 7 --last-n 25 --chunk-exponent 18
for n in 26 27 28 29 30; do
  PYTHONDONTWRITEBYTECODE=1 uv run --no-project python $S --first-n $n --last-n $n \
    --chunk-exponent 18 --histogram --skip-control
done
```

Exit 1 means the BWH+ kill fired. `*.log` is globally gitignored; the table
above is the artifact of record, and the logs need `git add -f` to be tracked.
Wall clock on this machine, lengths running concurrently: 46 s at `n=25`,
193 s at 26, 379 s at 27, 711 s at 28, 1541 s at 29, 3258 s at 30.
