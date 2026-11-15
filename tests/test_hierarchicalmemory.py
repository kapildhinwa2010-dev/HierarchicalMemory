import pytest

from hierarchicalmemory import Fact, HierarchicalMemory, KnowledgeNet


def test_fact_basic():
    fact = Fact("a", "knows", "b")
    assert fact.as_tuple() == ("a", "knows", "b")


def test_fact_rejects_empty():
    with pytest.raises(ValueError):
        Fact("", "knows", "b")


def test_layer_add_and_len():
    mem = HierarchicalMemory(n_levels=2)
    assert mem.add(0, "a", "knows", "b") is True
    assert mem.add(0, "a", "knows", "b") is False
    assert len(mem.layer(0)) == 1
    assert len(mem) == 2


def test_add_rejects_bad_level():
    mem = HierarchicalMemory(n_levels=2)
    with pytest.raises(ValueError):
        mem.add(5, "a", "knows", "b")


def test_layer_rejects_bad_level():
    mem = HierarchicalMemory()
    with pytest.raises(ValueError):
        mem.layer(-1)


def test_constructor_rejects_zero():
    with pytest.raises(ValueError):
        HierarchicalMemory(n_levels=0)


# --- hierarchical search (HierarchicalMemory-specific) ---


def test_search_reports_level():
    mem = HierarchicalMemory(n_levels=3)
    mem.add(1, "a", "knows", "b")
    hits = mem.search(subject="a")
    assert len(hits) == 1
    assert hits[0][0] == 1


def test_search_lowest_layer_first():
    mem = HierarchicalMemory(n_levels=2)
    mem.add(0, "a", "knows", "b")
    mem.add(1, "a", "knows", "b")
    hits = mem.search(subject="a")
    assert [h[0] for h in hits] == [0, 1]


def test_search_no_hits():
    mem = HierarchicalMemory()
    mem.add(0, "a", "knows", "b")
    assert mem.search(subject="zzz") == []


def test_copy_up_duplicates_fact():
    mem = HierarchicalMemory(n_levels=2)
    mem.add(0, "a", "knows", "b")
    assert mem.copy_up(0, "a", "knows", "b", to_level=1) is True
    assert len(mem.layer(0)) == 1
    assert len(mem.layer(1)) == 1


def test_copy_up_missing_fact_raises():
    mem = HierarchicalMemory(n_levels=2)
    with pytest.raises(KeyError):
        mem.copy_up(0, "a", "knows", "b", to_level=1)


def test_total_facts():
    mem = HierarchicalMemory(n_levels=2)
    mem.add(0, "a", "knows", "b")
    mem.add(1, "c", "knows", "d")
    assert mem.total_facts() == 2