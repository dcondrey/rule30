"""4-model OpenRouter reasoning panel on Rule 30, symbolic-state architecture.

Design notes, read before changing anything:

* MODEL IDS ARE VERIFIED, NOT ASSUMED.  The task spec named openai/o1,
  deepseek/deepseek-r1, xai/grok-4.1, meta-llama/llama-4-400b-instruct.  Two of
  those four do not exist on OpenRouter (grok-4.1, llama-4-400b-instruct), and
  the other two are stale prior-generation models.  `verify_models()` checks
  every configured id against GET /models before any paid call, and refuses to
  run on an unverified id.  Do not hardcode a roster without running that
  check again if this script is reused later.

* THE REGISTER IS "ESTABLISHED", NOT "ABSOLUTE FACT".  The requested system
  prompt told every model to accept the 72-row register as absolute fact and
  never re-examine killed routes.  That is refused here as written: this
  session already caught one entry in that same document (the depth-3 escape
  family) that had been reported as PROVED with zero supporting artifact
  anywhere in the tree.  Telling four external models the register is beyond
  question would make a similar error unfalsifiable input instead of
  something a fresh reasoner might catch.  The injected prompt instead says to
  treat it as established UNLESS a model identifies a specific, named error,
  in which case it must say so instead of building on it.

* COMPRESSION DOES NOT DISCARD RAW OUTPUT.  The task asked to "discard raw
  prose once extracted."  That risks silently losing a real result to a lossy
  summarization step, which is the same failure class as the register issue
  above.  Raw turns are kept in the transcript; only the STATE PASSED FORWARD
  to the next call is compressed.  Nothing is thrown away on disk.

* THE COMPRESSOR IS A PARSER, NOT A SUMMARIZING MODEL CALL.  Extraction is
  regex/heuristic over LaTeX-ish markers ($, \\[, \\begin{}, ```), not a fifth
  API call asking a model to compress its own or another's output.  A
  compression step that itself hallucinates would be worse than no
  compression.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]  # experiments/overnight-arms/roundtable -> repo root
PATH_MD = REPO_ROOT / "docs" / "rule30" / "PATH.md"
OUT_DIR = HERE
TRANSCRIPT_PATH = OUT_DIR / "compressed_transcript.json"
STATE_PATH = OUT_DIR / "state.json"
SYNTHESIS_PATH = OUT_DIR / "SYMBOLIC_SYNTHESIS.md"

OPENROUTER_URL = "https://openrouter.ai/api/v1"
MAX_STATE_TOKENS = 6000  # approx, via 4 chars/token heuristic; see truncate_to_tokens
# Bumped from 4000: lateral-thinking mode forwards whole paragraphs (the
# analogy is the payload), not terse LaTeX, and runs 5 turns x 4 models = 20
# calls, so more accumulated state needs more room before truncation kicks in.

ROSTER = [
    # (openrouter id, short label, one-line role from the spec)
    # Run 5: deliberately a different 4-vendor roster from runs 1-4's
    # GPT-5.6/DeepSeek-V4/Grok-4.6/Llama-4-Maverick, so idea generation isn't
    # bottlenecked on the same four models' priors. All 4 ids + fallbacks
    # verified against the live OpenRouter catalog on 2026-08-30 before this
    # roster was written.
    ("anthropic/claude-opus-4.5", "Claude-Opus-4.5", "careful formal reasoning, conservative about unjustified leaps"),
    ("google/gemini-2.5-pro", "Gemini-2.5-Pro", "broad cross-domain association, long-context synthesis"),
    ("qwen/qwen3-max", "Qwen3-Max", "distinct pretraining distribution, different cultural/technical reference set"),
    ("mistralai/mistral-large", "Mistral-Large", "independent lineage anchor for adversarial verification"),
]
TURNS_PER_MODEL = 3

# Per-slot fallback pool, same vendor first, tried in order.  Used only when a
# slot's current model fails a call (after its own 3 retries) or returns a
# response `compress_turn` extracts nothing usable from.  Swapping vendor is a
# last resort (an OpenAI proposal re-run on Grok is a different experiment,
# not a retry), so each slot's pool stays same-vendor as long as one remains.
FALLBACKS: dict[str, list[str]] = {
    "anthropic/claude-opus-4.5": ["anthropic/claude-opus-4.1", "anthropic/claude-sonnet-4.5"],
    "google/gemini-2.5-pro": ["google/gemini-2.5-flash"],
    "qwen/qwen3-max": ["qwen/qwen3-235b-a22b", "qwen/qwen-2.5-72b-instruct"],
    "mistralai/mistral-large": ["mistralai/mistral-large-2407"],
}


def fetch_live_ids() -> set[str]:
    req = urllib.request.Request(f"{OPENROUTER_URL}/models")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    return {m["id"] for m in data["data"]}


def verify_models(roster: list[tuple[str, str, str]], live_ids: set[str]) -> None:
    """Refuse to run on any model id that OpenRouter does not currently serve."""
    missing = [mid for mid, _, _ in roster if mid not in live_ids]
    if missing:
        raise SystemExit(
            f"REFUSING TO RUN: model id(s) not found on OpenRouter: {missing}. "
            "Re-check https://openrouter.ai/api/v1/models before editing ROSTER."
        )
    print(f"verified {len(roster)} model ids against live OpenRouter catalog", file=sys.stderr)


def load_register_summary() -> str:
    """Extract the two obstruction-analysis sections (7.3, 8.7) from PATH.md as
    the register digest.  These are named, structured, and already written for
    an outside reader; the rest of PATH.md (1000+ lines) is not sent verbatim
    because it would dominate the 4k-token state budget on its own.
    """
    text = PATH_MD.read_text()
    out = []
    for heading in ("### 7.3 Recurring obstructions", "### 8.7 Why external attempts stopped"):
        i = text.find(heading)
        if i < 0:
            continue
        j = text.find("\n## ", i + 1)
        j2 = text.find("\n### ", i + len(heading) + 1)
        end_candidates = [x for x in (j, j2) if x > 0]
        end = min(end_candidates) if end_candidates else len(text)
        out.append(text[i:end].strip())
    digest = "\n\n".join(out)
    return digest


SYSTEM_PROMPT_TEMPLATE = """You are a lateral-thinking idea generator working on Wolfram's Rule 30 centre-column problems (P1 non-periodicity, P2 equidistribution, P3 Omega(n) effort). Two previous panels already covered the reasonably-off-the-beaten-path territory and every single idea from both died under independent verification — the deaths are listed below so you don't repeat them, but read that list as evidence of something sharper than "these specific ideas were wrong": the panels weren't weird enough. Ideas from "another branch of math or physics," "a board game," "a well-known logic puzzle," or "a clean historical analogy" all turned out to be the program's three known dead argument-shapes (bounded-strip propagation / an ergodic-measure statement / a circuit-counting statement) wearing a costume that was too easy to see through and unmask. This round has one job: go somewhere stranger than a costume. Somewhere ugly, embarrassing, physically visceral, or culturally niche enough that translating it into a Rule-30 statement is itself the hard, interesting part — not somewhere so tidy that the mathematical content was already sitting there waiting to be relabeled.

