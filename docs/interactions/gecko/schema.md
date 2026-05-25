---
toc_depth: 3
---
# Response Schema

Each response has been mapped into a `pydantic` schema in a way that makes it easy to read and write codes that use them.

The classes identifying the response schema of an endpoint are the only ones ending with `Response` word, all other sub-schemes are used to identify the structures obtained from the responses.

::: cyhole.gecko.schema
    options:
        show_if_no_docstring: true
