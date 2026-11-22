# Tooling: what to take from AI Scientist, co-scientist, co-mathematician and AlphaGeometry

*2026-11-22. Each repository below was cloned and read this session. The co-mathematician paper (arXiv:2605.06651) was read in full. PSITIP was cloned but **not run**: the sandbox blocked running downloaded code.*

## 1. Bottom line

The four systems fall into two groups: workbenches for empirical ML papers, and narrow geometry provers. This program is mostly **proofs, definitions and citation hygiene**, plus a set of cheap simulations. No single system fits that. A useful stack takes one or two specific parts from each:

| Need in this repo | Take from | What exactly |
|---|---|---|
| Orchestration and state | **Co-mathematician** (design only; no code released) | Coordinator → workstreams → review gates, a living working paper with provenance notes, and a durable record of failures. Implemented on Claude Code over `program/` |
| Conjectures, falsifiers and debate verdicts | **Co-scientist**, via `jataware/open-coscientist` | Generate → review → Elo tournament → evolve → deduplicate, aimed at claims and debates rather than biology |
| Mechanical proof of the information-theoretic core | **AlphaGeometry's pattern** (symbolic closure plus an LLM that proposes auxiliary constructions), with **PSITIP** in the symbolic role | Shannon-type inequalities under Markov and conditional-independence constraints, plus counterexample search |
| Simulations: the cyclic world and E-series | **AI Scientist v1 template mode**; **v2 tree search** later | A fixed `experiment.py` and `plot.py` template that the agent edits; v2's staged best-first tree search for open-ended runs |
| Review of drafts | **AI Scientist v1 `perform_review.py`** plus co-mathematician-style persistent reviewers | Review-form ensemble as a gate before any PaperOrchestra draft leaves the repo |
| Formal statements | DeepMind **`formal-conjectures`** (Lean 4 + Mathlib) conventions | State K-claims as Lean theorems with `sorry`, each tagged with a status attribute |

## 2. What is actually open

| System | What's released | License | LLM backend | Notes |
|---|---|---|---|---|
| **AI Scientist v1** (`SakanaAI/AI-Scientist`) | Full pipeline: idea generation, template experiments via Aider, write-up, `perform_review.py`. 11 templates (nanoGPT, grokking, probes, SEIR…) | AI Scientist Source Code License (RAIL-based) | `anthropic` and `openai` SDKs, Aider | The license's **§3.2(e) requires a prominent disclosure** in any manuscript produced with it. That's compatible with this repo's honesty rules, but mandatory |
| **AI Scientist v2** (`SakanaAI/AI-Scientist-v2`) | Template-free ideation (Semantic Scholar), 4-stage best-first tree search with parallel workers and a journal, plotting, write-up, LLM and VLM review | Same license | `anthropic` and `openai` SDKs; Bedrock and Vertex for Claude | Built for Linux and NVIDIA GPUs. Default models are 2024-era. About 13k lines; the tree search is the reusable core |
| **AI co-scientist** (Google) | **No code.** Paper arXiv:2502.18864; a 2026 *Nature* paper is reported in search results (not checked here) | — | — | Two community versions: `jataware/open-coscientist` (active Feb 2026; LangGraph + **LiteLLM**; MCP literature tools; **MIT + Commons Clause**, which forbids selling, not research use) and `conradry/open-coscientist-agents` (MIT, last commit Jul 2025, LangChain) |
| **AI co-mathematician** (DeepMind) | **No code**; limited release. The paper describes the architecture in enough detail to copy | — | Gemini, including Deep Think | Uses no custom models; it is a harness, so the design carries over to Claude Code |
| **AlphaGeometry 1** (`google-deepmind/alphageometry`) | Deductive database + algebraic reasoning (DD+AR), beam search, LM inference (JAX/meliad); weights fetched via `bit.ly` | Apache-2.0 | Its own 150M-parameter model | The domain (Euclidean geometry) is irrelevant here. The architecture is the lesson |
| **AlphaGeometry 2** (`google-deepmind/alphageometry2`) | **DDAR only** (about 2.4k lines, numpy) with test problems; no LM, no search | Apache-2.0 | none | The symbolic engine alone |

