# PaperOrchestra integration

[PaperOrchestra](https://github.com/google-research/paper-orchestra) (Google Research, Apache-2.0) is a multi-agent pipeline that turns an idea file plus an experimental log into a LaTeX paper. Its stages are outline → literature review (Semantic Scholar + Gemini search) → section writing → refinement → PDF. It is vendored here as a git submodule at `paper-orchestra/`, and the pipeline reads this repository's canonical data.

## Layout

| Path | What it is | Edit? |
|---|---|---|
| `paper-orchestra/` | Upstream submodule | No |
| `briefs/<paper_id>.md` | Hand-written brief: front matter selects the source document, outline sections, claims, experiments and template | By hand |
| `build_materials.py` | Builds `raw_materials/<paper_id>/` from the brief, `program/data/*.json` and the source document | — |
| `raw_materials/<paper_id>/` | `idea_sparse.md`, `idea_dense.md`, `experimental_log.md`, `figures/info.json`, `paper.json` | Generated |
| `setup.sh` | TeX Live, submodule, `.venv`, requirements, `.env` | — |
| `run.sh` | Rebuilds the materials, then runs the pipeline into `output/<paper_id>_<timestamp>/` | — |
| `.env.example` | Keys the pipeline reads; copy it to `.env` (gitignored) | — |

## Usage

```
paperorchestra/setup.sh                         # once per container
$EDITOR paperorchestra/.env                     # GEMINI_API_KEY (or Vertex / OpenAI); SEMANTIC_SCHOLAR_API_KEY
paperorchestra/run.sh symmetry-convergence      # → paperorchestra/output/symmetry-convergence_*/final_paper.pdf
```

Extra arguments after the paper ID go to `paper_writing_cli.py`, for example `--writer_model_name gpt-5`. The upstream defaults are `gemini-3.1-pro-preview` for writing and reflection.

## Papers

| ID | Source | Claims | Template |
|---|---|---|---|
| `symmetry-convergence` | Outline v1 (`explorations/symmetry-platonic-program.md`), §§1, 2, 4, 5, 6, 10 | K1, K3, K4, K5, K30 | ICLR 2025 |

To add a paper, write a new brief with the same front matter. `build_materials.py` picks it up automatically.

## Honesty rails

The program has **run no experiments**, but PaperOrchestra is built for empirical papers and will produce results tables if the log seems to allow them. To prevent that, the generated `experimental_log.md`:

- opens by saying that no experiments were run;
- lists only closed-form quantities and published, attributed findings as reportable;
- marks every X-/E- experiment as a pre-registered prediction;
- carries each claim's status and each reference's verification status.

Plotting is off (`--use_plotting false`) because there is no data to plot, and `figures/info.json` is empty.

Still, **review every generated draft** against `program/data/claims.json` before using it. In particular, check that no New or Conjecture result is presented as proved, and that no number is invented. Drafts are outputs, not sources: never feed them back into `program/data/`.

## Environment notes

- **Network.** The pipeline contacts only `generativelanguage.googleapis.com` (Gemini; reachable from this environment as of 2026-11-22) and `api.semanticscholar.org` (added to the Default environment's allowed hosts). The OpenAI API is not allowed.
- **Rate limits.** Without a Semantic Scholar key, searches hit HTTP 429.
- **LaTeX.** `setup.sh` installs TeX Live. The ICLR template compiles cleanly.
