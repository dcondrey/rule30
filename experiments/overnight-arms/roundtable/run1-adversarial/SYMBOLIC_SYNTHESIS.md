# Symbolic roundtable: candidate research directions on Rule 30

Status: **UNEXECUTED PROPOSALS, NOT RESULTS.**  This panel's job was to
FORMULATE directions worth someone's time, not to prove or verify
anything.  Nothing below is PROVED, MEASURED, or even necessarily
internally consistent by virtue of a model having proposed it.  Every
entry needs the same treatment as any other route in `PATH.md`: a
kill condition, a Rule 90 check run in actual code, and an owner before
any compute is spent on it.  Treat this document as an intake list for
triage, ranked by no one yet.

Calls: 12 (0 errored). Roster (final model per slot,
after any live swaps):
- `openai/gpt-5.6-terra-pro` (GPT-5.6): deep System-2 formal logic and proof trees
- `deepseek/deepseek-v3.2` (DeepSeek-V4): RL reasoner for circuit-complexity verification
- `x-ai/grok-4.6` (Grok-4.6): lateral mathematical reasoning, unconstrained algebraic exploration
- `meta-llama/llama-4-scout` (Llama-4-Maverick): open-weights anchor for adversarial verification

**Live model swaps during the run:**
- DeepSeek-V4: `deepseek/deepseek-v4-pro-0813` -> `deepseek/deepseek-v4-pro` at call ? (response yielded no extractable content (see run.log))
- DeepSeek-V4: `deepseek/deepseek-v4-pro` -> `deepseek/deepseek-v4-flash-0731` at call ? (response yielded no extractable content (see run.log))
- DeepSeek-V4: `deepseek/deepseek-v4-flash-0731` -> `deepseek/deepseek-v3.2` at call ? (response yielded no extractable content (see run.log))
- Llama-4-Maverick: `meta-llama/llama-4-maverick` -> `meta-llama/llama-4-scout` at call ? (response yielded no extractable content (see run.log))

## Candidate directions surfaced (unverified, unexecuted)

- **GPT-5.6-H1.0**: global periodic-trace fibre rigidity).}
\]
Let \(F=F_{30}\), \(e=\delta_0\), and for \(p,q\ge1\) define the full (not
fixed-strip) trace fibre
\[
X_{p,q}:=\left\{x\in\{0,1\}^{\mathbb Z}:
(F^{t+p}x)_0=(F^t x)_0\ \forall t\ge q\right\}.
\]
Seek a classification theorem for the connected component, under finite
spacetime defects, of \(X_{p,q}\):
\[
e\in X_{p,q}\quad\Longrightarrow\quad
\exists\,L,R<\infty:\ 
F^q(e)\big|_{(-\infty,-L]\cup[R,\infty)}
\in \mathcal A_{p},
\]
where \(\mathcal A_p\) is a finite union of spatially eventually periodic
asymptotic phases forced by the \(p\)-periodic temporal boundary.

Target contradiction:
\[
F^q(e)\ \text{has two propagating finite-support interfaces}
\quad\notin\quad \mathcal A_p .
\]
Mechanism: solve the periodic trace constraint as an infinite half-plane
subshift and prove an \emph{interface conservation/creation law} specific to
\[
f_{30}(a,b,c)=a\oplus(b\vee c),
\]
rather than a bounded-width ladder.  This is intended to evade obstruction
A/F: the proposed object is the entire periodic-trace fibre and its
asymptotic components, not propagation from a trace through depth \(R\).

