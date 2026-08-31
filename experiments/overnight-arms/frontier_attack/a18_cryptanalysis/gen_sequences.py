"""Generate and GATE every bit sequence used by the a18 cryptanalysis arm.

Sequences (see PREREG.md):
  rule30   lone-seed Rule 30 centre column, OEIS A051023          -- the object
  rule90   lone-seed Rule 90 centre column (1,0,0,0,...)          -- rule filter (degenerate)
  lfsr32   maximal-length degree-32 LFSR keystream                -- power control, test 1
  bern51   i.i.d. Bernoulli(0.51)                                 -- power control, test 3
  lag1000  r_t XOR r_{t-1000}, r i.i.d. Bernoulli(1/2)            -- power control, tests 2,4
  iid_00..iid_19  i.i.d. Bernoulli(1/2)                           -- null band

GATE: the rule30 column is checked bit-for-bit over its first 2^16 bits against
BOTH experiments/rule30/center_column.py (repo ground truth, OEIS-gated) and
experiments/overnight-arms/common/rule30.py::center_column_bits.  The script
exits non-zero on any divergence and writes nothing.

Run: uv run python gen_sequences.py
Writes: seq/<id>.npy (uint8, one bit per byte) and gen_sequences_output.{json,txt}
"""

from __future__ import annotations

import importlib.util
import json
import logging
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
SEQ = HERE / "seq"
T = 1 << 20
GATE_BITS = 1 << 16

log = logging.getLogger("gen")


def _load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def centre_column(rule: int, n: int) -> np.ndarray:
    """Lone-seed centre column via the shifted-frame bigint recurrence.

    b_t(i) = s(t, i-t).  Rule 30: b <- (b<<2) ^ ((b<<1) | b).
    Rule 90: b <- (b<<2) ^ b.  Centre cell s(t,0) = bit t of b_t.
    """
    row = 1
    out = bytearray(n)
    if rule == 30:
        for t in range(n):
            out[t] = (row >> t) & 1
            row = (row << 2) ^ ((row << 1) | row)
    elif rule == 90:
        for t in range(n):
            out[t] = (row >> t) & 1
            row = (row << 2) ^ row
    else:
        raise ValueError(rule)
    return np.frombuffer(bytes(out), dtype=np.uint8)


