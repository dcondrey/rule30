"""a19: ML/symbolic mining as a CANDIDATE GENERATOR, with an exact out-of-range check.

DISCIPLINE (restated in the deliverable):
  An accuracy number is NOT a result.  The only legitimate output of this script
  is a PRECISE, FINITE, CHECKABLE candidate rule, exact-checked on a depth range
  DISJOINT FROM AND FAR BEYOND the training range.  Obstruction H means no depth
  ever settles the infinite statement; the exact check can only REFUTE.

DEPTH SPLIT (fixed here, quoted everywhere downstream):
  TRAIN t in [0, 20000)          -- fit / table extraction
  DEV   t in [20000, 50000)      -- in-range holdout, adjacent
  TEST  t in [200000, 1000000)   -- OUT OF RANGE, disjoint, 4x-50x deeper

Extraction methods, all exact and discrete (no black boxes reported as results):
  (1) exact lookup table   : pattern -> unanimous label on TRAIN (a finite-state
                             / boolean candidate by construction)
  (2) decision tree        : sklearn, small depth, then read out as a table
  (3) GF(2) symbolic fit   : exact solve for a polynomial over the feature bits
                             with monomials up to degree d (an ANF candidate)

Run: uv run python mine.py
"""

from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

from substrate import center_column, windows

TRAIN = (0, 20_000)
DEV = (20_000, 50_000)
TEST = (200_000, 500_000)
N = TEST[1]
WMAX = 24


# ---------------------------------------------------------------- feature sets


def build_features(A: np.ndarray, W: int) -> dict:
    """A is (n, 2W+1) with A[t, W+x] = s(t,x).  Returns named bit-matrices."""
    n = A.shape[0]
    c = A[:, W].astype(np.int8)
    return {"A": A, "c": c, "n": n, "W": W}


def col_history(c: np.ndarray, K: int) -> np.ndarray:
    """(n, K) with row t = (c_{t-K+1}, ..., c_t); zero-padded at the start."""
    n = len(c)
    out = np.zeros((n, K), dtype=np.int8)
    for j in range(K):
        out[j:, K - 1 - j] = c[: n - j]
    return out


def left_window(A: np.ndarray, W: int, Wl: int) -> np.ndarray:
    """(n, Wl+1) with row t = (s(t,-Wl), ..., s(t,0))."""
    return A[:, W - Wl : W + 1].astype(np.int8)


def mod_bits(n: int, p: int) -> np.ndarray:
    """(n, ceil(log2 p)) one-hot-free binary encoding of t mod p."""
    r = np.arange(n) % p
    b = max(1, int(np.ceil(np.log2(p))))
    return ((r[:, None] >> np.arange(b)) & 1).astype(np.int8)


def nearest_right_one(A: np.ndarray, W: int) -> np.ndarray:
    """m_t = least j>=1 with s(t,j)=1, capped at W (W means '>= W').

    This is a9's quantity (a9 proved the forced-left-half P_k is a function of m
    ALONE).  Used here only as an INPUT feature, never re-derived.
    """
    n = A.shape[0]
    R = A[:, W + 1 : W + 1 + W]  # s(t,1..W)
    m = np.full(n, W, dtype=np.int16)
    for j in range(W - 1, -1, -1):
        m = np.where(R[:, j] == 1, j + 1, m)
    return m


# ------------------------------------------------------- exact table extraction


def pack(X: np.ndarray) -> np.ndarray:
    """Pack an (n, B) 0/1 matrix into an (n,) int64 code.  B <= 62."""
    B = X.shape[1]
    assert B <= 62, B
    w = (1 << np.arange(B, dtype=np.int64))
    return (X.astype(np.int64) * w).sum(axis=1)


