"""Is the per-witness extension test a valid instrument?  Decided by control.

The rule-90 ladder at w = 0 (its TRUE eventually-zero centre column) is a case
where the answer is known: the true rule-90 lone-seed letter word is a genuine,
fully realizable member of the language, and extend_probe's control shows it
survives leftward extension to depth 24.

So if the lasso sampler is a valid instrument, it should be able to find words
of that quality in the rule-90 language.  This file checks two things:

  1. MEMBERSHIP.  Thread the true lone-seed letter word through the ladder's own
     `successors` relation with the Buchi phase and the Diff_q gadget live, and
     confirm it is accepted (a run exists that commits to the periodic tail and
     keeps producing diff events).  This is stronger than rung 0's safety
     regression, which held phase at None and never entered the accepting part
     of the automaton.
  2. REACH GAP.  Compare the leftward depth reached by the true word against the
     best depth reached by any sampled lasso.

If (1) holds and (2) shows a large gap, the sampler cannot find a genuine word
even when one is present, and no conclusion about Rule 30 may be drawn from the
fact that its sampled witnesses are spurious.
"""

from __future__ import annotations

import argparse
import json
import random

import extend_probe as EP

L = EP.L
Params = EP.Params


def accepts_word(P: Params, letters):
    """Does some run of the ladder automaton accept this finite letter word?

    Subset simulation over the nondeterministic `successors` relation, carrying
    with each state the letter index at which its run COMMITTED to the periodic
    tail (phase left None).  Reporting only "some committed run survives" is
    meaningless on a finite word: a run that commits two letters before the end
    always survives.  The load-bearing number is the EARLIEST commit index still
    alive at the end -- a run committed at index m and alive at index T asserts
    that col_0 is w-periodic on the whole of [m, T].

    `onset_direct` recomputes the same thing straight from the derived centre
    column, with no automaton, as an independent check on the above.
    """
    memo: dict = {}
    cur = {(((), 0, None, None, False), None)}
    safety_fail_at = None
    for i, letter in enumerate(letters):
        nxt = set()
        for st, born in cur:
            for ns in L.successors(st, letter, P, memo):
                b = born
                if b is None and ns[2] is not None:
                    b = i
                nxt.add((ns, b))
        if not nxt:
            safety_fail_at = i
            break
        cur = nxt
    alive_commits = [b for _, b in cur if b is not None]
    return {
        "safety_survived": safety_fail_at is None,
        "safety_fail_at": safety_fail_at,
        "n_letters": len(letters),
        "earliest_surviving_commit": min(alive_commits) if alive_commits else None,
        "n_states_final": len(cur),
        "onset_direct": onset_direct(P, letters),
    }


def onset_direct(P: Params, letters):
    """Smallest m with col_0(t) == w[(t-m) mod p] for every t in [m, T), or None.

    Computed from the derived centre column alone, independent of the automaton.
    """
    cols = EP.derive_deep(letters, P.right_depth, P.right_depth, P.rule)
    c = cols.get(0, [])
    w = P.period_word
    p = len(w)
    for m in range(len(c)):
        if all(c[t] == w[(t - m) % p] for t in range(m, len(c))):
            return m
    return None


def diff_events(P: Params, letters):
    """Count genuine Diff_q events on col_{-1} of the derived word."""
    cols = EP.derive_deep(letters, P.right_depth, P.right_depth + 1, P.rule)
    m1 = cols.get(-1, [])
    q = P.diff_q or 1
    return sum(1 for t in range(len(m1) - q) if m1[t] != m1[t + q]), len(m1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-R", type=int, default=2)
    ap.add_argument("--kmax", type=int, default=5)
    ap.add_argument("-n", type=int, default=60)
    ap.add_argument("-D", type=int, default=24)
    ap.add_argument("-T", type=int, default=400)
    ap.add_argument("--seed", type=int, default=20260905)
    args = ap.parse_args()

    out = {"args": vars(args), "cases": []}
    cases = [
        ("rule90_control", 90, "0", 1),
        ("rule30_p2", 30, "01", 1),
    ]
    for name, rule, w, q in cases:
        for k in range(1, args.kmax + 1):
            P = Params(rule=rule, right_depth=args.R, left_depth=k,
                       period_word=tuple(int(c) for c in w), diff_q=q)
            letters = EP.true_word(rule, args.R, args.T)
            acc = accepts_word(P, letters)
            nd, nlen = diff_events(P, letters)
            d_true, det_true = EP.left_reach(letters, args.R, rule, args.D)
            rng = random.Random(args.seed + 7 * k)
            try:
                lassos = EP.sample_lassos(P, args.n, rng)
                best = -1
                Tl = args.R + 2 * args.D + 80
                for wt in lassos:
                    wd = EP.lasso_word(wt["prefix"], wt["cycle"], Tl)
                    d, _ = EP.left_reach(wd, args.R, rule, args.D)
                    best = max(best, d)
                nsamp = len(lassos)
                pref = min(len(wt["prefix"]) for wt in lassos)
            except AssertionError as e:
                best, nsamp, pref = None, 0, None
                acc["language"] = str(e)
            row = {
                "case": name, "rule": rule, "w": w, "q": q, "R": args.R, "k": k,
                "true_word_membership": acc,
                "true_word_diff_events": nd,
                "true_word_col_-1_len": nlen,
                "true_word_left_depth": d_true,
                "true_word_left_detail": det_true,
                "sampled_best_left_depth": best,
                "n_sampled": nsamp,
                "min_sampled_prefix_len": pref,
            }
            out["cases"].append(row)
            print(json.dumps(row), flush=True)

    with open(f"sampler_validity_R{args.R}.json", "w") as f:
        json.dump(out, f, indent=1)
    print("written", f"sampler_validity_R{args.R}.json")


if __name__ == "__main__":
    main()
