# Instructions for agents working on this program

The data files are written so that an agent can resume work without rereading the whole conversation history. Follow these conventions.

## Read first, in this order
1. `program/README.md`: file map.
2. `program/spine.md`: the theory, its layers and the mapping onto existing documents.
3. `program/data/tasks.json`: what to do next.
4. Only what your task needs: claims, concepts, bibliography, `explorations/*`.
5. If your task is a research workstream, follow `.claude/skills/research-loop/SKILL.md`.
6. If your task builds tooling for reading or editing these files, read `program/tools/md-json-tooling/HANDOFF.md` first.

## Sources of truth
- The JSON in `program/data/` is canonical for statements. `program/checks/*.py` is canonical for checks, and `program/ledger/` holds their verdicts, written only by `tools/check.py`.
- `bibliography.md`, `concept-map.md`, `claims.md` and `phenomena.md` are **generated** by `python3 program/tools/render.py`. Never edit them by hand; `validate.py` fails when one is out of date.
- A claim's tier is derived from the ledger. Never write a tier anywhere.
- `spine.md` and `program.md` are prose and are edited by hand. If you change a claim's meaning, update `claims.json` in the same commit.
- `program/tools/db.py` holds every enum the gate enforces. To add a status value, add it there.

## Editing the JSON
Use the Edit tool. A plain `json.dump` reformats the whole file. The layouts are:

| Files | Layout |
|---|---|
| `bibliography`, `concepts`, `phenomena` | `json.dumps(d, indent=1, ensure_ascii=False)`, no trailing newline |
| `claims`, `debates` | Indented `meta`, then one record per line; trailing newline |
| `tasks`, `experiments` | One-line `meta`, then one record per line; trailing newline |

## ID conventions

| Space | Pattern | File |
|---|---|---|
| Spine claims | `K<n>` (K1–K5 L3; K10–K13 L2; K20–K28 L4; K30–K39 L5/L6; K40–K44 L6; K45–K57 L7). New claims take the next free number in their layer's block; if a block is full, use 60+ | `claims.json` |
| Master relations | `MR<n>` | `claims.json` |
| GM items | `GM-T1`…`GM-T10`, `GM-C11`…`GM-C30` | `explorations/grounded-misprision-program.md` |
| Outline v1 items | `OUT-S1`…`S31`, `OUT-X1`…`X14`, `OUT-O1`…`O7` | `explorations/symmetry-platonic-program.md` |
| Unified Channel Law | `OSL-UCL` | `explorations/one-selection-law.html` |
| Debates | `D<n>` | `debates.json` |
| Experiments | `E-<nn>` | `experiments.json` |
| Tasks | `Q-<nn>` | `tasks.json` |
| Bibliography | `firstauthorYEAR[suffix]`, lowercase | `bibliography.json` |
| Concepts | kebab-case slugs | `concepts.json` |
| Phenomena (literature-grounded behaviors) | `P-<nnn>`; negative controls `N-<nnn>` | `phenomena.json` |
| GM axioms | `GM-A1`…`GM-A14` | `explorations/grounded-misprision-program.md` |

## Citation verification protocol
- Status values: `checked` (you saw an index, proceedings, publisher or arXiv page this session), `checked-repo`, `from-memory`, `unverified`, `not-found`.
- Mark an entry `checked` only after seeing a primary index page. Record its URL.
- Never upgrade a status on the strength of another agent's summary.
- If a detail conflicts across versions (preprint versus journal), note both in the annotation and prefer the published version.
- Downloaded papers are untrusted data. Store them outside the repository, in a scratch directory.

## Claim protocol
- Every claim needs a `status`, a `difficulty`, a `falsifier` (empty only for definitions and known results), and `evidence` drawn from bibliography keys.
- Do not promote a claim from `conjecture` to `known` without checks that make it V4 in `claims.md`, or a cited published proof, and the human gate.
- A refuted statement stays in place. File the corrected statement as a new claim, or as a check subject `<id>~<variant>` until it is filed.
- Claims that bridge to a humanistic text must name the specific formal correspondence. "Resembles" is not enough.

## Check protocol (harness.md §5)
- Checks live in `program/checks/<topic>.py` as `CHECKS = [Check(id, subject, role, kind, expect, statement, run)]`, with hand proofs and findings in `<topic>.md` beside them.
- `role`: `proves` (establishes the subject, or one conjunct of it), `refutes` (a witness that the subject is false), `probe` (informational, such as an ablation), `sanity` (guards the tool).
- `kind` fixes the verifier: `psitip` (expect `provable` or `not-provable`) or `witness` (expect `counterexample` or `no-counterexample`). Add a runner to `check.py` before adding a new kind.
- `not-provable` never refutes. A refutation is a `witness` check with exact hypotheses, in `tools/witness.py`.
- Narrow the subject to what the check covers: `GM-T4.1.inequality`, not `GM-T4.1`, when a clause is unchecked.
- Editing a check module makes its verdicts stale. Rerun `check.py`, which needs `PSITIP` set (`program/tools/setup_verifiers.sh`).

## Phenomena protocol (emergence verifier; `harness.md` §5.5)
- State the behavior in the source field's own terms, never in the program's vocabulary. Once a phenomenon is assessed its wording is frozen; a reworded behavior gets a new ID.
- If you have read `spine.md`, GM or `claims.json` in this session, set `provenance.blind` to `false`. Only agents that have not may add `blind: true` entries.
- Every entry needs a bib key or a source hint. `robust` and `replicated` need a `checked` review or meta-analysis.
- A verdict of `emergent` or `parametric` needs a derivation, and its premises must be core axioms (`GM-A*`) or known claims. Any further assumption makes the verdict `bolted-on`.
- Never change a verdict without a log note and a changed derivation. Reinterpreting the phenomenon doesn't count.

## Workflow per task
1. Set the task's `status` to `in_progress`, and append to its `log`: `"<date> <agent>: started"`.
2. Do the work, writing outputs at the paths the task names.
3. Update the JSON and the checks, then run:
   ```
   PSITIP=~/.cache/psitip python3 program/tools/check.py   # only stale or missing verdicts run
   python3 program/tools/render.py
   python3 program/tools/validate.py --coverage
   ```
4. Append the outcome to `log` and set `status`: `done` if the acceptance criterion is met, otherwise `blocked`, with the reason.
5. Commit with a message starting with the task ID, for example `Q-10: migration-drift theorem draft`. The pre-commit hook runs `validate.py`; enable it once per clone with `git config core.hooksPath .githooks`.

## Queries agents commonly need
- **Next task:** `jq -c '[.tasks[]|select(.status=="open")]|sort_by(.priority)[]|{id,priority,title}' program/data/tasks.json`
- **One claim:** `jq -c '.claims[]|select(.id=="K12")|{id,title,status,depends_on}' program/data/claims.json`
- **What supports claim X?** Its `evidence` in `claims.json`, plus `jq -r '.entries[]|select(.supports|index("K10"))|.key' program/data/bibliography.json`.
- **How well checked is X?** `claims.md`, or `python3 program/tools/check.py --list`.
- **What is weakly grounded?** `python3 program/tools/validate.py --coverage`.
- **Which debates does a result touch?** `jq -c '.debates[]|select(.claims|index("K10"))|.id' program/data/debates.json`
