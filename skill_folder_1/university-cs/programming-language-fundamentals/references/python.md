# Python

Teaching priorities: data model first, then control flow, then the standard library, then packaging.

- Data model: everything is an object; mutability matters (`list` vs `tuple`, `dict`, `set`); context managers close resources.
- Functions: first-class, closures capture by reference, default arguments evaluated once.
- Concurrency: GIL limits CPU threads; prefer `asyncio` for I/O concurrency, `multiprocessing` for CPU parallelism.
- Idioms: list comprehensions, generators, `f-strings`, `pathlib`, `dataclasses`.
- Packaging: `pyproject.toml`, `venv`, test with `pytest`.