# Crosstalk elimination run 2, 2026-08-27

This bounded live run validated the new exclusion workflow with one generation, three candidates, six evolution call slots, one orchestration turn, and the measured ARM5/ARM6 negatives supplied as typed structural exclusions.

## Evolution result

No candidate survived. The generation report recorded three attempts, zero failures at the provider/schema layer, zero accepted candidates, and three `score_below_threshold` admissions. Unlike the earlier run, the output frontier was empty rather than presenting low-quality variants as solutions.

The three rejected contracts were:

1. a left-permutive affine boundary map that requires an unproved short period for the time-varying maps;
2. an inverse-diagonal transfer matrix that is exact only for the Rule 150 linear component and explicitly admits that the full Rule 30 map is nonlinear;
3. a carry-chain transfer matrix whose exactness is conditional on an undefined `LEMMA_GATE` predicate.

All three supplied structured state, identity, composition, complexity, and test fields, but each contract made its claimed polylogarithmic complexity conditional on precisely the missing lemma. The empty frontier is therefore the correct result. There is still no Rule 30 shortcut.

## Orchestration and verification result

The subsequent swarm again emitted a Lean artifact containing `sorry`. Crosstalk recorded the formal checker result as `PolicyViolation`, changed the turn to `VerificationFailed`, reduced completion probability to `0.3322`, removed the attempted Lean artifact from active state and the workspace, and emitted an empty `final_response` rather than the rejected proof.

The integrity audit passed because its typed graph was internally consistent. The separate scientific release assessment correctly returned `NOT_ESTABLISHED`: five claims were present, none was evidence-linked or objectively verified, and four counted as substantive facts or inferences.

The run also exposed a budget boundary worth fixing. The ten-call shared cap governed evolution and orchestration, but startup endpoint-validation and OpenRouter fallback pings happened before the session ledger existed. The displayed cap is therefore not yet an all-provider-call ceiling; the CLI and documentation now state that limitation explicitly.

## Residual transcript defect and closure

The first live export after these changes still exposed a stale provisional transcript hash at the second retained turn. This was valuable: the offline verifier rejected the bundle rather than blessing it. The finalization boundary now rebuilds the derived turn commitments from the retained, re-signed transcript before checkpointing. A deterministic two-turn regression test reproduces the exact sequence—user turn, rejected Lean proof, artifact rollback, export—and the resulting bundle verifies successfully.

## Interpretation

This run did not discover a mathematical solution. It demonstrated a more useful failure mode: implausible contracts were eliminated before entering the frontier, a checker-rejected synthesis could not masquerade as the final answer, and the scientific status remained explicitly unresolved. The next generation should consume the bounded rejection ledger, including the critic's fatal flaws, and seek a representation that does not assume periodic affine dynamics, linearize away Rule 30's nonlinear term, or hide the missing recurrence behind a predicate name.
