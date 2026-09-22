# Exact limits of a pointwise braid lift and a D8 interchange

Date: 2026-09-14. **No Yang–Baxter map, even on an infinite hidden set, can
have the prescribed Rule 30 block operation as its pointwise visible first
output on all inputs.** Separately, a genuine D8 group interchange preserves a
temporal endpoint but creates a persistent neighboring-column defect in the
actual initial context. That defect cannot be moved through another column by
a driver-independent invertible boundary change.

These are precise exclusions of particular interchange models. They do not
exclude other encodings, blocked or restricted-context constructions,
parameter-dependent visible interactions, spectral matrix identities, or P3
algorithms. No faster marked query follows from the group interchange.

## 1. Physical digits, permutation actions, and the proposed lift

Let D={0,1,2,3}, with arithmetic modulo 4, and define

```
M_0(x)=-x,     M_1(x)=x+1,     M_2(x)=M_3(x)=3-x.             (1)
```

These are the exact chronological column actions in the
[incoming-profile construction](RESULTS-p3-heisenberg-column-profiles.md):
`x_t=M_(w_t)(x_(t-1))`, with entering digit zero for each actual column.
We also write A=M_0, B=M_1 and C=M_2=M_3.

The visible two-input operation is

```
F(a,b)=M_a(b),                                              (2)
```

with the driver listed first. In binary block notation it is the same
Rule 30 two-cell operation, with the two arguments ordered to match (2).
The physical output is fixed; an auxiliary second output may be chosen.

Consider any set S, any surjection pi:S->D, and any map R:S^2->S^2 satisfying

```
pi(R(s,t)_1)=F(pi(s),pi(t))   for every s,t in S.             (3)
```

No finiteness, injectivity, or bijectivity of R is assumed. Hidden data may
be arbitrarily large. The proposed braid equation is

```
R_12 R_23 R_12 = R_23 R_12 R_23  on S^3,                    (4)
```

where R_12 and R_23 act on the indicated pair. Either chronological or
ordinary composition notation yields the same two palindromic words in (4).

## 2. No hidden completion with that first visible output exists

**Theorem.** Conditions (3) and (4) are incompatible.

**Proof.** Fix hidden x,y with visible values a,b, and put
`d=pi(R(x,y)_2)`. This d may depend on all their hidden data. Crucially, it is
fixed when a third hidden input z varies. Write c=pi(z).

The visible first coordinate of the left side of (4) is

```
M_(M_a(b))(M_d(c)),
```

whereas the visible first coordinate of the right side is

```
M_a(M_b(c)).
```

Thus surjectivity of pi forces

```
M_(M_a(b)) M_d = M_a M_b  as permutations of D.              (5)
```

Choose a=0 and b=1, which surjectivity also permits. Then
`M_0(1)=3` and `M_0 M_1=C`. Equation (5) becomes

```
C M_d=C.
```

Since C is invertible, M_d would be the identity. None of the four actions
in (1) is the identity. This contradiction proves the theorem.

The proof does not require choosing or searching hidden states, nor does it
assume that the second output is visible-data-dependent. Its obstruction is
already in the mandatory first coordinate. Adding central cover coordinates
cannot fix it while (3) remains true on every pair.

The scope of (3) matters. This is not a theorem against every hidden-state
integrable representation of Rule 30: a different visible gate, restricted
admissible pairs, a changed blocking, or a parameter-dependent visible action
need not obey this hypothesis. Nor does it address Yang–Baxter equations for
linear operators on tensor spaces merely because they share the same name.

## 3. A genuine group interchange and what it preserves

The actions (1) lie in

```
G=D8={x -> epsilon*x+a : epsilon in{+1,-1}, a in D}.
```

For any group define the Hurwitz map

```
H(g,h)=(h,h g h^(-1)).                                    (6)
```

A chronological pair g then h has endpoint action h g. The new pair has
endpoint `(h g h^(-1)) h=h g`, so (6) preserves its action on every entering
state. It also satisfies the braid equation. Both three-factor sides send
(g,h,k) to