def exact_table(codes: np.ndarray, y: np.ndarray) -> tuple[dict, int, int]:
    """Unanimous-label table over TRAIN.

    Returns (table, n_patterns, n_conflicted).  A pattern with both labels
    observed is 'conflicted' and gets no entry: the candidate rule is only a
    candidate on the unanimous patterns.
    """
    order = np.argsort(codes, kind="stable")
    cs, ys = codes[order], y[order]
    bounds = np.flatnonzero(np.diff(cs)) + 1
    starts = np.concatenate(([0], bounds))
    ends = np.concatenate((bounds, [len(cs)]))
    table: dict[int, int] = {}
    conflicted = 0
    for s, e in zip(starts, ends):
        seg = ys[s:e]
        lo, hi = seg.min(), seg.max()
        if lo == hi:
            table[int(cs[s])] = int(lo)
        else:
            conflicted += 1
    return table, len(starts), conflicted


def check_table(table: dict, codes: np.ndarray, y: np.ndarray, tvals: np.ndarray,
                split: np.ndarray | None = None):
    """Exact check of a candidate table on a disjoint range.

    Returns coverage, error count, and the FIRST t at which a unanimous-on-train
    pattern predicts the wrong label.  If `split` is given (boolean, True = the
    provable PIN CORE `c_t = 1`), the same numbers are also reported separately
    for the core and for the accidental shell `c_t = 0` -- see PREREG Lemma
    A19.1: only the core can be a local-rule consequence.
    """
    empty = {"n": int(len(codes)), "covered": 0, "coverage": 0.0,
             "errors_on_covered": 0, "acc_on_covered": None,
             "first_break_t": None}
    if not table:
        return dict(empty)
    keys = np.fromiter(table.keys(), dtype=np.int64, count=len(table))
    vals = np.fromiter(table.values(), dtype=np.int64, count=len(table))
    order = np.argsort(keys)
    keys, vals = keys[order], vals[order]
    idx = np.searchsorted(keys, codes)
    idx = np.clip(idx, 0, len(keys) - 1)
    covered = keys[idx] == codes
    pred = vals[idx]
    wrong = covered & (pred != y)

    def summarize(mask):
        cov = covered & mask
        wr = wrong & mask
        nw = int(wr.sum())
        nc = int(cov.sum())
        return {
            "n": int(mask.sum()),
            "covered": nc,
            "coverage": float(cov.sum() / max(1, int(mask.sum()))),
            "errors_on_covered": nw,
            "acc_on_covered": float(1 - nw / nc) if nc else None,
            "first_break_t": int(tvals[wr][0]) if nw else None,
        }

    out = summarize(np.ones(len(codes), dtype=bool))
    if split is not None:
        out["pin_core_c1"] = summarize(split)
        out["shell_c0"] = summarize(~split)
    return out


# ------------------------------------------------------------ GF(2) symbolic fit


def gf2_monomials(B: int, deg: int) -> list[tuple[int, ...]]:
    from itertools import combinations

    mons: list[tuple[int, ...]] = [()]
    for d in range(1, deg + 1):
        mons.extend(combinations(range(B), d))
    return mons


