/* analyze.c -- exact factor complexity p(n), n = 1..64, of a packed bitstream,
 * plus the longest repeated factor L.
 *
 * Method. For each start position i in [0, N-64] take the 64-bit window
 * w[i] = bits i..i+63 packed MSB-first, so that the length-n factor at i is
 * exactly the top n bits of w[i]. LSD-radix-sort the w[] array once; then for
 * every n <= 64 simultaneously, p(n) is the number of adjacent-distinct groups
 * under the top-n-bit key, because sorting by the full 64-bit value puts equal
 * n-bit prefixes in contiguous runs. One O(N) sort answers all 64 values of n.
 *
 * The <=63 tail positions i in (N-64, N-n] have a valid length-n factor but no
 * full 64-bit window; they are folded back in exactly by binary-searching each
 * against the sorted array (and de-duplicating among themselves), so the
 * reported p(n) is the exact factor count of the N-bit prefix, matching the
 * N-n+1 window convention of the earlier row-76 measurement.
 *
 * What the numbers mean. If the word is eventually periodic with preperiod r
 * and period q then p(n) <= r+q for EVERY n. So a single measured p(n) = V
 * forces r+q >= V. The exclusion bound reported is max_n p(n).
 *
 * Build: cc -O3 -o analyze analyze.c
 * Usage: ./analyze <bitstream.bin> [max_bits]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

static double now(void) {
    struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

static inline int getbit(const unsigned char *d, uint64_t i) {
    return (d[i >> 3] >> (i & 7)) & 1;
}

/* LSD radix sort, 8 passes of 8 bits. */
static void radix_sort(uint64_t *a, uint64_t *tmp, uint64_t n) {
    uint64_t *src = a, *dst = tmp;
    for (int pass = 0; pass < 8; pass++) {
        uint64_t cnt[256] = {0};
        int sh = pass * 8;
        for (uint64_t i = 0; i < n; i++) cnt[(src[i] >> sh) & 0xFF]++;
        uint64_t s = 0;
        for (int k = 0; k < 256; k++) { uint64_t c = cnt[k]; cnt[k] = s; s += c; }
        for (uint64_t i = 0; i < n; i++) dst[cnt[(src[i] >> sh) & 0xFF]++] = src[i];
        uint64_t *t = src; src = dst; dst = t;
    }
    if (src != a) memcpy(a, src, n * sizeof(uint64_t));   /* 8 passes -> even, but be safe */
}

/* does key (top n bits) occur in sorted w[0..m)? */
static int present(const uint64_t *w, uint64_t m, uint64_t key, int n) {
    uint64_t mask = (n == 64) ? ~0ULL : (~0ULL << (64 - n));
    uint64_t lo = 0, hi = m;
    while (lo < hi) {
        uint64_t mid = lo + (hi - lo) / 2;
        uint64_t v = w[mid] & mask;
        if (v < key) lo = mid + 1; else hi = mid;
    }
    return lo < m && (w[lo] & mask) == key;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s <bitstream.bin> [max_bits]\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "rb");
    if (!f) { perror("fopen"); return 1; }
    fseek(f, 0, SEEK_END); long fsz = ftell(f); fseek(f, 0, SEEK_SET);
    unsigned char *data = malloc(fsz);
    if (fread(data, 1, fsz, f) != (size_t)fsz) { perror("fread"); return 1; }
    fclose(f);

    uint64_t N = (uint64_t)fsz * 8;
    if (argc > 2) { uint64_t lim = strtoull(argv[2], NULL, 10); if (lim < N) N = lim; }
    if (N < 128) { fprintf(stderr, "prefix too short\n"); return 1; }
    uint64_t M = N - 63;                    /* positions with a full 64-bit window */

    fprintf(stderr, "prefix N=%llu bits, full windows M=%llu\n",
            (unsigned long long)N, (unsigned long long)M);
    double t0 = now();

    uint64_t *w = malloc(M * sizeof(uint64_t));
    uint64_t *tmp = malloc(M * sizeof(uint64_t));
    if (!w || !tmp) { fprintf(stderr, "alloc %.1f GB failed\n",
                              2.0 * M * 8 / 1e9); return 1; }

    /* rolling MSB-first 64-bit window */
    uint64_t cur = 0;
    for (int k = 0; k < 64; k++) cur = (cur << 1) | (uint64_t)getbit(data, k);
    w[0] = cur;
    for (uint64_t i = 1; i < M; i++) {
        cur = (cur << 1) | (uint64_t)getbit(data, i + 63);
        w[i] = cur;
    }
    fprintf(stderr, "windows built (%.1fs)\n", now() - t0);

    radix_sort(w, tmp, M);
    free(tmp);
    fprintf(stderr, "sorted (%.1fs)\n", now() - t0);

    printf("{\n \"prefix_length\": %llu,\n \"full_window_positions\": %llu,\n \"rows\": [\n",
           (unsigned long long)N, (unsigned long long)M);

    uint64_t best_p = 0; int best_n = 0; int longest_repeated = 0; int all_exceed = 1;
    for (int n = 1; n <= 64; n++) {
        uint64_t mask = (n == 64) ? ~0ULL : (~0ULL << (64 - n));
        uint64_t distinct = 1;
        uint64_t prev = w[0] & mask;
        for (uint64_t i = 1; i < M; i++) {
            uint64_t v = w[i] & mask;
            if (v != prev) { distinct++; prev = v; }
        }
        /* fold in the <=63 tail windows: positions M .. N-n */
        uint64_t extra = 0;
        if (N >= (uint64_t)n) {
            uint64_t tailvals[64]; int tn = 0;
            for (uint64_t i = M; i + (uint64_t)n <= N; i++) {
                uint64_t v = 0;
                for (int k = 0; k < n; k++) v = (v << 1) | (uint64_t)getbit(data, i + k);
                v <<= (64 - n);
                if (present(w, M, v, n)) continue;
                int dup = 0;
                for (int j = 0; j < tn; j++) if (tailvals[j] == v) { dup = 1; break; }
                if (!dup && tn < 64) tailvals[tn++] = v;
            }
            extra = (uint64_t)tn;
        }
        uint64_t p = distinct + extra;
        uint64_t avail = N - (uint64_t)n + 1;
        if (p > best_p) { best_p = p; best_n = n; }
        if (p < avail) longest_repeated = n;      /* some length-n factor repeats */
        if (p <= (uint64_t)n) all_exceed = 0;
        printf("  {\"n\": %d, \"p_n\": %llu, \"windows_available\": %llu, "
               "\"saturation\": %.9f, \"exceeds_n\": %s}%s\n",
               n, (unsigned long long)p, (unsigned long long)avail,
               (double)p / (double)avail, p > (uint64_t)n ? "true" : "false",
               n == 64 ? "" : ",");
        fflush(stdout);
    }
    printf(" ],\n");
    printf(" \"all_n_1_to_64_exceed_n\": %s,\n", all_exceed ? "true" : "false");
    printf(" \"L_is_only_a_lower_bound\": %s,\n", longest_repeated == 64 ? "true" : "false");
    printf(" \"max_p_n\": %llu,\n \"argmax_n\": %d,\n", (unsigned long long)best_p, best_n);
    printf(" \"longest_repeated_factor_L\": %d,\n", longest_repeated);
    printf(" \"excluded_preperiod_plus_period_below\": %llu,\n", (unsigned long long)best_p);
    printf(" \"elapsed_s\": %.1f\n}\n", now() - t0);
    fprintf(stderr, "done (%.1fs)\n", now() - t0);
    return 0;
}
