# S-01 report

*2026-11-22. Task done. Charter at [`charter.md`](charter.md).*

## What was filed

- **Definitions.** K60 to K63 are P1 to P4, and K64 is the cost functor.
- **§4 results (L3).** K65 to K72.
- **§5 results (L8).** K73 to K76.
- **Linked, not refiled.** The data-processing bound is GM-T2, the verifier term is MR1, and agreement across conditionally independent channels is OUT-S26. All three are already checked.

No claim entered as `known`. The sources behind K65, K71 and K73 are from memory, so they stay `new` until S-03 checks them.

## Findings from stating the results exactly

1. **K67 claims containment, not equality.** The surviving reference gauge provably contains the stabilizer of the sensorium. Equality fails in general, because a permutation outside the stabilizer can still leave the joint law unchanged when the law has its own symmetries. S-02 check 2 should test equality on the cyclic world, where it is expected to hold.
2. **K76 says more than equal interfaces.** Two learners at optimum on one corpus law have equal interfaces by definition. That their internal representations agree up to a reparametrization is a further claim, because one fiber of $\theta\mapsto f(\theta,-)$ can hold representations that are not isomorphic. The statement now says so, and the Platonic Representation result needs this extra step.
3. **K68 makes the dihedral case exact.** With one anchor on $\mathbb Z_N$ under $D_N$, exactly one reflection survives, the one through the anchored point, for both odd and even $N$.
4. **The vagueness in K69 is now a number.** "A handful of seeds" became "at most 50 seed pairs, within 10 points of precision@1." Those thresholds are the coordinator's choice and S-03 should check them against conneau2018.
5. **A symbol clash was caught.** P3's definition of a grounded agent used $k$ for a kernel, and §4.3 uses $k$ for the number of anchors. The kernel is now $q$.

## Cuts

- `formal/schema.py` and `formal/test_schema.py` are deleted, which removes 13 test cases.
- `formal/notation.md` went from 140 rows to 41. Each kept row is a symbol that `foundations.md` or `checks/info_core.md` uses. The notation test now requires the primitives' symbols instead of the F-00 task's.

## For S-02 and S-03

- S-02 targets K66 (check 1), K68 (check 2), K70 (check 3) and K71 with K72(c) (check 4). Each falsifier names its check.
- S-03 has 11 new from-memory entries: fritz2020, fong2019, capucci2021, harper2009, bradley2022, conneau2018, sogaard2018, lewis1969, frank1953, blasi2016 and rives2021. It also has the cited entries that were already from memory: firth1957, quine1960, harnad1990, bender2020, putnam1975, eigen1971 and shumailov2024.
