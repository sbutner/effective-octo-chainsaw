# Formalization plan: from grounded speakers to corpora

*v0.1 · 2026-11-22 · Status: plan, not started. Execution waits on the human's go.*

## Goal

Derive the behaviors that the grounding literature observes and argues about most, from as few primitives as possible. Ground citations lazily. Work from memory and `data/bibliography.json`, and check a source only when a behavior's statement depends on it.

## What changes

1. Formalization moves ahead of everything else. GROUND, PROVE, EXTEND and CONNECT tasks wait, except the info_core write-back and the blind menu build.
2. The spine gets a new foundation, built bottom up in eight rungs. The current L0 agent tuple $(b_a,S_a,\kappa_a)$ is replaced by a grounded learner defined from its own experience stream. L3 (the distributional layer) and L4 (archives) are rederived on top of it, not kept beside it.
3. There is no universal language model. Each agent has its own model and its own embedding geometry. Convergence across agents or models, the Platonic Representation Hypothesis (P-062), becomes a theorem with conditions, not an assumption.
4. A primitive budget is tracked. Each rung may add at most one primitive. A rung that needs two means the earlier rungs are wrong, and the plan stops for a redesign.

## The primitives, as proposed

| # | Primitive | Formal type | Already in the spine |
|---|---|---|---|
| 1 | World process $\omega_t$ | Stateful stochastic process on $\Omega$, with a symmetry group $G$ acting on it | L0 |
| 2 | Channel | Markov kernel with a time cost and an energy cost per use | L0, without the costs |
| 3 | Agent | A bounded-capacity predictor fitted online to its own joint stream of episodes | Replaces the L0 tuple |
| 4 | Payoff | What a channel use is tested against: the world, or the state of the relationship between agents | GM selection, generalized |

Everything below is meant to be derived from these four. Rows in the rung table say which primitive, if any, each rung adds.

## Data shape: the multi-typed graph

This graph is an object inside the formalism. It is distinct from `data/concepts.json`, which maps the program's ideas.

**Episode.** $e_t=(x_t,\ k_t,\ m_t,\ u_t)$. Here $x_t$ is the sensory input, $k_t=\kappa_a(x_t)$ is the agent's automatic classification of that input, $m_t$ is the internal state (mood, prediction, prediction error as salience), and $u_t$ is any co-occurring utterance, heard or spoken. An agent's experience is the sequence $E_a=(e_1,\dots,e_t)$.

**Agent model.** $M_a$ is the predictor fitted to $E_a$. Its embedding geometry $\mathsf G_a$ is the geometry its co-occurrence statistics induce over symbols and classes, for example a PMI matrix over symbols × (classes, internal states, other symbols). Two agents differ in geometry because their streams differ in three ways: what they were exposed to (corpus), what surrounds the current exchange (immediate context), and what they lived (sensory and internal history).

**Node types**, in the order the rungs add them:

| Node type | Added in | Defined as |
|---|---|---|
| agent, episode, class | R1 | Primitive 3 and its stream |
| signal | R2 | A channel use between two agents in one exchange |
| event (verb), entity (noun) | R3 | Verb: a transition the agent predicts. Noun: an invariant of a family of transitions, i.e., what persists while the verb happens. |
| sentence | R3 | A hyperedge rooted in one verb node, with labeled role edges to noun nodes (valency) |
| narrative | R5 | A sequence of sentences whose noun nodes persist across them and whose verbs are temporally or causally ordered |
| inscription | R6 | A signal with near-zero decay, detached from its sender and from the context of its production |
| genre, corpus | R7 | Genre: a shared prior over narratives and forms in a community. Corpus: a multiset of inscriptions with provenance, which is the L4 archive $\mathcal A_t$. |

**Edge types:** perceives, classifies, co-occurs-with, utters, hears, part-of, instantiates (narrative to genre), copies, reads, cites.

The noun and verb definition puts your "verbs are nouns in motion, nouns are verbs at rest" into one structure. Verbs are elements of a group or semigroup acting on states. Nouns are the orbits and invariants of that action. This reuses primitive 1's symmetry $G$, so it adds no primitive.

Writing is a parameter change on a channel: decay near zero, context removed, repair unavailable. It is a new node type on the graph but not a new primitive. R6 tests whether that holds.

## Rungs, in landing order

Each rung ends in four checks, and the next rung does not start until all four pass:

- **Definitions.** Typed definitions are added to the graph schema, and every symbol is entered in one notation table (this absorbs Q-04).
- **Toy run.** The cyclic world ($\Omega=\mathbb Z_N\times$ seasons) is instantiated with agents. The rung's target behaviors appear in it, and a code audit shows no behavior was written in.
- **Checks.** Every target that can be stated as an inequality or identity gets a `proves`, `probe` or `witness` check in `checks/<rung>.py`.
- **Review.** A blind agent that sees only the definitions back-translates them into prose, and a reviewer compares that prose with the intent.

