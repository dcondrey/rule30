"""Weight-matched random null at m=4: Hamming weight 9, matching Rule 30's
offset-0 truth table 1101110011000101, so the comparison is not partly a
measurement of table density."""
import json, random
from synth import k_min
rng = random.Random(30_2026)
ks = []
for i in range(60):
    idx = rng.sample(range(16), 9)
    tt = [1 if t in idx else 0 for t in range(16)]
    k, _ = k_min(tt, 4, kmax=7)
    ks.append(k)
    print(i, k, flush=True)
ks.sort()
json.dump({"weight": 9, "n": len(ks), "sorted": ks,
           "median": ks[len(ks)//2]}, open("null_weight9_m4.json", "w"), indent=1)
print("median", ks[len(ks)//2])
