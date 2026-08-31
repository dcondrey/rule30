// Rule 30 kernel v6: per-lane register chunks + warp shuffles at the lane
// boundaries. Shared memory is used ONCE per batch to stage in/out, never in
// the step loop. No __syncthreads() in the step loop.
//
// Measured on H100 (cell-updates/s). v1-v5 were gated on a 64-bit PREFIX of
// OEIS A051023, which is not a correctness gate on a generator -- see
// KERNEL-V6-DEFECT.md -- so read these as throughput only. v1-v5 have never
// been checked for full-output correctness and share this file's tiled-halo
// structure; do not quote a speedup against them as a speedup over a
// known-good kernel.
//   v1  uint32 shared stencil, STRIDED, 1 sync/step, 256 steps  4.09e13
//   v2  uint64 register chunks, 2 syncs/step                    2.84e13
//   v3  uint64 private halo, 0 syncs, 64 steps/batch            2.53e13
//   v4  uint32 ping-pong shared, CONTIGUOUS chunks              2.84e13 (C=4)
//   v5  warp shuffles, 1 word/lane, 32 steps/batch              3.42e13
//   v6  this file, R=16 H=16 W=4, band recording compiled in    1.06e14
//   v6  same, recording state held in lookup ARRAYS             2.68e13
//   v6  same, recording code removed entirely                   1.10e14
//
// v6 is the only one whose FULL output has been verified: all 9 recorded
// columns bit-exact against an independent gmpy2 generator, cross-run
// bit-identical, and the centre column bit-exact against the Wolfram Data
// Repository over 1.98e6 bits. See KERNEL-V6-DEFECT.md and verify_band.py.
//
// The gap between rows 1 and 2 is NOT the ownership fix, which measures 1.00x:
// it lives in a block the benchmark skips. It is where the recording state
// lives. Holding it as three MAX_REC arrays indexed by a runtime m puts them in
// LOCAL memory, and that dragged the hot `r` array down with them --
// local_size_bytes was exactly 192 + 4*WORDS_PER_LANE, the arrays plus the whole
// of r -- on every thread in the grid, for a kernel where one or two lanes in
// the grid record anything. Cost: 4.03x.
//
// Removing only the dynamic index into r, and keeping the arrays, bought 1.02x:
// the arrays were the anchor. The fix is that the recorded cells are
// CONSECUTIVE, so the owned columns form a contiguous range and slot/bit are
// arithmetic in k; no table is needed. local_size_bytes 256 -> 0, and recording
// now costs 1.03x against removing it outright. Numbers from
// modal_ablate_v6.py, which compiles every variant in one run on one GPU.
//
// What the four failures taught, in order:
//   - v4's halving per doubling of C exposed C-way bank conflicts; v1 wins
//     because STRIDED shared access is conflict free.
//   - v5 removed shared traffic entirely via shuffles and still lost, because
//     one word per lane caps the batch at 32*HALO_LANES steps, so it pays far
//     more global round trips than v1's 256-step batches.
//
// v6 takes the win from each: shuffles for the stencil (no bank conflicts, no
// syncs) AND R words per lane so a warp spans 32*R words, restoring long
// batches. A warp holding 32*R words tolerates HALO_WORDS words of decay at
// each end, buying 32*HALO_WORDS steps per global round trip. Inside a lane
// the neighbours are already in registers; only the two lane-boundary words
// move, via one __shfl_up_sync and one __shfl_down_sync per step, regardless
// of R.
//
// Global loads are staged through shared memory once per batch so the global
// access stays coalesced: a lane's chunk is contiguous, which would otherwise
// make the direct global read stride-R and waste ~R x the transactions.

#include <stdint.h>

#ifndef WORDS_PER_LANE             // R
#define WORDS_PER_LANE 8
#endif
#ifndef HALO_WORDS                 // words of decay per end of the warp tile
#define HALO_WORDS 8
#endif
#ifndef WARPS_PER_BLOCK
#define WARPS_PER_BLOCK 4
#endif

#define WARP_WORDS (32 * WORDS_PER_LANE)
#define STEPS_PER_BATCH (32 * HALO_WORDS)
#define USEFUL_WORDS (WARP_WORDS - 2 * HALO_WORDS)
#define FULL_MASK 0xffffffffu

