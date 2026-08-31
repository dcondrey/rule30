"""Test 1 (PREREG.md): Berlekamp-Massey linear complexity PROFILE statistics.

NOT a duplicate of register row 14.  Row 14 (ARM4-frequency-domain.md) already
measured the CEILING, L(n)/(n/2) ~= 1.0 through n = 16384, and that result is
taken as given here.  A maximal ceiling does NOT determine the profile: a
sequence can sit on the n/2 line while its jump structure is anomalous.  The
registered statistics are therefore

  J(n)     number of jumps of the profile in [1,n]
  Hbar(n)  mean jump height
  D(n)     (1/n) sum_{m<=n} (L(m) - m/2), the mean signed deviation from the line

for which a random sequence has known behaviour (Rueppel): jumps are sparse with
geometric heights and L(m) - m/2 is O(1), so D(n) concentrates near a small
constant.  Null band from 20 i.i.d. Bernoulli seeds.

One BM run to n_max yields L(m) for EVERY m <= n_max, so all prefix lengths come
from a single pass.  BM is Theta(n^2); with GF(2) polynomials held as Python ints
the cost is ~n^2/64 word operations.  Depth actually reached is reported.

Run: uv run python test1_bm_profile.py
"""

from __future__ import annotations

import json
import logging
import pathlib
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
SEQ = HERE / "seq"
NMAX = 1 << 18
NMAX_IID = 1 << 17
PREFIXES = (1 << 10, 1 << 12, 1 << 14, 1 << 16, 1 << 17, 1 << 18)
CONTROLS = ["rule30", "rule90", "lfsr32", "bern51", "lag1000", "copy1000"]
IID = [f"iid_{k:02d}" for k in range(20)]

log = logging.getLogger("t1")


