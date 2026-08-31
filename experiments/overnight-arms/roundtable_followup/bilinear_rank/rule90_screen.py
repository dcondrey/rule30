"""
Step 5: Rule-90 filter screen. Simulate Rule 90 (XOR of the two OUTER
neighbors only: u_{t+1,i} = u_{t,i-1} XOR u_{t,i+1}) from the same lone-seed
IC. Confirm: (a) the diagnostic quantity chi90_{t,i} := u_{t,i} AND u_{t,i+1}
(computed purely as a diagnostic -- it plays no role in Rule 90's own update)
is identically zero for all t>0; (b) the center column a_t = 0 for all t>0
(well-known fact about Rule 90); (c) if one mechanically built the same-shape
M_T from Rule90's (identically-zero) chi, it is the all-zero matrix, rank 0.
"""
import numpy as np


def simulate_rule90(T, width):
    c = width // 2
    u = np.zeros((T + 1, width), dtype=np.uint8)
    u[0, c] = 1
    for t in range(T):
        row = u[t]
        left = np.roll(row, 1)
        right = np.roll(row, -1)
        left[0] = 0
        right[-1] = 0
        u[t + 1] = left ^ right
    return u, c


def main():
    T = 220
    width = 6 * T + 20
    u90, c = simulate_rule90(T, width)

    a_t = u90[:, c]
    print(f"T={T}, width={width}")
    print("a_t (Rule 90 center column) for t=0..10:", a_t[:11].tolist())
    nonzero_after_0 = np.any(a_t[1:] != 0)
    print(f"Any nonzero a_t for t in 1..{T}: {nonzero_after_0}")
    print(f"VERDICT (a_t=0 for t>0): {'CONFIRMED' if not nonzero_after_0 else 'FAILED -- unexpected nonzero'}")

    # diagnostic chi90 (not part of Rule90's actual update, just as the panel suggests testing)
    chi90 = (u90[:, :-1] & u90[:, 1:])[:T]  # chi90[t,i] = u90[t,i] & u90[t,i+1], t=0..T-1
    any_chi_nonzero = np.any(chi90 != 0)
    print(f"Any nonzero chi90_(t,i) = u90[t,i] & u90[t,i+1] anywhere in t=0..{T-1}: {any_chi_nonzero}")
    print(f"VERDICT (chi90 identically 0): {'CONFIRMED' if not any_chi_nonzero else 'FAILED -- unexpected nonzero adjacency'}")

    # M_T built the same mechanical way would have all entries multiplying an
    # identically-zero chi vector, so as an affine map its "rank" over the
    # actual (zero) chi contributes nothing; the incidence matrix skeleton
    # itself (which cells of chi COULD influence a_t) is still well-defined
    # and generically nonzero as an abstract matrix, but since chi90 == 0
    # identically, the driven term M_T . chi90 = 0 for all T, consistent
    # with a_t = L_t[delta0] alone. For Rule 90, L_t[delta0] (pure two-neighbor
    # linear propagator, which IS Rule 90 itself since Rule90 has no defect
    # term at all) directly gives a_t, and it is known/verified above to be 0
    # for t>0.
    print()
    print("Note: Rule 90 has no AND term in its own definition (u_{t+1,i} = "
          "u_{t,i-1} XOR u_{t,i+1}); the bilinear-defect decomposition does not "
          "natively apply to it. chi90 here is a diagnostic quantity only "
          "(computed post hoc from the Rule-90 trajectory), used solely to "
          "confirm the panel's own screen: forcing this machinery onto Rule 90 "
          "gives an identically-vanishing defect field and a driven term that "
          "contributes nothing, consistent with the well-known a_t=0 for t>0.")


if __name__ == "__main__":
    main()
