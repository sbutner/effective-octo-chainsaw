# S-02 charter: check the gauge results on the cyclic world

*Coordinator draft, 2026-11-22. Approved by the human 2026-11-22.*

## Goal

Run `foundations.md` §7 checks 1 to 4 on the cyclic world, so the §4 gauge results either reach V3 or are refuted. S-02 is on the critical path: Q-05, Q-06, Q-07, Q-10 to Q-13, Q-16, Q-17 and Q-19 wait on it.

## Subjects in scope

| Id | Check | What the check must show |
|---|---|---|
| K66 | 1 | A `witness`: two worlds in one $\mathbb Z_N$ orbit whose corpus laws are identical, so text fixes geometry but not reference. |
| K67 | 1, 2 | Containment of the stabilizer in the surviving gauge, plus a test of equality on the cyclic world. Equality is expected to fail when the world's law has extra symmetry. If it does, that is recorded as a finding, not a refutation of containment. |
| K68 | 2 | One anchor fixes the rotation under $\mathbb Z_N$. Under $D_N$ one anchor leaves a reflection. |
| K70 | 3 | `grounded_information` is unchanged under the joint action. This extends `test_info_equivariant_under_shift` to reflections. |
| K71 | 4 | A naming-game simulation under the $S$ symmetry. Each run breaks the symmetry. The ensemble over seeds is symmetric within a tolerance stated before the run. |
| K72 | 4 | The simulation half only. One cheaper form shifts the ensemble in the predicted direction. |

## Acceptance

Every subject in scope reaches V3 or is refuted by an exact witness. K71 and K72 are simulations, so their tolerance and seed count are fixed in `checks/gauge.md` before the first run.

## Out of scope

- K69 (bilingual anchors) and the cross-language half of K72. These are empirical and need sources, which S-03 covers.
- Check 5 (replicator is Bayes). It needs the `finite_identity` runner, which does not exist yet.
- K65 and K73 to K76. No §7 check covers them.

## Outputs

`program/checks/gauge.py`, `program/checks/gauge.md`, a naming game in `program/experiments/cyclic_world/`, and ledger verdicts from `check.py`.
