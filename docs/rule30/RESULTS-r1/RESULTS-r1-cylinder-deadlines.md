# Sharp finite-left deadlines from the two proved periodic cylinders

Date: 2026-09-15. **Uniform exclusion for two right-prefix families;
the unrestricted period-two problem and P1 remain open.**

The [periodic-cylinder report](RESULTS-r1-periodic-cylinders.md) proved
that two finite right prefixes force periodic neighbours under an alternating
centre drive, for every continuation to the right. Those examples originally
served as counterexamples to a global topological proposal. Their fixed
traces also give a positive, quantitative exclusion for finite-left rows.
This is a corollary of those certificates and the existing left-permutive
trace reconstruction, not a new cylinder construction or a literature
priority claim.

## 1. Statement

Use the two exact words `u_124` and `u_104` printed in
[the source report, section 1](RESULTS-r1-periodic-cylinders.md#1-the-object-and-the-two-exact-prefixes).
Their characters specify cells `1,2,...`, in increasing spatial order.
Let `x` be any initial Rule 30 row satisfying

```
x_0 = 0,
x_i = 0 for i < -d,       d>=0,
(x_1,...,x_N) = u_N,      N=124 or 104.
```

The bits at `-d,...,-1` are arbitrary, and every cell beyond `N` is
arbitrary. The right tail need not be finite. Then the centre trace must
differ from `0,1,0,1,...` at some time

```
t <= d+7       for u_124,
t <= d+10      for u_104.                                  (1)
```

Both additive constants are sharp uniformly over `d`. More precisely,
the exact maximum first-failure time is depth plus the periodic gap
specified in section 2. Thus the maximal inclusive matching horizon is
one less than that time. No bounded-depth extrapolation is used.

## 2. The exact deadline

Let `v` be the corresponding source torus's phase-zero spatial row.
The [stored source certificate](../../experiments/rule30/r1-isolated-column/torus_prefix_cuts.json)
contains its full row, with site zero first:

| Right prefix | Neighbour time period | Spatial period of `v` | Largest cyclic gap between ones |
|---|---:|---:|---:|
| `u_124` | 10 | 155 | 7 |
| `u_104` | 14 | 728 | 10 |

Write `S` for the spatial period and define the forced left bits

```
a_j = v_((-j) mod S),       j>=1.
```

For a given support bound `d`, put

```
j_d = min{j>d : a_j=1}.                                    (2)
```

Then **the exact maximum first-failure time is `j_d`**, for every fixed
right continuation of `u_N`. Its gap above `d` has period `S` in `d`.
The complete table of these gaps is in the
[audit artifact](../../experiments/rule30/r1-cylinder-deadline-audit.json).
The largest gaps are seven and ten, proving (1) with sharp uniform
constants.

The support hypothesis is a bound, not a requirement that the leftmost
one be exactly at `-d`: the forced bit `a_d` may be zero.

## 3. Why the right tail cannot change the forced left tail

Prescribe the alternating centre `c_t=t mod 2` and evolve the right
half-line from any extension of `u_N`. The source cylinder theorem proves
that its adjacent column is the fixed periodic word

```
u_124: r = (1101000100)^infinity,
u_104: r = (11001101000100)^infinity.
```

The inverse local equation

```
s(t,i-1) = s(t+1,i) XOR (s(t,i) OR s(t,i+1))                 (3)
```

uniquely determines every left column from `(c,r)`. The known source
torus has exactly this pair. Its entire left half-plane is therefore the
unique left extension for **every** right continuation in the cylinder.
In particular its initial left row is `(a_j)` above, independently of
that continuation.

This use of uniqueness concerns two full adjacent time columns. It is
not an assertion that arbitrary one-cell traces are injective.

## 4. Proof of the deadline and sharpness

Suppose the actual centre agrees with the prescribed drive through time
`j_d`. Its actual right half agrees with the driven one through that time,
because a right-half update reads only its own row and the preceding
centre value. Recursing (3) back to time zero therefore forces
`x_(-j_d)=a_(j_d)=1`. But `j_d>d`, whereas the actual row is zero left of
`-d`. This proves failure at or before `j_d`.

To attain equality, choose `x_(-j)=a_j` for `1<=j<=d`, and zero beyond
that bound. By definition of `j_d`, this row agrees with the required
left extension at every depth less than `j_d` and first differs at
depth `j_d`.

Finite propagation prevents that first differing bit from affecting the
centre before time `j_d`. At time `j_d`, the differing leftmost ancestor
has coefficient one because the Rule 30 update is permutive in its left
argument. More distant differences cannot yet arrive. Hence the centre
agrees through time `j_d-1` and differs exactly at `j_d`.

This comparison uses a valid reference diagram: evolve the arbitrary
right continuation with prescribed `c`, then reconstruct the left by
(3). The cylinder fixes `r`, so the reconstructed left half is exactly
the source torus's. No assertion of zero-origin reachability for that
infinite-left reference is needed.

## 5. Meaning for the singleton orbit

At actual singleton time `T`, the leftmost one is at `-T`. Consequently,
if the centre is zero and the right row begins with `u_124`, an alternating
continuation must fail by absolute time `2T+7`. With `u_104`, it must fail
by `2T+10`.

Thus an actually eventually alternating singleton orbit would have to
avoid these two right-prefix cylinders at every sufficiently late
centre-zero phase. This is a proved necessary avoidance condition.
**No theorem that the singleton must enter either cylinder is supplied.**
Nor is eventual entry proved for every finite driven right row. The
earlier generic locking failures cannot be bypassed by assuming such
entry. The result excludes two infinite families of possible onset rows,
not all rows and not every period-two tail.

## 6. Verification

The standard-library
[checker](../../experiments/rule30/r1_cylinder_deadline_audit.py) reads the
existing certificate without importing its construction code. It verifies:

- both full torus cycles by the scalar Rule 30 truth table: 11,742 cells;
- all 17,408 complete return cones and their neighbour observations;
- agreement of inverse-column reconstruction with the torus left row;
- exact sharp first-failure times for 891 truncated-left examples,
  including every depth residue and depths beyond a spatial period;
- the upper deadline for all 1,022 arbitrary-left examples with `d<=8`.
- eight independent scalar first-failure checks with a different right
  continuation, including depths extending beyond each certified prefix.

The return cones and finite torus checks establish the finite premises of
the proof; the reconstruction argument establishes the unbounded-depth
claim. The finite orbit checks control its indexing and sharpness.

```sh
uv run --no-project python experiments/rule30/r1_cylinder_deadline_audit.py
```
