---
name: cyhole-interaction-creation
description: >
  Use this skill when implementing a new crypto API Interaction in the cyhole library.
  Trigger whenever the user says "add a new interaction", "implement [API name] interaction",
  "integrate [API name]", "create [API name] connector", or similar requests to wrap a new
  external crypto/blockchain API. Also trigger when the user provides an API documentation URL
  and asks to connect it to cyhole. This skill enforces all cyhole conventions (file structure,
  naming, overload pattern, tests, docs) and prevents duplicate work. Do NOT skip this skill
  even for "simple" single-endpoint APIs — the conventions must be applied consistently.
---

# cyhole New Interaction Skill

This skill guides the full implementation of a new `Interaction` in the cyhole library —
from research and branch creation through code, tests, and documentation.

## Step 0: Gather Requirements

Before touching code, collect the following from the user (ask if not provided):

1. **API documentation URL** — required. Fetch it with WebFetch to understand available endpoints.
2. **Interaction name** — the canonical lowercase identifier (e.g. `birdeye`, `jupiter`, `solscan`). Usually the site/service name.
3. **Which endpoints** to implement (or "all available").

Once you have these, proceed sequentially through the steps below.

---

## Step 1: Check for Duplicate Work

Before creating anything, verify the interaction is not already implemented:

```bash
ls src/cyhole/
```

If a folder matching `{name}` already exists → tell the user and stop. Do not re-implement.

---

## Step 2: Research the API

Use `WebFetch` on the provided documentation URL. For each endpoint, extract:

- HTTP method (GET / POST / …)
- Path
- Required and optional query/body parameters — note types and allowed values
- Response JSON shape (field names, types, nesting)
- **Authentication** — does it require an API key? Where (header, query param)? Is there a free tier?
- Rate limits and API tiers if mentioned

Document your findings in a compact internal summary before proceeding.

---

## Step 3: Create the Branch

Branch naming: `{name}-new-interaction`

```bash
git checkout -b {name}-new-interaction
```

---

## Step 4: Create the File Structure

Create the following (empty for now — fill in Step 5):

```
src/cyhole/{name}/
    __init__.py
    client.py
    exception.py
    interaction.py
    param.py
    schema.py

tests/resources/mock/{name}/
    (mock JSON files, one per endpoint — fill in Step 6)

docs/interactions/{name}/
    client.md
    exception.md
    index.md
    interaction.md
    param.md
    schema.md
```

---

## Step 5: Implement Core Files

Implement all six files following the conventions below exactly.

### `exception.py`

```python
from ..core.exception import CyholeException

class {Name}Exception(CyholeException):
    """Base exception for {Name} interaction."""
    pass

# Add specific exceptions as needed, inheriting from {Name}Exception
```

### `param.py`

For every endpoint parameter with a fixed value set, create an Enum:

```python
from ..core.param import CyholeParam

class {Name}{ParamName}(CyholeParam):
    """Docstring describing the param."""
    VALUE_A = "value_a"
    VALUE_B = "value_b"
```

If no fixed-value params exist, keep the file with just the import and a comment.

### `schema.py`

One Pydantic model per endpoint response + one per POST body (or query bag — see below).

Naming:
- Response: `{RequestType}{EndpointName}Response` (CamelCase, e.g. `GetPriceResponse`)
- POST body: `Post{EndpointName}Body`
- GET query bag (when an endpoint has >3 query params): `Get{EndpointName}Query`
- Sub-schemas: descriptive CamelCase names, no `Response`/`Body`/`Query` suffix

If `schema.py` is going to grow large from day one (10+ endpoints with many sub-schemas, or several distinct API domains), start directly with a `schema/` sub-package as described in CLAUDE.md → "Scaling patterns for large interactions" rather than building a monolithic `schema.py` you'll have to split later.

