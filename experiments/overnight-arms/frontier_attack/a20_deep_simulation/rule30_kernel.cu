// Rule 30 centre-column kernel, bit-packed with temporal blocking.
//
// Representation: the row is an array of uint32_t words, bit i of word w
// holds the cell at spatial position 32*w + i, LSB-first. One Rule 30 step
// is  new = l ^ (c | r)  where l is the cell to the LEFT (position-1) and r
// the cell to the RIGHT (position+1).
//
// In LSB-first packing the left neighbour of bit i is bit i-1, so the
// left-neighbour view of a word is (c << 1) with a carry-in of the previous
// word's MSB; the right neighbour is bit i+1, so (c >> 1) with a carry-in of
// the next word's LSB.
//
// Temporal blocking: each block loads WORDS_PER_TILE words plus HALO_WORDS of
// halo on each side into shared memory, then advances STEPS_PER_TILE steps
// entirely in shared memory, ping-ponging between two shared buffers. Each
// step shrinks the valid region by one cell per side, so the halo must cover
// STEPS_PER_TILE cells; HALO_WORDS = ceil(STEPS_PER_TILE/32) guarantees the
// written-back region is still valid after the last step. This is what turns
// a bandwidth-bound problem into a compute-bound one.
//
// Centre-column extraction: only the block owning the centre cell writes, and
// only its thread 0, so no atomics are needed.

#include <stdint.h>

#ifndef WORDS_PER_TILE
#define WORDS_PER_TILE 1024     // 1024 words = 32768 cells of useful output
#endif
#ifndef STEPS_PER_TILE
#define STEPS_PER_TILE 256      // k: steps per global memory round trip
#endif

#define HALO_WORDS ((STEPS_PER_TILE + 31) / 32)
#define TILE_TOTAL (WORDS_PER_TILE + 2 * HALO_WORDS)

extern "C" __global__ void rule30_block_step(
    const uint32_t* __restrict__ src,
    uint32_t* __restrict__ dst,
    uint64_t n_words,
    int64_t centre_word,
    int centre_bit,
    uint32_t* __restrict__ centre_out, // packed bits, one per step, or null
    int steps_this_launch)
{
    __shared__ uint32_t buf[2][TILE_TOTAL];

    const int64_t tile_start = (int64_t)blockIdx.x * WORDS_PER_TILE - HALO_WORDS;

    for (int i = threadIdx.x; i < TILE_TOTAL; i += blockDim.x) {
        int64_t gi = tile_start + i;
        buf[0][i] = (gi >= 0 && gi < (int64_t)n_words) ? src[gi] : 0u;
    }
    __syncthreads();

    const int64_t centre_local = centre_word - tile_start;
    const bool owns_centre = (centre_out != nullptr) &&
                             (centre_local >= 0) &&
                             (centre_local <  TILE_TOTAL);

    int cur = 0;
    for (int step = 0; step < steps_this_launch; ++step) {
        // Emit the centre bit for this step BEFORE advancing, so the batch's
        // step 0 is the state on entry. This matches the CPU reference, which
        // emits then steps.
        if (owns_centre && threadIdx.x == 0) {
            uint32_t bit = (buf[cur][centre_local] >> centre_bit) & 1u;
            if (bit) centre_out[step >> 5] |= (1u << (step & 31));
        }

        const int nxt = cur ^ 1;
        for (int i = threadIdx.x; i < TILE_TOTAL; i += blockDim.x) {
            uint32_t c  = buf[cur][i];
            uint32_t lo = (i > 0)              ? buf[cur][i - 1] : 0u;
            uint32_t hi = (i < TILE_TOTAL - 1) ? buf[cur][i + 1] : 0u;
            uint32_t l = (c << 1) | (lo >> 31);
            uint32_t r = (c >> 1) | (hi << 31);
            buf[nxt][i] = l ^ (c | r);
        }
        __syncthreads();
        cur = nxt;
    }

    for (int i = threadIdx.x; i < WORDS_PER_TILE; i += blockDim.x) {
        int64_t gi = tile_start + HALO_WORDS + i;
        if (gi >= 0 && gi < (int64_t)n_words) {
            dst[gi] = buf[cur][HALO_WORDS + i];
        }
    }
}

// One-step-per-launch kernel: the bandwidth-bound baseline that the
// temporal-blocking multiplier is measured against.
extern "C" __global__ void rule30_naive_step(
    const uint32_t* __restrict__ src,
    uint32_t* __restrict__ dst,
    uint64_t n_words)
{
    uint64_t i = (uint64_t)blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n_words) return;
    uint32_t c  = src[i];
    uint32_t lo = (i > 0)           ? src[i - 1] : 0u;
    uint32_t hi = (i + 1 < n_words) ? src[i + 1] : 0u;
    uint32_t l = (c << 1) | (lo >> 31);
    uint32_t r = (c >> 1) | (hi << 31);
    dst[i] = l ^ (c | r);
}
