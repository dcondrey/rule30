// Rule 30 kernel v4: ping-pong shared tile, contiguous per-thread chunks,
// ONE __syncthreads() per step.
//
// Measured on H100 (cell-updates/s):
//   v1  uint32, shared stencil, strided, 1 sync/step, 256 steps/batch  4.09e13
//   v2  uint64, register chunks, 2 syncs/step                          2.84e13
//   v3  uint64, private halo, 0 syncs/step but 64 steps/batch          2.53e13
//
// Diagnosis from the v1 numbers: 4 shared accesses per word-step (3 loads +
// 1 store) x 4 bytes = 16 B, giving 2.05e13 B/s against the H100's ~2.97e13
// B/s of shared bandwidth. That is 69% of peak, so v1 is shared-bandwidth
// bound, not ALU bound and not sync bound. v2 attacked syncs (wrong term,
// and added one) and v3 attacked syncs harder while cutting the batch from
// 256 steps to 64 (wrong term, and quadrupled global round trips).
//
// The right term is accesses per word. With STRIDED assignment each thread
// touches isolated words, so every word costs 3 loads. With CONTIGUOUS
// chunks of C words per thread, a chunk costs C+2 loads and C stores, i.e.
// 2 + 2/C accesses per word instead of 4. At C=8 that is 2.25, a 1.78x cut
// in shared traffic, while keeping exactly one sync per step by ping-ponging
// two shared buffers.
//
// Words are uint32 here on purpose: we are bandwidth bound per CELL, and
// uint64 does not change bytes-per-cell, it only reduces ALU work we are not
// limited by. The uint64 variant is selectable via WORD_BITS for the sweep.

#include <stdint.h>

#ifndef THREADS_PER_BLOCK
#define THREADS_PER_BLOCK 256
#endif
#ifndef WORDS_PER_THREAD           // C: contiguous words owned per thread
#define WORDS_PER_THREAD 8
#endif
#ifndef STEPS_PER_TILE
#define STEPS_PER_TILE 256
#endif

#define TILE_WORDS (THREADS_PER_BLOCK * WORDS_PER_THREAD)
#define HALO_WORDS ((STEPS_PER_TILE + 31) / 32)
#define USEFUL_WORDS (TILE_WORDS - 2 * HALO_WORDS)

extern "C" __global__ void rule30_v4(
    const uint32_t* __restrict__ src,
    uint32_t* __restrict__ dst,
    uint64_t n_words,
    int64_t centre_word,
    int centre_bit,
    uint32_t* __restrict__ centre_out,
    int steps_this_launch)
{
    __shared__ uint32_t buf[2][TILE_WORDS];

    const int tid = threadIdx.x;
    const int base = tid * WORDS_PER_THREAD;          // my chunk start in tile
    const int64_t tile_start = (int64_t)blockIdx.x * USEFUL_WORDS - HALO_WORDS;

    // coalesced stage-in
    for (int i = tid; i < TILE_WORDS; i += THREADS_PER_BLOCK) {
        int64_t gi = tile_start + i;
        buf[0][i] = (gi >= 0 && gi < (int64_t)n_words) ? src[gi] : 0u;
    }
    __syncthreads();

    const int64_t c_local = centre_word - tile_start;
    const bool owns_centre = (centre_out != nullptr) &&
                             (c_local >= base) &&
                             (c_local <  base + WORDS_PER_THREAD);
    const int c_slot = owns_centre ? (int)c_local : 0;

    int cur = 0;
    for (int step = 0; step < steps_this_launch; ++step) {
        if (owns_centre) {
            uint32_t bit = (buf[cur][c_slot] >> centre_bit) & 1u;
            if (bit) centre_out[step >> 5] |= (1u << (step & 31));
        }
        const int nxt = cur ^ 1;

        // Load my chunk plus one word of overlap on each side: C+2 loads for
        // C words, instead of 3C under strided assignment.
        uint32_t prev = (base > 0) ? buf[cur][base - 1] : 0u;
        uint32_t c    = buf[cur][base];
#pragma unroll
        for (int j = 0; j < WORDS_PER_THREAD; ++j) {
            int idx = base + j;
            uint32_t nx = (idx + 1 < TILE_WORDS) ? buf[cur][idx + 1] : 0u;
            uint32_t l  = (c << 1) | (prev >> 31);
            uint32_t r  = (c >> 1) | (nx << 31);
            buf[nxt][idx] = l ^ (c | r);
            prev = c;
            c = nx;
        }
        __syncthreads();
        cur = nxt;
    }

    for (int i = tid; i < USEFUL_WORDS; i += THREADS_PER_BLOCK) {
        int64_t gi = tile_start + HALO_WORDS + i;
        if (gi >= 0 && gi < (int64_t)n_words) {
            dst[gi] = buf[cur][HALO_WORDS + i];
        }
    }
}
