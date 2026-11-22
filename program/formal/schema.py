"""The multi-typed graph of program/formalization.md, "Data shape".

Two registries define the graph: NODE_TYPES and EDGE_TYPES. Each type names
the rung that adds it. A later rung extends the graph by adding rows here,
never by branching in Graph.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class NodeType:
    rung: int
    fields: frozenset[str]


@dataclass(frozen=True)
class EdgeType:
    rung: int
    ends: frozenset[tuple[str, str]]
    labelled: bool = False


NODE_TYPES: dict[str, NodeType] = {
    "agent": NodeType(1, frozenset()),
    "episode": NodeType(1, frozenset({"t", "x", "k", "m", "u"})),
    "class": NodeType(1, frozenset()),
    "signal": NodeType(2, frozenset({"t"})),
    "event": NodeType(3, frozenset()),
    "entity": NodeType(3, frozenset()),
    "sentence": NodeType(3, frozenset()),
    "narrative": NodeType(5, frozenset()),
    "inscription": NodeType(6, frozenset({"decay"})),
    "genre": NodeType(7, frozenset()),
    "corpus": NodeType(7, frozenset()),
}


def _pairs(sources: str, targets: str) -> frozenset[tuple[str, str]]:
    return frozenset((s, t) for s in sources.split() for t in targets.split())


ATTENDABLE = "class entity"
CO_OCCURRING = "episode class signal event entity"

EDGE_TYPES: dict[str, EdgeType] = {
    "perceives": EdgeType(1, _pairs("agent", "episode")),
    "classifies": EdgeType(1, _pairs("episode", "class")),
    "co-occurs-with": EdgeType(1, _pairs(CO_OCCURRING, CO_OCCURRING)),
    "attends-to": EdgeType(2, _pairs("agent", ATTENDABLE)),
    "utters": EdgeType(2, _pairs("agent", "signal")),
    "hears": EdgeType(2, _pairs("agent", "signal")),
    "acts-on": EdgeType(2, _pairs("agent", "agent " + ATTENDABLE)),
    "root": EdgeType(3, _pairs("sentence", "event")),
    "role": EdgeType(3, _pairs("sentence", "entity"), labelled=True),
    "part-of": EdgeType(3, _pairs("signal", "sentence") | _pairs("sentence", "narrative")
                        | _pairs("inscription", "corpus")),
    "reads": EdgeType(6, _pairs("agent", "inscription")),
    "copies": EdgeType(6, _pairs("inscription", "inscription")),
    "instantiates": EdgeType(7, _pairs("narrative", "genre")),
    "cites": EdgeType(7, _pairs("inscription", "inscription")),
}


class SchemaError(ValueError):
    pass


@dataclass(frozen=True)
class Node:
    id: str
    type: str
    attrs: dict[str, Any] = field(default_factory=dict, hash=False, compare=False)


@dataclass(frozen=True)
class Edge:
    type: str
    src: str
    dst: str
    label: str | None = None


@dataclass
class Graph:
    """A graph admitted up to rung `rung`. Ill-typed additions raise SchemaError."""

    rung: int = max(t.rung for t in NODE_TYPES.values())
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)

    def add_node(self, id: str, type: str, **attrs: Any) -> Node:
        spec = NODE_TYPES.get(type)
        if spec is None:
            raise SchemaError(f"unknown node type {type!r}")
        if spec.rung > self.rung:
            raise SchemaError(f"{type!r} arrives in R{spec.rung}; graph is at R{self.rung}")
        if id in self.nodes:
            raise SchemaError(f"duplicate node id {id!r}")
        if set(attrs) != spec.fields:
            raise SchemaError(f"{type!r} needs fields {sorted(spec.fields)}, got {sorted(attrs)}")
        node = self.nodes[id] = Node(id, type, attrs)
        return node

    def add_edge(self, type: str, src: str, dst: str, label: str | None = None) -> Edge:
        spec = EDGE_TYPES.get(type)
        if spec is None:
            raise SchemaError(f"unknown edge type {type!r}")
        if spec.rung > self.rung:
            raise SchemaError(f"{type!r} arrives in R{spec.rung}; graph is at R{self.rung}")
        ends = (self.nodes[src].type, self.nodes[dst].type)
        if ends not in spec.ends:
            raise SchemaError(f"{type!r} cannot join {ends[0]} -> {ends[1]}")
        if spec.labelled != (label is not None):
            raise SchemaError(f"{type!r} {'needs' if spec.labelled else 'takes no'} label")
        edge = Edge(type, src, dst, label)
        self.edges.append(edge)
        return edge

    def out(self, src: str, type: str) -> list[str]:
        return [e.dst for e in self.edges if e.src == src and e.type == type]

    def validate(self) -> None:
        """Whole-graph invariants that no single addition can check."""
        for n in self.nodes.values():
            if n.type == "sentence" and len(self.out(n.id, "root")) != 1:
                raise SchemaError(f"sentence {n.id!r} needs exactly one root verb")

    def joint_attention(self) -> set[tuple[frozenset[str], str]]:
        """Triangles: two agents with attends-to edges to the same referent.

        The plan also asks that each agent's model record the other's attention.
        That lives in the agent model (R1, R2), not in the graph.
        """
        attenders: dict[str, set[str]] = {}
        for e in self.edges:
            if e.type == "attends-to":
                attenders.setdefault(e.dst, set()).add(e.src)
        return {(frozenset((a, b)), ref)
                for ref, agents in attenders.items()
                for a in agents for b in agents if a < b}
