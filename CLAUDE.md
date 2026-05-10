# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```sh
# Install library dependencies
pip install -r src/requirements.txt

# Install test dependencies
pip install -r tests/requirements.txt

# Run all tests
pytest tests/

# Run single test file
pytest tests/test_jupiter.py

# Run single test
pytest tests/test_jupiter.py::TestJupiter::test_get_price_sync

# Run tests with coverage
coverage run -m pytest tests/

# Lint
ruff check src/
```

## Test Configuration

Tests require `tests/test.ini` (not committed). Copy `tests/test.default.ini` and rename to `test.ini`. Fill in API keys and toggle `mock_response` flags. When `mock_response = True`, tests load JSON fixtures from `tests/resources/mock/{interaction}/` instead of calling live APIs.

## Architecture

**cyhole** wraps crypto APIs (Birdeye, Jupiter, SolanaFM, Solscan) as *Interactions*. Each Interaction exposes both sync and async clients.

### Core layer (`src/cyhole/core/`)

- `interaction.py`: Base `Interaction` class. Owns `client` (sync) and `async_client` (async). Has `api_return_model()` helper that dispatches to the right client based on `sync: bool`.
- `client.py`: `APIClient` (uses `requests`) and `AsyncAPIClient` (uses `aiohttp`, context-manager required for async). Both implement `api(type, url, ...)` → `requests.Response`.
- `param.py`: `CyholeParam` (base `Enum`), `RequestType` (GET/POST).
- `exception.py`: `CyholeException` base + specific errors.

### Interaction modules (`src/cyhole/{name}/`)

Required files per interaction: `__init__.py`, `client.py`, `exception.py`, `interaction.py`, `param.py`, `schema.py`.

**Call flow for every endpoint:**

```
user → interaction.client.get_foo()        # sync
     → interaction._get_foo(sync=True)     # private method on Interaction subclass
     → client.api(GET, url, ...)           # APIClient
     → FooResponse(**response.json())      # pydantic model

user → async with interaction.async_client as c: await c.get_foo()   # async
     → interaction._get_foo(sync=False)    # returns Coroutine
     → async_client.api(GET, url, ...)     # AsyncAPIClient
     → FooResponse(**response.json())
```

**Naming conventions:**

| Artifact | Convention |
|---|---|
| Private method on Interaction | `_get_endpoint_name` |
| Public method on sync client | `get_endpoint_name` |
| Public method on async client | `async get_endpoint_name` |
| Response schema | `GetEndpointNameResponse` |
| POST body schema | `PostEndpointNameBody` |
| Param enum | `{Name}ParamName` |
| Exception base | `{Name}Exception` |

**Overload pattern** — every private method requires two `@overload` declarations:

```python
@overload
def _get_foo(self, sync: Literal[True]) -> FooResponse: ...
@overload
def _get_foo(self, sync: Literal[False]) -> Coroutine[None, None, FooResponse]: ...
def _get_foo(self, sync: bool) -> FooResponse | Coroutine[None, None, FooResponse]:
    return self.api_return_model(sync, RequestType.GET.value, url, FooResponse, ...)
```

### Tests (`tests/`)

- `config.py` + `test.default.ini`: central config loader (`load_config()`) and `MockerManager` for JSON fixture handling.
- Each interaction has `test_{name}.py`. Tests group into classes; each endpoint needs `_sync` and `_async` variants.
- Sync mock: `mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)`
- Async mock: `mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)`
- Mock JSON files live in `tests/resources/mock/{name}/{endpointMethodName}_{info}.json`.

## Coding Standards

- Python 3.12+. All code fully typed. Use `list`/`dict`/`str | None` — not `List`/`Dict`/`Optional`.
- All classes, methods, and functions need docstrings with `Parameters`, `Returns`, `Raises` sections (mkdocs-compatible).
- Operators surrounded by spaces: `x = 1`, not `x=1`.
- If endpoint takes >3 inputs, define a `Body` pydantic model instead of individual params.

## Adding a New Interaction

1. Create `src/cyhole/{name}/` with 6 required files.
2. Add `{name}` section to `tests/test.default.ini` with `mock_response` and `mock_folder`.
3. Extend `tests/config.py` for the new interaction.
4. Create `tests/test_{name}.py` and `tests/resources/mock/{name}/` fixture folder.
5. Create `docs/interactions/{name}/` with 6 markdown files.
6. Register in `mkdocs.yml` under `nav.Interactions`.
