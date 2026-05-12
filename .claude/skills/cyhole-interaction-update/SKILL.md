---
name: cyhole-interaction-update
description: >
  Use this skill when updating an existing cyhole Interaction to reflect API changes.
  Trigger whenever the user says "update [API name] interaction", "[API name] API changed",
  "add endpoint to [API name]", "remove deprecated endpoint from [API name]",
  "[API name] now requires an API key", "sync [API name] with latest docs", or similar requests
  to evolve an already-implemented Interaction. Also trigger when the user provides a new
  documentation URL for an API that is already in cyhole. Do NOT skip this skill even for
  "small" changes like adding one endpoint or updating one schema — conventions must be
  applied consistently.
---

# cyhole Interaction Update Skill

This skill guides the full update of an existing `Interaction` in the cyhole library when
API changes occur — new endpoints, deprecated endpoints, schema changes, authentication
changes, or structural reorganisation.

## Step 0: Gather Requirements

Before touching code, collect (ask if not provided):

1. **Interaction name** — the existing lowercase identifier (e.g. `jupiter`, `birdeye`).
2. **API documentation URL** — required. Fetch it to understand the current API surface.
3. **Release version** — the cyhole version this update ships in (e.g. `0.4.0`). Used to
   populate `index.md` endpoint table entries.
4. **Changes summary** — if the user already knows what changed (new endpoint X, deprecated
   endpoint Y, auth key added, etc.) accept their description. Otherwise detect changes in
   Step 2.

---

## Step 1: Audit the Current Implementation

Read the existing interaction to build a baseline inventory:

```bash
# list source files
ls src/cyhole/{name}/

# list all public methods (current endpoint set)
grep -n "def " src/cyhole/{name}/client.py

# read the endpoints table for deprecation/release history
# (look at docs/interactions/{name}/index.md, section ## Endpoints)
```

Document:
- All currently implemented endpoints (method name, HTTP type)
- Whether authentication is already wired (`api_key` in `__init__`, headers)
- Current base URL (`self.url_api`)

---

## Step 2: Research the New API State

Fetch the provided documentation URL with `WebFetch`. For every endpoint in the docs extract:

- HTTP method and path
- Required and optional parameters (types, allowed values, defaults)
- Response JSON shape (field names, types, nesting)
- Authentication requirements (header name, query param, format)
- Any structural changes (base URL, versioning prefix)

Then compare docs vs. baseline inventory to produce a **change list**:

| Endpoint | Change type | Notes |
|---|---|---|
| `get_foo` | **modified** | New optional param `bar` added |
| `get_baz` | **deprecated** | Removed from API |
| `post_new` | **new** | New endpoint |
| *(none)* | **auth added** | API now requires `X-API-KEY` header |

If the user already supplied the change list, skip the diff and accept it directly.

---

## Step 3: Create the Branch

```bash
git checkout -b {name}-interaction-update
```

---

## Step 4: Apply Changes — Cycle Over the Change List

Work through each item in the change list. The three change types each have their own
procedure below. Apply them sequentially.

---

### 4a — Deprecated Endpoint

An endpoint is **deprecated** when the API no longer provides it.

**Remove from `interaction.py`:**

- Delete the two `@overload` declarations and the implementation for `_{method_name}`.

**Remove from `client.py`:**

- Delete the sync `{method_name}` method from `{Name}Client`.
- Delete the async `{method_name}` method from `{Name}AsyncClient`.

**Remove from `schema.py`:**

- Delete the response model `{RequestType}{EndpointName}Response`.
- Delete any sub-schemas used *exclusively* by that endpoint (check no other endpoint imports them).

**Remove from `param.py`:**

- Delete any param enums used *exclusively* by that endpoint.

**Remove tests and mock files:**

- Delete `tests/test_{name}.py` test methods `test_{endpoint_name}_sync` and `test_{endpoint_name}_async`.
- Delete `tests/resources/mock/{name}/{endpointMethodName}_*.json` fixture files.

**Update `docs/interactions/{name}/index.md` — Endpoints table:**

- Keep the row in the table.
- Remove the hyperlink from the Method column (leave plain text method name).
- Fill the `Deprecated` column with the release version (e.g. `0.4.0`).

Example before:
```
| Foo | `GET` | [`get_foo`](../jupiter/interaction.md#cyhole.jupiter.Jupiter._get_foo) | `0.1.0` | - |
```
After deprecation in `0.4.0`:
```
| Foo | `GET` | `get_foo` | `0.1.0` | `0.4.0` |
```

---

### 4b — Modified Endpoint

An endpoint is **modified** when its parameters or response shape changes.

**Update `schema.py`:**

- Add new response fields. Use `str | None = None` for optional fields added mid-lifecycle.
- Remove fields that no longer appear in the API response (confirm they are truly gone).
- Update field types if the API changed them.
- Add new param enums to `param.py` for any new fixed-value parameters.
- Preserve all docstrings and add descriptions for any new fields — explain what the
  field represents, its units, and any edge cases (e.g. `None` when not applicable).
  `cyhole` is a user-facing library, so this functional description is what end-users
  actually consume in the docs site — it is not optional.
