# Primitive ledger

*Opened by F-00, 2026-11-22. The budget: each rung adds at most one primitive. A rung that needs two stops the ladder for a redesign (`formalization.md`, "What changes", item 4).*

## The four proposed primitives

| # | Primitive | Formal type | Added by | Instantiated in the testbed | Status |
|---|---|---|---|---|---|
| 1 | World process $\omega_t$ | Stateful stochastic process on $\Omega$, with a symmetry group $G$ acting on it. $\Omega$ consists of interactions. Agents' internal models are hidden and are not part of $\Omega$. | R0 (inherited from spine L0) | `experiments/cyclic_world`: $\Omega=\mathbb Z_N\times$ seasons, $G=\mathbb Z_N$ | Proposed |
| 2 | Channel | Markov kernel $K:X\to\Delta(Y)$ with a single cost $c$ per use | R0 (inherited from spine L0, cost new) | `Channel` in `experiments/cyclic_world` | Proposed |
| 3 | Agent | A bounded-capacity predictor fitted online to its own joint stream of episodes | R1 | R0 holds only the stream; the predictor is F-01's | Proposed |
| 4 | Goal | A preference over world states. A signal is scored by the change in $\omega$ it brings about through the receiver's action. | R2 | Not yet | Proposed |

A primitive moves from **Proposed** to **Used** when a rung's toy run depends on it, and to **Load-bearing** when a check shows a target behavior fails without it.

## Per rung

Each rung fills its row when it closes. "Extra term" records anything the toy run needed beyond the primitives listed, such as a processing-speed parameter or an information term in the payoff. A non-empty extra term on a rung that also adds a primitive breaks the budget.

| Rung | Task | Adds | Extra term needed | Closed |
|---|---|---|---|---|
| R0 Groundwork | F-00 | none (1 and 2 inherited) | | |
| R1 Grounded agent | F-01 | 3 Agent | | |
| R2 Communication game | F-02 | 4 Goal | | |
| R3 Sentence and composition | F-03 | none | | |
| R4 Divergence and alignment | F-04 | none | | |
| R5 Narrative | F-05 | none | | |
| R6 Writing | F-06 | none, if writing is a channel parameter change | | |
| R7 Genre and corpus | F-07 | none | | |

## Candidate extra terms already named in the plan

These come from `formalization.md`, "Open questions". None is admitted yet.

| Candidate | Rung that tests it | Where it would go |
|---|---|---|
| Timescale parameter for nouns of things that change ("river") | R3 | Noun as a slowly varying state |
| Processing-speed parameter for the 200 ms turn gap | R2 | The channel cost $c$ |
| Separate information or relationship term in the payoff | R2, R4 | The goal primitive's score |
| Computable afferent cost | R3 | Entropy rate of the sensorium $\sigma_a$ over the episode |