\[
\textit{Rule-90 screen:}\qquad
f_{90}(a,b,c)=a\oplus c
\]
admits the lone-seed trace \( (F_{90}^t e)_0=0\) for \(t>0\); hence its
corresponding fibre must contain the finite-defect Sierpiński interface.
Thus the required interface-rigidity lemma is necessarily false for Rule
90, plausibly because additive cancellation preserves a zero temporal trace
without forcing an asymptotic phase.
- **GPT-5.6-H1.1**: point-specific \(\omega\)-limit classification for P2).}
\]
Let
\[
\Omega(e):=\bigcap_{N\ge0}\overline{\{F^t e:t\ge N\}},
\qquad
\mathcal M_e:=\{\mu:\mu\text{ is }F\text{-invariant and }
\operatorname{supp}\mu\subseteq\Omega(e)\}.
\]
Propose a classification/reduction:
\[
\forall\mu\in\mathcal M_e,\qquad \mu[x_0=1]=\tfrac12,
\tag{\(\star\)}
\]
together with uniqueness of this one-site marginal on \(\Omega(e)\), or a
weaker uniform Cesàro statement
\[
\sup_{x\in\Omega(e)}
\left|\
- **DeepSeek-V4-H2.0**: periodic-trace fibre rigidity with interface conservation.}
\]
Let \(F=F_{30}\), \(e=\delta_0\). For \(p,q\ge1\) define the full trace fibre
\[
X_{p,q}:=\{x\in\{0,1\}^{\mathbb Z}: (F^{t+p}x)_0=(F^t x)_0\ \forall t\ge q\}.
\]
Proposed classification: if \(e\in X_{p,q}\) then \(\exists L,R<\infty\) such that
\(F^q(e)|_{(-\infty,-L]\cup[R,\infty)}\in\mathcal A_p\), where \(\mathcal A_p\) is a finite union of spatially eventually periodic asymptotic phases forced by the \(p\)-periodic temporal boundary condition. Target contradiction: \(F^q(e)\) has two propagating finite-support interfaces \(\notin\mathcal A_p\).

Mechanism: treat the periodic trace constraint as an infinite half-plane subshift and prove an interface conservation/creation law specific to \(f_{30}(a,b,c)=a\oplus(b\vee c)\). This evades obstructions A/F by working on the entire fibre rather than propagation through bounded depth \(R\).

Rule-90 screen: \(f_{90}(a,b,c)=a\oplus c\) gives lone-seed trace \((F_{90}^t e)_0=0\) for \(t>0\); its fibre contains the finite-defect Sierpiński interface. The required interface-rigidity lemma is necessarily false for Rule 90 because additive cancellation preserves a zero temporal trace without forcing an asymptotic phase.
- **DeepSeek-V4-H2.1**: point-specific \(\omega\)-limit classification for P2.}
\]
Define
\[
\Omega(e):=\bigcap_{N\ge0}\overline{\{F^t e:t\ge N\}},\qquad
\mathcal M_e:=\{\mu:\mu\text{ is }F\text{-invariant and }\operatorname{supp}\mu\subseteq\Omega(e)\}.
\]
Proposed classification: \(\forall\mu\in\mathcal M_e,\ \mu[x_0=1]=\frac12\) \((\star)\), together with uniqueness of this one-site marginal on \(\Omega(e)\), or the weaker uniform Cesàro statement
\[
\sup_{x\in\Omega(e)}\left|\frac1T\sum_{t=0}^{T-1}(F^t x)_0-\frac12\right|\to0.
\]
Mechanism: exploit the specific structure of \(\Omega(e)\) as a single orbit closure rather than a full measure set, converting the measure-zero gap (obstruction E) into a classification problem. This is the route shaped against obstruction E (row 8).

Rule-90 screen: for Rule 90, \(\Omega(e)\) is the singleton \(\{0^\infty\}\) and \((\star)\) fails (\(0\neq\frac12\)). The classification is trivially false, so the direction does not prove too much.
- **Grok-4.6-H3.0**: nonlinear spacetime series, rationality obstruction for P1.
Let \(u_{t,i}=(F_{30}^t e)_i\), \(G(x,z)=\sum_{t,i}u_{t,i}x^i z^t\in\mathbb F_2[[x^{\pm1},z]]\), and \(A(z)=[x^0]G=\sum_t(F^t e)_0 z^t\). On \(\mathbb F_2\), \(b\vee c=b+c+bc\), so the local rule is the quadratic identity
\[
u_{t+1,i}=u_{t,i-1}+u_{t,i}+u_{t,i+1}+u_{t,i}u_{t,i+1}.
\]
This lifts to a quadratic relation \(Q(G)=0\) in \(\mathbb F_2[[x^{\pm1},z]]\). \emph{Conjecture:} no rational \(A=P/Q\) can arise as the \(x^0\)-section of any \(G\) solving \(Q(G)=0\) with \(\operatorname{supp}G_0=\{\,0\,\}\). Target: a coefficient-wise obstruction (e.g.\ unbounded Hankel rank of \(A\), or a Mahler/Christol inequation that all rationals violate) derived from the bilinear term alone, not from any finite spacetime window.

Evades A/F (identity in the full series ring, no depth-\(R\) propagation) and H (the obstruction is algebraic, not a finite residual). Evades C: the object is the column series itself.

