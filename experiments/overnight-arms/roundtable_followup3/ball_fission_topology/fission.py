"""
ball-fission-topology followup: precise definitions, premise check, and the
pre-registered single-column-blindness kill test.

Two independent, precisely-specified readings of "connected component of
1-cells in the backward light cone" are implemented, because the spark text
under-specifies which one is meant (same failure mode as the gauge-holonomy
followup's kappa(x,t) ambiguity):

  READING 1 (causal-edge graph, cell-level).  Build a graph G on every
  1-valued lattice site (t,x). Add an edge (t,x)-(t+1,x') whenever
  |x-x'|<=1 AND diagram[t][x]==1 AND diagram[t+1][x']==1 (i.e. an actual
  1->1 causal dependency edge of the radius-1 rule). "The connected
  component of cell c=(t0,x0) in its backward light cone" = the connected
  component containing c in the induced subgraph restricted to time<=t0.
  This is the literal, no-slack reading of the spark's own words.

  READING 2 (same-row spatial run / domain tracking).  At each time t,
  identify maximal runs (intervals) of consecutive 1s in that row. Track
  runs across time via causal-footprint overlap. A "fission" event is a
  run at time t whose causal footprint touches >=2 runs at time t+1 that
  are not touched by any other run at time t (a clean 1-parent split); a
  "merge" event is symmetric (>=2 parent runs feeding one child run); an
  "annihilation" event is a run with zero children. This is the more
  charitable, "domain wall" reading that could in principle show a real
  rule30/rule90 asymmetry, and it is the reading actually exercised by
  the annihilation-vs-fission language in the spark.

Both are computed for real Rule 30 and Rule 90 lone-seed diagrams, then
both are run through the pre-registered single-column-blindness gate.
"""
import json
import sys
from dataclasses import dataclass


def rule30(a, b, c):
    return a ^ (b | c)


def rule90(a, b, c):
    return a ^ c


def simulate(rule, steps, half_width):
    """Lone-seed diagram, columns indexed -half_width..half_width (offset
    stored as list index = x + half_width). Returns list of rows (lists of
    0/1), row t = time t, t = 0..steps inclusive."""
    W = 2 * half_width + 1
    row = [0] * W
    row[half_width] = 1  # seed at x=0
    diagram = [row[:]]
    for t in range(steps):
        new = [0] * W
        for i in range(W):
            a = row[i - 1] if i - 1 >= 0 else 0
            b = row[i]
            c = row[i + 1] if i + 1 < W else 0
            new[i] = rule(a, b, c)
        diagram.append(new)
        row = new
    return diagram  # diagram[t][i], x = i - half_width


# ---------------------------------------------------------------------
# READING 1: causal-edge connected components (union-find, incremental)
# ---------------------------------------------------------------------

class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        p = self.parent.setdefault(x, x)
        while p != x:
            self.parent[x] = self.parent.get(p, p)
            x, p = p, self.parent.get(p, p)
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb
            return True
        return False


def causal_component_trace(diagram, half_width):
    """For a diagram, build the causal 1-1 edge graph incrementally row by
    row and return, for each time t, the number of distinct connected
    components among all 1-cells with time <= t (cumulative), plus whether
    any *new* isolated singleton component ever appears after t=0 that is
    not immediately merged by the very next row (a literal fission
    candidate under Reading 1)."""
    uf = UnionFind()
    W = len(diagram[0])
    n_components_over_time = []
    ones_seen = set()
    for t, row in enumerate(diagram):
        for i, v in enumerate(row):
            if v:
                ones_seen.add((t, i))
                uf.find((t, i))
        if t > 0:
            prev = diagram[t - 1]
            for i, v in enumerate(row):
                if not v:
                    continue
                for j in (i - 1, i, i + 1):
                    if 0 <= j < W and prev[j]:
                        uf.union((t - 1, j), (t, i))
        # count distinct roots among ones_seen so far
        roots = set(uf.find(node) for node in ones_seen)
        n_components_over_time.append(len(roots))
    return n_components_over_time


def verify_every_one_has_a_parent(diagram, rule_name):
    """Structural lemma check: for t>=1, every 1-valued output cell has at
    least one 1-valued causal parent among {x-1,x,x+1} at t-1. This is what
    forces Reading-1 connectivity back to the single seed. Returns the
    count of counterexamples (should be 0 for OR-rules and XOR-rules of
    this exact radius-1 form, by the algebra below)."""
    W = len(diagram[0])
    violations = 0
    for t in range(1, len(diagram)):
        row, prev = diagram[t], diagram[t - 1]
        for i, v in enumerate(row):
            if not v:
                continue
            has_parent = any(
                0 <= j < W and prev[j] for j in (i - 1, i, i + 1)
            )
            if not has_parent:
                violations += 1
    return violations


# ---------------------------------------------------------------------
# READING 2: same-row run tracking (domains / fission / merge / annihilate)
# ---------------------------------------------------------------------

def find_runs(row):
    runs = []
    start = None
    for i, v in enumerate(row):
        if v and start is None:
            start = i
        elif not v and start is not None:
            runs.append((start, i - 1))
            start = None
    if start is not None:
        runs.append((start, len(row) - 1))
    return runs


