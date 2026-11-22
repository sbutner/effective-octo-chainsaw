#!/usr/bin/env python3
"""Build PaperOrchestra raw materials from this repository.

PaperOrchestra expects, per paper:
    raw_materials/
        idea_sparse.md        short problem / hypothesis / approach brief
        idea_dense.md         brief + full technical content
        experimental_log.md   what was (and was not) measured
        figures/info.json     list of {"name", "caption"} for provided figures

This script generates those files from a hand-written brief in
paperorchestra/briefs/<paper_id>.md plus the canonical program data
(program/data/*.json) and the source exploration document named in the
brief's front matter. Re-run it whenever the program data changes.

Usage:
    python3 paperorchestra/build_materials.py                 # all briefs
    python3 paperorchestra/build_materials.py symmetry-convergence
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / "paperorchestra"
DATA = ROOT / "program" / "data"
OUT = HERE / "raw_materials"

STATUS_NOTE = {
    "known": "published result, re-applied (cite it)",
    "implicit": "follows from published results with little work",
    "new": "new theorem target; at most a proof sketch exists",
    "conjecture": "plausible but unproven; may be false",
    "test": "empirical prediction; experiment not yet run",
    "definition": "modeling choice",
}


def load(name):
    return json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))


def parse_brief(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        sys.exit(f"{path}: missing front matter")
    meta = {}
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        key, _, val = line.partition(":")
        val = val.strip()
        if val.startswith("["):
            val = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
        else:
            val = val.strip("'\"")
        meta[key.strip()] = val
    return meta, m.group(2).strip()


def extract_sections(md, numbers):
    """Return the '## <n>.' sections of a markdown document, in order."""
    parts = re.split(r"(?m)^(?=## )", md)
    keep = []
    for part in parts:
        m = re.match(r"## (\d+)\.", part)
        if m and int(m.group(1)) in {int(n) for n in numbers}:
            keep.append(part.rstrip().rstrip("-").rstrip())
    return "\n\n".join(keep)


def claim_block(c):
    lines = [
        f"### {c['id']}: {c['title']}",
        f"- **Status:** {c['status']} ({STATUS_NOTE.get(c['status'], '')}); difficulty: {c.get('difficulty', 'n/a')}",
        f"- **Statement:** {c['statement']}",
    ]
    if c.get("links"):
        lines.append(f"- **Corresponds to:** {', '.join(c['links'])}")
    if c.get("proof_route"):
        lines.append("- **Proof route:** " + "; ".join(c["proof_route"]))
    if c.get("falsifier"):
        lines.append(f"- **Falsifier:** {c['falsifier']}")
    return "\n".join(lines)


def bib_line(b):
    return (
        f"- `{b['key']}` [{b['status']}]: {b['authors']} ({b['year']}). "
        f"*{b['title']}*. {b.get('venue', '')}"
    )


def build(brief_path):
    meta, brief = parse_brief(brief_path)
    pid = meta["paper_id"]
    claims = {c["id"]: c for c in load("claims")["claims"]}
    exps = {e["id"]: e for e in load("experiments")["experiments"]}
    bib = {b["key"]: b for b in load("bibliography")["entries"]}

    sel_claims = [claims[i] for i in meta.get("claim_ids", [])]
    sel_exps = [exps[i] for i in meta.get("experiment_ids", [])]
    bib_keys = []
    for c in sel_claims:
        bib_keys += c.get("evidence", [])
    # Always include the papers the source document was verified against.
    bib_keys = ["huh2024", "karkada2026", "storan2026"] + bib_keys
    bib_keys = [k for k in dict.fromkeys(bib_keys) if k in bib]

    source_md = (ROOT / meta["source_document"]).read_text(encoding="utf-8")
    technical = extract_sections(source_md, meta.get("outline_sections", []))
    # Drop the source's own experiment table from the idea: experiments live in the log.
    technical_no_exp = re.sub(r"(?ms)^## 7\. Experiments.*?(?=^## |\Z)", "", technical)

    d = OUT / pid
    (d / "figures").mkdir(parents=True, exist_ok=True)

    header = f"# {meta.get('title_working', pid)}\n\n"
    (d / "idea_sparse.md").write_text(header + brief + "\n", encoding="utf-8")

    dense = [
        header + brief,
        "---\n\n# Technical content (from the project's verified outline)\n",
        "Labels S1–S31 are result IDs, O1–O7 open problems, GM-* items from the parent "
        "Grounded Misprision program. Each result carries a status tag: Known (published), "
        "Implicit, New (target theorem), Conjecture, or Test. Preserve these tags in the paper.\n",
        technical_no_exp,
        "---\n\n# Spine claims this paper addresses\n",
        "\n\n".join(claim_block(c) for c in sel_claims),
    ]
    (d / "idea_dense.md").write_text("\n\n".join(dense) + "\n", encoding="utf-8")

    # Experimental log: honest record of evidence, with nothing invented.
    exp_section = extract_sections(source_md, [7])
    log = [
        "# Experimental Log",
        "## 0. Summary of evidence status (read first)",
        "- **The authors have run no experiments for this paper.** There are no new datasets, "
        "training runs, baselines, metrics or numerical results of our own.",
        "- The paper is theoretical. Its evidence is (a) closed-form derivations stated in the idea, "
        "and (b) empirical findings already published in the cited anchor papers, reported below with attribution.",
        "- Do **not** produce results tables, ablations or plots of our own measurements. Any figure must be "
        "a conceptual diagram or a plot of a closed-form function defined in the idea "
        "(e.g. the seasonal coarse-graining gains in S18 or the CKA lower bound in S25).",
        "- Experiments listed in §3 are **pre-registered predictions** to be presented as future work / "
        "falsification tests, never as results.",
        "",
        "## 1. Closed-form quantities that may be reported",
        "- S18: coarse-graining months to seasons multiplies harmonic k by |sin(pi k/4) / (3 sin(pi k/12))|; "
        "for k = 1..5 the gains are 0.91, 0.67, 0.33, 0, 0.24.",
        "- S4: with southern-hemisphere corpus share s, the k-th Fourier coefficient of every seasonal "
        "profile is multiplied by 1 - s + s(-1)^k; at s = 1/2 the odd harmonics vanish exactly.",
        "- S25: for scalar nonnegative spectra with a shared leading irrep, CKA(a,b) >= sqrt((1 - tau_a)(1 - tau_b)), "
        "where tau is the spectral mass outside the leading irrep.",
        "- S26: if D_a and D_b are conditionally independent given Omega, I(X_a;X_b) <= I(D_a;D_b) <= "
        "min{I(Omega;D_a), I(Omega;D_b)}.",
        "",
        "## 2. Published empirical findings this paper builds on (prior work, not ours)",
        "These were checked against the full texts of the cited papers. Attribute every number.",
        "",
        extract_sections(source_md, [2]).replace("## 2. The anchor results, verified", "").strip(),
        "",
        "## 3. Pre-registered experiments (NOT run; predictions only)",
        exp_section.replace("## 7. Experiments", "").strip(),
        "",
        "### Related program experiments (NOT run)",
    ]
    for e in sel_exps:
        log.append(
            f"- **{e['id']}: {e['title']}.** Design: {e['design']} Prediction: {e['prediction']} "
            f"Cost: {e.get('cost', 'n/a')}. Tests claims {', '.join(e['tests'])}."
        )
    log += [
        "",
        "## 4. Claim status (do not overstate)",
        "| Claim | Status | Meaning |",
        "|---|---|---|",
    ]
    for c in sel_claims:
        log.append(f"| {c['id']} {c['title']} | {c['status']} | {STATUS_NOTE.get(c['status'], '')} |")
    log += [
        "",
        "## 5. Reference verification status",
        "`checked` = verified against a primary index page; `from-memory` = not yet verified, "
        "so confirm via literature search before citing details.",
        "",
        *[bib_line(bib[k]) for k in bib_keys],
        "",
    ]
    (d / "experimental_log.md").write_text("\n".join(log), encoding="utf-8")
    (d / "figures" / "info.json").write_text("[]\n", encoding="utf-8")
    (d / "paper.json").write_text(
        json.dumps({k: meta[k] for k in meta}, indent=2) + "\n", encoding="utf-8"
    )
    print(f"built {d.relative_to(ROOT)}: "
          f"{len(sel_claims)} claims, {len(sel_exps)} experiments, {len(bib_keys)} references")


def main():
    names = sys.argv[1:]
    briefs = sorted((HERE / "briefs").glob("*.md"))
    if names:
        briefs = [HERE / "briefs" / f"{n}.md" for n in names]
    for b in briefs:
        build(b)


if __name__ == "__main__":
    main()
