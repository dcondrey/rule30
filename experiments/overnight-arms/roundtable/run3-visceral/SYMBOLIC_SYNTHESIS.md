# Symbolic roundtable: lateral-thinking sparks on Rule 30

Status: **UNEXECUTED, DELIBERATELY UNFILTERED SPARKS, NOT RESULTS.**
This run asked four models to juxtapose Rule 30 against unrelated
domains (other sciences, magic, science fiction, etc.) and follow an
analogy before it can be justified.  Absurd and wrong were explicitly
invited; only "uninteresting" was penalized.  So a low idea-count or a
half-formed spark is not this run failing — it is the run doing its
job, which is coverage of unfamiliar territory, not correctness.
Nothing below is PROVED or MEASURED.  Most entries are not even
formal claims yet; they are analogies that would need real work to
become a checkable proposal at all, and THEN the same treatment as any
other route in `PATH.md`: a precise restatement, a Rule 90 check run
in actual code, a kill condition, and an owner.  Treat this document
as raw material for triage, not a triage list itself.

Calls: 12 (0 errored). Roster (final model per slot,
after any live swaps):
- `openai/gpt-5.6-terra-pro` (GPT-5.6): deep System-2 formal logic and proof trees
- `deepseek/deepseek-v4-pro` (DeepSeek-V4): RL reasoner for circuit-complexity verification
- `x-ai/grok-4.6` (Grok-4.6): lateral mathematical reasoning, unconstrained algebraic exploration
- `meta-llama/llama-4-maverick` (Llama-4-Maverick): open-weights anchor for adversarial verification

**Live model swaps during the run:**
- DeepSeek-V4: `deepseek/deepseek-v4-pro-0813` -> `deepseek/deepseek-v4-pro` at call 2 (response yielded no extractable hypothesis/refutation/obligation)

## Candidate directions surfaced (unverified, unexecuted)

- **GPT-5.6-H1.0**: tinnitus “residual inhibition” and rebound after a masking tone}

In severe tinnitus, a broadband masking sound can suppress the perceived tone for a while; then, perversely, the tone returns, sometimes louder or phase-shifted. The clinically important thing is not merely whether the patient reports a tone at one instant. It is whether repeated suppression episodes leave a reproducible \emph{rebound signature}: a hidden oscillator has been perturbed, and the recovery timing carries more information than the audible signal itself.

Treat a hypothetical eventual period-\(p\) centre column \(c_t\) not as the object to be disproved directly, but as a permanent masking tone imposed by the future: after some \(T\), the centre is assumed to supply the same \(p\)-beat stimulus forever. Rule 30’s update can be written
\[
c_{t+1}=L_t\oplus(c_t\lor R_t),
\]
so the audible centre report is the XOR of a left-diagonal “efferent signal” and a right-side inhibition gate. Under a periodic \(c_t\), every time one asks whether the gate was open, one gets a binary diagnosis of the left input:
\[
L_t=c_{t+1}\oplus(c_t\lor R_t).
\]
This is not yet useful: it is just the usual backwards ambiguity. The tinnitus analogy says to look not at a single inferred hidden state, but at the \emph{recovery curve after deliberately chosen virtual suppressions}.

A Rule-30 object would be a family of finite spacetime “masking lesions” attached along the presumed periodic centre tail. A lesion does not alter the actual lone-seed orbit; it is a counterfactual patch in which one replaces one full period of the centre word by its complement, or by the same word shifted one phase, and then asks whether the rule admits a bounded repair on both sides of the lesion. The key datum is the least distance/time at which the repair can be reabsorbed into the original periodic tail. Call this the rebound length.

Why this differs from a fixed strip: the lesion is not a boundary condition at distance \(R\). It is a finite \emph{defect in time} embedded in an otherwise bi-infinite periodic centre prescription. One could form its monoid of possible left/right recovery states, but the hoped-for invariant is not its cardinality. It is a signed recovery index: does a one-period phase lesion return with the same phase, disappear, or emerge shifted by one cell? A genuine tinnitus-like rebound would mean every attempted local repair exports a phase debt whose sign is determined by the local Rule-30 asymmetry \(c\lor r\), and repeated lesions add their debts. If \(k\) identical lesions force an unbounded accumulated phase displacement, an eventually periodic centre tail cannot coexist with a single fixed past cone: its “masked” future has no stable baseline to rebound to.

