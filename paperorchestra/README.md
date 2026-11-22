# PaperOrchestra integration

[PaperOrchestra](https://github.com/google-research/paper-orchestra) (Google Research, Apache-2.0) is a multi-agent pipeline that turns an idea file plus an experimental log into a LaTeX paper. Its stages are outline → literature review (Semantic Scholar plus web search) → section writing → refinement → PDF. It is vendored here, unmodified, as a git submodule at `paper-orchestra/`. The pipeline reads this repository's canonical data.

Upstream calls Gemini or OpenAI APIs. **Here, by default, every LLM call goes through the Claude Code CLI (`claude -p`) instead, so inference runs on your Claude Code login (for example a Pro/Max subscription) and no API key is needed.** See [LLM backend](#llm-backend).

## Layout

| Path | What it is | Edit? |
|---|---|---|
| `paper-orchestra/` | Upstream submodule | No |
| `briefs/<paper_id>.md` | Hand-written brief: front matter selects the source document, outline sections, claims, experiments and template | By hand |
| `build_materials.py` | Builds `raw_materials/<paper_id>/` from the brief, `program/data/*.json` and the source document | — |
| `raw_materials/<paper_id>/` | `idea_sparse.md`, `idea_dense.md`, `experimental_log.md`, `figures/info.json`, `paper.json` | Generated |
| `claude_backend.py` | Replaces the Gemini call with headless Claude Code (see below) | — |
| `po_run.py` | Entry point: installs the backend, then runs `paper_writing_cli.py` | — |
| `setup.sh` | TeX Live, submodule, `.venv`, requirements, `.env` | — |
| `run.sh` | Rebuilds the materials, then runs the pipeline into `output/<paper_id>_<timestamp>/` | — |
| `.env.example` | Backend, model and key settings; copy it to `.env` (gitignored) | — |

## Usage

```
paperorchestra/setup.sh                         # once per container
claude                                          # once, if Claude Code isn't logged in: /login with your subscription
paperorchestra/run.sh symmetry-convergence      # → paperorchestra/output/symmetry-convergence_*/final_paper.pdf
```

Extra arguments after the paper ID go to `paper_writing_cli.py`. Every prompt and response is saved under `output/<run>/claude_calls/` for auditing.

## LLM backend

Upstream sends every Gemini request through one function, `utils.gemini_utils.call_gemini_with_contents`. That covers the outline, paper discovery, Introduction and Related Work synthesis, section writing, refinement, and review of the compiled PDF. `claude_backend.install()` rebinds that function in every module that imported it. The replacement runs `claude -p --output-format json` with no MCP servers, no slash commands and no saved session.

| Upstream (Gemini) | Here (Claude Code) |
|---|---|
| `gemini-3.1-pro-preview` (writer, reflection) | `PO_CLAUDE_MODEL`, default `opus` |
| `gemini-3-flash-preview` (search, parsing; hard-coded upstream) | `PO_CLAUDE_FAST_MODEL`, default `sonnet` |
| `system_instruction` | `--system-prompt-file`, which replaces Claude Code's default prompt |
| Google Search tool | `WebSearch` only. It runs on Anthropic's side, so the container's network allowlist doesn't change. `WebFetch` stays off |
| PDF and image parts | Written to a temp dir that Claude reads with `Read`. PDFs also get their extracted text inlined |
| `temperature` | Ignored, because Claude Code has no sampling controls |
| Image generation (plotting agent only) | Not supported; keep plotting off |

Other settings: `PO_CLAUDE_EFFORT`, `PO_CLAUDE_CONCURRENCY` (default 3, since the literature agent fans out up to 10 searches), `PO_CLAUDE_TIMEOUT`. `CLAUDE_CODE_MAX_OUTPUT_TOKENS` defaults to 64000 because the section writer emits the whole paper in one response.

**Usage.** A full run is roughly 60–100 model calls, including about 40–60 web searches, plus several long-output calls. It counts against your plan's usage limits like any other Claude Code work.

**Fallback.** To use the upstream APIs instead, set `PO_BACKEND=gemini` and the keys in `.env`.

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

- **Network.** With the Claude Code backend, the pipeline contacts only Claude Code's own inference endpoint and `api.semanticscholar.org` (added to the Default environment's allowed hosts). The `gemini` backend also needs `generativelanguage.googleapis.com`, which is reachable here; the OpenAI API is not allowed.
- **Inside a Claude Code session.** `claude_backend` unsets `CLAUDECODE` so that the nested `claude -p` can start. In a cloud session it uses that session's credentials.
- **Rate limits.** Without a Semantic Scholar key, searches hit HTTP 429.
- **LaTeX.** `setup.sh` installs TeX Live. The ICLR template compiles cleanly.