Rules:
- All models inherit from `pydantic.BaseModel`
- Use `list[X]` / `dict[K, V]` / `str | None`, never `List` / `Dict` / `Optional`
- Use `Field(alias="originalName")` when JSON field names differ from Python naming conventions
- **Every class needs a functional docstring.** `cyhole` is a user-facing library — the docstring must explain what the schema represents (e.g. "Response payload from the `getAssetsByOwner` DAS endpoint, containing the paginated list of assets owned by the wallet"). A one-line restatement of the class name is NOT enough.
- **Field-level documentation uses the `Attributes:` section** (Google-style). Never use `Parameters:` for a pydantic BaseModel — griffe interprets `Parameters:` as the function/`__init__` signature and emits "Parameter X does not appear in the function signature" warnings that abort `mkdocs build --strict`. Each documented field must describe its meaning, units (if any), and the condition under which it is `None` (for optional fields).

```python
class GetFooResponse(BaseModel):
    """
    Response payload from the `getFoo` endpoint.

    Attributes:
        price: token price in USD; `None` when the API has no recent quote.
        last_updated: unix timestamp (seconds) of the latest quote.
    """
    price: float | None = None
    last_updated: int
```

### `interaction.py`

```python
from typing import Any, Coroutine, overload, Literal
from ..core.param import RequestType
from ..core.interaction import Interaction, ResponseModel
from ..{name}.client import {Name}Client, {Name}AsyncClient
from ..{name}.schema import ...   # import all response/body schemas
from ..{name}.param import ...    # import all param enums
from ..{name}.exception import {Name}Exception, ...

class {Name}(Interaction):
    """
    Class used to connect [{Name}]({api_url}) API.

    [Auth info: "No API key required." or "Requires an API key passed as X-API-KEY header."]

    **Example**

    ```python
    from cyhole.{name} import {Name}

    {name_lower} = {Name}()
    response = {name_lower}.client.get_something()
    ```
    """

    def __init__(self, api_key: str | None = None, headers: Any | None = None) -> None:
        # Only include api_key param if the API requires authentication
        super().__init__(headers)
        self.client = {Name}Client(self)
        self.async_client = {Name}AsyncClient(self)
        self.url_api = "https://api.{name}.com/"  # replace with actual base URL

    # --- Per endpoint: overloads + implementation ---

    @overload
    def _{request_type}_{endpoint_name}(self, sync: Literal[True], ...) -> {Response}Model: ...

    @overload
    def _{request_type}_{endpoint_name}(self, sync: Literal[False], ...) -> Coroutine[None, None, {Response}Model]: ...

    def _{request_type}_{endpoint_name}(self, sync: bool, ...) -> {Response}Model | Coroutine[None, None, {Response}Model]:
        """
        This function refers to the **{EndpointName}** API endpoint.

        [One-or-two-sentence functional description: what this endpoint returns, what
        it is useful for, and any important caveats — e.g. pagination defaults, rate
        limits, or units of returned values. Do NOT just restate the endpoint name.]

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            ...: each param described with its meaning, units, default, and the
                 enum it must come from (if a fixed-value param).

        Returns:
            {Response}Model: description of the response payload — call out the
                              key fields a caller is most likely to use.

        Raises:
            {Name}Exception: if the API returns an error.
        """
        url = self.url_api + "endpoint/path"
        # Build params dict or body as needed
        return self.api_return_model(sync, RequestType.GET.value, url, {Response}Model, params=params)
```

**Key rules:**
- Every endpoint = one private method `_{get|post|...}_{endpoint_name}` on the `Interaction` class
- Always two `@overload` declarations before the real method
- Use `self.api_return_model(sync, ...)` for the dispatch — never call `client.api()` directly inside `interaction.py`, and do **not** write the manual `if sync: ... else: async def async_request(): ...` ladder. The helper takes `(sync, type, url, response_model, *args, **kwargs)` and forwards every keyword to `client.api()`, so `params=`, `json=`, `headers=` all work as expected:
  ```python
  return self.api_return_model(sync, RequestType.POST.value, url, FooResponse, json = body.model_dump(exclude_none = True), headers = headers)
  ```
