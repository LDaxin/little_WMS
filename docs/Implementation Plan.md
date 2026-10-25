# Implementation Plan – little_WMS v2

> **Reference:** [Requirements Specification](Lastenheft.md) · [Known Issues](Known%20Issues.md)
> **Status:** Phase 1 in progress

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

### Phase 2 – Core Operations

- **2.1** Movement Redesign (§11)
- **2.2** QR Workflow + Sheet Printing (§5)
- **2.3** Sets / Bundles (§4d)
- **2.4** Audit Log (§32)

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
| 1 | 1.6 Storage Integrity | ⬜ open |
| 1 | 1.7 Tags | ⬜ open |
| 1 | 1.8 Locations | ⬜ open |
| 1 | 1.9 Article form (field_config + custom fields) | ⬜ open |
| 1 | 1.10 Store/Remove service + UI (discuss first) | ⬜ open |
| 2 | 2.1 Movement Redesign | ⬜ open |
| 2 | 2.2 QR Workflow | ⬜ open |
| 2 | 2.3 Sets / Bundles | ⬜ open |
| 2 | 2.4 Audit Log | ⬜ open |
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
