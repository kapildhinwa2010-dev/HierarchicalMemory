# HierarchicalMemory - Layered fact memory with level-ordered search
# Part of the Kapildhinwa2010-dev Toolkit.

"""Layered fact memory: separate KnowledgeNet per level.

Lineage: reserv.dean-part-2 (HELIX). Facts live in numbered layers
(0 = hot/fine-grained, higher = coarser). Searches walk layers in order
and report which layer answered; copy_up promotes a fact to a coarser
layer.

HONEST LIMITATION: layers are independent stores - there is no automatic
summarization or consistency between levels; copy_up duplicates, it does
not move.
"""

from __future__ import annotations

from collections import defaultdict

__all__ = ["Fact", "KnowledgeNet", "HierarchicalMemory"]


class Fact:
    """A single (subject, predicate, object) triple."""

    __slots__ = ("subject", "predicate", "object")

    def __init__(self, subject: str, predicate: str, obj: str) -> None:
        for value in (subject, predicate, obj):
            if not isinstance(value, str) or not value:
                raise ValueError("subject, predicate and object must be non-empty strings")
        self.subject = subject
        self.predicate = predicate
        self.object = obj

    def as_tuple(self):
        return (self.subject, self.predicate, self.object)

    def __eq__(self, other) -> bool:
        return isinstance(other, Fact) and self.as_tuple() == other.as_tuple()

    def __hash__(self) -> int:
        return hash(self.as_tuple())

    def __repr__(self) -> str:
        return "Fact({!r}, {!r}, {!r})".format(*self.as_tuple())


class KnowledgeNet:
    """Single-layer fact store with indexed queries."""

    def __init__(self) -> None:
        self._facts: set = set()
        self._by_subject: dict = defaultdict(list)
        self._by_object: dict = defaultdict(list)

    def add(self, subject: str, predicate: str, obj: str) -> bool:
        """Add a fact; returns False if it already exists."""
        fact = Fact(subject, predicate, obj)
        if fact in self._facts:
            return False
        self._facts.add(fact)
        self._by_subject[fact.subject].append(fact)
        self._by_object[fact.object].append(fact)
        return True

    def facts(self):
        return sorted(self._facts, key=lambda f: f.as_tuple())

    def __len__(self) -> int:
        return len(self._facts)

    def query(self, subject=None, predicate=None, obj=None):
        """Return facts matching the given pattern (None = wildcard)."""
        results = self._facts
        if subject is not None:
            results = [f for f in results if f.subject == subject]
        if predicate is not None:
            results = [f for f in results if f.predicate == predicate]
        if obj is not None:
            results = [f for f in results if f.object == obj]
        return sorted(results, key=lambda f: f.as_tuple())


class HierarchicalMemory:
    """Numbered fact layers searched in level order."""

    def __init__(self, n_levels: int = 3) -> None:
        if n_levels < 1:
            raise ValueError("n_levels must be >= 1")
        self.layers = [KnowledgeNet() for _ in range(int(n_levels))]

    def add(self, level: int, subject: str, predicate: str, obj: str) -> bool:
        """Add a fact to one layer; returns False if it already exists there."""
        self._check_level(level)
        return self.layers[level].add(subject, predicate, obj)

    def _check_level(self, level: int) -> None:
        if not 0 <= level < len(self.layers):
            raise ValueError("level must be in [0, {}]".format(len(self.layers) - 1))

    def layer(self, level: int) -> KnowledgeNet:
        """The KnowledgeNet at ``level``."""
        self._check_level(level)
        return self.layers[level]

    def search(self, subject=None, predicate=None, obj=None) -> list:
        """(level, facts) pairs for the first layers that match, lowest first.

        Walks layers 0..N; returns every layer that has matches. An empty
        result list means no layer contained the pattern.
        """
        hits = []
        for level, net in enumerate(self.layers):
            found = net.query(subject=subject, predicate=predicate, obj=obj)
            if found:
                hits.append((level, found))
        return hits

    def copy_up(self, level: int, subject: str, predicate: str, obj: str, to_level: int) -> bool:
        """Copy a fact from ``level`` to ``to_level`` (duplicate, not move)."""
        self._check_level(level)
        self._check_level(to_level)
        fact = Fact(subject, predicate, obj)
        if fact not in self.layers[level]._facts:
            raise KeyError("fact not present at level {}".format(level))
        return self.layers[to_level].add(subject, predicate, obj)

    def total_facts(self) -> int:
        return sum(len(net) for net in self.layers)

    def __len__(self) -> int:
        return len(self.layers)