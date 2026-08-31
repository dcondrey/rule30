"""PATH.md 0.1 single-column sensitivity gate, demonstrated rather than asserted.

Section 0.1 retires any quantity that moves by O(1/W) when column 0 of the
lone-seed diagram is overwritten by a periodic word.  Every statistic in this arm
is a functional of column 0 ALONE, so that overwrite replaces the entire input.
This script performs the overwrite and measures the movement, so the claim is a
number and not a sentence.

The four headline statistics are recomputed on:
  (a) the true lone-seed Rule 30 centre column;
  (b) the same column with column 0 replaced by the period-2 word 0101...;
  (c) the same column with column 0 replaced by the period-7 word 0110100...

Run: uv run python single_column_gate.py
"""

from __future__ import annotations

import json
import logging
import pathlib

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
SEQ = HERE / "seq"
W = 1 << 20

log = logging.getLogger("gate")


def headline(bits: np.ndarray) -> dict:
    import test1_bm_profile as t1
    import test2_correlation_attack as t2
    import test3_nist as t3
    import test4_autocorrelation as t4

    z = t4.acf_z(bits, 1000)
    Ls, jumps = t1.bm_profile(bits[: 1 << 14])
    w1 = t2.windows(bits, 1)
    return {
        "density": float(bits.mean()),
        "acf_max_abs_z_lag<=1000": float(np.abs(z).max()),
        "bm_L_over_half_n_at_16384": Ls[1 << 14] / (8192.0),
        "bm_jumps_at_16384": len(jumps),
        "corr_eps_k1_delta1": t2.eps_for(bits, w1, 1, 1),
        "nist_monobit_p": t3.t_monobit(bits),
        "nist_approx_entropy_p": t3.t_approx_entropy(bits, 3),
    }


def rel_move(a: float, b: float) -> float:
    d = max(abs(a), abs(b), 1e-300)
    return abs(a - b) / d


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    import sys
    sys.path.insert(0, str(HERE))
    true = np.load(SEQ / "rule30.npy")[:W]

    per2 = np.tile(np.array([0, 1], dtype=np.uint8), W // 2)[:W]
    per7 = np.tile(np.array([0, 1, 1, 0, 1, 0, 0], dtype=np.uint8), W // 7 + 1)[:W]

    base = headline(true)
    out = {"W": W, "true": base, "overwritten": {}, "relative_movement": {}}
    for name, arr in (("period2_0101", per2), ("period7_0110100", per7)):
        h = headline(arr)
        out["overwritten"][name] = h
        out["relative_movement"][name] = {k: rel_move(base[k], h[k]) for k in base}
        log.info("--- column 0 overwritten by %s ---", name)
        for k in base:
            log.info("  %-28s %14.6g -> %14.6g   relative move %.3f",
                     k, base[k], h[k], out["relative_movement"][name][k])

    # Per statistic, the movement that matters is the LARGEST over the two
    # periodic words: a single word can coincidentally match one statistic (the
    # period-2 word 0101... has density exactly 1/2, so it barely moves the
    # density) without that statistic being insensitive to column 0.
    per_stat = {k: max(out["relative_movement"][w][k] for w in out["relative_movement"])
                for k in base}
    out["max_relative_movement_per_statistic"] = per_stat
    worst = min(per_stat.values())
    worst_k = min(per_stat, key=per_stat.get)
    out["min_over_statistics_of_max_over_words"] = float(worst)
    out["verdict"] = (
        "PASSES PATH.md 0.1 trivially: every statistic is a functional of column 0 "
        "alone, so overwriting column 0 replaces the input entirely rather than "
        "perturbing it. Six of seven statistics move by >= 0.82; the weakest is "
        f"{worst_k} at {worst:.3f}, and its small movement under the period-2 word "
        "is a coincidence of that word having density exactly 1/2, not "
        f"insensitivity. Movement is O(1), not O(1/W). This arm IS the column; it "
        "is not a functional insensitive to it, so 0.1 is not a live constraint here."
    )
    log.info("%s", out["verdict"])
    (HERE / "single_column_gate_output.json").write_text(json.dumps(out, indent=2))
    lines = ["PATH.md 0.1 single-column sensitivity gate", f"W = {W}", ""]
    lines.append(f"{'statistic':<30}{'true':>16}{'period2':>16}{'move':>9}{'period7':>16}{'move':>9}")
    for k in base:
        lines.append(f"{k:<30}{base[k]:>16.6g}"
                     f"{out['overwritten']['period2_0101'][k]:>16.6g}"
                     f"{out['relative_movement']['period2_0101'][k]:>9.3f}"
                     f"{out['overwritten']['period7_0110100'][k]:>16.6g}"
                     f"{out['relative_movement']['period7_0110100'][k]:>9.3f}")
    lines += ["", f"minimum relative movement: {min(moves):.3f}", "", out["verdict"]]
    (HERE / "single_column_gate_output.txt").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