The concrete experiment is small but sharply diagnostic: enumerate all locally admissible repairs of a period-\(p\) centre word containing one phase-slip block, quotient by translation by \(p\), and inspect whether recovery displacement has a nonzero cocycle under concatenating lesions. The sought theorem would say that Rule 30 gives a one-sided sign law for this cocycle, not merely a finite-state transition graph. That sign law could turn periodicity itself into the source of an accumulating contradiction, rather than trying to propagate information from a far boundary.

Rule 90 is a real check, not a vacuous pass: its additive rule should allow paired phase lesions to superpose and cancel exactly, so its rebound cocycle ought to be zero or sign-indefinite; if the same one-sided rebound law appears there, this spark is dead.
- **DeepSeek-V4-H2.0**: **Spark: the "squatter's title" of adverse possession, applied to the centre-column's future light cone**
- **DeepSeek-V4-H2.1**: Source domain: **adverse possession law** — the specific common-law doctrine by which a trespasser who occupies land openly, continuously, and hostilely for a statutory period (often 10–21 years) extinguishes the original owner's title and gains legal ownership. The crucial detail is not the occupation itself but the *extinguishment*: the original owner's right doesn't merely go dormant; it is destroyed, and the squatter's title becomes the root of a new chain. The doctrine has a weird temporal asymmetry — the squatter's claim strengthens with time, while the owner's weakens, even though the underlying facts (who built the fence, who paid taxes) are symmetric. The legal magic is in the *running of the clock* against one party and for the other.
- **DeepSeek-V4-H2.2**: **The juxtaposition:** Suppose the centre column *were* eventually periodic with period \(p\). Then after some transient \(T\), the future light cone of the lone seed contains a repeating \(p\)-cycle of centre values. Treat that periodic tail as a piece of "land" — a spacetime region whose title (the right to determine cell values) is initially held by the lone-seed past. But the periodic tail also generates, via Rule 30's left-permutive backward light cone, a set of *competing claimants*: other past configurations, inconsistent with the lone seed, that would produce the *same* periodic centre tail if they were the true past. These are the "squatters." Each squatter is a finite perturbation of the lone seed — a different initial condition that, after some healing transient, locks onto the same periodic centre word.
- **DeepSeek-V4-H2.3**: The adverse-possession question is: does one of these squatters acquire *better* title than the lone seed? "Better title" means: for a given finite window of the centre column at large \(t\), the squatter's past requires fewer "hostile" cells (cells that disagree with the lone seed's actual past cone) to sustain the periodic tail than the lone seed itself does. The statutory clock is the number of periods for which the periodic tail has been running. The hostile occupation is the mismatch between the squatter's required past and the actual lone-seed past.
- **Llama-4-Maverick-H4.0**: "glossolalia and the 'initial fluency' illusion in speech-like centre-column patterns"

Source domain: **glossolalia** — the phenomenon of speaking in tongues, particularly the characteristic that the initial utterance sounds like a real language to the speaker but rapidly devolves into a non-linguistic vocal pattern.

The juxtaposition: Treat the centre column of Rule 30 as a "speech signal" generated by the lone seed's "utterance" at time zero. The initial values of the centre column might resemble a structured or "fluent" pattern, but as time progresses, the column's behavior becomes increasingly complex and "non-linguistic." The question is whether this initial "fluency" is an illusion created by the limited observation window, much like the initial coherence of glossolalia.

A Rule-30 object would be a family of finite observation windows on the centre column, each with a "comprehension metric" that measures how "language-like" the observed pattern is. The metric could be based on the presence of local patterns, repetition, or other features that make a sequence appear structured. The key question is whether, as the observation window grows, the centre column's pattern continues to appear "fluent" for a significant number of steps before devolving into a non-periodic, complex pattern.

The analogy bites if there exists a "devolution point" after which the centre column's pattern becomes recognizably non-periodic and complex, much like how glossolalia loses its initial language-like quality. The Rule-30 specific question is whether this devolution is related to the inherent properties of the rule, such as its left-permutivity and the structure of its backward light cone.