\textit{Rule-90 screen:} \(f_{90}\) drops the \(bc\) term; \(Q\) becomes linear and is solved by the Sierpiński generating function whose \(x^0\)-section is \(A_{90}=1\), rational. Any proof that does not use the quadratic monomial therefore proves too much and is low-priority.
- **Grok-4.6-H3.1**: time-bounded Kolmogorov of the prefix (P3, also P1).
Let \(a_t=(F^t e)_0\) and \(K^T(w)=\min\{|\pi|:\ U(\pi)\) outputs \(w\) in \(\le T\) steps\(\}\). \emph{Conjecture:} there is \(c>0\) such that
\[
K^{o(n)}(a_{[0,n)})\ge cn\qquad(n\to\infty).
\]
Mechanism: the first-1 loci of the two light-cone interfaces source a family of \(\vee\)-products whose supports in the unfolding DAG are nested but whose bilinear factors are pairwise incompressible over \(\mathbb F_2\) (no additive cancellation). A short \(o(n)\)-time program would have to share those factors, contradicting the support nesting. This is sequential \emph{work} on one fixed string (program+time), not circuit size of a variable-input Boolean function, so G/T4 do not apply as stated; D is not invoked (no dyadic seam).

\textit{Rule-90 screen:} all bilinear factors vanish, \(a_{[0,n)}=10^{n-1}\), and \(K^{O(n)}(a_{[0,n)})=O(1)\). The conjectured bound is false for Rule 90.
- **Llama-4-Maverick-H4.0**: $f_{90}(a,b,c) = a \oplus c$
- **Llama-4-Maverick-H4.1**: $(F_{90}^t e)_0 = 0$
- **Llama-4-Maverick-H4.2**: $t > 0$
- **Llama-4-Maverick-H4.3**: $\omega$
- **Llama-4-Maverick-H4.4**: $\Omega(e)$
- **Llama-4-Maverick-H4.5**: $\{0^\infty\}$
- **GPT-5.6-H5.0**: nonlinear temporal-defect
- **DeepSeek-V4-H6.0**: nonlinear temporal-defect conservation law for P1.
Let \(F=F_{30}\), \(e=\delta_0\). Define the temporal defect along the centre column for a configuration \(x\):
\[
D_t(x) := (F^{t+1}x)_0 \oplus (F^t x)_0 \oplus (F^t x)_1 \oplus ((F^t x)_1 \wedge (F^t x)_2).
\]
From the local rule \(f_{30}(a,b,c)=a\oplus(b\vee c)=a\oplus b\oplus c\oplus bc\), we have \(D_t(x)=0\) identically. For the lone seed, \((F^t e)_1\) and \((F^t e)_2\) are the left- and right-interface bits. The identity becomes
\[
a_{t+1}\oplus a_t = (F^t e)_1 \oplus (F^t e)_2 \oplus ((F^t e)_1 \wedge (F^t e)_2).
\]
Summing over \(t\) from \(0\) to \(T-1\) telescopes the LHS to \(a_T\oplus a_0\). This yields a conserved quantity:
\[
a_T = a_0 \oplus \bigoplus_{t=0}^{T-1}\big[(F^t e)_1 \oplus (F^t e)_2 \oplus ((F^t e)_1 \wedge (F^t e)_2)\big].
\]
If the centre column were eventually periodic with period \(p\), then for large \(T\) the RHS must become periodic in \(T\) with the same period. This imposes a strong constraint on the asymptotic behaviour of the two interface columns. Prove that the interface columns cannot jointly satisfy this periodicity constraint because the ∧-term introduces a nonlinear correlation that prevents cancellation. Specifically, show that the sequence \(\{(F^t e)_1, (F^t e)_2\}_{t\ge0}\) has a certain "bilinear complexity" that grows unbounded, forcing the RHS to be aperiodic.

Evades A/F: the constraint is global (sum over all time), not a bounded-depth propagation. Evades C: directly involves the centre column. Evades D: the conservation law is exact for all \(T\), no missing composition lemma.

