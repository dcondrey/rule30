# Clock-40 preimage-collision obstruction

Date: 2026-09-09. Evidence: **U** (uniform symbolic reduction), **C**
(complete four-state calculation). This is an intermediate obstruction to
one proposed construction. It does not prove or kill R1, or settle P1.

## 1. Claim and scope

Let `B_t` be the Rule 30 evolution of the spatially 8-periodic row whose
left-to-right period is `11100000`. Its temporal period is exactly 40.
Consider a finite-radius lookup

    y(t,x) = g(t mod 40, x mod q, R90(t,x-R .. x+R)),

with any finite spatial lookup period `q`, applied to the actual Rule 90
lone-seed diagram. Require the all-zero input-window lookup to equal this
entire periodic background `B_t(x)` wherever those lookup entries occur.
The proposed construction additionally preserves the background centre
and copies the Rule 90 neighbour at phase 23, or complements it at phase
7, to obtain an aperiodic neighbour on centre zeros.

**U+C:** Neither proposal can work, for any finite radius or spatial
lookup period. In fact the analogous same-centre, toggled-neighbour pulse
is impossible at all four recurring pulse phases 7, 15, 31, 23. Section 7
strengthens this to every temporal or spatial shift of the same torus:
the three new one-step collision candidates all fail within two further
inverse steps.

Fixing only the centre clock, while allowing a different all-zero-source
background, is outside this claim. Other source encodings, multiscale
lookups, and general Rule 30 diagrams also remain outside it.

## 2. Clock and source pulse checks

Bits are indexed with the least significant bit at spatial coordinate 0.
The comoving map

    K(y)_i = y_(i-2) XOR (y_(i-1) OR y_i)

has the ring-8 cycle `7 -> 19 -> 123 -> 18 -> 126 -> 7`; bit 7 is zero
throughout. The ordinary Rule 30 orbit starting at 7 has period 40, and
`B_t(-1-t)=0` for every time. The finite verifier checks one whole period,
which proves these periodic assertions by deterministic evolution.

At phase 7, `(c,r)=(0,1)`; at phase 23, `(c,r)=(0,0)`. Thus the proposed
complement/copy choices match the all-zero-source background.

For the Rule 90 lone seed, its neighbour is 1 exactly at `t=2^n-1`.
For `n>=3`, these times have phases `7,15,31,23`, cycling with `n mod 4`.
Each phase therefore contains infinitely many pulses with unbounded gaps.
The restriction to any one of these arithmetic progressions is not
eventually periodic: an eventually periodic binary sequence with
infinitely many ones has bounded gaps. Complementing it also preserves
nonperiodicity. This validates the proposed signal; feasibility is the
step that fails.

## 3. Uniform preimage reduction

**U, generic lemma:** Every full-line preimage of a spatially `q`-periodic
output under Rule 30 is spatially periodic with a period `m*q`, where
`1<=m<=4`.

The equation `F(a)_i=b_i` gives the deterministic inverse step

    a_(i-1) = b_i XOR (a_i OR a_(i+1)).

Advancing this inverse recurrence through one output period gives a
function on the four states `(a_i,a_(i+1))`. A full-line preimage induces
a bi-infinite orbit of this finite function. Such an orbit must stay on
a cycle: a transient state has bounded ancestry depth. Each cycle has
length at most four. A state on a cycle determines both the inverse
extension and its unique continuation around that cycle, so the cycle
enumeration lists every full-line preimage. This also excludes
aperiodic preimages of a periodic output; it is not just a ring scan.

**U, factor reduction:** At `t=2^n-1`, the Rule 90 row equals the
checkerboard with ones at odd positions throughout its light cone.
At `t+1=2^n`, its row is zero strictly between the two endpoints. For
fixed finite factor radius, and arbitrarily large `n` in any of the four
pulse phases, every fixed finite spatial interval consequently sees the
same checkerboard input at time `t` and zero input at `t+1`.

The lookup at the fixed phase defines a full-line periodic row `A` from
that checkerboard. The required local Rule 30 identities imply

    F(A) = B_(phase+1).

One may justify each coordinate by choosing a sufficiently large pulse;
no bounded-window inference about an unknown eventual trace is used.
The desired pulse additionally needs `A_0=B_phase(0)` and
`A_1 != B_phase(1)`. We now list every preimage and find none satisfying
these requirements.

## 4. Complete finite certificate

The state integer is `a_0 + 2*a_1`. Each map below sends this pair eight
positions to the left. Words are left-to-right from coordinate 0.

