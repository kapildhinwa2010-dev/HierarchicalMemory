# HierarchicalMemory

HierarchicalMemory is a small Python module for storing string-valued facts as `(subject, predicate, object)` triples in separate, numbered in-memory layers. It can query each layer and report matching layers in ascending level order. The repository is an early, minimal implementation: it provides basic storage and filtering, not an autonomous or persistent memory system.

## What is implemented

- `Fact` validates that its subject, predicate, and object are non-empty strings. Facts support tuple conversion, equality, hashing, and representation.
- `KnowledgeNet` stores unique facts in one layer, lists them in sorted order, and filters queries by optional subject, predicate, and object values. Duplicate triples in the same layer are ignored.
- `HierarchicalMemory(n_levels=3)` creates the requested number of independent `KnowledgeNet` layers. `add(level, subject, predicate, obj)` writes to one layer; `layer(level)` returns that layer; `search(...)` returns `(level, facts)` pairs for every matching layer in ascending level order.
- `copy_up(level, subject, predicate, obj, to_level)` copies a fact to another layer. It does not remove the source fact; it raises `KeyError` when the fact is absent from the source.
- `total_facts()` counts facts across all layers, including copies in multiple layers.

Invalid layer indices and empty fact fields raise `ValueError`. A search with no matches returns an empty list.

## Requirements and use from a checkout

The project metadata requires Python 3.9 or later and declares `numpy>=1.24`. The repository's `requirements.txt` also includes pytest for running the tests. The module itself is imported from the repository checkout; this repository does not provide a command-line interface.

```bash
git clone https://github.com/kapildhinwa2010-dev/HierarchicalMemory.git
cd HierarchicalMemory
python -m pip install -r requirements.txt
```

Example from the repository root:

```python
from hierarchicalmemory import HierarchicalMemory

memory = HierarchicalMemory(n_levels=3)
memory.add(0, "alice", "knows", "bob")
print(memory.search(subject="alice"))
# [(0, [Fact('alice', 'knows', 'bob')])]

memory.copy_up(0, "alice", "knows", "bob", to_level=1)
print(memory.total_facts())  # 2: the fact remains in both layers
```

The exported module names are `Fact`, `KnowledgeNet`, and `HierarchicalMemory`.

## Tests and CI

On the cloned repository commit `6c5d2bfcc547fd12d145a2e1495814155371d0db`, the local test run `python -m pytest -q` completed with **12 passed**. `python -m compileall -q hierarchicalmemory.py tests` and the configured import/constructor smoke check also completed successfully in that run. These are local results for that checkout; no claim is made here about a hosted CI run.

The GitHub Actions CI workflow is configured to run pytest, compile the module and tests, and perform an import/constructor smoke check on Python 3.10, 3.11, and 3.12. A separate workflow configures CodeQL analysis for Python. Workflow configuration is not itself evidence that a particular hosted run passed.

## Limitations and scope

- All data is held in memory; there is no persistence or serialization API in the implementation.
- Layers are independent stores. There is no automatic summarization, cross-layer consistency, inference, promotion, or demotion.
- The caller chooses the destination layer when adding or copying a fact. A copied fact is duplicated, not moved, and duplicates are only suppressed within an individual layer.
- Queries return matching stored triples; the code does not implement a graph traversal, semantic search, or model-backed memory system.
- The implementation has no documented performance guarantees or benchmark results.

## License

The repository's `LICENSE` file contains the MIT License (copyright 2026 Kapildhinwa2010-dev). See [LICENSE](LICENSE) for the full terms.
