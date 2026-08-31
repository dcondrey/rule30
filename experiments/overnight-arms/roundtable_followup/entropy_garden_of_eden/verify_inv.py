"""
Step 1 of the entropy/Garden-of-Eden followup: make T_w precise and verify it
against brute-force simulation.

Rule 30:  s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1))
Inverse (leftward, left-permutive): s(t,x-1) = s(t+1,x) XOR (s(t,x) OR s(t,x+1))

Rule 90:  s(t+1,x) = s(t,x-1) XOR s(t,x+1)
Inverse (leftward): s(t,x-1) = s(t+1,x) XOR s(t,x+1)

Key point worked out before writing this code (see RESULTS doc section 2):
the panel's map "u_{t,i-1} = u_{t+1,i} XOR (...)" cannot be a map from one row
rho_t to the next row rho_{t+1} taken alone, because the right-hand side
already needs u_{t+1,i}, a value that lives in the row you're trying to
produce. The only way to make this well-defined is the one this repo's ladder
code already uses: treat each column x as a FULL TIME TRACE col_x: t -> bit,
and let the inverse recursion move in x (spatial, leftward), consuming two
time-shifted values col_x(t), col_x(t+1) of the SAME column plus col_{x+1}(t)
of its right neighbour, to produce col_{x-1}(t) for every t at once:

    col_{x-1}(t) = col_x(t+1) XOR (col_x(t) OR col_{x+1}(t))     [[Rule 30]]
    col_{x-1}(t) = col_x(t+1) XOR col_{x+1}(t)                   [[Rule 90]]

This script:
  (a) simulates the true lone-seed diagram for both rules by direct forward
      application of the local rule (ground truth),
  (b) reconstructs columns x = -1, -2, ... leftward from columns x = 0, 1, ...
      using ONLY the inverse formula above (never touching the true left
      half-plane), and checks the reconstruction matches ground truth exactly,
  (c) separately sanity-checks the reduction identity from PATH.md section 2
      (constant center c_t=1 for all t => l_t = 0 for all t) on a synthetic
      constant trace, independent of any lone-seed data.
"""
from __future__ import annotations

def forward_rule30(T: int, xmin: int, xmax: int):
    """Ground truth: lone seed at (0,0), forward Rule 30 to time T (inclusive).
    Returns dict (t,x) -> bit for x in [xmin,xmax], t in [0,T]."""
    width = xmax - xmin + 1
    row = [0] * width
    row[0 - xmin] = 1
    grid = {}
    for x in range(xmin, xmax + 1):
        grid[(0, x)] = row[x - xmin]
    for t in range(0, T):
        new = [0] * width
        for i in range(width):
            x = xmin + i
            left = row[i - 1] if i - 1 >= 0 else 0
            cen = row[i]
            right = row[i + 1] if i + 1 < width else 0
            new[i] = left ^ (cen | right)
        row = new
        for i in range(width):
            grid[(t + 1, xmin + i)] = row[i]
    return grid


def forward_rule90(T: int, xmin: int, xmax: int):
    width = xmax - xmin + 1
    row = [0] * width
    row[0 - xmin] = 1
    grid = {}
    for x in range(xmin, xmax + 1):
        grid[(0, x)] = row[x - xmin]
    for t in range(0, T):
        new = [0] * width
        for i in range(width):
            x = xmin + i
            left = row[i - 1] if i - 1 >= 0 else 0
            right = row[i + 1] if i + 1 < width else 0
            new[i] = left ^ right
        row = new
        for i in range(width):
            grid[(t + 1, xmin + i)] = row[i]
    return grid


def reconstruct_leftward_rule30(col0, col1, Tmax):
    """col0, col1: dict t -> bit for t=0..Tmax (full time traces at x=0, x=1).
    Returns col_{-1} for t=0..Tmax-1 (need col_x(t+1), so last usable t is
    Tmax-1)."""
    out = {}
    for t in range(0, Tmax):
        out[t] = col0[t + 1] ^ (col0[t] | col1[t])
    return out


def reconstruct_leftward_rule90(col0, col1, Tmax):
    out = {}
    for t in range(0, Tmax):
        out[t] = col0[t + 1] ^ col1[t]
    return out


def extract_column(grid, x, Tmax):
    return {t: grid[(t, x)] for t in range(0, Tmax + 1)}


