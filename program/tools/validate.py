#!/usr/bin/env python3
"""Referential-integrity checks for program/data/*.json.

Usage:
    python3 program/tools/validate.py            # errors only; exit 1 on error
    python3 program/tools/validate.py --coverage # also report thin concepts/claims
"""
import json
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
EXTERNAL = [
    (re.compile(r"^GM-T([0-9]+)$"), 1, 10),
    (re.compile(r"^GM-C([0-9]+)$"), 11, 30),
    (re.compile(r"^OUT-S([0-9]+)$"), 1, 31),
    (re.compile(r"^OUT-X([0-9]+)$"), 1, 14),
    (re.compile(r"^OUT-O([0-9]+)$"), 1, 7),
    (re.compile(r"^GM-A([0-9]+)$"), 1, 14),
]
EXTERNAL_LITERALS = {"OSL-UCL"}
LAYERS = {f"L{i}" for i in range(9)}
BIB_STATUS = {"checked", "checked-repo", "from-memory", "unverified", "not-found"}


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def is_external(cid):
    if cid in EXTERNAL_LITERALS:
        return True
    for rx, lo, hi in EXTERNAL:
        m = rx.match(cid)
        if m:
            return lo <= int(m.group(1)) <= hi
    return False


def main():
    coverage = "--coverage" in sys.argv
    errors, warnings = [], []
    bib = load("bibliography.json")["entries"]
    concepts = load("concepts.json")
    claims_doc = load("claims.json")
    claims = claims_doc["claims"]
    debates = load("debates.json")["debates"]
    exps = load("experiments.json")["experiments"]
    tasks = load("tasks.json")["tasks"]
    phen_doc = load("phenomena.json")
    phen = phen_doc["phenomena"]

    def uniq(items, label):
        ids = [x["id"] if "id" in x else x["key"] for x in items]
        dup = {i for i in ids if ids.count(i) > 1}
        if dup:
            errors.append(f"duplicate {label} ids: {sorted(dup)}")
        return set(ids)

    bib_keys = uniq(bib, "bibliography")
    concept_ids = uniq(concepts["nodes"], "concept")
    claim_ids = uniq(claims, "claim")
    debate_ids = uniq(debates, "debate")
    exp_ids = uniq(exps, "experiment")
    uniq(tasks, "task")
    mr_ids = {m["id"] for m in claims_doc.get("master_relations", [])}

    def claim_ok(cid):
        return cid in claim_ids or is_external(cid) or cid in mr_ids

    for e in bib:
        k = e["key"]
        if e.get("status") not in BIB_STATUS:
            errors.append(f"bib {k}: bad status {e.get('status')}")
        for l in e.get("layers", []):
            if l not in LAYERS:
                errors.append(f"bib {k}: bad layer {l}")
        for c in e.get("concepts", []):
            if c not in concept_ids:
                errors.append(f"bib {k}: unknown concept {c}")
        for c in e.get("supports", []) + e.get("challenges", []):
            if not claim_ok(c):
                errors.append(f"bib {k}: unknown claim {c}")
        if not e.get("annotation"):
            warnings.append(f"bib {k}: no annotation")

    for n in concepts["nodes"]:
        if n["layer"] not in LAYERS:
            errors.append(f"concept {n['id']}: bad layer")
    for ed in concepts["edges"]:
        for side in ("source", "target"):
            if ed[side] not in concept_ids:
                errors.append(f"edge {ed}: unknown {side}")

    for c in claims:
        if c["layer"] not in LAYERS:
            errors.append(f"claim {c['id']}: bad layer")
        for d in c.get("depends_on", []) + c.get("links", []):
            if not claim_ok(d):
                errors.append(f"claim {c['id']}: unknown dependency/link {d}")
        for b in c.get("evidence", []):
            if b not in bib_keys:
                errors.append(f"claim {c['id']}: unknown bib key {b}")
    for m in claims_doc.get("master_relations", []):
        for c in m["claims"]:
            if not claim_ok(c):
                errors.append(f"master relation {m['id']}: unknown claim {c}")

    for d in debates:
        for b in d.get("llm_evidence", []):
            if b not in bib_keys:
                errors.append(f"debate {d['id']}: unknown bib key {b}")
        for c in d.get("claims", []):
            if not claim_ok(c):
                errors.append(f"debate {d['id']}: unknown claim {c}")

    for x in exps:
        for c in x.get("tests", []):
            if not (claim_ok(c) or c in debate_ids):
                errors.append(f"experiment {x['id']}: unknown claim {c}")
        for r in x.get("related", []):
            if not (r in bib_keys or claim_ok(r) or r in exp_ids):
                errors.append(f"experiment {x['id']}: unknown related {r}")

    # phenomena menu (emergence verifier, harness.md §5.5)
    pmeta = phen_doc["meta"]
    phen_ids = uniq(phen, "phenomenon")
    formalism_ids = {f["id"] for f in pmeta["formalisms"]}
    core = set(next(f for f in pmeta["formalisms"] if f["id"] == "spine-v0.1")["core_premises"])
    for p in phen:
        pid = p["id"]
        for k, legend in (("kind", "kind_legend"), ):
            if p[k] not in pmeta[legend]:
                errors.append(f"phenomenon {pid}: bad {k} {p[k]}")
        if p["field"] not in pmeta["fields"]:
            errors.append(f"phenomenon {pid}: bad field {p['field']}")
        for l in p["layers"]:
            if l not in LAYERS:
                errors.append(f"phenomenon {pid}: bad layer {l}")
        g = p["grounding"]
        if g["strength"] not in pmeta["strength_legend"] or g["pattern"] not in pmeta["pattern_legend"]:
            errors.append(f"phenomenon {pid}: bad strength/pattern")
        for b in g["theorized"] + g["observed"]:
            if b not in bib_keys:
                errors.append(f"phenomenon {pid}: unknown bib key {b}")
        if not (g["theorized"] or g["observed"] or g["source_hints"]) and p["kind"] != "non-phenomenon":
            errors.append(f"phenomenon {pid}: no grounding source")
        if p.get("contrast_with") and p["contrast_with"] not in phen_ids:
            errors.append(f"phenomenon {pid}: unknown contrast {p['contrast_with']}")
        for d in p.get("debates", []):
            if d not in debate_ids:
                errors.append(f"phenomenon {pid}: unknown debate {d}")
        for a in p["assessments"]:
            v = a["verdict"]
            if a["formalism"] not in formalism_ids:
                errors.append(f"phenomenon {pid}: unknown formalism {a['formalism']}")
            if v not in pmeta["verdict_legend"]:
                errors.append(f"phenomenon {pid}: bad verdict {v}")
            neg_only = v in ("excluded", "generated")
            if neg_only != (p["kind"] == "non-phenomenon") and v != "untested":
                errors.append(f"phenomenon {pid}: verdict {v} does not fit kind {p['kind']}")
            if a["derivation_status"] not in pmeta["derivation_status_legend"]:
                errors.append(f"phenomenon {pid}: bad derivation_status")
            for d in a["derivation"]:
                if not claim_ok(d):
                    errors.append(f"phenomenon {pid}: unknown derivation id {d}")
            if a["formalism"] == "spine-v0.1":
                if v == "bolted-on" and not a["extra_assumptions"]:
                    errors.append(f"phenomenon {pid}: bolted-on needs extra_assumptions")
                if v in ("emergent", "parametric") and a["extra_assumptions"]:
                    errors.append(f"phenomenon {pid}: {v} cannot carry extra_assumptions (that is bolted-on)")
                for pr in a["premises"]:
                    if pr not in core and not claim_ok(pr):
                        errors.append(f"phenomenon {pid}: premise {pr} is neither core nor a known claim")
                if v in ("emergent", "parametric") and not a["derivation"]:
                    errors.append(f"phenomenon {pid}: {v} needs a derivation")

    # dependency cycles among K-claims
    graph = {c["id"]: [d for d in c.get("depends_on", []) if d in claim_ids] for c in claims}
    state = {}

    def visit(u, stack):
        state[u] = 1
        for v in graph[u]:
            if state.get(v) == 1:
                errors.append(f"dependency cycle: {' -> '.join(stack + [u, v])}")
            elif not state.get(v):
                visit(v, stack + [u])
        state[u] = 2

    for u in graph:
        if not state.get(u):
            visit(u, [])

    if coverage:
        cnt = {c: 0 for c in concept_ids}
        for e in bib:
            for c in e.get("concepts", []):
                cnt[c] += 1
        thin = sorted(c for c, n in cnt.items() if n < 2)
        warnings.append(f"concepts with <2 bib entries ({len(thin)}): {', '.join(thin)}")
        noevid = sorted(c["id"] for c in claims if not c.get("evidence"))
        warnings.append(f"claims without evidence: {', '.join(noevid) or 'none'}")
        cited = {c for e in bib for c in e.get("supports", []) + e.get("challenges", [])}
        uncited = sorted(c for c in claim_ids if c not in cited)
        warnings.append(f"claims no bib entry supports/challenges: {', '.join(uncited) or 'none'}")
        st = {}
        for e in bib:
            st[e["status"]] = st.get(e["status"], 0) + 1
        warnings.append(f"bibliography status counts: {st}")

    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(bib)} bib, {len(concept_ids)} concepts, {len(concepts['edges'])} edges, "
          f"{len(claim_ids)} claims, {len(debate_ids)} debates, {len(exp_ids)} experiments, "
          f"{len(tasks)} tasks, {len(phen)} phenomena; {len(errors)} errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
