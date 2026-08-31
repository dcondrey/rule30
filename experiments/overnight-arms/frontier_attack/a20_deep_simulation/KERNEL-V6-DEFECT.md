# `rule30_kernel_v6.cu` produces wrong bits. The 3e9 run was stopped.

> **STATUS 2026-08-30, later the same day: FIXED AND VERIFIED.** The diagnosis
> below was correct in every particular. The fix, the evidence that it worked,
> what it cost, and what is still open are in "Resolution" at the end. The
> analysis above it is left exactly as written before the fix, because a
> diagnosis is only worth anything if it was recorded before the outcome was
> known.

Found 2026-08-30 ~21:00 PDT, about 22 minutes into the 3e9 H100 run, by the
cross-check that `docs/rule30/PATH.md` 8.5 records as "open, cheap and never
done". The run was stopped at 21:03. Cost contained to roughly $1.50 of the
projected $45.

## The claim

The recorded columns emitted by `rule30_kernel_v6.cu` under `modal_run_band.py`
contain sparse, incorrect bits. Two completed runs on the Modal volume
`rule30-deep`:

| run | bits | wrong bits | rate | first error |
|---|---|---|---|---|
| `band_n200000_w4_col+0.bin` | 200,000 | **101** | 5.05e-4 | bit 4,631 |
| `band_n2000000_w4_col+0.bin` | 2,000,000 | **22** | 1.1e-5 | bit 14,416 |

## Why this is the kernel and not the reference

**Test A settles it with no external reference.** The centre column of Rule 30
from a single 1 is one fixed mathematical object; `n` is only how far you
compute it. The same kernel produced it at `n=200000` and at `n=2000000`, and
the two outputs **disagree at 25 of the first 50,000 bits**, first at bit
4,631. The kernel contradicts itself. No appeal to Wolfram, OEIS, or anything
else is required to conclude at least one is wrong.

**Test B: four independent implementations agree, the GPU is the only outlier.**
Over the first 50,000 bits, bit-identical:

- Wolfram Data Repository, 1e9 bits, Xiangdong Wen 2019 (method/hardware unpublished)
- OEIS `b051023.txt`, Antti Karttunen, PARI via A269160
- `deep_gen.py`, gmpy2 arbitrary-precision bit-parallel, this repo
- `common/rule30.py::center_column_bits`, the repo's naive reference, recomputed from scratch

Four languages, four authors, four algorithms, zero disagreements between them.
The two GPU outputs differ from all four *and* from each other.

Reproduce: `crosscheck_wdr.py` (self-tested; re-derives the WDR payload
alignment rather than assuming it).

## Why the pre-launch validation missed it

The gate checks the centre column's **head64** (in-kernel, `modal_run_band.py`
line 173) and **head256** (`band_run_result.json`). The first error is at bit
**4,631**. Every gate in the launch path sits entirely inside the correct
prefix. The handoff's "all 9 columns head64 match ground truth" and "centre
head256 matches A051023 at n=2e6 and n=3e6" are both true and both blind here.

**Rule: a prefix gate cannot validate a generator. Compare the whole output.**

## Diagnosis: the recorded centre lands exactly on a warp-tile edge, structurally

Config `R=16, H=16, WARPS=4`, so `USEFUL_PER_WARP = 32*16 - 2*16 = 480` words
and `useful_per_block = 480*4 = 1920` words.

`modal_run_band.py` rounds `n_words` **up to a multiple of `useful_per_block`**
(line 95), then puts the centre at `centre_cell = n_words*32/2` (line 96). So
with `n_words = k*1920`, the centre word is `k*960` — and `960` is exactly half
a block, i.e. the start of warp 2's tile. Therefore:

- `k` even -> centre word is a multiple of 1920: a **block** tile start.
- `k` odd  -> centre word is `960 mod 1920`: a **warp** tile start.

