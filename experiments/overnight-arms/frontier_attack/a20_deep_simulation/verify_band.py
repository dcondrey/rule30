"""Full-output verification for a recorded Rule 30 column band.

Why this exists: the gates in `modal_run_band.py` are prefix gates (head64
in-kernel at line 173, head256 in the summary), and `KERNEL-V6-DEFECT.md`
records a defect whose first wrong bit was at 4,631 / 14,416. Every launch-path
gate sat inside the correct prefix. **A prefix gate cannot validate a
generator.** These checks look at the whole output.

Four checks, deliberately independent, so that no single wrong assumption can
make all of them agree:

  A  reference   Full-output equality of every column against an independent
                 gmpy2 band generator in the unshifted frame. Exact, but O(n^2),
                 so it is the gate for the ~1e5..1e6 validation runs, not 3e9.
  B  transduction  col_{x-1}(t) = col_x(t+1) XOR (col_x(t) OR col_{x+1}(t)),
                 applied to the RECORDED columns against each other. Needs no
                 reference generator and works at any depth, so it is the gate
                 that survives to 3e9. Each derived column is predicted from
                 two recorded neighbours, never from another prediction, so the
                 2*hw-1 checks are independent rather than chained.
  C  density     Ones per column. An all-zero column satisfies B against another
                 all-zero column, so B alone cannot see a column that ended up
                 with ZERO claiming tiles. Only C can.
  D  cross-run   Two runs whose layouts coincide must have bit-identical common
                 prefixes. This is the direct test for the non-determinism in
                 KERNEL-V6-DEFECT.md, where n=199998/199999/200000 gave 97/108/101
                 errors sharing only 4 positions.

Check B is the one that catches the recorded defect without any external data:
columns -hw..-1 and 0..+hw live in DIFFERENT tiles (the centre word is always a
tile start), so B spans the tile boundary that the race straddled.

Usage:
    uv run --with numpy --with gmpy2 python verify_band.py --self-test
    uv run --with numpy --with gmpy2 python verify_band.py \
        --dir gpu_pull --tag band_n200000_w4 --hw 4 --reference
    uv run --with numpy python verify_band.py \
        --identical gpu_pull/band_n199998_w4 gpu_pull/band_n199999_w4 --hw 4
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common"))


# ---------------------------------------------------------------- packing

def load_column(path: str, max_bits: int | None = None) -> np.ndarray:
    """Bits of a modal_run_band.py column file: uint32 LE, step i = bit (i&31)
    of word (i>>5), i.e. LSB-first over the byte stream."""
    buf = np.fromfile(path, dtype=np.uint8)
    bits = np.unpackbits(buf, bitorder="little")
    return bits if max_bits is None else bits[:max_bits]


def band_paths(prefix: str, hw: int) -> dict[int, str]:
    """{x: path} for x = -hw..+hw, matching modal_run_band.py's naming."""
    return {x: f"{prefix}_col{x:+d}.bin" for x in range(-hw, hw + 1)}


def steps_from_tag(s: str) -> int | None:
    """The step count n out of a `band_n{n}_w{hw}` tag or path prefix.

    Needed because a column file is ceil(t_done/32) WORDS long, so when t_done
    is not a multiple of 32 the final word is zero-padded. Those padding bits
    were never written by the kernel; comparing them against a reference reads
    them as dropped 1s, which is exactly the signature of the real defect. At
    n=199998 that produced 2 spurious "errors" at bits 199998-199999 and at
    n=199999 one at 199999. Cap every comparison at n.
    """
    import re
    m = re.search(r"(?:^|[^0-9])n(\d+)_w\d+", os.path.basename(s))
    return int(m.group(1)) if m else None


def load_band(prefix: str, hw: int, max_bits: int | None = None
              ) -> dict[int, np.ndarray]:
    return {x: load_column(p, max_bits) for x, p in band_paths(prefix, hw).items()}


# ---------------------------------------------------------------- reference

def band_reference(n: int, hw: int) -> dict[int, np.ndarray]:
    """Columns x = -hw..+hw for t = 0..n-1, from a lone 1 seed.

    Unshifted frame, deep_gen.py's convention: bit p of `row` holds s(t, p-off)
    and one step is row' = (row<<1) ^ (row | (row>>1)); column x is the fixed
    bit off+x throughout. `off` must exceed every t reached or bit positions run
    negative, so it is set to n+hw+2.
    """
    from gmpy2 import mpz, bit_test

    off = n + hw + 2
    row = mpz(1) << off
    cols = {x: np.zeros(n, dtype=np.uint8) for x in range(-hw, hw + 1)}
    for t in range(n):
        for x in range(-hw, hw + 1):
            cols[x][t] = bit_test(row, off + x)
        row = (row << 1) ^ (row | (row >> 1))
    return cols


