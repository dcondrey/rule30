"""
Step 3: stress-test the core inference "rank(M_T) -> infinity implies a_t
cannot be eventually periodic" INDEPENDENT of Rule 30.

Construction: let M_T be the TxT lower-triangular all-ones matrix over GF(2)
(row t has 1s in columns 0..t, i.e. M_T[t][s] = 1 for all s <= t). This is
exactly the same "shape" as the claim's M_T: unbounded, strictly growing rank
as T -> infinity (rank(M_T) = T always, full rank, same growth rate as the
real M_T measured in build_MT_rank.py), lower-triangular, each row picking up
one new column relative to the previous row.

We then pick an arbitrary eventually-periodic target sequence p_t (period 3:
0,1,1,0,1,1,...) and SOLVE for a driving vector "chi" (by back-substitution,
since the matrix is invertible over GF(2)) such that

    a_t := (M_T . chi)_t = p_t   for all t < T

exactly. This produces a driving sequence chi and a full-rank (rank=T,
growing without bound) matrix family M_T whose affine image contains a
genuinely periodic sequence. This directly refutes, in general, the claim
that "unbounded/growing rank of the incidence matrix implies the resulting
sequence cannot be eventually periodic."
"""
import numpy as np


def build_lower_triangular(T):
    M = np.zeros((T, T), dtype=np.uint8)
    for t in range(T):
        M[t, :t + 1] = 1
    return M


def gf2_matvec(M, x):
    T = M.shape[0]
    y = np.zeros(T, dtype=np.uint8)
    for t in range(T):
        y[t] = np.bitwise_xor.reduce(M[t] & x) if np.any(M[t]) else 0
    return y


def gf2_rank_dense(M):
    A = M.copy().astype(np.uint8)
    rows, cols = A.shape
    rank = 0
    for col in range(cols):
        pivot = None
        for r in range(rank, rows):
            if A[r, col]:
                pivot = r
                break
        if pivot is None:
            continue
        A[[rank, pivot]] = A[[pivot, rank]]
        for r in range(rows):
            if r != rank and A[r, col]:
                A[r] ^= A[rank]
        rank += 1
        if rank == rows:
            break
    return rank


def solve_lower_triangular(M, p):
    """Solve M . chi = p over GF(2) for lower-triangular M with 1s on diagonal."""
    T = M.shape[0]
    chi = np.zeros(T, dtype=np.uint8)
    for t in range(T):
        # (M chi)_t = XOR_{s<=t} M[t,s]*chi[s] = p[t]
        acc = np.bitwise_xor.reduce(M[t, :t] & chi[:t]) if t > 0 else 0
        # M[t,t] = 1 (diagonal), so chi[t] = p[t] XOR acc
        chi[t] = p[t] ^ acc
    return chi


def main():
    T = 200
    M = build_lower_triangular(T)
    rank = gf2_rank_dense(M)
    print(f"T={T}: rank(M_T) = {rank} (full rank, grows as T -> infinity, same as measured Rule30 M_T)")

    # periodic target, period 3: 0,1,1,0,1,1,...
    p = np.array([[0, 1, 1][t % 3] for t in range(T)], dtype=np.uint8)
    chi = solve_lower_triangular(M, p)
    a = gf2_matvec(M, chi)

    match = np.array_equal(a, p)
    print(f"Target periodic sequence p_t (period 3) reproduced exactly by M_T . chi: {match}")
    print("First 15 of p:  ", p[:15].tolist())
    print("First 15 of a=Mchi:", a[:15].tolist())
    print("chi (driving vector) is nontrivial (not all-zero):", bool(np.any(chi)))
    print(f"chi has {int(np.sum(chi))} nonzero entries out of {T}")

    if match and rank == T:
        print()
        print("KILLED: explicit counterexample constructed. A GF(2)-linear system with "
              "rank(M_T) = T -> infinity (full, growing rank, same qualitative growth as "
              "the claim's M_T) has an affine image containing an exactly periodic "
              "sequence. Therefore 'growing/unbounded rank of the incidence matrix' does "
              "NOT by itself imply the resulting sequence a_t cannot be eventually "
              "periodic. The inference in Conjecture B's argument is invalid as a "
              "general logical step; if it holds for actual Rule-30-generated chi it "
              "must be due to some additional, unproven, specific property of that chi "
              "(the panel's 'infinitely many 11-pairs' remark is not such a property: "
              "it only asserts chi is not eventually zero, which this counterexample's "
              "chi also satisfies for period-non-1 targets).")
    else:
        print("Counterexample construction failed unexpectedly -- see mismatch above.")


if __name__ == "__main__":
    main()