Rule 90 check: Rule 90's centre column is eventually periodic, so if the "initial fluency" metric is applied to it, the column should either remain "fluent" indefinitely or devolve in a predictable, periodic manner. If the glossolalia analogy holds for Rule 30 but not for Rule 90, it could indicate a meaningful difference in their centre-column behaviors.
- **GPT-5.6-H5.0**: telegraph-relay contact bounce and “chatter” in an exhausted electromechanical repeater chain}

An old telegraph relay does not simply transmit a dot as a dot. When a weak or badly timed pulse reaches a relay, its armature can chatter: make–break–make–break before settling. Crucially, the chatter is not arbitrary noise. It records an unresolved contest between the incoming current, the relay’s retained magnetic state, and the return spring. A perfectly periodic incoming rhythm can therefore produce a nonperiodic \emph{settling transcript} downstream: the nominal message repeats, while the microscopic sequence of contact closures carries a growing timing debt.

Rule 30 has an almost embarrassingly relay-like decomposition:
\[
a_{t+1,x}=a_{t,x-1}\oplus(a_{t,x}\lor a_{t,x+1}).
\]
The left neighbor is an always-effective incoming pulse: changing it always flips the output. The centre/right pair is a contact condition that can suppress or pass the effect according to whether the local relay is already held closed. Unlike an additive rule, a pulse may therefore
- **DeepSeek-V4-H6.0**: **Spark: the "phantom limb" map of a missing periodic tail, specifically the phenomenon of *referred sensation* — touching the face evokes a felt touch in the absent hand — as a model for how a non-periodic centre column might sustain a coherent but displaced "periodic after-image" that cannot be localized to any finite window.**
- **DeepSeek-V4-H6.1**: Source domain: **phantom limb referred sensation**, the specific neurological finding that after amputation of a hand, stimulation of the face (whose cortical representation invades the deafferented hand area) produces a vivid, topographically organized sensation in the missing hand. The key detail is not the mere persistence of a ghost limb, but the *systematic mislocalization*: a stimulus at one body site is felt at another, and the mapping is stable, somatotopic, and — crucially — it reveals the hidden geometry of the cortical reorganization. The phantom does not merely "hurt"; it *receives* input from a displaced source, and the displacement vector is the diagnostic signature.
- **DeepSeek-V4-H6.2**: **The juxtaposition:** Suppose the centre column *were* eventually periodic with period \(p\). Then after some \(T\), the infinite future tail is a repeating word \(w\) of length \(p\). Amputate that tail: delete the actual centre-column values for all \(t > T\), leaving a "stump" at time \(T\). The Rule 30 dynamics, running forward from the lone seed, now have a missing limb — the cells that used to be determined by the periodic tail are now free. But the dynamics also have a *cortical reorganization*: the left-permutive structure means that cells in the leftward cone (the "face" of the diagram) can, under the right conditions, supply the missing centre values through a displaced computation. The question is whether there exists a *referred sensation map* — a finite translation \(( \Delta t, \Delta x )\) and a finite local rule — such that the centre-column values at large \(t\) can be reconstructed, not from their own past, but from a *spatially displaced* patch of the diagram that lies entirely within the known lone-seed cone, with an error that vanishes as \(t \to \infty\).
- **DeepSeek-V4-H6.3**: **What a Rule-30 object would look like:** A *phantom decoder* is a pair \((D, \delta)\) where \(D\) is a finite-radius block rule and \(\delta = (\tau, \xi)\) is a fixed spacetime displacement. The claim is: for the true lone-seed centre column \(c_t\), there exists a time \(T_0\) such that for all \(t > T_0\), \(c_t = D( \text{cone patch at } (t - \tau, -\xi) )\). That is, the centre column is not self-determining; it is a referred copy of activity happening elsewhere in the cone. The displacement \(\delta\) is the "reorganization vector." If such a decoder exists, then the periodic tail hypothesis is false in a very specific way: the centre column *looks* like it has a periodic future, but that future is actually a shadow cast by a structurally different part of the diagram, and the shadow's coherence is the phantom, not the limb.
- **Grok-4.6-H7.0**: \emph{incubation of craving} in incentive-sensitization — the clinical fact that, after cocaine or similar, cue-triggered “wanting” is stronger at 30 days of abstinence than at 1 day, while “liking” is flat or gone)

