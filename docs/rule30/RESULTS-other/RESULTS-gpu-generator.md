# GPU centre-column generator: validated, 46x the CPU, and what it cannot do

## Status

**MEASURED (engineering).**  A correct, validated WGPU/WGSL centre-column
generator for the Rule 30 lone seed.  It is a constant-factor speedup.  It
contributes **nothing** to any of the three prize problems, for reasons given in
"Scope" below, and that limitation is structural rather than a matter of budget.

Source: `experiments/rule30/rule30_gpu/`.  Run
`cargo run --release -- <depth> <verify_bits>`.

## Result

| | depth `10^6` | rate | ratio 1:0 |
|---|---|---|---|
| GPU (Apple M4, 10 cores, Metal) | **2.98 s** | 335,643 gen/s | 1.003076726 |
| CPU (`center_column.py`, bit-parallel bigint) | 138.62 s | 7,214 gen/s | 1.003076725850907 |

**Speedup 46x.**  Both agree with the ratio `1.003076725850907` at `10^6`
recorded in `PREREGISTRATION.md`, to every digit the GPU path prints.
GPU throughput is near-flat from `10^5` (411k gen/s) to `10^6` (336k gen/s):
at these sizes the active row still fits in cache and the quadratic wall has not
yet bitten.

**Gate.**  Every run recomputes the first `verify_bits` centre bits with an
independent CPU implementation inside the Rust binary and exits non-zero on any
divergence.  All runs reported here: `MATCH`.

## Architecture

Standard and as proposed: ping-pong storage buffers that never leave VRAM,
`BATCH = 8192` generations recorded into one command encoder per submit, a
history buffer written by the single invocation owning the centre word, and a
`MAP_READ` staging buffer drained once per batch.  `atomicOr` bit-packing gives
32x history compression; the buffer is cleared before every batch because OR can
only set bits.  Active-cone dispatch bounds each batch's dispatch to the words
the light cone can have reached (411k vs 345k gen/s at `10^5`; asymptotically a
2x saving, since `sum_t 2t = T^2` against `2T^2` for full width).

## Four defects fixed, one silent

Recorded because three of them produce *wrong numbers rather than errors*.

1. **Neighbour shifts were swapped.**  With cell `32i+j` in bit `j` of word `i`,
   the left-neighbour word is `(c << 1) | (left >> 31)` and the right-neighbour
   word is `(c >> 1) | (right << 31)`.  The reversed form was checked against a
   dense reference and produces a wrong row at `t = 1`.
2. **Lattice width, the dangerous one.**  The centre cell at time `t` depends on
   cells `[-t, t]`.  A fixed `W`-cell array is correct only while `t <= W/2 - 1`;
   past that the zero boundary is not the true infinite-lattice evolution and
   **every later centre bit is wrong with nothing raised**.  A 10^7-cell array
   silently corrupts everything beyond `t ~ 5*10^6`.  The code now sizes the
   lattice from the requested depth and asserts the margin.
3. **History index must be batch-local** (`step % BATCH`).  A global generation
   counter walks off the end of the history buffer after the first batch.
4. `clear_buffer` requires `COPY_DST` usage on the history buffer; without it
   the encoder is rejected at validation.

## The real wall is bandwidth, not cores or VRAM

Each step reads and writes the full active row, so reaching depth `T` moves
about `T^2 / 2` bytes **regardless of core count**.  This dominates every other
consideration:

| target | bytes moved | Apple M4 (~120 GB/s) | 8x H100 (~24 TB/s aggregate) |
|---|---|---|---|
| `10^9` (equals the published record) | `5 * 10^17` | ~48 days | ~6 hours |
| `5 * 10^10` | `1.25 * 10^21` | — | **~1.6 years, ~$500k** |
| `2 * 10^13` (what `RESULTS-patch-scan.md` says rung 1 needs) | `2 * 10^26` | — | **~500,000 years** |

The VRAM ceiling (two rows of `2T` bits; ~250 MB at `10^9`, ~25 GB at `10^11`,
~250 GB at `10^12`) is real but is **never the operative limit**: the time wall
bites two to three orders of magnitude earlier.  Estimates circulating at "a few
hours for `10^9` on a desktop GPU" or "a month and $25k for `5*10^10` on an 8x
H100 pod" are optimistic by roughly two orders and twenty-fold respectively.

## Scope: why this cannot touch the prizes

* **P3** asks for `Omega(n)` **work**.  Parallelism reduces wall-clock, not
  work.  Worse, CA prediction is P-complete (Neary-Woods 2006; `PATH.md` 8.3),
  i.e. believed *inherently sequential* and not efficiently parallelizable, so
  the theory predicts exactly this: large constant factor, no asymptotic gain.
  Wolfram's announcement already notes word-packing yields constant factors only.
* **P1** is not decidable from any finite prefix: no computation distinguishes
  "aperiodic" from "period longer than what was computed" (`PREREGISTRATION.md`
  Arm 1).  Going from `10^9` to `10^11` bits changes no theorem.
* **P2** is an asymptotic density; no finite prefix bears on a limiting
  frequency (`PATH.md` 8.2, ceiling on statistical testing).

## What it is actually for

`PATH.md` 8.5 records that **no public SIMD, GPU, FPGA or distributed
centre-column generator exists**, and that nobody outside Wolfram Research has
published a computation within five orders of magnitude of the `10^9` record.
This is a validated open implementation of that missing artifact.  Its research
value is as **measurement infrastructure**: it extends the reachable depth for
instruments like `RESULTS-patch-scan.md` by a large constant factor, and it
makes the never-performed cross-check in `PATH.md` 8.5 cheap — diffing an
independent generator against the Wolfram Data Repository datasets and the OEIS
`b051023.txt` b-file.  Independent recomputation has caught a real error in
A051023 once before (Cristofani, 2004, from term 64).

## Reproduction

```sh
cd experiments/rule30/rule30_gpu
cargo run --release -- 1000000 50000     # depth, bits to verify
```

CPU baseline:

```sh
cd experiments/rule30
uv run python -c "from center_column import center_column; center_column(1000000)"
```