- If the endpoint takes more than ~3 meaningful inputs, define a Pydantic model and accept it as a single argument: `Post{EndpointName}Body` for POST endpoints, `Get{EndpointName}Query` for GETs with many filters. Pass it via `json = body.model_dump(exclude_none = True)` (POST) or `params = query.model_dump(exclude_none = True)` (GET). `exclude_none = True` keeps unset filters out of the request.
- **Consolidate single + multiple endpoint pairs.** When the API exposes a sibling pair like `.../single` and `.../multiple` whose only delta is input cardinality and response shape, expose them as one polymorphic cyhole method with `address: str | list[str]` (or equivalent). Four overloads — `(sync=True, str)`, `(sync=True, list[str])`, `(sync=False, str)`, `(sync=False, list[str])` — narrow the return type for callers. Routing inside the method picks the URL and response model based on `isinstance(address, str)`. Define distinct `…Response` and `…MultipleResponse` schemas (the payload shapes differ). This pattern works even when the two endpoints use different HTTP verbs (GET single + POST batch). See CLAUDE.md → "Scaling patterns for large interactions" for the full example.
- Authentication: add API key to headers in `__init__` if required
- **The functional description on the private method docstring is mandatory.** `cyhole` is a user-facing library and this docstring is what end-users see in the mkdocs site. Public client methods are intentionally thin wrappers; users land on the private method's docs via the cross-reference link. If the description is missing or just restates the name, the endpoint is not done.

### `client.py`

```python
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from ..core.client import APIClient, AsyncAPIClient
from ..{name}.schema import ...

if TYPE_CHECKING:
    from ..{name}.interaction import {Name}

class {Name}Client(APIClient):
    """Client for synchronous API calls for `{Name}` interaction."""

    def __init__(self, interaction: {Name}, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: {Name} = self._interaction

    def {endpoint_name}(self, ...) -> {Response}Model:
        """
        Call the {Name}'s {RequestType} **[{EndpointName}]({doc_url})** API endpoint for synchronous logic.
        All the API endpoint details are available on [`{Name}._{method_name}`][cyhole.{name}.interaction.{Name}._{method_name}].
        """
        return self._interaction._{method_name}(True, ...)

class {Name}AsyncClient(AsyncAPIClient):
    """Client for asynchronous API calls for `{Name}` interaction."""

    def __init__(self, interaction: {Name}, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: {Name} = self._interaction

    async def {endpoint_name}(self, ...) -> {Response}Model:
        """
        Call the {Name}'s {RequestType} **[{EndpointName}]({doc_url})** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`{Name}._{method_name}`][cyhole.{name}.interaction.{Name}._{method_name}].
        """
        return await self._interaction._{method_name}(False, ...)
```

**For consolidated single/multiple endpoints**, mirror the polymorphic overloads on both sync and async client wrappers so callers get a narrowed return type:

```python
@overload
def get_v3_token_meta_data(self, address: str) -> GetV3TokenMetaDataResponse: ...

@overload
def get_v3_token_meta_data(self, address: list[str]) -> GetV3TokenMetaDataMultipleResponse: ...

def get_v3_token_meta_data(self, address: str | list[str]) -> GetV3TokenMetaDataResponse | GetV3TokenMetaDataMultipleResponse:
    """…thin wrapper…"""
    return self._interaction._get_v3_token_meta_data(True, address)
```

### `__init__.py`

```python
from ..{name}.interaction import {Name}

__all__ = [
    "{Name}"
]
```

---

## Step 6: Create Mock JSON Files and Tests

### Mock JSON files

For each endpoint, you need a real or representative JSON response saved to:
`tests/resources/mock/{name}/{endpointMethodName}_{info}.json`

Naming: `{endpointMethodName}` = the public client method name in camelCase, e.g. `getPrice_default.json`.

