# Preregistration: do the extremal forcing STATES form a family across n?

Date: 2026-09-05. Frozen before any census was run. Directory:
`experiments/rule30/p2-needle-attack/`, all files prefixed `estate_`.
Read-only imports from `../p1-period2-invariant/` (`late_pull_diagonal_sat`,
`constant_tail_scale`, `dyadic_periodicity_analyzer`, `rank_zero_separator`);
no file outside this directory is written. Python only, venv
`/Volumes/A/researchpapers/.venv/bin/python3`. Exhaustive enumeration, no RNG
except where a random SAMPLE of the null population is explicitly drawn (seed
fixed at 0).

## 0. What object this is, and what it is NOT

The forcing `literal_extension(W, c, rows)` carries a STATE: the dependency
edge, a vector `edge` that has length `2n` after the padded source word
`(0,)^n · W` is consumed (`append_dependency_edge`,
`constant_tail_scale.py:205-218`). The recurrence
`new[0]=BOUNDARY[v]; new[1]=phi(prev,new[0]); new[j]=phi(old[j-2],new[j-1])`
reads `old[0..L-2]` and never reads `old[L-1]`, so **the last cell `edge[-1]`
is the exposed cut (output), not state**; the live state that determines the
entire future is `edge[:-1]`, and `prev = BOUNDARY[edge[0]]` (BOUNDARY is an
involution), so the live state is exactly `edge[:-1]`.

Edge orientation, verified empirically (`estate` orientation check, logged in
`estate_RESULTS.md` §0): **index 0 is shallow and driven by the NEWEST source
symbols; high index is deep and accumulates the whole history; `edge[-1]` is
the cut.** Varying the first (oldest) source symbol changes only the top cell;
varying the last (newest) changes every cell. Therefore two words that share a
suffix (same newest symbols) agree on a low-index PREFIX of the edge and differ
at the deep/output end. This fixes the alignment used below.

This is the STATE object. It is DISTINCT from the two string analyses already
completed and NOT to be redone:
- `RESULTS-FIBER-EXTREMAL-FAMILY.md`: extremal CONTINUATION strings (output
  symbols) and source RESIDUAL strings, n=10..16 — found NO clean family.
- The alpha PARITY of the surviving run is a bijective re-encoding of the
  continuation string (forced high bit `= 1 XOR alpha`), so a null there is
  already implied by the string negative and will not be reported as new.

Nobody has compared the edge STATE vectors across n. That is this task.

## 1. The census (exhaustive, both arms, r=0)

For each `n in 10..20`, `c in {2,3}`, residue `r=0`:

- Enumerate source words by BFS over the alphabet, deduplicating the frontier
  at every depth by the live state `edge[:-1]` (valid because the future
  depends only on `edge[:-1]`), summing fiber counts on merge and retaining one
  representative full edge, one representative word, and the SET of `edge[-1]`
  values seen. Two arms:
  - **all-W** (PRIMARY): `W in {1,2}^n`. This is the RW/DLP/H_r/gamma object;
    the BACKGROUND and `RESULTS-TERMINAL-CLASS-ARCHAEOLOGY.md` §10 establish
    the source ranges over all `{1,2}^n` and the extremum is non-hard-core.
  - **hard-core-W** (SECONDARY): `W in {1,2}^n` with no `11`. The constant-tail
    `s_c` object; its extremals are periodic and it is the arm the cocycle
    template actually wants (§10-11 of the archaeology). Reported per-arm.
    Neither arm is dropped if they disagree.
- For each distinct live state, force `rows = n+4` continuation symbols and
  compute `survival = hard_core_extension_length` (first row breaking `{1,2}`
  or `1`-after-`1`). `max_survival(n,c) = max` over states; `gamma = (n+2) -
  max_survival`. EXTREMAL states = the live states attaining `max_survival`;
  EXTREMAL words = their fibers.
- Record per extremal state: full edge, live edge `edge[:-1]`, the set of
  `edge[-1]` values, fiber size, the continuation string, the killer type at
  row `survival` (`E-miss:0`, `E-miss:3`, or `1-after-1`), and the per-row
  alpha profile + alpha SUPPORT (below).

## 2. Controls (must pass before any family claim)

1. **Reproduce `RESULTS-TERMINAL-CLASS-ARCHAEOLOGY.md` §2.1 exactly** for
   n=14..19 (all-W): `max_survival`, `gamma`, pooled fiber size, class count.
   n=14 both tails is run FIRST as a gate; disagreement halts the run.
2. **Cross-check extremal-state extraction against `literal_extension`
   directly**: for every extremal word, assert my incrementally-carried edge
   and survival equal those obtained by calling
   `late_pull_diagonal_sat.literal_extension(W, c, n+4)` and recomputing the
   hard-core run. Agreement on `max_survival` and the continuation for 100% of
   extremal words, else halt.
3. **State-object distinctness**: assert in the results that this is
   `edge[:-1]`, the live STATE, not the continuation/source strings of
   `RESULTS-FIBER-EXTREMAL-FAMILY.md`.
4. **alpha identities**: compute alpha two ways — eq(3)
   `1 XOR [p!=0] XOR parity{i<|E|-1: E_i!=0}` and eq(4) via `R=reverse(E)`,
   `parity{i>=1: R_i!=0}` — assert equal on every row (off-by-one catcher). On
   every forced row assert `forced_symbol>>1 == 1 XOR alpha`
   (`RESULTS-PULL-ROW-ALPHA-SUPPORT.md` eq 5-6); a single failure halts.