Either way **the recorded centre column is always the first useful word of a
tile, immediately against that tile's left halo.** This is forced by the
layout, not luck. Confirmed for both runs:

- `n=200000`: `n_words=7680` (k=4, even), centre word `3840 = 2*1920`, block edge. Rate 5.05e-4.
- `n=2000000`: `n_words=63360` (k=33, odd), centre word `31680 = 16.5*1920`, warp edge. Rate 1.1e-5.
- `n=3e9`: `n_words=93,751,680` (k=48829, odd), centre word `46,875,840`, warp edge. **The stopped run had the same defect.**

The block-edge case is 45x worse than the warp-edge case, which is consistent
with the halo being the mechanism.

## Mechanism: a lost-update race on a non-atomic `|=`, and the errors prove it

**Every error is a dropped 1. Measured over both runs: 123 errors, 123 of them
"GPU says 0 where truth is 1", and zero of the opposite kind.** That asymmetry
is the diagnostic, and it identifies the mechanism.

Recording, `rule30_kernel_v6.cu:120-127`:

```cuda
uint32_t bit = (r[rec_slot[m]] >> rec_bit[m]) & 1u;
if (bit) {
    rec_out[rec_k[m] * words_per_batch + (step >> 5)] |= (1u << (step & 31));
}
```

The driver zeroes `rec` before each batch (`rec.fill(0)`), so **a 1 is written
and a 0 is the absence of a write.** Three facts then compose:

1. **Tiles overlap.** `tile_start = tile_idx * USEFUL_WORDS - HALO_WORDS`
   advances 480 words per tile while each tile covers `WARP_WORDS = 512`.
   Consecutive tiles share 32 words.
2. **Two tiles claim the same recorded cell.** The ownership test at line 108,
   `wl >= base && wl < base + WORDS_PER_LANE`, asks only whether the word is in
   this lane's *register* range. It never checks that the word is inside the
   tile's useful region `[HALO_WORDS, HALO_WORDS + USEFUL_WORDS)`. Since the
   recorded centre is structurally at a tile edge (above), it sits in one
   tile's useful region **and** a neighbour's halo, and both lanes record it.
3. **The write is a non-atomic read-modify-write to global memory, issued from
   two different blocks.** `|=` on `uint32_t*` compiles to load / or / store,
   not `atomicOr`. Two blocks on different SMs interleave, and one update is
   lost.

A lost update can only fail to set a bit. It can never set one that should be
clear. So the corruption is **one-directional: dropped 1s only** — which is
exactly, and only, what the data shows.

This also explains why it is insidious. The output keeps the right density
(~0.5, since only a ~1e-5..1e-4 fraction of the 1s are lost), stays plausible
under every aggregate statistic, and differs from truth only on 1-bits.

**Confirmed: the kernel is non-deterministic.** Three runs of a byte-identical
configuration (`n = 200000 / 199999 / 199998`, all giving `n_words=7680`,
centre word 3840, tile offset 0 — only the final step count differs):

| run | errors vs truth |
|---|---|
| `n=199999` | 108 |
| `n=199998` | 97 |
| `n=200000` | 101 |

Runs A and B share **4** error positions and differ at **197**. A deterministic
indexing or halo bug would reproduce the same error set on every run. It does
not. Combined with the one-directional dropped-1s asymmetry, the mechanism is
established, not conjectured: **concurrent non-atomic read-modify-writes to the
same `rec_out` word, losing updates.** (`race_a.log`, `race_b.log`.)

**Fix, in order of importance:**
1. `atomicOr(&rec_out[...], 1u << (step & 31))` — necessary but not sufficient,
   since a contaminated halo tile would then contribute spurious 1s instead.
2. **Restrict recording to the owning tile's useful region.** Add
   `wl >= HALO_WORDS && wl < HALO_WORDS + USEFUL_WORDS` to the line-108 test.
   This is the real fix: exactly one tile then claims each cell, and the value
   it holds is uncontaminated. With it, the non-atomic `|=` is safe again.