Two adjacent open projects are referenced by these systems:

- **`google-deepmind/formal-conjectures`**: Apache-2.0, Lean `v4.33.1` + Mathlib, active as of yesterday. A house style for stating open problems formally, with category and status attributes.
- **OpenEvolve** (`algorithmicsuperintelligence/openevolve`): Apache-2.0. The co-mathematician paper cites it as the open counterpart of AlphaEvolve, for search and optimization workstreams.

## 3. Fit with the program's workstreams (`program.md` §2)

| Workstream | Biggest bottleneck now | Best tool |
|---|---|---|
| GROUND (Q-01–03, Q-09, Q-20): 165 from-memory references | Verifying references against primary pages, at scale, without hallucination | Co-mathematician's "systematic citation checking" reviewer, backed by Semantic Scholar and arXiv (both allowed hosts). v2's `tools/semantic_scholar.py` is a minimal client |
| FORMALIZE (Q-04–06) | Making definitions agree across GM, the outline and the spine | Co-scientist tournament over candidate definitions: each candidate is scored by how many claims it lets you state without patches |
| PROVE (Q-08, Q-10–13; S10, S25) | No proofs written yet | **The AlphaGeometry pattern with PSITIP** for the information-theoretic core: GM T1/T2/T4, K10, K26, S26, MR1. Sympy/numpy checks for the harmonic-analysis results (S4, S10, S18, S25). Lean via `formal-conjectures` style once paper proofs stabilize |
| EXTEND (Q-14; E-01, E-04, E-05, E-12; X1–X14) | No experiments run | AI Scientist v1 **template** for the cyclic world (CPU, deterministic, exact 𝒢); v2 tree search for E-01/E-04, which need many model samples |
| CONNECT (Q-15–17 bridges) | Writing for specialists without overclaiming | PaperOrchestra (already set up), gated by the v1 reviewer ensemble and the claim-status check |
| Debate audit (21 debates) | Turning each debate into a verdict | Co-scientist's scientific-debate tournament fits this almost literally: hypotheses = verdicts, the judge must cite `checked` sources only |

## 4. The recommended stack, layer by layer

### L0. Workbench: a co-mathematician-style harness on Claude Code

Build no new framework. Map the paper's architecture onto what this repo already has:

| Co-mathematician | Here |
|---|---|
| Project coordinator agent | The main Claude Code session |
| Approved research question and goals | `program/data/tasks.json` (Q-*) |
| Workstream coordinator | One subagent, or one cloud session, per Q-task |
| Shared file system and version history | The git branch; `program/data/*.json` is the canonical state |
| Working paper with margin notes (provenance, contentiousness) | Each claim's `status`, `evidence` and `log`, plus a `program/workstreams/<Q>/report.md` per task |
| Hard programmatic constraints | `validate.py` must pass; "no from-memory evidence in bridges"; tests must pass before code counts as done |
| Persistent reviewer agents; escalate on stall | A reviewer subagent per workstream that must approve before a task becomes `done`; otherwise `blocked`, with the reason |
| Failed explorations kept as first-class records | New `program/workstreams/<Q>/failures.md`. Never delete a refuted claim; mark it `refuted` and keep the counterexample |

Additions needed:

- the `refuted` status and a `failures.md` convention in `AGENTS.md`;
- a reviewer-gate step in the per-task workflow.

### L1. Hypotheses and conjectures: `open-coscientist`

- **Use for:**
  - candidate formalizations of each K-claim, and candidate falsifiers;
  - ranking the E-series by decisiveness per unit of cost;
  - debate verdicts.
