# S-01 charter: file the foundations as claims

*Coordinator draft, 2026-11-22. Awaiting human approval.*

## Goal

Turn `foundations.md` §2 to §5 into records the loop can check. The four primitives and the cost become `definition` claims. Each tagged result in §4 and §5 becomes a claim with explicit quantifiers and a falsifier. The pieces that §6 cuts are cut in the same commit.

## Subjects in scope

New claims take K60 onward, because no layer block has room for them. Primitives go in L0, the §4 results in L3 and the §5 results in L8.

| Id | Source | Title | Status | Difficulty |
|---|---|---|---|---|
| K60 | §3.1 | P1 World | definition | easy |
| K61 | §3.2 | P2 Language | definition | easy |
| K62 | §3.3 | P3 Agent, grounded agent, generative agent | definition | easy |
| K63 | §3.4 | P4 Selection | definition | easy |
| K64 | §2 | Cost functor | definition | easy |
| K65 | §4.1 | Firth is Yoneda | new | easy |
| K66 | §4.2 | Theorem 4.2, text fixes the world up to a gauge | new | easy |
| K67 | §4.3 | Grounding is gauge fixing | new | easy |
| K68 | §4.3 | Anchors fix a free gauge | new | easy |
| K69 | §4.3 | Anchor prediction for bilingual lexicon induction | test | open |
| K70 | §4.3 | Grounded information is gauge-invariant | new | easy |
| K71 | §4.4 | Conventions are spontaneous symmetry breaking | new | medium |
| K72 | §4.4 | Arbitrary form is symmetric across languages; the residue is explicit breaking | test | open |
| K73 | §5.1 | A text-only learner's world model is a function of $D$ | new | medium |
| K74 | §5.2 | A generative agent's reference comes from its readers | conjecture | medium |
| K75 | §5.3 | Error threshold for recursive training | conjecture | hard |
| K76 | §5.4 | Convergence of text-only learners is up to the representation gauge | new | medium |

Three tagged items in §5 already exist and are linked, not refiled: the data-processing bound (GM-T2), the verifier term (MR1) and agreement across conditionally independent channels (OUT-S26).

The status rules:

- **No claim enters as `known`.** §4.1, §4.4 and §5.1 rest on known mathematics, but every source for them is from memory, and §8 says no claim built on them leaves `new` until S-03 checks the source. The guard hook also admits a new claim only as `new`, `conjecture`, `test` or `definition`.
- **Evidence keys missing from the bibliography are added as `from-memory` entries.** These are fritz2020, fong2019, capucci2021, harper2009, bradley2022, conneau2018, sogaard2018, lewis1969, frank1953, blasi2016 and rives2021. The validator rejects evidence keys it can't resolve, and S-03 then checks these entries. §8 sources that no claim cites stay out.

## Cuts

- Delete `formal/schema.py` and `formal/test_schema.py`.
- Cut `formal/notation.md` to the symbols that `foundations.md` and the checked results use. A script decides which rows survive. The notation test's required list changes from the F-00 task's symbols to those in `foundations.md`.
- `formal/primitives.md` maps P1 to P4 to K60 to K63.

## Acceptance criterion

- Every row above is in `claims.json` with its status. Each non-definition claim has a falsifier.
- `python3 -m pytest program/formal program/experiments/cyclic_world` passes.
- `python3 program/tools/render.py` and then `python3 program/tools/validate.py` report 0 errors.

No V-tier target. S-02 writes the checks.

## Out of scope

- Checks of any kind, which belong to S-02.
- Verifying sources, which belongs to S-03.
- §9's open problems, and any structure on $V^*$ beyond concatenation.
- Spine L4 to L8 claims. Their tasks wait on S-02.
