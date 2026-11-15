# HierarchicalMemory

[![CI](https://github.com/kapildhinwa2010-dev/HierarchicalMemory/actions/workflows/ci.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/HierarchicalMemory/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kapildhinwa2010-dev/HierarchicalMemory/actions/workflows/codeql.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/HierarchicalMemory/actions/workflows/codeql.yml)


Layered fact memory: numbered KnowledgeNet layers searched lowest-first.

**Part of the [Kapildhinwa2010-dev Toolkit](https://github.com/kapildhinwa2010-dev/Kapildhinwa2010-dev).**

## What it does

Facts live in numbered layers (0 = hot/fine-grained, higher =
coarser). search() walks layers in order and reports which layer
answered; copy_up() promotes a fact to a coarser layer. HONEST
LIMITATION (also in the docstring): layers are independent stores -
no automatic summarization or consistency between levels; copy_up
duplicates, it does not move.

## Install

```bash
pip install -r requirements.txt
```

## Quick start

```python
from hierarchicalmemory import HierarchicalMemory

mem = HierarchicalMemory(n_levels=3)
mem.add(0, "a", "next", "b")
print(mem.search(subject="a"))  # [(0, [Fact(a, next, b)])]
mem.copy_up(0, "a", "next", "b", to_level=1)
print(mem.total_facts())        # 2 (duplicated, not moved)
```

## API

- add(level, s, p, o) / layer(level)
- search(subject, predicate, obj) - (level, facts) pairs, lowest first
- copy_up(level, s, p, o, to_level) - duplicate to a coarser layer
- total_facts()

## Honest results and limitations

- No automatic promotion or demotion: you decide what goes where.
- The same fact can exist in several layers; there is no dedup
  across layers, only within one.
- No persistence.

## License

MIT - see [LICENSE](LICENSE).