- **Adapt it:**
  - Write a domain YAML (its "Domain Customization") whose literature MCP is Semantic Scholar plus arXiv instead of PubMed.
  - Add prompt guidance that enforces the claim protocol: status, falsifier, checked evidence.
- **Subscription inference:** it calls models through LiteLLM. A small LiteLLM `CustomLLM` provider that shells out to `claude -p` works the same way as `paperorchestra/claude_backend.py`.
- **Output** goes into `claims.json` and `debates.json` as `conjecture` entries with a falsifier, never as `known`.

### L2. Symbolic core: the AlphaGeometry pattern for information theory

AlphaGeometry's lesson is the division of labor:

- a complete, sound symbolic engine (DD+AR) computes the deductive closure of the premises;
- a language model proposes only the *auxiliary constructions* the engine cannot invent;
- traceback extracts a minimal proof.

The theorems in this program's core are mostly linear information inequalities under conditional-independence constraints. The data-processing chain in S26, GM T2/T4, K10, K26 and the Unified Channel Law (MR1) all have this shape. For that class, **PSITIP** is the symbolic engine:

- it runs the Yeung–Zhang linear-programming method;
- it handles Markov chains and Bayesian networks;
- it searches for counterexample distributions;
- it produces human-readable proofs.

The LLM's role is the auxiliary construction, as in AlphaGeometry: choose the auxiliary random variables, the conditioning sets and the factorization that make an inequality Shannon-provable. Concretely:

1. **Translate each target into PSITIP form.** For example, HANDOFF correction 1 (GM T4.2) becomes "`C=f(D,ξ)` and `ξ⊥Ω` ⊬ `I(Ω;D,C)≤I(Ω;D)`, but `ξ⊥Ω|D` ⊢ it". PSITIP should return the XOR counterexample for the first and a proof for the second.
2. **Prove or refute,** and store each proof or counterexample under `program/proofs/` (the claim protocol already expects proof files there).
3. **When the LP fails,** have the LLM propose auxiliary variables and retry. That is AlphaGeometry's loop.

PSITIP is GPL-3.0. Using it is fine; vendoring or redistributing it would make derived code GPL.

*Not tested yet.* A first run should check S26, GM T4.2 (both versions) and MR1 in PSITIP, then compare the results with the hand analysis in HANDOFF §4.

The harmonic-analysis results (S4, S10, S18, S25, S30) aren't information inequalities. For those, the "symbolic engine" is exact computation over ℤ_N in sympy or numpy, plus Lean on `ZMod 12` (outline §8).

### L3. Experiments: the AI Scientist, scoped down

- **First: a v1 template, `templates/cyclic_world/`.** It contains:
  - `experiment.py` with the outline §6 world (Ω = ℤ_N × seasonal phenomena, two hemispheres, equivariant lexicalization with designated irregularities);
  - exact 𝒢;
  - a generational map (S21) and the metrics (Plancherel CKA, per-irrep radii, the B⊥ split).

  Template mode is the right fit because the testbed is fixed and small. The agent varies parameters and mechanisms rather than designing systems from scratch. This one template serves X2, X4, X5, X7, X11, X12 and X14, and calibrates every proxy before it touches natural text (`program.md`, EXTEND).

  Run it with Claude Code as the coding agent instead of Aider. Reuse v1's `generate_ideas.py` novelty check (Semantic Scholar) and its `perform_review.py`.
- **Later: v2's best-first tree search** for E-01 and E-04. These need many model samples and real training runs, so they're open-ended and need a GPU.
  - Reuse `treesearch/` (journal, parallel agents, staged search).
  - Replace the 2024 default models and route `ai_scientist/llm.py` through `claude -p`, as with PaperOrchestra.
  - Expect GPU and environment work. v2 assumes CUDA.
- **License duty:** anything written with either version needs the AI disclosure in its abstract or methods section (§3.2(e)).

### L4. Search and optimization: OpenEvolve, when needed

