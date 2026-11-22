# PSITIP pilot: results

*Run 2026-11-22 with PSITIP at `cheuktingli/psitip@2025-06-10` and the OR-Tools GLOP solver. The script is [`pilot.py`](pilot.py).*

PSITIP decides whether a linear information inequality follows from the given constraints by the Shannon-type LP method (Yeung–Zhang).

- `True` means a Shannon-type proof exists. This is **sound**.
- `False` means only that no Shannon-type proof exists. It does **not** mean the inequality is false, because non-Shannon inequalities exist. A refutation needs a counterexample distribution, and each one below was computed or given explicitly.

Variables: `W` = Ω (the world); `D` = corpus; `C` = commentary or retelling; `ξ` = noise; `E` = verifier or independent evidence; `T` = model output (Θ, Y); `Da, Db, Xa, Xb` = two agents' data and representations.

| # | Claim | Hypotheses | Conclusion | PSITIP | Verdict |
|---|---|---|---|---|---|
| 0 | Sanity check | none | I(W;D) ≤ 0 | False | Correctly rejected |
| 1 | GM T2 | W₁ = F(W₀, ξ); ξ ⊥ W \| W₀ | I(W;W₁) ≤ I(W;W₀) | True | **Proved** |
| 2 | GM T4.1 | C = f(D, E); E ⊥ D \| W | I(W;D,C) ≥ I(W;D) | True | **Proved**, but see 2a |
| 2a | Hypothesis ablation for T4.1 | **none** | same | True | **The hypothesis is unused** |
| 3 | GM T4.2 as written | C = f(D, ξ); ξ ⊥ W | I(W;D,C) ≤ I(W;D) | False | **Refuted** by the XOR counterexample |
| 4 | GM T4.2, corrected | C = f(D, ξ); ξ ⊥ W \| D | I(W;D,C) ≤ I(W;D) | True | **Proved** |
| 5 | GM T4.2, replacement clause | same as 4 | I(W;C) ≤ I(W;D) | True | **Proved** |
| 6 | GM T4.2, "fully independent noise" | C = f(D, ξ); ξ ⊥ (W, D) | I(W;D,C) ≤ I(W;D) | True | **Proved**: this reading also suffices |
| 7 | OUT-S26, first link | Da ⊥ Db \| W; Xa ⊥ (W, Db, Xb) \| Da; Xb ⊥ (W, Da) \| Db | I(Xa;Xb) ≤ I(Da;Db) | True | **Proved** |
| 8 | OUT-S26, second link | same as 7 | I(Da;Db) ≤ I(W;Da) | True | **Proved** (Db symmetric) |
| 9 | S26 ablation | 7 without Da ⊥ Db \| W | I(Xa;Xb) ≤ I(W;Da) | False | **The hypothesis is load-bearing**: counterexample below |
| 10 | MR1, Unified Channel Law | W ⊥ T \| (D, E) | I(W;T) ≤ I(W;D) + I(W;E\|D) | True | **Proved** |
| 11 | MR1 ablation | same as 10 | I(W;T) ≤ I(W;D) | False | **The verifier term is load-bearing**: counterexample below |

## Counterexamples

- **Row 3.** W and D are independent fair bits, ξ = W ⊕ D and C = D ⊕ ξ = W. Computed in `pilot.py` without PSITIP: I(ξ;W) = 0 and I(W;D) = 0, but I(W;D,C) = 1 bit. This confirms HANDOFF §4 correction 1.
- **Row 9.** Da = Db = Xa = Xb = B, where B is a fair bit independent of W. Then I(Xa;Xb) = 1 > 0 = I(W;Da). This is the "shared web text" case in S26: agreement with no grounding.
- **Row 11.** D is constant and T = E = W. Then I(W;T) = H(W) > 0 = I(W;D).

## Hand proofs

Each proof is short, and a reviewer should check it against the LP verdict.

- **Row 1.** W₁ is a function of (W₀, ξ), so I(W;W₁) ≤ I(W;W₀,ξ) = I(W;W₀) + I(W;ξ|W₀) = I(W;W₀).
- **Row 4.** By the chain rule, I(W;D,C) = I(W;D) + I(W;C|D). Since C is a function of (D, ξ), I(W;C|D) ≤ I(W;ξ|D), and that term is 0 by hypothesis.
- **Row 5.** I(W;C) ≤ I(W;D,C), which equals I(W;D) by row 4.
- **Row 6.** By weak union, ξ ⊥ (W, D) implies ξ ⊥ W | D. Then apply row 4.
- **Rows 7–8.** Data processing along Xa – Da – W – Db – Xb: I(Xa;Xb) ≤ I(Da;Xb) ≤ I(Da;Db) ≤ I(Da;W).
- **Row 10.** I(W;T) ≤ I(W;D,E) = I(W;D) + I(W;E|D).

## Findings for the claim registry

These are proposals. Under `AGENTS.md`, status changes go through review.

1. **GM T4.2 as written is false.** The correction ξ ⊥ Ω | D, or the stronger ξ ⊥ (Ω, D), is necessary and sufficient for the stated equality and for the replacement clause. The "strictly under finite sampling" clause is not a Shannon-type statement, and this pilot does not check it.
2. **GM T4.1's inequality is trivial.** It holds with no hypotheses, by the chain rule. Its content lies entirely in the strictness clause and the "gains shrink with overlap" clause, which need distributional conditions and are not checked here. Restate T4.1 so the independence hypothesis is attached to those clauses.
3. **MR1 holds under the Markov condition Ω – (D, E) – (Θ, Y), and the verifier term is necessary.** The `condition` field in `claims.json` MR1 says "ξ independent of Omega given D". That is the T4.2 condition, not the condition MR1 itself needs. Reconcile them.
4. **S26 depends on conditional independence of the two channels.** Without it, the counterexample is exactly shared training data. This supports the outline's reading of S26.

**Not checked:** rates, strictness, anything involving finite-sample estimation, and the harmonic-analysis results (S4, S10, S25). Those need exact computation over ℤ_N, not an information-inequality prover.
