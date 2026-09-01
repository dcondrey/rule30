# Literature check: what survives as novel in the fuel instrument

Run 2026-08-31, against `RESULTS-openevolve-p3-fuel.md` (register row 92), to
decide whether that instrument supports a standalone contribution off the Rule
30 axis. Verdict first: **four of the five claims are owned or closely
adjacent; one narrow slice survives.**

The citations below were gathered by a retrieval agent reading primary sources
and are recorded here with their identifiers so they can be checked. **They have
not been independently re-verified in this repo.** Treat every one as
"claimed, needs confirmation before it enters a submission".

## The one thing that survives

> **Cost-model granularity is not a free parameter.** When fitness is a fitted
> asymptotic exponent, charging a variable-width primitive operation by *bits*
> rather than by *machine words* injects a spurious `log n` term that corrupts
> the fitted exponent: 2.12-2.15 against a known `Theta(n^2)` ground truth,
> where the word model recovers 1.99946 at `r^2 = 0.9999999`.

Nothing found covering it. The near neighbours each miss it for a stated
reason: EIP-2565 is a fee schedule and never fits an exponent; Cachegrind
counts fixed-width x86 instructions so granularity cannot arise; Albert et al.
derive cost bounds rather than fitting measured exponents.

This is a result about cost-model design, checked against ground truth. It is
one sentence and one measurement. It is not a paper on its own; it is the
contribution *inside* a short paper whose motivation is the wall-clock failure.

**Now a three-point claim, at two distinct exponents.** As first written this
rested on two points (bits vs words), which was weak: two points on a
granularity axis do not establish that granularity is the controlling variable.
`experiments/openevolve-p3/PREREG-flat-opcode-ablation.md` added the third point
in the other direction, a flat opcode counter charging `O(1)` per operation
regardless of width, and its pre-registered **strong outcome** was obtained:

| candidate | true | word model | flat opcode |
|---|---|---|---|
| (c) bit-packed | 2 | 1.99410 | **0.99938** |
| (e) cubic | 3 | **2.97449** | **1.99690** |

The flat counter is wrong by a full exponent-unit on both, while the word model
recovers two *different* known exponents to within 0.03 — the first check of
this instrument against any exponent other than 2. Charging too coarsely loses
1.0; charging too finely (raw bits) adds a spurious `log n` worth 0.12-0.15.

None of this changes the decision below, which was made on prior-art grounds
before either run was read.

## What is owned, with the citation that owns it

**Q1. Counter-beats-clock as evolutionary-search fitness — OWNED.**
Bouras, Hanna & Petke, "Optimised Fitness Functions for Automated Improvement
of Software's Execution Time", SSBSE 2025, LNCS 16228,
doi:10.1007/978-3-032-24839-8_4. Compares 21 approximations of execution time as
fitness (perf counters, RAPL energy, weighted instruction cycles); perf `cycles`
outperforms wall-clock by 5.1%. Same problem setting, already measured.
Supporting: Langdon & Hanna, GI 2026 (fitness *is* perf instruction count);
Mytkowicz et al., ASPLOS 2009, "Producing Wrong Data Without Doing Anything
Obviously Wrong!" (measurement bias, the best single framing cite); Jin & Branke,
IEEE TEC 9(3), 2005 (noisy fitness — but this is about *stochastic objectives*
and resampling, not a broken instrument, so cite for framing only).

*Do not claim "nobody fits an asymptotic exponent as fitness."* That is a gap in
what people do, not in what is known, and a reviewer supplies the corollary for
free once Bouras is granted.

**Q3. Proportional-width charging of bignum operations — ADJACENT, broad
version dead three ways.** EIP-2565 charges `ceil(max_length/8)` words squared,
i.e. proportional-width metering, public since 2020 (revised by EIP-7883). The
word-RAM model exists precisely *because* unit cost is wrong for
arbitrary-precision arithmetic, so "a bytecode counter is the wrong cost model
for a bignum language" is the standard justification for the model, not a
missing observation. Deterministic parameterized cost models over bytecode are
published: Albert, Arenas, Genaim, Puebla & Zanardini, "Cost Analysis of Java
Bytecode", ESOP 2007; Binder et al., "Exact and Portable Profiling for the JVM
Using Bytecode Instruction Counting", ENTCS 2006.

**Also drop deny-by-default from the novelty claim.** It is sound engineering and
it is what every sandbox does. Claiming it weakens the rest.

**Q4. Deterministic counter replacing the clock — OWNED in general.**
Cachegrind/Callgrind: deterministic instruction counting, explicitly
reproducible, explicitly "does not measure time spent". The statistical branch
is the acknowledged alternative and should be cited as the road not taken:
Chen & Revels, "Robust benchmarking in noisy environments", arXiv:1608.04295
(the BenchmarkTools.jl paper) models timings as non-i.i.d., heavy-tailed,
bimodal and drifting, and explicitly *declines* the deterministic route as
platform-specific and privilege-requiring; Stabilizer (Curtsinger & Berger,
ASPLOS 2013) randomizes layout to make timing statistically sound rather than
eliminating it. None of these addresses variable-width primitives, because none
of their target languages has them at the primitive level.