# ---------------------------------------------------------------- checks

def check_reference(band: dict[int, np.ndarray], ref: dict[int, np.ndarray]) -> dict:
    """A: full-output equality, every column, every bit."""
    cols = {}
    for x in sorted(band):
        a, b = band[x], ref[x]
        n = min(len(a), len(b))
        d = np.flatnonzero(a[:n] != b[:n])
        cols[f"{x:+d}"] = {
            "bits_compared": int(n),
            "match": bool(d.size == 0),
            "n_diff": int(d.size),
            "first_diff_bit": int(d[0]) if d.size else None,
            # the defect was one-directional (dropped 1s); keep the direction
            "gpu0_ref1": int(np.count_nonzero((a[:n] == 0) & (b[:n] == 1))),
            "gpu1_ref0": int(np.count_nonzero((a[:n] == 1) & (b[:n] == 0))),
        }
    return {"pass": all(c["match"] for c in cols.values()), "columns": cols}


def check_transduction(band: dict[int, np.ndarray]) -> dict:
    """B: col_{x-1}(t) = col_x(t+1) XOR (col_x(t) OR col_{x+1}(t)).

    Predicts column x from RECORDED columns x+1 and x+2 only, so the checks do
    not chain and one bad column cannot mask another.
    """
    xs = sorted(band)
    n = min(len(band[x]) for x in xs)
    checks = {}
    for x in xs:
        if (x + 1) not in band or (x + 2) not in band:
            continue
        c1, c2 = band[x + 1][:n], band[x + 2][:n]
        pred = c1[1:] ^ (c1[:-1] | c2[:-1])          # predicts col x for t=0..n-2
        got = band[x][:n - 1]
        d = np.flatnonzero(pred != got)
        checks[f"{x:+d}"] = {
            "from": [f"{x+1:+d}", f"{x+2:+d}"],
            "bits_compared": int(n - 1),
            "match": bool(d.size == 0),
            "n_diff": int(d.size),
            "first_diff_bit": int(d[0]) if d.size else None,
        }
    return {"pass": all(c["match"] for c in checks.values()) and bool(checks),
            "n_checks": len(checks), "columns": checks}


def check_density(band: dict[int, np.ndarray]) -> dict:
    """C: catches a column with zero claiming tiles, which reads as all zeros
    and which check B cannot see.

    This is a GROSS-FAILURE detector, not a test of the density conjecture.
    Whether the centre column's density tends to 1/2 is open (it is Wolfram's
    Problem 2); asserting a tight band here would smuggle that in as an
    assumption and would also fail on honest data. So the window is deliberately
    loose: +/-0.1, widened at small n by the binomial spread a fair coin would
    show anyway (8 sigma, sigma = 0.5/sqrt(n)), which at n=400 is +/-0.2. A
    dead column reads 0.0 and is caught at any n; a real one is never near it.
    """
    cols = {}
    for x in sorted(band):
        a = band[x]
        n = len(a)
        ones = int(a.sum())
        dens = ones / n if n else 0.0
        half = max(0.1, 8 * 0.5 / (n ** 0.5)) if n else 0.5
        cols[f"{x:+d}"] = {"bits": int(n), "ones": ones, "density": dens,
                           "window": [0.5 - half, 0.5 + half],
                           "in_range": bool(abs(dens - 0.5) <= half)}
    return {"pass": all(c["in_range"] for c in cols.values()), "columns": cols}


def check_identical(prefix_a: str, prefix_b: str, hw: int,
                    cap: int | None = None) -> dict:
    """D: bit-identical common prefixes across two runs of the same layout.

    `cap` defaults to the smaller of the two runs' step counts: past that point
    one file is zero-padding and the other is real data, which would read as a
    disagreement that is only a difference in requested length.
    """
    cols = {}
    if cap is None:
        na, nb = steps_from_tag(prefix_a), steps_from_tag(prefix_b)
        cap = min(na, nb) if (na and nb) else None
    pa, pb = band_paths(prefix_a, hw), band_paths(prefix_b, hw)
    for x in sorted(pa):
        if not (os.path.exists(pa[x]) and os.path.exists(pb[x])):
            continue
        a, b = load_column(pa[x], cap), load_column(pb[x], cap)
        n = min(len(a), len(b))
        d = np.flatnonzero(a[:n] != b[:n])
        cols[f"{x:+d}"] = {
            "bits_compared": int(n), "match": bool(d.size == 0),
            "n_diff": int(d.size),
            "first_diff_bit": int(d[0]) if d.size else None,
        }
    return {"pass": all(c["match"] for c in cols.values()) and bool(cols),
            "a": os.path.basename(prefix_a), "b": os.path.basename(prefix_b),
            "columns": cols}


