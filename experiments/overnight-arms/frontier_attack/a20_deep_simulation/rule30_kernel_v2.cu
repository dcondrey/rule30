// Rule 30 kernel v2: 64-bit words + register blocking.
//
// v1 measured 4.09e13 cell-updates/s and was limited by shared-memory
// traffic, not arithmetic: each word-step cost 3 shared loads + 1 shared
// store (16 bytes) against only ~6 ALU ops. At 128 bytes/clock/SM of shared
// bandwidth that caps ~8 words/clock, while the ALUs could sustain ~21.
//
// v2 changes two things:
//   1. uint64_t words, so one word carries 64 cells instead of 32 for
//      essentially the same op count.
//   2. Register blocking: each thread owns WORDS_PER_THREAD *contiguous*
//      words held in registers across every step of the batch. Interior
//      neighbours are already in registers; only the two chunk-boundary
//      words are exchanged through shared memory each step. Shared traffic
//      per thread-step drops from 4*C accesses to 4 total.
//
// The in-place update uses a rolling `prev` so no second register array is
// needed: the old value of r[j] is saved into `prev` before r[j] is
// overwritten, which is exactly what the left-neighbour view of r[j+1]
// requires on the next iteration.

#include <stdint.h>

#ifndef THREADS_PER_BLOCK
#define THREADS_PER_BLOCK 256
#endif
#ifndef WORDS_PER_THREAD
#define WORDS_PER_THREAD 8
#endif
#ifndef STEPS_PER_TILE
#define STEPS_PER_TILE 256
#endif

#define TILE_WORDS (THREADS_PER_BLOCK * WORDS_PER_THREAD)
// halo must cover STEPS_PER_TILE cells on each side, in 64-cell words
#define HALO_WORDS ((STEPS_PER_TILE + 63) / 64)
#define USEFUL_WORDS (TILE_WORDS - 2 * HALO_WORDS)

extern "C" __global__ void rule30_v2(
    const uint64_t* __restrict__ src,
    uint64_t* __restrict__ dst,
    uint64_t n_words,
    int64_t centre_word,                // global word index of centre cell
    int centre_bit,                     // bit within that word
    uint32_t* __restrict__ centre_out,  // packed, one bit per step, or null
    int steps_this_launch)
{
    __shared__ uint64_t sL[THREADS_PER_BLOCK];  // each thread's first word
    __shared__ uint64_t sR[THREADS_PER_BLOCK];  // each thread's last word

    const int tid = threadIdx.x;
    const int64_t tile_start =
        (int64_t)blockIdx.x * USEFUL_WORDS - HALO_WORDS;
    const int64_t my_start = tile_start + (int64_t)tid * WORDS_PER_THREAD;

    uint64_t r[WORDS_PER_THREAD];
#pragma unroll
    for (int j = 0; j < WORDS_PER_THREAD; ++j) {
        int64_t gi = my_start + j;
        r[j] = (gi >= 0 && gi < (int64_t)n_words) ? src[gi] : 0ull;
    }

    // which thread/slot owns the centre cell this batch
    const int64_t c_local = centre_word - my_start;
    const bool owns_centre = (centre_out != nullptr) &&
                             (c_local >= 0) && (c_local < WORDS_PER_THREAD);
    const int c_slot = owns_centre ? (int)c_local : 0;

    for (int step = 0; step < steps_this_launch; ++step) {
        // emit the centre bit for the state on entry to this step, matching
        // the CPU reference which emits then advances
        if (owns_centre) {
            uint64_t bit = (r[c_slot] >> centre_bit) & 1ull;
            if (bit) centre_out[step >> 5] |= (1u << (step & 31));
        }

        sL[tid] = r[0];
        sR[tid] = r[WORDS_PER_THREAD - 1];
        __syncthreads();
        uint64_t left_of_first = (tid > 0) ? sR[tid - 1] : 0ull;
        uint64_t right_of_last =
            (tid < THREADS_PER_BLOCK - 1) ? sL[tid + 1] : 0ull;
        __syncthreads();  // all reads done before next iteration's writes

        uint64_t prev = left_of_first;
#pragma unroll
        for (int j = 0; j < WORDS_PER_THREAD; ++j) {
            uint64_t c  = r[j];
            uint64_t nx = (j < WORDS_PER_THREAD - 1) ? r[j + 1] : right_of_last;
            uint64_t l  = (c << 1) | (prev >> 63);
            uint64_t rr = (c >> 1) | (nx << 63);
            prev = c;                       // save old c for the next slot
            r[j] = l ^ (c | rr);
        }
    }

    // write back only the valid (non-halo) region
#pragma unroll
    for (int j = 0; j < WORDS_PER_THREAD; ++j) {
        int64_t local = (int64_t)tid * WORDS_PER_THREAD + j;
        if (local >= HALO_WORDS && local < TILE_WORDS - HALO_WORDS) {
            int64_t gi = tile_start + local;
            if (gi >= 0 && gi < (int64_t)n_words) dst[gi] = r[j];
        }
    }
}
