# Overnight autonomous prompt (paste as one message in a fresh session in /Volumes/A/researchpapers/13-rule30)

/goal Demonstrated in this session's own output, within at most 40 loop iterations: (1) a completed literature-novelty triage table covering at least eight candidate techniques (the seed list below plus at least two self-generated ones), each row citing the closest prior work found and a verdict of novel-open, known-adjacent-with-stated-open-edge, or closed; (2) at least two arms pre-registered (task, metric, strong outcome, kill condition that can fire) and executed to completion, each ending in a RESULTS file under docs/rule30/overnight/ whose status line is exactly one of PROVED, VERIFIED, KILLED, or REDUCED with the remaining obligation stated; (3) an explicit closing statement that no file outside experiments/overnight-arms/, docs/rule30/overnight/, and runs/overnight/ was created or modified and nothing was committed to git.

This prompt includes the keyword ultracode: use the Workflow tool to fan out the
literature review (one agent per candidate technique, schema-constrained verdicts)
and, later, to run independent arms in parallel. After the first planning turn,
start /loop with no interval (self-paced) to sustain execution overnight; each
iteration advances the active arms, checks kill conditions, and updates the arm's
RESULTS file before scheduling the next wakeup.

## Mission

Novel, proof-relevant progress on the Wolfram Rule 30 center-column prize
questions (P1 non-periodicity, P2 limiting frequency of 1s, P3 computational
effort). Empirical observation is only a means; every arm must state up front
what formal statement about the center column it could in principle produce.
An arm with no plausible path to a formal statement ranks below one that has it.

## Hard fences (non-negotiable)

- Work ONLY in: experiments/overnight-arms/, docs/rule30/overnight/, runs/overnight/.
- Read-only everywhere else. Never edit experiments/rule30/, docs/rule30/*.md,
  or runs/alt-trace-automaton/ — another session is active there.
- Off-limits as subject matter (active elsewhere): the alternating-trace fiber,
  bounded-left-depth exclusion certificates, the parity-checked survivor map,
  the {1,4} wallpaper member, and Rowland-style column-band lock proofs.
- No git commits. No pushes. Python via `uv run python`; deps via `uv add`.
- WebFetch of anything outside official docs goes through a subagent that
  returns a summary.

## Settled knowledge — do not re-derive, re-verify, or rediscover

Literature (treat as closed books):
- Rule 30 = 00011110; new state = p XOR (q OR r). Mirror/complement/mirror-complement
  equivalences with rules 86, 135, 149 yield no independent information.
- The center column passes standard statistical randomness tests and was used
  for random integer generation. Frequency and chi-squared tests at any feasible
  sample size prove nothing; only formal results count.
- Left side: regular, period-doubling diagonal structure. Right side and center: chaotic.
- Conditional time-reversibility under white-right-half tail conditions.
- Southeast diagonals eventually periodic via left-permutivity plus conditional
  reversibility. Any diagonal analysis must build on Rowland's nested local
  structures and OEIS A094603–A094606, not restart from bit strings.
- Left-permutivity makes the map on right-half configurations injective given
  the trace (this repo's Lemma 1 uses it; it is also classical).

This repo (read every docs/rule30/*.md FIRST, read-only; treat VERIFIED/PROVED/
FALSIFIED conclusions there as settled; any candidate arm overlapping an
existing ARM4–ARM8 doc must cite it and proceed only on its stated open edge):
- Zero-trace fiber fully classified (prefix-OR); all-ones trace is the checkerboard.
- Dead ends, do not retry: prefix-OR latch through zero phases (FALSIFIED),
  run-of-ones wedge descent, cascade descent, trace-anchored O(log t) propagation.

## Phase 0 — literature review and brainstorm (no experiments yet)

Ultracode workflow fan-out, one researcher agent per technique. Seed list:
1. Persistent homology / TDA on the growing (x,t) point cloud — birth/death of
   topological features as invariants.
2. Quantum circuit mapping: Rule 30 as Clifford+T circuit; entanglement entropy
   growth across the center cut.
3. p-adic / non-archimedean analysis: rows as 2-adic (or p-adic) integers,
   Rule 30 as a continuous non-archimedean map. (Warning: CA as continuous maps
   on Z_p is classical; find the actual open edge or kill it.)
4. Latent-space geometry: constrained generative model over spacetime patches;
   analyze learned manifold geometry for conserved continuous structure.
5. Thermodynamic/hydrodynamic limit: PDEs for coarse-grained 1s density.
   (Warning: Gutowitz local structure theory is adjacent prior art.)
6. Non-standard analysis / model theory: Rule 30 over hyperinteger row lengths;
   transfer and overspill applied to uniformity statements.
7. Homotopy type theory: transitions as paths; center column as a type universe;
   P1 as a statement about a loop space. (Feasibility check mandatory.)
8. Axiomatic reverse-engineering: the completed spacetime grid as the unique
   model of a minimal algebraic theory; definability and automatic-structure
   angles. (Check against this repo's automaticity and grammar ARM docs first.)
Plus at least two techniques generated fresh in a brainstorm that is explicitly
forbidden from being a variation on the eight above.

Each agent returns: closest prior work (citations), what is already proved,
the precise unexplored gap, proof-relevance path to P1/P2/P3, overnight
feasibility on a local machine, verdict. Assemble the triage table. Kill
closed rows without sentiment.

## Phase 1 — pre-registration

Pick the top 2–3 arms by (novelty x proof-relevance x feasibility). For each,
write docs/rule30/overnight/PREREG-<arm>.md BEFORE any experiment: task,
baselines, metric, strong outcome, kill condition that can fire on a plausible
negative, seeds, and the cheapest disconfirming test, which runs first.

## Phase 2 — execution (the loop lives here)

Run arms in parallel where independent (disjoint file sets). Every number
reported names its test and what it does and does not control for. Seed
everything; report distributions, not bare means. When a kill fires, write the
kill honestly and promote the next triaged arm. No claim before the curve.

## Phase 3 — write-up

One RESULTS-<arm>.md per arm under docs/rule30/overnight/: status
(PROVED / VERIFIED / KILLED / REDUCED), exact statements, reproduction
commands, spending. A REDUCED arm states the one remaining obligation the
way a referee would. Finish with the fence-compliance statement from the goal.