def gf2_fit(X: np.ndarray, y: np.ndarray, deg: int):
    """Exact GF(2) polynomial fit.  Returns (coeffs, mons) or None if the linear
    system is inconsistent (i.e. no such polynomial reproduces TRAIN exactly)."""
    mons = gf2_monomials(X.shape[1], deg)
    if len(mons) > 4000:
        return None
    M = np.ones((X.shape[0], len(mons)), dtype=np.uint8)
    for k, mon in enumerate(mons):
        if mon:
            col = X[:, mon[0]].astype(np.uint8)
            for i in mon[1:]:
                col = col & X[:, i].astype(np.uint8)
            M[:, k] = col
    # Gaussian elimination over GF(2) on [M | y].  Row i is packed into a Python
    # int whose bit k is monomial-column k (little-endian bit order both ways).
    ncol = len(mons)
    packed = np.packbits(M, axis=1, bitorder="little")
    seen: dict[int, int] = {}
    for i in range(M.shape[0]):
        v = int.from_bytes(packed[i].tobytes(), "little")
        b = int(y[i])
        if v in seen:
            if seen[v] != b:
                return None  # identical monomial vector, two labels
        else:
            seen[v] = b
    piv: dict[int, tuple[int, int]] = {}
    for v, b in seen.items():
        while v:
            h = v.bit_length() - 1
            if h in piv:
                pv, pb = piv[h]
                v ^= pv
                b ^= pb
            else:
                piv[h] = (v, b)
                v = 0
                b = 0
                break
        if v == 0 and b == 1:
            return None  # 0 = 1, system inconsistent: no such polynomial
    coef = np.zeros(ncol, dtype=np.uint8)
    for h in sorted(piv):  # increasing: a pivot row's other bits are all < h
        pv, pb = piv[h]
        s = pb
        w = pv ^ (1 << h)
        while w:
            j = w.bit_length() - 1
            s ^= int(coef[j])
            w &= ~(1 << j)
        coef[h] = s
    return coef, mons


def gf2_eval(coef, mons, X: np.ndarray) -> np.ndarray:
    out = np.zeros(X.shape[0], dtype=np.uint8)
    for k, mon in enumerate(mons):
        if not coef[k]:
            continue
        if not mon:
            out ^= 1
            continue
        col = X[:, mon[0]].astype(np.uint8)
        for i in mon[1:]:
            col = col & X[:, i].astype(np.uint8)
        out ^= col
    return out


# ------------------------------------------------------------------ experiments


def slices(n: int):
    tr = np.arange(*TRAIN)
    dv = np.arange(*DEV)
    te = np.arange(*TEST)
    return tr, dv, te


def run_framing(name: str, X: np.ndarray, y: np.ndarray, keep: np.ndarray,
                results: list, gf2_deg: int = 0,
                split: np.ndarray | None = None) -> None:
    """keep = boolean mask of usable t (e.g. restrict to the zero-set).

    split = boolean over all t, True on the provable PIN CORE (c_t = 1).
    """
    tr, dv, te = slices(len(y))
    t_all = np.arange(len(y))
    codes = pack(X)

    def sub(idx):
        m = keep[idx]
        return idx[m]

    itr, idv, ite = sub(tr), sub(dv), sub(te)
    if len(itr) < 200 or len(ite) < 200:
        return
    table, npat, nconf = exact_table(codes[itr], y[itr])
    base = max(float(y[itr].mean()), 1 - float(y[itr].mean()))
    rec = {
        "framing": name,
        "bits": int(X.shape[1]),
        "n_train": int(len(itr)),
        "n_test": int(len(ite)),
        "majority_baseline_train": round(base, 6),
        "train_patterns": npat,
        "train_conflicted_patterns": nconf,
        "table_consistent_on_train": nconf == 0,
        "dev_in_range": check_table(table, codes[idv], y[idv], t_all[idv],
                                    None if split is None else split[idv]),
        "test_out_of_range": check_table(table, codes[ite], y[ite], t_all[ite],
                                         None if split is None else split[ite]),
    }
    for deg in ([1, 2, 3] if gf2_deg else []):
        fit = gf2_fit(X[itr], y[itr], deg)
        rec.setdefault("gf2_by_degree", {})[deg] = (
            {"exact_fit_exists": False} if fit is None else
            {"exact_fit_exists": True,
             "n_terms": int(sum(1 for v in fit[0] if v))}
        )
    if gf2_deg:
        fit = gf2_fit(X[itr], y[itr], gf2_deg)
        if fit is None:
            rec["gf2"] = {"deg": gf2_deg, "exact_fit_exists": False}
        else:
            coef, mons = fit
            assert (gf2_eval(coef, mons, X[itr]) == y[itr]).all(), \
                "gf2_fit claimed an exact fit that does not reproduce TRAIN"
            pt = gf2_eval(coef, mons, X[ite])
            wrong = pt != y[ite]
            terms = [list(m) for k, m in enumerate(mons) if coef[k]]
            rec["gf2"] = {
                "deg": gf2_deg,
                "exact_fit_exists": True,
                "n_terms": len(terms),
                "terms": terms[:40],
                "test_errors": int(wrong.sum()),
                "test_acc": float(1 - wrong.mean()),
                "first_break_t": int(t_all[ite][wrong][0]) if wrong.any() else None,
            }
    results.append(rec)
    ok = "CONSISTENT" if nconf == 0 else f"{nconf}cf"
    oor, dev = rec["test_out_of_range"], rec["dev_in_range"]

    def fmt(d):
        a = "n/a" if d["acc_on_covered"] is None else f"{d['acc_on_covered']:.4f}"
        return f"acc={a:>6s} cov={d['coverage']:.3f} brk@{d['first_break_t']}"

    g = ""
    if "gf2_by_degree" in rec:
        d_ok = [str(d) for d, v in rec["gf2_by_degree"].items()
                if v["exact_fit_exists"]]
        g = " gf2exact@deg=" + (",".join(d_ok) if d_ok else "NONE")
    s = ""
    if "pin_core_c1" in oor:
        pc, sh = oor["pin_core_c1"], oor["shell_c0"]
        pa = "n/a" if pc["acc_on_covered"] is None else f"{pc['acc_on_covered']:.4f}"
        sa = "n/a" if sh["acc_on_covered"] is None else f"{sh['acc_on_covered']:.4f}"
        s = (f" | TEST-core(c=1) acc={pa} cov={pc['coverage']:.3f}"
             f" TEST-shell(c=0) acc={sa} cov={sh['coverage']:.3f}"
             f" brk@{sh['first_break_t']}")
    print(f"  {name:48s} b={X.shape[1]:2d} tr={ok:>10s} | DEV {fmt(dev)} "
          f"| TEST {fmt(oor)}{s}{g}")