- Field-level docs go under the Google-style `Attributes:` section, **never** `Parameters:`.
  Griffe interprets `Parameters:` as a function/`__init__` signature and emits
  "Parameter X does not appear in the function signature" warnings that abort
  `mkdocs build --strict`. If you encounter an existing class that uses `Parameters:`
  for its fields, fix it as part of this update.

**Update `interaction.py`:**

- Add or remove parameters from the private method signature (maintain the overload pattern).
- Update the `params` / body dict to include new params or drop removed ones.
- If a new param has fixed allowed values, use the new `{Name}{ParamName}` enum from `param.py`.
- Update the docstring `Parameters` and `Returns` sections to reflect the change.

**Update `client.py`:**

- Mirror every signature change in both `{Name}Client.{method_name}` and
  `{Name}AsyncClient.{method_name}`.
- The client methods must match the private method's public-facing signature exactly.

**Update tests and mock files:**

- If new params were added, add representative calls in the test.
- If the response shape changed, update the mock JSON file to match the new schema
  (all Pydantic model fields must be present in the fixture).
- Re-run tests to confirm mock responses deserialise correctly.

**Update `docs/interactions/{name}/index.md`:**

- No table change needed for a modified endpoint (release version and Deprecated column stay).

---

### 4c — New Endpoint

A new endpoint follows the same conventions as creating an endpoint in a brand-new
Interaction. Apply these steps:

**`schema.py` — add response model (and sub-schemas):**

- Name: `{RequestType}{EndpointName}Response` (e.g. `GetRecurringOrdersResponse`).
- Every field must have a concise docstring explaining what it represents, its units, and
  when it is `None`.
- Use `Field(alias="originalName")` when JSON keys differ from Python naming style.
- Nest sub-schemas for complex structures; name them descriptively without a `Response` suffix.
- For POST endpoints with >3 inputs, define a `Post{EndpointName}Body` model.

**`param.py` — add param enums (if needed):**

- One enum per fixed-value parameter domain.
- Name: `{Name}{ParamName}` (e.g. `JupiterRecurringType`).
- Document each enum member: what it means in the API context.

**`interaction.py` — add the overload + implementation:**

```python
@overload
def _{request_type}_{endpoint_name}(self, sync: Literal[True], ...) -> {Response}Model: ...

@overload
def _{request_type}_{endpoint_name}(self, sync: Literal[False], ...) -> Coroutine[None, None, {Response}Model]: ...

def _{request_type}_{endpoint_name}(self, sync: bool, ...) -> {Response}Model | Coroutine[None, None, {Response}Model]:
    """
    This function refers to the **{EndpointName}** API endpoint.

    [One-or-two-sentence functional description: what this endpoint returns, what it is
    useful for, and any important caveats — e.g. pagination defaults, rate limits, units
    of returned values. Do NOT just restate the endpoint name. This docstring is what
    end-users see in the mkdocs site since public client methods are intentionally thin
    wrappers that link here.]

    Parameters:
        sync: if True run synchronously, else return a coroutine.
        ...: [each param with type, description, units/default, and valid values
              or enum reference]

    Returns:
        {Response}Model: [description of the response, calling out the key fields
                          a caller is most likely to use]

    Raises:
        {Name}Exception: if the API returns an error.
    """
    url = self.url_api + "endpoint/path"
    return self.api_return_model(sync, RequestType.{TYPE}.value, url, {Response}Model, params=params)
```

**`client.py` — add sync and async methods:**

```python
def {endpoint_name}(self, ...) -> {Response}Model:
    """
    Call the {Name}'s {RequestType} **[{EndpointName}]({doc_url})** API endpoint for synchronous logic.
    All the API endpoint details are available on [`{Name}._{method_name}`][cyhole.{name}.interaction.{Name}._{method_name}].
    """
    return self._interaction._{method_name}(True, ...)

async def {endpoint_name}(self, ...) -> {Response}Model:
    """
    Call the {Name}'s {RequestType} **[{EndpointName}]({doc_url})** API endpoint for asynchronous logic.
    All the API endpoint details are available on [`{Name}._{method_name}`][cyhole.{name}.interaction.{Name}._{method_name}].
    """
    return await self._interaction._{method_name}(False, ...)
```

**Mock JSON files:**

- Create `tests/resources/mock/{name}/{endpointMethodName}_{info}.json`.
- If the API has no authentication, generate from live API (see Step 6 in
  `cyhole-interaction-creation` for the `mock_file_overwrite` workflow).
- If authentication is required, hand-craft a minimal valid JSON matching every field in the schema.

**Tests — add sync + async:**