Use it when a workstream needs a construction rather than a proof. Examples:

- spectra that make S25's bound tight;
- worst-case channels for S14;
- small finite worlds that break a conjectured threshold (S28, K33).

The co-mathematician paper names it as the place an evolutionary engine slots into a workstream. Not urgent.

### L5. Formalization: Lean conventions from `formal-conjectures`

When Lean comes back (HANDOFF §6.2), copy its conventions:

- state each K-claim as a Lean theorem with `sorry`, tagged with a status attribute (open, solved, false);
- add proofs only once the paper proof is stable.

This also gives the `InfoLattice` / irrep-lattice work (S31) a shape that could be contributed upstream.

It needs a Lean toolchain and a Mathlib cache. Neither is installed. Fetching them likely needs hosts that aren't allowed in this environment; check before trying.

### L6. Writing and review

- PaperOrchestra, already wired in `paperorchestra/`, with a reviewer gate:
  - the v1 `perform_review.py` ensemble (NeurIPS form, reflection, meta-review);
  - a claim-status checker that fails a draft if a `new` or `conjecture` claim is stated as proved, or if it cites a `from-memory` entry.
- Co-mathematician's rules on write-ups apply too:
  - exposition of the process, not just the result;
  - margin notes linking each claim to `claims.json` IDs;
  - review rounds that end only when every reviewer approves, or the workstream escalates.

## 5. What not to use

- **AlphaGeometry code itself.** The geometry DSL, DD rules and LM weights don't carry over. Keep the pattern, not the code.
- **AI Scientist end to end.** Its full loop is "idea → experiments → paper" for ML benchmarks. Run on this program, it would invent empirical results for what is mostly a theory program. Use its parts.
- **`conradry/open-coscientist-agents`** as the primary co-scientist: it has been dormant since July 2025. Keep it as a reference only.

## 6. Suggested order

1. **L0 conventions.** Add `refuted`, `failures.md` and the reviewer gate to `AGENTS.md`. Cheap, and everything else depends on it.
2. **L2 PSITIP pilot** on S26, GM T4.2 and MR1. This is the fastest route to the first actual proofs (Q-08). It needs approval to run PSITIP's code.
3. **L3 `cyclic_world` template** with closed-form unit tests (S4's odd harmonics vanish at s=½; S18's gains 0.91/0.67/0.33/0/0.24). These unlock the X-series and Q-14.
4. **L1 open-coscientist** with a subscription-routed LiteLLM provider, first on debates.json and E-series ranking.
5. **L6 reviewer gate** for PaperOrchestra drafts.
6. **L5, L4 and v2 tree search** as Lean, search problems and GPUs become relevant.

## Sources

- Lu et al., *The AI Scientist*, and Yamada et al., *The AI Scientist-v2* (arXiv:2504.08066). Code and LICENSE read at `SakanaAI/AI-Scientist@2025-12-19` and `SakanaAI/AI-Scientist-v2@2025-12-19`.
- Gottweis et al., *Towards an AI co-scientist* (arXiv:2502.18864). Community code read at `jataware/open-coscientist@2026-02-25` and `conradry/open-coscientist-agents@2025-07-21`.
- Zheng et al., *AI Co-Mathematician: Accelerating Mathematicians with Agentic AI* (arXiv:2605.06651; full text read).
- Trinh et al. (2024), *Nature* (AlphaGeometry), and *Gold-medalist Performance in Solving Olympiad Geometry with AlphaGeometry2* (arXiv:2502.03544; JMLR 26). Code read at `google-deepmind/alphageometry@2026-01-05` and `google-deepmind/alphageometry2@2026-01-07`.
- `google-deepmind/formal-conjectures@2026-11-21` (arXiv:2605.13171).
- `algorithmicsuperintelligence/openevolve@2026-11-22`.
- `cheuktingli/psitip@2025-06-10` (README read; not executed).
