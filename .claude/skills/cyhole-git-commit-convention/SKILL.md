---
name: cyhole-git-commit-convention
description: Use when creating any git commit - enforces structured commit messages with a 3-letter action code, title, and description following the project convention
---

# Git Commit Convention

## Overview

All commits in this project MUST follow the format: `CODE: Title` with a descriptive body.

**Core principle:** Every commit message clearly communicates WHAT action was taken and WHY through a structured, scannable format.

**Violating the letter of this convention is violating the spirit of this convention.**

## The Iron Law

```
NO COMMIT WITHOUT A PROPERLY FORMATTED MESSAGE
```

## Commit Message Format

```
CODE: Short descriptive title (imperative mood, max ~72 chars)

Detailed description of what was done and why.
Context, motivation, and any relevant details.
```

**Never** include co-authors information in the commit message.

## Action Codes

| Code | Meaning | Use When |
|------|---------|----------|
| `ADD` | Addition | New files, features, dependencies, or capabilities |
| `UPD` | Update | Enhancements, modifications to existing functionality |
| `FIX` | Fix | Bug fixes, error corrections, broken behavior |
| `DEL` | Delete | Removing files, features, dead code, dependencies |
| `DOC` | Documentation | README, comments, docstrings, CHANGELOG |
| `REF` | Refactor | Code restructuring without behavior change |
| `TST` | Test | Adding or updating tests |
| `STY` | Style | Formatting, linting, whitespace (no logic change) |
| `CFG` | Config | Configuration files, environment, build settings |
| `SEC` | Security | Security patches, vulnerability fixes, auth changes |
| `DEP` | Dependency | Dependency upgrades, additions, removals |
| `MRG` | Merge | Merging branches, resolving merge conflicts |
| `WIP` | Work in Progress | Incomplete work saved to branch (never on main) |

## Examples

### Good

```
ADD: User authentication with JWT tokens

Implement JWT-based auth system with login/logout endpoints,
token refresh, and role-based access control middleware.
```

```
FIX: Payslip parser failing on multi-page PDFs

The Azure CU response handler assumed single-page output.
Updated to iterate all pages and merge extracted fields.
```

```
REF: Extract payslip validation into dedicated service

Moved validation logic from workflow into PayslipValidator
service class to improve testability and separation of concerns.
```

```
DEL: Remove legacy CSV export endpoint

CSV export was replaced by the JSON export in v2.1.
Endpoint had no consumers for 3 months per access logs.
```

```
CFG: Add CORS configuration for staging environment

Added staging domain to allowed origins in FastAPI middleware
to support the new staging deployment pipeline.
```

### Bad

```
# Missing code
Updated stuff

# Vague title
UPD: Changes

# Wrong code (this is a fix, not an update)
UPD: Fix login crash on empty password

# No description
ADD: New component
```

## Rules

1. **Code is mandatory** - Every commit starts with a 3-letter code from the table above
2. **Title is imperative** - "Add feature" not "Added feature" or "Adding feature"
3. **Title is concise** - Max ~72 characters including the code prefix
4. **Description is required** - Explain the what and why, not just restate the title
5. **One code per commit** - If work spans multiple codes, split into multiple commits
6. **Choose the most specific code** - `SEC` over `FIX` for security fixes, `TST` over `ADD` for test files

## Choosing the Right Code

```
Is it brand new?
  Yes → ADD
  No ↓
Is something removed?
  Yes → DEL
  No ↓
Is it fixing broken behavior?
  Yes → Is it a security issue?
    Yes → SEC
    No → FIX
  No ↓
Is it changing how code is organized (no behavior change)?
  Yes → Is it formatting/whitespace only?
    Yes → STY
    No → REF
  No ↓
Is it modifying existing behavior or features?
  Yes → UPD
  No ↓
Is it only documentation?
  Yes → DOC
  No ↓
Is it only tests?
  Yes → TST
  No ↓
Is it config/build/environment?
  Yes → CFG
  No ↓
Is it dependency changes only?
  Yes → DEP
  No ↓
Is it a branch merge or merge conflict resolution?
  Yes → MRG
  No → Pick the most dominant action
```

## Red Flags - STOP

- Commit message without a code prefix
- Using a code not in the table
- Title longer than 72 characters
- Empty or missing description
- Code that doesn't match the actual changes
- Multiple unrelated changes in one commit (split them)

## When to Apply

**ALWAYS** - this skill applies to every single `git commit` in this project. No exceptions.