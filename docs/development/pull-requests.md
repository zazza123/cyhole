# Pull Requests

This section describes how to prepare and submit code changes to the `cyhole` library. All contributions are merged into `main` via pull requests.

## Branch Naming

Every contribution should live on a dedicated branch. The branch name must follow one of these patterns depending on the type of change:

| Type | Pattern | Example |
|------|---------|---------|
| New `Interaction` | `{name}-new-interaction` | `sun-new-interaction` |
| New endpoints on existing `Interaction` | `{name}-{scope}-api` | `jupiter-ultra-api` |
| General feature or improvement | `feature-{description}` | `feature-async-support` |
| Bug fix | `fix-{description}` | `fix-birdeye-token-parse` |

The branch must be created from an up-to-date `main`.

## Pull Request Title

The PR title must follow the same convention as commit messages (see [Commit Messages](#commit-messages) below):

```
CODE: Short descriptive title (imperative mood, max ~72 chars)
```

Developers using Claude Code can use the **`cyhole-git-commit-convention`** skill to ensure the title is formatted correctly.

## Commit Messages

Every commit must follow this structure:

```
CODE: Short descriptive title (imperative mood, max ~72 chars)

Detailed description of what was done and why.
Context, motivation, and any relevant details.
```

Where `{CODE}` is one of:

| Code | Meaning | Use When |
|------|---------|----------|
| `ADD` | Addition | New files, features, dependencies, or capabilities |
| `UPD` | Update | Enhancements, modifications to existing functionality |
| `FIX` | Fix | Bug fixes, error corrections, broken behavior |
| `DEL` | Delete | Removing files, features, dead code, dependencies |
| `DOC` | Documentation | README, comments, docstrings, docs pages |
| `REF` | Refactor | Code restructuring without behavior change |
| `TST` | Test | Adding or updating tests |
| `STY` | Style | Formatting, linting, whitespace (no logic change) |
| `CFG` | Config | Configuration files, environment, build settings |
| `SEC` | Security | Security patches, vulnerability fixes, auth changes |
| `DEP` | Dependency | Dependency upgrades, additions, removals |
| `MRG` | Merge | Merging branches, resolving merge conflicts |
| `WIP` | Work in Progress | Incomplete work saved to branch (never on `main`) |

Rules:

- Title in imperative mood — "Add endpoint", not "Added" or "Adding"
- Title max ~72 characters including the code prefix
- Description is required — explain the what and why, not just restate the title
- One code per commit — split unrelated changes into separate commits
- Choose the most specific code — `SEC` over `FIX` for security fixes, `TST` over `ADD` for test files

Developers using Claude Code can use the **`cyhole-git-commit-convention`** skill to enforce this convention automatically on every commit.

## Checklist Before Opening a PR

Before opening a pull request, verify that the following steps are complete:

1. **Lint passes** — run `ruff check src/` from the repository root. No errors should be reported.
2. **Tests pass** — run `pytest tests/` from the repository root. All tests must be green.
3. **Mock responses are committed** — any new endpoint must have at least one JSON mock file in `tests/resources/mock/{name}/`.
4. **Documentation is updated** — new or changed behaviour must be reflected in the relevant `docs/` pages and their index files.

!!! note
    The CI pipeline runs lint and the full test suite automatically on every pull request targeting `main`. A PR cannot be merged if CI is failing.

## CI Pipeline

When a pull request is opened against `main`, the following jobs run automatically via GitHub Actions:

- **Lint** — `ruff check src/cyhole tests` on Python 3.12.
- **Tests** — `coverage run -m pytest tests/` on Python 3.12, using the default `test.default.ini` configuration (all mock responses enabled).

Both jobs must succeed before the PR is eligible for merge.

## Pull Request Description

A good PR description makes review faster and creates a useful record in git history. Include:

- **What changed** — a brief summary of the additions, changes, or fixes.
- **Why** — the motivation or issue being addressed.
- **Scope** — which `Interaction`(s) or core components are affected.
- **Testing notes** — any relevant detail about how the change was tested (e.g. live API call vs. mock only).

## Related Documentation

- [New Interaction](new-interaction.md) — full guide for contributing a new `Interaction`.
- [Bugs & Improvements](bugs-improvements.md) — how to report bugs or propose improvements.
- [Testing](testing.md) — how tests and mock responses are managed.

---
**Last Updated:** May 2026  
**Status:** Implemented
