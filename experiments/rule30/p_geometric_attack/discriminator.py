"""Single-column sensitivity discriminator.

Claim under test (PATH.md R6 obstruction (i), generalised): any functional of
the space-time diagram that is continuous under changes on a density-zero
subset cannot distinguish a periodic centre column from an aperiodic one.

Three fields, identical except where stated, same seed, same T:
  A  true Rule 30 lone-seed diagram
  B  A with column 0 overwritten by the periodic word 01010...  (P1 answer
     flips; nothing else about the field changes)
  C  true Rule 90 lone-seed diagram (centre column eventually 0, so P1's
     answer is the opposite of A's; the repo's section-0 filter)

Three statistics, one per proposed geometric attack, each computed on a
width-W window about the centre:

  S1  hyperbolic lightcone embedding (Agent 1).  Cell (x,t) -> Poincare disk
      at hyperbolic radius rho*t, angle pi*x/(t+1); d_H(t) = mean hyperbolic
      distance from the origin over the ones of row t.
  S2  multilinear relaxation, mean log singular value of the Jacobian
      (Agent 2).  Rule 30 over [0,1]: XOR -> a+b-2ab, OR -> a+b-ab.  This is
      the expansion/"negative curvature" proxy.
  S3  spectral dimension of a discrete Dirac operator (Agent 3).
      D = S + S^dagger + diag(2s-1) on the window; d_s from the heat trace
      P(tau) = Tr exp(-tau D^2)/W via -2 dlogP/dlogtau.

PREDICTION, recorded before running: |S(A) - S(B)| = O(1/W) for all three,
and S(A) ~ S(C) for the P1-relevant ones.  KILL CONDITION: any statistic
separating A from B by more than O(1/W) refutes the lemma for that statistic
and puts the corresponding attack back in play.
"""

import json
import sys

import numpy as np

FWD = {30: lambda l, m, r: l ^ (m | r), 90: lambda l, m, r: l ^ r}


def diagram(rule, T, B):
    w = 2 * B + 1
    row = np.zeros(w, dtype=np.uint8)
    row[B] = 1
    out = [row]
    for _ in range(T):
        p = out[-1]
        nxt = np.zeros(w, dtype=np.uint8)
        l, m, r = p[:-2], p[1:-1], p[2:]
        nxt[1:-1] = FWD[rule](l, m, r)
        out.append(nxt)
    return np.array(out)


def overwrite_centre(grid, B, word=(0, 1)):
    g = grid.copy()
    for t in range(g.shape[0]):
        g[t, B] = word[t % len(word)]
    return g


def s1_hyperbolic(grid, B, W, rho=0.5):
    """Mean hyperbolic distance from origin over the ones of each row."""
    T = grid.shape[0]
    half = W // 2
    out = []
    for t in range(1, T):
        xs = np.nonzero(grid[t, B - half:B + half + 1])[0] - half
        if xs.size == 0:
            continue
        # Poincare disk: hyperbolic radius rho*t, angle pi*x/(t+1).
        # dist_H(0, p) is the hyperbolic radius itself, modulated by the
        # angular spread through the point's placement in the tessellation.
        r_h = rho * t
        th = np.pi * xs / (t + 1)
        # geodesic distance from origin to (r_h, th) on the disk is r_h;
        # use the pairwise-to-centroid form so the angle enters.
        ct = th.mean()
        d = np.arccosh(np.clip(
            np.cosh(r_h) ** 2 - np.sinh(r_h) ** 2 * np.cos(th - ct), 1, None))
        out.append(d.mean())
    return float(np.mean(out[len(out) // 2:]))


def s2_relaxation(grid, B, W):
    """Mean log singular value of the multilinear-relaxation Jacobian along
    the trajectory.  XOR(a,b)=a+b-2ab, OR(a,b)=a+b-ab, so
    f(l,m,r) = l + u - 2 l u  with  u = m + r - m r."""
    T = grid.shape[0]
    half = W // 2
    vals = []
    for t in range(1, T - 1):
        x = grid[t, B - half:B + half + 1].astype(float)
        l, m, r = x[:-2], x[1:-1], x[2:]
        u = m + r - m * r
        dl = 1 - 2 * u
        du_dm, du_dr = 1 - r, 1 - m
        c = 1 - 2 * l
        # tridiagonal Jacobian of the row map
        n = l.size
        Jm = np.zeros((n, n))
        idx = np.arange(n)
        Jm[idx, idx] = c * du_dm
        Jm[idx[:-1], idx[:-1] + 1] = (c * du_dr)[:-1]
        Jm[idx[1:], idx[1:] - 1] = dl[1:]
        s = np.linalg.svd(Jm, compute_uv=False)
        vals.append(np.mean(np.log(np.maximum(s, 1e-12))))
    return float(np.mean(vals[len(vals) // 2:]))


def s3_spectral_dim(grid, B, W, taus=(0.25, 0.5)):
    """Spectral dimension of D = S + S^dag + diag(2s-1) from the heat trace."""
    T = grid.shape[0]
    half = W // 2
    ds = []
    for t in range(T // 2, T, max(1, T // 40)):
        v = grid[t, B - half:B + half + 1].astype(float) * 2 - 1
        n = v.size
        D = np.zeros((n, n))
        idx = np.arange(n)
        D[idx, idx] = v
        D[idx[:-1], idx[:-1] + 1] = 1.0
        D[idx[1:], idx[1:] - 1] = 1.0
        ev = np.linalg.eigvalsh(D)
        p = [np.mean(np.exp(-tau * ev ** 2)) for tau in taus]
        ds.append(-2 * (np.log(p[1]) - np.log(p[0]))
                  / (np.log(taus[1]) - np.log(taus[0])))
    return float(np.mean(ds))


def s0_control(grid, B, W):
    """POSITIVE CONTROL: a statistic that looks only at column 0.  Fraction of
    times the centre column agrees with the period-2 word 0101...  A must be
    near 1/2 (aperiodic), B exactly 1.0 (it was overwritten with that word).
    If this does not separate A from B, the harness is not reading column 0
    and every null result below is meaningless."""
    c = grid[:, B]
    w = np.arange(c.size) % 2
    return float((c == w).mean())


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    B = T + 4
    A = diagram(30, T, B)
    Bg = overwrite_centre(A, B)
    C = diagram(90, T, B)
    assert (A != Bg).sum() == (A[:, B] != Bg[:, B]).sum(), \
        "B must differ from A on column 0 only"
    ndiff = int((A[:, B] != Bg[:, B]).sum())
    print(json.dumps({"T": T, "cells": int(A.size),
                      "cells_changed_A_to_B": ndiff,
                      "fraction_changed": round(ndiff / A.size, 8)}), flush=True)
    for W in (32, 64, 128, 256):
        row = {"W": W}
        for name, fn in (("S0_control_col0", s0_control),
                         ("S1_hyperbolic", s1_hyperbolic),
                         ("S2_relaxation", s2_relaxation),
                         ("S3_spectral_dim", s3_spectral_dim)):
            a, b, c = fn(A, B, W), fn(Bg, B, W), fn(C, B, W)
            row[name] = {"A": float(f"{a:.10g}"), "B": float(f"{b:.10g}"),
                         "C": float(f"{c:.10g}"),
                         "absAB": float(f"{abs(a - b):.4g}"),
                         "relAB": float(f"{abs(a-b)/max(abs(a),1e-12):.4g}"),
                         "relAC": float(f"{abs(a-c)/max(abs(a),1e-12):.4g}")}
        print(json.dumps(row), flush=True)


if __name__ == "__main__":
    main()