A person can sit in a room that no longer contains the drug and still be more captured by a glint of foil than they were the morning after they quit. Abstinence is not a reset. The gain on the cue turns up in the quiet. That is the embarrassing physiology: the street corner gets more potent because nothing is happening.

Treat an eventually periodic centre column as that quiet. After some \(T\) the centre is “abstinent”: it has stopped producing new non-repeating flips and is living in a loop of period \(p\). Rule 30 still has the same ugly gate it always had,
\[
c_{t+1}=L_t\oplus(c_t\lor R_t).
\]
The left bit is an internal pulse that can always land a hit. The right bit is the foil. The gate is clamped (so \(c_{t+1}=\neg L_t\), cue irrelevant) whenever \(c_t=1\); it is open to the street corner only on the 0-beats of the supposed period. Ordinary strip reasoning treats those 0-beats as a finite-state filter that either closes or it doesn’t. Incubation says the filter’s \emph{gain} is a function of how long the abstinence has already lasted.

A Rule-30 object is a sequence of cue-thresholds \(\theta(k)\): after \(k\) forced periods, the longest run of right-column zeros that can still be tolerated on unsaturated beats without a centre-bit relapse. Incubation is \(\theta(k)\to 0\) as \(k\to\infty\), with a one-sided sign — each period spent with \(c\) clamped at 1 is a use-episode that makes the next open beat \emph{more} obligatory, not less. Concatenating periods would then be a product of gains \(>1\), not a walk on a strip whose accepting tail stays nonempty because the outermost column remains free. The lone-seed cone only has to supply, infinitely often, a right-column fluctuation smaller than \(\theta(k)\) at that \(k\). Relapse is then forced by the actual past, not by a competing preimage count and not by information crawling in from a far boundary.

The analogy is not justified by any composition law yet; the whole point is that the recovery trajectory after a period is being claimed not to be a reset, and that claim has to be written as a signed gain, not named as a “seam.”

Rule-90 gut check: real, not vacuous. Rule 90 has no OR-gate; \(R\) always has gain 1, so incubation cannot even be stated. If a cloned \(\theta(k)\) still collapses on Rule 90’s eventually-zero centre, this spark is dead.
- **Llama-4-Maverick-H8.0**: **Spark: the \"numbers station\" anomaly signature in a degraded shortwave broadcast, applied to the centre-column's future light cone**
- **Llama-4-Maverick-H8.1**: Source domain: **numbers stations** — clandestine shortwave broadcast sites that transmit coded messages as sequences of numbers or other audio cues, often with deliberate distortion or anomalies to confound detection. The crucial detail is not the encryption itself but the *anomaly signature*: a specific pattern of distortion or irregularity that is not merely random noise, but a diagnostic signature of the transmission's origin or intent.
- **Llama-4-Maverick-H8.2**: The juxtaposition: Treat the centre column of Rule 30 as a received signal that is supposed to be eventually periodic with period \(p\). The future light cone of the lone seed is then a "broadcast" that generates this centre column. The numbers station analogy says to look not at the centre column itself, but at the pattern of "anomalies" or deviations from the expected periodic signal that appear in the backward light cone of the centre column. These anomalies are not random errors, but are systematically related to the Rule 30 dynamics.
- **Llama-4-Maverick-H8.3**: A Rule-30 object would be a family of "anomaly detectors" that scan the backward light cone for specific patterns of deviation from a hypothetical periodic centre tail. The key datum is not merely whether anomalies occur, but their *signature*: the specific spacetime geometry of the anomalies, and how they correlate with the Rule 30 update rule. The question is whether there exists a characteristic anomaly signature that is incompatible with an eventually periodic centre column.
- **GPT-5.6-H9.0**: the layer-order test that exposes a forged “old” painting}

A convincing forgery is not caught merely because it has cracks. A genuine old painting has a stratigraphy: cracks began in the support or ground, pass through the older pigment layers, and are then partly filled by later varnish and dirt. A forger who paints a new motif onto an old cracked canvas can imitate the visible crack network, but eventually a conservator finds the obscene giveaway: a crack that ought to continue through a layer terminates exactly at the new paint, or supposedly ancient dirt lies beneath a supposedly older fissure. The issue is not a local pattern count. It is an impossible \emph{order of events} recorded where two histories meet.

