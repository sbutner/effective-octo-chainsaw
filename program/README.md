# Program: a formal theory of knowledge production and transmission

This directory is the umbrella for the project. It reframes the earlier work in `explorations/` as components of one theory. That theory runs from information-theoretic first principles, through readings, archives and literary canons, to model ecosystems, and uses LLMs as an apparatus for *retrospectively verifying* claims in fields with long-standing debates. The model case is Firth's distributional hypothesis.

## Files

| File | What it is | Edit? |
|---|---|---|
| [`spine.md`](spine.md) | The theory: design principles, nine layers L0–L8, the state vector and master relations, and a mapping of every earlier idea onto the spine | By hand |
| [`program.md`](program.md) | The exploratory program: workstreams, proof queue, experiments, bridges, phases, decisions, risks | By hand |
| [`tooling.md`](tooling.md) | Review of AI Scientist, co-scientist, co-mathematician and AlphaGeometry, and the recommended tool stack | By hand |
| [`harness.md`](harness.md) | Operating spec for the research harness: roles, workstream loop, verifier routing, verification tiers, verifying theory without solvers | By hand |
| [`checks/`](checks/info_core.md) | Typed mechanical checks (`*.py`) with hand proofs and findings (`*.md`). First module: GM T2/T4, S26 and MR1, with ablations and exact counterexamples | By hand |
| `ledger/` | One verdict file per check | Written by `tools/check.py` |
| [`claims.md`](claims.md) | Claim index with derived tiers, and the ledger | Generated |
| [`AGENTS.md`](AGENTS.md) | Conventions for agents: IDs, citation verification, claim protocol, workflow | By hand |
| [`data/claims.json`](data/claims.json) | 46 spine claims (K-*) and 5 master relations (MR-*), with status, difficulty, proof route, falsifier, dependencies and evidence | Canonical |
| [`data/concepts.json`](data/concepts.json) | Concept map: 131 nodes, each with a layer, fields and a definition; 129 typed, directed edges | Canonical |
| [`data/bibliography.json`](data/bibliography.json) | Annotated bibliography, 196 entries. Each has a verification status, layers, concepts, and the claims it supports or challenges | Canonical |
| [`data/debates.json`](data/debates.json) | 21 long-standing debates, with LLM-era evidence, verdicts and next tests | Canonical |
| [`data/experiments.json`](data/experiments.json) | 12 new experiments (E-*), linked to claims | Canonical |
| [`data/phenomena.json`](data/phenomena.json) | Menu of literature-grounded behaviors and negative controls, with emergence verdicts per formalism (seed, unreviewed) | Canonical |
| [`phenomena.md`](phenomena.md) | Emergence scoreboard and menu view | Generated |
| [`data/tasks.json`](data/tasks.json) | 20 agent-ready tasks (Q-*), with inputs, outputs and acceptance criteria | Canonical |
| [`bibliography.md`](bibliography.md) | The bibliography, readable by layer | Generated |
| [`concept-map.md`](concept-map.md) | Mermaid diagrams per layer, plus a claim index | Generated |
| [`tools/validate.py`](tools/validate.py) | The gate: schema and enums, references, cycles, ledger currency, view freshness, emergence must-pass rules | — |
| [`tools/render.py`](tools/render.py) | Builds every generated view; `--check` reports drift | — |
| [`tools/check.py`](tools/check.py) | Runs checks, writes the ledger, derives tiers; `--verify` reruns everything and diffs | — |
| [`tools/db.py`](tools/db.py), [`tools/witness.py`](tools/witness.py), [`tools/phenomena.py`](tools/phenomena.py) | Schema and loader; exact counterexample distributions; emergence scoring | — |
| [`tools/test_gates.py`](tools/test_gates.py), [`tools/setup_verifiers.sh`](tools/setup_verifiers.sh) | Mutations the gate must reject; pinned PSITIP install | — |
| [`tools/md-json-tooling/HANDOFF.md`](tools/md-json-tooling/HANDOFF.md) | Handoff for token-efficient md and JSON tooling: evidence, a rejected proposal, and the plan | By hand |

## Quick start
```
git config core.hooksPath .githooks                         # once per clone: validate.py gates every commit
program/tools/setup_verifiers.sh                            # once per container: pinned PSITIP at ~/.cache/psitip
PSITIP=~/.cache/psitip python3 program/tools/check.py       # rerun stale or missing verdicts
python3 program/tools/render.py                             # regenerate the views
python3 program/tools/validate.py --coverage                # the gate, plus a list of thin spots
python3 program/tools/test_gates.py                         # prove the gate still rejects bad states
```

## Relation to `explorations/`

| Document | Role in the spine |
|---|---|
| Grounded Misprision | The selection core (L2, L4, L5) |
| Outline v1 | The symmetric sector (L3) |
| *One Selection Law* | The behavior stage (L8) |
| Lean drafts | The lattice skeleton (L0) |

`claims.json` links K-claims to GM and OUT IDs.

## Verification status
- Tiers are in [`claims.md`](claims.md). GM T2, the T4.1 inequality, corrected GM T4.2, OUT-S26 and MR1 are V4 (mechanically proved). GM T4.2 as written is R (refuted by an exact witness). Every K-claim is V0. The matching status changes in `claims.json` await the human gate.
- 18 bibliography entries were checked in this session and 11 in earlier sessions. 165 are from memory and 2 are unverified. Clearing these is tasks Q-01 and Q-02.
- No experiments have been run.
- 37 protocol violations predate the strict gate and are listed in `tools/db.py` `DEBT` (task Q-24).