**If the API requires no authentication**, generate mock files directly from live API responses on the first test run:

1. In `tests/test.ini` set in `[global]`: `mock_file_overwrite = True`
2. In `tests/test.ini` set in `[{name}]`: `mock_response = False`
3. Run `pytest tests/test_{name}.py -v` — tests hit the real API and store responses as JSON fixtures
4. Reset `mock_file_overwrite = False` in `[global]` for subsequent runs

This ensures mock files contain actual latest API responses, not hand-crafted approximations.

**If the API requires authentication** (or live calls are not possible), construct a minimal valid JSON
that matches the response schema. Every field in the Pydantic model must appear in the mock.

### `tests/config.py` — add configuration class

Add a new configuration class and integrate it:

```python
class {Name}Configuration(BaseModel):
    """Model in charge to manage the {Name} APIs."""
    mock_response: bool = True
    mock_folder: str = "{name}"
    # Add api_key field only if the API requires authentication:
    # api_key: str | None = None
```

Add `{name}: {Name}Configuration = {Name}Configuration()` to `TestConfiguration`.

Add loading block in `load_config()`:
```python
test_config.{name}.mock_response = config.getboolean("{name}", "mock_response", fallback=test_config.{name}.mock_response)
test_config.{name}.mock_folder = config.get("{name}", "mock_folder", fallback=test_config.{name}.mock_folder)
# Add api_key loading if required
```

### `tests/test.default.ini` — add section

```ini
[{name}]
# configuration for {name} integration
mock_response = True
mock_folder = {name}
# api_key = {{NAME_API_KEY}}   # uncomment if needed
```

### `tests/test_{name}.py`

```python
import pytest
from pathlib import Path
from pytest_mock import MockerFixture

from cyhole.{name} import {Name}
from cyhole.{name}.schema import {Response}Model

from .config import load_config, MockerManager
config = load_config()

mock_path = Path(config.mock_folder) / config.{name}.mock_folder
mock_path.mkdir(parents=True, exist_ok=True)

class Test{Name}:
    """Class grouping all unit tests for {Name} interaction."""
    {name_lower} = {Name}()
    mocker = MockerManager(mock_path)

    def test_{endpoint_name}_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "{EndpointName}" — synchronous logic.

        Mock Response File: {mock_file}.json
        """
        mock_file_name = "{mock_file}"
        if config.mock_response or config.{name}.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, {Response}Model)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.{name_lower}.client.{endpoint_name}(...)
        assert isinstance(response, {Response}Model)

        if config.mock_file_overwrite and not config.{name}.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_{endpoint_name}_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "{EndpointName}" — asynchronous logic.

        Mock Response File: {mock_file}.json
        """
        mock_file_name = "{mock_file}"
        if config.mock_response or config.{name}.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, {Response}Model)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.{name_lower}.async_client as client:
            response = await client.{endpoint_name}(...)
        assert isinstance(response, {Response}Model)
```

Rules:
- Every endpoint needs `_sync` and `_async` test variants
- Mock patch target: `"cyhole.core.client.APIClient.api"` (sync) / `"cyhole.core.client.AsyncAPIClient.api"` (async)
- Check `config.mock_response or config.{name}.mock_response` before patching

---

## Step 7: Create Documentation Files

### `docs/interactions/{name}/client.md`
```markdown
# Client

::: cyhole.{name}.client
```

### `docs/interactions/{name}/exception.md`
```markdown
# Exceptions

::: cyhole.{name}.exception
```

### `docs/interactions/{name}/interaction.md`
```markdown
# Interaction

::: cyhole.{name}.{Name}
    options:
        filters:
            - "^_"
```

**Critical:** Reference the class directly (not the module) and include `filters: ["^_"]` to expose private methods. Without this, cross-reference links from `client.py` docstrings will generate mkdocs warnings and broken anchors.

