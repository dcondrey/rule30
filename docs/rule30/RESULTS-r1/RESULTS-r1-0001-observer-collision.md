# Driven 0001: the eight-cell prefix does not determine its observer forever

Date: 2026-09-15. **Exact finite counterexample to one blocking cylinder;
no all-width obstruction or Rule 30 prize result.**

The [three-prefix certificate](RESULTS-r1-0001-boundary-certificate.md)
leaves a binary observer at every four-step block. A tempting stronger
claim is that the zero-initial trajectory's eight-cell prefix at time
eight already determines that observer for every future time, regardless
of the initial continuation. This claim is false.

## The exact pair

Start a driven right half-line at time zero, with boundary
`c=(0001)^infinity`. Initial strings list sites 1,2,..., left to right.
Compare the two finite right rows

```text
u = 0010100000000 0000...   (packed integer 20),
v = 0010100010001 0000...   (packed integer 4372).
```

Both have prefix `00101000`. The second adds ones only at sites 9 and 13.
The first row is exactly the zero-initial driven trajectory's full row
at time eight, so restarting it preserves the drive phase. The second
is a different permitted continuation of the same eight-cell prefix;
it is not claimed to be reachable from the zero initial row.

Define the block observer `eta_j=s(4j,2)`. Since both rows start with
`A=0010`, the existing invariant applies from this starting time: `eta_j`
is the indicator of prefix `C=0111`, and

```text
(r_(4j), r_(4j+1), r_(4j+2), r_(4j+3)) = (0, eta_j, 1, 1).
```

Literal Rule 30 evolution gives:

| Relative block time | 0 | 4 | 8 | 12 | 16 | 20 | 24 |
|---|---|---|---|---|---|---|---|
| Observer from u | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Observer from v | 0 | 0 | 0 | 0 | 0 | 1 | 0 |

Thus the observer first differs at relative time 20; the corresponding
neighbour differs at time 21. When these starting rows are placed at
the original experiment's time eight, those times are 28 and 29.

## Why the first possible split is certified

The observer at relative time 20 is site 2, whose radius-one cone uses
only initial sites 1 through 22 and the prescribed boundary. Fixing the
first eight sites leaves exactly `2^14=16,384` initial exterior words.
The [verifier](../../experiments/rule30/r1_0001_observer_collision_audit.py)
exhausts all of them through time 20. For **every assignment**, an integer
implementation agrees with independent evaluation of the literal
eight-entry Rule 30 truth table on a shrinking cone. The scalar calculation
never supplies an artificial right boundary.

The observer-one counts at relative block times `0,4,8,12,16,20` are
exactly

```text
0, 0, 0, 0, 0, 512.
```

Consequently every infinite continuation of `00101000` has the same
observer through time 16, and time 20 is the earliest possible observer
split. Of the complete cones, 15,872 give history `000000` and 512 give
`000001`. This finite-cone argument quantifies over all infinite tails;
it does not refresh exterior bits independently at later times.

All fourteen single-one perturbations at sites 9 through 22 still give
history `000000`; more distant sites cannot affect this horizon. Therefore
two added bits are minimal for creating a split by time 20 relative to
the all-zero continuation. No later-horizon minimality is claimed.
The two displayed finite rows are additionally checked by independent
full finite-support evolution through time 24, including their expanding
right edges.

## Scope and reproduction

This excludes the specific eight-cell cylinder as a means of determining
the whole future observer. It also shows that five identical observer
samples do not select a unique next sample within this cylinder.
It does not exclude a wider blocking cylinder, a certificate retaining
temporal correlations, or regularity of the particular all-zero-tail
trajectory. The [known periodic cylinders](RESULTS-r1-periodic-cylinders.md)
under a different drive remain valid; no global no-cylinder conclusion
is intended.

```sh
uv run --no-project python experiments/rule30/r1_0001_observer_collision_audit.py
```

The [JSON artifact](../../experiments/rule30/r1-0001-observer-collision-audit.json)
records the counts, both witnesses, exact observed histories, and the
verifier hash. No longer simulation supports the claim.
