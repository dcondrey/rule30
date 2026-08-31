"""Test 3 (PREREG.md): NIST SP 800-22 subtests under the BLOCK protocol.

Ten p-value streams: monobit frequency, frequency-within-block, runs,
longest-run-of-ones, cumulative sums forward, cumulative sums reverse,
approximate entropy (m=3), serial m=3 (p1 and p2), DFT spectral.

Protocol, as SP 800-22 actually specifies it: K = 100 disjoint blocks of 10^4
bits, one p-value per subtest per block, then the two meta-tests

  (a) pass proportion at alpha = 0.01 against 1-alpha +/- 3 sqrt(alpha(1-alpha)/K)
      = [0.9602, 1.0198];
  (b) uniformity of the 100 p-values: NIST chi-square on 10 equal bins
      (threshold P_T >= 0.0001) and a Kolmogorov-Smirnov test against U(0,1).

A single p-value on one long string is also reported (T = 2^20) but is the
weaker statement.

The DFT test uses sqrt(n * 0.95 * 0.05 / 4), the SP 800-22 (2001) constant.
Kim, Umeno and Hasegawa (2004) derive d = 3.8 as a correction to it.
`null_calibration.py` runs both, plus the DC-bin variants, over 2000 pure-null
blocks: all four behave identically to within noise, the choice does not move
the verdict, and the residual non-uniformity is the discreteness of the integer
count n1, not the constant.  See that script's output for the numbers.

Run: uv run python test3_nist.py
"""

from __future__ import annotations

import json
import logging
import math
import pathlib

import numpy as np
from scipy import stats
from scipy.special import erfc, gammaincc

HERE = pathlib.Path(__file__).resolve().parent
SEQ = HERE / "seq"
K_BLOCKS = 100
BLOCK = 10_000
GLOBAL_N = 100_838
CONTROLS = ["rule30", "rule90", "lfsr32", "bern51", "lag1000", "copy1000"]
IID = [f"iid_{k:02d}" for k in range(20)]

log = logging.getLogger("t3")


# ---------------------------------------------------------------- subtests
def t_monobit(b):
    n = b.size
    s = abs(int((2 * b.astype(np.int64) - 1).sum())) / math.sqrt(n)
    return float(erfc(s / math.sqrt(2)))


def t_block_frequency(b, M=100):
    n = b.size
    N = n // M
    pi = b[: N * M].reshape(N, M).mean(axis=1)
    chi2 = 4.0 * M * float(((pi - 0.5) ** 2).sum())
    return float(gammaincc(N / 2.0, chi2 / 2.0))


def t_runs(b):
    n = b.size
    pi = float(b.mean())
    if abs(pi - 0.5) >= 2.0 / math.sqrt(n):
        return 0.0  # NIST: frequency pretest failed -> p = 0
    v = 1 + int((b[1:] != b[:-1]).sum())
    num = abs(v - 2.0 * n * pi * (1 - pi))
    den = 2.0 * math.sqrt(2.0 * n) * pi * (1 - pi)
    return float(erfc(num / den))


_LR_M128 = {"M": 128, "N": 49, "K": 5, "lo": 4,
            "pi": [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]}


def t_longest_run(b):
    p = _LR_M128
    M, N = p["M"], p["N"]
    if b.size < M * N:
        return None
    blocks = b[: M * N].reshape(N, M)
    v = [0] * (p["K"] + 1)
    for row in blocks:
        run = best = 0
        for x in row:
            run = run + 1 if x else 0
            if run > best:
                best = run
        idx = min(max(best, p["lo"]), p["lo"] + p["K"]) - p["lo"]
        v[idx] += 1
    chi2 = sum((v[i] - N * p["pi"][i]) ** 2 / (N * p["pi"][i]) for i in range(p["K"] + 1))
    return float(gammaincc(p["K"] / 2.0, chi2 / 2.0))