// The halo margin is EXACTLY ZERO, by construction, at both ends.
// A tile loads WARP_WORDS words = 32*WARP_WORDS cells; Rule 30's cone eats one
// cell per end per step. After s steps, local cells [0,s) and (32*WARP_WORDS-1-s,
// ...] are contaminated. The useful region is local cells
// [32*HALO_WORDS, 32*(HALO_WORDS+USEFUL_WORDS)). Stage-out runs after
// steps <= STEPS_PER_BATCH = 32*HALO_WORDS, so the first useful cell 32*HALO_WORDS
// is clean iff 32*HALO_WORDS >= steps -- equality, not slack. Recording reads the
// state after at most steps-1 steps, one better.
// Raising STEPS_PER_BATCH above 32*HALO_WORDS silently corrupts both edges.

// block_offset lets the host launch only the blocks covering the active
// light cone. To produce c_0..c_n only cells with |x| <= min(t, n-t) matter,
// and that region is self-consistent: truncating outside it corrupts only
// cells that were already going to fall out of the cone. Launching the
// diamond instead of the full triangle halves total work.
// Band recording: instead of one centre column, record n_rec CONSECUTIVE
// columns starting at cell index rec_lo_cell. Two adjacent columns are the
// width-two trace that Jen 1990 Prop. 3 / Kopra Thm 3.5 concern, and they
// determine the whole left half-plane by iterated inverse transduction
// col_{x-1}(t) = col_x(t+1) XOR (col_x(t) OR col_{x+1}(t)). They do NOT give
// the right half, so this is not resumable state; the row checkpoint is.
//
// out layout: column k's bits for this batch live in
//   rec_out[k * words_per_batch + (step >> 5)], bit (step & 31), LSB-first.
#ifndef MAX_REC
#define MAX_REC 16
#endif