### `docs/interactions/{name}/param.md`
```markdown
# Parameters

Some endpoints require input parameters belonging to specific domains.  
On this page, all domains can be found in order to be in line with the standards required by the API.

::: cyhole.{name}.param
```

### `docs/interactions/{name}/schema.md`
```markdown
---
toc_depth: 3
---
# Response Schema

Each response has been mapped into a `pydantic` schema in a way that makes it easy to read and write codes that use them.

The classes identifying the response schema of an endpoint are the only ones ending with `Response` word, all other sub-schemes are used to identify the structures obtained from the responses.

::: cyhole.{name}.schema
    options:
        show_if_no_docstring: true
```

### `docs/interactions/{name}/index.md`

Structure:
````markdown
# :simple-{icon}: - {Name}

{Name} ([{api_url}]({api_url})) is ... [brief description].
[Authentication: "No API key is required." or "Authenticated endpoints require a Bearer token passed as `api_key` to the `{Name}` constructor."]

The API connector is [`{Name}`](../{name}/interaction.md) class imported from `cyhole.{name}` path.

## Quick Examples

### {Example Endpoint Title}

[Short description of what the example does.]

```python
from cyhole.{name} import {Name}
# ... example code using sync or async client
```

## Content

The documentation follows the library's structure by providing all the technical details required to use it.

<div class="grid cards" markdown>

-   :material-connection:{ .lg .middle } __Connector__

    ---

    `cyhole.{name}` - Explore the [`{Name}`](../{name}/interaction.md) API connector and all its methods.

    [:octicons-arrow-right-24: Reference](../{name}/interaction.md)

-   :material-list-status:{ .lg .middle } __API Parameters__

    ---

    `cyhole.{name}.param` - Ensure to use the correct parameters during the API calls.

    [:octicons-arrow-right-24: Reference](../{name}/param.md)

-   :material-graph:{ .lg .middle } __Response Schema__

    ---

    `cyhole.{name}.schema` - Extract only what is necessary by exploiting response mapping thanks to `pydantic` schemes.

    [:octicons-arrow-right-24: Reference](../{name}/schema.md)

-   :octicons-stop-24:{ .lg .middle } __Exceptions__

    ---

    `cyhole.{name}.exception` - Make sure you intercept all exceptions correctly.

    [:octicons-arrow-right-24: Reference](../{name}/exception.md)

</div>

## Endpoints