```python
def test_{endpoint_name}_sync(self, mocker: MockerFixture) -> None:
    """Unit Test for endpoint "{EndpointName}" — synchronous logic.

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
    """Unit Test for endpoint "{EndpointName}" — asynchronous logic.

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

**Update `docs/interactions/{name}/index.md` — Endpoints table:**

Add a new row with the current release version and `-` in Deprecated:

```
| {EndpointName} | `GET` | [`{method_name}`](../{name}/interaction.md#cyhole.{name}.{Name}._{method_name}) | `{version}` | - |
```

---

### 4d — API-Level Structural Changes

These affect the entire interaction, not a single endpoint.

**Authentication added (API key required):**

In `interaction.py.__init__`:
- Add `api_key: str | None = None` parameter.
- Inject the key into headers (check the API docs for the exact header name):

```python
def __init__(self, api_key: str | None = None, headers: Any | None = None) -> None:
    super().__init__(headers)
    if api_key:
        self._headers["X-API-KEY"] = api_key  # replace with actual header name
    self.client = {Name}Client(self)
    self.async_client = {Name}AsyncClient(self)
```

Update the class docstring in `interaction.py` to document the new auth requirement.

Update `docs/interactions/{name}/index.md` intro paragraph to state that an API key is now required and how to pass it.

Update `tests/config.py`:
- Add `api_key: str | None = None` to `{Name}Configuration`.
- Add loading in `load_config()`:

```python
test_config.{name}.api_key = config.get("{name}", "api_key", fallback=None)
```

Update `tests/test.default.ini` — add the commented api_key line:

```ini
[{name}]
# api_key = {NAME_API_KEY}
```

Update the test class to pass the key when constructing the interaction:
```python
{name_lower} = {Name}(api_key=config.{name}.api_key)
```

**Base URL changed:**

Update `self.url_api` in `interaction.py.__init__` and verify all endpoint path strings
are still correct relative to the new base.

---

## Step 5: Run Tests, Lint, and Docs Build

These three checks are mandatory — do not skip any of them, and do not declare the task done until all three are clean.

```bash
# 1. Tests must pass with mock responses
pytest tests/test_{name}.py -v

# 2. Lint must be clean for the modified code
ruff check src/

# 3. Docs build must succeed in strict mode (zero WARNINGs, zero ERRORs)
mkdocs build --strict
```

Fix every issue before proceeding. Common failures:
- `ruff` flags: imports left behind by removing a deprecated endpoint (schemas, enums, exceptions no longer referenced); unused helper variables.
- `mkdocs --strict` failures:
  - Pydantic class docstrings using `Parameters:` instead of `Attributes:` for fields.
  - Cross-reference links in `client.py` or `index.md` pointing to a method that was deprecated/renamed.
  - `index.md` endpoint table row still linking to a now-removed private method anchor.

---

## Step 6: Final Checklist

- [ ] Change list fully processed — no skipped items
- [ ] **Deprecated**: method gone from `interaction.py`, `client.py`, `schema.py`, `param.py`, tests, mock files; `index.md` row updated (no link, deprecation version filled)
- [ ] **Modified**: schema updated, overload signature updated, client signatures updated, mock JSON matches new schema, tests pass
- [ ] **New**: two `@overload` + implementation in `interaction.py`; sync + async in `client.py`; response model + sub-schemas in `schema.py`; param enums in `param.py` if needed; mock JSON created; `_sync` + `_async` tests added; `index.md` row added
- [ ] **Auth added**: `api_key` param in `__init__`, header injection, `config.py` + `test.default.ini` updated, test class updated, docs updated
- [ ] All Pydantic models have docstrings, and field-level docs use `Attributes:` (never `Parameters:`)
- [ ] Every documented field describes meaning, units, and `None` conditions
- [ ] Every new or modified private endpoint method (`_{verb}_{name}`) has a true functional description (what the endpoint returns, why a user would call it), not just a name restatement
- [ ] All param enum members have docstrings
- [ ] Overload pattern correct on every private method (two `@overload` + implementation)
- [ ] `api_return_model` used — no raw `client.api()` calls in `interaction.py`
- [ ] `ruff check src/` is clean
- [ ] `mkdocs build --strict` runs with zero WARNINGs and zero ERRORs
- [ ] `pytest tests/test_{name}.py` passes

---

## Reference: Naming Quick-Reference

| Artifact | Pattern | Example |
|---|---|---|
| Private method | `_{get\|post}_{endpoint_name}` | `_get_recurring_orders` |
| Public method (both clients) | `{get\|post}_{endpoint_name}` | `get_recurring_orders` |
| Response schema | `{RequestType}{EndpointName}Response` | `GetRecurringOrdersResponse` |
| POST body schema | `Post{EndpointName}Body` | `PostRecurringCreateOrderBody` |
| Param enum | `{Name}{ParamName}` | `JupiterRecurringType` |
| Mock file | `{endpointMethodName}_{info}.json` | `getRecurringOrders_default.json` |
| Branch | `{name}-interaction-update` | `jupiter-interaction-update` |
