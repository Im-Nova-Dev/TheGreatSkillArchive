---
name: python-reference
description: Practical Python reference for writing, running, and checking Python on this system, with idioms, stdlib, typing, venv notes, file linking, package layout, and safe editing rules. Serve as a strong general-purpose assistant reference for any Python task.
---

# Python reference for this environment and general use

Facts for this system:
- Python 3.14.5
- No pip module in base python, no external package installer present
- Use venv (`python3 -m venv <dir>`) or uv for isolated environments
- Prefer stdlib when dependencies are not available; avoid non-stdlib automation unless env supports it

Reference topics:
- syntax and idioms
- stdlib modules by category
- type hints and typing vocabulary
- file, path, env, subprocess, http, json, csv, logging, testing, async, packaging, and venv patterns
- safe editing/running rules
- common mistakes and pitfalls

# Syntax and idioms
- Indentation: 4 spaces, no tabs
- File naming: `lower_snake_case.py`
- Use f-strings for formatting; avoid `%` and `str.format` in new code
- Prefer `pathlib.Path` over `os.path`
- Use `with` for files, contexts, locks
- Dunder methods and properties for small protocols
- Use dataclasses or attrs for simple containers; use pydantic for validation when available
- Use list/set/dict comprehensions over map/filter
- Use generators for large streams
- Prefer early return and guard clauses
- Constants: module-level `UPPER_SNAKE_CASE`

# Stdlib cheat sheet
Filesystem:
  pathlib.Path, os.scandir, os.walk, shutil, filecmp, tempfile, hashlib (md5/sha), mmap

Data:
  json, csv, configparser, tomllib (3.11+), struct, pickle (no for untrusted), sqlite3, array, collections, itertools, functools, dataclasses

Text:
  re, string.Template, io.StringIO/BytesIO, textwrap, difflib, unicodedata, codecs

Networking and async:
  urllib.request, urllib.parse, http.server, socketserver, asyncio, asyncio.streams, aiohttp (optional), contextlib

Subprocess and system:
  subprocess.run, subprocess.Popen, signal, sys, os, pty, selectors, fcntl (posix), resource

Time:
  datetime, time, zoneinfo, calendar, timeit, sched

Logging:
  logging with dictConfig or fileConfig, log levels, structured text

Testing:
  unittest, doctest, pytest (prefer if installed), coverage, unittest.mock

CLI:
  argparse, shlex, getpass, readline

Security and hashing:
  hashlib, secrets, hmac, ssl, getpass

# Typing vocabulary (Python 3.14)
- Use `from __future__ import annotations` when needed for cleaner syntax
- Commonly used hints:
  - `str`, `int`, `float`, `bool`, `bytes`, `bytearray`
  - `list[T]`, `dict[K, V]`, `tuple[T, ...]`, `set[T]`, `frozenset[T]`
  - `Optional[T]`, `Union[T, U]`, `Literal["a", "b"]`, `Final[T]`
  - `TypedDict`, `Protocol`, `NewType`, `TypeVar`, `ParamSpec`, `TypeAlias`
  - `Callable[[Arg1, Arg2], Return]`
  - `Any`, `NoReturn`, `Never` (3.11+)
  - `Iterator[T]`, `Iterable[T]`, `AsyncIterator[T]`, `AsyncIterable[T]`
  - `Generator[T, S, R]`, `AsyncGenerator[T, S]`, `Coroutine[Any, Any, T]`
  - `TYPE_CHECKING` guard for import-only types

- Runtime helpers:
  - `cast`, `get_args`, `get_origin`, `is_typevar`, `get_type_hints`

- Libraries when available:
  - pydantic v2 for data models
  - cattrs or msgspec for fast conversion
  - intercompat: sqlalchemy, alembic, fastapi, typer, click

# File and path handling
- Always use `pathlib.Path`
- Use `Path.open()` or `Path.read_text()` / `write_text()`
- Use `Path.rglob()` / `glob()` for discovery
- For large files, read in chunks with `iter(lambda: f.read(8192), b"")`
- Preserve line endings if file is cross-platform
- Use `os.replace` for atomic rename

