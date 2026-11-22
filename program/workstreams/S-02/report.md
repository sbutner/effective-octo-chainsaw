# S-02 report: gauge checks on the cyclic world

*Workstream agent's findings, saved by the coordinator after the merge, 2026-11-22.*

## Result

All 31 checks in `checks/gauge.py` are `ok` and none missed. `check.py --verify` on the merged tree reproduces all 31. Two strengthened statements are refuted by exact witness: `K66~reference-identifiable` and `K67~equality`. Evidence and hand proofs are in `checks/gauge.md`. Dead ends are in `failures.md`.

The task is `blocked`. The charter asked for V3, and `check.py` derives only V0, V4 and R, because V3 needs a calibrated review that does not exist yet (`harness.md` §4). The bare claims K66 to K72 also stay V0, because their dependencies K60 to K64 are definitions with no checks.

## Tiers by subject

| Claim | Subject | Tier |
|---|---|---|
| K66 | `K66.cyclic-world`, `K66.geometry` | V4 on finite instances |
| K66 | `K66~reference-identifiable` | R |
| K67 | `K67.containment` | V4 on finite instances |
| K67 | `K67~equality` | R |
| K68 | `K68.cyclic-world` | V4 on finite instances |
| K70 | `K70.cyclic-world` | V4 on finite instances |
| K71 | `K71.small-population` (exact 3-agent, 3-form chain) | V4; the ensemble simulation is a probe |
| K72 | `K72.c` (exact direction) | V4; the simulation is a probe |

"V4 on finite instances" means every `proves` check passed on the stated instances. The general statements rest on the unreviewed hand proofs in `gauge.md` Part D.

## Findings

1. **K67 equality fails when the world has extra symmetry.** With `N = 12` and the half-speaking profile (period 6), the shift by 6 maps the world to itself. It lies outside `Stab(σ)` and leaves the joint law unchanged. K67 claims containment, so it stands. In the four cases computed, the surviving gauge is `Stab(σ) · Fix(P, K)`. That holds only in those cases and is a conjecture beyond them.
2. **K68 needs a qualifier.** In the hemisphere-blind world, the shift by 6 survives one anchor. Foundations §4.3 and §7 check 2 should say "up to the symmetry of the corpus-world pair". A reflection survives one anchor in `D_N` for every `N` from 3 to 16. Two anchors leave a reflection exactly when they are antipodal and `N` is even.
3. **Text geometry is fixed up to `D_N`, not `Z_N`, even for a chiral speaker.** The two words of a pair are exchangeable, so pair statistics cannot see a reflection.
4. **K70 holds exactly** under all of `D_12` and `Sym(5)`.
5. **Naming game.** The setup was 20 agents, 5 forms, 2000 seeds and 50000 interactions. The tolerance of 0.036 was committed before the first run (`35b9b3c`).
   - With symmetric costs, the largest deviation from 1/5 was 0.0105.
   - The cheaper form's share was 0.7475 at `r = 2` and 0.925 at `r = 3`.
   - The tolerance comes from sampling error, so a bias below about 0.03 would go undetected.
6. **Tooling hazards.**
   - `witness.verdict` returns `no-counterexample` when a precondition fails, so an `expect: no-counterexample` witness can pass without testing anything. `gauge.py` guards against this, but other modules don't.
   - `check.py` hashes only the check module. `gauge.py` pins the simulation sources by SHA-256.

## Proposed status changes (none applied)

- **K66, K68, K70:** candidates for `known` once the hand proofs are reviewed and the tier rules allow it.
- **K67:** unchanged. Optionally, file `Stab(σ) · Fix(P, K)` as a new `conjecture`.
- **K71 and K72:** unchanged. K72 parts (a) and (b), and its cross-language half, belong to S-03.

## Informal residue

- The general-`N` hand proofs for K66, K67 containment, K68 and K70.
- K71 (a) and (b) for every population size. Only the 3-agent chain is checked.
- K71 (c) as a linearization at the symmetric state.