| Rung | Content | Adds a primitive | Target behaviors (candidates, from memory; the blind menu decides) |
|---|---|---|---|
| R0 | Groundwork: graph schema, cyclic-world testbed with agents, notation table, primitive ledger. The blind menu build for the new fields runs in parallel. | — | None. Its check is that the toy world runs and the schema validates. |
| R1 | Grounded agent: the episode stream, classification by predictive utility, internal state, per-agent geometry $\mathsf G_a$ | Agent (3) | Basic-level categories (Rosch); categorical perception; cross-situational word learning (Smith and Yu); form alone does not ground meaning (P-041; harnad1990, bender2020); the vocabulary problem, where two people pick the same name under 20% of the time (Furnas 1987); geometry that mirrors the world (P-002, N-005) |
| R2 | Communication game: recursive sender-receiver reasoning in the style of Rational Speech Acts over $M_a$ and $M_b$, costs in time, a two-term payoff | Payoff (4) | Implicature, scalar and general (Grice; Goodman and Frank); Zipf's law of abbreviation and uniform information density; turn-taking gaps near 200 ms across languages, which needs the listener to predict turn ends while planning (Stivers 2009; Levinson); repair and universal "huh?" (Dingemanse); small talk as phatic communion (Malinowski); indirect speech and plausible deniability (Brown and Levinson; Pinker 2008) |
| R3 | Sentence: verbs as transitions, nouns as invariants, the sentence as a verb-rooted hyperedge | None | The noun-verb distinction in every language; noun bias in early word learning (Gentner 1982), predicted because invariants need fewer episodes than transitions; argument structure and valency |
| R4 | Speaker divergence and alignment in speech: geometry distance between agents, and alignment through joint attention, repair and entrainment | None | Lexical entrainment and conceptual pacts (Brennan and Clark); interactive alignment (Pickering and Garrod); joint attention in word learning (tomasello1999); idiolect divergence alongside convergence at scale (P-062) |
| R5 | Narrative: entity persistence and event ordering | None | Serial reproduction regresses to schemas (P-010, Bartlett); stories transmit as formulas and themes (P-020) |
| R6 | Writing: the inscription node type and the channel parameter change | None, if the hypothesis holds | Orality-to-literacy shifts (ong1982; Goody); decontextualized language (Olson); print fixity (P-021) |
| R7 | Genre and corpus, with alignment across writing: instruction in tradition, genre conventions as a replacement for shared context, commentary | None | Genre as social action (Miller 1984); speech genres (Bakhtin); interpretive communities (P-038); the hand-off to L4 and the existing canon claims (K20 to K28) |

**Order, and why.** You said the communication game comes first. R2 therefore lands before R3, and it uses atomic signals as in a Lewis signaling game. Sentence structure in R3 should then follow from the pressure to compose signals, which is a testable prediction. R1 has to come before R2 because the game needs each agent's model of the other. R1 delivers only the minimum geometry R2 needs. R4 does the full theory of speaker divergence.

**Small talk and alignment are one mechanism, as a hypothesis.** In R2, small talk is a channel use whose payoff is the relationship term: it lowers the distance between $\mathsf G_a$ and $\mathsf G_b$ while carrying little information about $\Omega$. If that holds, R4's alignment methods are the same payoff term used deliberately, and the alignment rung adds nothing. If it fails in the toy run, R4 needs its own mechanism, and the primitive ledger records the cost.

## Changes to `data/tasks.json` (applied on go)

| Task | Change | Why |
|---|---|---|
| New F-00 to F-07 | One FORMALIZE task per rung, priority 1, with `depends_on` | The rungs are the work |
| Q-04 | Merged into F-00 | The notation table is part of the rung definitions |
| Q-05, Q-06 | Kept, `depends_on` F-04 and F-07 | $\delta_{\text{latent}}$ and $N_e$ are defined from per-agent geometry. Compression progress needs reader state from R1. |
| Q-08 | Split. Q-08a, the Shannon-type core, is closed by the info_core write-back. Q-08b, the cyclic-world proofs, waits on F-00. | Q-08a is done. Q-08b needs the testbed. |
| Q-21 | Field list extended with conversation analysis, psycholinguistics, grounded cognition, orality and literacy, genre theory. Stays priority 1, in parallel with F-00. | The rungs need a target menu that was not written to fit them |
| Q-01, Q-02, Q-03, Q-09, Q-20 | Priority 4. Each rung opens a narrow citation check when a target behavior depends on a from-memory source. | Lazy grounding |
| Q-10 to Q-14, Q-15 to Q-17, Q-19 | Priority 4, `depends_on` the rung each needs | Proofs and essays come after formalization |
| Q-18 | Deleted | The pre-commit hook enforces it |
| `tasks.json` schema | Add `depends_on`. `validate.py` rejects a task ranked above a task it depends on. The research-loop picker skips tasks with unfinished dependencies. | The order becomes a check, not prose |

## Measures of success

- **Coverage.** Must-emerge behaviors from the blind menu that are produced, divided by the primitive count. `phenomena.py` already scores emergence. It gains a per-primitive column.
- **Rivals.** The same menu scored against the rivals in `phenomena.json` (Q-22), now including Rational Speech Acts and conversation-analysis-only models, so the spine's score is relative, not absolute.

## Open questions this plan does not settle

1. **The noun-as-invariant definition.** It may not survive nouns for things that change, such as "river" or "the weather". R3's toy run tests it. The fallback is a noun as a slowly varying state, which would cost a timescale parameter.
2. **The relationship term in the payoff.** It could be a primitive, or it could be derived from expected future grounded information, since an aligned partner is a better future channel. Deriving it would keep the primitive count at three. R2 tests both.
3. **The 200 ms gap.** It may need a processing-speed parameter that the four primitives do not supply. If so, the channel time cost is the place to put it.
4. **The blind menu.** It does not exist yet for these fields. Every target behavior in the rung table is a candidate from memory, written by an agent who has read the spine. The blind builder must not see this table, and coverage is measured only against what the builder produces.
