"""Thm(p) sweep: for every primitive binary necklace w of length p <= PMAX,
decide emptiness of the ladder language (mode i, q=None) and of the Diff_q
tightening (mode ii, q=1).  EMPTY = Thm for that tail word.  Rotations are
equivalent because the Buchi onset is guessed, so one representative per
necklace suffices; imprimitive words are covered by their primitive divisor.
"""
import json, sys, time
from ladder import Params, decide, verify_witness

PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
R = int(sys.argv[2]) if len(sys.argv) > 2 else 2
K = int(sys.argv[3]) if len(sys.argv) > 3 else 2
CAP = 2_000_000

def necklaces(p):
    seen, out = set(), []
    for n in range(1 << p):
        w = tuple((n >> i) & 1 for i in range(p))
        if any(all(w[i] == w[(i + d) % p] for i in range(p)) for d in range(1, p) if p % d == 0):
            continue                      # imprimitive
        rots = frozenset(tuple(w[(i + r) % p] for i in range(p)) for r in range(p))
        if rots in seen:
            continue
        seen.add(rots); out.append(w)
    return out

for p in range(1, PMAX + 1):
    for w in necklaces(p):
        row = {"p": p, "w": "".join(map(str, w))}
        for q in (None, 1):
            P = Params(30, R, K, w, q)
            t0 = time.time()
            r = decide(P, CAP)
            if r["witness"] is not None:
                ok, note = verify_witness(r["witness"]["prefix"], r["witness"]["cycle"], P)
                assert ok, (w, q, note)
            row[f"q{q}"] = r["verdict"]
            row[f"n{q}"] = r["states"]
            row[f"s{q}"] = round(time.time() - t0, 2)
        print(json.dumps(row), flush=True)
