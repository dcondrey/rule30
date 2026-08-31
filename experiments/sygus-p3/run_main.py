"""Main run: k_min for Rule 30's centre column against structured controls
and a random-function null distribution, at fixed m.

Order matters and follows PREREGISTRATION.md section 4: the instrument
kill-check (structured controls vs random median at m=4) runs first.
"""

import json
import random
import sys
import time

from rule30 import truth_table
from synth import k_min, verify_chain

U = {2: 1, 3: 4, 4: 7, 5: 12}


def tt_fn(fn, m):
    return [fn([(t >> (m - 1 - j)) & 1 for j in range(m)]) for t in range(1 << m)]


def controls(m):
    out = {
        "rule30_offset0": truth_table(30, m, 0),
        "rule30_offset1": truth_table(30, m, 1),
        "rule90": truth_table(90, m, 0),
        "rule150": truth_table(150, m, 0),
        "rule60": truth_table(60, m, 0),
        "parity": tt_fn(lambda v: sum(v) % 2, m),
        "and_m": tt_fn(lambda v: int(all(v)), m),
    }
    if m >= 3:
        out["maj3"] = tt_fn(lambda v: int(sum(v[:3]) >= 2), m)
    return out


def measure(name, tt, m, kmax, log):
    t0 = time.time()
    k, trace = k_min(tt, m, kmax=kmax)
    ok = verify_chain(trace[-1].chain, tt, m) if trace and trace[-1].sat else (k == 0)
    rec = {
        "name": name, "m": m, "k_min": k, "verified": ok,
        "total_s": round(time.time() - t0, 3),
        "per_k": [{"k": r.k, "sat": r.sat, "s": round(r.seconds, 3),
                   "clauses": r.n_clauses} for r in trace],
        "tt": "".join(map(str, tt)),
    }
    log.append(rec)
    print(f"  {name:16s} m={m} k_min={k} verified={ok} "
          f"({rec['total_s']}s)", flush=True)
    return k


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    nrand = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    kmax = U.get(m, 20)
    log = []

    print(f"=== m={m} (N={1<<m}), kmax={kmax} ===")
    print("structured controls and target:")
    ks = {}
    for name, tt in controls(m).items():
        ks[name] = measure(name, tt, m, kmax, log)

    print(f"random null distribution, {nrand} seeded samples:")
    rng = random.Random(30_2026)
    rand_ks = []
    for i in range(nrand):
        tt = [rng.randint(0, 1) for _ in range(1 << m)]
        k = measure(f"random_{i:03d}", tt, m, kmax, log)
        rand_ks.append(k)

    rand_ks.sort()
    med = rand_ks[len(rand_ks) // 2]
    tgt = ks["rule30_offset0"]
    below = sum(1 for k in rand_ks if k < tgt)
    eq = sum(1 for k in rand_ks if k == tgt)
    pct = 100.0 * (below + eq / 2) / len(rand_ks)

    summary = {
        "m": m, "kmax": kmax, "controls": ks,
        "random_kmin_sorted": rand_ks, "random_median": med,
        "rule30_percentile_of_random": round(pct, 1),
        "instrument_check": {
            "structured_min": min(ks[n] for n in ("rule90", "rule150", "parity", "and_m")),
            "random_median": med,
        },
    }
    print(json.dumps(summary, indent=2))
    with open(f"results_m{m}.json", "w") as fh:
        json.dump({"summary": summary, "records": log}, fh, indent=1)


if __name__ == "__main__":
    main()
