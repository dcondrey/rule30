# A rational-frequency scale target and its exact residual error

Date: 2026-09-16. **Exact identities and a sufficient P1 target; no growth
estimate or noncancellation theorem for the actual singleton center.**

An irrational coherent line is not the only frequency statement that
could prove nonperiodicity. At a rational frequency, a proved intermediate
growth rate of the unnormalized Fourier sum also suffices. The known
Thue–Morse contribution suggests one precise scale to test, but the actual
residual is not known to preserve it.

## 1. Eventually periodic sequences have bounded-or-linear rational sums

Let `s_t` be a bounded, eventually periodic sequence and let `alpha=p/q`
be rational. Then `s_t exp(-2*pi*i*alpha*t)` is eventually periodic, with
period dividing a common multiple of the tail period and q. Splitting
its sum into complete periods and a bounded remainder proves

```text
S(N) := sum_(t<N) s_t exp(-2*pi*i*alpha*t) = N*ell + O(1).    (1)
```

The finite transient changes only the bounded error. Thus either `ell=0`
and the sums are bounded, or `ell!=0` and their magnitude grows linearly.

Consequently, for any increasing sequence `N_k`, proving both
`S(N_k)=o(N_k)` and unboundedness of `|S(N_k)|` rules out eventual
periodicity. These are statements about the same sequence and frequency;
an upper bound alone does not suffice.

In particular, put `omega=exp(-2*pi*i/3)` and, on the Rule 30 singleton,

```text
s_t=(-1)^c_t,
F_k=sum_(0<=t<4^k) s_t*omega^t.
```

The sign convention is the negative of `2*c_t-1` in the
[frequency-search report](RESULTS-fundamental-frequency-search.md);
amplitudes are unchanged. A sufficient new target is

```text
3^(-k)*F_k -> L != 0.                                     (2)
```

Indeed, this gives unbounded sums of size `N^(log_4(3))` along `N=4^k`,
while `F_k/4^k -> 0`. Equation (1) excludes this behavior for every
eventually periodic center, so (2) would prove P1. It would not by itself
prove P2 or provide a P3 algorithm. The normalized coefficient at frequency
1/3 would tend to zero along these scales, not to a coherent line.

