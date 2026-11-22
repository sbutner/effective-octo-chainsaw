#!/usr/bin/env python3
"""The gate: schema, references, dependency cycles, the check ledger, and generated views.

Usage:
    python3 program/tools/validate.py                    # exit 1 on any error
    python3 program/tools/validate.py --coverage         # also report thin spots
    python3 program/tools/validate.py --baseline DIR     # also check changes against DIR/<name>.json
                                                         # (the pre-commit hook passes HEAD's data files)

Exit 0 is required before any commit (see .githooks/pre-commit). It needs no prover: it
checks that every ledger verdict is current for its check's source, not the math itself.
`check.py --verify` reruns the math.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check  # noqa: E402
import db  # noqa: E402
import phenomena  # noqa: E402
import protocol  # noqa: E402
import render  # noqa: E402


def check_schema(name, recs, errors):
    """Required fields, types and enums from db.SCHEMA. Returns the records that pass."""
    spec, optional = db.SCHEMA.get(name, {}), db.OPTIONAL.get(name, set())
    _, idk = db.COLLECTIONS[name]
    good = []
    for r in recs:
        rid = r.get(idk, "?")
        bad = []
        for field, want in spec.items():
            if field not in r:
                if field not in optional:
                    bad.append(f"missing {field}")
                continue
            v = r[field]
            if isinstance(want, list):
                inner = want[0]
                ok = isinstance(v, list) and all(x in inner if isinstance(inner, set) else isinstance(x, inner) for x in v)
            elif isinstance(want, set):
                ok = type(v) in {type(x) for x in want} and v in want
            else:
                ok = isinstance(v, want) and not isinstance(v, bool)
            if not ok:
                bad.append(f"bad {field} {v!r}")
        for b in bad:
            errors.append(f"{name} {rid}: {b}")
        if not bad:
            good.append(r)
    ids = [r.get(idk) for r in recs]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        errors.append(f"{name}: duplicate ids {dup}")
    return good


def main():
    coverage = "--coverage" in sys.argv
    baseline = Path(sys.argv[sys.argv.index("--baseline") + 1]) if "--baseline" in sys.argv else None
    errors, warnings = [], []
    docs = {n: db.load(n) for n in db.COLLECTIONS}
    for n in db.COLLECTIONS:
        errors += protocol.layout_errors(n, (db.DATA / f"{n}.json").read_text(encoding="utf-8"))
    base_ph = baseline / "phenomena.json" if baseline else None
    if base_ph and base_ph.exists():
        errors += protocol.phenomena_violations(json.loads(base_ph.read_text(encoding="utf-8")), docs["phenomena"])
    recs = {n: check_schema(n, docs[n][key], errors) for n, (key, _) in db.COLLECTIONS.items()}
    bib_keys = {e["key"] for e in recs["bibliography"]}
    concept_ids = {n["id"] for n in recs["concepts"]}
    claim_ids = {c["id"] for c in recs["claims"]}
    debate_ids = {d["id"] for d in recs["debates"]}
    exp_ids = {x["id"] for x in recs["experiments"]}
    phen_ids = {p["id"] for p in docs["phenomena"]["phenomena"]}
    mrs = docs["claims"]["master_relations"]
    claim_ok = db.claim_space()
    debt_hit = {k: set() for k in db.DEBT}

    def violation(kind, rid, msg):
        """A protocol violation: a warning while the id is listed debt, an error otherwise."""
        if rid in db.DEBT[kind]:
            debt_hit[kind].add(rid)
            if coverage:
                warnings.append(f"debt: {msg}")
        else:
            errors.append(msg)

    def refs(owner, ids, ok, what):
        for i in ids:
            if not ok(i):
                errors.append(f"{owner}: unknown {what} {i}")

    for e in recs["bibliography"]:
        refs(f"bibliography {e['key']}", e.get("concepts", []), concept_ids.__contains__, "concept")
        refs(f"bibliography {e['key']}", e.get("supports", []) + e.get("challenges", []), claim_ok, "claim")
        if e["status"] == "checked" and not e.get("url"):
            errors.append(f"bibliography {e['key']}: checked without a url")
    for ed in docs["concepts"]["edges"]:
        if ed["relation"] not in docs["concepts"]["meta"]["relations"]:
            warnings.append(f"concept edge {ed['source']}->{ed['target']}: relation {ed['relation']} not in meta.relations")
        refs(f"concept edge {ed['source']}->{ed['target']}", [ed["source"], ed["target"]], concept_ids.__contains__, "concept")
    for c in recs["claims"]:
        refs(f"claim {c['id']}", c["depends_on"] + c.get("links", []), claim_ok, "claim")
        refs(f"claim {c['id']}", c.get("evidence", []), bib_keys.__contains__, "bib key")
        if not c["falsifier"] and c["status"] not in ("known", "definition"):
            violation("falsifier", c["id"], f"claim {c['id']}: {c['status']} claim needs a falsifier")
    for m in mrs:
        refs(f"master relation {m['id']}", m["claims"], claim_ok, "claim")
    for d in recs["debates"]:
        refs(f"debate {d['id']}", d["llm_evidence"], bib_keys.__contains__, "bib key")
        refs(f"debate {d['id']}", d["claims"], claim_ok, "claim")
    for x in recs["experiments"]:
        refs(f"experiment {x['id']}", x["tests"], lambda i: claim_ok(i) or i in debate_ids, "claim or debate")
        refs(f"experiment {x['id']}", x.get("related", []), lambda i: i in bib_keys or claim_ok(i) or i in exp_ids, "reference")

    tasks = {t["id"]: t for t in recs["tasks"]}
    for t in recs["tasks"]:
        refs(f"task {t['id']}", t["depends_on"], tasks.__contains__, "task")
        for d in t["depends_on"]:
            if d in tasks and t["priority"] < tasks[d]["priority"]:
                errors.append(f"task {t['id']}: priority {t['priority']} outranks its dependency {d} (priority {tasks[d]['priority']})")

    # phenomena menu (emergence verifier, harness.md §5.5)
    pmeta = docs["phenomena"]["meta"]
    formalisms = {f["id"]: f for f in pmeta["formalisms"]}
    core = set(formalisms["spine-v0.1"]["core_premises"])
    for p in docs["phenomena"]["phenomena"]:
        pid, g, own = p["id"], p["grounding"], f"phenomenon {p['id']}"
        for field, legend in (("kind", "kind_legend"),):
            if p[field] not in pmeta[legend]:
                errors.append(f"{own}: bad {field} {p[field]}")
        if p["field"] not in pmeta["fields"]:
            errors.append(f"{own}: bad field {p['field']}")
        refs(own, p["layers"], db.LAYERS.__contains__, "layer")
        if g["strength"] not in pmeta["strength_legend"] or g["pattern"] not in pmeta["pattern_legend"]:
            errors.append(f"{own}: bad strength/pattern")
        refs(own, g["theorized"] + g["observed"], bib_keys.__contains__, "bib key")
        if not (g["theorized"] or g["observed"] or g["source_hints"]) and p["kind"] != "non-phenomenon":
            errors.append(f"{own}: no grounding source")
        if g["strength"] in ("robust", "replicated"):
            checked = {e["key"] for e in recs["bibliography"] if e["status"] == "checked"}
            if not checked & set(g["theorized"] + g["observed"]):
                violation("unchecked-strength", pid, f"{own}: {g['strength']} needs a checked source (AGENTS.md phenomena protocol)")
        if p.get("contrast_with") and p["contrast_with"] not in phen_ids:
            errors.append(f"{own}: unknown contrast {p['contrast_with']}")
        refs(own, p.get("debates", []), debate_ids.__contains__, "debate")
        for a in p["assessments"]:
            v = a["verdict"]
            if a["formalism"] not in formalisms:
                errors.append(f"{own}: unknown formalism {a['formalism']}")
            if v not in pmeta["verdict_legend"]:
                errors.append(f"{own}: bad verdict {v}")
            if (v in ("excluded", "generated")) != (p["kind"] == "non-phenomenon") and v != "untested":
                errors.append(f"{own}: verdict {v} does not fit kind {p['kind']}")
            if a["derivation_status"] not in pmeta["derivation_status_legend"]:
                errors.append(f"{own}: bad derivation_status {a['derivation_status']}")
            refs(own, a["derivation"], claim_ok, "derivation id")
            if a["formalism"] != "spine-v0.1":
                continue
            if v == "bolted-on" and not a["extra_assumptions"]:
                errors.append(f"{own}: bolted-on needs extra_assumptions")
            if v in ("emergent", "parametric"):
                if a["extra_assumptions"]:
                    errors.append(f"{own}: {v} cannot carry extra_assumptions (that is bolted-on)")
                if not a["derivation"]:
                    errors.append(f"{own}: {v} needs a derivation")
            refs(own, a["premises"], lambda i: i in core or claim_ok(i), "premise (neither core nor a claim)")

    for kind, listed in db.DEBT.items():
        for rid in sorted(listed - debt_hit[kind]):
            errors.append(f"debt {kind}: {rid} is fixed; remove it from db.DEBT")

    ph = docs["phenomena"]["phenomena"]
    sc, mf = phenomena.score(ph, phenomena.SPINE), phenomena.must_failures(ph, phenomena.SPINE)
    for pid, v in mf:
        errors.append(f"phenomenon {pid}: must-emerge item is {v} for {phenomena.SPINE}")
    for pid in sc["contradicted"] + sc["false_positives"]:
        errors.append(f"phenomenon {pid}: {phenomena.SPINE} contradicts it or generates a negative control")

    # dependency cycles among K-claims
    graph = {c["id"]: [d for d in c["depends_on"] if d in claim_ids] for c in recs["claims"]}
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

    # checks and ledger (harness.md §5)
    checks = check.load_checks()
    ledger = check.read_ledger()
    seen = set()
    for c, src, digest in checks:
        own = f"check {c.id} ({src})"
        if c.id in seen:
            errors.append(f"{own}: duplicate id")
        seen.add(c.id)
        if c.role not in check.ROLES:
            errors.append(f"{own}: bad role {c.role}")
        if c.kind not in check.EXPECT or c.expect not in check.EXPECT.get(c.kind, ()):
            errors.append(f"{own}: bad kind/expect {c.kind}/{c.expect}")
        if (c.subject is None) != (c.role == "sanity"):
            errors.append(f"{own}: sanity checks have no subject; every other check needs one")
        if c.subject and not claim_ok(db.subject_base(c.subject)):
            errors.append(f"{own}: subject {c.subject} names no known claim")
        if c.role == "refutes" and (c.kind, c.expect) != ("witness", "counterexample"):
            errors.append(f"{own}: a refutation must be a witness expecting a counterexample")
        st = check.entry_state(c, digest, ledger.get(c.id))
        if st != "ok":
            errors.append(f"{own}: verdict {st}; run python3 program/tools/check.py")
    for orphan in sorted(set(ledger) - seen):
        errors.append(f"ledger {orphan}: no such check; delete {check.ledger_path(orphan).relative_to(db.REPO)}")
    for s, (tier, why) in check.tiers(checks, ledger).items():
        if "encoding is wrong" in why:
            errors.append(f"subject {s}: {why}")

    for p in render.stale():
        errors.append(f"generated view out of date: {p.relative_to(db.REPO)}; run python3 program/tools/render.py")

    if coverage:
        cnt = {c: 0 for c in concept_ids}
        for e in recs["bibliography"]:
            for c in e.get("concepts", []):
                cnt[c] = cnt.get(c, 0) + 1
        thin = sorted(c for c, n in cnt.items() if n < 2)
        warnings.append(f"concepts with <2 bib entries ({len(thin)}): {', '.join(thin)}")
        warnings.append("claims without evidence: " + (", ".join(sorted(c["id"] for c in recs["claims"] if not c.get("evidence"))) or "none"))
        cited = {c for e in recs["bibliography"] for c in e.get("supports", []) + e.get("challenges", [])}
        warnings.append("claims no bib entry supports/challenges: " + (", ".join(sorted(claim_ids - cited)) or "none"))
        st = {}
        for e in recs["bibliography"]:
            st[e["status"]] = st.get(e["status"], 0) + 1
        warnings.append(f"bibliography status counts: {st}")

    if not coverage and any(debt_hit.values()):
        warnings.append("protocol debt: " + ", ".join(f"{len(v)} {k}" for k, v in debt_hit.items())
                        + " (listed in db.DEBT; --coverage shows them; task Q-24)")
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(bib_keys)} bib, {len(concept_ids)} concepts, {len(docs['concepts']['edges'])} edges, "
          f"{len(claim_ids)} claims, {len(mrs)} master relations, {len(debate_ids)} debates, {len(exp_ids)} experiments, "
          f"{len(recs['tasks'])} tasks, {len(phen_ids)} phenomena, {len(checks)} checks; {len(errors)} errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
