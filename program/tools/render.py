#!/usr/bin/env python3
"""Render human-readable views from program/data/*.json.

Writes:
    program/bibliography.md   annotated bibliography grouped by layer
    program/concept-map.md    Mermaid diagram per layer + claim index
    program/data/graph.json   merged node-link graph (concepts, claims, bib, debates)
                              for agents that want one traversable structure

Usage: python3 program/tools/render.py
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def main():
    bib = load("bibliography.json")
    concepts = load("concepts.json")
    claims = load("claims.json")
    debates = load("debates.json")
    layers = concepts["meta"]["layers"]

    # --- bibliography.md
    by_layer = defaultdict(list)
    for e in bib["entries"]:
        by_layer[e["layers"][0] if e["layers"] else "L?"].append(e)
    out = ["# Annotated bibliography", "",
           "*Generated from `data/bibliography.json` by `tools/render.py`. Edit the JSON, not this file.*", "",
           "Status: **checked** (verified 2026-11-21) · **checked-repo** (verified in an earlier session) · "
           "*from-memory* (verify before quoting) · *unverified* (from an author draft).", ""]
    for l in sorted(by_layer):
        out += [f"## {l}. {layers.get(l, '')}", ""]
        for e in sorted(by_layer[l], key=lambda x: (x["year"], x["key"])):
            yr = f"{-e['year']} BCE" if e["year"] < 0 else str(e["year"])
            title = f"[{e['title']}]({e['url']})" if e.get("url") else e["title"]
            st = e["status"]
            st = f"**{st}**" if st.startswith("checked") else f"*{st}*"
            rel = []
            if e.get("supports"):
                rel.append("supports " + ", ".join(e["supports"]))
            if e.get("challenges"):
                rel.append("challenges " + ", ".join(e["challenges"]))
            out.append(f"- `{e['key']}` {e['authors']} ({yr}). {title}. *{e['venue']}*. [{st}]  ")
            out.append(f"  {e['annotation']}" + (f"  \n  _{'; '.join(rel)}._" if rel else ""))
        out.append("")
    (ROOT / "bibliography.md").write_text("\n".join(out), encoding="utf-8")

    # --- concept-map.md (Mermaid, one diagram per layer incl. cross-layer edges)
    node_layer = {n["id"]: n["layer"] for n in concepts["nodes"]}
    out = ["# Concept map", "",
           "*Generated from `data/concepts.json`. Each diagram shows one layer's concepts and every edge touching them.*", ""]
    for l in sorted(layers):
        ids = [n["id"] for n in concepts["nodes"] if n["layer"] == l]
        if not ids:
            continue
        es = [e for e in concepts["edges"] if e["source"] in ids or e["target"] in ids]
        out += [f"## {l}. {layers[l]}", "", "```mermaid", "graph LR"]
        def nid(x):
            return x.replace("-", "_")
        shown = set(ids) | {e["source"] for e in es} | {e["target"] for e in es}
        for x in sorted(shown):
            label = x if node_layer[x] == l else f"{x} ({node_layer[x]})"
            out.append(f'  {nid(x)}["{label}"]')
        for e in es:
            out.append(f'  {nid(e["source"])} -- {e["relation"]} --> {nid(e["target"])}')
        out += ["```", ""]
        for n in concepts["nodes"]:
            if n["layer"] == l:
                f = f" `{n['formal']}`" if n.get("formal") else ""
                out.append(f"- **{n['id']}**: {n['definition']}{f}")
        out.append("")
    out += ["## Claim index", "", "| ID | Layer | Status | Difficulty | Title |", "|---|---|---|---|---|"]
    for c in claims["claims"]:
        out.append(f"| {c['id']} | {c['layer']} | {c['status']} | {c['difficulty']} | {c['title']} |")
    (ROOT / "concept-map.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    # --- graph.json: merged node-link structure
    nodes, links = [], []
    for n in concepts["nodes"]:
        nodes.append({"id": "concept:" + n["id"], "type": "concept", **n})
    for e in concepts["edges"]:
        links.append({"source": "concept:" + e["source"], "target": "concept:" + e["target"], "relation": e["relation"]})
    for c in claims["claims"]:
        nodes.append({"id": "claim:" + c["id"], "type": "claim", "layer": c["layer"], "title": c["title"], "status": c["status"]})
        for b in c.get("evidence", []):
            links.append({"source": "bib:" + b, "target": "claim:" + c["id"], "relation": "evidence_for"})
        for d in c.get("depends_on", []):
            links.append({"source": "claim:" + c["id"], "target": "claim:" + d, "relation": "depends_on"})
        for d in c.get("links", []):
            links.append({"source": "claim:" + c["id"], "target": "external:" + d, "relation": "corresponds_to"})
    for e in bib["entries"]:
        nodes.append({"id": "bib:" + e["key"], "type": "bib", "year": e["year"], "title": e["title"], "status": e["status"], "layers": e["layers"]})
        for c in e.get("concepts", []):
            links.append({"source": "bib:" + e["key"], "target": "concept:" + c, "relation": "discusses"})
        for c in e.get("challenges", []):
            tgt = ("claim:" if not c.startswith(("GM-", "OUT-", "OSL-")) else "external:") + c
            links.append({"source": "bib:" + e["key"], "target": tgt, "relation": "challenges"})
    for d in debates["debates"]:
        nodes.append({"id": "debate:" + d["id"], "type": "debate", "field": d["field"], "question": d["question"], "verdict_strength": d["verdict_strength"]})
        for c in d.get("claims", []):
            tgt = ("claim:" if not c.startswith(("GM-", "OUT-", "OSL-")) else "external:") + c
            links.append({"source": "debate:" + d["id"], "target": tgt, "relation": "adjudicated_by"})
        for b in d.get("llm_evidence", []):
            links.append({"source": "bib:" + b, "target": "debate:" + d["id"], "relation": "evidence_in"})
    ext = {l["target"] for l in links if l["target"].startswith("external:")}
    for x in sorted(ext):
        nodes.append({"id": x, "type": "external", "ref": x.split(":", 1)[1]})
    with open(DATA / "graph.json", "w", encoding="utf-8") as f:
        json.dump({"meta": {"generated_by": "tools/render.py", "node_types": ["concept", "claim", "bib", "debate", "external"]},
                   "nodes": nodes, "links": links}, f, indent=1, ensure_ascii=False)
    print(f"wrote bibliography.md, concept-map.md, data/graph.json ({len(nodes)} nodes, {len(links)} links)")


if __name__ == "__main__":
    main()
