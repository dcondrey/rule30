"""Tile layout for rule30_kernel_v6.cu, and a host-side mirror of its
recording-ownership predicate. Stdlib only, no modal, no cupy: it has to be
importable both inside the Modal image and by the local verifier.

The mirror exists because the defect in KERNEL-V6-DEFECT.md was an ownership
bug, and ownership is pure arithmetic that the host can settle before spending
any GPU time. It reports the claimant list rather than a boolean so that BOTH
failure directions are visible:

  2 claimants -> the pre-fix defect: two tiles race on a non-atomic |= and drop 1s.
  0 claimants -> the column is never written and reads as all zeros, which is
                 the same failure class and is SILENT under a self-consistency
                 check (all-zeros satisfies the transduction relation against
                 all-zeros). verify_band.py's density check is the other half.

Keep R/H/WARPS here in step with the -D flags passed to nvcc; they are the same
numbers and a mismatch would make every claim below fiction.
"""

R, H, WARPS = 16, 16, 4               # WORDS_PER_LANE, HALO_WORDS, WARPS_PER_BLOCK

WARP_WORDS = 32 * R                   # words held by one warp tile
STEPS_PER_BATCH = 32 * H              # 512; see the halo-margin note in the .cu
USEFUL_PER_WARP = WARP_WORDS - 2 * H  # 480
USEFUL_PER_BLOCK = USEFUL_PER_WARP * WARPS
WORDS_PER_BATCH = STEPS_PER_BATCH // 32


def recording_claimants(rec_lo_cell: int, n_rec: int, b_off: int, b_cnt: int,
                        useful_only: bool = True) -> list[list[tuple[int, int]]]:
    """[(tile_idx, lane), ...] claiming each recorded column, in kernel terms.

    Mirrors rule30_kernel_v6.cu's ownership test literally, including the tile
    geometry, rather than asserting the conclusion:

        tile_start = tile_idx * USEFUL_WORDS - HALO_WORDS
        wl         = (cell >> 5) - tile_start
        claim      = (useful_only -> HALO_WORDS <= wl < HALO_WORDS+USEFUL_WORDS)
                     and base <= wl < base + WORDS_PER_LANE

    `useful_only=False` is the pre-fix predicate, kept so the mirror can be shown
    to reproduce the double claim rather than only ever reporting success.

    Tiles overlap, so a word can fall inside at most two tiles' full ranges
    ([T*U-H, T*U-H+32R) has width 32R = 512 against a stride of U = 480). The
    scan window below is wider than that bound and so cannot miss a claimant.
    """
    out = []
    for k in range(n_rec):
        w = (rec_lo_cell + k) >> 5
        t0 = w // USEFUL_PER_WARP
        hits = []
        for tile in range(max(0, t0 - 2), t0 + 3):
            if not (b_off <= tile // WARPS < b_off + b_cnt):
                continue                       # block not launched
            wl = w - (tile * USEFUL_PER_WARP - H)
            if useful_only and not (H <= wl < H + USEFUL_PER_WARP):
                continue
            if 0 <= wl < WARP_WORDS:
                hits.append((tile, wl // R))   # lane owning that register slot
        out.append(hits)
    return out


def assert_unique_claimants(rec_lo_cell: int, n_rec: int, b_off: int,
                            b_cnt: int) -> None:
    """Abort before launch unless every recorded column has exactly one owner."""
    claims = recording_claimants(rec_lo_cell, n_rec, b_off, b_cnt)
    bad = {k: c for k, c in enumerate(claims) if len(c) != 1}
    if bad:
        raise RuntimeError(
            f"recording ownership is not unique: {bad} "
            f"(rec_lo_cell={rec_lo_cell}, n_rec={n_rec}, "
            f"b_off={b_off}, b_cnt={b_cnt}). "
            "0 claimants => column reads as all zeros; 2 => the v6 race.")