Assume the Rule-30 centre tail is period \(p\) from time \(T\). Overlay the actual spacetime diagram with itself shifted forward by \(p\), and call
\[
D(t,x)=a(t+p,x)\oplus a(t,x).
\]
The periodicity hypothesis says that the superposed paintings agree on the vertical half-ray \(x=0,\ t\ge T\): \(D(t,0)=0\). But the two layers need not agree off that line. Their disagreement set is the craquelure.

The object is not a bounded window around the centre, but a \emph{stratigraphic annotation} on each disagreement edge. At a cell where the two overlaid Rule-30 updates differ, record which of the two OR-gates changed status:
\[
(a_{t,x}\lor a_{t,x+1}) \neq
(a_{t+p,x}\lor a_{t+p,x+1}),
\]
and whether the output disagreement was inherited from the left input or created by this gate-status mismatch. Thus each crack segment carries a layer-order label: “old left signal passed through altered varnish,” versus “the varnish itself changed what could pass.”

The hoped-for Rule-30-specific statement is an \emph{anachronistic termination law}. A disagreement crack can meet the agreement ray \(x=0\) only in certain orientations. Because the left input enters by XOR while the centre/right pair enters through OR, a crack that is killed at the ray may leave behind a compulsory gate-status scar on one temporal layer. Periodicity requires infinitely many such killings—every comparison across \(p\) steps has a permanently crack-free centre line—yet the lone seed supplies only one original substrate boundary. If each killed crack deposits a scar of one irreversible stratigraphic type, then repeated temporal overlay produces an impossible ordering: later “varnish” scars would have to sit beneath earlier “pigment” scars, or an unbounded number of distinct scars would have to terminate at the finite seed-era substrate.

The formal target would be a signed chain complex, not a strip automaton: disagreement arcs in the \((t,x)\)-overlay, with vertices labelled by the four paired local states and a boundary map counting OR-status transitions. Show that for Rule 30 an arc ending on an agreement half-ray has nonzero signed stratigraphic charge, while charges cannot be created in the interior except at a finite initial interface. Then an eventual periodic centre supplies infinitely many charged endpoints and contradicts finite origin. The key danger is that the charge may simply leak sideways forever; the needed novelty is a genuine layer-order obstruction showing that lateral escape changes the charge rather than merely relocating it.

Rule-90 gut check: real and hostile. For Rule 90, \(D\) itself obeys the same additive rule and there is no gate-status layer; cracks can cancel without leaving stratigraphic residue. If a comparable signed endpoint charge survives there, this spark is dead.
- **DeepSeek-V4-H10.0**: **Spark: the "autoimmune self-attack" of molecular mimicry, specifically the mechanism by which a pathogen's surface protein, resembling a host protein just enough to trigger an immune response, causes the immune system to attack not only the invader but the body's own tissues indefinitely, long after the original pathogen is cleared.**
- **DeepSeek-V4-H10.1**: Source domain: **autoimmune molecular mimicry** — the specific pathological process in diseases like rheumatic fever or Guillain-Barré syndrome. A streptococcal bacterium displays a surface antigen (M protein) that is structurally similar to a human cardiac myosin protein. The immune system learns to target the bacterial antigen, successfully clearing the infection. But the learned immune memory now recognizes the *self*-protein as foreign. The attack continues against the heart tissue indefinitely, driven not by the continued presence of the pathogen, but by the persistent, self-sustaining error in the immune system's own targeting logic. The crucial detail is the *epitope spreading*: once the self-attack begins, the tissue damage exposes new self-antigens, which are then targeted in a cascading, diversifying autoimmune response that becomes structurally independent of the original molecular mimic. The original infection is a transient seed; the chronic disease is a self-perpetuating dynamical error.
- **DeepSeek-V4-H10.2**: **The juxtaposition:** Suppose the centre column *were* eventually periodic with period \(p\) from time \(T\). This periodic tail is a "self"-pattern: a repeating word \(w\) of length \(p\) that the Rule 30 dynamics, running forward from the lone seed, has "learned" to produce. The lone seed is the initial "infection" that kicked off the dynamics. The question is whether the periodic tail itself, once established, acts as a molecular mimic that triggers a self-attack *within the rule's own backward light cone*.
- **DeepSeek-V4-H10.3**: Treat the periodic centre word \(w\) as a "surface antigen." The Rule 30 update rule, applied backwards, is the "immune system's" recognition logic. A preimage of the periodic tail under Rule 30 is a past configuration that would produce that tail. The lone seed's actual past cone is one such preimage. But there are others: "molecular mimics" — finite perturbations of the lone seed's past that also produce the *same* periodic centre tail, but whose off-centre structure differs. The autoimmune attack is the process by which the requirement to sustain the periodic tail *forces* the actual past cone to incorporate these differing off-centre structures, which then act as "neo-antigens" that demand further, escalating structural changes in the deeper past.
- **Grok-4.6-H11.0**: the ideomotor planchette, specifically the cheap circular drift that sitters then credit to a spirit}

