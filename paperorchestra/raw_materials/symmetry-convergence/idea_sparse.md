# Convergence Is Not Grounding: Closed-Form Representational Alignment on Symmetric Word Families

## Problem Statement

The Platonic Representation Hypothesis (PRH; Huh, Cheung, Wang & Isola, 2024) holds that neural networks trained on different data, objectives and modalities converge toward a shared statistical model of reality. It is supported by alignment scores (CKA, mutual-kNN) that rise with scale, but it leaves two questions open in its own §6: what a given alignment score (e.g. a mutual-kNN of 0.16) actually means, and whether alignment is capped by the mutual information between the input signals. Separately, recent work shows that when word co-occurrence statistics are invariant under a group G, the geometry of a single model's embeddings is fixed by G's irreducible representations (Karkada et al., 2026; Storan, Tolias & Miolane, 2026). Neither line of work connects the single-model geometry result to multi-model convergence, and neither says when alignment between models is evidence about the world rather than about a shared corpus.

## Core Hypothesis

On word families whose statistics carry a group symmetry (months, weekdays, hues, musical chords, celestial positions), PRH-style convergence is a theorem rather than a hypothesis, and it has a closed form: the alignment between two models is a Plancherel inner product of their irrep spectra, so the alignment ceiling is computable. The same harmonic analysis shows that **convergence is not grounding**. Closed-loop (self-generated) training acts as a spectral low-pass filter; alignment metrics are dominated by the leading irrep; so collapse can *raise* cross-model alignment while *lowering* the grounded information the representations carry about the world. Alignment is evidence about reality only across training channels that are conditionally independent given the world.

## Proposed Approach (theory paper; no new experiments have been run)

1. **Setting.** A world with a symmetry group G acting on an orbit of states; an equivariant lexicalization channel; a word family in bijection with the orbit; learners whose targets are entrywise transforms (PMI, shifted PMI, the M* surrogate) followed by spectral maps (positive part, absolute value), plus a class of exchangeable deep networks.
2. **Symmetry inheritance and objective independence (S1–S3).** Invariant world statistics push forward to invariant co-occurrence statistics; every learner in the linear class shares the same isotypic decomposition; deviations split into a G-invariant part (which only rescales) and an orthogonal part (the only part that can rotate eigenvectors).
3. **Theory for deep networks (S7).** Equivariant training plus exchangeable initialization plus an invariant corpus law makes the law of every token-level representation G-invariant, addressing the limitation both anchor papers state (their theorems cover word embeddings only).
4. **Closed-form alignment and ceilings (S9–S15).** CKA between two models on a family equals the Plancherel inner product of their Fourier coefficients; disjoint corpora still align, with Davis–Kahan rates in the family-relevant token mass; bijective observations are not needed for cross-modal convergence.
5. **Convergence versus grounding (S22, S24–S27).** Grounded information decomposes by irrep; collapse removes high irreps first; a lower bound CKA ≥ sqrt((1−τ_a)(1−τ_b)) shows collapsed models align almost perfectly; a data-processing bound shows agreement implies grounding only under conditional independence of the training channels; symmetry breaking splits into a world part (keep) and an agent part (average away).
6. **A finite cyclic world testbed (§6)** in which every statement is computable, and a list of falsifiable experiments with stated predictions.

## Expected Contributions

- A closed-form answer, on symmetric families, to the PRH's question of what an alignment score means.
- The first theory of family geometry for deep networks (via exchangeability), not only word embeddings.
- A precise, falsifiable statement that alignment metrics are blind to exactly what model collapse destroys, with a recommendation for tail-sensitive, independently checked grounding measures.
- A set of pre-registered experimental predictions (not yet run).

## Honesty constraints for the writer

- This is a theory/position paper. **No experiments have been run by the authors.** Every number in the paper must be either derived in closed form from the stated theory or quoted from a cited paper with attribution.
- Results tagged New or Conjecture are proof targets or proof sketches, not established theorems; present them as Propositions with proof sketches or as Conjectures, matching the status given in the idea and log.