\textit{Rule-90 screen:} For \(f_{90}\), the local rule is \(a\oplus c\), so the defect identity becomes \(D_t^{90}(x) = (F^{t+1}x)_0 \oplus (F^t x)_0 \oplus (F^t x)_2 = 0\). For the lone seed, \((F^t e)_2=0\) for \(t>0\), so \(a_{t+1}\oplus a_t = 0\), giving \(a_t=0\) for \(t>0\) (periodic). The nonlinear ∧-term is absent, so the proposed bilinear complexity obstruction vanishes. The mechanism fails for Rule 90.
- **DeepSeek-V4-H6.1**: single-orbit closure as a Toeplitz system for P2.
Consider the orbit closure \(\Omega(e)\) of the lone seed under \(F_{30}\). Observe that the centre column \(a_t\) is generated by a deterministic finite automaton with two counters (the distances to the next 1 in the left and right interfaces). Conjecture that \(\Omega(e)\) is a Toeplitz system (i.e., can be described by a sequence of periodic patterns on successive scales). Specifically, the interfaces \((F^t e)_1\) and \((F^t e)_2\) have well-defined asymptotic densities \(\alpha,\beta\) (by P2 for the interfaces, which may be easier). The joint pattern of the three columns (centre, left interface, right interface) is Toeplitz-like with frequencies determined by \(\alpha,\beta\). Prove that any invariant measure \(\mu\) on \(\Omega(e)\) must have the same three-column frequencies, and that the centre density is a continuous function \(g(\alpha,\beta)\) of the interface densities. Then prove that \(g(\alpha,\beta)=1/2\) uniquely, using the nonlinear coupling from the ∧-term.

Evades E: works directly on the single orbit closure, not on full-measure sets. Evades C: involves the centre column explicitly.

\textit{Rule-90 screen:} For Rule 90, \(\Omega(e)=\{0^\infty\}\) is a singleton, the interface densities are 0, and \(g(0,0)=0\neq1/2\). The proposed functional relation \(g\) is false for Rule 90, so the direction does not prove too much.
- **Grok-4.6-H7.0**: Sierpiński–Duhamel representation of the bilinear defect field (P1, with a P3 corollary).

Write \(u_{t+1,i}=u_{t,i-1}\oplus u_{t,i}\oplus u_{t,i+1}\oplus\chi_{t,i}\) with \(\chi_{t,i}:=u_{t,i}u_{t,i+1}\in\mathbb F_2\) (Rule 150 linear part \(+\) defects). Lone seed \(u_{0,\cdot}=\delta_0\). Variation of constants over \(\mathbb F_2\):
\[
u_{t,0}=L_t[\delta_0]\oplus\bigoplus_{s<t}\bigoplus_{i\in\mathbb Z}K_{t-s,-i}\,\chi_{s,i},
\]
where \(K_n(j)=\binom{n}{(n+j)/2}\bmod 2\) on \(n+j\) even (Lucas/Sierpiński kernel; composition law is Lucas, so obstruction D is not invoked). Let \(M_T\) be the \(\mathbb F_2\)-incidence matrix of centre bits \((a_t)_{t\le T}\) against defects \(\chi|_{s<T}\). \emph{Conjecture:} \(\operatorname{rk}M_T\to\infty\), and moreover the only eventually periodic sequences in the column-space compatible with a \(\chi\) generated by \(f_{30}\) from \(\delta_0\) are those with \(\chi\) eventually vanishing on every light-cone section, which fails because the right nested triangles produce infinitely many \(11\)-pairs.

Evades A/F: kernel support is the full cone \(\Theta(t)\), not depth \(R\). Evades C/H: the object is the column series itself; unbounded rank is an algebraic identity, not a residual count. P3 corollary (conjecture): any algorithm computing \(a_n\) must materialise \(\Omega(n)\) independent Lucas-sections of \(\chi\), hence \(\Omega(n)\) work on the fixed unfolding (G/T4: sequential work on one DAG, not circuit size of a variable-input function).

\textit{Rule-90 screen:} \(\chi\equiv0\), \(a_t=0\) for \(t>0\), \(\operatorname{rk}M_T=0\). Any argument not using \(\chi\) proves too much.
- **Grok-4.6-H7.1**: Left-permutive skew-product cocycle over the centre column (P1 and a P2 reduction).

Left-permutivity: \(u_{t,-1}=a_{t+1}\oplus(a_t\vee u_{t,1})\). View \((a_t)_{t\ge0}\) as a base sequence and \(r_t:=u_{t,1}\) as a fibre. This defines a skew product
\[
\Phi_a:\ \{0,1\}^{\mathbb Z_{\ge0}}\to\{0,1\}^{\mathbb Z_{\ge0}},\qquad
(\Phi_a r)_t=F\bigl(a_t,r_t,\text{right-of-}1\bigr)
\]
with left ray a sliding-block function of \((a,r)\). \emph{Conjecture:} (i) if \(a\) is eventually periodic then the only \(r\) making \(\Phi_a\) consistent with a finite-support initial row is eventually periodic on the right, contradicting the two-interface geometry of \(F^t e\); (ii) every \(\Phi_a\)-invariant joining of \((a,r)\) on \(\Omega(e)\) has one-site marginal \(\tfrac12\) on \(a\), because the \(\vee\)-cocycle is unbiased on \(\{01,10,11\}\) once \(r\not\equiv0\).

