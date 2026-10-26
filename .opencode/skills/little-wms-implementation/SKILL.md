---
name: little-wms-implementation
description: Use when implementing little_WMS v2 plan steps, making code changes to the little_WMS project, or working through the phased implementation. Applies to coding, testing, branching, and committing against the Implementation Plan.
---

# little_WMS Implementation

Enforce the agreed workflow and conventions for anyone implementing the
little_WMS v2 plan.

## References

- `docs/Implementation Plan.md` — the phased step plan.
- `docs/Lastenheft.md` — the requirements.
- `docs/Known Issues.md` — central register of defects found in the codebase.
- `Agents.md` — project conventions (language, commit namespace, branch
  naming, merges by humans only).

## Known Issues

- Before touching a view/model, check `docs/Known Issues.md` for related
  entries.
- When you find a defect, add an entry (ID, location, symptom, status, test)
  instead of only mentioning it in chat.
- When you fix a defect, set its status to ✅ and update the pinned test.
- Bug-specific workflow: see the `little-wms-bugfix` skill.

## Workflow

- Branch off `ki` — never directly off `dev`.
- Branch naming: `type/step/name` (e.g. `feat/0.1/CharacterizationTests`).
- Keep steps small: one coherent unit, reviewable in ~15–30 min.
- Add tests per step where sensible.
- **Merge only after approval.** The human maintainer reviews and approves;
  the agent then performs the merge. Never merge without explicit approval.
- After each step, report: "done, here is what I did".

## Commit Convention

`type: what` with types `fix`, `add`, `clean`, `refactor`, `delete`.
See `docs/git commit namespace.md`.

## Language

English only — code, docs, commits, branches.

## Principles

- Ponytail: no over-engineering, simplest solution that works, stdlib/native
  first, deletion over addition.
- Follow existing code patterns (see `Agents.md`).
- Don't break existing functionality — tests must stay green.

## Review Checklist

- Does it do what it should?
- Does it break anything existing? (tests green?)
- Is it not over-engineered?
- Does it match the code style?
- Are the commits clean?
- Is it revertible?

## Testing via Docker

All tests and manual verification run through **Docker** — never rely on a
locally installed Python/Django.

**Always run Docker via `sg docker`.** The shell has no direct docker-group
access, so every `docker` / `docker compose` command must be wrapped:

```bash
sg docker -c "docker compose <args>"
```

- Run the full test suite (must be green before reporting):
  ```bash
  sg docker -c "docker compose run --rm --no-deps --entrypoint python web manage.py test"
  ```
- The image bakes in `src/`; the running container only mounts `./data`.
  After code changes you must rebuild so the app serves the new code:
  ```bash
  sg docker -c "docker compose build"
  sg docker -c "docker compose up -d"
  ```
- Migrations on the dev DB:
  ```bash
  sg docker -c "docker compose run --rm --no-deps --entrypoint python web manage.py migrate"
  ```

## Tooling

- **Never write `rtk`.** opencode prepends it to shell commands automatically;
  type plain commands (`git status`, not `rtk git status`).
- **Docker only via `sg docker`** (see *Testing via Docker*).

## Per-Step Flow

```
1. Branch off `ki`: type/step/name
2. Work
3. Commits
4. Run the full test suite in Docker (must be green)
5. `sg docker -c "docker compose build" && sg docker -c "docker compose up -d"` — so the owner can test
6. Report: what was done + how to test it (URL, credentials)
7. Human reviews and approves
8. Agent merges into `ki` (only after approval)
```

**Always rebuild Docker before asking for the merge** — the owner tests the
running container, not the working tree.