extern "C" __global__ void rule30_v6(
    const uint32_t* __restrict__ src,
    uint32_t* __restrict__ dst,
    uint64_t n_words,
    int64_t rec_lo_cell,
    int n_rec,
    uint32_t* __restrict__ rec_out,
    int steps_this_launch,
    int64_t block_offset,
    int words_per_batch)
{
    __shared__ uint32_t stage[WARPS_PER_BLOCK][WARP_WORDS];

    const int lane    = threadIdx.x & 31;
    const int warp_id = threadIdx.x >> 5;
    const int64_t tile_idx =
        ((int64_t)blockIdx.x + block_offset) * WARPS_PER_BLOCK + warp_id;
    const int64_t tile_start = tile_idx * USEFUL_WORDS - HALO_WORDS;

    // coalesced stage-in: consecutive lanes read consecutive words
    for (int i = lane; i < WARP_WORDS; i += 32) {
        int64_t gi = tile_start + i;
        stage[warp_id][i] = (gi >= 0 && gi < (int64_t)n_words) ? src[gi] : 0u;
    }
    __syncwarp();

    // each lane pulls its contiguous chunk into registers
    const int base = lane * WORDS_PER_LANE;
    uint32_t r[WORDS_PER_LANE];
#pragma unroll
    for (int j = 0; j < WORDS_PER_LANE; ++j) r[j] = stage[warp_id][base + j];

    // Work out, once, which recorded columns this lane holds. Across the
    // whole grid only one or two lanes own anything, so the per-step cost is
    // a single compare for everyone else.
    //
    // OWNERSHIP MUST BE UNIQUE ACROSS THE WHOLE GRID. Tiles overlap: tile_start
    // advances USEFUL_WORDS per tile while each tile covers WARP_WORDS, so
    // consecutive tiles share 2*HALO_WORDS words. A word in tile T's useful
    // region also sits in tile T-1's or T+1's halo. Testing only the lane's
    // register range (wl in [base, base+WORDS_PER_LANE)) lets BOTH lanes claim
    // it, and the recording store below is a non-atomic read-modify-write to
    // global memory issued from two different blocks -- so one update is lost
    // and the recorded column silently drops 1s. Measured at 5.05e-4 (block
    // edge) and 1.1e-5 (warp edge); see KERNEL-V6-DEFECT.md.
    //
    // The useful regions [T*USEFUL_WORDS, (T+1)*USEFUL_WORDS) partition the
    // global word space exactly, no gaps and no overlaps, so restricting the
    // claim to wl in [HALO_WORDS, HALO_WORDS+USEFUL_WORDS) leaves each cell
    // with exactly one claiming tile -- provided the host launches the block
    // containing it. It also guarantees the claimed word is uncontaminated
    // (see the halo-margin note above), which the halo copy is not.
    // Store the owned columns as a RANGE, not as arrays. The recorded cells are
    // consecutive (rec_lo_cell + k), so wl is non-decreasing in k and the
    // ownership predicate is an intersection of two intervals in wl; the set of
    // owned k is therefore contiguous, and slot/bit are recoverable from k by
    // arithmetic. Three MAX_REC arrays here cost 192 bytes of LOCAL memory per
    // thread -- they are indexed by a runtime m, so they cannot live in
    // registers -- and they dragged the hot `r` array down with them: measured
    // local_size_bytes was exactly 192 + 4*WORDS_PER_LANE, i.e. the arrays plus
    // the whole of r, on every thread in the grid, for a kernel where one or
    // two lanes in the grid record anything. That cost 4.03x.
    int rec_k_lo = MAX_REC, rec_k_hi = 0;        // half-open, empty if lo >= hi
    if (rec_out != nullptr) {
        for (int k = 0; k < n_rec && k < MAX_REC; ++k) {
            int64_t cell = rec_lo_cell + k;
            int64_t wl = (cell >> 5) - tile_start;   // word index within tile
            if (wl >= HALO_WORDS && wl < HALO_WORDS + USEFUL_WORDS &&
                wl >= base && wl < base + WORDS_PER_LANE) {
                if (k < rec_k_lo) rec_k_lo = k;
                rec_k_hi = k + 1;
            }
        }
    }

    const int steps = (steps_this_launch < STEPS_PER_BATCH)
                        ? steps_this_launch : STEPS_PER_BATCH;

    for (int step = 0; step < steps; ++step) {
        for (int k = rec_k_lo; k < rec_k_hi; ++k) {
            // slot and bit are recomputed from k rather than looked up. A few
            // integer ops on the one or two lanes in the grid that record
            // anything is far cheaper than a lookup table that puts `r` in
            // local memory for every thread in the grid.
            const int64_t cell = rec_lo_cell + k;
            const int slot = (int)((cell >> 5) - tile_start) - base;
            // Index r ONLY by the compile-time j. A dynamic index into r would
            // force the whole hot array out of registers, which is the other
            // half of the same 4x.
            uint32_t word = 0u;
#pragma unroll
            for (int j = 0; j < WORDS_PER_LANE; ++j) {
                if (j == slot) word = r[j];
            }
            if ((word >> (int)(cell & 31)) & 1u) {
                // The ownership test above already makes this the only writer
                // of this word in the grid, so a plain |= would be correct.
                // atomicOr costs ~nothing here (n_rec stores per step, on one
                // or two lanes of the whole grid) and removes the lost-update
                // failure mode from the code rather than from an argument.
                atomicOr(&rec_out[k * words_per_batch + (step >> 5)],
                         1u << (step & 31));
            }
        }
        // only the two boundary words cross lanes, one shuffle each
        uint32_t lo = __shfl_up_sync(FULL_MASK, r[WORDS_PER_LANE - 1], 1);
        uint32_t hi = __shfl_down_sync(FULL_MASK, r[0], 1);
        if (lane == 0)  lo = 0u;
        if (lane == 31) hi = 0u;

        uint32_t prev = lo;
#pragma unroll
        for (int j = 0; j < WORDS_PER_LANE; ++j) {
            uint32_t c  = r[j];
            uint32_t nx = (j < WORDS_PER_LANE - 1) ? r[j + 1] : hi;
            uint32_t l  = (c << 1) | (prev >> 31);
            uint32_t rr = (c >> 1) | (nx << 31);
            prev = c;
            r[j] = l ^ (c | rr);
        }
    }

    // stage out, then coalesced global store of the useful region only
    __syncwarp();
#pragma unroll
    for (int j = 0; j < WORDS_PER_LANE; ++j) stage[warp_id][base + j] = r[j];
    __syncwarp();
    for (int i = lane; i < USEFUL_WORDS; i += 32) {
        int64_t go = tile_start + HALO_WORDS + i;
        if (go >= 0 && go < (int64_t)n_words) {
            dst[go] = stage[warp_id][HALO_WORDS + i];
        }
    }
}
