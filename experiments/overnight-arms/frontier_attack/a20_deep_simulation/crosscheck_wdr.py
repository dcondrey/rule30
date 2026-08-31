"""Cross-check this repo's Rule 30 centre-column generators against the two
published sources: Wolfram's 10^9-bit dataset and the OEIS b-file for A051023.

PATH.md 8.5 records this check as open, cheap and never performed by anyone.

The Wolfram Data Repository resource
    A-Billion-Bits-of-the-Center-Column-of-the-Rule-30-Cellular-Automaton
    uuid 368ea1f8-e51f-468a-aac7-06de2d6f94cc
is served as a Wolfram Language .mx DumpSave container, 125,000,345 bytes:
a 239-byte header, the 125,000,000-byte payload, and a 106-byte trailer.
Fetch it with no Wolfram Engine at

    curl -L -o ref/wdr_billion.bin \
      https://datarepository.wolframcloud.com/api/1.0/resources/368ea1f8-e51f-468a-aac7-06de2d6f94cc

The payload offset and bit order are NOT hardcoded here.  They are re-derived
on every run by matching the first 64 bits against A051023, and the derivation
must be unique -- that is what makes a reported match mean something.  A tool
that assumed the alignment could report agreement produced by the assumption.

Two packings are in play in this tree and they differ:
  deep_gen.py       MSB-first within each byte  (`0x80 >> (i % 8)`)
  modal_run_band.py LSB-first, uint32 LE        (step i = bit (i&31) of word i>>5)
The Wolfram payload is MSB-first, same as deep_gen.py.

Usage:
    uv run --with numpy python crosscheck_wdr.py --self-test
    uv run --with numpy python crosscheck_wdr.py \
        --cpu depth24h_column.bin --gpu band_n3000000000_w4_col+0.bin
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "ref")

WDR_UUID = "368ea1f8-e51f-468a-aac7-06de2d6f94cc"
WDR_BITS = 1_000_000_000
SEARCH_BYTES = 700          # header is 239; a generous window with room to spare

# A051023 (centre column of Rule 30 from a single 1), t = 0..63.
A051023_64 = np.array([
    1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1,
    0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1,
    0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0,
    1, 0, 1, 1,
], dtype=np.uint8)


# ---------------------------------------------------------------- unpacking

def unpack(buf: np.ndarray, order: str, count: int | None = None) -> np.ndarray:
    """Bits of `buf` in stream order under `order` ('msb' or 'lsb')."""
    bits = np.unpackbits(buf, bitorder="big" if order == "msb" else "little")
    return bits if count is None else bits[:count]


def find_alignment(blob: np.ndarray, want: np.ndarray = A051023_64):
    """Every (offset, order) in the search window whose bits start with `want`.

    Returned as a list so the caller can insist the answer is unique; a second
    hit would mean the prefix is too short to pin the alignment.
    """
    need = (len(want) + 7) // 8
    hits = []
    for off in range(min(SEARCH_BYTES, len(blob) - need + 1)):
        win = blob[off:off + need]
        for order in ("msb", "lsb"):
            if np.array_equal(unpack(win, order, len(want)), want):
                hits.append((off, order))
    return hits


# ---------------------------------------------------------------- comparison

def first_diff(a: np.ndarray, b: np.ndarray) -> int | None:
    """Index of the first disagreement, or None. Both are 0/1 bit arrays."""
    d = np.flatnonzero(a != b)
    return int(d[0]) if d.size else None


def compare_bits(name: str, ours: np.ndarray, ref: np.ndarray) -> dict:
    n = min(len(ours), len(ref))
    ours, ref = ours[:n], ref[:n]
    idx = first_diff(ours, ref)
    r = {"name": name, "bits_compared": n, "match": idx is None}
    if idx is not None:
        lo = max(0, idx - 8)
        r["first_diff_bit"] = idx
        r["ours_window"] = ours[lo:idx + 8].tolist()
        r["ref_window"] = ref[lo:idx + 8].tolist()
        r["n_diff"] = int((ours != ref).sum())
    return r


def load_column(path: str, order: str, max_bits: int) -> np.ndarray:
    """Bits from a packed column file, capped at `max_bits`."""
    nbytes = min(os.path.getsize(path), (max_bits + 7) // 8)
    buf = np.fromfile(path, dtype=np.uint8, count=nbytes)
    return unpack(buf, order, min(max_bits, nbytes * 8))


def load_bfile(path: str) -> np.ndarray:
    vals = []
    with open(path) as fh:
        for ln in fh:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            i, v = ln.split()
            if int(i) != len(vals):
                raise ValueError(f"b-file index gap: expected {len(vals)}, got {i}")
            vals.append(int(v))
    return np.array(vals, dtype=np.uint8)


# ---------------------------------------------------------------- self-test

def self_test() -> int:
    """Pins the two bit-order conventions and the alignment search.

    These are the failure modes that would silently turn a real disagreement
    into a reported match, so they are the part worth a test.
    """
    # 0x80 is bit 0 under MSB-first, bit 7 under LSB-first.
    b = np.array([0x80], dtype=np.uint8)
    assert unpack(b, "msb").tolist() == [1, 0, 0, 0, 0, 0, 0, 0]
    assert unpack(b, "lsb").tolist() == [0, 0, 0, 0, 0, 0, 0, 1]

    # deep_gen.py's packing loop, reproduced, must round-trip as 'msb'.
    want = A051023_64
    pend = bytearray(8)
    for i, bit in enumerate(want):
        if bit:
            pend[i // 8] |= 0x80 >> (i % 8)
    assert np.array_equal(unpack(np.frombuffer(bytes(pend), dtype=np.uint8),
                                 "msb", 64), want), "deep_gen packing != msb"

    # modal_run_band.py's packing, reproduced, must round-trip as 'lsb'.
    words = np.zeros(2, dtype="<u4")
    for i, bit in enumerate(want):
        if bit:
            words[i >> 5] |= np.uint32(1) << np.uint32(i & 31)
    assert np.array_equal(unpack(words.view(np.uint8), "lsb", 64), want), \
        "modal_run_band packing != lsb"

    # A synthetic blob: junk header, msb payload, junk trailer. The search must
    # find the planted offset and must find it exactly once.
    rng = np.random.default_rng(30)
    payload = np.packbits(np.concatenate(
        [want, rng.integers(0, 2, 4096, dtype=np.uint8)]), bitorder="big")
    for planted in (0, 1, 239, 500):
        blob = np.concatenate([rng.integers(0, 256, planted, dtype=np.uint8),
                               payload,
                               rng.integers(0, 256, 106, dtype=np.uint8)])
        hits = find_alignment(blob)
        assert (planted, "msb") in hits, f"missed planted offset {planted}"
        assert len(hits) == 1, f"offset {planted}: non-unique alignment {hits}"

    # first_diff must actually fire, not just return None on everything.
    a = want.copy()
    c = want.copy()
    c[37] ^= 1
    assert first_diff(a, c) == 37
    assert first_diff(a, a) is None
    assert compare_bits("x", a, c)["match"] is False
    assert compare_bits("x", a, a)["match"] is True

    print("self-test OK: bit orders pinned, alignment search unique, diff fires")
    return 0


# ---------------------------------------------------------------- main

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--wdr", default=os.path.join(REF, "wdr_billion.bin"))
    p.add_argument("--bfile", default=os.path.join(REF, "b051023.txt"))
    p.add_argument("--cpu", help="deep_gen.py column (MSB-first packing)")
    p.add_argument("--gpu", help="modal_run_band.py centre column (LSB-first uint32 LE)")
    p.add_argument("--out", default=os.path.join(HERE, "crosscheck_wdr_result.json"))
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()

    if a.self_test:
        return self_test()

    res: dict = {"wdr_uuid": WDR_UUID, "comparisons": []}

    if not os.path.exists(a.wdr):
        print(f"missing {a.wdr}\nfetch: curl -L -o {a.wdr} \\\n"
              f"  https://datarepository.wolframcloud.com/api/1.0/resources/{WDR_UUID}",
              file=sys.stderr)
        return 2

    blob = np.fromfile(a.wdr, dtype=np.uint8)
    res["wdr_container_bytes"] = int(len(blob))

    hits = find_alignment(blob)
    res["alignment_hits"] = [{"offset": o, "order": r} for o, r in hits]
    if len(hits) != 1:
        print(f"FAIL: alignment not unique in first {SEARCH_BYTES} bytes: {hits}",
              file=sys.stderr)
        json.dump(res, open(a.out, "w"), indent=2)
        return 1
    off, order = hits[0]
    print(f"WDR alignment: byte offset {off}, {order}-first  (re-derived, unique)")

    nbytes = WDR_BITS // 8
    if off + nbytes > len(blob):
        print(f"FAIL: container too short for {WDR_BITS:,} bits from offset {off}",
              file=sys.stderr)
        return 1
    pay = blob[off:off + nbytes]
    res.update(payload_offset=off, payload_order=order,
               payload_bytes=int(nbytes),
               trailer_bytes=int(len(blob) - off - nbytes),
               payload_sha256=hashlib.sha256(pay.tobytes()).hexdigest(),
               payload_ones=int(np.unpackbits(pay).sum()))
    res["payload_density"] = res["payload_ones"] / WDR_BITS
    print(f"  payload {nbytes:,} bytes  sha256 {res['payload_sha256']}")
    print(f"  ones {res['payload_ones']:,}/{WDR_BITS:,}  "
          f"density {res['payload_density']:.9f}")

    def add(r):
        res["comparisons"].append(r)
        status = "MATCH" if r["match"] else f"MISMATCH at bit {r['first_diff_bit']:,}"
        print(f"  {r['name']:<38} {r['bits_compared']:>15,} bits  {status}")

    print("\ncomparisons against the WDR payload:")
    if os.path.exists(a.bfile):
        bf = load_bfile(a.bfile)
        add(compare_bits(f"OEIS b-file {os.path.basename(a.bfile)}", bf,
                         unpack(pay[:(len(bf) + 7) // 8], order, len(bf))))
    if a.cpu:
        cpu = load_column(a.cpu, "msb", WDR_BITS)
        add(compare_bits(f"deep_gen.py {os.path.basename(a.cpu)}", cpu,
                         unpack(pay[:(len(cpu) + 7) // 8], order, len(cpu))))
    if a.gpu:
        gpu = load_column(a.gpu, "lsb", WDR_BITS)
        add(compare_bits(f"band GPU {os.path.basename(a.gpu)}", gpu,
                         unpack(pay[:(len(gpu) + 7) // 8], order, len(gpu))))

    res["all_match"] = all(c["match"] for c in res["comparisons"])
    res["n_comparisons"] = len(res["comparisons"])
    json.dump(res, open(a.out, "w"), indent=2)
    print(f"\n{'ALL MATCH' if res['all_match'] else 'DISAGREEMENT'}"
          f" over {res['n_comparisons']} comparison(s) -> {a.out}")
    return 0 if res["all_match"] else 1


if __name__ == "__main__":
    sys.exit(main())
