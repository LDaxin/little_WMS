# Known Issues – little_WMS

> Central register of defects found while working on the codebase.
> Entries describe the **current** behaviour (characterization), not the desired behaviour.
> Reference: [OpenSpec specs](../openspec/specs) · [Requirements Specification](Lastenheft.md)

**Status:** 🔴 open · 🟡 in progress · ✅ fixed · ⚪ won't fix

Most entries are pinned by a characterization test (see the *Test* column) so a fix
will make that test fail and force it to be updated.

## Movement (§11)

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-001 | `movement/views.py` `movementStore` | No error handling: unknown code → `DoesNotExist` (500); unknown prefix → `UnboundLocalError` (500) | ✅ fixed | 0.3 | `movement/tests/test_movement.py` |
| KI-002 | `movement/views.py` `movementStore` | Toast always "Error" with `str(hallo)` (debug leftover) | ✅ fixed | 0.3 | – |
| KI-003 | `movement/views.py` `movementStore` | No validation: target space active? article storable? self-storage? | ✅ fixed | 0.3 | `movement/tests/test_movement.py` |
| KI-004 | `movement/views.py` `movementStore` | No transaction: partial state on mid-loop failure | ✅ fixed | 0.3 | `movement/tests/test_movement.py` |
| KI-005 | `movement/views.py` `movementRemove` | No error handling: unknown code → `DoesNotExist` (500) | ✅ fixed | 0.3 | `movement/tests/test_movement.py` |
| KI-006 | `movement/views.py` `movementRemove` | Only reads `articleCode1`; further buffered articles are ignored | ✅ fixed | 0.3 | `movement/tests/test_movement.py` |
| KI-007 | `movement/views.py` `movementCodeInfo` | `request.GET['code']` without `.get()` → `KeyError` (500) | ✅ fixed | 0.3 | `movement/tests/test_movement.py` |
| KI-008 | `movement/views.py` `movementSearch` | `request.GET['search']` without `.get()` → `KeyError` (500) | ✅ fixed | 0.3 | – |
| KI-009 | `movement/views.py` `movementCodeInfo` | Article without a `Space` → `AttributeError` (500) | ✅ fixed | 0.3 | `movement/tests/test_movement.py` |
| KI-010 | movement (all) | No audit trail (planned in §32) | ✅ fixed | 0.3 | `movement/tests/test_movement.py` |

## Code System

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-011 | `codeSystem/urls.py` | `^code/add` was registered before `^code/add/modal`, so `addModal` was unreachable; `GET /code/add/modal` → `MultiValueDictKeyError` (500). Fixed by anchoring `^code/add$`. | ✅ fixed | 0.2 | `codeSystem/tests/test_views.py` |

## Location

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-012 | `location/views.py` `searchLocations` | Filters on `name__contains`, but `Location` has no `name` field → `FieldError` (500) for any non-empty search | ✅ fixed | 0.2 | `location/tests/test_views.py` |
| KI-017 | `location/models.py` `Location.save` | Used the `ArticleType` prefix `at` instead of `l0`, so Location codes collided with ArticleType codes | ✅ fixed | 1.5 | `location/tests/test_models.py` |

## Tag

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-013 | `tag/views.py` | `tags`, `addTag`, `delTag`, `tagIncert`, `updateTag` lacked `@login_required` → reachable without login. Fixed by `add: enforce permissions on all views`. | ✅ fixed | 0.2 | – |

## Article

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-014 | `article/views.py` `updateArticle` | Error branch used bare names (`toastName:`) → `NameError`; branch is unreachable dead code. Fixed by `add: store/remove service and article/storage UI`. | ✅ fixed | 0.2 | – |
| KI-019 | `ArticleType.field_config` / `custom_fields_schema`, `ArticleBase.attributes` | `JSONField(default=dict)` without `blank=True` → required in forms/admin despite having a default | ✅ fixed | 1.6 | `article/tests/test_schema.py` |

## Storage

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-018 | `Article.stored` / `hub/fields.py` `SelfForeignKey` | Cycles between articles/spaces were possible; `SelfForeignKey` silently set the value to `None` on a cycle; `Settings.storageDepth` was unused | ✅ fixed | 1.6 | `space/tests/test_services.py`, `hub/tests/test_fields.py` |
| KI-025 | `storage/views.py` `updateStorage` | Used `FormStorage` (fields `name`, `parent`, `code`) while the storage detail page renders `FormChangeStorage` (which also has `location`) → a location selected on the storage was silently dropped on save | ✅ fixed | add-outdoor-map | `storage/tests/test_views.py` |