def bm_profile(bits: np.ndarray) -> tuple[list[int], list[tuple[int, int]]]:
    """Berlekamp-Massey over GF(2).

    Returns (L, jumps) where L[n] is the linear complexity of the first n bits
    (L[0] = 0) and jumps is the list of (n, height) at which L increased,
    n being the 1-based prefix length after which the jump took effect.

    Connection polynomial C held as a Python int, bit i = coefficient of x^i.
    R holds the reversed bit window so the discrepancy is
    popcount(C & R) mod 2.
    """
    n_total = int(bits.size)
    b = bits.astype(np.uint8).tolist()
    C = 1
    B = 1
    L = 0
    m = -1
    R = 0
    Ls = [0] * (n_total + 1)
    jumps: list[tuple[int, int]] = []
    for n in range(n_total):
        R = (R << 1) | b[n]
        if (n & 1023) == 0:
            # Only the low L+1 bits of R are ever read, and L <= n/2 + 1 for BM.
            # Truncating keeps the AND from degrading to O(n) words. Done every
            # 1024 steps so the mask construction is amortized away.
            R &= (1 << (n // 2 + 1032)) - 1
        d = (C & R).bit_count() & 1
        if d:
            T = C
            C ^= B << (n - m)
            if 2 * L <= n:
                jumps.append((n + 1, n + 1 - 2 * L))
                L = n + 1 - L
                B = T
                m = n
        Ls[n + 1] = L
    return Ls, jumps


def stats_at(Ls: list[int], jumps: list[tuple[int, int]], n: int) -> dict:
    j = [h for (pos, h) in jumps if pos <= n]
    dev = sum(Ls[m] - m / 2.0 for m in range(1, n + 1)) / n
    return {"L": Ls[n], "L_over_half_n": Ls[n] / (n / 2.0),
            "J": len(j), "Hbar": (sum(j) / len(j)) if j else 0.0, "D": dev}


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    out: dict = {"nmax_controls": NMAX, "nmax_iid": NMAX_IID, "prefixes": list(PREFIXES),
                 "sequences": {}, "note": "row 14 already measured the ceiling; the "
                 "registered statistics here are J, Hbar, D"}
    prof = {}
    for name in CONTROLS + IID:
        cap = NMAX if name in CONTROLS else NMAX_IID
        bits = np.load(SEQ / f"{name}.npy")[:cap]
        t0 = time.time()
        Ls, jumps = bm_profile(bits)
        el = time.time() - t0
        prof[name] = (Ls, jumps)
        rows = {n: stats_at(Ls, jumps, n) for n in PREFIXES if n <= cap}
        out["sequences"][name] = {"nmax": cap, "seconds": el, "profile": {str(k): v for k, v in rows.items()}}
        if name in CONTROLS:
            top = rows[max(rows)]
            log.info("%-9s n=%d L=%d L/(n/2)=%.4f J=%d Hbar=%.3f D=%.4f  (%.1fs)",
                     name, max(rows), top["L"], top["L_over_half_n"], top["J"], top["Hbar"],
                     top["D"], el)

    # Null band per prefix, per statistic, over the 20 i.i.d. seeds.
    band: dict = {}
    for n in PREFIXES:
        if n > NMAX_IID:
            continue
        band[str(n)] = {}
        for st in ("J", "Hbar", "D", "L_over_half_n"):
            v = np.array([out["sequences"][s]["profile"][str(n)][st] for s in IID])
            band[str(n)][st] = {"min": float(v.min()), "max": float(v.max()),
                                "mean": float(v.mean()), "sd": float(v.std(ddof=1))}
    out["iid_band"] = band

    verdicts = {}
    for name in CONTROLS:
        exceed = []
        zs = []
        for n in PREFIXES:
            if str(n) not in band or str(n) not in out["sequences"][name]["profile"]:
                continue
            for st in ("J", "Hbar", "D"):
                val = out["sequences"][name]["profile"][str(n)][st]
                bd = band[str(n)][st]
                z = (val - bd["mean"]) / bd["sd"] if bd["sd"] > 0 else float("inf") if val != bd["mean"] else 0.0
                zs.append({"n": n, "stat": st, "value": val, "z": z,
                           "outside_seed_band": bool(val < bd["min"] or val > bd["max"])})
                if val < bd["min"] or val > bd["max"]:
                    exceed.append(f"{st}@{n}")
        out["sequences"][name]["z_vs_iid"] = zs
        out["sequences"][name]["outside_seed_band"] = exceed
        mz = max((abs(x["z"]) for x in zs), default=0.0)
        verdicts[name] = ("REJECT (profile anomalous)" if mz > 5.032
                          else f"profile within i.i.d. band; max |z| = {mz:.2f}")
        out["sequences"][name]["verdict"] = verdicts[name]
        log.info("%-9s max |z| vs iid band = %.2f  outside band: %s", name, mz,
                 ",".join(exceed) or "none")

    (HERE / "test1_bm_profile_output.json").write_text(json.dumps(out, indent=2))
    lines = ["Test 1: Berlekamp-Massey linear complexity PROFILE",
             "(row 14 already measured the ceiling L/(n/2) ~= 1 to n=16384; not re-run as the claim)",
             f"controls to n={NMAX}, i.i.d. null seeds to n={NMAX_IID}", ""]
    for name in CONTROLS:
        lines.append(f"--- {name} (n_max = {out['sequences'][name]['nmax']}) ---")
        lines.append(f"{'n':>8}{'L':>10}{'L/(n/2)':>10}{'J':>8}{'Hbar':>9}{'D':>10}")
        for n in PREFIXES:
            p = out["sequences"][name]["profile"].get(str(n))
            if p:
                lines.append(f"{n:>8}{p['L']:>10}{p['L_over_half_n']:>10.4f}{p['J']:>8}"
                             f"{p['Hbar']:>9.3f}{p['D']:>10.4f}")
        lines.append(f"outside i.i.d. seed band: {','.join(out['sequences'][name]['outside_seed_band']) or 'none'}")
        lines.append(f"verdict: {verdicts[name]}")
        lines.append("")
    lines.append("i.i.d. null band (20 seeds):")
    for n in PREFIXES:
        if str(n) not in band:
            continue
        for st in ("J", "Hbar", "D"):
            b = band[str(n)][st]
            lines.append(f"  n={n:<7} {st:<5} [{b['min']:.4f}, {b['max']:.4f}] mean={b['mean']:.4f} sd={b['sd']:.4f}")
    (HERE / "test1_bm_profile_output.txt").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
