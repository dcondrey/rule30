// Rule 30 kernel v3: per-thread trapezoidal tiling, zero syncs inside a batch.
//
// Measured history on H100:
//   v1 (uint32, shared-memory stencil, 1 sync/step) 4.09e13 cell-updates/s
//   v2 (uint64, register blocking, 2 syncs/step)    2.84e13  <- REGRESSION
//
// v2 regressed because exchanging chunk boundaries every step needs two
// __syncthreads() per step (write, sync, read, sync), and at 256 steps per
// batch that sync traffic cost more than the shared-memory traffic it saved.
//
// v3 removes per-step communication altogether. Each thread loads its C
// useful words PLUS H halo words on each side. One Rule 30 step shrinks the
// valid region by exactly one cell per side, so a thread holding H words
// (64H cells) of halo can advance 64H steps with no neighbour information at
// all. We therefore run STEPS = 64*H steps in registers with zero syncs, at
// the cost of recomputing the halo (2H/C redundant work).
//
// Global memory is still touched coalesced: the tile is staged through
// shared memory once per batch (one sync in, one sync out), then each thread
// pulls its own slice, including halo, out of shared into registers.

#include <stdint.h>

#ifndef THREADS_PER_BLOCK
#define THREADS_PER_BLOCK 256
#endif
#ifndef WORDS_PER_THREAD          // C: useful 64-bit words per thread
#define WORDS_PER_THREAD 8
#endif
#ifndef HALO_W                    // H: halo words each side -> 64*H steps
#define HALO_W 1
#endif

#define STEPS_PER_BATCH (64 * HALO_W)
#define USEFUL_WORDS (THREADS_PER_BLOCK * WORDS_PER_THREAD)
#define TILE_WORDS (USEFUL_WORDS + 2 * HALO_W)
#define REG_WORDS (WORDS_PER_THREAD + 2 * HALO_W)

extern "C" __global__ void rule30_v3(
    const uint64_t* __restrict__ src,
    uint64_t* __restrict__ dst,
    uint64_t n_words,
    int64_t centre_word,
    int centre_bit,
    uint32_t* __restrict__ centre_out,
    int steps_this_launch)          // must be <= STEPS_PER_BATCH
{
    __shared__ uint64_t tile[TILE_WORDS];

    const int tid = threadIdx.x;
    const int64_t tile_start = (int64_t)blockIdx.x * USEFUL_WORDS - HALO_W;

    // coalesced stage-in of the whole tile (useful + both halos)
    for (int i = tid; i < TILE_WORDS; i += THREADS_PER_BLOCK) {
        int64_t gi = tile_start + i;
        tile[i] = (gi >= 0 && gi < (int64_t)n_words) ? src[gi] : 0ull;
    }
    __syncthreads();

    // each thread pulls its own slice, including its private halo
    const int base = tid * WORDS_PER_THREAD;   // index into tile of my first useful word
    uint64_t r[REG_WORDS];
#pragma unroll
    for (int j = 0; j < REG_WORDS; ++j) {
        int idx = base + j;                    // base-HALO_W+j shifted: see below
        r[j] = (idx < TILE_WORDS) ? tile[idx] : 0ull;
    }
    __syncthreads();   // everyone done reading before anyone could overwrite

    // Which register slot holds the centre cell, if any. My useful words are
    // r[HALO_W .. HALO_W+C), mapping to tile[base .. base+C), i.e. global
    // words tile_start+base .. +C.
    const int64_t my_first_useful_global = tile_start + base + HALO_W;
    const int64_t c_local = centre_word - my_first_useful_global;
    const bool owns_centre = (centre_out != nullptr) &&
                             (c_local >= 0) && (c_local < WORDS_PER_THREAD);
    const int c_slot = owns_centre ? (int)(c_local + HALO_W) : 0;

    const int steps = (steps_this_launch < STEPS_PER_BATCH)
                        ? steps_this_launch : STEPS_PER_BATCH;

    for (int step = 0; step < steps; ++step) {
        if (owns_centre) {
            uint64_t bit = (r[c_slot] >> centre_bit) & 1ull;
            if (bit) centre_out[step >> 5] |= (1u << (step & 31));
        }
        // one step, entirely in registers, no communication
        uint64_t prev = 0ull;      // left of r[0]: unknown, so r[0] decays
#pragma unroll
        for (int j = 0; j < REG_WORDS; ++j) {
            uint64_t c  = r[j];
            uint64_t nx = (j < REG_WORDS - 1) ? r[j + 1] : 0ull;
            uint64_t l  = (c << 1) | (prev >> 63);
            uint64_t rr = (c >> 1) | (nx << 63);
            prev = c;
            r[j] = l ^ (c | rr);
        }
    }

    // stage out only the useful words, coalesced through shared
    __syncthreads();
#pragma unroll
    for (int j = 0; j < WORDS_PER_THREAD; ++j) {
        tile[HALO_W + base + j] = r[HALO_W + j];
    }
    __syncthreads();
    for (int i = tid; i < USEFUL_WORDS; i += THREADS_PER_BLOCK) {
        int64_t gi = tile_start + HALO_W + i;
        if (gi >= 0 && gi < (int64_t)n_words) dst[gi] = tile[HALO_W + i];
    }
}
