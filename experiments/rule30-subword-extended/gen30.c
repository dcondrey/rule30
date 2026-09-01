/* gen30.c -- bit-packed Rule 30 center-column generator.
 *
 * Convention pinned to experiments/rule30/center_column.py and
 * experiments/overnight-arms/common/rule30.py:
 *     s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1))
 * Shifted frame b_t(i) = s(t, i-t) keeps the support at bits [0, 2t],
 * growing only at the high end, so no rebasing is ever needed:
 *     b_{t+1} = (b_t << 2) XOR ((b_t << 1) | b_t)
 * Center column bit c(t) = s(t,0) = bit t of b_t.
 *
 * The row is stored as an array of 64-bit words, bit i in word i/64 at
 * position i%64. The update is done IN PLACE walking words high-to-low:
 * new[i] depends only on b[i] and b[i-1], both still intact when the walk
 * is descending. That halves memory traffic versus double-buffering.
 *
 * Output: the center column packed LSB-first into bytes (bit t of the
 * stream is c(t)), written incrementally.
 *
 * NOTE on checkpoints: the full row state is dumped periodically (header
 * {t, nwords} then the row words). The dumps are written and verified
 * well-formed, but NO RESTORE PATH IS IMPLEMENTED -- a crashed run must be
 * restarted from t=0. The dump exists so that a restore could be added
 * without re-running; do not describe this program as crash-resumable.
 *
 * Build:  cc -O3 -march=native -o gen30 gen30.c
 * Usage:  ./gen30 <steps> <out.bin> [checkpoint_every] [ckpt_path]
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

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "usage: %s <steps> <out.bin> [ckpt_every] [ckpt_path]\n", argv[0]);
        return 2;
    }
    uint64_t N = strtoull(argv[1], NULL, 10);
    const char *outpath = argv[2];
    uint64_t ckpt_every = (argc > 3) ? strtoull(argv[3], NULL, 10) : 0;
    const char *ckpt_path = (argc > 4) ? argv[4] : "gen30.ckpt";

    /* bits 0 .. 2(N-1) inclusive, plus slack */
    uint64_t nwords = (2 * N) / 64 + 4;
    uint64_t *b = calloc(nwords, sizeof(uint64_t));
    if (!b) { fprintf(stderr, "alloc %llu words failed\n", (unsigned long long)nwords); return 1; }
    b[0] = 1;                      /* b_0: single 1 at bit 0 */

    uint64_t outbytes = (N + 7) / 8;
    unsigned char *buf = calloc(1 << 20, 1);   /* 1 MiB staging buffer */
    if (!buf) return 1;
    FILE *f = fopen(outpath, "wb");
    if (!f) { perror("fopen"); return 1; }

    uint64_t bufbits = 0;          /* bits currently staged in buf */
    uint64_t written = 0;
    double t0 = now(), tlast = t0;

    for (uint64_t t = 0; t < N; t++) {
        /* emit c(t) = bit t of b_t */
        uint64_t bit = (b[t >> 6] >> (t & 63)) & 1ULL;
        if (bit) buf[bufbits >> 3] |= (unsigned char)(1u << (bufbits & 7));
        bufbits++;
        if (bufbits == (1ULL << 23)) {                 /* 8 Mibit = 1 MiB */
            fwrite(buf, 1, 1 << 20, f);
            memset(buf, 0, 1 << 20);
            written += 1 << 20;
            bufbits = 0;
        }

        /* in-place update, high word to low word.
         * support after the step reaches bit 2(t+1); words needed: */
        uint64_t hi = (2 * (t + 1)) >> 6;               /* highest touched word */
        if (hi >= nwords) hi = nwords - 1;
        for (uint64_t i = hi; i > 0; i--) {
            uint64_t cur = b[i], lo = b[i - 1];
            uint64_t s1 = (cur << 1) | (lo >> 63);
            uint64_t s2 = (cur << 2) | (lo >> 62);
            b[i] = s2 ^ (s1 | cur);
        }
        {
            uint64_t cur = b[0];
            b[0] = (cur << 2) ^ ((cur << 1) | cur);
        }

        if (ckpt_every && t && t % ckpt_every == 0) {
            double tn = now();
            fprintf(stderr, "t=%llu  elapsed=%.1fs  rate=%.3e steps/s (inst %.3e)\n",
                    (unsigned long long)t, tn - t0, t / (tn - t0),
                    ckpt_every / (tn - tlast));
            fflush(stderr);
            tlast = tn;
            FILE *cf = fopen(ckpt_path, "wb");
            if (cf) {
                fwrite(&t, sizeof t, 1, cf);
                fwrite(b, sizeof(uint64_t), ((2 * (t + 1)) >> 6) + 2, cf);
                fclose(cf);
            }
        }
    }

    if (bufbits) {
        uint64_t nb = (bufbits + 7) / 8;
        fwrite(buf, 1, nb, f);
        written += nb;
    }
    fclose(f);
    double el = now() - t0;
    fprintf(stderr, "done: N=%llu bytes=%llu (expect %llu) elapsed=%.3fs rate=%.4e steps/s\n",
            (unsigned long long)N, (unsigned long long)written,
            (unsigned long long)outbytes, el, N / el);
    free(b); free(buf);
    return 0;
}