| Phase | Background integer | Next row | Backward 8-step map on states 0,1,2,3 | All full-line preimages |
|---:|---:|---:|---|---|
| 7 | 246 | 18 | `[2,2,2,2]` | `01101111` |
| 15 | 14 | 19 | `[2,2,2,2]` | `01110000` |
| 31 | 38 | 123 | `[2,2,2,2]` | `01100100` |
| 23 | 36 | 126 | `[0,1,1,1]` | `00100100`, `10010011` |

All cycles are fixed points, so all preimages already have period 8.
There are no extra preimages of periods 16, 24, 32, or any other period.
At phases 7, 15, 31, the sole preimage is the background itself. At phase
23, both preimages have neighbour 0; the additional preimage changes the
centre from 0 to 1. Thus all four necessary pulse collisions fail.

This initial gate checks 16 inverse-map states, independently scans
1,024 ring-8 rows, and verifies the 40-step clock and all five preimages
using the unchanged ladder engine: 8,552 Rule 30 cell updates. The
verifier additionally checks the whole-torus strengthening in section 7;
the combined counts are recorded in its JSON. The unchanged engine's
SHA-256 is checked before use.

## 5. Rule 90 control and reproduction

The generic inverse-periodicity lemma alone does not distinguish the
rules. The explicit four-state maps above use Rule 30's OR term. Under
the unchanged ladder Rule 90 function, both `00000000` and `01010101`
map to `00000000`; they agree at the centre and disagree at the
neighbour. Thus the needed preimage collision exists for Rule 90.
The verifier checks these 16 control updates directly.

Run from the repository root:

```sh
uv run python experiments/rule30/r1-isolated-column/clock40_preimage_collision.py
```

Exact rows, inverse maps, all preimages, counts, and the frozen engine
hash are saved in
`experiments/rule30/r1-isolated-column/clock40_preimage_collision.json`.

## 6. Honest scope

This is a uniform obstruction to the specified periodic-background
lookup construction, covering every finite radius and spatial lookup
period. It is not an extrapolation from finitely many SAT instances.
It does not show that all periodic backgrounds fail the collision gate,
and it does not establish any eventual-periodicity conclusion about the
Rule 30 lone seed. R1 remains open; the research program continues.

## 7. Every clock shift fails within two further inverse steps

**U+C:** The same construction is impossible for every temporal and
spatial shift of this torus background. Enumerating the complete
full-line preimages at all 40 phases leaves precisely three phases with
a centre-zero, toggled-neighbour alternative. Their backward extensions
are forced as follows:

| Old clock phase | Alternative pulse row | Its unique predecessor | Required predecessor centre | Outcome |
|---:|---|---|---:|---|
| 3 | `00111001` (156) | `11001101` (179) | 0 | predecessor centre is 1 |
| 8 | `00100111` (228) | `10111001` (157) | 0 | predecessor centre is 1 |
| 39 | `01000000` (2) | `01111111` (254) | 0 | this step survives |

For the last row, the next unique predecessor is `01001001` (146),
whose centre is 0; old clock phase 37 requires centre 1. Thus this branch
also dies, at backward distance two. The four backward eight-step maps
in this table and final step are respectively `[3,3,3,3]`,
`[3,1,1,1]`, `[1,2,2,2]`, `[1,2,2,2]`. Their sole cyclic states prove
uniqueness among all full-line preimages, including every spatial period.

The preceding lookup rows exist as exact central limits of the Rule 90
source. At times `2^n-1`, `2^n-2`, `2^n-3`, the local source patterns,
throughout arbitrarily wide central intervals as `n` grows, are the
8-periodic words `01010101`, `00100010`, `00010100`, respectively.
The Lucas no-carry formula proves these by inspecting the low bits of
`2^n-d`; their Rule 90 images are successively the preceding words and
then zero. For any fixed lookup radius, substituting each periodic
pattern therefore defines a full-line row. The local Rule 30 identities
force the predecessor relations above, and eventual centre periodicity
forces their centres to equal the corresponding clock bits. No
assumption that a bounded window determines an unknown trace is used.

Every spatial rotation of the initial 8-bit word already occurs in the
40-step ordinary Rule 30 orbit. This is checked directly; equivalently,
the comoving period 5 and spatial period 8 are coprime. Therefore adding
spatial shifts introduces no further clock cases.

This strengthening remains specific to this torus as the entire
all-zero-source background. It does not exclude other clocks or prove
that a general periodic-centre diagram has a periodic neighbour.
