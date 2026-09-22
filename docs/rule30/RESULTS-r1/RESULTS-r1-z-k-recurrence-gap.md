# The Z/K staircase-data recurrence gap

Date: 2026-09-09. Evidence: **U** (exact symbolic identity), **C**
(finite independent check), **R** (an unclosed implication).

The reversed zero-cost map has an exact relation to the comoving Rule 30
map `K`, but this relation does not supply the finite recurrent point
needed by the new finite-K-recurrence obstruction. No Z mortality or R1
claim is made here.

## 1. Exact time shear

Use the reversed triangular coordinates from
`RESULTS-alt-trace-fiber.md`. At fixed indices, the bulk recurrence is

```text
b_k(n+1) = b_(k-1)(n+1) XOR (a_(k-1)(n) OR b_k(n))
a_k(n+1) = a_(k-1)(n+1) XOR (b_k(n+1) OR a_k(n)).
```

The boundary values at index -1 are zero. The first pair is
`a_0=1, b_0=beta`. Define a time-staggered field

```text
X_(2k)(tau)   = b_k(tau-k)
X_(2k+1)(tau) = a_k(tau-k-1).
```

**U:** Wherever all entries are defined, direct substitution gives

```text
X_i(tau+1) = X_(i-2)(tau) XOR
            (X_(i-1)(tau) OR X_i(tau)) = K(X(tau))_i.
```

For even indices this is the first recurrence, and for odd indices it
is the second. This is an exact relation between space-time fields. It
is not a conjugacy taking one Z row to one horizontal K row: different
coordinates on a K row use different Z times.

## 2. The initial data are on a staircase

For a Z state initially of active length `r`, site `k` is available when
`n>=0` and `k<=r+n-1`. The shear therefore defines the K field only where

```text
tau >= ceil(i/2),   tau >= i-r+1,
```

or equivalently `0<=i<=min(2*tau,tau+r-1)`. The original initial entries
appear at `(tau,i)=(k,2k)` and `(k+1,2k+1)`, not on a horizontal row.
The growing terminal edge becomes `i=tau+r-1`. After undoing the
comoving spatial shift this is a fixed spatial column, but identifying
it with a particular column of the original frontier construction
requires additional bookkeeping and is not asserted here.

Thus a finite initial Z state is not automatically a finite initial K
configuration. There is also no automatic zero extension: take the
smallest surviving Z state `a=(1), b=(1)`. The actual growing update
appends one pair and gives `a'=(1,1), b'=(1,0)`. If instead the initial
pair is padded by zeros and the autonomous bulk recurrence is used at
every index, its exact output is

```text
a'_k = 1 for all k>=0,
b'_0 = 1, b'_k = 0 for k>=1.
```

The natural zero-padded bulk extension immediately has infinite support.

## 3. Eventual prefix periodicity is insufficient

The finite-K-recurrence proof needs every finite prefix of the same
initial K row to lie on a cycle from time zero. Topological recurrence
supplies precisely that condition. The established Z fixed-prefix
result supplies eventual periodicity, which allows a transient before
the cycle. The time shear preserves this distinction.

The smallest explicit witness is the initial K row with a single 1 at
coordinate 0. Its two-cell prefix evolves

```text
(1,0) -> (1,1) -> (1,1) -> ... .
```

It becomes periodic, but cannot return to its initial prefix. Larger
fixed prefixes of the same row are also eventually periodic by
triangularity; this does not make the finite row recurrent.

Consequently, passing to recurrent limit points of prefix dynamics would
need a separate proof that the resulting full row retains finite
support. The new K theorem says a nonzero recurrent row cannot retain
that support; it does not imply that the initial finite row was itself
recurrent.

## 4. Verification and honest scope

The independent verifier checks the shear against the unchanged ladder
Rule 30 function on every autonomous Z start of widths 1 through 6. It
also checks the two smallest witnesses above. Run:

```sh
uv run python experiments/rule30/r1-isolated-column/z_k_shear_audit.py
```

Exact counts and the frozen ladder SHA-256 are saved in the adjacent
`z_k_shear_audit.json`. The finite check supplements the symbolic identity;
it does not establish an all-length survival assertion.

The exact remaining implication is:

> Does an immortal, legal zero-cost frontier force a nonzero finite
> horizontal K configuration to be recurrent?

No such implication has been proved. The explicit shear supplies neither
the horizontal finite configuration nor its recurrence. This report
does not rule out another transformation that might supply them, does
not construct an immortal Z orbit, and does not settle the vertical
centre-column obligation R1.
