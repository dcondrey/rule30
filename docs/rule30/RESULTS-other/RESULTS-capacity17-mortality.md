# A sharp uniform mortality theorem through two-step capacity 17

Date: 2026-09-13. Status: exact finite certificates proving the stated
all-length theorem, with an independent forward-row verification.

## 1. The theorem and its domain

Let `w` be any legal finite auxiliary Z frontier of original length `r` that
passes its first two chronological guards. Define

```text
Q_2(w) = |E_2(r, (s_0,s_1), Z^2(w))|,
N(w)   = number of successful updates before the first failed guard,
D(w)   = number of adjacent equal scalars in that successful tape.
```

`E_2` counts all legal originals of the SAME original length, with the SAME
two scalars and full second endpoint. It retains both chronological guards.
It is not a count of arbitrary current predecessors. See the
[original-fiber definition](RESULTS-canonical-merger-capacity.md).

**Theorem. For every original length r, if Q_2(w) <= 17, then w dies and**

```text
N(w) <= 24,                 D(w) <= 14.
```

Both constants are attained, already at capacity six. The original

```text
w = 20001 0^1633864,          r = 1633869,
successful tape = 001000001101001100000111,
Q_2 = 6,                     N = 24, D = 14
```

fails its next guard. Here concatenation and the power denote quaternary
symbols, not a binary integer. No assertion is made that this auxiliary
frontier is reachable from the singleton seed. This theorem does not prove
unrestricted finite-frontier mortality, period-two exclusion, or P1.

## 2. An exhaustive language classification, at every length

The [capped-count construction](RESULTS-bounded-capacity-language.md) retains
eight nonnegative inverse-path counts and the second bulk output pair.
Saturating every count at `K+1` is exact for acceptance with count at most K:
all transitions use nonnegative addition, so an excess cannot cancel.
Terminal acceptance tests both original guards and labels the exact count.

At K=17 its entire reachable graph closes at 62 states and 133 edges; 19
states can reach acceptance. Its complete accepted language is below. Each
`k` ranges independently over all nonnegative integers. Append the birth
suffix to obtain the FULL second endpoint. N and D include the initial two
scalars, not just updates after this endpoint.

| Second bulk output | Initial scalars | Birth suffix | Q_2 | Max N | Max D |
|---|---|---|---:|---:|---:|
| `21210` | `01` | `32` | 6 | 2 | 0 |
| `21213(13)^k` | `00` | `03` | 6 | 24 | 14 |
| `21213(13)^k0` | `11` | `32` | 12 | 3 | 1 |
| `213(13)^k` | `00` | `03` | 6 | 2 | 1 |
| `213(13)^k0` | `11` | `32` | 12 | 2 | 1 |
| `3` | `10` | `03` | 1 | 2 | 0 |
| `303` | `00` | `03` | 2 | 3 | 1 |
| `3030` | `11` | `32` | 12 | 3 | 1 |
| `3031(31)^k3` | `00` | `03` | 6 | 17 | 9 |
| `3031(31)^k30` | `11` | `32` | 12 | 3 | 1 |
| `3210` | `01` | `32` | 12 | 2 | 0 |
| `32100(0)^k` | `01` | `32` | 12 | 4 | 1 |
| `321210` | `01` | `32` | 12 | 3 | 0 |

There are no other positive two-step capacities at most 17: only 1,2,6,12
occur. This is an all-length exclusion, not a short-word census.

The pattern grammar is converted to a separate epsilon-NFA. Its complete
reachable product with the counted automaton has 74 states and 296 edges.
Every product state agrees on the entire set of `(s_0,s_1,exact count)`
acceptance labels. Closure under all four input symbols proves equality of
the labeled languages at all lengths. A further independent check enumerates
10,922 legal originals of lengths 1 through 7 using frozen forward updates,
and compares all 68 nonempty two-step fibers with the inverse counts. This
last check validates the implementation against a different formulation;
the closed-product argument supplies the unbounded-length conclusion.

## 3. Closing the previously unresolved six-ancestor family

The previous report stopped the family `21213(13)^k03` at a declared spatial
period cap of 262,144. That was an incomplete computation, not a failure of
mortality. The new certificate closes the full spatial column at every
further temporal depth through 23.

A depth-n column stores the original high bit and both bits in each of n
bulk scans. Read the prefix, then repeatedly apply the deterministic
column map of the block `13`. Exact return to the initial FULL column
certifies its period P_n, so every nonnegative k is represented modulo P_n.
Reading the terminal suffix and testing the full chronological signature
includes all guards and every birth symbol, not only the last guard.

| Further depth n | Closed block period P_n | Surviving k modulo P_n |
|---:|---:|---|
| 19 | 262144 | 30500, 194340 |
| 20 | 524288 | 194340, 292644 |
| 21 | 524288 | 292644 |
| 22 | 1048576 | 816932 |
| 23 | 1048576 | none |

