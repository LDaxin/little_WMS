# Implementation Plan – little_WMS v2

> **Reference:** [Requirements Specification](Lastenheft.md) · [Known Issues](Known%20Issues.md)
> **Status:** Phase 2 in progress

This plan describes the phased implementation of little_WMS v2. Each step is small, reviewable, and merged by the project owner.

---

## Workflow

### Branching

```
dev
 └── ki                          ← integration branch for AI work
      ├── feat/0.1/CharacterizationTests
      ├── feat/0.2/ViewTests
      └── ...
```

- Work branches off `ki` (never directly off `dev`)
- Branch naming: `type/step/name` (e.g. `feat/0.1/CharacterizationTests`)
- Types: `feat`, `fix`, `doc`

### Commits

Commit namespace (see [git commit namespace](git%20commit%20namespace.md)):

- `fix` – bug fix
- `add` – new feature
- `clean` – cleanup
- `refactor` – restructuring
- `delete` – removal

Format: `type: what` (e.g. `add: article model tests`)

### Rules

1. **Small steps** – one coherent unit per step, reviewable in ~15–30 min
2. **Tests per step** – where sensible
3. **Merge only after approval** – the project owner reviews and approves; the agent then performs the merge
4. **Review before merge** – the owner checks each step
5. **No over-engineering** – ponytail principles apply
6. **Follow existing conventions** – code style, structure

### Per-Step Flow

```
1. Branch off `ki`:  type/step/name
2. Work (via sub-agents)
3. Commits
4. Report: "done, here is what I did"
5. Owner reviews and approves
6. Agent merges into `ki` (only after approval)
7. At the end: owner merges `ki` → `dev`
```

### Review Checklist

```
□ Does it do what it should?
□ Does it break anything existing? (tests green?)
□ Is it not over-engineered?
□ Does it match the code style?
□ Are the commits clean?
□ Is it revertible?
```

---

## Phases

### Phase 0 – Safety Net

> Before anything is changed.

- **0.1** Model characterization tests (Article, Storage, Location, Tag)
- **0.2** View characterization tests (all pages return 200, CRUD works)
- **0.3** Movement tests (store/remove, space validation)
- **0.4** Migration workflow documented → [`docs/developer/migrations.md`](developer/migrations.md)
- **0.5** Demo seed + migration dry-run

### Phase 1 – Data Foundation

- **1.1** `organisation` field on all models (§1)
- **1.2** Data migration for existing records (§18)
- **1.3** Article Model: 3 levels, custom-field levels (§25)
- **1.4** Dynamic Article Types: hybrid approach (§4a–c)
- **1.5** Code System (§26)
- **1.6** Storage Integrity: cycle prevention, depth limit (§21)
- **1.7** Tags (§13)
- **1.8** Locations: django-address, Plus Codes (§28)
- **1.9** Article form: show only `field_config`-relevant fields, render custom fields (§4a–c)
- **1.10** Store/Remove service + UI in article & storage views — **discuss in detail before implementing**
- **1.11** Tag UI: chips with color/icon, add/remove in article & storage views

### Phase 2 – Core Operations

- **2.1** Movement Redesign (§11)
- **2.2** QR Workflow + Sheet Printing (§5)
- **2.3a** Composition model + status (§4d)
- **2.3b** Default location via composition (§5b)
- **2.3c** Composition UI (§4d)
- **2.3d** Consume + `menge=0` (§4d)
- **2.3e** Merge on store (§4d)
- **2.3f** Partial store / split (§4d)
- **2.3g** Stock: separate identity from quantity (§4d)
- **2.3h** Minimums (per location + global) + not-stored hints (§4d)
- **2.4a** AuditLog model + logging (§32, §4e)
- **2.4b** Movement session / undo (§11)
- **2.4c** Admin log, filters, retention (§32)
- **2.5** Inventory Mode (§5c)

### Phase 3 – Users & Organisations

- **3.1** Roles & Permissions (§3)
- **3.2** Multi-Organisation Membership (§22)
- **3.3** Registration & Invitations (§23)
- **3.4** Onboarding (server, organisation, user) (§8, §23)

### Phase 4 – Planning

- **4.1** Occasions (§2)
- **4.2** Dashboard (§24)
- **4.3** Notifications (§6)

### Phase 5 – UX & Mobile

- **5.1** Mobile & Navigation (§12)
- **5.2** Query Builder (§9)
- **5.3** Saved Views & Share Links (§10)
- **5.4** PWA (§34)

### Phase 6 – System & Admin

- **6.1** Soft-Delete & Trash View (§27)
- **6.2** Security (§29)
- **6.3** E-Mail / SMTP (§30)
- **6.4** API Authentication (§31)
- **6.5** Reporting & Statistics (§33)
- **6.6** Data Protection / GDPR (§35)
- **6.7** Concurrency (§36)
- **6.8** Database & Scaling (§37)

### Phase 7 – Extended