## What survives weakly, as evidence rather than as topic

The wall-clock failure itself. Frame it as **existence-of-falsification on
ground truth**, which is a different class of evidence from Bouras et al.'s
aggregate proxy comparison: a rank inversion on a pair with a *provable*
asymptotic separation (naive 1.807-2.164 vs bit-packed 1.573-1.833, overlapping),
and a program credited with beating **itself** by 0.41 exponent-units (0.7896 vs
0.200000). Motivation, not contribution. Order it that way.

## What survives as a scoped, cited absence

Across six LLM-driven code-evolution systems whose fitness specification was
read directly, **none reports a control candidate or an instrument-validation
step for its measurement.**

| system | fitness signal | timing? | instrument validation? |
|---|---|---|---|
| FunSearch (Nature 2024) | cap-set size; bin-packing excess bins | only as a discard timeout | none |
| AlphaEvolve (arXiv:2506.13131) | task scalar; **wall clock for TPU kernels** | yes | correctness only; the cascade is a cheap prefilter, and fleet measurements confirmed the *simulator*, not the timer |
| ShinkaEvolve (arXiv:2509.19349) | packing radii; AIME count; ALE-Bench; MoE loss | never | **partial** — cross-validated its *verifier* against AlphaEvolve's exact code (agreement < 1e-6), not its timer |
| OpenEvolve `examples/rust_adaptive_sort` | `0.6*perf + 0.4*adaptability` | yes, parses `avg_time` from a subprocess | none |
| AlgoTune (arXiv:2507.15887) | speedup vs SciPy/sklearn/CVXPY, harmonic mean | yes | none |
| Ishibashi, Yano & Oyamada (arXiv:2605.15221) | packing radii | no | none |

**Bounded negative.** This covers six systems read directly. It is *not* a
code-search sweep: `api.github.com/search/code` returns 401 unauthenticated and
GitHub web search gives false negatives through fetch, so no search-based
absence claim is available. State the bound in the paper.

**AlgoTune is the closest prior art and must be engaged head-on.** Untimed
warmup, then one timed `perf_counter_ns` measurement, repeated 10x keeping the
minimum, on an isolated AMD EPYC 9454. That is deliberate, serious timing
methodology. It is **mitigation-by-statistics**, not **replacement-by-counter**,
and it runs at fixed instance sizes so it never fits an exponent. That is the
distinction to draw, and it is a fair one.

Related but *not* overlapping: Ishibashi et al. establishes harness design as a
first-class research object, but its concern is evaluation **hacks**, not
evaluation **noise** (see also EvilGenie, arXiv:2511.21654).

## Naming: rename before publication

"Fuel" collides with wasmtime's meaning and is **semantically inverted** from
this instrument's. Wasmtime fuel (and EVM gas) is a *budget* that is consumed
and traps at zero, charged one unit per instruction, used to bound untrusted
code. This instrument's fuel is a *cost metric to be minimized*, charged
proportionally, with no trap. No third meaning found in the program-search
literature, so the collision is with the metering world rather than the target
field.

Recommended: *word cost* or *charged word count*. If "fuel" is kept, the
inversion must be stated in the sentence that introduces it. The existing
explicit rejection of wasmtime for reuse is a good argument and should stay.

Renaming `fuel.py` and its API across `experiments/openevolve-p3/` is a refactor
of experiment code and was **not** done here; it is proposed, not applied.

## Decision: NOT PUBLISHED. Do not re-propose.

**Decided 2026-08-31 by the user, on reading this check: dropped.** The fuel
instrument was ranked first among three candidate contributions specifically
because it was believed to be off the Rule 30 axis *and* novel. It is not novel.
Once Bouras et al., Cachegrind and EIP-2565 are granted, what remains is one
sentence of genuine result surrounded by competent engineering on owned ground,
and one sentence does not carry a paper -- not even a short one at GI @ ICSE or
SSBSE, where the incumbent already lives and would be the reviewer.

The shape that *was* on the table, recorded so nobody reconstructs it from
scratch and reaches the same place: motivation from the self-beating control;
contribution the granularity result; the six-system absence as a section; and
two honest costs that would have had to survive into it -- the instrument has
**never been run in an actual search**, and the anti-lookup-table gate is weaker
than the pre-registered one because the fuel ladder stops at `n = 4000` against
the wall clock's 16000 (`RESULTS-openevolve-p3-fuel.md` section 8).

**The instrument itself stands and is unaffected.** It remains the correct tool
for row 91's blocked arm, and register row 92's validation claims are all
measured and hold. What this check removes is the *publication* claim, not the
engineering. The rename to *word cost* is still worth doing if the instrument is
ever used in a write-up of any kind, for the wasmtime semantic inversion above.

**Typed exclusion, in the register's own idiom:** a deterministic cost counter
replacing wall-clock fitness in program search is **prior art, not a
contribution**. Any future arm proposing to publish an instrument of this shape
should read this file first and needs a reason that survives Bouras, Hanna &
Petke (SSBSE 2025) and Cachegrind specifically.