Evades A/F: no fixed-width strip; the fibre is the full right ray. Evades E: the joining is supported on \(\Omega(e)\), not on Bernoulli. Bipermutative rigidity is not imported.

\textit{Rule-90 screen:} \(a\vee r\) is replaced by \(0\); \(\Phi_a\) is linear, \(a\equiv0\) (\(t>0\)) is consistent, \(r\equiv0\). The \(\vee\)-cocycle obstruction is empty.
- **Llama-4-Maverick-H8.0**: $F=F_{30}$
- **Llama-4-Maverick-H8.1**: $e=\delta_0$
- **Llama-4-Maverick-H8.2**: $p,q\ge1$
- **Llama-4-Maverick-H8.3**: $X_{p,q}:=\{x\in\{0,1\}^{\mathbb Z}:(F^{t+p}x)_0=(F^t x)_0~\forall t\ge q\}$
- **Llama-4-Maverick-H8.4**: $X_{p,q}$
- **Llama-4-Maverick-H8.5**: $e\in X_{p,q}~\Longrightarrow~\exists L,R<\infty: F^q(e)|_{(-\infty,-L]\cup[R,\infty)}\in\mathcal A_p$
- **GPT-5.6-H9.0**: periodic-trace return transducer on the full right ray.}
\]
For \(w\in\{0,1\}^{p}\), impose \(a_{t+p}=a_t=w_{t\bmod p}\) and use left-permutivity
\[
u_{t,-1}=a_{t+1}\oplus(a_t\vee u_{t,1})
\]
iteratively to reconstruct the entire left half-plane from the right-half-plane history
\(\rho_t=(u_{t,i})_{i\ge0}\).
Seek an exact \(p\)-step ray map
\[
\mathcal T_w:\{0,1\}^{\mathbb N_0
- **DeepSeek-V4-H10.0**: periodic-trace return transducer on the full right ray.}
For \(w\in\{0,1\}^{p}\), impose \(a_{t+p}=a_t=w_{t\bmod p}\) and use left-permutivity
\[
u_{t,-1}=a_{t+1}\oplus(a_t\vee u_{t,1})
\]
iteratively to reconstruct the entire left half-plane from the right-half-plane history \(\rho_t=(u_{t,i})_{i\ge0}\).  
Seek an exact \(p\)-step ray map
\[
\mathcal T_w:\{0,1\}^{\mathbb N_0}\to\{0,1\}^{\mathbb N_0},\qquad \rho_{t+p}=\mathcal T_w(\rho_t),
\]
defined by solving the left-permutive recurrence for \(u_{t,-1},u_{t,-2},\dots\) until the leftmost cell needed for \(u_{t+p,0}\) is determined, which depends only on \(\rho_t\) because the leftward propagation is deterministic and finite-per-step.  
Conjecture: \(\mathcal T_w\) is a finite-state transducer (its state is a bounded suffix of \(\rho_t\)) whose iteration on the actual right ray \(\rho_t\) from the lone seed must eventually become periodic in the spatial tail, contradicting the known two-interface structure (the right ray under \(F^t e\) is not eventually periodic in space).  
Evades A/F: the transducer consumes the full right ray, not a fixed-width strip; the state is a finite window but the map is exact for all future times.  
Evades D: the recurrence is exact, no missing composition law.  

\textit{Rule-90 screen:} For Rule 90, \(u_{t,-1}=a_{t+1}\oplus u_{t,1}\) (no \(\vee\)). The resulting transducer \(\mathcal T_w\) is linear; with \(a_t\equiv0\) for \(t>0\), the right ray \(\rho_t\) can be identically zero, which is a fixed point of \(\mathcal T_w\). Thus the contradiction fails.

---
- **DeepSeek-V4-H10.1**: bilinear defect accumulation as a superlinear work witness for P3.}
Let \(\chi_{t,i}=u_{t,i}u_{t,i+1}\) as in Dir. 7. Define the *defect influence set* for \(a_n\):
\[
I_n:=\{(s,i):K_{n-s,-i}=1 \text{ and } \chi_{s,i}=1\},
\]
where \(K\) is the Sierpiński kernel.  
Conjecture: \(|I_n|=\Omega(n)\) and, more strongly, the family \(\{\chi_{s,i}:(s,i)\in I_n\}\) is *pairwise independent* in the sense that no \(\mathbb F_2\)-linear combination of the corresponding kernel rows vanishes identically on the support of \(\chi\) generated from \(\delta_0\).  
Mechanism: any algorithm computing \(a_n\) must, in the sequential model where each \(\chi_{s,i}\) is a black-box gate, query at least \(|I_n|\) distinct \(\chi\)-gates because the kernel rows are linearly independent over the actual defect field. This yields an \(\Omega(n)\) work lower bound on the fixed unfolding DAG.  
Evades G/T4: the lower bound is on sequential work (gate queries) for a fixed input, not circuit size of a variable function. Evades H: the linear independence is an algebraic identity, not a finite residual.  

