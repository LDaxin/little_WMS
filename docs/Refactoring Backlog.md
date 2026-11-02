# Refactoring Backlog – little_WMS

> Central register of **duplication / over-engineering** found across the codebase.
> This is technical debt, not defects — defects live in [Known Issues](Known%20Issues.md).
> Each entry describes the current shape and a suggested consolidation.

**Status:** 🔴 open · 🟡 in progress · ✅ done · ⚪ won't fix

Scope: the whole `ki` line (252 commits / 52 changes since `dev`).

| ID | Where | Current shape | Suggested fix | Status |
|---|---|---|---|---|
| RF-001 | `loans/models.py`, `loans/views.py`, `notifications/checks.py` | Two models for one concept (§20): `Lending` (org lends out, with a `CalendarEntry`) and `Loan` (org borrows in, inline dates). Parallel views and templates; `return_overdue_findings` builds near-identical findings for both. | One `Loan` model with a `direction` field; one view set, one template, one overdue path. | ✅ done |
| RF-002 | `hub/models.py`, `organisation/models.py`, `savedviews/models.py` | Token capability links built three times: `Invitation`, `ShareLink`, `EmailVerification` — each with `token = secrets.token_urlsafe(32)`, `expires_at`, `is_valid()`/status, revocation. | Shared abstract base (token + expiry + validity). | ✅ done |
| RF-003 | `occasion/services.py`, `occasion/views.py` | The packlist shape exists twice: `Packlist` (model: occasion, article, quantity, status) and `OccasionTemplate.default_packlist` (JSON `{"article", "quantity"}`). | One serialisation for the packlist shape (template renders to the same structure). | ✅ done |
| RF-004 | `article/models.py`, `loans/models.py` | `Article.ownership` (`owned`/`borrowed`) is a second source of truth for "there is a loan". | Derive ownership from the open loan, or keep one canonical field. | 🔴 open |
| RF-005 | `codeSystem/services.py`, `movement/` | Prefix→object lookup scattered across `resolve_space`, `_resolve_target`, `movementScan`, `where`, `_resolve_location`, `inventoryScan`. | One shared code resolver. | ✅ done |
| RF-006 | `hub/csv.py`, `article/`, `storage/`, `codeSystem/`, `movement/`, `reports/` | The `HttpResponse + csv.writer` export skeleton repeated six times. | One CSV helper. | ✅ done |
| RF-007 | all apps | 13 `*Search` views repeat the same `Q(...__contains=...)` + `results.html` pattern. | Shared search helper / template. | 🔴 open |

## Order

1. **RF-001** first (the only real "same function built twice").
2. Then the smaller pattern repetitions (RF-002 … RF-007) one by one.