| Endpoint | Type | Method | `cyhole` Release | Deprecated |
| --- | --- | --- | --- | --- |
| {EndpointName} | `GET` | [`get_{endpoint_name}`](../{name}/interaction.md#cyhole.{name}.{Name}._{get_endpoint_name}) | `{version}` | - |
````

**Important:**
- Use `<div class="grid cards" markdown>` for the Content section — not a plain table.
- The Endpoints table must link to the private method anchors in `interaction.md` (e.g., `#cyhole.{name}.{Name}._get_{endpoint_name}`).
- List every endpoint in the table with its HTTP type, cyhole release version, and Deprecated column.

### `README.md` — add to interactions table

Find the interactions table and add a row for the new interaction (keep alphabetical or logical order):

```markdown
|[{site}]({api_url}) |`cyhole.{name}` |[`{Name}`](https://zazza123.github.io/cyhole/interactions/{name}/index.html) |
```

### `mkdocs.yml` — register new interaction

Find the `nav:` → `Interactions:` section and add:

```yaml
- {Name}:
  - interactions/{name}/index.md
  - Client: interactions/{name}/client.md
  - Interaction: interactions/{name}/interaction.md
  - Parameters: interactions/{name}/param.md
  - Schema: interactions/{name}/schema.md
  - Exceptions: interactions/{name}/exception.md
```

---

## Step 8: Run Tests, Lint, and Docs Build

These three checks are mandatory — do not skip any of them, and do not declare the task done until all three are clean.

```bash
# 1. Tests must pass with mock responses
pytest tests/test_{name}.py -v

# 2. Lint must be clean for the new code
ruff check src/

# 3. Docs build must succeed in strict mode (zero WARNINGs, zero ERRORs)
mkdocs build --strict
```

Fix every issue before proceeding. Common failures:
- `ruff` flags: unused imports left from scaffolding, unsorted imports, missing newlines.
- `mkdocs --strict` failures:
  - Pydantic class docstrings using `Parameters:` instead of `Attributes:` → 76-style griffe warnings per class.
  - Cross-references in `client.py` docstrings pointing to a private `_method` while `interaction.md` uses module-level `:::` without `filters: ["^_"]` → broken anchors.
  - Missing entries in `mkdocs.yml` `nav:` for the new interaction.

---

## Step 9: Final Checklist

Before declaring the implementation complete, verify:

- [ ] All 6 source files created in `src/cyhole/{name}/`
- [ ] `__init__.py` exports only the main class
- [ ] Every endpoint has `@overload` × 2 + implementation (× 4 for consolidated single/multiple endpoints)
- [ ] `api_return_model` used (no raw `client.api()` and no manual sync/async ladder in interaction.py)
- [ ] Endpoints with >3 params use a `Post{Name}Body` (POST) or `Get{Name}Query` (GET) Pydantic model, serialised with `model_dump(exclude_none = True)`
- [ ] Sibling `.../single` and `.../multiple` endpoints consolidated under one polymorphic method with `str | list[str]` argument; sync + async clients mirror the overloads for narrowed return types
- [ ] If `schema.py` grows large or covers multiple domains, use a `schema/` sub-package per CLAUDE.md → "Scaling patterns for large interactions"
- [ ] All Pydantic models have docstrings, and field-level docs use `Attributes:` (never `Parameters:`)
- [ ] Every private endpoint method (`_{verb}_{name}`) has a true functional description (what the endpoint returns, why a user would call it), not just a name restatement
- [ ] Every documented field on a response/body schema describes meaning, units, and `None` conditions
- [ ] Param enums inherit from `CyholeParam`
- [ ] Exception hierarchy: `{Name}Exception` → `CyholeException`
- [ ] Mock JSON files created for every endpoint
- [ ] `tests/config.py` updated (new config class + loading block)
- [ ] `tests/test.default.ini` updated with new section
- [ ] `tests/test_{name}.py` has `_sync` and `_async` test for each endpoint
- [ ] All 6 doc files created in `docs/interactions/{name}/`
- [ ] `interaction.md` uses class-level `:::` with `filters: ["^_"]` (not module-level)
- [ ] `index.md` uses grid cards for Content section and full Endpoints table with all methods
- [ ] `mkdocs.yml` updated under `nav: Interactions:`
- [ ] `README.md` interactions table updated with new row for `{name}`
- [ ] `ruff check src/` is clean
- [ ] `mkdocs build --strict` runs with zero WARNINGs and zero ERRORs
- [ ] `pytest tests/test_{name}.py` passes

---

## Reference: Naming Quick-Reference

| Artifact | Pattern | Example |
|---|---|---|
| Interaction class | `{Name}` | `Jupiter` |
| Sync client | `{Name}Client` | `JupiterClient` |
| Async client | `{Name}AsyncClient` | `JupiterAsyncClient` |
| Private method | `_{get\|post}_{endpoint_name}` | `_get_price` |
| Public method (both clients) | `{get\|post}_{endpoint_name}` | `get_price` |
| Response schema | `{RequestType}{EndpointName}Response` | `GetPriceResponse` |
| POST body schema | `Post{EndpointName}Body` | `PostSwapBody` |
| Param enum | `{Name}{ParamName}` | `JupiterApiTier` |
| Exception base | `{Name}Exception` | `JupiterException` |
| Branch | `{name}-new-interaction` | `jupiter-new-interaction` |
| Mock file | `{endpointMethodName}_{info}.json` | `getPrice_default.json` |
| Test class | `Test{Name}` | `TestJupiter` |