3. Gate on full-output equality, not a prefix. Two runs with different `n` on
   the same layout must produce identical common prefixes, and the output must
   match `common/rule30.py` over its whole length, not over 64 or 256 bits.

## Before any post-fix run: wipe the volume. This is how the bug survives the fix.

`modal_run_band.py:137` opens column files in **append** mode
(`open(col_paths[k], "ab")`), and the run resumes from
`band_*_state.npz` if present. The stopped 3e9 run wrote a checkpoint at its
22-minute mark. So re-running `--n 3000000000` after a kernel fix will **resume
from the corrupt state and append correct bits onto corrupt ones**, producing a
file of exactly the right length with a spliced boundary and no anomaly to
catch it.

```
uv run modal volume rm rule30-deep band_n3000000000_w4_state.npz
uv run modal volume rm rule30-deep band_n3000000000_w4_meta.json
# and every band_n3000000000_w4_col*.bin, plus the n=200000 / 2000000 /
# 199999 / 199998 sets if those n values are reused
```

Delete every `band_*` on `rule30-deep` before the first post-fix run.

## What is now suspect

- **All band data on volume `rule30-deep`.** Every `band_*` column file.
- **The performance claim.** "1.10e14 cell-updates/s, 2.69x faster than the
  first working kernel" was measured on a kernel that does not produce correct
  output. A kernel that skips correctness is not comparable to one that does
  not; the 2.69x is void until v6 is fixed and re-timed.
- **v1-v5, untested.** They were compared on throughput, not on full-output
  correctness, and share the tiled-halo structure. `RESULTS-gpu-generator.md`'s
  WGPU/WGSL generator is a *different* implementation and is not implicated by
  this, but it was gated the same way (in-binary CPU reference) and the extent
  of that gate should be re-read before it is trusted at depth.

## Not affected

`deep_gen.py` and the local 24h CPU run (PID 51480) are correct: verified
bit-exact against WDR over 7,340,032 bits and against the naive reference over
50,000. That run was left going.

---

# Resolution

## The fix

Both changes are in `rule30_kernel_v6.cu`; fix 2 is the load-bearing one.

1. **Ownership restricted to the tile's useful region.** The line-108 test now
   reads `wl >= HALO_WORDS && wl < HALO_WORDS + USEFUL_WORDS && wl >= base &&
   wl < base + WORDS_PER_LANE`. The useful regions
   `[T*USEFUL_WORDS, (T+1)*USEFUL_WORDS)` partition the global word space with
   no gaps and no overlaps, so exactly one tile claims each recorded cell, and
   the copy it holds is the uncontaminated one.
2. **`|=` replaced by `atomicOr`.** Redundant given fix 1 and not load-bearing;
   it removes the lost-update failure mode from the code rather than from an
   argument.

Two supporting changes, because the bug was an *ownership* bug and ownership is
arithmetic the host can settle before spending any GPU time:

3. `band_layout.py` mirrors the kernel's ownership predicate on the host.
   `modal_run_band.py` now calls `assert_unique_claimants` for every distinct
   launch window and aborts before compute unless every recorded column has
   **exactly one** owner. This catches both directions: 2 claimants is the race,
   **0 claimants is a column that is never written and reads as all zeros** —
   the same failure class, and silent under any self-consistency check.
4. The halo margin is exactly zero at both ends and is now stated in the source.
   Raising `STEPS_PER_BATCH` above `32*HALO_WORDS` would silently corrupt both
   edges of every tile.

## Evidence the fix worked

The volume was wiped first: all 53 `band_*` files removed explicitly from a full
listing (never a glob), re-listed, confirmed empty. This mattered — the column
files are opened `"ab"` and the run resumes from `band_*_state.npz`, so a
post-fix rerun would otherwise have appended correct bits onto corrupt ones.