Source domain: \textbf{ouija-board ideomotor mechanics} — not “spirits,” and not the epistemic puzzle of who knows what. The ugly laboratory fact: several people rest fingers on a plastic pointer; each produces grams of unintended force; the vector sum moves. A repeating circle is the default of that sum (arm-fatigue oscillator, planchette touring the board’s empty centre). A spelled sentence is a residual after near-cancellation. Sitters, embarrassed to be pushing, attribute the circle to an occupant. Closing the seance (“GOODBYE”) is a social act; the physics does not need an occupant to loop.

Juxtaposition: treat the three inputs of Rule 30 as sitters and the centre bit as the planchette. The left sitter never lifts (the XOR always couples); the right sitter \emph{may} lift whenever the centre sitter is already bearing down (\(c\lor r\) saturates, \(R\) is ideomotor-silent); the centre sitter is both medium and message. An eventually periodic centre tail is exactly the cheap circle — the motion you get when nobody is authoring letters and the residual has fallen into a rotating bias — and the periodicity hypothesis is the seance interpretation of that circle.

What bites is not that circles are possible. It is that this particular left sitter cannot supply one. From the lone seed the left half-triangle is a delirious, always-on pusher, not a metronome. A circle of period \(p\) with any \(1\) in the word requires that on every \(1\)-beat the planchette ignore \(R\) and take \(\neg L\); those beats therefore \emph{subsample} the delirious sitter and demand that the subsample already be rhythmic. The right sitter’s on/off pattern is then only a peel-off dance around a rhythm that had to be present on the left. The spirit is doing no work.

The Rule-30 object is not a strip automaton and not a count of preimages. It is an \emph{integer ideomotor residual} along a candidate circle: lift the right sitter’s participation off \(\mathrm{GF}(2)\) to \(\mathbb{Z}\),
\[
\rho_k=\sum_{j=0}^{k-1}\bigl(1-c_{T+jp}\bigr)(2r_{T+jp}-1),
\]
the signed on-time of \(R\) only on the unlocked (centre-\(0\)) beats of \(k\) supposed periods. A genuine cheap circle needs \(\rho_k\) bounded — fatigue oscillator, not a random walk, not a drift. The nested right of lone-seed Rule 30 is visibly biased; the claim is that \(\rho_k\) is one-sided and \(|\rho_k|\to\infty\), so the residual cannot be credited to a spirit-loop. No composition seam is named: \(\rho\) is just the lift of the peel-off dance the OR already writes.

This is not “the planchette spells aperiodic text.” It is: the only loop the hardware cheaply supports is a circle, and this left sitter is the wrong kind of drunk for a circle.

\textbf{Rule-90 gut check:} real, hostile. Both sitters always push; there is no peel-off, \(\rho\) is not even definable from an OR, and the planchette does stop (centre eventually \(0\), a circle of radius zero). If a cloned integer residual, built from XOR-imbalance instead, still drifts on Rule 90, the spark is dead.
- **Llama-4-Maverick-H12.0**: the "degraded photocopy of a photocopy" chain in a fax relay, applied to the centre-column's future light cone

Source domain: **fax machine generation loss** — the phenomenon where repeated photocopying or faxing of a document leads to a progressive degradation of image quality, characterized by the accumulation of speckles, loss of fine detail, and eventual illegibility.

