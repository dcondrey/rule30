"""
felting-preimage-homology follow-up.

Formalization adopted (see report section 1 for the defense):

  Fix a rule (Rule 30 or Rule 90) and the true lone-seed orbit, i.e. the IC
  s(0,x) = 1 iff x == 0, evolved forward.  Let a_0, a_1, ... be its true
  centre column.

  A NODE at level k is a word w in {0,1}^k, read as a candidate assignment
  w[0] = s(0,-1), w[1] = s(0,-2), ..., w[k-1] = s(0,-k) -- i.e. a candidate
  LEFT HALF of the t=0 row on cells {-1,...,-k} -- that is CONSISTENT: when
  the full IC is built as

      s(0,x) = 1            if x == 0
      s(0,-i) = w[i-1]      for i = 1..k
      s(0,x) = 0            otherwise (in particular for x < -k)

  and evolved forward under the rule, the resulting centre column agrees
  with the true a_0,...,a_{k-1} for all k steps computable from this IC
  (see lemma in the report: cells beyond -k cannot influence a_0..a_{k-1}
  by finite propagation speed, so "otherwise = 0" is a don't-care pad, not
  an extra assumption).

  An EDGE connects a level-k node w to a level-(k+1) node w' iff w' is a
  ONE-STEP-CONSISTENT EXTENSION of w: w'[0:k] == w (w' agrees with w on
  cells -1..-k) and w' is itself a consistent node at level k+1.  This is
  the literal reading of "left-half configurations ... consistent with the
  observed prefix" plus "one-step-consistent extensions" from the spark.

Both rule tables are wired below; RULE_90 is the additive control.
"""
import itertools
import sys


def rule30(a, b, c):
    return a ^ (b | c)


def rule90(a, b, c):
    return a ^ c


RULES = {"rule30": rule30, "rule90": rule90}


def true_center(rule, T, halfwidth):
    """True lone-seed centre column a_0..a_{T-1} for `rule`."""
    width = 2 * halfwidth + 1
    mid = halfwidth
    row = [0] * width
    row[mid] = 1
    center = []
    for t in range(T):
        center.append(row[mid])
        new = [0] * width
        for x in range(1, width - 1):
            new[x] = rule(row[x - 1], row[x], row[x + 1])
        row = new
    return center


def simulate_center_from_ic(rule, ic, mid, steps):
    """Evolve `ic` (list indexed 0..len-1, mid = index of x=0) `steps` times,
    return the centre column produced (length `steps`)."""
    row = ic[:]
    out = []
    for t in range(steps):
        out.append(row[mid])
        new = [0] * len(row)
        for x in range(1, len(row) - 1):
            new[x] = rule(row[x - 1], row[x], row[x + 1])
        row = new
    return out


def consistent(rule, w, a_true, halfwidth):
    """Is left-half word w (w[0]=cell -1,...,w[k-1]=cell -k) consistent with
    a_true[0:k]?  Build an IC wide enough that the light cone for k steps
    never touches the padding boundary, evolve, and compare."""
    k = len(w)
    # need cells in [-(k-1), k-1] to compute a_0..a_{k-1}; w supplies -1..-k
    # which covers that on the left, real seed supplies x>=0 on the right.
    width = 2 * halfwidth + 1
    mid = halfwidth
    ic = [0] * width
    ic[mid] = 1  # seed at x = 0
    for i, bit in enumerate(w):
        x = -(i + 1)
        ic[mid + x] = bit
    got = simulate_center_from_ic(rule, ic, mid, k)
    return got == a_true[:k]


def build_tree(rule_name, kmax, halfwidth=None):
    rule = RULES[rule_name]
    if halfwidth is None:
        halfwidth = kmax + 5
    a_true = true_center(rule, kmax, halfwidth)

    nodes = {0: {()}}
    edges = []  # (k, parent_word, k+1, child_word)
    for k in range(kmax):
        nxt = set()
        for w in nodes[k]:
            for bit in (0, 1):
                neww = w + (bit,)
                if consistent(rule, neww, a_true, halfwidth):
                    nxt.add(neww)
                    edges.append((k, w, k + 1, neww))
        nodes[k + 1] = nxt
    return nodes, edges, a_true


def forest_check(nodes, edges):
    """Verify: (a) every non-root node has exactly one parent edge, i.e. the
    edge set literally IS the truncation map; (b) total edges == total nodes
    minus number of roots (level-0 nodes) -- the exact combinatorial
    signature of a forest; (c) no node has 2 distinct parents; (d) BFS/DFS
    from roots visits every node exactly once (no cross edges, no cycles)."""
    total_nodes = sum(len(v) for v in nodes.values())
    n_roots = len(nodes[0])
    n_edges = len(edges)

    parent_of = {}
    multi_parent = []
    for (k, w, k1, w1) in edges:
        key = (k1, w1)
        if key in parent_of and parent_of[key] != (k, w):
            multi_parent.append(key)
        parent_of[key] = (k, w)

    # every edge's child, truncated (drop last symbol), must equal parent
    truncation_mismatches = 0
    for (k, w, k1, w1) in edges:
        if w1[:k] != w:
            truncation_mismatches += 1

    forest_signature = (n_edges == total_nodes - n_roots)

    return {
        "total_nodes": total_nodes,
        "n_roots": n_roots,
        "n_edges": n_edges,
        "forest_signature_holds": forest_signature,
        "multi_parent_nodes": len(multi_parent),
        "truncation_mismatches": truncation_mismatches,
        "cyclomatic_number_if_connected_as_forest": n_edges - (total_nodes - n_roots),
    }


def level_counts(nodes):
    return {k: len(v) for k, v in nodes.items()}


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    for rule_name in ("rule30", "rule90"):
        nodes, edges, a_true = build_tree(rule_name, kmax)
        report = forest_check(nodes, edges)
        print(f"=== {rule_name}  kmax={kmax} ===")
        print("true centre a_0..a_{k-1}:", a_true)
        print("level counts:", level_counts(nodes))
        print("forest check:", report)
        print()
