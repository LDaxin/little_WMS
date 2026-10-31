## Context

§19 lists import. The article model is `ArticleBase` (name + type) → `Article`
(identity) → `Stock` (quantity at a `Space`). This change adds a two-step CSV
import that handles real-world spreadsheets.

## Goals / Non-Goals

**Goals:**

- Upload → preview (dry-run) → confirm.
- Per unknown type/storage: create, map to an existing one, or skip.
- Duplicates: skip or update.
- Delimiter detection and German/English header aliases.
- A downloadable template.

**Non-Goals:**

- Excel, importing other objects, a per-row column-mapping UI.

## Decisions

### Decision 1: Two steps, the file kept in the session

Step 1 parses and previews; the raw text is stored in the session (DB-backed).
Step 2 re-parses it and applies the choices. This avoids re-uploading and keeps
the service stateless.

### Decision 2: Delimiter by counting, not `csv.Sniffer`

The delimiter is chosen by comparing `;` and `,` in the header line — predictable
and enough for Excel exports. `csv.Sniffer` is unreliable on small samples.

### Decision 3: Header aliases

Headers are lowercased and mapped through an alias table (`Name`/`name`,
`Typ`/`type`, `Menge`/`menge`, `Lagerort`/`storage`, `Zustand`/`zustand`).
Unknown headers are ignored.

### Decision 4: Validate before creating

Each row is validated first; only valid rows create records. Unknown types and
storages are resolved by the user's choice (create / map / skip); a skipped one
fails only its row.

### Decision 5: A service module

`article/importer.py` exposes `parse_csv`, `preview_import`, and
`import_articles`, so the logic is testable without HTTP.

## Risks / Trade-offs

- [Session holds the file] → fine for a personal WMS; a very large file is
  rejected.
- [Creating a storage needs a type] → a default `other` storage type is used.

## Migration Plan

- None.