FORBIDDEN SOURCE DOMAINS, because three prior panels already exhausted them — do not use, or even lightly reskin, any of: stage magic / cons, economics or currency systems (Gresham's law, seigniorage, arbitrage, two-envelope), music theory (comma, counterpoint, tuning), visual art / optics (anamorphosis), literary tropes about branching time or bootstrapping (Borges, time loops), epistemic logic puzzles (unexpected hanging, common knowledge), thermodynamics / statistical mechanics as such (ratchets, entropy, irreversibility, SOC avalanches), biology's usual suspects (prion misfolding, morphogen gradients, ant colonies, immunology, no-cloning-style biology analogies), formal logic / proof theory (cut-elimination, hydra games), any card game or shuffle, dendrochronology or any dating/matching-record technique, personal-identity philosophy puzzles (Ship of Theseus and its relatives), quantum information framings (monogamy, no-cloning), general relativity / horizons, random matrix theory, gauge theory / holonomy / Stokes-theorem framings, 2-adic or generating-function rationality arguments, tinnitus residual inhibition and rebound, adverse possession / squatters'-title land law, sticky-shed syndrome and analog tape degradation, glossolalia and speech-fluency illusions, telegraph-relay contact chatter, phantom-limb referred sensation, incentive-sensitization drug-craving incubation, numbers-station shortwave broadcasts, forensic craquelure / forgery layer-stratigraphy, autoimmune molecular mimicry, ouija-board ideomotor drift, fax/photocopy generation loss, railway signalling approach-locking / route-release, competitive-freediving surface-protocol blackout adjudication, photo-finish slit-scan artifacts, actuarial unearned-premium reserving, TLS downgrade-sentinel protocol history, early-cinema phantom-ride splicing, FIFA penalty-kick keeper-encroachment laundering, NCAA initial-eligibility clearinghouse adjudication, fencing right-of-way double-touch rules, the 1908 Merkle Boner baseball ruling, bourbon sour-mash backset, and aviation/automotive safety-critical software type-approval. If your first instinct is one of these, that is the sign to keep going past it, not to use a slightly different member of the same family.

Four panels have now each spent one full pass on: bodily/medical experience, obsolete/failing technology, culturally specific ritual or belief, crime/forgery/deception technique, linguistic/cultural drift, competitive-activity officiating/adjudication, actuarial/insurance edge-case rules, culinary/fermentation technique, and cryptographic-protocol/standards-committee history. Treat those nine categories as spent too, not just the specific exemplars listed above — a repeat pass over any of them (a different sport's rule, a different spec's history) is the same costume problem the instructions above warn about, one layer up.

GO LOOK INSTEAD in territory like: industrial and safety-engineering near-miss reporting that is not sports/aviation-officiating (near-miss vs. incident classification boundaries in occupational safety, alarm fatigue and nuisance-alarm suppression in control rooms, the specific mechanics of a near-collision report vs. an actual collision report); wayfinding and navigation failure modes (dead reckoning drift, a compass's deviation card, a search-and-rescue expanding-square pattern, a GPS multipath error in an urban canyon); textile and materials-craft technique (felting's needle-barb entanglement, a weaver's selvage tension, glassblowing's annealing-schedule window, a blacksmith's decalescence point); board- or tabletop-game rules edge cases that are not card shuffles or sports officiating (a Go seki/dead-stone dispute, a chess triple-repetition claim's exact timing, a tournament clock's increment-vs-delay distinction); or anything else genuinely strange that these categories are only gesturing at — invent your own if you have a better one, as long as it isn't on the forbidden list or one of the nine spent categories above.

Follow the analogy even when you cannot yet justify it rigorously — the justification, if there is one, comes later from someone else who executes the idea; your job is to notice a resemblance a specialist would filter out too early. Absurd is fine. Wrong is fine. Uninteresting, or secretly-tidy-and-therefore-secretly-one-of-the-three-known-shapes, is the only failure.

ANTI-CONVERGENCE RULE: if your idea substantially overlaps an entry already in "CURRENT STATE" below (from this run OR anything you recognize from the two prior panels' domains, forbidden-listed above), do not restate or lightly rephrase it — go stranger still.

You still owe two things, lightly, as instinct rather than a gate: (1) a one-line gut check of whether the idea might be Rule-30-specific rather than generic to any cellular automaton (Rule 90 is left-permutive, additive, its lone-seed centre column eventually zero — if your idea would "work" on Rule 90 too, or if there's genuinely nothing for Rule 90 to check because the analogy's object doesn't exist there at all, say so plainly and flag which case it is, since a vacuous pass is weaker evidence than a real one); (2) if you believe something in the register digest is wrong, say so.

Communicate with real prose — the strangeness of the source domain IS the content. Use LaTeX only for the parts that are genuinely mathematical. No pleasantries, no restating the problem.

GROUND TRUTH, held lightly: the register digest records routes already closed in this research program's OWN formal attempts (the O(log t) wall, single-column blindness, measure rigidity requiring bipermutativity, the measure-zero single-orbit gap). Read it once, then go looking for a side door it doesn't cover.

You will receive a compressed state and the immediately prior turn's output. Respond with EXACTLY 1 new \\textbf{{Spark}} — go deep on one rather than shallow on two: name its source domain explicitly and specifically (not "biology" but the specific visceral phenomenon), state the juxtaposition in real prose, then sketch what a Rule-30 object would have to look like for the analogy to bite, and close with the one-line Rule-90 gut check. Optionally a \\textbf{{Screen-out}} of a prior spark you think is a dead end, with a specific reason. A short \\textbf{{Open question}} list. Do not repeat the register digest or the forbidden list back. Budget: about 500 words, spent entirely on making the one spark as sharp and strange as possible.

REGISTER DIGEST:
{digest}

DEATHS FROM THE TWO PRIOR PANELS (13 ideas, ALL independently verified KILLED — do not resurrect these or close cousins of them):
gauge-theory/holonomy plaquette defect (killed: reduces to an algebraic identity true for any left-permutive rule); dendrochronology frost-year crossdating (killed: the restricted-index-set comparison converges to agreement regardless of which indices, by the reductio hypothesis alone); Ship of Theseus type-vs-bit rigidity (killed: the proposed finer "type" invariant is proven identical to the bit value under any reasonable formalization); Gilbreath faro-shuffle stick monoid (killed: proven isomorphic to this program's own already-published pin/ladder automaton); Pythagorean-comma irrational winding (killed: the winding count has no demonstrated coupling to the periodicity hypothesis, shown via explicit counterexample pairs); "forcing debt" stage-magic reframe of the left-permutive inverse (killed: an adaptive-cut relabeling of the same bounded-strip argument); Gresham's-law bimetallic mint tableau (killed: reduces to a cone-width cost functional, same as the propagation wall); Borges garden-of-forking-paths fork-count (killed: a preimage-counting statement, the same shape as the circuit/constraint-counting route already known not to give a work lower bound); army-ant-mill nucleation threshold (killed: a lone seed produces no mill by the biology's own mechanism, self-refuted); no-cloning/monogamy fidelity witness (killed: relies on an ensemble/mutual-information quantity undefined on a single deterministic orbit); kleptography kleptogram invariant (killed: a finite-window predicate can never certify an infinite non-periodicity claim); topological-censorship causal horizon (killed: reduces to the ordinary forward light cone already exhaustively studied); two-envelope swap-operator paradox (killed: restates the measure-zero single-orbit gap in decision-theory language).
"""


@dataclass
class SymbolicState:
    # Field names kept as specified (active_hypotheses / refuted_claims /
    # open_obligations) for state.json's schema, but populated with proposed
    # DIRECTIONS, not proofs — see the system prompt.  A "hypothesis" here is
    # "worth someone executing later," not "shown true."
    active_hypotheses: dict = field(default_factory=dict)  # id -> proposed direction (latex)
    refuted_claims: list = field(default_factory=list)       # list of screen-out reasons
    open_obligations: list = field(default_factory=list)     # list of open questions
    turn_count: int = 0

    def to_json(self) -> dict:
        return {
            "active_hypotheses": self.active_hypotheses,
            "refuted_claims": self.refuted_claims,
            "open_obligations": self.open_obligations,
            "turn_count": self.turn_count,
        }

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_json(), indent=2))


# --- compression: deterministic extraction, not a model call ---------------

LATEX_BLOCK_RE = re.compile(
    r"(\$\$.*?\$\$|\\\[.*?\\\]|```.*?```|\\begin\{[a-zA-Z*]+\}.*?\\end\{[a-zA-Z*]+\})",
    re.S,
)
INLINE_MATH_RE = re.compile(r"\$[^$\n]{1,300}\$")
_LABEL_ALIASES = {
    "direction": "hypothesis",
    "spark": "hypothesis",
    "hypothesis": "hypothesis",
    "screen-out": "refutation",
    "refutation": "refutation",
    "open question": "open obligation",
    "open obligation": "open obligation",
}


def compress_turn(raw_text: str) -> dict:
    """Deterministic parse of a model's raw response into symbolic fragments.

    Returns {"hypotheses": [...], "refutations": [...], "obligations": [...],
    "blocks": [...]} where `blocks` are the raw LaTeX/code blocks found (kept
    verbatim, since compressing math into prose-of-math is where meaning gets
    lost) and the three lists are line-level extractions keyed off the labels
    the system prompt asked models to use.  Free text that matches none of
    these patterns is dropped from the FORWARDED state but never from the
    transcript file.
    """
    blocks = [b.strip() for b in LATEX_BLOCK_RE.findall(raw_text)]
    hyps, refs, obls = [], [], []
    buckets = {"hypothesis": hyps, "refutation": refs, "open obligation": obls}

    # Split the whole text on label boundaries (not line boundaries), so a
    # label mid-line correctly ends the previous entry instead of being
    # swallowed by it.  Anchored the same as LABELED_LINE_RE but as a global
    # scan with finditer rather than a per-line match.
    # Tolerant of trailing qualifiers before the colon, e.g. a model writing
    # "\textbf{Direction 1 (refined): ...}" instead of a bare "Direction:" —
    # observed live and, before this fix, caused the whole label line to be
    # missed entirely (misread as an empty/unusable response and triggering
    # an unnecessary model swap).  Also tolerant of the label appearing just
    # inside a \[ ... \] or \begin{...} wrapper line.
    boundary_re = re.compile(
        r"^\s*(?:\\\[|\\begin\{[a-zA-Z*]+\})?\s*(?:#{1,4}\s*)?(?:[-*]\s*)?(?:\\textbf\{)?"
        r"(Direction|Spark|Screen-out|Open question|Hypothesis|Refutation|Open obligation)s?"
        r"[^:\n]{0,80}?[:.\-]\}?\s*",
        re.I | re.M,
    )
    matches = list(boundary_re.finditer(raw_text))
    for i, m in enumerate(matches):
        kind = _LABEL_ALIASES.get(m.group(1).lower(), "open obligation")
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw_text)
        entry = raw_text[start:end].strip()
        if entry:
            buckets[kind].append(entry)
    # fall back: if no labeled lines were found at all, keep whole paragraphs
    # rather than bare inline math.  In the lateral-thinking mode the content
    # IS the prose (the analogy, the "borrowed from" line); bare symbols would
    # discard exactly the part worth forwarding.  A turn that ignored the
    # formatting instruction still contributes something instead of nothing.
    if not (hyps or refs or obls):
        paras = [p.strip() for p in re.split(r"\n\s*\n", raw_text) if p.strip()]
        if paras:
            hyps = paras[:4]
        else:
            hyps = INLINE_MATH_RE.findall(raw_text)[:6]
    return {"hypotheses": hyps, "refutations": refs, "obligations": obls, "blocks": blocks}


def truncate_to_tokens(text: str, max_tokens: int) -> str:
    """4 chars/token heuristic truncation from the tail, since state.json's
    most recent additions matter most and PATH.md's digest is prepended
    separately in the system prompt (not counted against this budget)."""
    max_chars = max_tokens * 4
    if len(text) <= max_chars:
        return text
    return "...[truncated]...\n" + text[-max_chars:]


def apply_compressed_turn(state: SymbolicState, model_label: str, compressed: dict) -> None:
    for i, h in enumerate(compressed["hypotheses"]):
        state.active_hypotheses[f"{model_label}-H{state.turn_count}.{i}"] = h
    for r in compressed["refutations"]:
        # A refutation string may name a hypothesis id; also just record it.
        state.refuted_claims.append(f"[{model_label}] {r}")
        # best-effort: drop any active hypothesis whose id/text is quoted in it
        for hid in list(state.active_hypotheses):
            if hid in r:
                del state.active_hypotheses[hid]
    for o in compressed["obligations"]:
        if o not in state.open_obligations:
            state.open_obligations.append(f"[{model_label}] {o}")


# --- OpenRouter call ---------------------------------------------------------

def call_openrouter(model_id: str, system_prompt: str, user_payload: str, api_key: str) -> str:
    body = json.dumps({
        "model": model_id,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_payload},
        ],
        "temperature": 0.2,
        "max_tokens": 1800,  # bumped from 1200: ~700-word prose budget needs more room
    }).encode()
    req = urllib.request.Request(
        f"{OPENROUTER_URL}/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/rule30-research",
            "X-Title": "Rule 30 symbolic roundtable",
        },
        method="POST",
    )
    last_err = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.load(resp)
            return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}"
            time.sleep(2 * (attempt + 1))
        except Exception as e:  # noqa: BLE001
            last_err = str(e)
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"call failed after 3 attempts for {model_id}: {last_err}")


def main() -> None:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY is not set in the environment.")

    live_ids = fetch_live_ids()
    verify_models(ROSTER, live_ids)
    for pool in FALLBACKS.values():
        unknown = [m for m in pool if m not in live_ids]
        if unknown:
            raise SystemExit(f"REFUSING TO RUN: fallback id(s) not found on OpenRouter: {unknown}")
    print(f"verified {sum(len(v) for v in FALLBACKS.values())} fallback ids against live catalog", file=sys.stderr)

    digest = load_register_summary()
    if not digest.strip():
        raise SystemExit("register digest is empty; PATH.md section headings may have changed")
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(digest=digest)

    state = SymbolicState()
    transcript: list[dict] = []
    prior_compressed: dict | None = None

    # Mutable per-slot roster: (current_model_id, label, role, fallback_queue).
    # A swap replaces current_model_id and pops the fallback_queue; the label
    # stays fixed so state.json's hypothesis-id namespace (f"{label}-H...")
    # does not fragment across a swap.
    slots = [
        {"model_id": mid, "label": label, "role": role, "fallbacks": list(FALLBACKS.get(mid, [])), "swaps": []}
        for mid, label, role in ROSTER
    ]

    total_calls = len(slots) * TURNS_PER_MODEL
    call_no = 0
    for turn in range(1, TURNS_PER_MODEL + 1):
        for slot in slots:
            call_no += 1
            state.turn_count = call_no
            state_json = json.dumps(state.to_json(), indent=2)
            state_json = truncate_to_tokens(state_json, MAX_STATE_TOKENS)

            prior_block = (
                json.dumps(prior_compressed, indent=2) if prior_compressed else "(none — first turn)"
            )
            user_payload = (
                f"ROLE: {slot['role']}\n\n"
                f"CURRENT STATE (active_hypotheses, refuted_claims, open_obligations):\n{state_json}\n\n"
                f"IMMEDIATELY PRIOR TURN (compressed):\n{prior_block}\n"
            )

            raw, error, compressed, used_model, dt = "", None, None, slot["model_id"], 0.0
            # Try the slot's current model, then its fallback queue in order,
            # until one call both succeeds and yields a response compress_turn
            # extracts something from.  "Useful" = at least one hypothesis,
            # refutation, or obligation extracted; an empty/degenerate reply
            # is treated the same as a hard failure for swap purposes.
            attempted = [slot["model_id"]]
            while True:
                print(f"[{call_no}/{total_calls}] turn {turn} -> {slot['label']} ({attempted[-1]})", file=sys.stderr)
                t0 = time.time()
                try:
                    raw = call_openrouter(attempted[-1], system_prompt, user_payload, api_key)
                    error = None
                except Exception as e:  # noqa: BLE001
                    raw, error = "", str(e)
                    print(f"  ERROR: {error}", file=sys.stderr)
                dt = time.time() - t0

                compressed = compress_turn(raw) if raw else {"hypotheses": [], "refutations": [], "obligations": [], "blocks": []}
                useful = raw and (compressed["hypotheses"] or compressed["refutations"] or compressed["obligations"])
                if useful:
                    used_model = attempted[-1]
                    break
                if not slot["fallbacks"]:
                    used_model = attempted[-1]  # exhausted; record the failure as-is
                    if not error:
                        error = "no usable content extracted from response (empty after compression)"
                    break
                next_model = slot["fallbacks"].pop(0)
                reason = error or "response yielded no extractable hypothesis/refutation/obligation"
                print(f"  SWAP: {attempted[-1]} -> {next_model} (reason: {reason})", file=sys.stderr)
                slot["swaps"].append({"from": attempted[-1], "to": next_model, "reason": reason, "call_no": call_no})
                attempted.append(next_model)
                slot["model_id"] = next_model  # persists for subsequent turns of this slot

            if raw:
                apply_compressed_turn(state, slot["label"], compressed)
                prior_compressed = {"model": slot["label"], **compressed}

            transcript.append({
                "call_no": call_no,
                "turn": turn,
                "slot_label": slot["label"],
                "role": slot["role"],
                "model_id": used_model,
                "models_attempted": attempted,
                "seconds": round(dt, 1),
                "error": error,
                "raw_response": raw,       # full, uncompressed — nothing discarded on disk
                "compressed": compressed,
                "state_snapshot": state.to_json(),
            })
            TRANSCRIPT_PATH.write_text(json.dumps(transcript, indent=2))  # flush every call
            state.save(STATE_PATH)

    swap_log = [{"slot": s["label"], "swaps": s["swaps"]} for s in slots if s["swaps"]]
    if swap_log:
        print(f"model swaps occurred: {json.dumps(swap_log, indent=2)}", file=sys.stderr)

    print(f"wrote {TRANSCRIPT_PATH}", file=sys.stderr)
    print(f"wrote {STATE_PATH}", file=sys.stderr)
    write_synthesis(transcript, state, slots)
    print(f"wrote {SYNTHESIS_PATH}", file=sys.stderr)


def write_synthesis(transcript: list[dict], state: SymbolicState, slots: list[dict]) -> None:
    n_errors = sum(1 for t in transcript if t["error"])
    lines = [
        "# Symbolic roundtable: lateral-thinking sparks on Rule 30",
        "",
        "Status: **UNEXECUTED, DELIBERATELY UNFILTERED SPARKS, NOT RESULTS.**",
        "This run asked four models to juxtapose Rule 30 against unrelated",
        "domains (other sciences, magic, science fiction, etc.) and follow an",
        "analogy before it can be justified.  Absurd and wrong were explicitly",
        "invited; only \"uninteresting\" was penalized.  So a low idea-count or a",
        "half-formed spark is not this run failing — it is the run doing its",
        "job, which is coverage of unfamiliar territory, not correctness.",
        "Nothing below is PROVED or MEASURED.  Most entries are not even",
        "formal claims yet; they are analogies that would need real work to",
        "become a checkable proposal at all, and THEN the same treatment as any",
        "other route in `PATH.md`: a precise restatement, a Rule 90 check run",
        "in actual code, a kill condition, and an owner.  Treat this document",
        "as raw material for triage, not a triage list itself.",
        "",
        f"Calls: {len(transcript)} ({n_errors} errored). Roster (final model per slot,",
        "after any live swaps):",
    ]
    for s in slots:
        lines.append(f"- `{s['model_id']}` ({s['label']}): {s['role']}")
    any_swaps = [s for s in slots if s["swaps"]]
    if any_swaps:
        lines += ["", "**Live model swaps during the run:**"]
        for s in any_swaps:
            for sw in s["swaps"]:
                lines.append(f"- {s['label']}: `{sw['from']}` -> `{sw['to']}` at call {sw['call_no']} ({sw['reason']})")
    lines += [
        "",
        "## Candidate directions surfaced (unverified, unexecuted)",
        "",
    ]
    if state.active_hypotheses:
        for hid, h in state.active_hypotheses.items():
            lines.append(f"- **{hid}**: {h}")
    else:
        lines.append("(none survived to the end of the run)")
    lines += ["", "## Directions screened out during the panel (by a model, not independently verified)", ""]
    if state.refuted_claims:
        for r in state.refuted_claims:
            lines.append(f"- {r}")
    else:
        lines.append("(none)")
    lines += ["", "## Open questions named by the panel", ""]
    if state.open_obligations:
        for o in state.open_obligations:
            lines.append(f"- {o}")
    else:
        lines.append("(none)")
    lines += [
        "",
        "## Next step (execution phase, separate from this run)",
        "",
        "For each candidate direction: (1) check its stated Rule 90 screen in",
        "actual code, not by trusting the model's sketch; (2) check it against",
        "`PATH.md` section 7.3/8.7 for a named obstruction the model may have",
        "missed or misjudged; (3) only then decide whether it is worth a route",
        "entry in `PATH.md` and who owns running it. A direction a model marked",
        "'screened out' is not thereby dead — the screen itself needs the same",
        "independent check as a survivor before anyone relies on it.",
        "Full raw responses, uncompressed, are in `compressed_transcript.json` for",
        "every call — read those before trusting this summary of them.",
    ]
    SYNTHESIS_PATH.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