## Floor plans (§15)

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-024 | `hub/templates/hub/modules/floorPlan.html` | Server-rendered rect coordinates used the locale's decimal separator (`x="20,0"` in German) → invalid SVG numbers, so the drawn areas were invisible on the plan page. The editor was unaffected because it builds the rects in JavaScript. | ✅ fixed | add-floor-plans | `storage/tests/test_floor_plans.py` |

## Migrations

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-015 | `article/migrations/0003_restruckture_article.py` | `RunPython(dataTransfer)` had no `reverse_code` → the migration was irreversible and blocked any rollback that would unapply it. Fixed with `reverse_code=RunPython.noop`. | ✅ fixed | 0.5 | – |

## Database / Environment

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-016 | `data/wms.sqlite3` | Dev DB had a `codeSystem_uuidcode.shortCode` column (`NOT NULL`) that no model or migration defines → every INSERT into `codeSystem_uuidcode` failed. DB was rebuilt from migrations. | ✅ fixed | 0.5 | – |

## Roles & Permissions (§3)

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-020 | `organisation/models.py` `Role` / `organisation/views.py` `roleCreate` | `unique_together = ("organisation", "name")` made a role created from a template collide with the template row of the same name → `IntegrityError` (500) on `/roles/create/` with the prefilled name | ✅ fixed | 3.1b | `organisation/tests/test_views.py` |
| KI-021 | `organisation/views.py` `roles`/`users` (all) | Roles & Permissions pages had only `@login_required` → every logged-in user could view/edit roles and assign them | ✅ fixed | 3.1c | `organisation/tests/test_views.py` |

## Store / Packlist search (§ code-input)

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-022 | `hub/modules/storeActions.html`, `hub/modules/storageContents.html`, `occasion/packlist.html` | The live-search input had no own `hx-swap`, so it inherited `hx-swap="outerHTML"` from the surrounding `<form>` → the first search **replaced** `#storeResults`/`#packlistResults` instead of filling it, so every later keystroke found no target and the dropdown stopped updating ("works only once") | ✅ fixed | 3.2 | `article/tests/test_store_search.py`, `storage/tests/test_store_search.py`, `occasion/tests/test_occasions.py` |

## List views (all)

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-026 | `hub/modules/results.html` | The detail link was relative (`./<id>`), so on the "all" pages (`/article/`, `/storage/`) it resolved to `/article/<id>` / `/storage/<id>` — no matching route (the detail URL needs the type) → broken link. | ✅ fixed | ki | `article/tests/test_all_views.py`, `storage/tests/test_all_views.py` |
| KI-027 | `article/views.py` `_article_stocks` | The advanced-search query was validated against a prefixed field map (`article__base__name`) while the query used unprefixed names (`base__name`) → every query raised `QueryError`, which was swallowed, so the advanced search never filtered. | ✅ fixed | redesign-list-views | `article/tests/test_all_views.py`, `querybuilder/tests/test_parser.py` |
| KI-028 | `hub/modules/search.html`, `hub/modules/list.html` | The list state (`sort`, `cols`, `mode`) lived in static hidden inputs and in the search input's URL, rendered once; htmx swaps never updated them → after sorting, typing a filter reset the sort; after changing columns/mode, paging reverted them. | ✅ fixed | redesign-list-views | `article/tests/test_all_views.py` |
| KI-029 | `hub/templates/hub/header.html` | Card selection set `check.checked` in JS without firing a `change` event, so the bulk-action forms (`#delForm`/`#exportForm`/`#qrForm`) never received the selected cards — bulk actions on card selections did nothing. | ✅ fixed | redesign-list-views | – (client-side) |
| KI-030 | `hub/modules/search.html`, `hub/modules/list.html` | `#modeInput` was rendered with the resolved list mode (on the first request, which carries no client hint, that is the desktop default) and the search field sent it on every request, so `mode=table` overrode the per-device setting — a phone never got its configured default (cards). | ✅ fixed | list-views | `article/tests/test_all_views.py`, `storage/tests/test_all_views.py` |

## Frontend / Assets

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-023 | `hub/templates/hub/header.html` | Loaded `bootstrap.min.js` (non-bundle), which expects a global `Popper` that was never loaded → every Bootstrap dropdown (and tooltip/popover) threw `TypeError: Bootstrap's dropdowns require Popper` and never opened. Also the `html5-qrcode` `<script>` tag had no closing `</script>`, so the following `select2` script was swallowed and never loaded. | ✅ fixed | 3.3 | – |