\textit{Rule-90 screen:} \(\chi\equiv0\), so \(|I_n|=0\) and the lower bound is false.

---
- **Grok-4.6-H11.0**: Keep the exact \(p\)-step left-permutive ray map
\[
\mathcal T_w:\{0,1\}^{\mathbb N_0}\to\{0,1\}^{\mathbb N_0},\qquad
u_{t,i-1}=u_{t+1,i}\oplus(u_{t,i}\vee u_{t,i+1}),
\]
but drop finite state. Let \(\mathcal R\) be the one-sided subshift of light-cone rays (support in \([0,t]\) at time \(t\), seed-compatible). \emph{Conjecture:} if \(w\) is purely periodic then \(h(\mathcal T_w(\mathcal R))<h(\mathcal R)\) (entropy drop sourced by the \(\vee\)-bias on \(\{01,10,11\}\)), so \(\mathcal T_w\) is non-surjective on \(\mathcal R\). Hence no infinite backward \(\mathcal T_w\)-orbit of the actual \(\rho\) can hit \(\delta_0\) in finite time (Garden-of-Eden on the ray, not on a strip).

Evades F: no truncation; entropy is global on \(\{0,1\}^{\mathbb N_0}\). Evades A: the map uses the full right cone, not \(O(\log t)\) diagonals. Evades D: the \(p\)-fold composition is the local rule iterated, not a named seam. Evades H: non-surjectivity is a closed identity on \(\mathcal R\), not a residual count.

\textit{Rule-90 screen:} \(\vee\) deleted \(\Rightarrow\mathcal T_w\) linear; \(h\) preserved; \(0^\infty\in\mathcal R\) is a fixed point. The entropy drop is empty.
- **Grok-4.6-H11.1**: Duhamel as in Dir.\ 7: \(A(z)=L[\delta_0]\oplus K\ast X\) in \(\mathbb F_2[[z]]\), with \(X=\sum\chi_{s,i}z^s\) the generating function of \(\chi=u\cdot\sigma_x u\) and \(K\) the Lucas/Sierpiński kernel (composition law known). If \(A\) were rational, deconvolution against lacunary \(K\) (support = 1-bits of \(n\)) would force \(X\) to have linear Newton polygon (degree \(\le C\cdot\mathrm{per}(A)\)). But \(\chi=u\cdot\sigma_x u\) is quadratic on a cone of width \(\Theta(t)\), so the Newton polygon of \(X\) is strictly superlinear unless \(\chi\) vanishes on a positive-density set of nested right-triangles. \emph{Conjecture:} these two Newton polygons cannot coincide for \(\mathrm{supp}\,u_0=\{0\}\).

Evades A/F: kernel support is the full cone. Evades C: the object is \(A\) itself. Evades H: the contradiction is a comparison of two entire polygons, not a finite Hankel rank. Evades D: Lucas is the composition law.

\textit{Rule-90 screen:} \(X\equiv0\), polygons are \(-\infty\), no clash.

