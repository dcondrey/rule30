import json
from fission import (rule30, simulate, substitute_column0, UnionFind)

STEPS = 300
HALF_WIDTH = 320

def component_membership(diagram, half_width):
    """Return dict: component root -> list of (t, x) cells (x = signed offset)."""
    uf = UnionFind()
    W = len(diagram[0])
    ones = []
    for t, row in enumerate(diagram):
        for i, v in enumerate(row):
            if v:
                ones.append((t, i))
                uf.find((t, i))
    for t in range(1, len(diagram)):
        row, prev = diagram[t], diagram[t - 1]
        for i, v in enumerate(row):
            if not v:
                continue
            for j in (i - 1, i, i + 1):
                if 0 <= j < W and prev[j]:
                    uf.union((t - 1, j), (t, i))
    comps = {}
    for (t, i) in ones:
        r = uf.find((t, i))
        comps.setdefault(r, []).append((t, i - half_width))
    return comps


def summarize(diagram, half_width, label):
    comps = component_membership(diagram, half_width)
    sizes = sorted((len(v) for v in comps.values()), reverse=True)
    # spatial extent of every non-dominant component
    biggest = max(comps.values(), key=len)
    others = [v for v in comps.values() if v is not biggest]
    x_ranges = []
    t_ranges = []
    for v in others:
        xs = [x for (t, x) in v]
        ts = [t for (t, x) in v]
        x_ranges.append((min(xs), max(xs)))
        t_ranges.append((min(ts), max(ts)))
    max_abs_x = max((max(abs(a), abs(b)) for a, b in x_ranges), default=0)
    print(f"--- {label} ---")
    print(f"n_components={len(comps)}, dominant_size={len(biggest)}, "
          f"other_sizes={sizes[1:] if len(sizes)>1 else []}")
    print(f"max |x| reached by any non-dominant component: {max_abs_x}")
    print(f"non-dominant x-ranges: {x_ranges}")
    print(f"non-dominant t-ranges: {t_ranges}")
    return dict(n_components=len(comps), dominant_size=len(biggest),
                other_sizes=sizes[1:] if len(sizes) > 1 else [],
                max_abs_x_nondominant=max_abs_x,
                x_ranges=x_ranges, t_ranges=t_ranges)


base = simulate(rule30, STEPS, HALF_WIDTH)
out = {}
out["baseline"] = summarize(base, HALF_WIDTH, "baseline rule30")
for word_name, word in (("[0,0]_period2", [0, 0]),
                         ("[0,1]_period2", [0, 1]),
                         ("[0,1,1]_period3", [0, 1, 1])):
    d2 = substitute_column0(base, HALF_WIDTH, word)
    out[word_name] = summarize(d2, HALF_WIDTH, word_name)

with open("component_locality.json", "w") as f:
    json.dump(out, f, indent=2)
