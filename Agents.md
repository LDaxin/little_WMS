# Agents — AI Agents for little_WMS

This document describes which opencode agents are available for work on **little_WMS** and how they are used in the context of the project.

---

## Project Context

| Property | Value |
|---|---|
| **Name** | little_WMS |
| **Purpose** | Personal Warehouse Management System – simple enough that you actually use it |
| **Stack** | Django 6.0.3, Django REST Framework 3.14, Gunicorn, SQLite, Docker |
| **Language** | Python 3.12 |
| **Django Apps** | `article`, `codeSystem`, `export`, `hub`, `little_wms`, `location`, `movement`, `softdelete`, `space`, `storage`, `tag` |
| **Development** | Docker-based via `sg docker -c "docker compose up"`, dev entrypoint at `scripts/entrypoint-dev.sh` |

---

## Available Agents & Use Cases

### Development

| Agent | When to Use |
|---|---|
| **implementierer** | Implement new features: Django models, views, templates, REST endpoints, forms. Always referencing existing patterns in the codebase. |
| **bug-fixer** | Fix bugs. Describe the expected vs. actual behavior, relevant logs, and the affected Django app. |
| **refactorer** | Improve code structure without changing behavior, e.g. eliminate duplication in views, optimize querysets, unify template structure. |
| **tester** | Write or run tests. The project currently has minimal test coverage – tests should be added before any refactoring. See `docs/developer/testing.md` for the manual test checklist. |

### Quality Assurance

| Agent | When to Use |
|---|---|
| **code-reviewer** | Review PRs or diffs for code quality, Django best practices, and project conventions. |
| **security** | Security analysis: secrets in code/config, insecure querysets, missing permission checks, dependency vulnerabilities. |

### Planning & Research

| Agent | When to Use |
|---|---|
| **explore** | Explore the codebase: find files, understand dependencies between Django apps, identify existing patterns. |
| **planer** | Create an execution plan for complex features that distributes tasks to the appropriate agents. |
| **dirigent** | Orchestrate complex, parallelizable tasks and delegate them to sub-agents. |
| **rechercheur** | External research (Django docs, DRF, deployment questions). |
| **bewerter** | Compare and evaluate technical decisions (e.g. library choice, architectural approaches). |

### Infrastructure & Operations

| Agent | When to Use |
|---|---|
| **devops** | Docker, docker-compose, CI/CD, deployment configuration. |
| **dependency-manager** | Check and update `requirements.txt`. |
| **scaffolder** | Create a new Django app within the project (models, admin, views, URLs, template scaffold). |

### Documentation

| Agent | When to Use |
|---|---|
| **dokumentierer** | README, docs under `docs/`, inline docstrings, API documentation. |

---

## Project-Specific Conventions

These conventions must be included in every agent prompt when relevant:

### Language

- **English only**: The project is conducted entirely in English — code, documentation, commit messages, branch names, and issues are all written in English. Avoid German terms.

### Git

- **Commit Namespace**: `type: what` — types are `fix`, `add`, `clean`, `refactor`, `delete` (see `docs/git commit namespace.md`)
- **Branch Naming**: `type/step/name` — e.g. `feat/0.1/CharacterizationTests`, `doc/0.0/RequirementsSpec`
- **Base Branch**: `ki` (branched off `dev`). Work branches off `ki`, never directly off `dev`.
- **Merging**: Agents may merge **only after explicit approval** from the human maintainer. The maintainer reviews the branch and gives the go-ahead; the agent then performs the merge. Without approval, agents never merge or rebase.
- **Co-Author**: Commits made by AI agents include a co-author trailer:
  `Co-authored-by: opencode <noreply@opencode.ai>`

### Django

- **App Structure**: Each Django app lives directly under `src/` (e.g. `src/article/`, `src/storage/`)
- **Templates**: Per app under `templates/<app>/`, modules under `templates/<app>/modules/` (no `extends header.html`)
- **Settings**: Central configuration in `src/little_wms/settings.py`
- **URLs**: One `urls.py` per app, included in `src/little_wms/urls.py`
- **Soft Delete**: The app `softdelete` provides cross-app soft-delete logic