The final empty residue set proves that every endpoint in this infinite
family has at most 22 further successes, hence at most 24 from its original.
The independent checker computes repeat counts throughout all surviving
histories, including branches that die earlier, and finds maximum 14.

The [six-prefix ancestor identity](RESULTS-bounded-capacity-language.md#4-six-ancestors-can-support-twelve-repeats)
is exact for all k:

```text
{20001,20020,20021,21001,21020,21021} 0^(2k)
    --00--> 21213(13)^k03, with complete original fiber size six.
```

At `k=816932`, the surviving depth-22 residue gives the stated sharp
original and complete tape. The older `k=30500, D=12` witness remains valid
but is no longer the strongest known lower bound on B(6). We now have
`B(6)=14` for the qualitative repeat-budget definition on Q_2<=6.
Consequently a no-prefactor bound `Q_2 >= 2^(epsilon D)` requires
`epsilon <= log_2(6)/14`, approximately 0.18464. A free fixed additive
constant in the exponent can absorb this finite witness.

## 4. Why the second checker verifies a uniform theorem

The primary engine is a C++ full-column orbit scanner. The independent
checker does not import its column transition or its signature function.
It builds two complete spatial periods and evolves whole bulk rows with the
unchanged `panel/cert33.py` forward oracle. It then evolves the growing birth
suffix separately for every residue, testing each chronological guard and
reconstructing every successful scalar tape.

At each depth both endpoint bits return after the asserted period. All
lower layers have already been checked and their periods divide this one.
Thus the entire column state returns. Determinism proves repetition beyond
the two displayed periods. The checker verifies all residues, all preceding
guards, complete tapes, and repeat maxima. It also checks primary source
hashes. A period cap, a nonreturn, or surviving final residues is rejected
as an incomplete proof. The six finite exceptions and all seven periodic
patterns in the table are checked; the maximum over this exhaustive table
proves the theorem.

These are reproducible computational proofs with explicit mathematical
closure arguments, not a proof-assistant formalization.

## 5. The next obstacle appears at capacity 18

The complete K=32 counted graph has 90 states and 196 edges. A separate
147-state, 588-edge closed product verifies its 40 labeled patterns.
Seven patterns, first appearing at exact capacity 18, contain TWO free
repetition parameters. Their second bulk outputs include:

```text
21213(13)^a031(31)^b3       [00]
21213(13)^a1213(13)^b       [00]
213(13)^a031(31)^b3         [00]
213(13)^a1213(13)^b         [00]
3031(31)^a213(13)^b         [00]
3031(31)^a3031(31)^b3       [00]
30322(2)^a100(0)^b          [01]
```

Here a,b are arbitrary nonnegative integers; append `03` for scalar pair
`00`, and `32` for `01`. Classification proves exact capacities and
coverage, not mortality of these families.

**Concrete next obligation:** close the joint action of the two repeated
blocks, carrying the seam column, then test the full suffix and all guards
over the entire reachable joint state set. Testing one diagonal a=b, a
bounded rectangle, or independent marginal phases cannot certify the whole
family. Begin with `213(13)^a1213(13)^b03`: its first repeated block alone
belongs to a family that dies immediately, so its seam exposes exactly how
another block can change the terminal guard. This is a research choice,
not a proved ranking of difficulty. A successful uniform certificate for
each new family would extend the capacity theorem. A survivor at a finite
depth would only enlarge its lower bound.

The broader hypothesis remains: for every K there is finite B(K), uniform
over all original lengths with Q_2<=K. This would imply all auxiliary
mortality and hence provide a sufficient route to the period-two rung.
It is stronger than mortality, since fixed K still allows unbounded
original length. The weakest period-two separator remains a separate target;
failure of this stronger capacity program would not refute that separator.

## 6. Reproduction and artifacts

From the repository root, with a C++17 compiler available:

```sh
uv run --no-project --with numpy python experiments/rule30/capacity_language_decomposition.py --cap 17
uv run --no-project --with numpy python experiments/rule30/capacity_language_decomposition.py --cap 32
uv run --no-project --with numpy python experiments/rule30/capacity17_mortality.py
```

The aggregate verification took about 11 seconds in the saved run. Its
per-family scanner has a 120-second wall budget and explicit period/depth
caps; incomplete work cannot set its uniform-proof flag.

- [All-length capacity-17 language](../../experiments/rule30/capacity-17-language.json)
- [Aggregate mortality certificate and source hashes](../../experiments/rule30/capacity17-mortality-certificate.json)
- [Independent whole-row checker](../../experiments/rule30/verify_six_ancestor_family.py)
- [Full-column scanner](../../experiments/rule30/six_ancestor_family_orbit.cpp)
- [Capacity-32 classification and the two-parameter frontier](../../experiments/rule30/capacity-32-language.json)

No prize problem is claimed solved, and no universal statement about other
capacities is inferred from the completed cases.
