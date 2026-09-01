/* gen30v2.c -- vectorization-friendly bit-packed Rule 30 center column.
 *
 * Same math and same convention as gen30.c:
 *   b_{t+1} = (b_t << 2) ^ ((b_t << 1) | b_t),  c(t) = bit t of b_t.
 * Difference: double-buffered ASCENDING pass with __restrict pointers, so the
 * loop has no loop-carried dependence the compiler must serialize and clang can
 * emit NEON. Word i of the new row depends on words i and i-1 of the old row.
 *
 * Build:  cc -O3 -march=native -o gen30v2 gen30v2.c
 * Usage:  ./gen30v2 <steps> <out.bin> [ckpt_every] [ckpt_path]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

static double now(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

static inline void step_rows(const uint64_t *__restrict src,
                             uint64_t *__restrict dst, uint64_t hi) {
    /* dst[0] has no lower neighbour word */
    uint64_t c0 = src[0];
    dst[0] = (c0 << 2) ^ ((c0 << 1) | c0);
    for (uint64_t i = 1; i <= hi; i++) {
        uint64_t cur = src[i], lo = src[i - 1];
        uint64_t s1 = (cur << 1) | (lo >> 63);
        uint64_t s2 = (cur << 2) | (lo >> 62);
        dst[i] = s2 ^ (s1 | cur);
    }
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "usage: %s <steps> <out.bin> [ckpt_every] [ckpt_path]\n", argv[0]);
        return 2;
    }
    uint64_t N = strtoull(argv[1], NULL, 10);
    const char *outpath = argv[2];
    uint64_t ckpt_every = (argc > 3) ? strtoull(argv[3], NULL, 10) : 0;
    const char *ckpt_path = (argc > 4) ? argv[4] : "gen30.ckpt";

    uint64_t nwords = (2 * N) / 64 + 8;
    uint64_t *a = calloc(nwords, sizeof(uint64_t));
    uint64_t *b = calloc(nwords, sizeof(uint64_t));
    if (!a || !b) { fprintf(stderr, "alloc failed (%llu words x2)\n",
                            (unsigned long long)nwords); return 1; }
    a[0] = 1;

    unsigned char *buf = calloc(1 << 20, 1);
    FILE *f = fopen(outpath, "wb");
    if (!f || !buf) { perror("open"); return 1; }
    uint64_t bufbits = 0, written = 0;
    double t0 = now(), tlast = t0;

    uint64_t *cur = a, *nxt = b;
    for (uint64_t t = 0; t < N; t++) {
        uint64_t bit = (cur[t >> 6] >> (t & 63)) & 1ULL;
        if (bit) buf[bufbits >> 3] |= (unsigned char)(1u << (bufbits & 7));
        bufbits++;
        if (bufbits == (1ULL << 23)) {
            fwrite(buf, 1, 1 << 20, f);
            memset(buf, 0, 1 << 20);
            written += 1 << 20;
            bufbits = 0;
        }

        uint64_t hi = (2 * (t + 1)) >> 6;
        if (hi >= nwords) hi = nwords - 1;
        step_rows(cur, nxt, hi);
        uint64_t *tmp = cur; cur = nxt; nxt = tmp;

        if (ckpt_every && t && t % ckpt_every == 0) {
            double tn = now();
            fprintf(stderr, "t=%llu elapsed=%.1fs avg=%.4e inst=%.4e steps/s\n",
                    (unsigned long long)t, tn - t0, t / (tn - t0),
                    ckpt_every / (tn - tlast));
            fflush(stderr);
            tlast = tn;
            FILE *cf = fopen(ckpt_path, "wb");
            if (cf) {
                uint64_t w = ((2 * (t + 1)) >> 6) + 2;
                fwrite(&t, sizeof t, 1, cf);
                fwrite(&w, sizeof w, 1, cf);
                fwrite(cur, sizeof(uint64_t), w, cf);
                fclose(cf);
            }
        }
    }
    if (bufbits) { uint64_t nb = (bufbits + 7) / 8; fwrite(buf, 1, nb, f); written += nb; }
    fclose(f);
    double el = now() - t0;
    fprintf(stderr, "done: N=%llu bytes=%llu elapsed=%.3fs rate=%.4e steps/s\n",
            (unsigned long long)N, (unsigned long long)written, el, N / el);
    return 0;
}
