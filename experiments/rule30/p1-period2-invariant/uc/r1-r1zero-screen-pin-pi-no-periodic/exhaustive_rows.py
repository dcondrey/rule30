"""TEST 3 (exhaustive finite left data) for (PIN-Pi).

Any counterexample (y, c = prefix + w^inf) passes at time L through a row R (the left half-plane at time L,
width(y) + L bits since the left edge moves one cell per step) from which the drive is purely periodic; and
any finite row R is itself admissible initial data (y = R, c_0 = R & 1).  So the lemma restricted to pure
periodic drives and initial data of width exactly W is decided by testing every row R in [2^(W-1), 2^W)
against every phase of w matching R & 1.  This is the complete finite slice of the lemma, exhaustive in y
rather than in the pin-consistent prefix.  FAILURE = any row reaching the cap.

usage: exhaustive_rows.py Wmin Wmax cap tails(comma) [workers]
"""
import sys, time, math
from collections import Counter
from multiprocessing import get_context
sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero-screen-pin-pi-no-periodic')
from lhp_lib import tail_survival, periodic_tail

SPECS = None
CAP = None

def work(args):
    lo, hi = args
    tails = {}
    for spec in SPECS:
        w = [int(ch) for ch in spec]
        tails[spec] = [(ph, periodic_tail(w, ph, CAP + 2)) for ph in range(len(w))]
    hists = {spec: Counter() for spec in SPECS}
    best = {spec: (-1, None, None) for spec in SPECS}
    for row in range(lo, hi):
        b0 = row & 1
        for spec, tl in tails.items():
            h = hists[spec]
            for ph, tail in tl:
                if tail[0] != b0:
                    continue
                s = tail_survival(row, tail, CAP)
                h[s] += 1
                if s > best[spec][0]:
                    best[spec] = (s, row, ph)
    return hists, best

def main():
    global SPECS, CAP
    Wmin = int(sys.argv[1]); Wmax = int(sys.argv[2]); CAP = int(sys.argv[3])
    SPECS = sys.argv[4].split(',')
    workers = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    jsonpath = sys.argv[6] if len(sys.argv) > 6 else None
    out = [f"W={Wmin}..{Wmax} cap={CAP} tails={SPECS} workers={workers}"]
    t0 = time.time()
    allhist = {spec: {} for spec in SPECS}
    with get_context('fork').Pool(workers) as pool:
        for W in range(Wmin, Wmax + 1):
            lo, hi = (0, 1) if W == 0 else (1 << (W - 1), 1 << W)
            nchunk = max(1, min(workers * 16, (hi - lo) // 256))
            step = (hi - lo + nchunk - 1) // nchunk
            chunks = [(a, min(a + step, hi)) for a in range(lo, hi, step)]
            hists = {spec: Counter() for spec in SPECS}
            best = {spec: (-1, None, None) for spec in SPECS}
            for h, b in pool.imap_unordered(work, chunks):
                for spec in SPECS:
                    hists[spec].update(h[spec])
                    if b[spec][0] > best[spec][0]:
                        best[spec] = b[spec]
            line = [f"W={W} rows={hi-lo}"]
            for spec in SPECS:
                h = hists[spec]
                allhist[spec][W] = dict(h)
                n = sum(h.values())
                mx = max(h) if h else 0
                # alive at width W: residues in [0, 2^W) whose first W-1 steps are violation-free; these are the
                # only rows whose survival is not yet decided by their low W bits (light cone: step k reads bits <= k+1)
                alive = sum(v for W2, h2 in allhist[spec].items() for k, v in h2.items() if k >= W - 1)
                band_alive = sum(v for k, v in h.items() if k >= W - 1)
                w = [int(ch) for ch in spec]
                null_steps = math.log2(max(n, 2)) / (sum(w) / len(w))
                bs, brow, bph = best[spec]; brow = brow if brow is not None else 0
                marks = [s for s in (8, 16, 24, 32, 48, 64) if s <= mx]
                surv = " ".join(f"{s}:{sum(v for k, v in h.items() if k >= s)}" for s in marks)
                line.append(f"  {spec}: tests={n} max={mx} atcap={h[CAP]} alive(S>=W-1, all residues<2^W)={alive} band_alive={band_alive} null~{null_steps:.0f} ratio={mx/null_steps:.2f} surv>=s {surv} witness row=0x{brow:x} ph={bph}")
            out.append("\n".join(line))
            print(out[-1], flush=True)
    out.append(f"elapsed {time.time()-t0:.1f}s")
    print(out[-1])
    if jsonpath:
        import json
        json.dump(allhist, open(jsonpath, 'w'))

if __name__ == '__main__':
    main()
