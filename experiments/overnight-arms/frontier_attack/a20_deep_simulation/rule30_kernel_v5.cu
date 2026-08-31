// Rule 30 kernel v5: warp-shuffle stencil. No shared memory, no syncs.
//
// Measured on H100 (cell-updates/s), all gated on OEIS A051023:
//   v1  uint32 shared stencil, STRIDED, 1 sync/step          4.09e13  <- champ
//   v2  uint64 register chunks, 2 syncs/step                 2.84e13
//   v3  uint64 private halo, 0 syncs, 64 steps/batch         2.53e13
//   v4  uint32 ping-pong shared, CONTIGUOUS chunks           2.84e13 (C=4)
//
// v4's sweep was the diagnostic that mattered: throughput halved every time
// the chunk width C doubled (C=4 2.81e13, C=8 1.51e13, C=16 7.82e12,
// C=32 2.65e12). That is a C-way shared-memory bank conflict, because lane
// tid touching word tid*C+j collides on (tid*C+j) mod 32. v1 wins precisely
// because its STRIDED assignment is bank-conflict free, and that outweighs
// the accesses-per-word saving contiguous chunks were meant to buy.
//
// The way out is to stop using shared memory for the stencil at all. One
// warp owns 32 consecutive words in registers, one word per lane, and reads
// its neighbours with __shfl_up_sync / __shfl_down_sync, which run at
// register-file speed with no bank conflicts and no __syncthreads(). Lanes
// 0 and 31 have no in-warp neighbour, so their words decay; that is exactly
// the private-halo trick from v3, and HALO_LANES words of decay buy
// 32*HALO_LANES steps before the useful region is touched.
//
// Per warp per batch: read 32 words, write (32 - 2*HALO_LANES), run
// 32*HALO_LANES steps, with zero shared traffic and zero synchronisation.

#include <stdint.h>

#ifndef HALO_LANES                 // words of decay allowed at each end
#define HALO_LANES 2
#endif
#ifndef WARPS_PER_BLOCK
#define WARPS_PER_BLOCK 8
#endif

#define STEPS_PER_BATCH (32 * HALO_LANES)
#define USEFUL_LANES (32 - 2 * HALO_LANES)
#define FULL_MASK 0xffffffffu

extern "C" __global__ void rule30_v5(
    const uint32_t* __restrict__ src,
    uint32_t* __restrict__ dst,
    uint64_t n_words,
    int64_t centre_word,
    int centre_bit,
    uint32_t* __restrict__ centre_out,
    int steps_this_launch)          // must be <= STEPS_PER_BATCH
{
    const int lane    = threadIdx.x & 31;
    const int warp_id = threadIdx.x >> 5;
    const int64_t tile_idx =
        (int64_t)blockIdx.x * WARPS_PER_BLOCK + warp_id;
    const int64_t tile_start = tile_idx * USEFUL_LANES - HALO_LANES;
    const int64_t gi = tile_start + lane;

    uint32_t w = (gi >= 0 && gi < (int64_t)n_words) ? src[gi] : 0u;

    const bool owns_centre = (centre_out != nullptr) && (gi == centre_word);
    const int steps = (steps_this_launch < STEPS_PER_BATCH)
                        ? steps_this_launch : STEPS_PER_BATCH;

    for (int step = 0; step < steps; ++step) {
        if (owns_centre) {
            uint32_t bit = (w >> centre_bit) & 1u;
            if (bit) centre_out[step >> 5] |= (1u << (step & 31));
        }
        // neighbours from adjacent lanes, register speed, no bank conflicts
        uint32_t lo = __shfl_up_sync(FULL_MASK, w, 1);    // word of lane-1
        uint32_t hi = __shfl_down_sync(FULL_MASK, w, 1);  // word of lane+1
        if (lane == 0)  lo = 0u;   // outside the warp: decays, it is halo
        if (lane == 31) hi = 0u;

        uint32_t l = (w << 1) | (lo >> 31);
        uint32_t r = (w >> 1) | (hi << 31);
        w = l ^ (w | r);
    }

    if (lane >= HALO_LANES && lane < 32 - HALO_LANES) {
        int64_t go = tile_start + lane;
        if (go >= 0 && go < (int64_t)n_words) dst[go] = w;
    }
}
