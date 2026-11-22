# Information-theoretic core: hand proofs and findings

*Checks: [`info_core.py`](info_core.py). Verdicts: `program/ledger/`, summarized in [`claims.md`](../claims.md). First run 2026-11-22 as the PSITIP pilot; rerun the same day through `tools/check.py`, which reproduced every row.*

The ledger holds what a machine decided. This file holds what a person should read alongside it: a hand proof for each `provable` row, so a reviewer can check the LP verdict, and what the verdicts mean for the claim registry.

Rows are named by check id.

## Hand proofs

Each proof is short, and a reviewer should check it against the LP verdict.

- **GM-T2/main.** W₁ is a function of (W₀, ξ), so I(W;W₁) ≤ I(W;W₀,ξ) = I(W;W₀) + I(W;ξ|W₀) = I(W;W₀).
- **GM-T4.2~cond-D/joint.** By the chain rule, I(W;D,C) = I(W;D) + I(W;C|D). Since C is a function of (D, ξ), I(W;C|D) ≤ I(W;ξ|D), and that term is 0 by hypothesis.
- **GM-T4.2~cond-D/replacement.** I(W;C) ≤ I(W;D,C), which equals I(W;D) by the joint row.
- **GM-T4.2~indep-WD/joint.** By weak union, ξ ⊥ (W, D) implies ξ ⊥ W | D. Then apply the joint row.
- **OUT-S26/first-link, second-link.** Data processing along Xa – Da – W – Db – Xb: I(Xa;Xb) ≤ I(Da;Xb) ≤ I(Da;Db) ≤ I(Da;W).
- **MR1/main.** I(W;T) ≤ I(W;D,E) = I(W;D) + I(W;E|D).

## Findings for the claim registry

These are proposals. Under `AGENTS.md`, status changes go through review.

1. **GM T4.2 as written is false.** The correction ξ ⊥ Ω | D, or the stronger ξ ⊥ (Ω, D), is necessary and sufficient for the stated equality and for the replacement clause. The "strictly under finite sampling" clause is not a Shannon-type statement, and this pilot does not check it.
2. **GM T4.1's inequality is trivial.** It holds with no hypotheses, by the chain rule. Its content lies entirely in the strictness clause and the "gains shrink with overlap" clause, which need distributional conditions and are not checked here. Restate T4.1 so the independence hypothesis is attached to those clauses.
3. **MR1 holds under the Markov condition Ω – (D, E) – (Θ, Y), and the verifier term is necessary.** The `condition` field in `claims.json` MR1 says "ξ independent of Omega given D". That is the T4.2 condition, not the condition MR1 itself needs. Reconcile them.
4. **S26 depends on conditional independence of the two channels.** Without it, the counterexample is exactly shared training data. This supports the outline's reading of S26.

**Not checked:** rates, strictness, anything involving finite-sample estimation, and the harmonic-analysis results (S4, S10, S25). Those need exact computation over ℤ_N, not an information-inequality prover.
