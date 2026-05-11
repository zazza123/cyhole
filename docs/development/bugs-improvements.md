# Bugs & Improvements

This section explains how to report bugs or propose improvements to the `cyhole` library. Both are tracked as GitHub Issues in the [zazza123/cyhole](https://github.com/zazza123/cyhole) repository.

## Reporting a Bug

Before opening a new issue, search the existing issues to avoid duplicates. If the bug has not been reported yet, open a new issue and include:

- **Description** — what behaviour is observed vs. what is expected.
- **Interaction** — which `Interaction` or core component is affected (e.g. `cyhole.birdeye`, `cyhole.core.client`).
- **Reproduction steps** — the minimal sequence of calls that triggers the bug.
- **Environment** — Python version, `cyhole` version, operating system.
- **Error output** — the full traceback or unexpected response, if applicable.

!!! tip
    The more detail you provide, the faster the bug can be confirmed and fixed.

## Proposing an Improvement

Improvements include anything that makes the library more useful, reliable, or ergonomic — for example: new parameters on an existing endpoint, better error messages, or additional response fields.

When opening an improvement issue, include:

- **Motivation** — why the change is useful and what problem it solves.
- **Scope** — which `Interaction`(s) or core components would be affected.
- **Proposed approach** — a brief description of how the change could be implemented (optional, but helpful).

## From Issue to Pull Request

Once a bug or improvement has been discussed and agreed upon:

1. Fork the repository or create a branch following the naming conventions in [Pull Requests](pull-requests.md#branch-naming).
2. Implement the fix or improvement, including tests and documentation updates.
3. Open a pull request referencing the original issue.

See [Pull Requests](pull-requests.md) for the full contribution workflow and checklist.

## Related Documentation

- [Pull Requests](pull-requests.md) — how to submit code changes.
- [Testing](testing.md) — how tests and mock responses are managed.
- [New Interaction](new-interaction.md) — guide for contributing a new `Interaction`.

---
**Last Updated:** May 2026  
**Status:** Implemented