The juxtaposition: Treat the centre column of Rule 30 as a "signal" being transmitted through a fax relay, where each step in the future light cone is a "copy" of the previous state. The initial lone seed is the original document. The question is whether the centre column's behavior, as it evolves, resembles the degradation seen in a fax relay chain.

A Rule-30 object would be a family of "degradation metrics" that measure the quality of the "signal" (centre column) at each step, based on features like the density of "speckles" (random flips), loss of "text" (long-range correlations), or other characteristics that degrade in a fax relay. The key question is whether there exists a characteristic degradation signature in the centre column that is incompatible with an eventually periodic signal.

The analogy bites if the centre column's pattern becomes increasingly degraded, much like a fax relay chain, and this degradation is related to the inherent properties of Rule 30, such as its left-permutivity and the structure of its backward light cone.

The specific Rule-30 object to examine is the sequence of "error counts" in the backward light cone of the centre column: for each centre-column bit at time $t$, count the number of discrepancies between the actual past cone and a hypothetical periodic past cone. If this error count grows in a manner similar to the degradation in a fax relay chain, it could indicate a non-periodic centre column.

Rule 90 check: Rule 90's centre column is eventually periodic, so if the "degradation metric" is applied to it, the column should either remain "intact" indefinitely or degrade in a predictable, periodic manner. If the fax relay analogy holds for Rule 30 but not for Rule 90, it could indicate a meaningful difference in their centre-column behaviors.

### Open questions
- Can a "degradation metric" be defined for the centre column that captures its progressive degradation?
- Is there a characteristic "degradation signature" for Rule 30's centre column, incompatible with eventual periodicity?
- How does the degradation in the fax relay analogy relate to the actual structural properties of Rule 30, such as its ergodicity or the complexity of its backward light cone?

## Directions screened out during the panel (by a model, not independently verified)

- [Grok-4.6] possession spark: “better title” by hostile-cell count is a competing-preimage cost. That is the already-killed fork-count shape, and a sparse hostility score is density-zero-blind besides.

\textbf{Open questions}
- Does one full period of desiccant already move the flake line, or only an infinite tail?
- Is “shed” ever witnessed inside the true lone-seed cone for small \(p\), or only wetness (which would be the free-boundary obstruction in costume)?
- Can the glue-count be signed, so that \(c\lor r\) debts accumulate instead of merely failing to close?
- [Grok-4.6] limb decoder: a fixed-displacement finite-radius \(D\) is a sliding-block factor of a cone patch. If it matches the centre forever, the centre is a sofic image of the seed cone — either it already fails at small \(T\), or it cannot be lifted from finite data to an infinite statement. The “referred type” is also the Theseus refinement that already collapsed onto the bit.

\textbf{Open questions}
- Can \(\theta(k)\) be read off the rule without putting the periodic centre in by hand (the Faraday slip of imposing the spirit message, then finding sitters)?
- Does \(k=1\) already move \(\theta\), or is incubation only an infinite-tail phenomenon?
- On the true lone-seed right column, for small candidate \(p\), does any unsaturated beat already violate the \(k=1\) threshold?
- [Grok-4.6] the autoimmune-mimicry spark is squatters again — competing preimages of a periodic tail, epitope spreading as fork-count — already killed in that shape and density-zero-blind besides.

\textbf{Open questions}
- Does \(\rho_1\) already move for any small candidate \(p\) with a \(0\) in the word, on the true lone-seed right column?
- Can the lift be read from the rule without inserting the periodic centre by hand (Faraday’s slip)?
- If every \(1\)-beat subsample of column \(-1\) is empirically unpatterned at reachable \(T\), is that a peculiarity of the seed or an artifact of \(T\) still sitting under the \(O(\log t)\) wall?

## Open questions named by the panel

- [Llama-4-Maverick] - Can a "comprehension metric" be defined for the centre column that captures its initial "fluency" and subsequent devolution?
- Is there a characteristic "devolution point" for Rule 30's centre column, after which it becomes recognizably non-periodic?
- How does the "initial fluency" illusion in glossolalia relate to the actual structural properties of Rule 30, such as its ergodicity or the complexity of its backward light cone?

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
