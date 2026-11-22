import re
from pathlib import Path

import pytest

from schema import EDGE_TYPES, NODE_TYPES, Graph, SchemaError

PLAN = (Path(__file__).parents[1] / "formalization.md").read_text()
STRUCTURAL_EDGES = {"root", "role"}  # the sentence hyperedge's own edges


def plan_node_types():
    rows = re.findall(r"^\| ([a-z, ()]+) \| R(\d) \|", PLAN, re.M)
    return {name.split(" (")[0]: int(r) for cell, r in rows for name in cell.split(", ")}


def plan_edge_types():
    line = re.search(r"\*\*Edge types:\*\* (.+)\.", PLAN).group(1)
    return {name.split(" (")[0] for name in line.split(", ")}


def test_registry_matches_plan():
    assert {k: v.rung for k, v in NODE_TYPES.items()} == plan_node_types()
    assert set(EDGE_TYPES) - STRUCTURAL_EDGES == plan_edge_types()


def full_graph():
    g = Graph()
    g.add_node("a", "agent")
    g.add_node("b", "agent")
    g.add_node("e1", "episode", t=0, x=3, k=None, m=None, u=None)
    for i, typ in enumerate(["class", "event", "entity", "sentence", "narrative",
                             "genre", "corpus"]):
        g.add_node(typ, typ)
    g.add_node("s1", "signal", t=0)
    g.add_node("i1", "inscription", decay=0.0)
    g.add_node("i2", "inscription", decay=0.0)
    edges = [
        ("perceives", "a", "e1"), ("classifies", "e1", "class"),
        ("co-occurs-with", "e1", "s1"), ("attends-to", "a", "class"),
        ("attends-to", "b", "class"), ("utters", "a", "s1"), ("hears", "b", "s1"),
        ("acts-on", "a", "b"), ("root", "sentence", "event"),
        ("part-of", "s1", "sentence"), ("part-of", "sentence", "narrative"),
        ("part-of", "i1", "corpus"), ("reads", "b", "i1"), ("copies", "i2", "i1"),
        ("instantiates", "narrative", "genre"), ("cites", "i2", "i1"),
    ]
    for e in edges:
        g.add_edge(*e)
    g.add_edge("role", "sentence", "entity", label="agent")
    return g


def test_every_type_instantiates_and_validates():
    g = full_graph()
    g.validate()
    assert {n.type for n in g.nodes.values()} == set(NODE_TYPES)
    assert {e.type for e in g.edges} == set(EDGE_TYPES)


def test_joint_attention_is_the_triangle():
    assert full_graph().joint_attention() == {(frozenset({"a", "b"}), "class")}


@pytest.mark.parametrize("bad", [
    lambda g: g.add_node("x", "verb"),                        # unknown type
    lambda g: g.add_node("a", "agent"),                       # duplicate id
    lambda g: g.add_node("e2", "episode", t=0, x=1),          # missing fields
    lambda g: g.add_edge("perceives", "e1", "a"),             # wrong direction
    lambda g: g.add_edge("utters", "a", "class"),             # wrong target
    lambda g: g.add_edge("role", "sentence", "entity"),       # role needs a label
    lambda g: g.add_edge("cites", "i2", "i1", label="x"),     # cites takes none
    lambda g: g.add_edge("bites", "a", "b"),                  # unknown edge
])
def test_ill_typed_additions_are_rejected(bad):
    with pytest.raises(SchemaError):
        bad(full_graph())


def test_sentence_needs_one_root():
    g = full_graph()
    g.add_node("ev2", "event")
    g.add_edge("root", "sentence", "ev2")
    with pytest.raises(SchemaError):
        g.validate()


def test_rung_gates_types():
    g = Graph(rung=1)
    g.add_node("a", "agent")
    with pytest.raises(SchemaError):
        g.add_node("s", "signal")
    g2 = Graph(rung=2)
    g2.add_node("a", "agent")
    g2.add_node("c", "class")
    g2.add_edge("attends-to", "a", "c")   # joint attention needs no entity node in R2
    with pytest.raises(SchemaError):
        g2.add_node("n", "entity")
