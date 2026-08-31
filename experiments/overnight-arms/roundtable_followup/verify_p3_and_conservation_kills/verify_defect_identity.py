"""
Verify Claim 1: DeepSeek's temporal-defect conservation-law identity for Rule 30's
lone-seed center column, vs Grok's kill, vs the algebraically-corrected version.

Rule 30 local rule: f(a,b,c) = a XOR (b OR c), applied as
    F(x)_i = x_{i-1} XOR (x_i OR x_{i+1})

Let u_{t,i} = (F^t x)_i, a_t = u_{t,0}.

By hand: a_{t+1} = u_{t,-1} XOR (a_t OR u_{t,1})
                  = u_{t,-1} XOR a_t XOR u_{t,1} XOR (a_t AND u_{t,1})
       => a_{t+1} XOR a_t = u_{t,-1} XOR u_{t,1} XOR (a_t AND u_{t,1})   ... (CORRECTED, = Grok's claim)

DeepSeek's claimed identity: a_{t+1} XOR a_t = u_{t,1} XOR u_{t,2} XOR (u_{t,1} AND u_{t,2})   ... (DEEPSEEK)

We test both against direct simulation of Rule 30 from a single lone seed.
"""
import numpy as np

def step_rule30(row):
    n = len(row)
    left = np.roll(row, 1)
    right = np.roll(row, -1)
    # zero-pad boundary effect out by only checking interior region, using large enough array
    return left ^ (row | right)

def simulate(T, width):
    assert width % 2 == 1
    x = np.zeros(width, dtype=np.uint8)
    c = width // 2
    x[c] = 1
    rows = [x.copy()]
    for t in range(T):
        x = step_rule30(x)
        rows.append(x.copy())
    return rows, c

def main():
    T = 2000
    width = 2 * T + 5  # generous margin so boundary (zero) never reaches columns we inspect
    rows, c = simulate(T, width)

    deepseek_holds = True
    corrected_holds = True
    first_deepseek_fail = None
    first_corrected_fail = None

    for t in range(T - 1):
        row_t = rows[t]
        a_t = row_t[c]
        a_t1 = rows[t + 1][c]
        u_tm1 = row_t[c - 1]   # u_{t,-1}
        u_t1 = row_t[c + 1]    # u_{t,1}
        u_t2 = row_t[c + 2]    # u_{t,2}

        lhs = a_t1 ^ a_t

        deepseek_rhs = u_t1 ^ u_t2 ^ (u_t1 & u_t2)
        corrected_rhs = u_tm1 ^ u_t1 ^ (a_t & u_t1)

        if lhs != deepseek_rhs:
            deepseek_holds = False
            if first_deepseek_fail is None:
                first_deepseek_fail = t
        if lhs != corrected_rhs:
            corrected_holds = False
            if first_corrected_fail is None:
                first_corrected_fail = t

    print(f"T tested: {T}")
    print(f"DeepSeek identity holds for all t? {deepseek_holds}"
          + (f" (first failure at t={first_deepseek_fail})" if not deepseek_holds else ""))
    print(f"Corrected (Grok-implied) identity holds for all t? {corrected_holds}"
          + (f" (first failure at t={first_corrected_fail})" if not corrected_holds else ""))

    # Report failure rate for DeepSeek's identity to show it's not just an edge case
    fails = 0
    for t in range(T - 1):
        row_t = rows[t]
        a_t = row_t[c]
        a_t1 = rows[t + 1][c]
        u_t1 = row_t[c + 1]
        u_t2 = row_t[c + 2]
        lhs = a_t1 ^ a_t
        deepseek_rhs = u_t1 ^ u_t2 ^ (u_t1 & u_t2)
        if lhs != deepseek_rhs:
            fails += 1
    print(f"DeepSeek identity failure rate: {fails}/{T-1} = {fails/(T-1):.4f}")

if __name__ == "__main__":
    main()
