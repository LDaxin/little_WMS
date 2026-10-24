# Requirements Specification – little_WMS v2

> **Status:** 22.09.2026 – fully discussed  
> This document describes requirements and technical implementation ideas.

---

## Table of Contents

1. [Multi-User Preparation](#1-multi-user-preparation-) ⚡
2. [Occasion System](#2-occasion-system-) ⚡
3. [Roles & Permissions](#3-roles--permissions-) ⚡
4. [Article Management](#4-article-management)
   - [4a–c: Dynamic Article Types](#4ac-dynamic-article-types-) ⚡
   - [4d: Sets / Bundles](#4d-sets--bundles-) ⚡
   - [4e: Article History / Audit Trail](#4e-article-history--audit-trail-) ⚡
5. [QR-Code System](#5-qr-code-system)
   - [5a: QR Sheet Printing](#5a-qr-sheet-printing-) ⚡
   - [5b–c: QR Workflow](#5bc-qr-workflow-) ⚡
6. [Notification System](#6-notification-system-) ⚡
7. [Technical Architecture](#7-technical-architecture)
   - [7a: API-First](#7a-api-first-) ⚡
   - [7b: Testing Strategy](#7b-testing-strategy-) ⚡
   - [7c: Migrations](#7c-migrations-safe-handling-) ⚡
8. [Standard Configurations & Onboarding](#8-standard-configurations--onboarding-) ⚡
9. [Query Builder](#9-query-builder-) ⚡
10. [Saved Views & Share Links](#10-saved-views--share-links-) ⚡
11. [Movement Redesign](#11-movement-redesign-) ⚡
12. [Mobile & Navigation](#12-mobile--navigation-) ⚡
13. [Tags](#13-tags-) ⚡
14. [Internationalization](#14-internationalization-) ⚡
15. [Images & Floor Plans](#15-images--floor-plans-) ⚡
16. [Power Functions (not prioritized)](#16-power-functions-not-prioritized-) ⚡
17. [Admin Dashboard & Backup](#17-admin-dashboard--backup-) ⚡
18. [Data Migration & Transformation](#18-data-migration--transformation-) ⚡
19. [Import (CSV / Excel)](#19-import-csv--excel-) ⚡
20. [Loans & Shared Pools](#20-loans--shared-pools-) ⚡
21. [Storage Integrity](#21-storage-integrity-) ⚡
22. [Multi-Organisation Membership](#22-multi-organisation-membership-) ⚡
23. [Registration, Invitations & Onboarding](#23-registration-invitations--onboarding-) ⚡
24. [Dashboard](#24-dashboard-) ⚡
25. [Article Model (3 Levels, Custom-Field Levels, Merge/Split)](#25-article-model-three-levels-custom-field-levels-mergesplit-) ⚡
26. [Code System & Links](#26-code-system--links-) ⚡
27. [Soft-Delete & Trash](#27-soft-delete--trash-) ⚡
28. [Locations](#28-locations-) ⚡
29. [Security](#29-security-) ⚡
30. [E-Mail / SMTP](#30-e-mail--smtp-) ⚡
31. [API Authentication](#31-api-authentication-) ⚡
32. [Audit Log](#32-audit-log-) ⚡
33. [Reporting & Statistics](#33-reporting--statistics-) ⚡
34. [PWA (Progressive Web App)](#34-pwa-progressive-web-app-) ⚡
35. [Data Protection / GDPR](#35-data-protection--gdpr-) ⚡
36. [Concurrency](#36-concurrency-) ⚡
37. [Database & Scaling](#37-database--scaling-) ⚡

---

## 1. Multi-User Preparation ⚡

### Requirement

The system should later be multi-tenant (multiple organisations, multiple users per organisation). Full multi-user operation is not a priority right now, but the data model should be prepared now so that the later migration is painless.

### Implementation

- **Every relevant model** (`Article`, `Storage`, `Location`, `Tag`, `ArticleType`, `ArticleBase`, `StorageType`, `Space`, `ExportTemplate`, `NotificationRule`, etc.) gets a field:
  ```python
  organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE, default=1)
  ```
- **All queries** are filtered by the user's organisation.
- **Authorship** (who created/changed something) lives in the audit log (§4e), **not** as a separate field on the object.
- **Later** the `Organisation` model is added; the `organisation` fields then point to it.

### Migration

- One migration per app that adds the `organisation` field.
- `default=1` ensures that all existing records are assigned to the first organisation.
- Backward migration: remove the field again.

---

## 2. Occasion System ⚡

### Concept

An **Occasion** is the reason why material is needed – neutral term that works for both organizations and private users. Maintenance/Purchase/Disposal are NOT occasions – they go into the **Calendar** as separate entry types.

### Occasion Types (configurable, like ArticleTypes)

| Organization | Private Person |
|---|---|
| Summer camp | Summer vacation |
| Youth group trip | Birthday party |
| Club festival | Wedding |
| Choir weekend | Moving house |
| Conference | Garden party |

### Every Occasion has

- Name, date (from–to), location, participant count, responsible user
- **Packlist** (which articles are needed?)
- Dynamic fields per OccasionType (same system as ArticleTypes)
- **Recurrence** (optional) – see below
- **Template** reference (optional) – created from template

### Calendar – the central planning view

The Calendar shows everything on a timeline:

| Visible in Calendar | Type |
|---|---|
| Summer camp (with packlist) | Occasion |
| Tent "Jurte 8P" – maintenance due | Maintenance |
| Order new camp beds | Purchase |
| Dispose broken pegs | Disposal |
| Inventory Room 2 | Inventory |

### Article-level Calendar

Each article's detail view also shows a **mini calendar** with that article's terms:

- Upcoming maintenance
- Occasions the article is assigned to (packlist entries)
- Past movements / due dates
- Expiry date (for consumables)

This connects the central calendar to individual articles: "Where and when is this tent used?"

### Occasion Templates

Predefined occasions with a default packlist – reusable:

```
Template: "Standard Summer Camp"
  Occasion Type: Camp
  Default Packlist:
    - Tent "Jurte 8P"        × 4
    - Camp bed               × 20
    - Kitchen set "Large"    × 2
    - First aid kit          × 1
```

- Creating an occasion from a template: pick template → set date → packlist is pre-filled
- Templates are editable and can be created from any existing occasion ("Save as template")

### Recurring Occasions

An occasion can be recurring (e.g. "Annual summer camp" every year):

```
Recurrence:
  Frequency:  [Yearly ▼]   Interval: [1]   (every 1 year)
  Ends:       ( ) Never   (•) On [2028-12-31]   ( ) After [5] occurrences
```

| Frequency | Example |
|---|---|
| Daily | Every day |
| Weekly | Every week (with weekday selection) |
| Monthly | Every month (with day-of-month selection) |
| Yearly | Every year (annual camp) |

Each recurrence generates a separate Occasion instance (with its own packlist, so packlists can differ per year). Recurrence can be edited for the whole series or a single instance.

### Copying Occasions

- "Duplicate" button on any occasion → creates a copy with:
  - Same occasion type, same packlist
  - New (empty) date to be set by user
  - Optional: shift dates by N days ("next year's camp = this year's dates + 364 days")

### Data Model

```python
class CalendarEntry(models.Model):
    entry_type = models.CharField(choices=[
        ('occasion', 'Occasion'),
        ('maintenance', 'Maintenance'),
        ('purchase', 'Purchase'),
        ('disposal', 'Disposal'),
        ('inventory', 'Inventory'),
        ('other', 'Other'),
    ])
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    notes = models.TextField(blank=True)
    responsible_user = models.ForeignKey(User, null=True, ...)

class OccasionType(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=20)
    custom_fields_schema = models.JSONField(default=dict)

class OccasionTemplate(models.Model):
    name = models.CharField(max_length=100)
    occasion_type = models.ForeignKey(OccasionType, ...)
    default_packlist = models.JSONField(default=list)
    # [{"article": "a0-xyz", "quantity": 4}, ...]

class Occasion(models.Model):
    calendar_entry = models.OneToOneField(CalendarEntry, ...)
    occasion_type = models.ForeignKey(OccasionType, ...)
    template = models.ForeignKey(OccasionTemplate, null=True, ...)
    location = models.ForeignKey(Location, null=True, ...)
    participant_count = models.IntegerField(null=True)
    attributes = models.JSONField(default=dict)

class RecurrenceRule(models.Model):
    frequency = models.CharField(choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ])
    interval = models.IntegerField(default=1)
    end_date = models.DateField(null=True)
    end_after_occurrences = models.IntegerField(null=True)

class Packlist(models.Model):
    occasion = models.ForeignKey(Occasion, related_name='packlist', ...)
    article = models.ForeignKey(Article, ...)
    quantity = models.IntegerField(default=1)
    status = models.CharField(choices=[
        ('needed', 'Needed'),
        ('reserved', 'Reserved'),
        ('checked_out', 'Checked out'),
        ('returned', 'Returned'),
    ], default='needed')
```

---

## 3. Roles & Permissions System ⚡

### Concept

A **permission construction kit** – every organisation defines their own permission concept. Pre-configured **Role Templates** are offered as suggestions, adoptable with one click and then customizable.

### Connection to Multi-User (§1)

- An `Organisation` has multiple `User`s (via `UserProfile`)
- Each `User` gets one `Role` within that `Organisation`
- All objects are owned by an `Organisation` (via the `organisation` field from §1)
- Permissions are always scoped within the user's `Organisation` – users never see objects from other organisations

### Atomic Permissions

Each permission is `object.scope.action`:

| Object | Scopes | Actions |
|---|---|---|
| `article` | `assigned`, `all` | `view`, `create`, `edit`, `delete`, `move` |
| `storage` | `assigned`, `all` | `view`, `create`, `edit`, `delete` |
| `occasion` | `assigned`, `all` | `view`, `create`, `edit`, `delete`, `manage_packlist` |
| `tag` | `all` | `view`, `create`, `edit`, `delete` |
| `location` | `all` | `view`, `create`, `edit`, `delete` |
| `code` | `all` | `view`, `create`, `delete`, `export` |
| `user` | `all` | `view`, `invite`, `edit_role`, `deactivate` |
| `settings` | `all` | `view`, `edit` |
| `notification` | `all` | `view`, `manage_rules` |
| `export` | `all` | `csv`, `qr_sheet` |
| `calendar` | `all` | `view`, `create_entries` |
| `trash` | `all` | `view`, `restore`, `delete_forever` |

**Scope explanation:**
- `assigned` – only objects explicitly assigned to this user
- `all` – all objects in the organisation

### Role = Named Collection of Permissions

```python
class Role(models.Model):
    organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE)  # roles are per organisation
    name = models.CharField(max_length=50)         # free text: "Lagerchef", "Praktikant", "Mum"...
    is_template = models.BooleanField(default=False)
    permissions = models.JSONField(default=dict)
    # {
    #   "article": ["view_assigned", "move_assigned"],
    #   "storage": ["view_all"],
    #   "occasion": ["view_assigned", "manage_packlist"],
    #   ...
    # }

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE)

class Organisation(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Field-Level Permissions (optional)

Per `ArticleType` / `StorageType` / `OccasionType` and Role, the admin can set field visibility. Default: everything visible.

```python
class FieldPermission(models.Model):
    role = models.ForeignKey(Role, ...)
    content_type = models.ForeignKey(ContentType, ...)  # ArticleType, StorageType, or OccasionType
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    field_permissions = models.JSONField(default=dict)
    # {"anschaffungswert": "hidden", "notiz": "readonly", "zustand": "editable"}
```

Applies to: `ArticleType`, `StorageType`, `OccasionType`.

#### Interaction with `field_config` (§4a–c)

Two mechanisms control field visibility – **both must agree**:

| Mechanism | Question | Level |
|---|---|---|
| `field_config` | Is the field relevant for this **article type**? | Type |
| `FieldPermission` | May this **role** see/edit the field? | Role |

```
Field visible    =  field_config.visible  AND  FieldPermission != "hidden"
Field editable   =  FieldPermission == "editable"
```

Example:

```
ArticleType "Tent":   field_config["anschaffungswert"].visible = true
Role "Helper":        FieldPermission["anschaffungswert"] = "hidden"

→ Helper does NOT see the value (role overrides)
```

```
ArticleType "Office": field_config["anschaffungswert"].visible = false
Role "Admin":         FieldPermission["anschaffungswert"] = "editable"

→ Nobody sees the value (type says: irrelevant)
```

### Pre-configured Role Templates

Created on first start – not active, just templates:

| Template | For whom? | Key Permissions |
|---|---|---|
| **Full Access** | Admin, single user | All permissions, all scopes |
| **Warehouse Team** | Warehouse crew in org | article: view_all, edit, move_all / storage: view_all / occasion: view_all, manage_packlist / export: csv, qr_sheet / calendar: view |
| **Read Only** | Temp helpers, externals | article: view_all / storage: view_all / occasion: view_all / calendar: view |
| **Family** | Private household | All permissions, all scopes (everyone can do everything) |
| **Occasion Manager** | Camp/event planner | article: view_all / occasion: all / calendar: all / export: qr_sheet |
| **Section Lead** | Department head | article: view_all, edit, move_assigned / storage: view_all / occasion: view_assigned, manage_packlist |

### UI Flow

1. Admin opens "Roles & Permissions"
2. Sees: "No roles yet. Start with a template or create from scratch:"
3. Cards: `[Full Access] [Warehouse Team] [Read Only] [Family] [Occasion Manager] [Section Lead] [Empty]`
4. Click template → "Role name?" → "Create" → Done
5. Every role is editable afterwards: checkbox matrix (Object × Scope × Action)
6. Optional: "Field Permissions" tab → per type, per role

---

## 4. Article Management

### 4a–c: Dynamic Article Types (Hybrid Approach) ⚡

### Requirement

The administrator should be able to define different article types. Each article type has its own type-specific fields (e.g. "Tent" has person count, "Food" has expiry date). In the user view, only the fields relevant to the article type are shown. In addition, there are global fields that every article has (condition, value, note, etc.).

### Comparison: Two Approaches

#### Approach A: Boolean Fields in ArticleType (previous approach, extended)

```python
class ArticleType(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=20)

    # For each possible field a boolean pair (show + require):
    show_zustand = models.BooleanField(default=True)
    require_zustand = models.BooleanField(default=False)
    show_anschaffungswert = models.BooleanField(default=False)
    require_anschaffungswert = models.BooleanField(default=False)
    show_kaufdatum = models.BooleanField(default=False)
    require_kaufdatum = models.BooleanField(default=False)
    show_ablaufdatum = models.BooleanField(default=False)
    require_ablaufdatum = models.BooleanField(default=False)
    show_gewicht = models.BooleanField(default=False)
    require_gewicht = models.BooleanField(default=False)
    # ... two booleans for every further field
```

| Pros | Cons |
|---|---|
| ✅ Easy to understand – every developer immediately sees what's going on | ❌ **Every new field needs a migration** – does not scale |
| ✅ Database-level constraints possible | ❌ **ArticleType table becomes huge** – 20+ boolean fields |
| ✅ Django admin usable automatically | ❌ **No type-specific fields** – "Tent" cannot have a "person count" |
| ✅ Query performance: simple WHERE clauses | ❌ **No choice fields** – "Season: 3-Season/4-Season/Winter" not representable |
| | ❌ **No units** – "Weight" is always just a number field |
| | ❌ **Not extensible by power users** – only developers can add new fields |

#### Approach B: JSON Schema

```python
class ArticleType(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=20)
    schema = models.JSONField(default=dict)
    # schema example:
    # {
    #   "fields": [
    #     {"name": "personenzahl", "type": "integer", "label": "Personenzahl",
    #      "required": true, "visible": true, "min": 1, "max": 20},
    #     {"name": "saison", "type": "choice", "label": "Saison",
    #      "required": false, "visible": true,
    #      "options": ["3-Season", "4-Season", "Winter"]}
    #   ]
    # }

class Article(models.Model):
    attributes = models.JSONField(default=dict)
    # {"personenzahl": 8, "saison": "4-Season"}
```

| Pros | Cons |
|---|---|
| ✅ **No migration for new fields** – the administrator defines them himself | ❌ More complex to understand – the JSON structure must be documented |
| ✅ **Type-specific fields** – "Tent" has person count, "Food" has allergens | ❌ Django admin shows JSON as raw text (needs a custom widget) |
| ✅ **Choice fields, units, validation** – everything definable in the schema | ❌ Querying JSON fields is less performant (but SQLite/JSON1 can do it) |
| ✅ **Infinitely extensible** – power users can add fields | ❌ No DB-level constraints (must be validated in app logic) |
| ✅ **Compact model** – ArticleType has only 3 fields | |
| ✅ **Export/import of schemas** – export "tent schema" as JSON | |

### Recommendation: Hybrid Approach

**Global fields** (that every article has) as **real DB columns** – for performance and simple queries:

```python
class Article(models.Model):
    # === Real DB columns (global fields, every article has them) ===
    zustand = models.CharField(max_length=20, choices=[...], default='gut')
    anschaffungswert = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    kaufdatum = models.DateField(null=True)
    ablaufdatum = models.DateField(null=True)
    gewicht_gramm = models.IntegerField(null=True)
    mindestbestand = models.IntegerField(null=True)
    notiz = models.TextField(blank=True)
    standard_lagerplatz = models.ForeignKey(Space, null=True, ...)
    ist_verbrauchsartikel = models.BooleanField(default=False)
    menge = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    mengeneinheit = models.CharField(max_length=20, blank=True)
    # ... existing fields (base, stored, space, code, amount) ...

class ArticleBase(models.Model):
    # === Catalog properties (shared by all instances of this model) ===
    outer_length_mm = models.IntegerField(null=True, blank=True)
    outer_width_mm = models.IntegerField(null=True, blank=True)
    outer_height_mm = models.IntegerField(null=True, blank=True)
    size_class = models.CharField(max_length=2, choices=[
        ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')
    ], null=True, blank=True)
    attributes = models.JSONField(default=dict)   # custom field values (base level)
```

> **Updated:** `bild` is superseded by `ArticleImage` (§15). `masse_mm` is replaced by explicit columns (§16.1). Custom field values (`attributes`) and dimensions live on `ArticleBase` (§25).

**ArticleType** gets both – visibility configuration for global fields PLUS schema for type-specific fields:

```python
class ArticleType(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=20)

    # Visibility/required of global fields (as JSON for flexibility)
    field_config = models.JSONField(default=dict)
    # {
    #   "zustand": {"visible": true, "required": false},
    #   "anschaffungswert": {"visible": false, "required": false},
    #   "gewicht_gramm": {"visible": true, "required": false}
    # }

    # Type-specific fields
    custom_fields_schema = models.JSONField(default=dict)
    # {
    #   "fields": [
    #     {"name": "personenzahl", "type": "integer", "label": "Personenzahl", ...}
    #   ]
    # }
```

> **Note:** Field visibility is further refined per role via `FieldPermission` (§3). Both must agree – see §3 for the resolution rules.

### Result of the Hybrid Approach

| Property | Achieved by |
|---|---|
| Performance for global fields | Real DB columns, native SQL queries |
| Flexibility for type-specific fields | JSON schema, no migrations needed |
| Configurability | `field_config` controls visibility/required of global fields |
| Simplicity | Global fields are self-explanatory, JSON only for power users |

---

### 4d: Sets / Bundles ⚡

#### Requirement

An article can be a "set" consisting of several individual articles (e.g. "Tent Set Large" = 1× yurt + 12× peg + 1× hammer + 4× guy rope). When the set is moved, all individual parts are moved along with it. On return, it is checked whether all parts are complete.

#### Implementation

```python
class ArticleSetItem(models.Model):
    set = models.ForeignKey(
        'article.Article',
        on_delete=models.CASCADE,
        related_name='set_items'
    )
    article = models.ForeignKey(
        'article.Article',
        on_delete=models.CASCADE,
        related_name='contained_in_sets'
    )
    menge = models.IntegerField(default=1)

    class Meta:
        unique_together = ('set', 'article')
```

#### Behavior

| Action | Behavior |
|---|---|
| **Store set** | All `set_items` are stored along with it (same target space) |
| **Remove set** | All `set_items` are removed along with it (`stored = None`) |
| **Return check** | UI shows: "Expected: 18 parts / Present: 17 – missing: 1× peg" |
| **Dissolve set** | Set is deleted, individual parts remain independently |
| **Replace individual part** | Remove article from set, add a new one |

#### UI

- When creating an article: checkbox "Is a set" → below it a table for adding individual parts
- Detail view of a set: list of contained articles with quantities
- Movement: when a set is scanned, all individual parts are loaded into the buffer

---

### 4e: Article History / Audit Trail ⚡

#### Requirement

Every action on an article should be traceable: who did what and when? This serves traceability and helps with troubleshooting ("Who moved the tent last?").

#### Implementation

> **Updated:** The article history is now a filtered view of the unified `AuditLog` (§32). The separate `ArticleLog` model is no longer needed.

The article detail view shows all `AuditLog` entries where `content_object` is this article.

#### Action Types

| Action | Description | `detail` content |
|---|---|---|
| `created` | Article created | `{"article_type": "Zelt", "name": "Jurte 8-Personen"}` |
| `moved` | Article relocated | `{"from_space": "s0-abc", "to_space": "s0-def"}` |
| `removed` | Article removed | `{"from_space": "s0-abc"}` |
| `quantity_changed` | Quantity changed | `{"old": 10, "new": 8, "reason": "Verbrauch"}` |
| `damaged` | Marked as damaged | `{"note": "Gestänge gebrochen"}` |
| `repaired` | Marked as repaired | `{"note": "Gestänge ersetzt"}` |
| `attributes_changed` | Properties changed | `{"changed_fields": ["zustand", "notiz"]}` |
| `set_modified` | Set composition changed | `{"added": ["a0-xyz"], "removed": ["a0-abc"]}` |

#### UI

- In the article detail view: timeline of the last actions
- Filter: "All movements by user X", "All changes this week"
- Export the history as CSV

---

## 5. QR Code System

### 5a: QR Sheet Printing ⚡

### Requirement

Generic print configurator for QR code sheets. The article selection is done via the [Query Builder](#9-query-builder-) (see §9).

### Layout Options

- **Label format**: A4 with grid (2×4, 3×7, 4×10, etc.)
- **QR code size**: Small / Medium / Large
- **Content**: QR code only / QR code + article name / QR code + name + symbol
- **Sorting**: By name, by storage location, by code, by article type
- **Preview**: Live preview before printing

### Output

- Printable HTML page (browser print via `window.print()`)
- PDF download (optional, via WeasyPrint or similar)

### Storage QR Codes

Not only articles but also **storage (storage locations)** have QR codes – these should likewise be printable on sheets:

- Separate section in the print dialog: "Articles" / "Storage" (or both)
- Selection of storage entries via the Query Builder (§9) – e.g. "all shelves in building A"
- Layout as for articles (grid, size, content with name/designation)
- Use: QR labels to stick on shelves, rooms, crate locations

---

### 5b–c: QR Workflow ⚡

#### Requirement

The QR code workflow should become smoother and more powerful. Three core functions:

1. **"Where is...?"** – scan or search an article → show current storage location + default storage location
2. **"Where should it go?"** – show the default storage location prominently, with one-click storage
3. **Mass scan / inventory** – scanner on, scan all articles → compare with target state

#### Implementation

##### "Where is...?" in Search

- The search field gets a "Where is...?" button next to the normal search
- Scan an article or enter a name → result shows:
  - Article name + symbol
  - **Current storage location** (with breadcrumb: Building > Room > Shelf > Compartment)
  - **Default storage location** (if different, highlighted in color)
  - "Last movement X days ago by user Y"
  - Button: "Navigate here" (shows the storage location hierarchy)

##### "Where should it go?" on Storage

- Article is scanned → system checks:
  - Does the article have a `standard_lagerplatz`?
  - If yes: "Default location: Shelf 3, Compartment B – store here?" with a green button
  - If no: Normal storage location selection
- After successful storage: toast "Article X was stored in Shelf 3, Compartment B"

##### Inventory Mode

- New mode on the dashboard / in the Movement page: "Start inventory"
- Scanner is permanently active
- Every scanned article is checked off in a list
- Display: "45/120 articles scanned"
- Deviations are marked:
  - Article scanned, but system says it should be elsewhere → ⚠️ "Should be in Room 2, was scanned in Room 1"
  - Article not scanned (after time elapsed) → ❓ "Not found yet"
- At the end: inventory report exportable as CSV/PDF

##### QR Code at the Storage Location

- Every storage already has a QR code (via `Space` → `UuidCode`)
- Scan storage location → show all articles contained in it
- Workflow: scan article (buffer) → scan storage location → all buffered articles are stored (already exists, UI is being optimized)

---

## 6. Notification System ⚡

### Concept

Configurable notifications with multiple triggers. Recipients are defined via the Roles system (§3), individual users, or by relation (responsible user). Delivery via In-App, Email (with customizable templates), or Webhook. Optional daily/weekly digest.

### Triggers & Default Recipients

| Trigger | Default Recipients | Description |
|---|---|---|
| `expiry_date_reached` | Admin + Warehouse Operator | "Article X expires in 7 days" |
| `minimum_stock_undercut` | Admin + Warehouse Operator | "Only 2 of 10 camp beds left" |
| `maintenance_due` | Admin + Warehouse Operator | "Tent needs maintenance (interval exceeded)" |
| `not_moved_for_long` | Admin | "Article X not moved in 90 days – still there?" |
| `return_overdue` | Admin + Occasion responsible | "Material from summer camp not yet returned" |
| `article_damaged` | Admin + Warehouse Operator | Immediately when status changes to "damaged" |
| `occasion_upcoming` | Occasion responsible + assigned helpers | "Summer camp starts in 7 days" |
| `inventory_due` | Admin + Warehouse Operator | "Last inventory in Room 2 was 6 months ago" |

### Recipients (per rule, combinable)

```
Notify:
  ☑ By Role:      [Warehouse Team ▼]  [+ add role]
  ☑ By User:      [Anna ▼]            [+ add user]
  ☑ Responsible:  ☑ (the user assigned to the related article/occasion)
```

References the Role model from §3. Individual users can be added on top.

### Delivery Modes

| Mode | Behavior |
|---|---|
| **Instant** | Notification sent immediately when triggered |
| **Daily digest** | Collected, sent once per day (configurable time, default 08:00) |
| **Weekly digest** | Collected, sent once per week (configurable weekday, default Monday 09:00) |

### Channels (per rule, combinable)

```
Channels:
  ☑ In-App   (always on)
  ☑ Email    → Template: [Standard "article_expiry" ▼] [edit] [preview]
  ☐ Webhook  → URL: [________________________]
```

### Email Templates

Per trigger type, a standard template is provided – customizable by the admin:

```
Subject: ⚠️ {{article_name}} expires in {{threshold_days}} days

Body:
Hello {{user_name}},

the article "{{article_name}}" ({{article_code}}) 
expires on {{expiry_date}} – that's in {{threshold_days}} days.

→ View article: {{link}}

---
Sent by little_WMS – Notification settings: {{settings_link}}
```

**Available variables (depend on trigger type):**

| Variable | Available for |
|---|---|
| `{{user_name}}` | always |
| `{{article_name}}`, `{{article_code}}` | article-related triggers |
| `{{occasion_name}}` | occasion-related triggers |
| `{{threshold_days}}`, `{{threshold_value}}` | triggers with threshold |
| `{{link}}` | always (deeplink to object) |
| `{{settings_link}}` | always (link to notification settings) |

### Webhook (future)

URL + optional secret → POST with JSON payload. Enables Slack, Discord, custom integrations.

### Notification Center (UI)

- Bell icon in navigation with unread badge
- Dropdown: last 5 notifications
- "View all" → notification page with:
  - Filter: read/unread, by type
  - Each notification has a deeplink (e.g. "→ View article")
  - "Mark all as read"

### Data Model

```python
class NotificationRule(models.Model):
    trigger_type = models.CharField(max_length=30, choices=[...])
    active = models.BooleanField(default=True)
    threshold_days = models.IntegerField(null=True)
    threshold_value = models.IntegerField(null=True)

    # Recipients
    notify_roles = models.ManyToManyField(Role, blank=True)
    notify_users = models.ManyToManyField(User, blank=True, related_name='notification_rules')
    notify_responsible = models.BooleanField(default=False)

    # Delivery
    digest_mode = models.CharField(choices=[
        ('instant', 'Instant'),
        ('daily', 'Daily digest'),
        ('weekly', 'Weekly digest'),
    ], default='instant')
    channel_in_app = models.BooleanField(default=True)
    channel_email = models.BooleanField(default=False)
    channel_webhook = models.URLField(null=True, blank=True)

class EmailTemplate(models.Model):
    trigger_type = models.CharField(max_length=30, unique=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_default = models.BooleanField(default=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rule = models.ForeignKey(NotificationRule, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 7. Technical Architecture

### 7a: API-First ⚡

#### Requirement

The existing DRF serializers (so far rudimentary) should be expanded into a complete REST API. This later enables a PWA, native app, or external integration without rebuilding the entire logic.

#### Implementation

- **Serializer per model**: For every model (`Article`, `Storage`, `Location`, `Tag`, `ArticleType`, `StorageType`, `Space`, `AuditLog`, `ArticleSetItem`, `Notification`, etc.) a complete `ModelSerializer`.
- **ViewSets**: `ModelViewSet` for CRUD operations, with `permission_classes` that are later coupled to the role system.
- **Service layer**: Business logic (storing, removing, set movement, inventory) is extracted into service classes. Both the HTMX views and the API ViewSets use the same services.
- **API router**: Register all ViewSets under `/api/v1/`.
- **Documentation**: DRF Browsable API + optional `drf-spectacular` for OpenAPI/Swagger.

#### Service Layer Example

```python
# src/movement/services.py

class MovementService:
    """Business logic for storing/removing – used by HTMX views AND API."""

    @staticmethod
    def store_article(article: Article, target_space: Space, user: User) -> AuditLog:
        """Stores an article in a space."""
        old_space = article.stored
        article.stored = target_space
        article.save()
        return AuditLog.objects.create(
            content_object=article,
            user=user,
            action='moved',
            changes={'space': {'old': str(old_space), 'new': str(target_space)}}
        )

    @staticmethod
    def remove_article(article: Article, user: User) -> AuditLog:
        """Removes an article."""
        old_space = article.stored
        article.stored = None
        article.save()
        return AuditLog.objects.create(
            content_object=article,
            user=user,
            action='removed',
            changes={'space': {'old': str(old_space), 'new': None}}
        )
```

---

### 7b: Testing Strategy ⚡

#### Requirement

There are currently hardly any tests. Before larger changes are made to the system used in production, the current state must be secured with tests.

#### Implementation

##### 1. Characterization Tests (now)

Tests that document and secure the current behavior – without changing it:

- **Model tests**: Are articles/storage/locations created correctly? Do soft-delete and undelete work?
- **View tests**: Do all pages return HTTP 200? Do add/update/delete work?
- **Movement tests**: Does store/remove work correctly? Is the space validation respected?
- **QR code tests**: Are codes generated and assigned correctly?

##### 2. Fixtures

A test database with realistic data:
- 3 article types (tent, tool, kitchen)
- 20 articles
- 5 storage locations (building > room > shelf > compartment)
- 3 tags
- 1 user

##### 3. Regression Tests (on every change)

- After every migration: run the characterization tests
- Before every merge: full test run

##### 4. Migration Tests

- Test that a migration can be run forward AND backward
- Test that existing data is still readable after the migration

#### Test Structure

```
src/
  article/
    tests/
      __init__.py
      test_models.py
      test_views.py
      test_services.py
  storage/
    tests/
      ...
  movement/
    tests/
      ...
  conftest.py          # Shared fixtures
```

---

### 7c: Migrations – Safe Handling ⚡

#### Requirement

Since the system is already used in production, every schema change must be safe and backward-compatible.

#### Rules

1. **Every migration gets a backward migration** – no `makemigrations` without a verifiable rollback.
2. **Descriptive migration names**: `makemigrations --name "add_owner_field_to_article"` instead of `0003_auto`.
3. **Before every migration: backup** of the SQLite database (`data/wms.sqlite3`).
4. **No `--merge` without manual review** of the migrations to be merged.
5. **Data migrations** (e.g. creating standard configurations) always with `elidable=True` and a check whether data already exists.
6. **Test migrations**: forward + backward + forward again must be error-free.

#### Workflow

```bash
# 1. Backup
cp data/wms.sqlite3 data/wms.sqlite3.backup_$(date +%Y%m%d_%H%M%S)

# 2. Create migration
python manage.py makemigrations --name "descriptive_name"

# 3. Check migration (forward)
python manage.py migrate

# 4. Check migration (backward)
python manage.py migrate app_name $(python manage.py showmigrations --plan | grep app_name | tail -2 | head -1 | awk '{print $2}')

# 5. Forward again
python manage.py migrate

# 6. Run tests
python manage.py test
```

---

## 8. Standard Configurations & Onboarding ⚡

### Philosophy: Article vs. Storage

> **Everything easily movable = Article. Everything hard to move = Storage.**  
> Boxes, crates, bags are Articles – they can contain other articles (`article_toggle_space = True`).

### Standard Storage Types (hard to move)

| Storage Type | Description |
|---|---|
| Building | Main building |
| Room | A room in the building |
| Shelf | A shelf in the room |
| Compartment | A compartment in the shelf |
| Cabinet | A cabinet |
| Container | Shipping/storage container |
| Vehicle | Car, van, trailer (when used as storage) |

### Standard Article Types (easily movable)

| Article Type | `article_toggle_space` | Typical Custom Fields |
|---|---|---|
| Tent | ✅ Yes | Person count, water column, season, pole type |
| Kitchen | ❌ No | Dishwasher safe?, material |
| Tool | ❌ No | Manufacturer, serial number, maintenance interval |
| Office | ❌ No | – |
| Sport | ❌ No | Sport type |
| Tech | ❌ No | Power consumption (watt), battery type |
| Box/Crate | ✅ Yes | Dimensions, material, stackable?, load capacity |
| Consumable | ❌ No | Expiry date, hazardous? |
| Other | ❌ No | – |

### Standard Role Templates

| Template | For whom? |
|---|---|
| Full Access | Admin, single user |
| Warehouse Team | Warehouse crew in org |
| Read Only | Temp helpers, externals |
| Family | Private household |
| Occasion Manager | Camp/event planner |
| Section Lead | Department head |

### Standard Notification Rules

All disabled – admin activates as needed.

### Onboarding Wizard

On first start, a guided setup helps configure the system. It can be **skipped**, **restarted later** (from Settings), and **scripted** (via env vars or management command for automated deployments).

#### Wizard Flow

**Step 1 – Usage:**
```
How will you use little_WMS?

  ( ) For an organization (youth group, club, church...)
  ( ) For private use (household, family...)
  ( ) Both
```

**Step 2 – Context (depends on Step 1):**

*If organization:*
```
What kind of organization?

  [ ] Youth / camp (tents, outdoor gear...)
  [ ] Club / association (event equipment...)
  [ ] Church / religious (event materials...)
  [ ] Other: [____________]
```

*If private:*
```
What do you want to manage?

  [ ] Camping & outdoor gear
  [ ] Party & event equipment
  [ ] Household items
  [ ] Moving boxes & storage
  [ ] Other: [____________]
```

**Step 3 – Team size:**
```
How many people will use the system?

  ( ) Just me
  ( ) 2–5 people
  ( ) 6–20 people
  ( ) 20+ people
```

**Step 4 – Suggestions:**
```
Based on your answers, we suggest:

Article Types:         Role Templates:
  ☑ Tent                 ☑ Full Access
  ☑ Kitchen              ☑ Warehouse Team
  ☑ Tool                 ☑ Read Only
  ☐ Office               ☐ Family
  ☑ Sport                ☐ Occasion Manager
  ☐ Tech                 ☐ Section Lead
  ☑ Box/Crate
  ☐ Consumable         Storage Types:
  ☐ Other                 ☑ Building
                           ☑ Room
                           ☑ Shelf
                           ☑ Compartment
                           ☐ Cabinet
                           ☐ Container
                           ☐ Vehicle

        [Create]   [Skip – I'll configure manually]
```

**Step 5 – Done:**
```
All set! You can change everything later in Settings → Configuration.

  [Go to Dashboard]
```

#### Scripting / Automation

For automated deployments (Docker, CI), the wizard can be bypassed:

```bash
# Environment variable
ONBOARDING_SKIP=true

# Or management command
python manage.py setup_defaults --profile=camp_organization
```

Available profiles: `camp_organization`, `club`, `church`, `private_camping`, `private_household`, `minimal`.

### Technical Implementation

- **Data Migration**: Creates defaults only if tables are empty (`elidable=True`)
- **Wizard state**: Stored in `Settings` model (`onboarding_completed = BooleanField`)
- **Defaults are normal DB records** – deletable, renameable, extendable

---

## 9. Query Builder ⚡

### Concept

A visual, Django-filter-inspired query builder for power users. Instead of typing search queries, the user builds filters graphically – field by field, with AND/OR logic and nested parentheses (groups). Available in all list views, the QR print dialog, export, and packlist builder.

### How It Looks

```
┌──────────────────────────────────────────────────────────────┐
│ ┌─ AND ──────────────────────────────────────────────── [−] ┐│
│ │  article_type   =    Tent                                    ││
│ │  condition      =    good                                    ││
│ │ ┌─ OR ────────────────────────────────────────────── [−] ┐  ││
│ │ │  weight_gramm  >    5000                                   ││
│ │ │  tag           contains  summer                            ││
│ │ └────────────────────────────────────────────────────────┘  ││
│ └───────────────────────────────────────────────────────────┘  │
│                                                      [+]       │
└──────────────────────────────────────────────────────────────┘
```

This produces: **(article_type = Tent AND condition = good AND (weight > 5000 OR tag contains summer))**

### Building Blocks

**Each condition row:**
```
[ Field ▼ ]  [ Operator ▼ ]  [ Value ]
```

**Operators (depend on field type):**

| Field Type | Operators |
|---|---|
| Text | `=`, `≠`, `contains`, `starts with`, `ends with`, `is empty`, `is not empty` |
| Number | `=`, `≠`, `<`, `>`, `≤`, `≥`, `between`, `is empty` |
| Date | `=`, `≠`, `before`, `after`, `between`, `in last X days`, `is empty` |
| Choice | `=`, `≠`, `is any of`, `is none of` |
| Boolean | `is true`, `is false` |
| ForeignKey | `=`, `≠`, `is empty` |

**Groups = Parentheses:**
- `+ Group` → new parenthesized block, default AND
- `+ Condition` → new row inside current group
- Click `AND`/`OR` label → toggles the group operator
- `[−]` on a group → deletes the entire parentheses block
- `[−]` on a row → deletes only that condition
- Groups can be nested arbitrarily deep
- Visual: indented, color-coded border (AND = blue, OR = orange)

### Presets

- Users can save filter combinations as **named presets** ("My damaged tents", "Everything in Room 2")
- Presets are available across all views
- Presets can be shared within the organisation

### Where the Query Builder Is Used

| View | Access |
|---|---|
| Article list | "Advanced Search" button opens builder |
| Storage list | "Advanced Search" button |
| QR Sheet Print (§5a) | The entire article selection IS the query builder |
| Export | "What should be exported?" |
| Occasion packlist | "Add articles to packlist" |
| Movement search | Quick search + "Advanced" |
| Dashboard widgets | Widget based on saved preset |

### Quick Search vs. Query Builder

| | Quick Search (existing) | Query Builder (new) |
|---|---|---|
| Input | Single text field | Visual rows |
| Searches in | Name, code | Any field |
| Logic | Always OR | AND/OR with parentheses |
| Target group | All users | Power users |
| Access | Always visible | "Advanced" button |

### Technical Implementation

**Client:** HTMX + Alpine.js (or vanilla JS). The builder produces a JSON object describing the query.

**Server:** A `QueryParser` service translates JSON into Django `Q` objects:

```python
# Input (from client)
{
    "type": "AND",
    "conditions": [
        {"field": "article_type__name", "op": "eq", "value": "Tent"},
        {"field": "condition", "op": "eq", "value": "good"},
        {
            "type": "OR",
            "conditions": [
                {"field": "weight_gramm", "op": "gt", "value": 5000},
                {"field": "tags__name", "op": "contains", "value": "summer"}
            ]
        }
    ]
}

# Translation (server)
Q(article_type__name="Tent") & Q(condition="good") & (Q(weight_gramm__gt=5000) | Q(tags__name__icontains="summer"))
```

**Security:**
- Whitelist of allowed fields per model
- Whitelist of allowed operators per field type
- Value validation (type check, max length, etc.)

### NOT Groups

Each group can additionally be negated ("NOT") – e.g. to express "everything EXCEPT damaged articles":

```
┌─ NOT ────────────────────────────────────────────── [−] ┐
│  condition  =  damaged                                    │
└──────────────────────────────────────────────────────────┘
```

- Toggle: clicking the "NOT" label switches the group between normal and negated
- Visual: marked red / struck-through border
- Server: translation into `~Q(...)`

### Drag & Drop

To reorder conditions and groups:

- Drag a row/group to another position
- The target indentation shows the new nesting
- Drop targets: inside a group (as a condition) or between groups (as a new group)

```python
# NOT translation
~Q(condition="damaged")   # → Q(condition="damaged") with negation
```

---

## 10. Saved Views & Share Links ⚡

### Concept

Users can create custom list views (based on the Query Builder §9) and save them with their own name, sort order, column selection, and display mode. These views can be shared via links – internally or externally – and the links can carry their own permissions, independent of the recipient's role.

### Saved Views

A Saved View stores:

- **Query** – the Query Builder JSON (filters, AND/OR/NOT, parentheses)
- **Sort** – e.g. `{"field": "name", "dir": "asc"}`
- **Columns** – which columns are shown, e.g. `["name", "code", "condition", "location"]`
- **Display mode** – list / cards / table
- **Name + description**
- **Owner + organisation**
- **Shared within organisation?** (yes/no)

Saved Views can also be used as dashboard widgets.

### Share Links

A Share Link shares a Saved View. Three access modes (configurable per link):

| Access Mode | Description |
|---|---|
| **Public** | No login required – anyone with the link |
| **Guest token** | One-time / guest access token |
| **Internal** | Only users of the organisation (login required) |

### Link Permissions

Per link, configurable which actions the recipient may perform:

- **Default: `view` only**
- Optional: `reserve`, `check_out`, `check_in`, `edit`, `quantity_change`

Example: Helper Max normally has no right to reserve articles. But a shared link "Material for Summer Camp" grants him `reserve` for exactly the articles in that view.

### Security Options (all configurable)

- **Expiry date** – link invalid after date
- **Single use** – link can be used once
- **Revocable** – deactivate link at any time
- **Password / PIN** – optional protection for external links

### Permission Scope

The link permission applies only to the articles in the view:

- If only **part of a set** is in the view → only that part can be acted on
- If a **whole set** is in the view → the set's individual articles are automatically included (e.g. reserved together)

### Data Model

```python
class SavedView(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE)
    query = models.JSONField(default=dict)          # Query Builder JSON
    sort = models.JSONField(default=dict)           # {"field": "name", "dir": "asc"}
    columns = models.JSONField(default=list)        # ["name", "code", "condition"]
    display_mode = models.CharField(choices=[
        ('list', 'List'), ('cards', 'Cards'), ('table', 'Table')
    ], default='list')
    is_shared = models.BooleanField(default=False)  # within organisation
    created_at = models.DateTimeField(auto_now_add=True)

class ShareLink(models.Model):
    saved_view = models.ForeignKey(SavedView, on_delete=models.CASCADE, related_name='share_links')
    token = models.CharField(max_length=64, unique=True)  # random, URL-safe
    access_mode = models.CharField(choices=[
        ('public', 'Public (no login)'),
        ('guest', 'Guest token'),
        ('internal', 'Internal (organisation only)'),
    ], default='internal')
    permissions = models.JSONField(default=list)    # ["view"] default
    expires_at = models.DateTimeField(null=True, blank=True)
    single_use = models.BooleanField(default=False)
    used_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)   # revoke
    password_hash = models.CharField(max_length=128, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Permission Resolution

When a request arrives with a share-link token:

1. Validate token (exists, active, not expired, not used up)
2. Check password (if set)
3. Effective permissions = link permissions (NOT the user's role)
4. Scope = articles of the Saved View
5. Execute action (e.g. reserve)

This is a **capability URL** – the link itself is the permission.

### UI

- "Save as View" button in every list view
- "My Views" overview (own + shared)
- Per view: "Share" → dialog with access mode, permissions, expiry, password
- Copy link
- "Active Links" overview with revoke button

---

## 11. Movement Redesign ⚡

### Concept

The Movement view is the heart of the system: fast, clear storing, moving, and removing of articles. Redesign based on the principle **"Scan → See → Confirm"**.

### Current State (as-is)

- Frontend: `movement.html` with jQuery, scanner always active
- On scan → `GET /movement/request?code=...` → JSON info
- Mode toggle: Store (green) / Remove (red)
- Store: buffer articles, then scan location → POST all at once
- Remove: each scan immediately POSTs (one at a time)
- Quick search dropdown

### Bugs Found (to fix)

| # | Location | Problem |
|---|---|---|
| 1 | `movementStore` | No error handling: `DoesNotExist` → 500; unknown prefix → `UnboundLocalError` |
| 2 | `movementStore` | Broken toast: always "Error" with `str(hallo)` (debug leftover) |
| 3 | `movementStore` | No validation: target space active? article storable? self-storage? |
| 4 | `movementStore` | No transaction: partial state on mid-loop failure |
| 5 | `movementRemove` | No error handling: `DoesNotExist` → 500 |
| 6 | `movementRemove` | Only reads `articleCode1` |
| 7 | `movementCodeInfo` | `request.GET['code']` without `.get()` → KeyError |
| 8 | `movementSearch` | `request.GET['search']` without `.get()` → KeyError |
| 9 | everywhere | No audit trail (see §4e) |

### New UX Design

#### Visible Buffer

```
┌─────────────────────────────────────────────┐
│  Mode:  [ Store ] [ Remove ]                 │
│                                              │
│  ┌─ Active (last scanned) ────────────────┐ │
│  │ 🏕️ Jurte 8P        current: Room 2      │ │
│  │ [Move] [Remove] [Qty] [Damaged]         │ │
│  └─────────────────────────────────────────┘ │
│                                              │
│  ┌─ Buffer (2) ───────────────────────────┐ │
│  │ 🛏️ Camp bed        current: Room 1  [×] │ │
│  │ 🔨 Hammer          current: —       [×] │ │
│  └─────────────────────────────────────────┘ │
│                                              │
│  Target:  [ scan location... ]               │
│  ┌─────────────────────────────────────────┐ │
│  │ 📦 Shelf 3 / Compartment B              │ │
│  │    [ Store ]   [ Clear ]                │ │
│  └─────────────────────────────────────────┘ │
│                                              │
│  [ ↶ Undo last action ]                      │
└─────────────────────────────────────────────┘
```

#### Two Modes

- **Store/Move** (to a location): buffer articles → scan/select target → confirm
- **Remove** (out of storage): buffer articles → confirm → all removed at once

#### Location-First

Scanning a **Storage** first sets it as target → each subsequently scanned article moves there immediately (fast bulk storing).

#### Container Handling (Smart Default)

| Scan | Behavior |
|---|---|
| **Storage** (s0) | Always becomes target |
| **Article** (a0) | Goes to buffer |
| **Article with active space** (container), target empty | Smart default: becomes target, with visible hint "Container detected – set as target. [Treat as article]" |
| **Article with active space**, target already set | Goes to buffer |

The hint makes the smart default visible and reversible with one tap.

#### Quick Actions + Buffer

- The **last scanned** article is "active" and shows a card with quick actions: Move, Remove, Change quantity, Mark damaged, Set as target (containers only)
- Scanning the next article pushes the previous one into the buffer (compact list)
- The active article stays on top with its actions

#### Undo (two levels)

1. **"Undo last action"** button – reverts the last step
2. **Session list** – walkable, each entry individually undoable

```
┌─ Session ───────────────────────────────────┐
│ ✓ 14:32  3 articles → Shelf 3       [↶]     │
│ ✓ 14:28  Jurte 8P removed           [↶]     │
│ ✓ 14:25  Camp bed → Box A           [↶]     │
└─────────────────────────────────────────────┘
```

Builds on `AuditLog` (§32) – each movement is a log entry, undo creates the counter-entry.

#### Sound & Haptic Feedback

- **Sound** on successful scan (short beep), **different tone** on error
- **Vibration** (on mobile) on success/error
- **Configurable** in settings: sound on/off, vibration on/off, volume

### Architecture

- **Service layer** (`MovementService`) – logic out of views (§7a)
- **HTMX instead of jQuery** – consistent with the rest of the app
- **Transactions** – `transaction.atomic()` for multi-movements
- **Centralize prefix logic** – no scattered "s0"/"a0"
- **Tests** – characterization tests first (§7b)

### Data Model Additions

```python
class MovementSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

# AuditLog (§32) gets an optional session reference:
# session = models.ForeignKey(MovementSession, null=True, blank=True, on_delete=models.SET_NULL)
# undone = models.BooleanField(default=False)
```

The session list is built from `AuditLog` entries of the current session. Undo creates a counter-entry and marks the original as `undone`.

### Settings (configurable)

- Sound on/off
- Vibration on/off
- Volume
- Smart default for containers on/off

---

## 12. Mobile & Navigation ⚡

### Concept

One responsive codebase (no separate templates). The layout adapts via CSS media queries + touch detection. The **sidebar replaces the top navbar entirely**.

### Device Detection (multi-stage)

- **CSS media queries** (viewport width) – primary for layout
- **Touch detection** (`@media (pointer: coarse)`) – for touch behavior
- **User-Agent** – coarse hint only (unreliable)
- **Manual override** – always available ("Auto / Always mobile / Always desktop")

### Sidebar (replaces navbar)

The sidebar replaces the top navigation bar. It is a vertical rail:

**Mobile:**
- Narrow bar on the right edge (right-handed) / left (left-handed)
- Full height
- Logo at top
- Narrow by default (icons only)
- A toggle symbol under the logo expands it (shows text)

**Desktop:**
- Default on the left, configurable in settings (left/right)
- Narrow by default
- Auto-expands on hover (shows text)

### Sidebar Structure (top to bottom)

```
┌────┐
│ 🏠 │  ← Logo (top)
├────┤
│ 📊 │  ← Quick nav 1: Dashboard
│ 📦 │  ← Quick nav 2: most used
│ 📅 │  ← Quick nav 3: most used
├────┤
│ ⚙️ │  ← Context action: least important
│ 📤 │  ← Context action
│ ➕ │  ← Context action
│ 🗑️ │  ← Context action
│ ⬇️ │  ← Context action: most important (bottom)
└────┘
```

Rule: Logo top → quick nav → context actions, ordered least important (top) to most important (bottom).

### Quick Navigation

3 targets:

1. Dashboard (hub) – always
2. Most-used view #1 (not the current view)
3. Most-used view #2 (not the current view)

Determination: auto-tracked frequency, user can override in settings.

### Search Field

- Separate bar, spans width up to the sidebar
- Desktop: top
- Mobile: bottom
- Not expandable from the sidebar (rejected as gimmicky)

### Sidebar Contents per View (draft – to be refined)

| View | Context actions (bottom = most important) |
|---|---|
| Hub | Settings, Notifications |
| Article list | Advanced search, Export, Delete, Add |
| Article detail | History, Delete, Edit, Move |
| Storage list | Advanced search, Export, Delete, Add |
| Movement | Undo, Remove, Store/Move |
| Calendar | Filter, Today, Add occasion |
| Settings | Reset, Save |

Existing bottom-right buttons (Add/Delete/Export in lists) move into the sidebar.

### Settings

- Sidebar position: left / right (desktop)
- Sidebar position: left / right (mobile, for handedness)
- Sidebar behavior: auto-expand on hover (desktop) on/off
- View mode: Auto / Always mobile / Always desktop
- Quick nav targets: auto / manual

### Accessibility

- Sidebar keyboard/screenreader accessible
- Content area gets padding so the sidebar never covers content

---

## 13. Tags ⚡

### Concept

Tags are the flexible layer above the system:

| Concept | Character |
|---|---|
| **ArticleType** | Strict classification – exactly one per article |
| **Location** | Physical place |
| **Occasion** | Time-bound |
| **Tag** | Flexible, many per object, hierarchical, cross-cutting |

Tags group articles and storages across types, locations, and occasions.

### Core Integration

```python
class Article(models.Model):
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')

class Storage(models.Model):
    tags = models.ManyToManyField(Tag, blank=True, related_name='storages')
```

### Tag Extensions

```python
class Tag(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=20)
    parent = SelfForeignKey('self', ...)          # existing
    color = models.CharField(max_length=7, default='#6c757d')  # NEW
    icon = models.CharField(max_length=20, blank=True)         # NEW
    code = models.OneToOneField(UuidCode, ...)    # existing
```

### Tag Categories

```python
class TagCategory(models.Model):
    name = models.CharField(max_length=50)        # "Status", "Group", "Season"
    color = models.CharField(max_length=7)
    allow_multiple = models.BooleanField(default=True)
    inherit_to_contents = models.BooleanField(default=False)
```

Example categories:

| Category | Example Tags | Behavior |
|---|---|---|
| **Status** | damaged, to check, retired | `allow_multiple=False`, triggers notifications |
| **Group** | Summer camp 2026, Kitchen, First aid | `allow_multiple=True`, for filtering |
| **Season** | Summer, Winter | `allow_multiple=True` |
| **Department** | North, South | `allow_multiple=True` |

### Tag Inheritance (configurable per category)

Each category has `inherit_to_contents` (on/off):

- **ON**: an article stored inside a tagged container/storage inherits the tag for filtering
- **OFF**: tags only apply to the directly tagged object

Example:

- Category "Group" has `inherit_to_contents = True`
- Box "Crate A" is tagged "Summer camp 2026"
- Tent inside Crate A → counts as "Summer camp 2026" when filtering
- So "show all Summer camp 2026" finds the tent too

- Category "Status" has `inherit_to_contents = False`
- Box "Crate A" is tagged "damaged"
- Tent inside → does NOT inherit "damaged" (the tent itself is fine)

### Usage

| Where | How |
|---|---|
| **Query Builder (§9)** | Filter "tag contains X" |
| **QR Printing (§5a)** | "all articles with tag X" |
| **Saved Views (§10)** | Tag filter in saved views |
| **Packlists (§2)** | "add all articles with tag 'Kitchen' to packlist" |
| **Notifications (§6)** | "notify when article with tag 'damaged' is moved" |
| **Dashboard widgets** | "all articles with tag 'to check'" |
| **Search** | Tag chips as quick filters |

### UI

- **Tag chips** (colored) on article/storage detail pages
- **Tag selector** with autocomplete when editing
- **Tag management** (CRUD already exists)
- **Tag overview**: all tags with count of assigned objects
- **Quick filter**: tag chips above the list to toggle on/off

### Standard Tags (provided, overwritable)

| Category | Tags |
|---|---|
| Status | damaged, to check, retired |
| Season | Summer, Winter |

Rest empty – the user creates their own.

---

## 14. Internationalization ⚡

### Concept

- **UI texts** are translated (Django i18n)
- **User content** (article names, tags, locations) is NOT translated – it is data
- **Standard configurations** are created in the user's language at onboarding

### Languages

- German (de)
- English (en)
- Extensible (more languages via locale files)

### Implementation

```python
# settings.py
LANGUAGES = [
    ("de", "Deutsch"),
    ("en", "English"),
]
LOCALE_PATHS = [BASE_DIR / "locale"]
```

- `LocaleMiddleware` in the middleware chain
- Templates: `{% trans "Add article" %}` / `{% blocktrans %}...{% endblocktrans %}`
- Python: `from django.utils.translation import gettext_lazy as _`
- Locale files: `locale/de/LC_MESSAGES/django.po`, `locale/en/...`
- Language switcher in settings
- `UserProfile.language` (per user)

### Per User

Language is set per user, with the organisation language as default.

### Onboarding

The onboarding wizard asks for the user's language. Standard configurations are created in that language:

- German user → "Zelt", "Küche", "Werkzeug"
- English user → "Tent", "Kitchen", "Tool"

Afterwards they are normal data – not auto-translated when the language changes.

### What is NOT translated

- Article names, tags, locations, occasions → user data
- Codes (a0..., s0...) → technical

### Timezone (three levels)

Timezone resolution, from lowest to highest priority:

| Level | Where set | Purpose |
|---|---|---|
| **Server** | Docker env var (`TZ`) | Global fallback |
| **Organisation** | `Organisation.timezone` | Overrides server |
| **User** | `UserProfile.timezone` (settings) | Manually overrides organisation |

Effective timezone = user.timezone OR organisation.timezone OR server.timezone

```python
class Organisation(models.Model):
    timezone = models.CharField(max_length=64, default='Europe/Berlin')

class UserProfile(models.Model):
    timezone = models.CharField(max_length=64, blank=True)  # empty = use organisation
```

- `USE_TZ = True` (already active) – all timestamps stored in UTC
- Display converted to the effective timezone
- Digest times ("08:00") use the effective timezone

### Date / Number Formats

- Django formats dates/numbers automatically per locale

### RTL (future)

- Not needed for German/English
- If Arabic/Hebrew later: RTL support via CSS (`dir="rtl"`)

---

## 15. Images & Floor Plans ⚡

### Article & Storage Images

Multiple images per object, one primary:

```python
class ArticleImage(models.Model):
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='articles/%Y/%m/')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

class StorageImage(models.Model):
    storage = models.ForeignKey(Storage, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='storages/%Y/%m/')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
```

Note: The single `bild` field from §4a–c is superseded by the `ArticleImage` relation.

Features:

- Multiple images per object, one primary
- Upload directly from phone (camera)
- Automatic resize + thumbnail
- Usage:
  - List: thumbnail
  - Detail: gallery
  - Movement: visual confirmation when scanning
  - Search: image in result

### Floor Plans

#### Two Stages

1. **Stage 1 – Upload:** Upload an existing plan (photo/scan/PDF), assign to a storage
2. **Stage 2 – Draw:** Draw the plan in the system – rooms as areas, shelves as positions

#### Assignment via Hierarchy

Storages are hierarchical (`House > Floor > Room > Shelf > Compartment`). A plan is assigned to a storage level. E.g. the "Floor" gets a floor plan, or a "Shelf" gets a shelf plan.

#### Data Model

```python
class FloorPlan(models.Model):
    name = models.CharField(max_length=100)
    storage = models.OneToOneField(Storage, related_name='floor_plan', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='floorplans/', null=True, blank=True)  # Stage 1
    drawing = models.JSONField(default=dict)  # Stage 2 (shapes)

class FloorPlanArea(models.Model):
    floor_plan = models.ForeignKey(FloorPlan, related_name='areas', on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, null=True, blank=True, on_delete=models.SET_NULL)
    shape = models.JSONField()                             # rectangle/polygon
    label = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=7, default='#0d6efd')
```

#### Features

- **Click areas** → navigate to the area / view contents
- **Shelf plan**: multiple positions (compartments) as clickable areas
- **"Where is X?"** → highlights the area
- **Scan QR** → highlights the area
- Drawing via **SVG** (rectangles/polygons), stored as JSON

### Outdoor Map

- **OpenStreetMap** for map display
- **Plus Codes (Open Location Code)** instead of What3Words – open (Apache 2.0), offline-capable, free
- `Location` keeps lat/long + Plus Code

### Movement Visualization

- When scanning an article, its image appears for visual confirmation
- Configurable on/off in settings

---

## 16. Power Functions (not prioritized) ⚡

> Optional features, not prioritized. The data model is prepared so they don't block the path.
>
> **All AI features run locally on the server (self-hosted). No cloud APIs** – data stays in-house.

### 16.1 Dimensions & Packing

#### Tiered Data (only what you want)

| Tier | Data | Effort | Accuracy |
|---|---|---|---|
| 0 – Nothing (default) | – | none | – |
| 1 – Size class | S / M / L / XL | minimal | coarse |
| 2 – Volume | liters | low | medium |
| 3 – 3D dimensions | L×W×H (mm) | medium | exact |

The system works fully without any dimensions entered.

#### Where Dimensions Live

- **Outer dimensions** → on the object (Article / Storage) – the physical size of the object itself
- **Inner dimensions** → on the Space – the container capacity (what fits inside)

Rationale: `Space` is the container abstraction attached to everything that can contain things. So inner dimensions belong there – uniformly for boxes (Article) and shelves (Storage).

```python
class Space(models.Model):
    active = models.BooleanField(default=True)
    prefix = models.CharField(max_length=2)
    # Inner dimensions (what fits inside):
    inner_length_mm = models.IntegerField(null=True, blank=True)
    inner_width_mm = models.IntegerField(null=True, blank=True)
    inner_height_mm = models.IntegerField(null=True, blank=True)

class Article(models.Model):
    # Outer dimensions (the article itself):
    outer_length_mm = models.IntegerField(null=True, blank=True)
    outer_width_mm = models.IntegerField(null=True, blank=True)
    outer_height_mm = models.IntegerField(null=True, blank=True)
    size_class = models.CharField(max_length=2, choices=[
        ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')
    ], null=True, blank=True)

class Storage(models.Model):
    outer_length_mm = models.IntegerField(null=True, blank=True)
    outer_width_mm = models.IntegerField(null=True, blank=True)
    outer_height_mm = models.IntegerField(null=True, blank=True)
```

Note: These explicit columns replace the earlier `masse_mm` JSON idea.

#### Low Maintenance

1. **Inheritance from ArticleBase** – dimensions entered once per article type, all instances inherit
2. **Enter on demand** – never forced; asked only when needed (e.g. when packing a box)
3. **Size class fallback** – if no exact dimensions, use S/M/L/XL
4. **Bounding box** – for irregular shapes, the enclosing cuboid suffices

#### Fit Check

```python
def fits(item, space):
    a = sorted(item)   # item L,B,H
    s = sorted(space)  # space L,B,H
    return all(a[i] <= s[i] for i in range(3))
```

Rotation is allowed (sorted dimensions), so an item can be turned to fit.

#### Auto Pack (Box Packing)

- Input: set of articles (with dimensions) + available boxes (with dimensions)
- Output: suggestion which articles go in which box → minimal box count
- Algorithm: **First-Fit-Decreasing with rotation** (heuristic; exact 3D bin packing is NP-hard)

### 16.2 Image Recognition (AI)

#### Use Case

Some articles can't easily carry a QR code (tents in bags, loose or irregular objects). Instead of scanning a code, point the phone camera at the object → the system recognizes which article it is.

#### Two-Stage Recognition

**Stage 1 – Type Recognition (object category):**
A general AI model recognizes *what* it is: "tent", "hammer", "crate", "bottle". Maps to the ArticleType the system already has.

**Stage 2 – Instance Recognition:**
Within the recognized type, match against the reference images: *which specific instance* is it.

```
Camera image
   │
   ├─► Type recognition  → "Tent" (0.85)
   │        │
   │        └─► ArticleType "Tent" → narrow candidates
   │
   └─► Instance recognition (within candidates)
            └─► "Jurte 8P #3" (0.90)

Result:  Jurte 8P #3  – type and instance agree → high confidence
```

The type recognition **shrinks the search space** for instance recognition → more accurate and faster.

#### One Model Does Both

A **CLIP-like model** handles both:

- **Type (zero-shot):** image embedding vs. text embedding of ArticleType names → "looks like a tent" – **no training needed**
- **Instance:** image embedding vs. reference image embeddings → specific instance

One model, two uses.

#### Advantages of Combining

1. **More accurate**: smaller search space → better instance hits
2. **Cold start solved**: type recognition works **without reference images** (zero-shot) → "this is a tent" → show all tents → user picks
3. **Cross-check**: if type and instance disagree → mark uncertain and ask
4. **Fallback**: if no instance found, the type still helps

#### Result Display

```
Recognized:  Tent                       (type 0.85)
  Candidate 1:  Jurte 8P #3   (0.90)  ← best match
  Candidate 2:  Jurte 8P #7   (0.72)
  Candidate 3:  Dome tent 4P  (0.65)

  [Accept candidate 1]  [choose another]  [cancel]
```

If type and instance agree → candidate 1 preselected. If they disagree → show broader selection.

#### Technical Approaches

| Approach | Offline? | Cost | Accuracy |
|---|---|---|---|
| Feature matching (SIFT/ORB) | yes | free | medium (distinct objects) |
| Local embedding model (MobileNet/CLIP via ONNX) | yes | free | good |
| Cloud vision API (Google/AWS) | no | per request | best |

Recommendation: local embedding model – offline, free, data stays in-house.

#### Challenges

- **Similar items** (10 identical tents) – instances hard to distinguish
- **Cold start** – mitigated by zero-shot type recognition
- **Lighting/angle** – variations complicate recognition
- **Never auto-commit** – always confirm

#### Integration

- Fits into Movement (§11) as an **alternative to QR scanning**
- Optional: only for articles **without** QR code
- On/off switchable

### 16.3 Natural Language → Query Builder

Type a sentence, it becomes a query:

> "show me all damaged tents in room 2" → Query Builder JSON (§9)

- Local LLM (e.g. Ollama + Llama / Mistral / Qwen)
- Output is the same JSON the Query Builder produces
- User can review and adjust before applying
- Lowers the barrier for power users

### 16.4 Auto-Categorization on Article Creation

When creating an article, the system suggests ArticleType and tags:

- From the name (text → LLM / embeddings)
- From an uploaded image (CLIP)

> "Jurte 8P" → Type "Tent", Tags "Outdoor", "Group"

- Reduces data entry
- Suggestions, not automatic (user confirms)

### 16.5 Smart Packlist Suggestions

For an occasion, suggest items based on past occasions of the same type:

> "Last summer camp had these 30 items – include them again?"

- Based on occasion history (§2)
- Very valuable for recurring camps
- User picks/edits

### 16.6 Duplicate Detection

When creating an article, find similar existing ones:

> "There's already a 'Jurte 8P' – did you mean that one?"

- Similarity via name embeddings (local)
- Prevents data clutter

### 16.7 Voice Input for Movement

Hands-free commands:

> "store 5 camp beds in shelf 3"

- Local speech-to-text (Whisper)
- Maps to Movement actions (§11)
- Combines with image recognition

### 16.8 Anomaly Detection

Detect unusual patterns:

> "Article X was moved 5 times today – unusual"
> "10 tents disappeared at once"

- Statistical (no model needed) or local ML
- Security-relevant

### 16.9 Photo Damage Assessment

Photo of a damaged item → AI describes the damage / suggests severity:

- Uses the same local vision model (§16.2)
- Fits condition tracking (§4e)
- Suggests: "minor / major / total"

### 16.10 Receipt OCR

Photograph a receipt → extract purchased items → create articles:

- Local OCR (Tesseract) + LLM for structuring
- Fits the Purchase power function

### 16.11 Photo Counting (lowest priority)

Shelf photo → AI counts the items:

- Technically demanding
- Interesting for inventory (§5b–c)
- **Deliberately placed last** – uncertain value, high effort

### 16.12 AI Size Recognition from Photo

Estimate an object's dimensions from a photo using a known reference.

#### Approaches

| Approach | Accuracy | Effort | Device-dependent? |
|---|---|---|---|
| **Reference object in frame** | ±5–10 % | low | no |
| **AR measurement** (ARKit/ARCore) | ±1–3 % | medium | yes (not all phones) |
| **Two photos / photogrammetry** | ±2–5 % | high | no |

#### Recommended: Reference Card (reuses QR infrastructure)

The system already has QR codes (§5a). Print a reference card with a known size:

```
┌─────────────────────────┐
│  ██ ▄▄ ██  QR code      │  ← known: 30 mm
│  ██ ▄▄ ██               │
│  ─────────────────────  │  ← measurement lines / grid
│  0   1   2   3   4 cm   │
└─────────────────────────┘
```

Workflow:

1. Place the reference card next to the article
2. Take a photo (perpendicular, from above)
3. AI detects the QR code (known size) and the article
4. Computes the article dimensions relative to the reference
5. User confirms / corrects
6. Dimensions are saved (§16.1)

Advantage: reuses the existing QR infrastructure, no new device needed.

#### Combination with §16.2

The same photo can do both:

```
Photo
 ├─► Article recognition (§16.2)  → "Jurte 8P #3"
 └─► Size recognition             → 4000 × 3000 × 2200 mm
```

One photo → article identified AND measured.

#### Limits (honest)

- **Perspective**: must be shot perpendicular, otherwise distorted
- **Plane**: reference and article must be in the same plane
- **Accuracy**: ±5–10 % – enough for packing, not for precision work
- **Irregular shapes**: only the bounding box
- **AR would be more accurate**, but only on devices with ARKit/ARCore

#### Classification

A power function (§16) – makes entering dimensions (§16.1) convenient, but not required for the system to run.

### 16.13 Offline Queue (Movement)

Buffer scans when offline, sync when online.

#### Concept

- Offline: only the **scanned codes + action** are stored locally
- Online: resolve (look up articles, apply movements)
- Feedback: "3 actions pending sync"
- Conflicts: **report after sync** ("X was moved elsewhere in the meantime")

#### Why "Blind Queue"

- Simpler than full offline (no local data cache)
- No conflict resolution during capture
- Conflicts reported after sync

#### Technical

- IndexedDB for the queue
- Service Worker for offline detection
- Sync on reconnect

#### Conflict Handling

```
User A (offline):  Article X → Shelf 3
User B (online):   Article X → Shelf 5

A comes online → sync:
   → X was moved elsewhere → report: "X is now in Shelf 5, your action was skipped"
```

#### Difficulty

- Basic queue: moderate
- Conflict handling: hard
- Not prioritized

---

## 17. Admin Dashboard & Backup ⚡

### Admin Dashboard

Two access levels:

- **Superuser** – full system access (all organisations)
- **Organisation Admin** – restricted to their own organisation

| Area | Superuser | Org Admin |
|---|---|---|
| System health (DB size, version, uptime, last backup) | ✅ | – |
| Statistics (articles, storages, users, movements, storage usage) | ✅ all orgs | ✅ own org |
| Backup management | ✅ | ✅ own org (export/import) |
| Restore | ✅ full + per-org | ✅ own org only |
| Organisation management | ✅ | – |
| System settings | ✅ | – |
| Logs / Audit | ✅ all | ✅ own org |

### Backup Strategy (three levels)

#### Level 1 – Full Backup (file)

- Copy the SQLite file (consistent via `VACUUM INTO`)
- Scheduled (configurable) or manual
- For disaster recovery
- Restores everything

#### Level 2 – Per-Organisation Export/Import (logical)

- Export one organisation as JSON (all objects + relations)
- Re-importable → only that organisation affected
- Solves the multi-org restore problem
- Import assigns new IDs and remaps foreign keys

```json
{
  "organisation": { "name": "...", "timezone": "..." },
  "users": [...],
  "article_types": [...],
  "articles": [...],
  "storages": [...],
  "tags": [...],
  "occasions": [...],
  "movements": [...]
}
```

#### Level 3 – Soft-Delete Recovery

- Already exists (`softdelete` app)
- For accidental deletions

### Configurable Settings

| Setting | Options |
|---|---|
| **Schedule** | Manual / Daily / Weekly / Custom |
| **Storage** | Local / Download / External path |
| **Retention** | Keep last N backups (e.g. 7) |
| **Auto-backup before restore** | Always on (safety) |

### Safety Rule

> Before every restore, a backup is created automatically. Otherwise a wrong restore could destroy data irrecoverably.

### Restore

- **Full restore** → affects all organisations (disaster only)
- **Per-organisation restore** → only that organisation (safe)
- Always backup before restore

---

## 18. Data Migration & Transformation ⚡

### Concept

**Schema migration** changes the structure (new column, new table) – Django handles it automatically.

**Data transformation** reshapes the *existing values* so they fit the new structure – must be programmed explicitly.

### Why It Matters

Without planned transformations, one of two things happens:

1. **Migration fails** (a required field has no value)
2. **Migration runs but data is broken** (e.g. all articles invisible because `organisation = NULL`)

Some transformations are **not reversible** – they must be thought through beforehand.

### Concrete Transformations

| Existing | New | Transformation |
|---|---|---|
| `Article.amount` (text) | `menge` + `mengeneinheit` | Parse text ("5 Stück" → 5 + "Stück") |
| – | `Article.owner` | All → User 1 |
| – | `Article.organisation` | Create organisation, assign all |
| – | `Article.zustand` | Default "gut" |
| – | `Article.tags` | Empty (M2M) |
| – | `ArticleType.field_config` | Set sensible default |
| – | `ArticleType.custom_fields_schema` | Empty default |
| – | `Storage.owner` / `Tag.owner` | All → User 1 |
| `Location.modernWhat3Words` | Plus Codes | Keep field or migrate |
| – | `Space.inner_*_mm` | NULL (optional) |
| – | `Article.outer_*_mm` | NULL (optional) |

### Rules

1. **Every transformation is a data migration** with `RunPython` (forward + backward)
2. **Backward migration** must be defined (even if lossy → document the loss)
3. **Test on a copy** of the production DB before applying
4. **Backup before** every data migration (§7c)
5. **Idempotent** where possible (running twice does not break)
6. **Log** what was transformed (how many records)

### Order (expand–contract pattern)

1. Schema migration (add fields/tables, nullable)
2. Data migration (fill values)
3. Schema migration (make required, if needed)

### Example: amount → menge + mengeneinheit

```python
def parse_amount(apps, schema_editor):
    Article = apps.get_model('article', 'Article')
    for article in Article.objects.all():
        raw = (article.amount or '').strip()
        parts = raw.split(' ', 1)
        if parts and parts[0].replace('.', '').replace(',', '').isdigit():
            article.menge = float(parts[0].replace(',', '.'))
            article.mengeneinheit = parts[1] if len(parts) > 1 else ''
            article.save()

def reverse_parse_amount(apps, schema_editor):
    Article = apps.get_model('article', 'Article')
    for article in Article.objects.all():
        if article.menge is not None:
            article.amount = f"{article.menge} {article.mengeneinheit}".strip()
            article.save()
```

### Non-Reversible Transformations

Some transformations lose information:

- `"5 Stück"` → `5` + `"Stück"` is reversible
- `"ca. 5"` → `5` loses "ca."
- W3W → Plus Code is lossy (different systems)

For these: document the loss, keep the old field if possible.

---

## 19. Import (CSV / Excel) ⚡

### Concept

New organisations often have their inventory in Excel/CSV. Without import, they would have to type hundreds of articles by hand. So a guided import is essential.

### Flow

1. **Upload** – CSV or Excel file
2. **Column mapping** – assign file columns to system fields
3. **Preview** – show first rows with mapped values
4. **Validation** – check for errors (duplicate codes, unknown types)
5. **Import** – create records
6. **Report** – how many imported, how many failed, why

### Column Mapping

```
File column      →  System field
─────────────────────────────────
"Name"           →  Article name
"Typ"            →  ArticleType (match by name)
"Menge"          →  menge
"Lagerort"       →  Storage (match by name/code)
"Zustand"        →  zustand
```

- Auto-suggest mapping based on column names
- User can adjust

### Validation

| Case | Behavior |
|---|---|
| Duplicate code | Skip or update? (selectable) |
| Unknown ArticleType | Create? or error? (selectable) |
| Unknown Storage | Create? or error? (selectable) |
| Invalid values | Report |

### Template

- Downloadable import template (CSV/Excel) with expected columns
- Pre-filled with example rows

### What Can Be Imported

| Object | Import |
|---|---|
| Articles | ✅ |
| Storages | ✅ |
| Locations | ✅ |
| Tags | ✅ |
| ArticleTypes | ✅ |

Note: Occasions are **not** imported – they are created in the system.

### Technical

- `openpyxl` (Excel) + Python `csv` (CSV)
- Preview via HTMX

---

## 20. Loans & Shared Pools ⚡

### Concept

An article can be **borrowed** (not owned by the organisation). It behaves normally (in packlists, movable) but is marked as not the organisation's property.

### Data Model

```python
class Article(models.Model):
    organisation = models.ForeignKey(Organisation, ...)
    ownership = models.CharField(choices=[
        ('owned', 'Owned by organisation'),
        ('borrowed', 'Borrowed from external'),
    ], default='owned')
    loan_requires_confirmation = models.BooleanField(default=True)  # per-article default
    # ...

class Loan(models.Model):
    article = models.ForeignKey(Article, ...)
    lender_type = models.CharField(choices=[
        ('person', 'External person'),
        ('organisation', 'Another organisation'),
    ])
    lender_name = models.CharField(max_length=200, blank=True)            # for private person
    lender_organisation = models.ForeignKey(Organisation, null=True, ...)  # for org-to-org
    borrower_organisation = models.ForeignKey(Organisation, related_name='loans_in', ...)
    occasion = models.ForeignKey(Occasion, null=True, blank=True, ...)     # tied to occasion or independent
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    status = models.CharField(choices=[('active', 'Active'), ('returned', 'Returned')])
    notes = models.TextField(blank=True)

class LoanOffer(models.Model):
    """A list of articles offered for loan."""
    lender_organisation = models.ForeignKey(Organisation, related_name='loan_offers', ...)
    name = models.CharField(max_length=200)
    requires_confirmation = models.BooleanField(default=True)  # default: confirm
    # ...

class LoanOfferItem(models.Model):
    offer = models.ForeignKey(LoanOffer, related_name='items', ...)
    article = models.ForeignKey(Article, ...)
    requires_confirmation = models.BooleanField(null=True, blank=True)  # None = use offer default

class OrganisationMembership(models.Model):
    pool = models.ForeignKey(Organisation, related_name='members', ...)
    member = models.ForeignKey(Organisation, related_name='pools', ...)
    can_borrow = models.BooleanField(default=True)
    can_add = models.BooleanField(default=False)
```

### Confirmation Resolution

From specific to general:

```
1. LoanOfferItem.requires_confirmation  (if set)
2. LoanOffer.requires_confirmation      (list default)
3. Article.loan_requires_confirmation   (article default)
```

### Flow

```
Lender creates offer (list or single article)
   │
   ├─► requires_confirmation = True
   │     Borrower selects → status "pending"
   │     Lender confirms → status "active"
   │
   └─► requires_confirmation = False
         Borrower selects → status "active" (immediate)
```

### Friend Scenario (via Share Link)

```
Friend opens the loan link
   │
   ├─► Form: "What do you want to lend?"
   │     Name, description, period, photo
   │
   ├─► Article created (ownership = 'borrowed')
   │
   └─► Friend sees status (active / returned)
         and can confirm return

Optional: "Create an account to manage your loans"
```

- No account needed – the link is the access (like §10)
- Optional: create account and link the loan
- Link can expire, be single-use, have a password (all from §10)

### Account Rules

| Linkage | Allowed | Reason |
|---|---|---|
| **With account** | Permanent loan OR occasion | Reminder email possible |
| **Without account** | **Only one occasion** | No email possible → no reminder |

The person can withdraw (cancel) the loan.

### After Return

- Article is **archived** (soft-delete)
- Loan record stays (history)
- Linked account still sees it ("My loans → returned")
- Occasion history remains visible

### Shared Pool

A pool is simply **an organisation that lends**:

```
Regional association (Organisation)
   │  owns the pool inventory
   ├─► Local group North (member)  ── borrows from pool
   ├─► Local group South (member)  ── borrows from pool
   └─► Local group East (member)   ── borrows from pool
```

No new concept needed – uses:

- **Organisation** (the pool owner)
- **Loan** (members borrow from the pool)
- **Roles/Permissions** (§3) – who may borrow, who may add

### Resolved Decisions

1. **Direction of confirmation**: The **lending** organisation confirms (it controls what leaves its inventory). For pools, confirmation can be disabled.
2. **Shared pool**: Included – a pool is an organisation that lends.
3. **After return**: Archive (soft-delete) – confirmed.

---

## 21. Storage Integrity (Cycle Prevention & Depth Limit) ⚡

### Problem

- `Article.stored` → `Space` → `Article` (via `Space.itemArticle`) – **nothing prevents cycles**
- `SelfForeignKey` (used for `Storage.parent`, `Tag.parent`) **silently sets the value to `None`** on a cycle – no error message
- `Settings.storageDepth` exists but is **unused**

### Risk

```
Article A ──stored──► Space S ──itemArticle──► Article B ──stored──► Space T ──itemArticle──► Article A  ← CYCLE
```

A query "what is inside A?" would loop forever.

### Solution

#### 1. Central Service

```python
def can_store(article, target_space) -> tuple[bool, str]:
    """Check whether article may be stored in target_space."""
    # 1. Not into its own space
    if target_space == article.space:
        return False, "Article cannot be stored in itself"
    # 2. No cycle: walk up the chain
    space = target_space
    depth = 0
    while space is not None:
        depth += 1
        if depth > settings.storageDepth:
            return False, f"Maximum storage depth ({settings.storageDepth}) exceeded"
        owner = space.itemArticle or space.itemStorage
        if owner == article:
            return False, "Cycle detected"
        space = owner.stored if isinstance(owner, Article) else None
    return True, ""
```

#### 2. Fix SelfForeignKey

- Instead of silently returning `None` → raise `ValidationError`
- Also use `storageDepth`

#### 3. Activate storageDepth

- Default: **7** (was 5)
- Configurable in settings
- **Asked during onboarding** (§8)

#### 4. Validate in Both Places

- **On save** (model/service) – hard limit
- **In the UI** (Movement) – friendly message beforehand

### Settings

- `storageDepth` default **7**
- Configurable in settings
- Asked during onboarding

---

## 22. Multi-Organisation Membership ⚡

### Concept

A user can belong to **multiple organisations**, with a **different role in each**. The active organisation is selected at login and switchable in the sidebar.

### Data Model

```python
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('user', 'organisation')
```

### Active Organisation

- Selected at login
- Switchable in the sidebar
- Session-based
- All queries filter by the active organisation
- Roles apply per organisation

### Login Flow

```
Login
  │
  ├─► User belongs to 1 org  → use it directly
  │
  └─► User belongs to N orgs → choose:
        ┌─────────────────────────────┐
        │  Which organisation?         │
        │  ( ) Pfadfinder St. Georg    │
        │  ( ) Regionalverband Süd     │
        │  ( ) Privat                  │
        └─────────────────────────────┘
```

### Sidebar Switcher

```
┌─────────────────────────────┐
│  Active organisation:        │
│  [ Pfadfinder St. Georg ▼ ]  │
└─────────────────────────────┘
```

### Role per Organisation

- In Org A: Admin
- In Org B: Helper
- The role determines permissions within that organisation

### Implications

- All queries filter by the active organisation
- The `organisation` FK on all objects (§1)
- Permissions (§3) are evaluated against the role in the active organisation

---

## 23. Registration, Invitations & Onboarding ⚡

### Three Onboarding Levels

| Level | Who | When | Content |
|---|---|---|---|
| **Server onboarding** | Server admin | Once on first start | Registration policy, SMTP, default language, timezone, storage depth |
| **Organisation onboarding** (§8) | Org admin | When creating the organisation | Article types, roles, storage types |
| **User onboarding** | Every user | On first login | Learn the "tricks" |

Separate because each audience only sees what it needs.

### Server Registration Policy

The server admin decides how new organisations are created:

```
How can new organisations register?

  ( ) Open          – anyone can self-register
  ( ) Invite only   – only via invitation from an organisation
  ( ) Request       – request with reason, server admin approves
```

### Organisation Request (for "Request")

```python
class OrganisationRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    reason = models.TextField()                    # mandatory
    status = models.CharField(choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    reviewed_at = models.DateTimeField(null=True)
```

The reason is a **mandatory** field.

### Invitation via Link

```python
class Invitation(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)          # optional – for email sending
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    token = models.CharField(max_length=64, unique=True)
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()            # default: +7 days
    accepted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ], default='pending')
```

- **Link-based** – the link can be copied/shared
- **Optionally sent by email** (if SMTP is configured)
- **Expiry**: default 7 days, **configurable by the inviter**
- **Role** is set at invitation time

### Double-Opt-In Rules

| Situation | Behavior |
|---|---|
| **"Open" selected** | Email confirmation **on by default** |
| **Confirmation deselected** | ⚠️ **Warning**: "Without confirmation, spam accounts can register" |
| **No SMTP configured** | ⚠️ **Explanation**: "Without an email server, no confirmation is possible. Registration happens directly." |

### User Onboarding (the "tricks")

A guided tour through the key features:

```
Welcome to little_WMS! 👋
   │
   ├─► 1. The sidebar – everything is here
   ├─► 2. Scanning – capture articles via camera
   ├─► 3. Movement – store/remove in seconds
   ├─► 4. "Where is...?" – find articles
   ├─► 5. Occasions – plan material for camps
   └─► 6. Done! [End tour]
```

- **Skippable**
- **Repeatable later** (from settings)
- **Role-specific** (admin sees more than helper)

### Flow

```
Server admin sets up (onboarding)
   │  → Policy: Open / Invite / Request
   │  → SMTP (optional)
   │
   ├─► "Open":     New org registers directly
   ├─► "Invite":   Admin invites → link → user joins
   └─► "Request":  New org sends request + reason
                      → server admin approves → org created
```

---

## 24. Dashboard ⚡

### Concept

The dashboard is the **command center** – it shows what matters right now, role-specific. Not just tiles (as today), but the important information at a glance.

### Widgets

| Widget | Content | Required Permission |
|---|---|---|
| **Upcoming occasions** | Next occasions + packlist status | `occasion.view` |
| **Notifications** | Unread (§6) | `notification.view` |
| **Alerts** | Expiring, low stock, maintenance due | `article.view` |
| **Quick actions** | Scan, add article, movement | `article.create` / `article.move` |
| **Statistics** | Articles, storages, movements, usage | `settings.view` |
| **Recent activity** | Recent movements/changes | `article.view` |
| **Custom widgets** | Based on Saved Views (§10) | depends on the view |

### Permission-Linked

Each widget requires a permission (§3). The dashboard only shows widgets the user is allowed to see.

```python
WIDGET_PERMISSIONS = {
    'upcoming_occasions': 'occasion.view',
    'notifications': 'notification.view',
    'alerts': 'article.view',
    'quick_actions': 'article.create',
    'statistics': 'settings.view',
    'recent_activity': 'article.view',
}
```

### Role-Specific

```
Admin:        Statistics + Alerts + Users + all widgets
Warehouse:    Movement + Alerts + upcoming Occasions + activity
Helper:       "Where is...?" + upcoming Occasions + notifications
```

### Custom Widgets (from §10)

Users can place **Saved Views as widgets** on the dashboard:

```
┌─ My damaged tents (Saved View) ─────────────┐
│ 🏕️ Jurte 8P #3   damaged                    │
│ 🏕️ Jurte 8P #7   damaged                    │
│                          [Show all →]       │
└─────────────────────────────────────────────┘
```

### Customizable

- Show/hide widgets
- Order via drag & drop
- Saved per user

---

## 25. Article Model (Three Levels, Custom-Field Levels, Merge/Split) ⚡

### Three Levels

```
ArticleType  →  kind of article       "Tents"
ArticleBase  →  basis / model         "Jurte 8P" (same dimensions, color, material)
Article      →  individual instances  "Jurte 8P #1", "#2", "#3"
```

| Level | Analogy | Properties |
|---|---|---|
| ArticleType | Category | Field schema |
| ArticleBase | Product / SKU | Catalog properties (dimensions, color, material) |
| Article | Stock lot | Stock (quantity, location, condition, code) |

### Where Data Lives

| Data | Level |
|---|---|
| Custom field schema | ArticleType |
| Custom field values | ArticleBase (`attributes`) or Article (per `level`) |
| Global fields (condition, quantity, location, purchase date) | Article |
| Dimensions | ArticleBase (§16.1) |
| Tags, images, sets | Article |

### Custom-Field Levels

Each custom field in the schema has a `level`:

```python
# ArticleType.custom_fields_schema
{
  "fields": [
    {"name": "farbe", "type": "text", "level": "base"},           # default
    {"name": "personenzahl", "type": "integer", "level": "base"},
    {"name": "seriennummer", "type": "text", "level": "article"}  # per instance
  ]
}
```

- **Default: `base`** → simple, propagates
- **`article`** → only when needed (serial number)

UI separation:

- Base fields → in the Base form (once per model)
- Article fields → in the Article form (per instance)

### Merge / Split

An ArticleType option:

```python
class ArticleType(models.Model):
    # ...
    allow_merge_split = models.BooleanField(default=False)
```

| ArticleType | Merge/Split | Article-level fields |
|---|---|---|
| Tent | ❌ off | ✅ possible (serial number) |
| Fuse beads | ✅ on | ❌ none (else conflict) |

**Rule:** If merge/split is on and there are article-level fields → **warning** (conflicts possible).

### Merge / Split Behavior

**Merge two Articles (same Base):**

- Quantity: summed
- Base values: identical (same Base) → nothing to do
- Article values (condition, location): conflict → user chooses

**Split an Article:**

- Quantity: divided
- New code for the new Article
- Base values: same
- Article values: copied to both (or asked)

### Propagation

Changing the Base (e.g. fixing an error) propagates automatically to all instances.

---

## 26. Code System & Links ⚡

### Code System (existing)

```python
class UuidCode(models.Model):
    uuidCode = models.UUIDField(unique=True, default=uuid.uuid4)
    code = models.CharField(max_length=34)   # prefix + UUID without dashes
    prefix = models.CharField(max_length=2)
    used = models.BooleanField(default=True)
```

### Prefixes

| Prefix | Object |
|---|---|
| `a0` | Article |
| `s0` | Storage |
| `l0` | Location (new) |
| `ab` | ArticleBase |
| `at` | ArticleType |
| `st` | StorageType |
| `t0` | Tag |

### How It Works

```
1. Code is generated (prefix + UUID)
   → code = "a0" + "3f2b8c..." (34 chars)

2. Code can be created BEFORE the object (used=False)
   → for printing QR codes

3. Object is created → code assigned (used=True)

4. When creating with a given code:
   → check: is the code already used? (used=True → error)
```

### Rules

- **Format**: `prefix + UUID` (34 chars) – stays
- **No reuse**: codes stay consumed, even after deletion
- **Custom codes**: possible as a custom field, not as the standard code
- **Barcode type**: QR only
- **Codes for**: Article, Storage, Location (physical objects)

### Links

Every object has a canonical URL:

```
Article:    https://wms.example/a/a0-3f2b8c...
Storage:    https://wms.example/s/s0-9d4e1a...
Location:   https://wms.example/l/l0-...
Occasion:   https://wms.example/o/42
SavedView:  https://wms.example/v/17
```

**URL structure: by code** (stable – the code never changes).

### Short Links (optional)

```python
class ShortLink(models.Model):
    token = models.CharField(max_length=10, unique=True)   # e.g. "x7k2p9"
    content_type = models.ForeignKey(ContentType, ...)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
```

- Only created when needed → no ballast on every object
- Generic → works for any object
- Stable → once created, stays valid

Flow:

```
User: "Share short link"
   │
   ├─► ShortLink exists? → use it
   └─► Otherwise: generate new token → /a/x7k2p9
```

### QR Content

| QR type | Content | For |
|---|---|---|
| **Object label** (physical) | **Code** | Sticker on article/shelf – app scanner, offline |
| **Shared/printed** | **Link** | Packlists, share links, emails – any camera |

The print dialog (§5a) lets you choose:

```
QR content:  (•) Code (app scanner)   ( ) Link (universal)
```

### App Scanner

The app scanner understands **both** codes and links.

---

## 27. Soft-Delete & Trash ⚡

### Existing Mechanism

```python
class SoftDeleteObject(models.Model):        # abstract base
    deleted_at = models.DateTimeField(null=True)
    objects = SoftDeleteManager()            # filters deleted_at__isnull=True

class ChangeSet(models.Model):               # groups changes
    created_date = models.DateTimeField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

class SoftDeleteRecord(models.Model):        # tracks deleted objects
    changeset = models.ForeignKey(ChangeSet)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
```

### How It Works

```
1. Delete → deleted_at is set (no real DELETE)
2. All queries automatically filter deleted_at__isnull=True
3. Undelete → restores ALL objects in the same ChangeSet
```

### Rules

| Point | Decision |
|---|---|
| **What** | All objects (articles, storages, tags, occasions, ...) |
| **Retention** | Forever |
| **Who restores** | Configurable per organisation |
| **Trash view** | Yes |
| **Permanent delete** | Yes, configurable per organisation (who) |

### Permissions

The restore/permanent-delete rights fit into the roles system (§3):

```
trash.view           – see the trash
trash.restore        – restore objects
trash.delete_forever – permanently delete
```

### Trash View

- Lists all soft-deleted objects
- Filter by type, date, who deleted
- Restore (single or as a ChangeSet)
- Permanently delete (with confirmation)

---

## 28. Locations ⚡

### Concept

A Location is a physical place (address + coordinates). Used for:

- **Occasion location** – where does the camp take place?
- **Storage location** – where is the building?
- **Outdoor map** (§15)

### Address: django-address

Uses the `django-address` library (Google i18n address data):

```python
from address.models import AddressField

class Location(models.Model):
    address = AddressField(on_delete=models.CASCADE)
    # ...
```

- International address formats (adapts to the country)
- Replaces the rigid "traditional" fields (Land, City, Zipcode, Street, ...)

### Coordinates (separate)

```python
class Location(models.Model):
    address = AddressField(on_delete=models.CASCADE)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    plus_code = models.CharField(max_length=20, blank=True)  # Open Location Code
    code = models.OneToOneField(UuidCode, ...)               # prefix l0
```

- Coordinates stay separate (for the map §15)
- **Plus Code** instead of What3Words (§15)

### Links

```python
class Storage(models.Model):
    location = models.ForeignKey(Location, null=True, ...)  # where is the building?

class Occasion(models.Model):
    location = models.ForeignKey(Location, null=True, ...)  # existing
```

### Map

- OpenStreetMap shows all locations with coordinates
- Click marker → location details

### Migration

The existing "traditional" fields (`traditionalLand`, `traditionalCity`, ...) and the What3Words fields are replaced:

- Address → `django-address`
- What3Words → Plus Code

Data migration (§18): convert existing address fields to `django-address`, drop What3Words.

---

## 29. Security ⚡

### Already Covered (Django defaults)

| Topic | Status |
|---|---|
| CSRF | ✅ Active (integrated with HTMX) |
| XSS | ✅ Django templates auto-escape |
| SQL injection | ✅ Django ORM parameterized |
| Password hashing | ✅ Django default |
| Session auth | ✅ Django default |

### File Uploads (Images §15)

| Measure | Best Practice |
|---|---|
| Formats | JPEG, PNG, WebP (+ HEIC from iPhone → convert to JPEG) |
| No SVG | SVG can contain scripts (XSS) → avoid |
| Size limit | e.g. 10 MB per image |
| Validation | MIME type **and** magic bytes (not just extension) |
| Re-encode | Re-save with Pillow → strips EXIF (privacy!) and hidden code |
| Filenames | Generate randomly, never use user names |
| Thumbnails | Generate smaller versions |
| Storage | Outside web root, served via controlled view |

Core: **always re-encode images** – defuses most attacks and removes GPS data from photos.

### Login Rate Limiting

| Measure | Best Practice |
|---|---|
| Limit | e.g. 5 failed attempts per minute (per IP **and** per account) |
| Backoff | Progressive delay after failures |
| Lockout | Temporary (e.g. 15 min) after too many attempts |
| Logging | Log failed attempts |
| Library | `django-axes` or `django-ratelimit` |

Core: limit **per account** too, not just per IP.

### Password Policy

- Django standard validators (length, common passwords, numeric, similarity)

### HTTPS

| Measure | Best Practice |
|---|---|
| TLS | Certbot / Let's Encrypt |
| Redirect | HTTP → HTTPS automatically |
| Secure cookies | `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` |
| HSTS | `SECURE_HSTS_SECONDS` |
| Reverse proxy | nginx/Caddy terminates TLS, Django behind |

Deployment-dependent, but the code must be HTTPS-capable.

### Backup Encryption

| Measure | Best Practice |
|---|---|
| Encrypt | Encrypt backup files (`age` or `gpg`) |
| Access control | Restrict file permissions, separate directory |
| Off-site | Encrypted copy at another location |
| Keys | Store separately from the backup |

Core: if backups leave the house, they **must** be encrypted.

### API Authentication

- Token auth (see §7a / A10)

### Permissions

- Every view checks the role (§3)

---

## 30. E-Mail / SMTP ⚡

### Where Email Is Needed

| Use | Where |
|---|---|
| Notifications | §6 |
| Invitations | §23 |
| Password reset | Django built-in |
| Double-Opt-In | §23 |
| Loan reminders | §20 |

### Configuration: Environment Variables

> Secrets belong in environment variables, not in the database.

```bash
# .env
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@example.com
EMAIL_HOST_PASSWORD=secret
DEFAULT_FROM_EMAIL=little_WMS <noreply@example.com>
```

Why:

- No encryption overhead – the file is protected by file permissions
- Standard for infrastructure config
- Not in git (`.env` is in `.gitignore`)
- Fits Docker (env_file, already present)

### Alternatives (and why not)

| Option | Rating |
|---|---|
| `.env` | ✅ Best practice |
| DB, encrypted | ⚠️ Only if UI-configurable needed – key must also come from `.env` |
| DB, plaintext | ❌ Never |
| In code | ❌ Never (ends up in git) |

### Server-Level (not per organisation)

- SMTP config → `.env` (like `SECRET_KEY`, DB password)
- No DB field, no encryption needed
- Server onboarding (§23) shows the config (read-only) and checks it works ("Send test email")

```
Server onboarding → Email:
   Status: ✅ SMTP configured (smtp.example.com)
   [Send test email]

   (Configuration via .env – see documentation)
```

### Fallback Without SMTP

| Situation | Behavior |
|---|---|
| No SMTP configured | Emails are **skipped** + warning in log |
| In-app notifications | Still work (§6) |
| Invitations | Link can still be copied/shared (§23) |

### Email Templates

- Standard templates (§6) for notifications
- Templates for invitations, password reset
- Translatable (§14)

---

## 31. API Authentication ⚡

### Two Paths in Parallel

```
Web UI (HTMX)     →  Session auth (existing)
API clients       →  Token auth (DRF)
```

### Token Auth (DRF)

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',   # for browser
        'rest_framework.authentication.TokenAuthentication',     # for API clients
    ],
}
```

- Each user gets **one token** (`rest_framework.authtoken`)
- Client sends: `Authorization: Token abc123...`
- Token can be created/revoked in settings

### Why Token Instead of JWT?

- Simpler – no refresh handling
- Revocable – delete token = access gone
- Enough for PWA / mobile / integrations
- JWT can be added later if needed (currently not planned)

### Permissions in the API

The API uses the **same roles** (§3):

```python
class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, HasRolePermission]
    # checks: article.view / article.edit / ...
```

- Organisation filter also applies in the API (§22)
- No access to other organisations

### API Versioning

- All endpoints under `/api/v1/` (as planned in §7a)

---

## 32. Audit Log ⚡

### Concept

A **unified audit log** for all objects. Replaces the article-only `ArticleLog` (§4e).

### Data Model

```python
class AuditLog(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=30)   # created, updated, deleted, restored, moved, ...
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    changes = models.JSONField(default=dict)   # what changed (old → new)
    session = models.ForeignKey('MovementSession', null=True, blank=True, on_delete=models.SET_NULL)
    undone = models.BooleanField(default=False)
```

### Actions

| Action | Description |
|---|---|
| `created` | Object created |
| `updated` | Object changed |
| `deleted` | Object soft-deleted |
| `restored` | Object restored from trash |
| `moved` | Article moved (from/to space) |
| `removed` | Article removed from storage |
| `quantity_changed` | Quantity changed |
| `damaged` / `repaired` | Condition changed |
| `set_modified` | Set composition changed |

### Changes Detail

```json
{
  "condition": {"old": "good", "new": "damaged"},
  "notes": {"old": "", "new": "Pole broken"}
}
```

### What Is Logged

- All create / update / delete operations
- All movements
- All restores

### Retention

- Configurable per organisation
- Options: forever / X days / X months

### UI

- Article detail: timeline of actions
- Admin: general log with filters (user, type, date, action)
- Filter: "All movements by user X", "All changes this week"

### Impact on §4e and §11

- §4e (Article History) now uses `AuditLog` instead of `ArticleLog`
- §11 (Movement) uses `AuditLog` for the session list and undo

---

## 33. Reporting & Statistics ⚡

### Two Levels

```
1. Dashboard widgets (§24)   →  at a glance
2. Reports view              →  dig deeper, filter, export
```

### Reports

| Report | Question | For |
|---|---|---|
| Usage | How often was article X moved/used? | Admin |
| Movements over time | Activity trends (week/month) | Admin |
| Storage usage | How full are the storages? | Warehouse |
| Occasion history | Which occasion used what? | Admin |
| Damage / maintenance | How many damaged items? Maintenance costs? | Admin |
| Consumption | Usage over time, reorder forecast | Admin |
| User activity | Who did what? | Admin |
| Stock development | Additions / removals over time | Admin |

### Reports View

- Filter via the Query Builder (§9)
- Selectable time range
- **Diagrams** (bar, line) + tables
- Export as **CSV and PDF**

### Examples

```
Usage:        Top 10 most-used articles
Movements:    Line chart over 12 months
Usage:        Bar per storage (used / free)
Consumption:  Consumption curve + forecast
```

### Forecasts (low priority)

- Consumption forecast (reorder prediction)
- Noted, but not important

---

## 34. PWA (Progressive Web App) ⚡

### Concept

The app is **installable** on mobile devices (like a native app) and caches the app shell so it starts without network.

### Features

- **Installable** – "Add to home screen"
- **App shell cached** – starts offline
- **But:** data needs the server
- **Icons, splash screen** – app-like
- **Standalone display** – no browser chrome

### Technical

- `manifest.json` (name, icons, theme color, `display: standalone`)
- Service Worker (cache app shell, static assets)
- HTTPS required (already planned §29)

### What Works Offline

| Feature | Offline? |
|---|---|
| App shell (UI) | ✅ |
| Static assets (CSS, JS, icons) | ✅ |
| Data (articles, storages) | ❌ needs server |
| Scanning movements | ❌ (see §16.13 offline queue) |

### Not Full Offline

- Full offline (local DB + sync) is explicitly **out of scope**
- See §16.13 for the offline queue power function

---

## 35. Data Protection / GDPR ⚡

### Personal Data Processed

- User names, email addresses
- Activity logs (who did what)
- Loans (who lent what)

### User Deletion (with Anonymization)

```
Delete user
   │
   ├─► Account + profile deleted
   ├─► Logs remain, but anonymized:
   │     "Anna moved X" → "Deleted user moved X"
   └─► Loans: name removed
```

Why anonymize instead of delete? The logs are important for traceability, but the personal reference must go.

### User Data Export

```
"Export my data"
   → JSON with: profile, activities, loans
```

### Retention

- Log retention configurable per organisation (§32)
- Users can be deleted

### Privacy Policy

- Configurable link (server-level)
- Template provided (admin reviews and adapts)
- Link to generators as help

### Consent

- Checkbox at registration: "I accept the privacy policy"

### What the Operator Must Do (not the system)

- Fill in the privacy policy
- Keep a record of processing activities
- Data processing agreement (if cloud hosting)
- Breach notification process

The system cannot do this – it only provides the **technical means** (deletion, export, anonymization).

### Important Note

> Since the system is **self-hosted**, the **organisation is the controller** (not the software). The system only needs to provide the technical measures – the legal documents are the operator's responsibility.

### Privacy Policy Template

The system provides a **placeholder** with the typical processing (what data, for what, how long). The server admin reviews and adapts it.

---

## 36. Concurrency ⚡

### The Problem

Two users edit/move the same article simultaneously:

```
User A:  Article X → Shelf 3   (loads, changes, saves)
User B:  Article X → Shelf 5   (loads, changes, saves)

→ Who wins?
```

### Strategy by Operation

#### Movements (Movement §11)

**Last-Write-Wins**:

- A movement is quick (scan → save)
- The article ends up somewhere – no data loss
- Conflicts are rare

#### Edits (changing properties)

**Optimistic Locking**:

- If two users change properties simultaneously, one change would be lost
- Check: "The object was changed in the meantime – please reload"

```python
class Article(models.Model):
    version = models.IntegerField(default=0)   # incremented on every save

# On save:
if article.version != loaded_version:
    raise ConflictError("Object was changed by someone else")
```

### Implementation

- `version` field on editable models (Article, ArticleBase, Storage, ...)
- On save: compare version, increment
- On conflict: show a message, let the user reload

---

## 37. Database & Scaling ⚡

### SQLite Limits

| Limit | Meaning |
|---|---|
| Write lock | Only **one** writer at a time (whole DB locked) |
| Size | Theoretically huge, practically slower from GB |
| Concurrency | Many simultaneous writers → queue |
| Features | No full-text index like PostgreSQL, fewer types |

### When SQLite Is Enough

- Few simultaneous users (one warehouse, one team)
- Low write load (movements are short)
- Moderate data volume (thousands of articles, not millions)
- Images NOT in the DB (on filesystem, only paths in the DB)

### When to Switch (to PostgreSQL)

- Many simultaneous writers (many organisations active)
- Large data volume
- Full-text search over everything
- Higher availability

### Decisions

1. **Keep SQLite** (for now) – simple, file-based, easy backups (§17)
2. **Images on filesystem** – not in the DB
3. **Keep the switch open** – Django ORM makes it easy (only `DATABASES` setting); no SQLite-specific tricks; DB already configurable via env (`SQL_ENGINE`)
4. **Document the threshold** – "from X simultaneous users → PostgreSQL"

### Threshold

- **Recommended threshold**: from ~20 simultaneous users → PostgreSQL
- (To be validated in practice)

---

## Summary

| # | Topic | Status |
|---|---|---|
| 1 | Multi-User preparation (owner field) | ⚡ abgenommen |
| 2 | Occasion System (types, templates, recurring, calendar) | ⚡ abgenommen |
| 3 | Roles & Permissions (construction kit, assigned/all, field-level) | ⚡ abgenommen |
| 4a–c | Dynamic Article Types (hybrid: JSON + DB columns) | ⚡ abgenommen |
| 4d | Sets / Bundles | ⚡ abgenommen |
| 4e | Article History / Audit Trail | ⚡ abgenommen |
| 5a | QR Sheet Printing (uses Query Builder §9) | ⚡ abgenommen |
| 5b–c | QR Workflow ("Where is...?", "Where should it go?", Inventory) | ⚡ abgenommen |
| 6 | Notification System (roles + users + channels + digest) | ⚡ abgenommen |
| 7a | API-First (service layer, ViewSets) | ⚡ abgenommen |
| 7b | Testing Strategy | ⚡ abgenommen |
| 7c | Migrations – safe handling | ⚡ abgenommen |
| 8 | Standard Configurations & Onboarding Wizard | ⚡ abgenommen |
| 9 | Query Builder (visual, AND/OR, parentheses, presets) | ⚡ abgenommen |
| 10 | Saved Views & Share Links (custom views, share links, link permissions) | ⚡ abgenommen |
| 11 | Movement Redesign (visible buffer, smart container default, undo, sound) | ⚡ abgenommen |
| 12 | Mobile & Navigation (responsive, sidebar replaces navbar, quick nav) | ⚡ abgenommen |
| 13 | Tags (categories, colors, inheritance, cross-cutting usage) | ⚡ abgenommen |
| 14 | Internationalization (de/en, per-user language, 3-level timezone) | ⚡ abgenommen |
| 15 | Images & Floor Plans (galleries, floor/shelf plans, OpenStreetMap) | ⚡ abgenommen |
| 16 | Power Functions (dimensions, packing, AI: vision, NLP, voice, OCR, size) | ⚡ abgenommen |
| 17 | Admin Dashboard & Backup (3-level backup, per-org export/import, restore) | ⚡ abgenommen |
| 18 | Data Migration & Transformation (existing data → new schema) | ⚡ abgenommen |
| 19 | Import (CSV/Excel, column mapping, validation, template) | ⚡ abgenommen |
| 20 | Loans & Shared Pools (borrowed articles, lender confirms, pools) | ⚡ abgenommen |
| 21 | Storage Integrity (cycle prevention, depth limit 7, onboarding) | ⚡ abgenommen |
| 22 | Multi-Organisation Membership (user in N orgs, role per org, switcher) | ⚡ abgenommen |
| 23 | Registration, Invitations & Onboarding (3 levels, policy, double-opt-in) | ⚡ abgenommen |
| 24 | Dashboard (permission-linked widgets, customizable, saved-view widgets) | ⚡ abgenommen |
| 25 | Article Model (3 levels, custom-field levels, merge/split) | ⚡ abgenommen |
| 26 | Code System & Links (codes, canonical URLs, short links, QR content) | ⚡ abgenommen |
| 27 | Soft-Delete & Trash (all objects, forever, trash view, permissions) | ⚡ abgenommen |
| 28 | Locations (django-address, coordinates, Plus Code, map) | ⚡ abgenommen |
| 29 | Security (uploads, rate limiting, HTTPS, backup encryption) | ⚡ abgenommen |
| 30 | E-Mail / SMTP (server-level, .env, fallback, templates) | ⚡ abgenommen |
| 31 | API Authentication (session + token, role-based, /api/v1/) | ⚡ abgenommen |
| 32 | Audit Log (unified, all objects, changes detail, per-org retention) | ⚡ abgenommen |
| 33 | Reporting & Statistics (reports view, diagrams, CSV/PDF export) | ⚡ abgenommen |
| 34 | PWA (installable, app shell cached, offline queue as power function) | ⚡ abgenommen |
| 35 | Data Protection / GDPR (deletion+anonymization, export, consent, template) | ⚡ abgenommen |
| 36 | Concurrency (last-write-wins for movements, optimistic locking for edits) | ⚡ abgenommen |
| 37 | Database & Scaling (SQLite limits, images on filesystem, switch threshold) | ⚡ abgenommen |