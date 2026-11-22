# Handoff: token-efficient tooling for the md and JSON files

*Last updated 2026-11-22. Branch: `claude/ecstatic-albattani-urj2dx`. Status: explored and reviewed. No tool code exists yet.*

Read this before you build a helper for reading or editing `program/data/*.json` or the Markdown docs. It records what agents actually spend tokens on in this repo, a proposal that failed review, and the smaller plan that replaced it.

## Goal

Agents read and edit the md and JSON files here constantly. The goal is a CLI that cuts the tokens those interactions cost, without corrupting data or file layout, and that agents actually use.

## What the evidence shows

The evidence is the transcript of one prior session, "Language and world models", from 2026-11-21 17:03Z to 2026-11-22 07:35Z. That session built `program/`. About 93 of its tool calls touched md or JSON. Two short stretches are missing from the transcript, 07:14Z to 07:22Z and 19:38Z to 20:46Z.

The summaries are in [`evidence/`](evidence/). `recon_early.json`, `recon_mid.json`, and `recon_late.json` each cover one time window. [`evidence/parse.py`](evidence/parse.py) loads a page of `list_events` output.

The md and JSON calls cost between 665k and 752k characters in total. The range comes from how each reviewer attributed mixed calls. The cost splits as follows:

| Bucket | Share | Can a tool reduce it? |
|---|---|---|
| Whole-file `Write` | About 45% | No. 22 of the 23 Writes created new files. The only rewrite was `explorations/symmetry-platonic-program.md` (38,400 chars). |
| Large reads, 2,000 chars or more | About 247k chars | Mostly no. Only about 37k of it read `program/` md or JSON. The rest read `explorations/`, `HANDOFF.md`, vendored repos, and plugin docs. |
| Python heredoc `s.replace(old, new)` patches on md | About 45k chars | Partly. Edit sends the same delta at a similar size. |
| Ad hoc `python3 -c "json.load(...)"` lookups | About 56k chars, about 35k of it JSON | Partly. `jq` and `rg` are installed and do the same job. |
| Running `validate.py`, then `render.py` | About 2k chars per cycle | No. The scripts already print one summary line. |

Other observations:

- Agents used Bash heredocs almost everywhere. The Edit tool appeared three times, with 0 failures.
- One append to `tasks.json` used a plain `json.dump`. The dump reformatted the whole file, and a second heredoc had to restore the layout.

## The proposal that failed review

The rejected proposal was `pk`, a CLI with about 18 commands. It covered JSON `get`, `ls`, `count`, `refs`, `set`, `add`, and `task`. For Markdown it had `outline`, `sec`, `sec-set`, and `row`. It also had a `check` wrapper and a `brief` command for orientation. It claimed a 40% to 60% saving. The full text is in [`evidence/pk-proposal.md`](evidence/pk-proposal.md).

Three independent reviewers tried to break it. The main agent reran each finding below and confirmed it:

1. **The saving is about 17% to 23%, not 40% to 60%.** The proposal's own per-command estimates add up to 130k to 150k characters, and most of the spend is new-file authoring that the tool cannot change.
2. **`sec-set` costs more than Edit.** In `program/harness.md`, the median section is 1,749 characters and the largest is 9,230. A one-word change costs about 80 characters with Edit and 9,230 with `sec-set`. Measured over the real `harness.md` patches, `sec-set` cost 2 to 50 times more.
3. **Edits to generated files disappear without a warning.** `render.py` regenerates `bibliography.md`, `concept-map.md`, and `data/graph.json`. `phenomena.py` regenerates `phenomena.md`. A hand edit to `concept-map.md` is gone after the next `render.py` run.
4. **`data/graph.json` duplicates all 131 concept ids from `data/concepts.json`.** An id lookup must skip `graph.json`. The hand-edited files have 0 id collisions across 762 ids.
5. **`validate.py` does not catch bad values or a broken layout.** A `tasks.json` with `status: "bogus"`, `priority: "1"`, and a full re-dump still prints `0 errors` and exits 0. The script checks status values only for the bibliography and the phenomena. This is a gap in the repo today, with or without a new tool.
6. **`jq` already covers the JSON reads.** For example, `jq -c '.claims[]|select(.id=="K12")|{id,title,status}' program/data/claims.json` prints one line.
7. **Many ids in the md files are not headings.** In `explorations/grounded-misprision-program.md`, `T1` is a heading, `A3` is a table row (line 49), and `S26` is a bullet. Any lookup by id must also find table rows and bullets.

These results held up under review:

- A writer can preserve the JSON layout. A prototype that replaces one record changed exactly 2 diff lines per file.
- Headings are unique in every md file in `program/`, in `explorations/`, and in `HANDOFF.md`.

## File layouts a JSON writer must preserve

The data files use five layouts. A plain `json.dump` breaks every one of them.

| Files | Layout | Trailing newline |
|---|---|---|
| `bibliography`, `concepts`, `graph`, `phenomena` | `json.dumps(d, indent=1, ensure_ascii=False)` | No |
| `claims`, `debates` | Indented `meta`, then one record per line | Yes |
| `tasks`, `experiments` | One-line `meta`, then one record per line | Yes |

`phenomena.json` changes bytes unless you pass `ensure_ascii=False`. The one-record-per-line files round-trip when you rewrite only the record lines with `json.dumps(record, ensure_ascii=False)` and leave the other lines alone.

## The recommended plan

Build these in order. Each step ends with a check you can run.

1. **Make `program/tools/validate.py` stricter.**
	- Check `status` against an allowed set for tasks, claims, debates, and experiments.
	- Check that `priority` is an integer.
	- Add a check that fails when a generated file differs from what `render.py` and `phenomena.py` would write.
	- Check: the bogus `tasks.json` from finding 5 must fail, and the current tree must pass.
2. **Write a read-only `program/tools/pk.py` of about 100 lines with three commands.**
	- `pk where <id>` prints `file:line` for an id in the JSON and md files. It skips generated files and finds table rows and bullets.
	- `pk get <id> [-f fields]` finds the right file and prints the record with long fields cut short.
	- `pk outline <file.md>` prints headings and ids with their line ranges, so that you can Read just those lines.
	- Check: run each command against `K12`, `lackey2008`, `A3`, and `S26`.
3. **Add a short note to `program/AGENTS.md`.** Use Edit for md sections and for one-record-per-line JSON. Use `pk where` or `pk outline` before you read a whole md file. Never edit a generated file.

Do not build `sec-set`, `ls`, `count`, `check`, or a JSON writer unless new evidence shows a need. Edit, `jq`, and the existing scripts already do those jobs at a lower cost. The expected saving from this plan is 10% to 20% of md and JSON spend. That figure is inferred from one session.

## Open questions

- No one has tested whether agents follow an `AGENTS.md` note about which tool to use. Measure it in the next session's transcript.
- The evidence comes from one session that mostly created files. A session that maintains and edits files may show a different mix.

## How to reproduce the recon

1. Call `mcp__claude-code-remote__list_events` with session `session_015CcAscxj9XPDSVN5sBKJqX`, `kinds: ["assistant", "user"]`, and `limit: 100`. Page backward with `before_id` set to the page's `first_id`. Large pages are saved to the session's `tool-results/` folder.
2. Load each page with `evidence/parse.py`.
3. Pair each `tool_use` block with its `tool_result` block by id.
4. Bucket the pairs by tool, target path, and operation.
