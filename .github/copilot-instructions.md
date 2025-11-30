# Instructions

You are a python developer and you are working on developing cyhole library.  
Thi library is designed to help python's developers to interact to the most popular external API services in crypto and create automation processes.

During implementation you **must** the guidelines described below.

## Coding Guidelines

### Main

- All code should always typed using python type hints.
- Typyng should follow the modern python typing standards (e.g. use `list` instead of `List` from `typing` module).
- Do not use `Optional` from `typing` module, instead modern notation should be used (e.g. `str | None`).
- All objects (classes, functions, methods, variables) should have have docstrings describing their purpose and usage.
- Use docstrings aligned to `mkdocs` standards; in particular, use `Parameters`, `Returns`, and `Raises` sections where appropriate.
- Operators like `=`, `==`, `+`, etc. should be surrounded by a single space on both sides; for example: `x = 1` and not `x=1`.

### Library

- Library code should be inside `src/cyhole` folder.
- Every site (API provider) is identified as an "interaction" and it should have its own module inside `src/cyhole/{name}`.
- In the interaction's code folder there must be the following files:

  - __init__.py: the actual entry point in the library.
  - client.py: API client classes.
  - exception.py: dedicated exceptions.
  - interaction.py: interaction class.
  - param.py: possible parameters required by the endopints.
  - schema.py: response and body schemas to use in the endpoints.

  There could be other additional files if needed.

Below a details on the guidelines for each of the files.

#### `__init__.py`

This file should recall **only** the new `Interaction` class from the `interaction.py` file.

#### `interaction.py`

This is the most important file because the new `Interaction`'s class is defined here.

- The `Interaction` class **must** inherits from `cyhole.core.interaction.Interaction` class.
- The name of the interaction should refers univocally to the external API site; e.g. it is usually the site name.
- The attributes `client` and `async_client` are initiated inside the `__init__` method and defined in `client.py` file.
- Every endpoint is identified by **one private** method with the following assumptions:

  - The name should recall univocally the endpoint and the type of the request. The naming convention is `_{request_type}_{endpoint_name}`, where `{request_type}` reflects the request's type (get, post, ...) and `{endpoint_name}` recalls the name of the original endpoint.
  - The **first** parameter is called `sync` of type `bool` and is used to define the synchronous/asynchronous behavior of the method.
  - The output/input schema of an endpoint is defined by a `pydantic.BaseModel` inside the `schema.py` file.
  - The naming convention of an output/input schema should recall univocally the corresponding endpoint. The naming convention is `{request_type}{endpoint_name}Response/Body`, where `{request_type}` and `{endpoint_name}` recalls the name of the original endpoint, and they are concatenated using the camel case syntax.
  - To manage the `sync` and `async` behavior, the output of the method must be of type `{output_schema_response} | Coroutine[None, None, {output_schema_response}]`, where `{output_schema_response}` is the output schema.
  - Above the method definition is required to include two `@overload` definitions to specify the output type according to the value of `sync` parameter:

    - `True`: the output should be `{output_schema_response}`.
    - `False`: the output should be `Coroutine[None, None, {output_schema_response}]`.

#### `client.py`

In this file are defined the Clients used by the `Interaction` to perform the actual calls to the external API endpoints.

- An `Interaction` requires two Clients:

  - The Client in charge to perform the **synchronous** logic must inherits from `cyhole.core.client.APIClient`, and its name should follow the naming convention `{name}Client`, where `{name}` is the name of the new interaction.
  - The Client in charge to perform the **asynchronous** logic must inherits from `cyhole.core.client.AsyncAPIClient`, and its name should follow the naming convention `{name}AsyncClient`, where `{name}` is the name of the new interaction.

- As described in the previous section, every endpoint is identified inside the `Interaction` class by a private function. Since the clients are responsable for the *actual* interaction with the external API, it is required to implement on **both** clients, a **public** version of the method; one for `sync` logic and one for `async`. The method's name should be the same for both clients, and it must be equals the private method's name without the `_` prefix. Hence, we should obtain the following situation:
  - `_get_example` method defined in the `Interaction` class with the actual endpoint's logic.
  - `get_example` method defined inside the **synchronous** client and recalling the `_get_example` method with `sync` equals `True`.
  - `async get_example` method defined inside the **asynchronous** client and recalling the `_get_example` method with `sync` equals `False`.

### `schema.py`

Inside this file are defined all the classes used to standardise the input/output schemas required by all the implemented enpoints.

- Every schema **must** inherits from `pydantic.BaseModel` class.
- Every schema and sub-schema name **must** recall the corresponding endpoint. The naming convention to use is `{endpoint_method_name}{type}`, where the `{endpoint_method_name}` is the name of the endpoint function using the camel-case syntax, and `{type}` depends on the situation:
    - `Response`: if the schema refers to the actual response of the endpoint.
    - `Body`: if the schema refers to the input body required by a POST endpoint.
    - Other names can be used for intermediate schemas.
- If an endpoints requires more than 3 inputs, it is **required** to create a dedicated `Body` schema to standardise the input body.

#### `param.py`

It could happen that the external endpoints require parameters (`params`) coming from specific value lists. To help as much as possible the users and avoid wrong values, this file stores all the `Enum` classes identifing the `params` with value lists.

- Every param **must** inherits from `cyhole.core.param.CyholeParam` class.
- The naming convention **must** be `{name}{param_name}`, where `{name}` is the name of the new interaction, and `{param_name}` a set of words that identify the param univocally.

#### `exception.py`

All the exceptions dedicated to this extension are defined inside this file.

- There should be a general `Exception` extension specific. This exception **must** inherits from `cyhole.core.exception.CyholeException`, and its name should follow the naming convention `{name}Exception`, where `{name}` is the name of the new interaction.
- All other exceptions **must** inherits from the `{name}Exception` class.

### Tests

- All the tests **must** be available in a file called `test_{name}.py` inside `tests` folder, where `{name}` is the name of the new interaction.
- Every endpoint **must** have at least one basic test to ensure the response schema consistency.
- Every test that call an endpoint **must** be available for both *synchronous* (test's name ends with `_sync`) and *asynchronous* (test's name ends with `_async`) logic.
- The mock responses **must** be available inside the `tests/resources/{name}` folder.
- Every endpoint **must** have at least one mock response JSON file, and the naming convention is `{endpoint_method_name}_{info}.json`, where the `{endpoint_method_name}` is the name of the endpoint function using the camel-case syntax, and `{info}` provides additional information to the test.
- The test's configuration (`tests/config.py`) **must** be extended to manage at least `mock_response` and `mock_folder` variables, and the corresponding `tets.default.ini` configuration must be updated as well.
- Every test involving a call to an endopint and checking the respoonse **must** implement the `mocker` functionlity to ensure the test's execution also in offline mode.