"""Fit log(fuel) against log(n) across the sealed per-band reports."""
import glob, json, math, re, sys

rows = {}
for path in sorted(glob.glob("report-*.json")):
    m = re.match(r"report-(\d+)-(\d+)\.json", path)
    lo, hi = int(m.group(1)), int(m.group(2))
    if hi - lo != 64:
        continue
    d = json.load(open(path))
    n = (lo + hi - 1) / 2
    rows.setdefault("naive", {})[n] = d["baseline_value"]
    for t in d["trials"]:
        if t["eligible"]:
            rows.setdefault(t["candidate_id"], {})[n] = t["primary_value"]


def fit(pts):
    xs = [math.log(n) for n in pts]
    ys = [math.log(f) for f in pts.values()]
    k = len(xs)
    mx, my = sum(xs) / k, sum(ys) / k
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    a = num / den
    ss = sum((y - my) ** 2 for y in ys)
    res = sum((y - (my + a * (x - mx))) ** 2 for x, y in zip(xs, ys))
    return a, 1 - res / ss if ss else float("nan")


for name, pts in rows.items():
    a, r2 = fit(pts)
    per = {int(n): f"{v/64:.3g}" for n, v in sorted(pts.items())}
    print(f"{name:12s} alpha_hat={a:.4f} R2={r2:.5f}  fuel/case={per}")