\textbf{Open question}
\begin{enumerate}
\item Dir.\ 1: exhibit a strictly invariant (cylinder or measure of \(\vee\)-triples) proving \(h(\mathcal T_w(\mathcal R))<h(\mathcal R)\) for every \(w\in\{0,1\}^p\setminus\{0^p\}\), without a width cutoff.
\item Dir.\ 1: is \(\delta_0\)'s forward ray in the eventual image of \(\mathcal T_w^{\circ n}\) for any \(n\), or does GoE already kill the first preimage?
\item Dir.\ 2: write the Newton polygon of \(K\ast X\) explicitly from Lucas digits; does rationality of \(A\) give a uniform linear bound independent of solving for \(u\)?
\item Dir.\ 2: can superlinearity of \(X\) be read off the nested-\(11\) geometry of \(F_{30}^t e\) as a support identity, not an empirical density?
\end{enumerate}
- **Llama-4-Maverick-H12.0**: $p$
- **Llama-4-Maverick-H12.1**: $\mathcal T_w$
- **Llama-4-Maverick-H12.2**: $\mathcal R$
- **Llama-4-Maverick-H12.3**: $w$
- **Llama-4-Maverick-H12.4**: $h(\mathcal T_w(\mathcal R)) < h(\mathcal R)$
- **Llama-4-Maverick-H12.5**: $h$

## Directions screened out during the panel (by a model, not independently verified)