def main(rule: str = "30") -> list:
    t0 = time.time()
    print(f"== rule {rule}: building exact windows to depth {N} (W={WMAX})")
    A = windows(N, WMAX, rule)
    print(f"   built in {time.time()-t0:.1f}s")
    c = A[:, WMAX].astype(np.int8)
    n = len(c)
    t_all = np.arange(n)
    results: list = []
    allmask = np.ones(n, dtype=bool)

    # ---- Target A: c_{t+1} from various framings -------------------------
    yA = np.zeros(n, dtype=np.int8)
    yA[:-1] = c[1:]
    okA = allmask.copy()
    okA[-1] = False
    pin = c == 1  # PREREG Lemma A19.1: only here can a left-window rule be forced
    print(" TARGET A: predict c_{t+1}")
    for K in (4, 8, 12, 16, 20):
        run_framing(f"A/col-history K={K}", col_history(c, K), yA, okA, results,
                    gf2_deg=3 if K <= 12 else 0, split=pin)
    for K, p in ((8, 2), (8, 3), (8, 4), (8, 6), (8, 8), (12, 16)):
        X = np.hstack([col_history(c, K), mod_bits(n, p)])
        run_framing(f"A/col-history K={K} + t mod {p}", X, yA, okA, results,
                    split=pin)
    for Wl in (2, 4, 8, 12, 16, 20):
        run_framing(f"A/left-window W={Wl}", left_window(A, WMAX, Wl), yA, okA,
                    results, gf2_deg=3 if Wl <= 8 else 0, split=pin)
    # positive control: the full local window makes this exact by the CA rule
    run_framing("A/CONTROL full window W=1 (rule itself)",
                A[:, WMAX - 1 : WMAX + 2].astype(np.int8), yA, okA, results,
                gf2_deg=3, split=pin)

    # ---- Target B: r_t = s(t,1) on the zero-set {c_t = 0}  (R1's obligation)
    yB = A[:, WMAX + 1].astype(np.int8)
    okB = c == 0
    print(" TARGET B: predict r_t = s(t,1) restricted to the zero-set {c_t=0} (R1)")
    for Wl in (2, 4, 8, 12, 16, 20, 24):
        run_framing(f"B/left-window W={Wl}", left_window(A, WMAX, Wl), yB, okB,
                    results, gf2_deg=3 if Wl <= 8 else 0)
    for K in (8, 16):
        X = np.hstack([left_window(A, WMAX, 8), col_history(c, K)])
        run_framing(f"B/left-window W=8 + col-history K={K}", X, yB, okB, results)

    # ---- Target C: the ONE branch of m_{t+1} the local rule does not determine.
    # PREREG derives m_{t+1} = f(m_t, c_t) off the branch (m_t, c_t) = (1,1);
    # mining anywhere else would rediscover the CA rule.  Target bit: is
    # m_{t+1} >= 3, i.e. s(t+1,2) = 1 XOR (s(t,2) OR s(t,3)) = 0.
    m = nearest_right_one(A, WMAX)
    print(" TARGET C: m_{t+1} on the ONLY undetermined branch (m_t=1, c_t=1)")
    yC = np.zeros(n, dtype=np.int8)
    yC[:-1] = (m[1:] >= 3).astype(np.int8)
    okC = allmask.copy()
    okC[-1] = False
    okC &= (m == 1) & (c == 1)
    for Wl in (4, 8, 12, 20):
        run_framing(f"C/branch(m=1,c=1) left-window W={Wl}",
                    left_window(A, WMAX, Wl), yC, okC, results)
    for K in (8, 16):
        X = np.hstack([left_window(A, WMAX, 8), col_history(c, K)])
        run_framing(f"C/branch(m=1,c=1) left-W=8 + col-history K={K}", X, yC,
                    okC, results)
    # CONTROL: the same target OFF the branch must be a local-rule tautology.
    okC_off = allmask.copy()
    okC_off[-1] = False
    okC_off &= ~((m == 1) & (c == 1)) & (m < WMAX)
    mb = ((m[:, None] >> np.arange(5)) & 1).astype(np.int8)
    run_framing("C/CONTROL off-branch (m_t,c_t) only -> m_{t+1}>=3",
                np.hstack([mb, c[:, None]]), yC, okC_off, results)

    # ---- Target D: period-break indicator 1[c_t != c_{t+p}]  (a1 Lemma Z)
    print(" TARGET D: predict 1[c_t != c_{t+p}] (periodicity-break events)")
    for p in (1, 2, 3, 4, 5, 6, 7, 8):
        yD = np.zeros(n, dtype=np.int8)
        yD[: n - p] = (c[:-p] != c[p:]).astype(np.int8)
        okD = allmask.copy()
        okD[n - p:] = False
        run_framing(f"D/p={p} left-window W=12", left_window(A, WMAX, 12), yD,
                    okD, results)
        X = np.hstack([col_history(c, 12), mod_bits(n, max(2, p))])
        run_framing(f"D/p={p} col-history K=12 + t mod {p}", X, yD, okD, results)
        # zero-set restriction: Lemma Z's predicate lives on {c_t = 0}
        run_framing(f"D/p={p} left-window W=12 on zero-set",
                    left_window(A, WMAX, 12), yD, okD & (c == 0), results)

    for r in results:
        r["rule"] = rule
        r["train_range"] = list(TRAIN)
        r["dev_range"] = list(DEV)
        r["test_range"] = list(TEST)
    print(f"   rule {rule} done in {time.time()-t0:.1f}s, {len(results)} framings")
    return results


if __name__ == "__main__":
    rules = sys.argv[1:] or ["30", "90"]
    out = []
    for r in rules:
        out.extend(main(r))
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "mine_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote mine_results.json ({len(out)} records)")