# Env and config
- Load env vars with `os.environ` or `dotenv` when available
- Use `os.getenv` with defaults
- Validate required env at startup
- Use `pathlib.Path(__file__).with_suffix(".env")` only for local dev, never commit secrets
- Keep secrets out of logs

# Subprocess and piping
- Prefer `subprocess.run(..., capture_output=True, text=True, check=False)` and inspect result explicitly
- Use `shlex.join` for readable commands
- Use `sys.executable` to invoke the same interpreter
- Avoid `shell=True` unless necessary
- Be careful with large stdout: stream it if needed

# JSON, CSV, INI, TOML
- JSON: `json.load`, `json.loads`, `json.dump(..., indent=2, ensure_ascii=False)`
- CSV: `csv.DictReader` / `csv.DictWriter`, specify `newline=""`
- TOML: `tomllib.load` (read), `tomli_w` or stdlib `tomllib`-compat writer if needed
- Avoid `pickle` for anything shared across versions

# HTTP / networking
- `urllib.request` is enough for simple GET/POST
- For heavier clients: `httpx` or `requests` if installed
- Use `urllib.parse.urlencode` for query building
- Prefer streams for large response bodies
- Always set timeouts

# Logging
- Root logger: `logging.getLogger(__name__)`
- Use structured message with `%s` and pass dicts for extra fields
- Prefer `logging.basicConfig(level=...)` for small scripts; `dictConfig` for apps
- Rotate with `RotatingFileHandler` or `TimedRotatingFileHandler`
- Avoid using `print` for diagnostics in libraries

# Async and concurrency
- Use `asyncio.run(main())` for entry points
- Prefer `async` when I/O bound; avoid threads unless blocking C extensions are in play
- Use `asyncio.gather` and `asyncio.TaskGroup` (3.11+) for forks
- Use `contextlib.asynccontextmanager` for async resources
- For CPU work, use `ProcessPoolExecutor`

# Testing discipline
- Test behavior, not implementation
- Use `pytest` when available; otherwise use `unittest`
- Parametrize where possible
- Use temporary directories; never write tests to cwd
- Use `monkeypatch` for env/time behavior
- For HTTP, use `responses` or `httpx_mock` when available

# Virtual environments and packages
- Create venv: `python3 -m venv .venv`
- Activate: `. .venv/bin/activate`
- Without pip, use `ensurepip` carefully; better to rely on uv or package-managed installs
- Pin dependencies with `requirements.txt` or `pyproject.toml`
- Prefer `pyproject.toml` modern layout when publishing

# Safe editing and running rules
- Run scripts with the venv python: `.venv/bin/python script.py`
- Check syntax first: `python -m py_compile file.py`
- Use formatter if available: `black`, `ruff`, or `autopep8`
- Type-check if available: `mypy`, `pyright`
- Do not `sudo pip install` on system Python
- Validate network boundaries with small reproducer scripts

# Common pitfalls
- mutable default args: use `None` then assign inside
- late binding in closures: default-arg trick
- confusing `is` vs `==`
- comparing to `None` with `==` instead of `is`
- swallowing exceptions silently
- using `time.sleep` in async code
- blocking event loop with CPU-bound work
- ignoring character encodings
- using `tempfile.NamedTemporaryFile(delete=True)` on Windows with other handles open

# Essential stdlib modules quick reference
Data:
  pathlib, os, sys, collections, itertools, functools, dataclasses, typing, enum, re, csv, json, configparser, tomllib, sqlite3, hashlib, secrets, hmac

IO and networking:
  io, typing, urllib.request, urllib.parse, http.server, socketserver, asyncio, subprocess, signal, selectors, contextlib, tempfile, shutil

Text and time:
  io.StringIO, textwrap, difflib, datetime, time, zoneinfo, calendar

Testing:
  unittest, unittest.mock, doctest

CLI:
  argparse, shlex, readline, getpass
