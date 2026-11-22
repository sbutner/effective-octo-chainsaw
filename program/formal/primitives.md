# Primitive ledger

*Opened by F-00, 2026-11-22. Rewritten the same day for [`foundations.md`](../foundations.md). The budget rule: a result that needs anything beyond P1 to P4 records the extra term here, and two results that each need a new term stop the work for a redesign.*

## The four primitives

| # | Primitive | Formal type | Replaces | In the testbed | Status |
|---|---|---|---|---|---|
| P1 | World | An object $\Omega$ of interactions in $\mathsf{Stoch}$, with a state $P$ and a group $G$ of automorphisms preserving $P$. Internal models are not part of $\Omega$. | Spine L0 world and symmetry | `experiments/cyclic_world`: $\Omega=\mathbb Z_N\times$ seasons, $G=\mathbb Z_N$ | Proposed |
| P2 | Language | The free monoid $V^*$ on a finite vocabulary $V$. Speaking is a kernel $\pi:\Omega\to V^*$, and reading is a kernel $r$ out of $V^*$. | Spine L0 channels for speech and reading | Not yet | Proposed |
| P3 | Agent | A parametrized kernel $(\Theta,f)$, $f:\Theta\otimes X\to Y$, with the parameter hidden ($\mathrm{Para}$) | Spine L0 agent tuple; the plan's episode | `Agent` holds only a sensorium; no parameter yet | Proposed |
| P4 | Selection | Conditioning a state on a fitness $w$, $P\mapsto wP/\langle w,P\rangle$ | GM's $\mathcal F_{\text{test}}$; the plan's goal | Not yet | Proposed |

The ambient category $\mathsf{Stoch}$ and the cost functor $c$ to $(\mathbb R_{\ge0},+)$ are setting, not primitives.

S-01 filed P1 to P4 as definition claims K60 to K63 and the cost as K64. The §4 and §5 results are K65 to K76, and each lists the primitives it depends on in `depends_on`.

A primitive moves from **Proposed** to **Used** when a checked result depends on it, and to **Load-bearing** when a probe shows the result fails without it.

## Extra terms

Each result records here anything its proof or toy run needed beyond P1 to P4.

| Result | Extra term needed | Recorded by |
|---|---|---|
| | | |

## Candidates already named

| Candidate | Where it came from | Where it would go |
|---|---|---|
| Structure on $V^*$ beyond concatenation (a grammar) | `foundations.md` §9.4 | A functor from a grammar category, if a sentence-level result needs one |
| A measure of reference, distinct from $\mathcal G$ | `foundations.md` §9.5 | A definition over the surviving gauge group |
| A timescale for nouns of things that change | `formalization.md` open question 1 | Only if a result about nouns needs it |
