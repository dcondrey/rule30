# Draft public question: a four-symbol transducer orbit

Targets: MathOverflow; Wolfram Community Rule 30 thread.  **Draft only; do
not post without review.**

**Question.** Let (A=\{0,1,2,3\}), let (B=(3,2,1,0)), and define
(g_s:A\to A) by the table whose rows (s=0,1,2,3) are respectively
((0,3,2,3),(1,2,3,2),(3,1,1,1),(2,0,0,0)).  For
(a\in\{0,1,2\}), define a one-sided sequential transducer (T_a:A^{\mathbb
N}\to A^{\mathbb N}) by (T_a(x)_0=a) and
(T_a(x)_j=g_{x_j}(T_a(x)_{j-1})) for (j\ge1); for a finite word
(u=a_1\cdots a_m), put (T_u=T_{a_m}\circ\cdots\circ T_{a_1}), and for
(c\in\{2,3\}) write (Q_c(u)=T_u(c^\omega)).  Thus the finite transducer
orbit is (O_c=\{Q_c(u):u\in\{0,1,2\}^*\}).  Independently, define
(\phi:A^2\to A) by the rows
((0,1,3,2),(3,2,1,0),(3,2,0,1),(3,2,1,0)), let
(H=\{e\in\{1,2\}^{\mathbb N}:11\text{ never occurs in }e\}), and define
(I(e)=(r^t_0)_{t\ge0}) from the triangular recurrence
(r^0_i=B(e_i)), (r^1_i=\phi(e_i,r^0_{i+1})), and
(r^t_i=\phi(r^{t-2}_{i+1},r^{t-1}_{i+1})) for (t\ge2).  The set
(I(H)) is the inverse-terminal image of the hard-core subshift.  Is
(O_c\cap I(H)=\varnothing) for both (c=2) and (c=3), and is there a
standard automata-theoretic or symbolic-dynamical way to prove this
disjointness?  As a check on the definitions, (I(2^\omega)=(12)^\omega),
while (T_0(2^\omega)=0311\ldots), since
(g_2(0)=3,g_2(3)=1,g_2(1)=1); this illustrates one hard-core image and one
one-letter orbit calculation without deciding their intersection.
