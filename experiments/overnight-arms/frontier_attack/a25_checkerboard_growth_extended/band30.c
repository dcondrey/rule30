/* band30.c -- fast bit-packed generator for the centre band of the lone-seed
 * Rule 30 spacetime diagram.  Semantics identical to a3's `_band_series` in
 * a3_p2_orbit_closure/band_census.py (internal frame b_t(i) = s(t, i - t),
 * b_{t+1} = (b<<2) ^ ((b<<1) | b)); the only change is a single fused pass
 * over the live prefix instead of numpy's six separate array passes.
 *
 * Bit-exactness against the numpy kernel is enforced by verify_kernel.py.
 *
 * out[t] = uint32 with bit (x + WMAX) = s(t, x), x in [-WMAX, WMAX].
 *
 * build: cc -O3 -march=native -o band30 band30.c
 * run:   ./band30 STEPS OUT.bin
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#if defined(__ARM_NEON)
#include <arm_neon.h>
#endif

#define WMAX 15

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: band30 STEPS OUT.bin\n"); return 2; }
    long long steps = atoll(argv[1]);
    const char *outpath = argv[2];

    long long words = (2 * steps + 2 * WMAX + 128) / 64 + 4;
    uint64_t *row = calloc((size_t)words, 8);
    uint32_t *out = malloc((size_t)steps * 4);
    if (!row || !out) { fprintf(stderr, "alloc failed\n"); return 1; }
    row[0] = 1ULL;
    const uint32_t mask = (1u << (2 * WMAX + 1)) - 1u;

    struct timespec ta, tb;
    clock_gettime(CLOCK_MONOTONIC, &ta);

    long long live = 1;
    long long ckpt = (argc > 3) ? atoll(argv[3]) : 0; /* dump every ckpt steps */
    for (long long t = 0; t < steps; t++) {
        if (ckpt && t > 0 && t % ckpt == 0) {
            char p[1024];
            snprintf(p, sizeof p, "%s.ck%lld", outpath, t);
            FILE *cf = fopen(p, "wb");
            if (cf) { fwrite(out, 4, (size_t)t, cf); fclose(cf); }
            clock_gettime(CLOCK_MONOTONIC, &tb);
            fprintf(stderr, "checkpoint t=%lld seconds=%.1f\n", t,
                    (tb.tv_sec - ta.tv_sec) + 1e-9 * (tb.tv_nsec - ta.tv_nsec));
            fflush(stderr);
        }
        /* --- extract columns [-WMAX, WMAX] at time t --- */
        long long i = t - WMAX;
        if (i >= 0) {
            long long w = i / 64, b = i % 64;
            uint64_t v = row[w] >> b;
            if (b) v |= row[w + 1] << (64 - b);
            out[t] = (uint32_t)v & mask;
        } else {
            /* t < WMAX: window hangs off the left end of the array */
            unsigned sh = (unsigned)(-i);
            uint64_t v = row[0];
            out[t] = (uint32_t)(v << sh) & mask;
        }

        /* --- one Rule 30 step over the live prefix, single fused pass --- */
        long long nl = (2 * t + 2 * WMAX + 128) / 64 + 2;
        live = nl < words ? nl : words;
        long long w = 0;
        uint64_t prev = 0; /* pre-update value of row[w-1] */
#if defined(__ARM_NEON) && !defined(BAND30_SCALAR)
        /* Two words per iteration.  prevv holds {row[w-1], row[w]} (pre-update)
         * built with vextq_u64 from the previous pair, so the cross-word carry
         * is exact and the semantics match the scalar path bit for bit. */
        {
            uint64x2_t prevpair = vdupq_n_u64(0); /* {row[-2], row[-1]} = 0 */
            long long vend = live & ~1LL;
            for (; w < vend; w += 2) {
                uint64x2_t cur = vld1q_u64((const uint64_t *)&row[w]);
                uint64x2_t prevv = vextq_u64(prevpair, cur, 1);
                uint64x2_t a1 = vorrq_u64(vshlq_n_u64(cur, 1), vshrq_n_u64(prevv, 63));
                uint64x2_t a2 = vorrq_u64(vshlq_n_u64(cur, 2), vshrq_n_u64(prevv, 62));
                vst1q_u64((uint64_t *)&row[w], veorq_u64(a2, vorrq_u64(a1, cur)));
                prevpair = cur;
            }
            if (w > 0) prev = vgetq_lane_u64(prevpair, 1); /* pre-update row[w-1] */
        }
#endif
        for (; w < live; w++) {
            uint64_t cur = row[w];
            uint64_t a1 = (cur << 1) | (prev >> 63);
            uint64_t a2 = (cur << 2) | (prev >> 62);
            row[w] = a2 ^ (a1 | cur);
            prev = cur;
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &tb);
    double dt = (tb.tv_sec - ta.tv_sec) + 1e-9 * (tb.tv_nsec - ta.tv_nsec);
    fprintf(stderr, "band30 steps=%lld wmax=%d seconds=%.1f\n", steps, WMAX, dt);

    FILE *f = fopen(outpath, "wb");
    if (!f) { perror("fopen"); return 1; }
    if (fwrite(out, 4, (size_t)steps, f) != (size_t)steps) { perror("fwrite"); return 1; }
    fclose(f);
    return 0;
}
