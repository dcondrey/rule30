"""Columns of Rule 30 in the frame co-moving with the left edge.

A_J(t) = s(t, J - t) for J >= 0.  Chain: A_J(t+1) = A_{J-2}(t) XOR (A_{J-1}(t) OR A_J(t)).
The centre column is the diagonal c_t = A_t(t); r_t = A_{t+1}(t); l_t = A_{t-1}(t).
Measure, for each J <= Jmax, the eventual period and preperiod of t -> A_J(t) within horizon T,
and the same for the right-edge-frame diagonals D_k(t) = s(t, t + k), k <= 0 (R4 control).
"""
import sys
sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
from r1zero_lib import lone_seed_rows

def exact_period(seq, max_q):
    """Smallest q with seq[i] == seq[i+q] for all i >= onset; onset minimal; require onset + 2q <= len."""
    n = len(seq)
    best = None
    for q in range(1, max_q + 1):
        onset = 0
        for i in range(n - q - 1, -1, -1):
            if seq[i] != seq[i + q]:
                onset = i + 1
                break
        if n - onset >= max(8 * q, 128):
            return q, onset
    return None

def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 8192
    Jmax = int(sys.argv[2]) if len(sys.argv) > 2 else 64
    A = [[] for _ in range(Jmax + 1)]
    D = [[] for _ in range(Jmax + 1)]
    for t, row, off in lone_seed_rows(T):
        left = row >> (off - t)          # bit J = s(t, J - t)
        for J in range(Jmax + 1):
            A[J].append((left >> J) & 1)
        for k in range(Jmax + 1):
            D[k].append((row >> (off + t - k)) & 1)   # D_{-k}(t) = s(t, t - k)
    out = [f"T={T} Jmax={Jmax}"]
    out.append("left-edge frame columns A_J (anti-diagonals x + t = J): J, period, preperiod")
    for J in range(Jmax + 1):
        ep = exact_period(A[J], T // 4)
        out.append(f"  A_{J}: {ep}")
    out.append("right-edge frame diagonals D_{-k} (x - t = -k): k, period, preperiod")
    for k in range(Jmax + 1):
        ep = exact_period(D[k], T // 4)
        out.append(f"  D_-{k}: {ep}")
    print("\n".join(out))

if __name__ == '__main__':
    main()