```
(k, k h k^(-1), k h g h^(-1) k^(-1)).                       (7)
```

These algebraic identities prove the full statement, with no finite-depth
inference. They do not contradict section 2, because the group map (6) does
not have the prescribed visible first output (3).

The physical driver family in (1) is not closed under (6). On the first two
actual drivers 1,2, whose actions are B,C, the new pair is

```
(C, C B C^(-1))=(C,B^(-1)).                                (8)
```

The translation B^(-1):x->x-1 is not any M_d. For entering digit zero the two
successive state values are

```
original: 1,2;       after (8): 3,2.                        (9)
```

The endpoint agrees and the one intermediate output changes. Replacing the
nonphysical group label by extra physical factors would change the number of
time steps and is not a free interchange of an actual history.

## 4. The changed intermediate output has a permanent actual-context effect

Let z_0,z_1,z_2 be the actual chronological column words from the zero orbit,
with the virtual preceding column equal to the constant word 1. In particular

```
z_0=(1230)^infinity,      z_1 starts 1,2,
T_0(z_0)=z_1,            T_0(z_1)=z_2.                      (10)
```

Apply (8) only to the first two group actions driven by z_0 and retain the
subsequent actions. By (9), the changed output word z'_1 differs from z_1
only at time 1, where it is 3 instead of 1. From time 2 onward the states
are identical because the endpoints and all later drivers agree.

In the next spatial column, both entering states are zero. Its first state
therefore changes from `M_1(0)=1` to `M_3(0)=3`. Every later driver is common,
and every physical action obeys

```
M_d(x+2)=M_d(x)+2 mod4.                                    (11)
```

Consequently

```
T_0(z'_1)_t = z_(2,t)+2 mod4  for every t>=1.                (12)
```

This is an exact persistent high-bit flip, not a short temporal boundary
transient. The source context in (10) is actual; the modified construction
is a proposed interchange of it and is not asserted to be a second actual
singleton trajectory. The theorem shows why preserving one temporal endpoint
is insufficient to preserve a marked cell in the neighboring column.

## 5. No invertible boundary gauge independent of the current driver

One possible repair of (12) would move a uniform driver flip `u->u+2` through
a column using invertible changes gamma,delta of its entering and exiting
state, independent of the current u. The required identity is

```
M_(u+2) gamma = delta M_u   for every u in D.                (13)
```

Here gamma and delta may be arbitrary permutations of D, not only elements
of D8. They may also vary with the time position; the assertion at a given
crossing requires them to be fixed as u varies.

There is no such pair. At u=0 and u=1 the left sides agree because M_2=M_3.
Hence `delta M_0=delta M_1`; injectivity of delta forces M_0=M_1, contrary to
(1). This excludes the stated driver-independent repair. A rule whose
parameter update depends on the actual current driver, or which retains
additional histories, lies outside this argument and still needs its own
construction and cost bound.

## 6. Exact verifier and remaining scope

The [verifier](../../experiments/rule30/p3_braid_interchange_audit.py) and
[artifact](../../experiments/rule30/p3-braid-interchange-audit.json) retain the
complete 16-visible-pair necessary-action table, its 64 coordinate identities,
and all 64 candidate second-output checks. The decisive pair 0,1 records a
specific failing third visible input for each proposed second output.

They also check the Hurwitz endpoint identity for all 64 D8 pairs and all
four incoming states, the actual pair in (9), and all 16 physical values in
(11). The four-column control consists of the virtual column and three actual
columns, using only eight time positions read from the existing
[prefix-orbit artifact](../../experiments/rule30/p3-autonomous-profile-bound.json).
The changed neighboring trace is evaluated and compared with (12); no actual
trajectory census or larger center prefix is generated. Source and report
hashes are recorded.

The maintained results distinguish a valid group endpoint identity, a
persistent trace defect, and an impossible pointwise hidden braid completion.
They supply neither a scaling theorem for driver-dependent interchanges nor a
new Rule 30 complexity or period exclusion.
