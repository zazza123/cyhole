---
toc_depth: 3
---
# Response Schema

Each response has been mapped into a `pydantic` schema in a way that makes it easy to read and write codes that use them.

The classes identifying the response schema of an endpoint are the only ones ending with `Response` word, all other sub-schemes are used to identify the structures obtained from the responses.

!!! tip "Schema Enhancement"

    If some schema are __incorrect__ or __needs to be enhanced__ (optional/mandatory fields changes, incorrect datatype or schema update) feel free to open a pull request or issue by attaching:

        - method
        - endpoint call executed
        - response obtained

::: cyhole.birdeye.schema
    options:
        show_if_no_docstring: true