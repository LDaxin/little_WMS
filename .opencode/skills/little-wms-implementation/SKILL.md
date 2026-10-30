---
name: little-wms-implementation
description: Use when implementing little_WMS work, making code changes to the little_WMS project, or working through an OpenSpec change. Applies to coding, testing, branching, and committing against the OpenSpec specs and changes.
---

# little_WMS Implementation

Enforce the agreed workflow and conventions for anyone implementing little_WMS.

## References

- `openspec/specs/` — **source of truth**: what the system does today.
- `openspec/changes/` — upcoming work as OpenSpec change proposals.
- `docs/Lastenheft.md` — requirements / backlog (built sections link to their spec).
- `docs/Known Issues.md` — central register of defects found in the codebase.
- `Agents.md` — project conventions (language, commit namespace, branch
  naming, merges by humans only).

## Spec-driven workflow

The specs are the truth; every piece of work is an OpenSpec **change** that
moves the code (and, on archive, the specs) forward.

- **Specs** (`openspec/specs/<capability>/spec.md`) describe current behaviour.
  Never write unbuilt behaviour into a spec.
- **Changes** (`openspec/changes/<name>/`) hold the plan for one unit of work:
  `proposal.md` → `specs/<capability>/spec.md` (delta) → `design.md` → `tasks.md`.
- The unbuilt vision lives in `docs/Lastenheft.md` (backlog). When a section is
  picked up, it becomes a change.

Useful commands:

```bash
openspec new change <name>                       # scaffold a change
openspec status --change <name>                  # artifact progress
openspec instructions <artifact> --change <name> --json
openspec validate --specs --strict               # validate specs
openspec validate <change> --strict              # validate a change
openspec archive <name>                          # merge deltas into specs
```

The `openspec-*` skills and `opsx-*` commands (installed by `openspec init`)
wrap this workflow.

## Per-change flow

```
1. Pick the next piece of work (from the Lastenheft backlog / a spec gap).
2. `openspec new change <name>` and write the artifacts
   (proposal → specs delta → design → tasks).
3. Branch off `ki`: type/<change-name>
4. Implement the tasks; tick them off in tasks.md (`- [ ]` → `- [x]`).
5. Run the full test suite in Docker (must be green).
6. `sg docker -c "docker compose build" && sg docker -c "docker compose up -d"`
   — so the owner can test.
7. Report: what was done + how to test it (URL, credentials).
8. Human reviews and approves.
9. Agent merges into `ki` (only after approval).
10. `openspec archive <name>` — updates the main specs.
```

**Always rebuild Docker before asking for the merge** — the owner tests the
running container, not the working tree.

## Known Issues

- Before touching a view/model, check `docs/Known Issues.md` for related
  entries.
- When you find a defect, add an entry (ID, location, symptom, status, test)
  instead of only mentioning it in chat.
- When you fix a defect, set its status to ✅ and update the pinned test.
- Bug-specific workflow: see the `little-wms-bugfix` skill.

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