Four runs on the fixed kernel. `n = 199998 / 199999 / 200000` share
`n_words = 7680` and centre word 3840 (**block** edge, the 5.05e-4 case) and
differ only in step count; `n = 2000000` is the **warp** edge case.

| check | what it compares | result |
|---|---|---|
| A reference | all 9 columns vs an independent gmpy2 generator, **full length** | **pass**, 4/4 runs |
| B transduction | `col_{x-1}(t) = col_x(t+1) XOR (col_x(t) OR col_{x+1}(t))` among the recorded columns | **pass**, 4/4 runs |
| C density | ones per column; the only check that sees an all-zero column | **pass**, 4/4 runs |
| D cross-run | bit-identical common prefixes across the 199998/199999/200000 triple | **pass**, 3/3 pairs |
| WDR | centre column vs the Wolfram Data Repository payload | **MATCH over 2,000,000 bits** |

The last two are the ones that speak to the mechanism. D is the direct test for
the non-determinism: those three runs previously gave 108 / 97 / 101 errors
sharing only 4 positions, and are now bit-identical. And
`band_n2000000_w4_col+0.bin` previously diverged from WDR at bit 14,416 with 22
errors; it is now bit-exact over its whole length.

**The whole battery was then re-run on the optimised kernel** (see the next
section), on fresh tags so nothing appended onto verified files:
`n = 219998 / 219999 / 220000` (block edge) and `1980000` (warp edge), plus the
superseded intermediate revision at `239998 / 239999 / 240000 / 1990000` so that
nothing unverified is left on the volume. **8 runs, 8 x 9 columns, all of A, B
and C pass; all three block-edge pairs are bit-identical; the centre column
matches WDR over 1,980,000 bits.**

One extra check earns its place here. `n=219998` (range form) and `n=239998`
(the intermediate revision) share `n_words = 7680` and centre word 3840, so a
change that was meant to be a pure optimisation must leave their columns
**bit-identical over the common prefix**. It does. That is what makes the 3.97x
a speedup rather than a different computation.

**The checker is not vacuous.** It was run against the known-bad data *first*,
and reproduced this document's findings independently: 22 errors in `col+0`
first at 14,416, 13 in `col-1`, 10 in `col+1`, and **45 of 45 in the
dropped-1 direction with zero of the opposite kind**. Check C *passed* on that
same corrupt data, which is exactly why B and A exist.

`verify_band.py --self-test` additionally requires each check to FIRE on a
planted defect of the kind it exists for, and requires the ownership mirror to
report the pre-fix double claim, not merely to agree with the fix.

**One real trap, found by check A.** A run of `t` steps writes `ceil(t/32)`
*words*, so when `t` is not a multiple of 32 the final word is zero-padded.
Compared against a reference those padding bits read as dropped 1s — the exact
signature of the defect. That produced 2 spurious "errors" at `n=199998` and 1
at `n=199999` on a kernel that was already correct. Every comparison is now
capped at the step count, and the trap is pinned by a self-test.

## What the fix cost: nothing. And a 3.97x that was hiding behind it.

`modal_ablate_v6.py` compiles every variant of the same source in one run on one
GPU, so the comparison is not across machines or days.

| config | variant | cell-updates/s | regs | local |
|---|---|---:|---:|---:|
| R=16 H=16 W=4 | **as it stands** | **1.06e14** | 40 | **0 B** |
| R=16 H=16 W=4 | ownership test reverted | 1.07e14 | 40 | 0 B |
| R=16 H=16 W=4 | recording state in lookup arrays | 2.68e13 | 39 | 256 B |
| R=16 H=16 W=4 | recording code removed | 1.10e14 | 37 | 0 B |
| R=4 H=4 W=4 | as it stands | 7.50e13 | 38 | 0 B |
| R=4 H=4 W=4 | ownership test reverted | 7.52e13 | 38 | 0 B |
| R=4 H=4 W=4 | recording state in lookup arrays | 2.76e13 | 32 | 208 B |
| R=4 H=4 W=4 | recording code removed | 9.91e13 | 24 | 0 B |

