"""Summarise exhaustive_rows histograms: per tail and width W, max survival, excess max_S - W, alive count
(residues < 2^W with S >= W-1) and its growth ratio, plus the count of width-W rows with S >= W + 8.
usage: analyse_excess.py hist.json"""
import sys, json, math
H = json.load(open(sys.argv[1]))
for spec, byW in H.items():
    print(f"tail {spec}")
    print("  W  maxS  excess=maxS-W  alive  alive_ratio  log2(alive)/W  band rows with S>=W+8")
    prev = None
    cum = {}
    for W in sorted(byW, key=int):
        h = {int(k): v for k, v in byW[W].items()}
        Wi = int(W)
        cum[Wi] = h
        mx = max(h) if h else 0
        alive = sum(v for W2, h2 in cum.items() for k, v in h2.items() if k >= Wi - 1)
        deep = sum(v for k, v in h.items() if k >= Wi + 8)
        ratio = f"{alive/prev:.2f}" if prev else "-"
        print(f"  {Wi:2d}  {mx:4d}  {mx-Wi:5d}        {alive:7d}  {ratio:>5}  {math.log2(max(alive,1))/max(Wi,1):.3f}  {deep}")
        prev = alive
