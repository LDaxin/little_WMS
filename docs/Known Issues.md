# Known Issues – little_WMS

> Central register of defects found while working on the codebase.
> Entries describe the **current** behaviour (characterization), not the desired behaviour.
> Reference: [Implementation Plan](Implementation%20Plan.md) · [Requirements Specification](Lastenheft.md)

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
| KI-010 | movement (all) | No audit trail (planned in §32) | 🔴 open | 0.3 | – |

## Code System

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-011 | `codeSystem/urls.py` | `^code/add` is registered before `^code/add/modal`, so `addModal` is unreachable; `GET /code/add/modal` → `MultiValueDictKeyError` (500) | 🔴 open | 0.2 | `codeSystem/tests/test_views.py` |

## Location

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-012 | `location/views.py` `searchLocations` | Filters on `name__contains`, but `Location` has no `name` field → `FieldError` (500) for any non-empty search | ✅ fixed | 0.2 | `location/tests/test_views.py` |
| KI-017 | `location/models.py` `Location.save` | Used the `ArticleType` prefix `at` instead of `l0`, so Location codes collided with ArticleType codes | ✅ fixed | 1.5 | `location/tests/test_models.py` |

## Tag

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-013 | `tag/views.py` | `tags`, `addTag`, `delTag`, `tagIncert`, `updateTag` lack `@login_required` → reachable without login | 🔴 open | 0.2 | – |

## Article

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-014 | `article/views.py` `updateArticle` | Error branch uses bare names (`toastName:`) → `NameError`; branch is unreachable dead code | 🔴 open | 0.2 | – |
| KI-019 | `ArticleType.field_config` / `custom_fields_schema`, `ArticleBase.attributes` | `JSONField(default=dict)` without `blank=True` → required in forms/admin despite having a default | ✅ fixed | 1.6 | `article/tests/test_schema.py` |

## Storage

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-018 | `Article.stored` / `hub/fields.py` `SelfForeignKey` | Cycles between articles/spaces were possible; `SelfForeignKey` silently set the value to `None` on a cycle; `Settings.storageDepth` was unused | ✅ fixed | 1.6 | `space/tests/test_services.py`, `hub/tests/test_fields.py` |

## Migrations

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-015 | `article/migrations/0003_restruckture_article.py` | `RunPython(dataTransfer)` has no `reverse_code` → the migration is irreversible and blocks any rollback that would unapply it | 🔴 open | 0.5 | – |

## Database / Environment

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-016 | `data/wms.sqlite3` | Dev DB had a `codeSystem_uuidcode.shortCode` column (`NOT NULL`) that no model or migration defines → every INSERT into `codeSystem_uuidcode` failed. DB was rebuilt from migrations. | ✅ fixed | 0.5 | – |

## Roles & Permissions (§3)

| ID | Location | Symptom | Status | Found in | Test |
|---|---|---|---|---|---|
| KI-020 | `organisation/models.py` `Role` / `organisation/views.py` `roleCreate` | `unique_together = ("organisation", "name")` made a role created from a template collide with the template row of the same name → `IntegrityError` (500) on `/roles/create/` with the prefilled name | ✅ fixed | 3.1b | `organisation/tests/test_views.py` |