def causal_touch(run_a, run_b):
    """Does run_a's causal footprint (each cell influences x-1..x+1 at the
    next step) overlap run_b's interval?"""
    a0, a1 = run_a
    b0, b1 = run_b
    return not (a1 + 1 < b0 or b1 < a0 - 1)


def run_events(diagram):
    """Returns per-transition-step counts of fission / merge / annihilation
    / simple-continuation events, using causal-footprint touch as the
    parent/child relation between runs(t) and runs(t+1)."""
    fissions = 0
    merges = 0
    annihilations = 0
    plain = 0
    creations = 0
    per_step = []
    for t in range(len(diagram) - 1):
        runs_t = find_runs(diagram[t])
        runs_t1 = find_runs(diagram[t + 1])
        # children of each parent run
        children = {a: [] for a in runs_t}
        parents = {b: [] for b in runs_t1}
        for a in runs_t:
            for b in runs_t1:
                if causal_touch(a, b):
                    children[a].append(b)
                    parents[b].append(a)
        step_fission = 0
        step_merge = 0
        step_annih = 0
        step_plain = 0
        step_creation = 0
        for a in runs_t:
            kids = children[a]
            if len(kids) == 0:
                step_annih += 1
                annihilations += 1
            elif len(kids) >= 2:
                # clean fission: none of these kids has another parent
                clean = all(len(parents[b]) == 1 for b in kids)
                if clean:
                    step_fission += 1
                    fissions += 1
                else:
                    step_plain += 1  # ambiguous, part of a merge tangle
                    plain += 1
            else:
                step_plain += 1
                plain += 1
        for b in runs_t1:
            if len(parents[b]) >= 2:
                step_merge += 1
                merges += 1
            elif len(parents[b]) == 0:
                step_creation += 1
                creations += 1
        per_step.append(dict(t=t, fission=step_fission, merge=step_merge,
                              annihilation=step_annih, plain=step_plain,
                              creation=step_creation,
                              n_runs_t=len(runs_t), n_runs_t1=len(runs_t1)))
    return dict(total_fissions=fissions, total_merges=merges,
                total_annihilations=annihilations, total_plain=plain,
                total_creations=creations, per_step=per_step)


# ---------------------------------------------------------------------
# Kill-condition test: overwrite column 0 only, leave everything else
# ---------------------------------------------------------------------

def substitute_column0(diagram, half_width, period_word):
    d2 = [row[:] for row in diagram]
    p = len(period_word)
    for t, row in enumerate(d2):
        row[half_width] = period_word[t % p]
    return d2


def summarize_run_events(ev):
    return dict(total_fissions=ev["total_fissions"],
                total_merges=ev["total_merges"],
                total_annihilations=ev["total_annihilations"],
                total_creations=ev["total_creations"])


def main():
    STEPS = 300
    HALF_WIDTH = 320  # comfortably beyond light cone reach (<=300)

    results = {}

    diagrams = {}
    for name, rule in (("rule30", rule30), ("rule90", rule90)):
        d = simulate(rule, STEPS, HALF_WIDTH)
        diagrams[name] = d

    # --- Item 2: premise check ---------------------------------------
    premise = {}
    for name, d in diagrams.items():
        violations = verify_every_one_has_a_parent(d, name)
        comp_trace = causal_component_trace(d, HALF_WIDTH)
        ev = run_events(d)
        premise[name] = dict(
            parent_violations=violations,
            reading1_final_component_count=comp_trace[-1],
            reading1_component_trace_sample=comp_trace[::30],
            reading2_events=summarize_run_events(ev),
        )
    results["premise_check"] = premise

    # --- Item 3: kill-condition test on Rule 30 -----------------------
    kill = {}
    base = diagrams["rule30"]
    base_ev = run_events(base)
    base_comp_trace = causal_component_trace(base, HALF_WIDTH)
    kill["baseline"] = dict(
        reading1_final_components=base_comp_trace[-1],
        reading2_events=summarize_run_events(base_ev),
    )

    for word_name, word in (("[0,0]_period2", [0, 0]),
                             ("[0,1]_period2", [0, 1]),
                             ("[0,1,1]_period3", [0, 1, 1])):
        d2 = substitute_column0(base, HALF_WIDTH, word)
        ev2 = run_events(d2)
        comp_trace2 = causal_component_trace(d2, HALF_WIDTH)
        s2 = summarize_run_events(ev2)
        s1 = summarize_run_events(base_ev)
        delta = {k: s2[k] - s1[k] for k in s1}
        kill[word_name] = dict(
            reading1_final_components=comp_trace2[-1],
            reading1_component_delta=comp_trace2[-1] - base_comp_trace[-1],
            reading2_events=s2,
            reading2_delta_from_baseline=delta,
        )
    results["kill_condition_test"] = kill

    # Fraction-of-diagram sensitivity context
    W_full = 2 * HALF_WIDTH + 1
    results["context"] = dict(
        steps=STEPS, half_width=HALF_WIDTH, full_width=W_full,
        column0_fraction_of_columns=1.0 / W_full,
    )

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2)[:4000])
    print("... (full output in results.json)")


if __name__ == "__main__":
    main()
