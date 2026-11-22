# F-00 charter: groundwork for the formalization ladder (rung R0)

*Coordinator draft, 2026-11-22. Awaiting human approval.*

## Goal

Lay the ground every later rung builds on: a typed graph schema, a runnable cyclic-world testbed with many agents, one clash-free notation table, and a ledger of primitives. R0 adds no primitive and targets no behavior. Its check is that the world runs and the schema validates.

## Subjects in scope

| Output | What it is | Owner |
|---|---|---|
| `program/formal/schema.py` | Node and edge types as one registry. Each type names its rung, its required fields and its allowed endpoints. A `Graph` that rejects ill-typed nodes and edges, a sentence invariant (exactly one root verb), and joint attention as a derived query | Coordinator |
| `program/formal/test_schema.py` | Builds one instance of every node and edge type in the plan and validates it. Builds ill-typed cases and checks they are rejected | Coordinator |
| `program/experiments/cyclic_world/` | World $\mathbb Z_N\times$ seasons with $G=\mathbb Z_N$, channels as Markov kernels with time and energy costs, a population of agents with hemisphere offsets and sensoria, episode streams, an exact $\mathcal G=I(\Omega;\cdot)$ for finite kernels. No learning: the agent model is R1's | Workstream W1 |
| `program/experiments/cyclic_world/test_*.py` | S4: the $k$-th seasonal coefficient scales by $1-s+s(-1)^k$, and odd harmonics vanish at $s=\tfrac12$ before and after the log. S18: the width-3 box gains on $\mathbb Z_{12}$ are 0.91, 0.67, 0.33, 0, 0.24. The world runs with 1, 2 and 7 agents. Equivariance of $\mathcal G$ under the shift | Workstream W1 |
| `program/formal/notation.md` | Every symbol in spine, GM, outline §4 and the plan, mapped to one meaning, its definition and its first use. Known clashes to resolve: $r$ (reading, reflexivity), $\varphi/\phi$ (fidelity, copying), $\lambda$ (GM ratio, eigenvalues), $\kappa_a$ (context, the plan's classification), $E_a$ (GM evidence, the plan's experience stream), $M_a$ (outline co-occurrence, the plan's agent model), $N$ (group size, the task's "N agents"), $G$ / $\mathcal G$ / $\mathsf G_a$, $D$ (corpus, distortion). A test parses the table and fails on a duplicate symbol | Workstream W2 |
| `program/formal/primitives.md` | The four proposed primitives with formal types, the rung that adds each, and an empty row per later rung for "extra term needed" | Coordinator |

## Acceptance criterion

All four of the task's acceptance clauses hold, each shown by a command that passes:

- `python3 -m pytest program/formal program/experiments/cyclic_world` passes;
- the notation test finds no duplicate symbol, and every symbol in the task's list appears;
- `python3 program/tools/validate.py` reports 0 errors.

No claim tier moves, so there is no V-tier target. The `proves` checks start in F-01.

## Out of scope

- Agent learning, classification, internal state and geometry (F-01).
- Signals, goals, joint attention in the toy run (F-02). The schema defines the joint-attention triangle; nothing produces one yet.
- Rewriting spine.md or the outline to the new notation. The table records renames; prose migrates rung by rung.
- New check kinds in `check.py`.

## Known issue to carry forward

The plan puts joint attention in R2 but the entity node in R3. The schema lets attends-to target a class node in R2, and an entity node from R3 on. F-02 decides whether that holds.