# ---------------------------------------------------------------- self-test

def self_test() -> int:
    """Every check must FIRE on a planted defect, not merely pass on good data.
    A check that has never been seen to fail is not evidence of anything."""
    import rule30 as R

    n, hw = 400, 4

    # 1. the reference generator must agree with the repo's naive frame method.
    ref = band_reference(n, hw)
    rows = R.rows_frame(n)
    for x in range(-hw, hw + 1):
        want = np.array([R.cell(rows[t], t, x) for t in range(n)], dtype=np.uint8)
        assert np.array_equal(ref[x], want), f"band_reference disagrees at x={x}"
    assert ref[0][:20].tolist() == R.center_column_bits(20), "centre != A051023"

    # 2. packing round-trip: modal_run_band.py's writer, read back by load_column.
    import tempfile
    bits = ref[0]
    words = np.zeros((len(bits) + 31) // 32, dtype="<u4")
    for i, b in enumerate(bits):
        if b:
            words[i >> 5] |= np.uint32(1) << np.uint32(i & 31)
    with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as fh:
        words.tofile(fh)
        tmp = fh.name
    assert np.array_equal(load_column(tmp, len(bits)), bits), "packing mismatch"
    os.unlink(tmp)

    # 2b. the zero-padding trap. A run of t steps writes ceil(t/32) WORDS, so
    #     when t is not a multiple of 32 the tail of the last word is padding
    #     that the kernel never wrote. Compared against a reference it reads as
    #     dropped 1s -- indistinguishable from the real defect's signature. This
    #     is not hypothetical: it made n=199998 and n=199999 report 1-2 errors
    #     each at bits 199997-199999 on a kernel that was in fact correct.
    assert steps_from_tag("band_n199998_w4") == 199998
    assert steps_from_tag("gpu_pull/band_n2000000_w4") == 2000000
    assert steps_from_tag("nonsense") is None
    t_odd = 397                                  # 13 words = 416 bits on disk
    padded = band_reference(((t_odd + 31) // 32) * 32, hw)
    truncated = {x: v.copy() for x, v in padded.items()}
    for x in truncated:
        truncated[x][t_odd:] = 0                 # what the file actually holds
    assert not check_reference(truncated, padded)["pass"], \
        "expected the uncapped comparison to fail on padding"
    capped = {x: v[:t_odd] for x, v in truncated.items()}
    assert check_reference(capped, {x: v[:t_odd] for x, v in padded.items()})["pass"], \
        "capping at the step count must clear the padding artefact"

    # 3. all four checks pass on clean data.
    assert check_reference(ref, ref)["pass"]
    assert check_transduction(ref)["pass"], "transduction fails on TRUE data"
    assert check_transduction(ref)["n_checks"] == 2 * hw - 1
    assert check_density(ref)["pass"]

    # 4. each check FIRES on the defect it exists for.
    #    (a) a dropped 1 -- the measured failure mode -- in one column.
    bad = {x: v.copy() for x, v in ref.items()}
    drop = int(np.flatnonzero(bad[0] == 1)[7])
    bad[0][drop] = 0
    ra = check_reference(bad, ref)
    assert not ra["pass"] and ra["columns"]["+0"]["gpu0_ref1"] == 1, "A blind to dropped 1"
    assert not check_transduction(bad)["pass"], "B blind to a dropped 1"

    #    (b) B must span the tile boundary: a drop in a NEGATIVE column, which
    #        lives in a different tile from the centre, must also be caught.
    bad2 = {x: v.copy() for x, v in ref.items()}
    bad2[-3][int(np.flatnonzero(bad2[-3] == 1)[5])] = 0
    assert not check_transduction(bad2)["pass"], "B blind to a defect at x=-3"

    #    (c) a zero-claimant column reads as all zeros. B cannot see it when its
    #        two predictors are also zero; C must.
    zero = {x: v.copy() for x, v in ref.items()}
    for x in (2, 3, 4):
        zero[x][:] = 0
    assert check_transduction(zero)["columns"]["+2"]["match"], \
        "expected B to be blind here -- that is why C exists"
    assert not check_density(zero)["pass"], "C blind to an all-zero column"

    #    (d) D must fire on runs that differ, and pass on runs that do not.
    d = tempfile.mkdtemp()
    def write_band(prefix, cols):
        for x, v in cols.items():
            w = np.zeros((len(v) + 31) // 32, dtype="<u4")
            for i, b in enumerate(v):
                if b:
                    w[i >> 5] |= np.uint32(1) << np.uint32(i & 31)
            w.tofile(f"{prefix}_col{x:+d}.bin")
    write_band(os.path.join(d, "a"), ref)
    write_band(os.path.join(d, "b"), ref)
    write_band(os.path.join(d, "c"), bad)
    assert check_identical(os.path.join(d, "a"), os.path.join(d, "b"), hw)["pass"]
    assert not check_identical(os.path.join(d, "a"), os.path.join(d, "c"), hw)["pass"], \
        "D blind to a differing run"

    # 5. the kernel's recording-ownership predicate, mirrored on the host, must
    #    give exactly one claimant -- and must itself be able to report 0 and 2.
    from band_layout import recording_claimants, USEFUL_PER_BLOCK as upb
    for k_mult, tag in ((4, "block edge"), (33, "warp edge")):
        n_words = k_mult * upb
        centre = n_words * 32 // 2
        cl = recording_claimants(centre - hw, 2 * hw + 1, 0, n_words // upb)
        assert all(len(c) == 1 for c in cl), f"{tag}: claimants {[len(c) for c in cl]}"
        # the band really does straddle two tiles -- that is the whole defect
        assert len({c[0][0] for c in cl}) == 2, f"{tag}: expected a tile straddle"
    # zero claimants when the covering block is not launched
    n_words = 4 * upb
    centre = n_words * 32 // 2
    assert any(len(c) == 0 for c in
               recording_claimants(centre - hw, 2 * hw + 1, 0, 1)), \
        "ownership mirror cannot report a missing block"
    # two claimants under the PRE-FIX predicate, which is the defect itself
    assert any(len(c) == 2 for c in
               recording_claimants(centre - hw, 2 * hw + 1, 0, n_words // upb,
                                   useful_only=False)), \
        "ownership mirror cannot reproduce the pre-fix double claim"

    print("self-test OK: reference matches common/rule30.py; packing pins;\n"
          "  A/B/C/D each fire on the defect they exist for; ownership mirror\n"
          "  gives exactly 1 claimant post-fix and reproduces the pre-fix 2.")
    return 0


# ---------------------------------------------------------------- main

def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dir", default=HERE, help="directory holding the column files")
    p.add_argument("--tag", help="e.g. band_n200000_w4")
    p.add_argument("--hw", type=int, default=4)
    p.add_argument("--reference", action="store_true",
                   help="also run check A (O(n^2); use for <= ~2e6 steps)")
    p.add_argument("--max-bits", type=int, default=None)
    p.add_argument("--identical", nargs=2, metavar=("PREFIX_A", "PREFIX_B"),
                   help="run check D on two band prefixes")
    p.add_argument("--out", default=None)
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()

    if a.self_test:
        return self_test()

    res: dict = {}
    if a.identical:
        res["D_cross_run"] = check_identical(a.identical[0], a.identical[1], a.hw)

    if a.tag:
        prefix = os.path.join(a.dir, a.tag)
        # Cap at the steps actually computed: everything past t_done is padding
        # in the final word and was never written by the kernel.
        cap = a.max_bits or steps_from_tag(a.tag)
        if cap is None:
            print(f"WARNING: no step count in tag {a.tag!r}; comparing the whole "
                  "file including any zero-padding in its final word",
                  file=sys.stderr)
        band = load_band(prefix, a.hw, cap)
        n = min(len(v) for v in band.values())
        res["tag"] = a.tag
        res["bits"] = int(n)
        res["cap_steps"] = cap
        res["B_transduction"] = check_transduction(band)
        res["C_density"] = check_density(band)
        if a.reference:
            res["A_reference"] = check_reference(band, band_reference(n, a.hw))

    checks = {k: v for k, v in res.items() if isinstance(v, dict) and "pass" in v}
    if not checks:
        p.error("nothing to do: pass --tag and/or --identical")
    res["all_pass"] = all(c["pass"] for c in checks.values())

    for k, v in checks.items():
        print(f"{'PASS' if v['pass'] else 'FAIL'}  {k}")
        for name, c in v.get("columns", {}).items():
            if not c.get("match", c.get("in_range", True)):
                print(f"        col {name}: {c}")
    print(f"\n{'ALL PASS' if res['all_pass'] else 'FAILED'} "
          f"over {len(checks)} check(s)")

    out = a.out or os.path.join(HERE, "verify_band_result.json")
    json.dump(res, open(out, "w"), indent=2)
    print(f"-> {out}")
    return 0 if res["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
