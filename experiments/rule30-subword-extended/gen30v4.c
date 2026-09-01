/* gen30v4.c -- NEON bit-packed Rule 30 center column, in-place descending.
 *
 * Same math and convention as gen30.c / gen30v2.c:
 *   b_{t+1} = (b_t << 2) ^ ((b_t << 1) | b_t),  c(t) = bit t of b_t.
 *
 * Two 64-bit words per NEON lane pair. The block writing words {i, i+1} reads
 * src words {i-1, i, i+1}; descending by 2 keeps every read ahead of the
 * writes, so the update stays in place (half the traffic of double-buffering,
 * which measured slower -- see gen30v2.c).
 *
 * The inner loop is unrolled 4x (8 words per iteration). That unroll, not the
 * NEON width, is where the 1.17x over scalar comes from; see benchmarks.json.
 *
 * Checkpoints: the row state is dumped every ckpt_every steps as
 * {t, nwords, row words}. Dumps are written and verified well-formed, but
 * there is NO RESTORE PATH -- a crashed or stopped run restarts from t=0.
 * Do not describe this program as crash-resumable.
 *
 * Build:  cc -O3 -o gen30v4 gen30v4.c
 * Usage:  ./gen30v4 <steps> <out.bin> [ckpt_every] [ckpt_path]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <arm_neon.h>

static double now(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

static inline void step_inplace(uint64_t *b, uint64_t hi) {
    uint64_t i = hi;
    /* unrolled x4: four independent NEON blocks per iteration (8 words) */
    for (; i >= 8; i -= 8) {
        uint64x2_t v0 = vld1q_u64(&b[i-1]), l0 = vld1q_u64(&b[i-2]);
        uint64x2_t v1 = vld1q_u64(&b[i-3]), l1 = vld1q_u64(&b[i-4]);
        uint64x2_t v2 = vld1q_u64(&b[i-5]), l2 = vld1q_u64(&b[i-6]);
        uint64x2_t v3 = vld1q_u64(&b[i-7]), l3 = vld1q_u64(&b[i-8]);
        uint64x2_t a0 = vorrq_u64(vshlq_n_u64(v0,1), vshrq_n_u64(l0,63));
        uint64x2_t a1 = vorrq_u64(vshlq_n_u64(v1,1), vshrq_n_u64(l1,63));
        uint64x2_t a2 = vorrq_u64(vshlq_n_u64(v2,1), vshrq_n_u64(l2,63));
        uint64x2_t a3 = vorrq_u64(vshlq_n_u64(v3,1), vshrq_n_u64(l3,63));
        uint64x2_t c0 = vorrq_u64(vshlq_n_u64(v0,2), vshrq_n_u64(l0,62));
        uint64x2_t c1 = vorrq_u64(vshlq_n_u64(v1,2), vshrq_n_u64(l1,62));
        uint64x2_t c2 = vorrq_u64(vshlq_n_u64(v2,2), vshrq_n_u64(l2,62));
        uint64x2_t c3 = vorrq_u64(vshlq_n_u64(v3,2), vshrq_n_u64(l3,62));
        vst1q_u64(&b[i-1], veorq_u64(c0, vorrq_u64(a0,v0)));
        vst1q_u64(&b[i-3], veorq_u64(c1, vorrq_u64(a1,v1)));
        vst1q_u64(&b[i-5], veorq_u64(c2, vorrq_u64(a2,v2)));
        vst1q_u64(&b[i-7], veorq_u64(c3, vorrq_u64(a3,v3)));
    }
    for (; i >= 2; i -= 2) {
        uint64x2_t v = vld1q_u64(&b[i-1]), vlo = vld1q_u64(&b[i-2]);
        uint64x2_t s1 = vorrq_u64(vshlq_n_u64(v,1), vshrq_n_u64(vlo,63));
        uint64x2_t s2 = vorrq_u64(vshlq_n_u64(v,2), vshrq_n_u64(vlo,62));
        vst1q_u64(&b[i-1], veorq_u64(s2, vorrq_u64(s1,v)));
    }
    for (; i >= 1; i--) {
        uint64_t cur = b[i], lo = b[i-1];
        b[i] = ((cur<<2)|(lo>>62)) ^ (((cur<<1)|(lo>>63))|cur);
    }
    uint64_t z = b[0];
    b[0] = (z<<2) ^ ((z<<1)|z);
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
    uint64_t *b = calloc(nwords, sizeof(uint64_t));
    if (!b) { fprintf(stderr, "alloc %llu words failed\n", (unsigned long long)nwords); return 1; }
    b[0] = 1;

    unsigned char *buf = calloc(1 << 20, 1);
    FILE *f = fopen(outpath, "wb");
    if (!f || !buf) { perror("open"); return 1; }
    uint64_t bufbits = 0, written = 0;
    double t0 = now(), tlast = t0;

    for (uint64_t t = 0; t < N; t++) {
        uint64_t bit = (b[t >> 6] >> (t & 63)) & 1ULL;
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
        step_inplace(b, hi);

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
                fwrite(b, sizeof(uint64_t), w, cf);
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
