# Agents — KI-Agenten für little_WMS

Dieses Dokument beschreibt, welche opencode-Agenten für die Arbeit an **little_WMS** zur Verfügung stehen und wie sie projektbezogen eingesetzt werden.

---

## Projektkontext

| Eigenschaft | Wert |
|---|---|
| **Name** | little_WMS |
| **Zweck** | Persönliches Warehouse Management System – so einfach, dass man es benutzt |
| **Stack** | Django 6.0, Django REST Framework 3.14, Gunicorn, SQLite, Docker |
| **Sprache** | Python 3.12 |
| **Django-Apps** | `article`, `codeSystem`, `export`, `hub`, `little_wms`, `location`, `movement`, `softdelete`, `space`, `storage`, `tag` |
| **Entwicklung** | Docker-basiert via `docker compose up`, Dev-Entrypoint unter `scripts/entrypoint-dev.sh` |

---

## Verfügbare Agenten & Einsatzzweck

### Entwicklung

| Agent | Wann einsetzen |
|---|---|
| **implementierer** | Neue Features umsetzen: Django-Models, Views, Templates, REST-Endpoints, Formulare. Immer mit Verweis auf bestehende Patterns in der Codebase. |
| **bug-fixer** | Fehler beheben. Beschreibe das erwartete vs. tatsächliche Verhalten, relevante Logs und betroffene Django-App. |
| **refactorer** | Code-Struktur verbessern ohne Verhaltensänderung. Z. B. Duplikate in Views beseitigen, Querysets optimieren, Template-Struktur vereinheitlichen. |
| **tester** | Tests schreiben oder ausführen. Das Projekt hat aktuell minimale Testabdeckung – vor jedem Refactoring sollten Tests ergänzt werden. Siehe `docs/developer/testing.md` für die manuelle Test-Checkliste. |

### Qualitätssicherung

| Agent | Wann einsetzen |
|---|---|
| **code-reviewer** | PRs oder Diffs auf Codequalität, Django-Best-Practices und Projektkonventionen prüfen. |
| **security** | Sicherheitsanalyse: Secrets in Code/Config, unsichere Querysets, fehlende Permission-Checks, Dependency-Schwachstellen. |

### Planung & Recherche

| Agent | Wann einsetzen |
|---|---|
| **explore** | Codebase erkunden: Dateien finden, Abhängigkeiten zwischen Django-Apps verstehen, bestehende Patterns identifizieren. |
| **planer** | Ausführungsplan für komplexe Features erstellen, der Aufgaben auf die passenden Agenten verteilt. |
| **dirigent** | Komplexe, parallelisierbare Aufgaben orchestrieren und an Sub-Agenten delegieren. |
| **rechercheur** | Externe Recherche (Django-Docs, DRF, Deployment-Fragen). |
| **bewerter** | Technische Entscheidungen vergleichen und bewerten (z. B. Library-Wahl, Architekturansätze). |

### Infrastruktur & Betrieb

| Agent | Wann einsetzen |
|---|---|
| **devops** | Docker, docker-compose, CI/CD, Deployment-Konfiguration. |
| **dependency-manager** | `requirements.txt` prüfen und aktualisieren. |
| **scaffolder** | Neue Django-App innerhalb des Projekts anlegen (Models, Admin, Views, URLs, Templates-Grundgerüst). |

### Dokumentation

| Agent | Wann einsetzen |
|---|---|
| **dokumentierer** | README, Docs unter `docs/`, Inline-Docstrings, API-Dokumentation. |

---

## Projektspezifische Konventionen

Diese Konventionen müssen jedem Agenten-Prompt mitgegeben werden, wenn sie relevant sind:

### Git

- **Commit-Namespace**: `type: what` — Typen sind `fix`, `add`, `clean`, `refactor`, `delete` (siehe `docs/git commit namespace.md`)
- **Branch-Naming**: `typ/kanban-id/kurzerName` — z. B. `feat/42/ArticleCalendar`, `bug/67/MultiSelectError`
- **Base-Branch**: `dev` (nicht `main`)
- **Mergen**: Merges werden **nicht** von Agenten durchgeführt. Das Zusammenführen von Branches (z. B. nach `dev` oder `main`) ist ausschließlich Aufgabe des menschlichen Maintainers. Agenten erstellen und committen auf ihren Feature-Branches, führen aber keine Merge- oder Rebase-Operationen durch.

### Django

- **App-Struktur**: Jede Django-App liegt direkt unter `src/` (z. B. `src/article/`, `src/storage/`)
- **Templates**: Pro App unter `templates/<app>/`, Module unter `templates/<app>/modules/` (kein `extends header.html`)
- **Settings**: Zentrale Konfiguration in `src/little_wms/settings.py`
- **URLs**: Pro App eine `urls.py`, eingehängt in `src/little_wms/urls.py`
- **Soft-Delete**: Die App `softdelete` stellt übergreifende Soft-Delete-Logik bereit

### Docker-Entwicklung

- Dev-Entrypoint: `scripts/entrypoint-dev.sh` (mit Livereload)
- Bei neuen Abhängigkeiten: Image mit `./scripts/build.sh` neu bauen, dann `docker compose up`
- Datenbank-Persistenz: `./data/` wird als Volume gemountet

---

## Prompt-Bausteine

Diese Abschnitte können in Agenten-Prompts wiederverwendet werden:

### Django-Kontext (immer mitgeben bei Code-Aufgaben)

```
Das Projekt ist ein Django 6.0 WMS mit Django REST Framework 3.14.
Arbeitsverzeichnis: src/
Django-Apps: article, codeSystem, export, hub, little_wms, location, movement, softdelete, space, storage, tag
Templates liegen unter templates/<app>/, Module unter templates/<app>/modules/.
Settings: src/little_wms/settings.py
URLs: src/little_wms/urls.py (Root) + pro App eine urls.py
```

### Docker-Dev-Kontext

```
Entwicklungsumgebung: Docker via docker compose up.
Dev-Entrypoint: scripts/entrypoint-dev.sh (mit Livereload).
Bei neuen Abhängigkeiten: requirements.txt aktualisieren, dann Image mit ./scripts/build.sh neu bauen.
Daten persistieren in ./data/ (als Volume gemountet).
```

---

## Typische Workflows

### Neues Feature entwickeln

1. **planer** → Plan erstellen lassen
2. **explore** → Betroffene Dateien und Patterns identifizieren
3. **implementierer** → Feature umsetzen (mit Django-Kontext-Prompt)
4. **tester** → Tests schreiben/ausführen
5. **code-reviewer** → Diff prüfen lassen

### Bug fixen

1. **explore** → Fehlerquelle eingrenzen
2. **bug-fixer** → Fix umsetzen
3. **tester** → Regression prüfen

### Refactoring

1. **explore** → Betroffenen Code kartieren
2. **tester** → Vorher Tests schreiben (Absicherung)
3. **refactorer** → Refactoring durchführen
4. **tester** → Nachher Tests ausführen