def _cusum(b, reverse):
    n = b.size
    x = 2 * b.astype(np.int64) - 1
    if reverse:
        x = x[::-1]
    z = int(np.abs(np.cumsum(x)).max())
    if z == 0:
        return 1.0
    sq = math.sqrt(n)
    s = 0.0
    k0 = int((-n / z + 1) // 4)
    k1 = int((n / z - 1) // 4)
    for k in range(k0, k1 + 1):
        s += stats.norm.cdf((4 * k + 1) * z / sq) - stats.norm.cdf((4 * k - 1) * z / sq)
    k0 = int((-n / z - 3) // 4)
    for k in range(k0, k1 + 1):
        s -= stats.norm.cdf((4 * k + 3) * z / sq) - stats.norm.cdf((4 * k + 1) * z / sq)
    return float(max(0.0, min(1.0, 1.0 - s)))


def t_cusum_fwd(b):
    return _cusum(b, False)


def t_cusum_rev(b):
    return _cusum(b, True)


def _psi2(b, m):
    """NIST psi^2_m using circularly-extended overlapping m-blocks."""
    n = b.size
    if m <= 0:
        return 0.0
    ext = np.concatenate([b, b[: m - 1]]) if m > 1 else b
    idx = np.zeros(n, dtype=np.int64)
    for j in range(m):
        idx += ext[j : j + n].astype(np.int64) << (m - 1 - j)
    counts = np.bincount(idx, minlength=1 << m).astype(np.float64)
    return float((1 << m) / n * (counts ** 2).sum() - n)


def t_approx_entropy(b, m=3):
    n = b.size
    phi_m = _apen_phi(b, m)
    phi_m1 = _apen_phi(b, m + 1)
    apen = phi_m - phi_m1
    chi2 = 2.0 * n * (math.log(2) - apen)
    return float(gammaincc(2 ** (m - 1), chi2 / 2.0))


def _apen_phi(b, m):
    n = b.size
    ext = np.concatenate([b, b[:m]])
    idx = np.zeros(n, dtype=np.int64)
    for j in range(m):
        idx += ext[j : j + n].astype(np.int64) << (m - 1 - j)
    c = np.bincount(idx, minlength=1 << m).astype(np.float64) / n
    nz = c[c > 0]
    return float((nz * np.log(nz)).sum())


def t_serial(b, m=3):
    n = b.size
    p_m = _psi2(b, m)
    p_m1 = _psi2(b, m - 1)
    p_m2 = _psi2(b, m - 2)
    d1 = p_m - p_m1
    d2 = p_m - 2 * p_m1 + p_m2
    return (float(gammaincc(2 ** (m - 2), d1 / 2.0)),
            float(gammaincc(2 ** (m - 3), d2 / 2.0)))


def t_dft(b):
    n = b.size
    x = 2.0 * b.astype(np.float64) - 1.0
    mods = np.abs(np.fft.rfft(x)[: n // 2])
    thr = math.sqrt(math.log(1.0 / 0.05) * n)
    n1 = float((mods < thr).sum())
    n0 = 0.95 * n / 2.0
    d = (n1 - n0) / math.sqrt(n * 0.95 * 0.05 / 4.0)  # SP 800-22 (2001) constant
    return float(erfc(abs(d) / math.sqrt(2)))


def all_subtests(b) -> dict[str, float | None]:
    s1, s2 = t_serial(b, 3)
    return {
        "monobit": t_monobit(b),
        "block_frequency": t_block_frequency(b),
        "runs": t_runs(b),
        "longest_run": t_longest_run(b),
        "cusum_fwd": t_cusum_fwd(b),
        "cusum_rev": t_cusum_rev(b),
        "approx_entropy_m3": t_approx_entropy(b, 3),
        "serial_m3_p1": s1,
        "serial_m3_p2": s2,
        "dft_spectral": t_dft(b),
    }


STREAMS = ["monobit", "block_frequency", "runs", "longest_run", "cusum_fwd", "cusum_rev",
           "approx_entropy_m3", "serial_m3_p1", "serial_m3_p2", "dft_spectral"]

# SP 800-22 has 15 tests. Eight are implemented above (10 p-value streams, since
# cusum and serial each yield two). The seven NOT implemented are named here with
# reasons, so the omission is an explicit artifact rather than a silent gap.
NOT_IMPLEMENTED = {
    "binary_matrix_rank": "Not implemented. Needs GF(2) rank of 32x32 submatrices; "
        "a 10^4-bit block supplies only ~9 matrices against the 38 NIST requires "
        "for the chi-square to be valid, so it could not be run under this arm's "
        "block protocol without changing the block size.",
    "non_overlapping_template": "Not implemented. 148 templates x 100 blocks would "
        "add ~14,800 hypotheses to a ledger fixed at N = 100,838 before data; "
        "adding it post hoc would break the pre-registration.",
    "overlapping_template": "Not implemented, same reason, plus it needs the "
        "Pi-value table for m = 9 at the NIST-recommended n = 10^6 per block, "
        "which this block protocol does not supply.",
    "maurer_universal": "Not implemented. NIST requires n >= 387,840 for L = 6 and "
        "much more for larger L; a 10^4-bit block cannot support it. It would run "
        "on the whole 2^20 sequence but not under the block protocol, and a "
        "whole-sequence-only stream is the weaker statement this test 3 avoids.",
    "linear_complexity": "Deliberately omitted as REDUNDANT: test 1 measures the "
        "Berlekamp-Massey profile directly, to n = 2^20, with a 500-seed "
        "non-parametric null. NIST's version is a coarser chi-square on jump "
        "classes over short blocks and would add nothing test 1 does not cover.",
    "random_excursions": "Not implemented. Requires at least 500 cycles of the "
        "cumulative-sum random walk; a 10^4-bit block yields far fewer, so NIST's "
        "own applicability condition fails at this block size.",
    "random_excursions_variant": "Not implemented, same applicability failure.",
}


def meta(pvals: list[float]) -> dict:
    p = np.asarray([x for x in pvals if x is not None], dtype=float)
    Kn = p.size
    passed = int((p >= 0.01).sum())
    prop = passed / Kn
    lo = 0.99 - 3 * math.sqrt(0.01 * 0.99 / Kn)
    hi = min(1.0, 0.99 + 3 * math.sqrt(0.01 * 0.99 / Kn))
    hist = np.histogram(np.clip(p, 0, 1 - 1e-15), bins=10, range=(0, 1))[0]
    chi2 = float(((hist - Kn / 10.0) ** 2 / (Kn / 10.0)).sum())
    p_uni = float(gammaincc(4.5, chi2 / 2.0))
    ks = stats.kstest(p, "uniform")
    return {"K": Kn, "n_pass_at_0.01": passed, "pass_proportion": prop,
            "nist_interval": [lo, hi], "proportion_ok": bool(lo <= prop <= hi),
            "chi2_uniformity": chi2, "P_T": p_uni, "P_T_ok": bool(p_uni >= 0.0001),
            "ks_stat": float(ks.statistic), "ks_p": float(ks.pvalue)}


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    out: dict = {"K_blocks": K_BLOCKS, "block_bits": BLOCK, "global_N": GLOBAL_N,
                 "streams": STREAMS, "not_implemented": NOT_IMPLEMENTED,
                 "n_of_15_implemented": 8, "sequences": {}}
    for name in CONTROLS + IID:
        bits = np.load(SEQ / f"{name}.npy")
        per_block = [all_subtests(bits[i * BLOCK:(i + 1) * BLOCK]) for i in range(K_BLOCKS)]
        whole = all_subtests(bits)
        rec = {"whole_sequence_T": int(bits.size), "whole": whole, "block_meta": {}}
        if name in CONTROLS:
            # Every per-block p-value, so a reader can redo any correction or
            # re-derive the meta-tests. Kept for the 6 named sequences; the 20
            # null seeds contribute only through the calibration summaries.
            rec["per_block_pvalues"] = {s: [blk[s] for blk in per_block] for s in STREAMS}
        for s in STREAMS:
            rec["block_meta"][s] = meta([blk[s] for blk in per_block])
        fails = [s for s in STREAMS
                 if not rec["block_meta"][s]["proportion_ok"] or not rec["block_meta"][s]["P_T_ok"]]
        whole_bonf = [s for s in STREAMS
                      if whole[s] is not None and whole[s] * GLOBAL_N < 0.05]
        rec["block_meta_failures"] = fails
        rec["whole_sequence_bonferroni_rejections"] = whole_bonf
        rec["verdict"] = ("REJECT (bias detected)" if (fails or whole_bonf)
                          else "all 10 streams pass both meta-tests; no whole-sequence p survives Bonferroni")
        out["sequences"][name] = rec
        if name in CONTROLS:
            log.info("%-9s block-meta failures: %-58s whole-seq Bonferroni rejects: %s",
                     name, ",".join(fails) or "none", ",".join(whole_bonf) or "none")

    (HERE / "test3_nist_output.json").write_text(json.dumps(out, indent=2))

    lines = [f"Test 3: NIST SP 800-22 subtests, K={K_BLOCKS} blocks of {BLOCK} bits + whole T=2^20",
             "meta-tests: pass proportion in [0.9602, 1.0] and p-value uniformity P_T >= 0.0001", ""]
    for name in CONTROLS:
        r = out["sequences"][name]
        lines.append(f"--- {name} ---")
        lines.append(f"{'stream':<20}{'pass/K':>8}{'prop_ok':>9}{'P_T':>12}{'P_T_ok':>8}{'KS p':>11}{'whole p':>12}")
        for s in STREAMS:
            m = r["block_meta"][s]
            w = r["whole"][s]
            lines.append(f"{s:<20}{m['n_pass_at_0.01']:>4}/{m['K']:<3}{str(m['proportion_ok']):>9}"
                         f"{m['P_T']:>12.4g}{str(m['P_T_ok']):>8}{m['ks_p']:>11.3g}"
                         f"{('n/a' if w is None else f'{w:.4g}'):>12}")
        lines.append(f"verdict: {r['verdict']}")
        lines.append("")
    n_iid_fail = sum(1 for s in IID if out["sequences"][s]["block_meta_failures"])
    lines.append(f"i.i.d. null seeds with at least one block-meta failure: {n_iid_fail} of 20")
    lines += ["", "SP 800-22 has 15 tests. 8 implemented above (10 p-value streams).",
              "The 7 NOT run, and why:"]
    for k, v in NOT_IMPLEMENTED.items():
        lines.append(f"  - {k}: {v}")
    (HERE / "test3_nist_output.txt").write_text("\n".join(lines) + "\n")
    log.info("i.i.d. null seeds with >=1 block-meta failure: %d of 20", n_iid_fail)


if __name__ == "__main__":
    main()