- **7.1** Internationalization (§14)
- **7.2** Images & Floor Plans (§15)
- **7.3** Import (CSV / Excel) (§19)
- **7.4** Loans & Shared Pools (§20)
- **7.5** Power Functions (§16)

---

## Status Tracking

| Phase | Step | Status |
|---|---|---|
| 0 | 0.1 Model characterization tests | ✅ done |
| 0 | 0.2 View characterization tests | ✅ done |
| 0 | 0.3 Movement tests | ✅ done |
| 0 | 0.4 Migration workflow | ✅ done |
| 0 | 0.5 Demo seed + migration dry-run | ✅ done |
| 1 | 1.1 organisation field | ✅ done |
| 1 | 1.2 Data migration | ⏭️ skipped |
| 1 | 1.3 Article Model | ✅ done |
| 1 | 1.4 Dynamic Article Types | ✅ done |
| 1 | 1.5 Code System | ✅ done |
| 1 | 1.6 Storage Integrity | ✅ done |
| 1 | 1.7 Tags | ✅ done |
| 1 | 1.8 Locations | ✅ done |
| 1 | 1.9 Article form (field_config + custom fields) | ✅ done |
| 1 | 1.10 Store/Remove service + UI (discuss first) | ✅ done |
| 1 | 1.11 Tag UI (chips, colors, add/remove) | ✅ done |
| 2 | 2.1 Movement Redesign | ✅ done |
| 2 | 2.2 QR Workflow + Sheet Printing | ✅ done |
| 2 | 2.3a Composition model + status | ✅ done |
| 2 | 2.3b Default location via composition | ✅ done |
| 2 | 2.3c Composition UI | ✅ done |
| 2 | 2.3d Consume + menge=0 | ✅ done |
| 2 | 2.3e Merge on store | ✅ done |
| 2 | 2.3f Partial store / split | ✅ done |
| 2 | 2.3g Stock (identity vs. quantity) | ✅ done |
| 2 | 2.3h Minimums + not stored | ✅ done |
| 2 | 2.4a AuditLog model + logging | ✅ done |
| 2 | 2.4b Movement session / undo | ✅ done |
| 2 | 2.4c Admin log, filters, retention | ⬜ open |
| 2 | 2.5 Inventory Mode | ⬜ open |
| 3 | 3.1 Roles & Permissions | ⬜ open |
| 3 | 3.2 Multi-Org Membership | ⬜ open |
| 3 | 3.3 Registration & Invitations | ⬜ open |
| 3 | 3.4 Onboarding | ⬜ open |
| 4 | 4.1 Occasions | ⬜ open |
| 4 | 4.2 Dashboard | ⬜ open |
| 4 | 4.3 Notifications | ⬜ open |
| 5 | 5.1 Mobile & Navigation | ⬜ open |
| 5 | 5.2 Query Builder | ⬜ open |
| 5 | 5.3 Saved Views & Share Links | ⬜ open |
| 5 | 5.4 PWA | ⬜ open |
| 6 | 6.1 Soft-Delete & Trash | ⬜ open |
| 6 | 6.2 Security | ⬜ open |
| 6 | 6.3 E-Mail / SMTP | ⬜ open |
| 6 | 6.4 API Authentication | ⬜ open |
| 6 | 6.5 Reporting & Statistics | ⬜ open |
| 6 | 6.6 Data Protection / GDPR | ⬜ open |
| 6 | 6.7 Concurrency | ⬜ open |
| 6 | 6.8 Database & Scaling | ⬜ open |
| 7 | 7.1 Internationalization | ⬜ open |
| 7 | 7.2 Images & Floor Plans | ⬜ open |
| 7 | 7.3 Import | ⬜ open |
| 7 | 7.4 Loans & Shared Pools | ⬜ open |
| 7 | 7.5 Power Functions | ⬜ open |

**Legend:** ⬜ open · 🟡 in progress · ✅ done · ⏭️ skipped

---

## Notes

- Model tiers are intentionally excluded from this plan for now.
- Step sizes may change as we learn how the process runs.
- The existing system is already in use – Phase 0 protects it.
- **2.1** covers the core Movement redesign (service layer, HTMX, two modes, location-first, smart container default, quick actions, atomic store/remove). The remaining §11 features – Undo (two levels), session list, sound/haptic feedback and their settings – are deferred: they build on `AuditLog` (§32, step **2.4**) and the settings work in later phases.
- **2.2** covers QR sheet printing (§5a: format, size, label, QR content, sorting, printable HTML, storage sheets) and the "Where is...?" / "Where should it go?" workflow (§5b). Deferred: live preview, PDF download, sorting by location/type and selection via Query Builder (§9); "last movement" info needs `AuditLog` (§32). Inventory mode (§5c) is split out into step **2.5**.
- **2.3** is reworked around a **composition** on the storage location instead of a separate set model: a `Space` declares `(ArticleBase, soll_menge, mindestmenge)`. This replaces `standard_lagerplatz` (default location becomes a reverse lookup) and models sets as containers with a composition. See [`docs/design/composition.md`](design/composition.md).