The Thue–Morse product formula and its enhanced peaks at denominator three
are established context, not a discovery here; see
[Baake, Grimm and Nilsson, page 2](https://arxiv.org/pdf/1311.4371).
For Thue–Morse signs, the unnormalized amplitude at length `2^m` is
`3^(m/2)`. Its square divided by sample length has a different exponent;
the exponent used in (2) concerns the unnormalized amplitude.

## 2. An exact four-adic residual identity

The [left-edge decomposition](RESULTS-duhamel-left-edge-thue-morse.md)
proves `c_t=theta(t) XOR R_t` for `t>=1`, where
`theta(t)=popcount(t) mod 2` and R is the endogenous projected defect parity.
Write

```text
tau_t=(-1)^theta(t),
b_t=(-1)^R_t for t>=1,     b_0=-1.
```

This explicit time-zero convention gives `s_t=tau_t*b_t` for every
`t>=0`, including `c_0=1`. Define the complex residual variation

```text
delta_n = b_(4n) - omega*b_(4n+1) - omega^2*b_(4n+2)
          + b_(4n+3) - 3*b_n,
D_k = sum_(n<4^k) tau_n*omega^n*delta_n.                    (3)
```

These `D_k` are Fourier sums of residual variations. They are not the
local integer correction in the spatial extraction identity.

The identities

```text
(tau_(4n),tau_(4n+1),tau_(4n+2),tau_(4n+3))
    = tau_n*(1,-1,-1,1),
omega^(4n)=omega^n,
1-omega-omega^2+1=3
```

give, by grouping four terms,

```text
F_(k+1)=3*F_k+D_k,
3^(-k)*F_k=b_0+sum_(j<k) D_j/3^(j+1).                    (4)
```

No approximation, independence assumption, limiting measure, or P1/P2
hypothesis enters this calculation. It is also an identity for arbitrary
binary sequences after defining `b_t=s_t*tau_t`; its validity alone
provides no Rule-30-specific estimate.

## 3. The missing estimate includes noncancellation

Absolute summability

```text
sum_(j>=0) |D_j|/3^(j+1) < infinity                       (5)
```

would give existence of the scaled limit
`L=b_0+sum_(j>=0)D_j/3^(j+1)`. It does **not** imply `L!=0`.
Both existence and noncancellation are needed for target (2).

A sufficient quantitative certificate, starting at any scale h, is

```text
sum_(j>=h) |D_j|/3^(j-h+1) < |F_h|.                      (6)
```

Dividing (6) by `3^h` bounds the entire remaining change in the scaled
sum strictly below its current magnitude. It proves convergence and a
nonzero limit. For example, an independently proved uniform bound
`|D_j|<=K*rho^j` for all `j>=h`, with `0<rho<3`, would make

```text
|F_h| > K*rho^h/(3-rho)                                  (7)
```

a sufficient finite margin. No such bound or margin is established here.

The simplest version, starting at `h=0`, is already ruled out exactly on
the actual seed. Its first two defects are `D_0=-2*omega` and
`D_1=6+4*omega`, with norms 2 and `2*sqrt(7)`. Therefore

```text
|D_0|/3 + |D_1|/9 = 2/3 + 2*sqrt(7)/9 > 1 = |b_0|.
```

This rejects the origin-based strict absolute perturbation margin, not
summability (5), a margin beginning at a later scale, or a nonzero limit L.

There is also a direct unsigned residual-variation bound. Let

```text
V_j = #{(n,r): 0<=n<4^j, 0<=r<4, b_(4n+r)!=b_n}.
```

Subtracting `b_n` separately in the four terms of (3), whose coefficients
have modulus one and sum three, gives `|D_j|<=2*V_j`.
Replacing `|D_j|` by `2*V_j` in (6) is therefore sufficient, but stronger.
Signed cancellation in (3) could matter even when these mismatches are
numerous.

The need for noncancellation has an exact control. For the constant
sequence `s_t=-1`, we have `b_t=-tau_t`. Since `4^k=1 mod 3`,

```text
F_k=-1,     D_k=2,
sum_(j>=0) |D_j|/3^(j+1)=1,
L=-1+sum_(j>=0) 2/3^(j+1)=0.
```

Thus even uniformly bounded residual defects can cancel the whole
Thue–Morse scale. Conversely, for `s_t=-tau_t`, the residual is constant
`b_t=-1`, every `D_k=0`, and `F_k=-3^k`. A period-three control with signs
`(-1,1,1)` has `F_k=-(2*4^k+1)/3`, displaying the linear alternative
in (1). These are calibration sequences, not alternative singleton orbits.

## 4. Exact finite checks on the existing prefix

The [standard-library verifier](../../experiments/rule30/third_frequency_scale_audit.py)
uses exact Eisenstein arithmetic: `(a,b)` denotes `a+b*omega`, with
`|a+b*omega|^2=a^2-a*b+b^2`. It independently sums the actual center
signs by time residue modulo three and computes (3) from four-adic
residual variations. All ten scale identities through `4^10=1,048,576`
agree exactly. The three controls receive another 21 exact scale checks.

No larger seed simulation is performed. The same previously used cache
supplies this prefix; 8,192 bits are independently recomputed by packed
evolution and 257 by the literal scalar Rule 30 truth table. The full
cache is not independently regenerated. The
[JSON artifact](../../experiments/rule30/third-frequency-scale-audit.json)
records its offset and used-payload hash, the verifier hash, exact sums,
residual differences, and control formulas.

Selected values are:

| N | Exact F as a+b*omega | Approximate `|F|/3^k` |
|---:|---|---:|
| 256 | -5 | 0.06172840 |
| 4,096 | 95+26*omega | 0.11664648 |
| 16,384 | 29-22*omega | 0.02025869 |
| 65,536 | 17-484*omega | 0.07509831 |
| 262,144 | 151-1220*omega | 0.06615269 |
| 1,048,576 | -173-1758*omega | 0.02842048 |

The unperturbed negative Thue–Morse control has scaled magnitude one
at every scale. The actual values do not establish stabilization at a
nonzero limit, and they do not disprove a later nonzero limit either.
At the last residual-comparison scale, 525,128 of 1,048,576 child/parent
pairs disagree. Thus unsigned sparsity is not evident in this finite
sample; an all-length signed estimate remains a separate obligation.

```sh
uv run --no-project python experiments/rule30/third_frequency_scale_audit.py
```

The result is a precise conditional P1 target and its exact error budget.
Neither summability nor noncancellation has been proved for Rule 30.