def check_chain(rule: str, T: int, depth: int, xmax_extra: int = 2):
    """Reconstruct `depth` columns leftward from columns x=0..depth (ground
    truth) and check every one against the ground-truth left half-plane.
    Also chain the reconstruction (feed reconstructed col_{-1} back in to get
    col_{-2}, etc.) using ONLY reconstructed data past the first step, to
    verify iterating T_w reproduces direct simulation."""
    xmin = -(depth + xmax_extra)
    xmax = depth + xmax_extra
    if rule == "30":
        grid = forward_rule30(T, xmin, xmax)
        recon = reconstruct_leftward_rule30
    elif rule == "90":
        grid = forward_rule90(T, xmin, xmax)
        recon = reconstruct_leftward_rule90
    else:
        raise ValueError(rule)

    cols = {x: extract_column(grid, x, T) for x in range(0, depth + 1)}

    mismatches = 0
    checks = 0
    # First reconstruction uses only ground-truth columns 0 and 1.
    cur_left = cols[1]
    cur_center = cols[0]
    reconstructed = {}
    for d in range(1, depth + 1):
        Tmax = T - d  # each leftward step loses one usable time step
        rec = recon(cur_center, cur_left, Tmax)
        reconstructed[-d] = rec
        truth = {t: grid[(t, -d)] for t in range(0, Tmax)}
        for t in range(0, Tmax):
            checks += 1
            if rec[t] != truth[t]:
                mismatches += 1
        # chain: shift left by one column, using the JUST-RECONSTRUCTED
        # column as the new "center" and the previous center as new "left
        # neighbour" -- this iterates T_w using its own output, not fresh
        # ground truth, which is the actual claim under test.
        cur_left = cur_center
        cur_center = rec
    return checks, mismatches


def check_constant_identity():
    """PATH.md section 2: c_t = 1 for all t (synthetic, not lone-seed) must
    force l_t = 0 for all t, via l_t = c_{t+1} XOR (c_t OR r_t), independent
    of r_t. This checks the Rule 30 inverse formula's algebra directly."""
    Tmax = 50
    col0 = {t: 1 for t in range(0, Tmax + 5)}
    for r_pattern in ([0] * (Tmax + 5), [1] * (Tmax + 5), [t % 2 for t in range(Tmax + 5)]):
        col1 = {t: r_pattern[t] for t in range(0, Tmax + 5)}
        rec = reconstruct_leftward_rule30(col0, col1, Tmax)
        assert all(v == 0 for v in rec.values()), "constant-one identity failed"
    return True


def check_period2_synthetic_rule30():
    """Sanity check on a synthetic (non-lone-seed) exactly period-2 center
    trace w = 01 repeating, to see what the formula predicts for col_{-1}
    under a genuinely periodic center, matching PATH.md's general reduction:
    c_t=1 => l_t = 1 XOR c_{t+1} (free); c_t=0 => l_t = c_{t+1} XOR r_t (needs
    right neighbour)."""
    Tmax = 40
    w = [t % 2 for t in range(Tmax + 5)]  # 0,1,0,1,...
    col0 = {t: w[t] for t in range(Tmax + 5)}
    for r_pattern_name, r_pattern in [
        ("zero", [0] * (Tmax + 5)),
        ("match_w", w),
        ("one", [1] * (Tmax + 5)),
    ]:
        col1 = {t: r_pattern[t] for t in range(Tmax + 5)}
        rec = reconstruct_leftward_rule30(col0, col1, Tmax)
        # verify against the closed-form reduction cell by cell
        ok = True
        for t in range(Tmax):
            c_t, c_t1, r_t = col0[t], col0[t + 1], col1[t]
            if c_t == 1:
                expect = 1 ^ c_t1
            else:
                expect = c_t1 ^ r_t
            if rec[t] != expect:
                ok = False
        assert ok, f"reduction mismatch for r_pattern={r_pattern_name}"
    return True


if __name__ == "__main__":
    print("=== Step 1: T_w precise definition + brute-force verification ===")
    print()
    print("Constant-center (c_t=1) identity check:", check_constant_identity())
    print("Period-2 synthetic center closed-form check:", check_period2_synthetic_rule30())
    print()
    for rule in ("30", "90"):
        for depth in (1, 2, 3, 4, 5):
            T = 60
            checks, mismatches = check_chain(rule, T, depth)
            print(f"rule={rule} depth={depth} T={T}: checks={checks} mismatches={mismatches}")
    print()
    print("If mismatches=0 everywhere, T_w (the leftward per-column inverse")
    print("map, chained) reproduces true lone-seed brute-force simulation")
    print("exactly, for both Rule 30 and Rule 90, at every depth tested.")