### Docker Development

- Dev entrypoint: `scripts/entrypoint-dev.sh` (with live reload)
- **Always run Docker via `sg docker`** — the shell has no direct docker-group
  access, so every `docker` / `docker compose` command must be wrapped:
  `sg docker -c "docker compose <args>"`
- For new dependencies: rebuild the image with `./scripts/build.sh`, then
  `sg docker -c "docker compose up"`
- Database persistence: `./data/` is mounted as a volume
- **All testing runs through Docker** — never rely on a local Python/Django:
  - Tests: `sg docker -c "docker compose run --rm --no-deps --entrypoint python web manage.py test"`
  - Migrations: `sg docker -c "docker compose run --rm --no-deps --entrypoint python web manage.py migrate"`
- `src/` is **baked into the image** (only `./data` is mounted). After code
  changes, rebuild so the app serves the new code:
  `sg docker -c "docker compose build" && sg docker -c "docker compose up -d"`
- **Rebuild Docker before asking for a merge** — the maintainer tests the
  running container, not the working tree.

---

## Project Documents

| Document | Purpose |
|---|---|
| `docs/Lastenheft.md` | Requirements specification (37 sections, all confirmed) |
| `docs/Implementation Plan.md` | Phased implementation plan (8 phases, 40 steps) |
| `docs/Known Issues.md` | Central register of defects found in the codebase |
| `docs/Structure.md` | Data model definitions (Articles, Storages, Locations) |
| `docs/Development Workflow.md` | Kanban-based workflow (human contributors) |
| `docs/git commit namespace.md` | Commit types |

### Skills

| Skill | Purpose |
|---|---|
| `little-wms-implementation` | Enforces the implementation workflow (branch off `ki`, small steps, never merge, ponytail) |
| `little-wms-bugfix` | Bug workflow (record findings in the register, root-cause fix, regression test, register upkeep) |
| `requirements-collaboration` | Working style for requirements/planning (discuss before writing, small steps, user decides) |

### Kanban

The Kanban board (`kanban.krauseadrian.de`) is used by **human contributors**. AI-agent work does **not** require a Kanban task — a branch with a descriptive name is sufficient.

---

## Prompt Building Blocks

These sections can be reused in agent prompts:

### Django Context (always include for code tasks)

```
The project is a Django 6.0.3 WMS with Django REST Framework 3.14.
Working directory: src/
Django apps: article, codeSystem, export, hub, little_wms, location, movement, softdelete, space, storage, tag
Templates live under templates/<app>/, modules under templates/<app>/modules/.
Settings: src/little_wms/settings.py
URLs: src/little_wms/urls.py (root) + one urls.py per app
```

### Docker Dev Context

```
Development environment: Docker via `sg docker -c "docker compose up"`.
Always run Docker through `sg docker` (no direct docker-group access).
Dev entrypoint: scripts/entrypoint-dev.sh (with live reload).
For new dependencies: update requirements.txt, then rebuild the image with ./scripts/build.sh.
Data persists in ./data/ (mounted as a volume).
Never write `rtk` — opencode prepends it to shell commands automatically.
```

---

## Typical Workflows

### Develop a New Feature

1. **planer** → create a plan
2. **explore** → identify affected files and patterns
3. **implementierer** → implement the feature (with Django context prompt)
4. **tester** → write/run tests
5. **code-reviewer** → have the diff reviewed

### Fix a Bug

1. **explore** → narrow down the source of the error
2. **bug-fixer** → implement the fix
3. **tester** → check for regressions

### Refactoring

1. **explore** → map the affected code
2. **tester** → write tests beforehand (safety net)
3. **refactorer** → perform the refactoring
4. **tester** → run tests afterwards