def lfsr32(n: int, state: int = 0xACE1_2345) -> np.ndarray:
    """Fibonacci LFSR, taps 32,22,2,1 (a maximal-length degree-32 primitive poly).

    Output bit is the shifted-out low bit, so the keystream has linear
    complexity exactly 32 and must break the Berlekamp-Massey profile test.
    """
    out = bytearray(n)
    s = state & 0xFFFF_FFFF
    assert s != 0
    for i in range(n):
        bit = s & 1
        out[i] = bit
        fb = ((s >> 0) ^ (s >> 1) ^ (s >> 21) ^ (s >> 31)) & 1
        s = (s >> 1) | (fb << 31)
    return np.frombuffer(bytes(out), dtype=np.uint8)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    SEQ.mkdir(exist_ok=True)
    rec: dict = {"T": T, "gate_bits": GATE_BITS, "sequences": {}}

    t0 = time.time()
    cache = SEQ / "rule30.npy"
    if cache.exists():
        c30 = np.load(cache)
        assert c30.shape == (T,)
        log.info("rule30 loaded from cache (still gated below)")
    else:
        c30 = centre_column(30, T)
    gen_s = time.time() - t0
    log.info("rule30 generated: %d bits in %.1f s", T, gen_s)

    # ---- GATE ----------------------------------------------------------
    truth_mod = _load(REPO / "experiments/rule30/center_column.py", "repo_truth")
    truth = np.fromiter(truth_mod.center_column(GATE_BITS), dtype=np.uint8, count=GATE_BITS)
    common = _load(REPO / "experiments/overnight-arms/common/rule30.py", "common_r30")
    common_bits = np.asarray(common.center_column_bits(GATE_BITS), dtype=np.uint8)

    g1 = bool(np.array_equal(c30[:GATE_BITS], truth))
    g2 = bool(np.array_equal(c30[:GATE_BITS], common_bits))
    log.info("GATE vs experiments/rule30/center_column.py  (%d bits): %s", GATE_BITS, "MATCH" if g1 else "DIVERGE")
    log.info("GATE vs common/rule30.py::center_column_bits (%d bits): %s", GATE_BITS, "MATCH" if g2 else "DIVERGE")
    if not (g1 and g2):
        log.error("GATE FAILED -- writing nothing")
        return 1
    rec["gate"] = {"vs_repo_center_column": g1, "vs_common_rule30": g2, "bits": GATE_BITS}
    rec["gen_seconds_rule30"] = gen_s

    seqs: dict[str, np.ndarray] = {"rule30": c30}

    c90 = centre_column(90, T)
    assert c90[0] == 1 and not c90[1:].any(), "rule 90 lone-seed column is not 1,0,0,..."
    seqs["rule90"] = c90

    seqs["lfsr32"] = lfsr32(T)
    period = None
    ls = seqs["lfsr32"]
    for p in (2**32 - 1,):
        period = p
    rec["lfsr32_period_claimed"] = period

    rng = np.random.default_rng(1234)
    seqs["bern51"] = (rng.random(T) < 0.51).astype(np.uint8)

    # lag1000: the ORIGINAL pre-registered control, kept because it is an
    # instructive failure.  y_t = r_t XOR r_{t-1000} has NO lag-1000
    # autocorrelation: y_t XOR y_{t+1000} = r_{t-1000} XOR r_{t+1000}, which is
    # uniform.  The construction is a linear combination that destroys the very
    # correlation it was meant to plant.  Retained and reported as such.
    rng2 = np.random.default_rng(5678)
    r = rng2.integers(0, 2, size=T + 1000, dtype=np.uint8)
    seqs["lag1000"] = (r[1000:] ^ r[:-1000])[:T].astype(np.uint8)

    # copy1000: the CORRECTED power control for tests 2 and 4.  A copy channel:
    # y_t = y_{t-1000} with probability p, else an independent fair bit.  Then
    # Pr[y_t = y_{t+1000}] = 1/2 + p/2, so the lag-1000 autocorrelation is
    # exactly p and z ~ p*sqrt(T) = 20 at p = 0.02, T = 2^20.
    P_COPY = 0.02
    rng3 = np.random.default_rng(9012)
    fresh = rng3.integers(0, 2, size=T, dtype=np.uint8)
    copy_mask = rng3.random(T) < P_COPY
    y = fresh.copy()
    for t in range(1000, T):
        if copy_mask[t]:
            y[t] = y[t - 1000]
    seqs["copy1000"] = y
    rec["copy1000_p"] = P_COPY

    for k in range(20):
        seqs[f"iid_{k:02d}"] = np.random.default_rng(k).integers(0, 2, size=T, dtype=np.uint8)

    for name, arr in seqs.items():
        assert arr.dtype == np.uint8 and arr.shape == (T,), (name, arr.dtype, arr.shape)
        assert arr.max() <= 1
        np.save(SEQ / f"{name}.npy", arr)
        ones = int(arr.sum())
        rec["sequences"][name] = {"len": T, "ones": ones, "density": ones / T}
        log.info("%-9s ones=%d density=%.6f  prefix=%s", name, ones, ones / T,
                 "".join(map(str, arr[:32].tolist())))

    (HERE / "gen_sequences_output.json").write_text(json.dumps(rec, indent=2))
    lines = [f"a18 gen_sequences  T={T}",
             f"GATE vs repo center_column.py: {'MATCH' if g1 else 'DIVERGE'} ({GATE_BITS} bits)",
             f"GATE vs common/rule30.py:      {'MATCH' if g2 else 'DIVERGE'} ({GATE_BITS} bits)",
             ""]
    for name, d in rec["sequences"].items():
        lines.append(f"{name:<9} len={d['len']} ones={d['ones']} density={d['density']:.6f}")
    (HERE / "gen_sequences_output.txt").write_text("\n".join(lines) + "\n")
    log.info("wrote %d sequences to %s", len(seqs), SEQ)
    return 0


if __name__ == "__main__":
    sys.exit(main())