5. **Self-consistency / validation label**: assert `survival < n+2` for every
   state (this re-confirms `gamma>=1` on my own code for n=10..20; it is
   VALIDATION of a settled finite result, not a discovery).
6. **hard-core sub-check**: reproduce the §10 hard-core fibers (n=16 c=2,
   n=17 c=2, n=18 c=3 all pooled-fiber 2, periodic top-class suffix).

## 3. Family tests with a NULL model (the decisive part)

Because the forcing forgets down to the last cell or two, short low-index
agreement between ANY two states is generic. A raw agreement number is
therefore uninterpretable. Each test below is measured against a null, and the
KILL condition is the failure of separation from the null.

Let `S_n` = the set of distinct live extremal states at `(n,c,arm)` (expected
1-3). For a consecutive pair `(n, n+1)` and an ALIGNMENT
(prefix = index-0-first; suffix = index-(-1)-first):

- **(a) extremal-extremal**: over `s in S_n, s' in S_{n+1}`, the agreement
  score = length of the maximal matching run under the alignment. `A_a` = the
  MAX over all such pairs (best-matching pair). Full per-cell agreement profile
  of the best pair is reported alongside the scalar.
- **(b) extremal-typical (null)**: for each `s in S_n`, agreement of `s`
  against a sample of up to 300 distinct non-extremal reachable live states at
  `n+1` (seed 0). `A_b` = the 95th percentile of this distribution.
- **(c) typical-typical (null)**: agreement of up to 1000 sampled pairs of
  distinct reachable live states at the SAME `n` (seed 0), for calibration.

### 3.1 Test (i): shared structure across consecutive n

STRONG OUTCOME (family): in SOME fixed `(arm, alignment)`,
`A_a >= A_b + 2` (best extremal-extremal agreement beats the 95th percentile of
extremal-typical by at least 2 cells) for at least 70% of the consecutive-n
pairs (>= 8 of the ~11 pairs across n=10..20).

KILL: if for BOTH arms and BOTH alignments the extremal-extremal agreement is
within +1 cell of the extremal-typical 95th percentile on a majority of pairs,
the low-index agreement is generic forgetting and (i) is NULL — the states share
no more structure across n than a random reachable state does. Said plainly if
so.

### 3.2 Test (ii): fixed operation relating state(n) to state(n+1)/(n+2)

The edge grows by 2 cells per unit `n`. Preregistered operation list (fixed
before running):
- `o1` PREFIX-extension: some `s' in S_{n+1}` has `s` as a prefix (`s' = s`
  then 2 deeper cells appended at the high-index end).
- `o2` SUFFIX-extension: some `s' in S_{n+1}` has `s` as a high-index suffix
  (2 shallow cells prepended at index 0).
- `o3` cocycle `2^k`-prepend analog: test whether the ENDPOINT word of the
  extremal at `n+1` is `2 · (endpoint word of extremal at n)` up to the
  documented `F(2e)=r_2(e_0).F(e)` shift (`RESULTS-ENDPOINT-RESTART-COCYCLE.md`
  eq 1), i.e. whether extremal endpoint words are an orbit under a leading-`2`
  restart. (Endpoint word = the raw source+forced symbol stream, not the edge.)
- `o4` n -> n+2 versions of o1/o2 (the phase-4 restart suggests a period, so a
  relation may only appear at stride 2 or 4).

STRONG OUTCOME: one operation in the list holds for >= 70% of the applicable
pairs in at least one arm. KILL: none of o1-o4 exceeds coincidence (defined as:
the same containment holds no more often between extremal(n) and a typical
state at n+1 than between extremal(n) and extremal(n+1)).

### 3.3 Test (iii): alpha SUPPORT pattern in n

The genuinely new object (not the parity, which re-encodes the string): the
SUPPORT `{i : E_i != 0, 0 <= i <= |E|-2}` of the live state at the killing row
`survival` and the row before it, for each extremal state. Report the support
as index sets under both alignments. STRONG OUTCOME: the support at the killing
row, expressed as offsets from a fixed reference (index 0 OR the deep end
`|E|-1`), coincides across >= 70% of consecutive n in at least one arm/tail.
KILL: the support reshuffles with n (as the missing-block sets did in
`RESULTS-FIBER-EXTREMAL-FAMILY.md` §2) with no stable offset pattern.

## 4. Compute discipline and honesty ceiling

- Single process. Do not fan out; `fastdk_benchmark.py` and
  `terminal_fiber_classes.py` are running and are left alone. Checkpoint each
  `(n,c,arm)` cell to `estate_census.json` as it completes so a timeout loses
  nothing. If n=20 all-W exceeds a wall-clock budget it is reported as "reached
  through n=k exhaustively," per the CONTROL to seed nothing and go as far as
  exhaustive allows.
- CLAIM CEILING (fixed now): even a clean positive on (i)/(ii) does NOT by
  itself deliver the cocycle proof template. That template
  (`RESULTS-ENDPOINT-RESTART-COCYCLE.md`) closes a case because it has an
  autonomous finite quotient of BOUNDED dimension (the L=5, period-32
  traversal). The live-state dimension here grows as `2n`, so a suffix-nested
  extremal family reaches the template ONLY IF a bounded-window kill rule can be
  derived; the closure collisions (bounded summaries collide at lengths 8, 9,
  13; `FACT-INDEX.md:310-319`) and Obstruction D (`PATH.md:768-774`) are the
  standing obstruction to that. The verdict will state the template as "in
  range PROVIDED a bounded-window kill rule is derivable," never as delivered.
- A clean negative is a real result: it makes the needle a per-n certificate,
  not a proof route via this door. It will be stated plainly.