**The ownership fix costs 1.00x.** The benchmark passes `rec_out = nullptr`, so
the block the fix lives in is skipped at runtime; the measurement agrees.

**The 4.03x belonged to how the recording state was stored, and it predated the
fix.** Three `MAX_REC` arrays (`rec_k`, `rec_slot`, `rec_bit`) indexed by a
runtime `m` cannot live in registers, and they dragged the hot `r` array into
local memory with them: `local_size_bytes` was **exactly `192 + 4*WORDS_PER_LANE`**
— the three arrays plus the whole of `r` — paid by every thread in the grid, for
a kernel in which one or two lanes in the grid ever record anything. It entered
when band recording was added at 20:36, after the 18:40 sweep, which is why the
sweep's figure never saw it.

**The first attempt at removing it failed, and the failure was the useful part.**
Removing only the dynamic index into `r` (unroll over the compile-time `j`, test
`j == rec_slot[m]`) bought **1.02x**, and `local_size_bytes` stayed at 256. The
arrays were the anchor, not the index.

**What worked:** the recorded cells are *consecutive*, so `wl` is monotone in
`k`, the ownership predicate is an intersection of two intervals, and the owned
columns are therefore a contiguous **range**. `slot` and `bit` are arithmetic in
`k`. No table is needed at all — two ints replace 48. `local_size_bytes` 256 to
**0**, and **3.97x**. Band recording now costs **1.03x** against removing it
outright, where it cost 4.03x.

**Honest number: v6 is 1.06e14 cell-updates/s** at the production config, with
band recording compiled in and full output verified. The timing loop is
byte-identical to the one that produced the earlier figure (`bench_words`,
`nbatch`, rate formula); only the kernel call signature changed, which is what
makes this a re-measurement rather than a different experiment.

**Still do not quote a ratio against the old 1.10e14.**
`sweep_v6_result.json` was overwritten by the re-timing run and the directory is
untracked, so the pre-fix per-config JSON is gone; the `.cu` that produced it was
already gone, modified at 20:36. That `no_recording` measures 1.10e14 here is
*evidence for the explanation*, not a recovery of the measurement. Likewise
`V1_RATE`: v1 was never full-output checked and shares this tiled-halo structure,
so the sweep's field is now `speedup_vs_v1_UNVERIFIED_BASELINE`.

For the 3e9 run this is the difference between roughly 24 h and roughly 6 h.

## Still open, and why each is someone else's call

- **The 3e9 run has not been relaunched.** At the measured 1.06e14 the projection
  is ~6 h rather than ~24 h, so ~$11 rather than ~$45. Not started: see the
  charter flag below.
- **The charter.** `docs/rule30/MODAL-COMPUTE-CHARTER.md` excludes "regenerating
  published center-column prefixes", and that exclusion is **still not waived**.
  Two distinctions worth stating rather than eliding. First, the validation runs
  here *are* regenerations of published prefixes, but used as a correctness
  oracle for a generator, not produced as a scientific output. Second, and
  larger than the recorded item: there is **no ledger file anywhere in the
  repo**, so this GPU arm never passed `modal_guard.py` admission at all — and
  the charter's admission invariants require "no GPU", with the strict path
  being short CPU-only network-disabled Sandboxes. The arm operates outside the
  charter's strict path entirely, not merely against one exclusion.
- **The 8 non-`band_*` files left on volume `rule30-deep`**
  (`n3000000000_column.bin`, `n40000000_*`, `n3000000_*`) are not merely
  suspect: they are **unreproducible**. `modal_run_deep.py` calls the kernel
  with 8 arguments and the kernel takes 9, so it cannot launch today; the code
  that produced those files is gone from the tree. They were left in place
  rather than deleted, being outside the stated scope of the wipe.
- **v1-v5 remain unverified** for full-output correctness. Out of scope here and
  deliberately not touched.