- [DeepSeek-V4] none.}
\]
- [Grok-4.6] none of H1.0/H2.0 or H1.1/H2.1. (A/F claimed evaded by fibre-asymptotics; E is the intended target of the \(\Omega(e)\) classification. Keep both, but treat bipermutative rigidity lemmas as inadmissible imports unless restricted to \(\Omega(e)\).)
- [DeepSeek-V4] None.
- [Grok-4.6] V4-H6.0 / Dir.\ 5. The identity is false: \(f_{30}\) at site \(0\) uses stencil \(\{-1,0,1\}\), so
\[
a_{t+1}\oplus a_t=u_{t,-1}\oplus u_{t,1}\oplus a_t u_{t,1},
\]
not the claimed \(u_{t,1}\oplus u_{t,2}\oplus(u_{t,1}\wedge u_{t,2})\). Thus \(D_t\not\equiv0\) as written and the telescoping “conservation law” is not a theorem. (A corrected stencil is absorbed into Dir.\ 7 via \(\chi\).)
- [Grok-4.6] V4-H6.1 / Dir.\ 6. (i) “DFA with two counters” is a 2-counter machine, not a DFA. (ii) Existence of interface densities \(\alpha,\beta\) is a P2-type statement on adjacent columns (circular for
- [DeepSeek-V4] 3 (nonlinear spacetime series rationality):  
The approach is likely killed by obstruction H (finite data cannot establish an infinite statement).  
Christol’s theorem (algebraic \(\Leftrightarrow\) automatic) already tells us that a rational \(A(z)\) is automatic of bounded rank; proving that \(A(z)\) is not rational amounts to proving unbounded Hankel rank, which is equivalent to proving non-automaticity.  
But the register digest (H) states: “any sequence agreeing with \(a\) on \([0,N)\) and zero thereafter is eventually periodic, so \(N\) terms buy a kernel lower bound of about \(N/8\) and nothing more, ever.”  
Thus an algebraic proof that \(A(z)\) is not rational would need to use an infinite exact identity (the quadratic relation \(Q(G)=0\)), but that identity involves the full 2D series \(G\), whose coefficients for \(i\neq0\) are not known – they are exactly the unknown right ray.  
Hence the approach reduces to the same infinite subshift problem as Dir. 1, but with an algebraic dressing that does not obviously bypass H.

---

\textbf{Open questions}
1. For Dir. 1: Can the transducer \(\mathcal T_w\) be shown to have a finite number of spatial asymptotic states (attractors) when iterated on *any* right ray that is consistent with the periodic trace \(w\)?  
2. For Dir. 1: Is there a combinatorial invariant (e.g., a weighted sum of interface positions) that must be conserved or grow under \(\mathcal T_w\), forcing eventual spatial periodicity?  
3. For Dir. 2: Can the linear independence of kernel rows over the actual defect field \(\{\chi_{s,i}\}\) be proven without solving the dynamics, e.g., by a geometric argument on the supports (the right-interface triangles are nested and
- [Grok-4.6] \ 1 (finite-state \(\mathcal T_w\)).
Obstruction F: a finite-state claim is a bounded suffix of \(\rho_t\), hence a fixed-depth strip; the phase slip relocates at the free end (\(\mathrm{plain}(R+1)\subseteq\mathrm{pin}(R)\)). “Exact for all future times” does not cancel F. If the state is unbounded, \(\mathcal T_w\) is not a transducer and spatial-tail periodicity is not forced.
- [Grok-4.6] \ 2 (black-box \(\chi\)-queries / \(|I_n|=\Omega(n)\)).
The gates \(\chi_{s,i}\) are not oracles: they are local products on the same unfolding that computes \(a_n\). Query complexity in a self-generated DAG is circular. Moreover \(|I_n|=\Omega(n)\) is a density statement on \(11\)-pairs along Lucas sections, i.e.\ a P1/P2 claim in disguise, so it cannot witness P3. (Lucas kernel itself is admissible; the fake sequential-query reduction is not.)

## Open questions named by the panel

- [DeepSeek-V4] can the half-plane subshift \(X_{p,q}\) be characterized combinatorially for Rule 30, and does it admit a finite description of its asymptotic spatial phases \(\mathcal A_p\)?
- [DeepSeek-V4] can one prove that every \(F\)-invariant measure on \(\Omega(e)\) has marginal \(\frac12\) without first proving P2 itself? What structural property of \(\Omega(e)\) (e.g., minimality, unique ergodicity, or a specific joining rigidity) would force \((\star)\)?
- [DeepSeek-V4] \]
\begin{enumerate}
\item For Direction 1: does the half-plane subshift \(X_{p,q}\) admit a finite combinatorial characterization for Rule 30, and can the asymptotic phases \(\mathcal A_p\) be enumerated without solving the full dynamics?
\item For Direction 1: can an interface conservation law be derived from the local rule \(a\oplus(b\vee c)\) that prevents two propagating interfaces from coexisting with a periodic temporal trace?
\item For Direction 2: what ergodic-theoretic property of the single-orbit closure \(\Omega(e)\) (minimality, unique ergodicity, coalescence, or a specific joining constraint) would force the marginal to be exactly \(\frac12\)?
\item For Direction 2: can the uniform Cesàro statement be approached via a specification-like property or a gluing lemma on \(\Omega(e)\) that does not require bipermutativity?
\end{enumerate}
\]
- [Grok-4.6] \begin{enumerate}
\item Dir.\ 3: write \(Q(G)=0\) explicitly and extract a closed relation on the Hankel matrices of \(A\); does unbounded Hankel rank follow from the quadratic term plus \(\operatorname{supp}G_0=\{0\}\) without solving the CA?
\item Dir.\ 3: is there a rational (or algebraic) \(A\) compatible with \(Q(G)=0\) for some other compactly supported seed, i.e.\ is the obstruction seed-specific?
\item Dir.\ 4: can one define a bilinear rank \(r_n\) of the unfolding such that \(r_n=\Omega(n)\) is provable from \(a\oplus(b\vee c)\) and such that \(K^{o(n)}(a_{[0,n)})\ge r_n-O(1)\)? Exhibit the reduction, do not name it.
\item Dir.\ 1 (prior): does \(\mathcal A_p\) remain finite when the half-plane is genuinely infinite (no outer free column), or does obstruction F reappear as a spatial end?
\item Dir.\ 2 (prior): name one joining/coalescence property of \(\Omega(e)\) that forces \((\star)\) and is false on the full Bernoulli system (so bipermutativity is not required).
\end{enumerate}
- [DeepSeek-V4] \begin{enumerate}
\item For Direction 5: Can the "bilinear complexity" of the joint interface sequence be formalized (e.g., as the rank of a certain Hankel matrix over \(\mathbb{F}_2\) built from the ∧-terms) and shown to grow unbounded for Rule 30 but bounded for Rule 90?
\item For Direction 5: Does the periodicity constraint on the RHS of the conservation law force the interface sequence to be eventually periodic? If so, can one derive a contradiction from the known structure of the interfaces (e.g., they are Sturmian-like)?
\item For Direction 6: Can the three-column system be rigorously shown to be Toeplitz (or quasi-Toeplitz) using the hierarchical structure of the first-1 loci? What are the scaling relations?
\item For Direction 6:

## Next step (execution phase, separate from this run)

For each candidate direction: (1) check its stated Rule 90 screen in
actual code, not by trusting the model's sketch; (2) check it against
`PATH.md` section 7.3/8.7 for a named obstruction the model may have
missed or misjudged; (3) only then decide whether it is worth a route
entry in `PATH.md` and who owns running it. A direction a model marked
'screened out' is not thereby dead — the screen itself needs the same
independent check as a survivor before anyone relies on it.
Full raw responses, uncompressed, are in `compressed_transcript.json` for
every call — read those before trusting this summary of them.
