# Test Development Documentation

**Version:** 1.0  
**Letzte Aktualisierung:** 10. Dezember 2025  
**Status:** ✅ Active

---

## 🎯 Übersicht

Diese Directory (`tests/doc/`) enthält **alle Dokumentation**, die während der **Test-Entwicklung** entsteht. Dies umfasst Anleitungen, Pläne, Templates und Entscheidungsdokumente.

**Trennung:**
- `docs/` (Root-Level) = Production-Dokumentation für Endbenutzer
- `tests/doc/` (hier) = Entwicklungs-Dokumentation für Entwickler/Tester

---

## 📁 Verzeichnisstruktur

```
tests/doc/
├── README.md              ← Diese Datei (Index/Übersicht)
│
├── guides/                ← Anleitungen & Handbücher
│   ├── struktur_optimierung_v1.0.md
│   ├── tester_anleitung_v1.1.md
│   └── development_setup_v1.0.md
│
├── planning/              ← Planung & Roadmaps
│   ├── parser_entwicklungsplan_v2.3.md
│   ├── test_strategy_v1.0.md
│   └── feature_backlog_v1.0.md
│
├── templates/             ← Wiederverwendbare Templates
│   ├── implementation_templates_v2.3.md
│   ├── test_case_template_v1.0.md
│   └── bug_report_template_v1.0.md
│
├── decisions/             ← Architecture Decision Records (ADR)
│   ├── 001_test_structure_decision.md
│   ├── 002_parser_precedence_approach.md
│   └── 003_documentation_location.md
│
└── archive/               ← Alte Versionen (zur Referenz)
    ├── parser_entwicklungsplan_v2.2.md
    └── struktur_optimierung_v0.9.md
```

---

## 📂 Verzeichnis-Details

### guides/
**Zweck:** Anleitungen, Handbücher und How-Tos für Entwickler und Tester

**Inhalt:**
- Benutzerhandbücher für Tools (z.B. Parser Tester)
- Setup-Anleitungen
- Best Practices
- Troubleshooting Guides

**Beispiele:**
- `struktur_optimierung_v1.0.md` - Projekt-Struktur Optimierungsleitfaden
- `tester_anleitung_v1.1.md` - Parser Tester Benutzerhandbuch
- `development_setup_v1.0.md` - Entwicklungsumgebung Setup

---

### planning/
**Zweck:** Planungsdokumente, Roadmaps und Strategien

**Inhalt:**
- Entwicklungs-Roadmaps
- Test-Strategien
- Feature-Backlogs
- Sprint-Pläne

**Beispiele:**
- `parser_entwicklungsplan_v2.3.md` - Parser Development Roadmap v2.3
- `test_strategy_v1.0.md` - Test-Strategie und -Ansatz
- `feature_backlog_v1.0.md` - Geplante Features

---

### templates/
**Zweck:** Wiederverwendbare Templates für wiederkehrende Aufgaben

**Inhalt:**
- Code-Implementation Templates
- Test-Case Templates
- Bug-Report Templates
- Dokumentations-Templates

**Beispiele:**
- `implementation_templates_v2.3.md` - Code-Implementation Vorlagen
- `test_case_template_v1.0.md` - Test-Fall Vorlage
- `bug_report_template_v1.0.md` - Bug-Report Vorlage

---

### decisions/
**Zweck:** Architecture Decision Records (ADRs) - Dokumentation wichtiger technischer Entscheidungen

**Format:** Nummeriert (001, 002, 003, ...)

**Inhalt:**
- Kontext der Entscheidung
- Getroffene Entscheidung
- Alternativen die erwogen wurden
- Konsequenzen

**Beispiele:**
- `001_test_structure_decision.md` - Warum tests/ Struktur so gewählt wurde
- `002_parser_precedence_approach.md` - Operator Precedence Ansatz
- `003_documentation_location.md` - Dokumentations-Struktur Entscheidung

---

### archive/
**Zweck:** Alte Versionen von Dokumenten zur Referenz

**Inhalt:**
- Superseded Dokumentationen
- Alte Versionen von Plänen/Anleitungen
- Historische Referenz

**Beispiele:**
- `parser_entwicklungsplan_v2.2.md` - Alte Roadmap-Version
- `struktur_optimierung_v0.9.md` - Vorherige Struktur-Empfehlung

**Hinweis:** Wird optional in .gitignore ignoriert

---

## 📝 Naming Convention

Alle Dateien folgen dieser Namenskonvention:

```
{topic}_{description}_v{version}.md
```

### Komponenten:

| Teil | Beschreibung | Beispiel |
|------|--------------|----------|
| `topic` | Hauptthema | parser, tester, struktur, setup |
| `description` | Beschreibung | entwicklungsplan, anleitung, optimierung |
| `v{version}` | Versionsnummer | v1.0, v1.1, v2.3 |

### Beispiele:

```
parser_entwicklungsplan_v2.3.md
tester_anleitung_v1.1.md
struktur_optimierung_v1.0.md
implementation_templates_v2.3.md
test_strategy_v1.0.md
```

### Regeln:

1. **Kleinschreibung** (lowercase)
2. **Unterstriche** statt Leerzeichen (`_`)
3. **Deskriptiv** aber **kurz**
4. **Versioniert** mit `v{major}.{minor}`
5. **Konsistent** mit bestehenden Dateien

---

## 🔄 Versionierung

### Versionsschema: `v{major}.{minor}`

| Version | Bedeutung | Wann verwenden |
|---------|-----------|----------------|
| v1.0 | Initial Release | Erste Version eines Dokuments |
| v1.1 | Minor Update | Kleine Änderungen, Ergänzungen, Korrekturen |
| v1.2 | Minor Update | Weitere kleine Änderungen |
| v2.0 | Major Update | Große Änderungen, Umstrukturierung |

### Update-Prozess:

Wenn du ein Dokument aktualisierst:

```bash
# 1. Alte Version archivieren
mv tests/doc/guides/tester_anleitung_v1.1.md tests/doc/archive/

# 2. Neue Version erstellen
cp tests/doc/archive/tester_anleitung_v1.1.md tests/doc/guides/tester_anleitung_v1.2.md

# 3. Änderungen vornehmen
vim tests/doc/guides/tester_anleitung_v1.2.md

# 4. README.md aktualisieren (diese Datei)
# - Neue Version in Liste eintragen
# - Datum aktualisieren
```

### Changelog-Format (in Dokument):

Jedes Dokument sollte einen Changelog am Ende haben:

```markdown
## Changelog

### v1.2 (10. Dez 2025)
- Feature XYZ hinzugefügt
- Sektion ABC verbessert
- Typos korrigiert

### v1.1 (09. Dez 2025)
- Neue Beispiele hinzugefügt
- Troubleshooting erweitert

### v1.0 (08. Dez 2025)
- Initial Release
```

---

## 📋 Aktuelle Dokumente

### Guides

| Datei | Version | Datum | Beschreibung |
|-------|---------|-------|--------------|
| `struktur_optimierung_v1.0.md` | v1.0 | 10. Dez 2025 | Projekt-Struktur Optimierung & Best Practices |
| `tester_anleitung_v1.1.md` | v1.1 | 10. Dez 2025 | Parser Tester Benutzerhandbuch |

### Planning

| Datei | Version | Datum | Beschreibung |
|-------|---------|-------|--------------|
| `parser_entwicklungsplan_v2.3.md` | v2.3 | 10. Dez 2025 | Parser Development Roadmap |

### Templates

| Datei | Version | Datum | Beschreibung |
|-------|---------|-------|--------------|
| `implementation_templates_v2.3.md` | v2.3 | 10. Dez 2025 | Code-Implementation Vorlagen |

---

## 🎯 Verwendung

### Neues Dokument erstellen

```bash
# 1. Wähle passende Kategorie (guides/, planning/, templates/, decisions/)
# 2. Wähle aussagekräftigen Namen nach Naming Convention
# 3. Erstelle Datei mit v1.0

touch tests/doc/guides/neues_feature_anleitung_v1.0.md

# 4. Fülle mit Inhalt
vim tests/doc/guides/neues_feature_anleitung_v1.0.md

# 5. Aktualisiere dieses README.md
```

### Dokument aktualisieren

```bash
# 1. Archiviere alte Version
mv tests/doc/guides/dokument_v1.0.md tests/doc/archive/

# 2. Erstelle neue Version
cp tests/doc/archive/dokument_v1.0.md tests/doc/guides/dokument_v1.1.md

# 3. Bearbeite
vim tests/doc/guides/dokument_v1.1.md

# 4. Update README.md (diese Datei)
```

### Dokument finden

```bash
# Suche nach Thema
grep -r "parser" tests/doc/

# Liste alle aktuellen Versionen
ls tests/doc/guides/
ls tests/doc/planning/

# Zeige alle Versionen eines Dokuments
ls tests/doc/guides/tester_anleitung_*
ls tests/doc/archive/tester_anleitung_*
```

---

## 🔗 Verwandte Dokumentation

### Production Docs (Root-Level)
- `docs/DOCUMENTATION.md` - Haupt-Dokumentation für Endbenutzer
- `docs/pubmed-syntax.md` - PubMed Syntax Guide
- `docs/europe-pmc-syntax.md` - Europe PMC Syntax Guide
- `README.md` - Projekt-Übersicht

### Test-Related (tests/)
- `tests/README.md` - Test-Environment Übersicht
- `tests/queries/` - Test-Query-Dateien
- `tests/fixtures/` - Test-Daten

---

## 💡 Best Practices

### DO ✅

- **Versioniere** alle Dokumente
- **Archiviere** alte Versionen statt sie zu löschen
- **Dokumentiere** Änderungen in Changelog
- **Verwende** konsistente Namenskonvention
- **Aktualisiere** dieses README.md bei Änderungen
- **Schreibe** verständlich und strukturiert
- **Füge** Beispiele und Screenshots hinzu

### DON'T ❌

- ❌ Dokumente ohne Versionsnummer
- ❌ Alte Versionen einfach überschreiben
- ❌ Inkonsistente Dateinamen
- ❌ Fehlende Changelogs
- ❌ Zu lange oder kryptische Namen
- ❌ Dokumente ohne Kontext
- ❌ README.md vergessen zu aktualisieren

---

## 🛠️ Wartung

### Regelmäßige Aufgaben

**Monatlich:**
- Überprüfe Aktualität der Dokumente
- Archiviere veraltete Versionen
- Aktualisiere Tabellen in diesem README.md

**Bei Releases:**
- Update Versionen in planning/ Dokumenten
- Erstelle neue Versionen von Guides falls nötig
- Archiviere alte Roadmap-Versionen

**Bei strukturellen Änderungen:**
- Aktualisiere entsprechende Guide-Dokumente
- Dokumentiere Entscheidung in decisions/
- Update README.md

---

## 📞 Kontakt & Support

Bei Fragen zur Dokumentation:
1. Lese dieses README.md vollständig
2. Checke existierende Dokumente in `guides/`
3. Lese entsprechende ADRs in `decisions/`
4. Öffne Issue im Projekt-Tracker

---

## 🔄 Changelog (README.md)

### v1.0 (10. Dezember 2025)
- Initial Version
- Struktur definiert (guides/, planning/, templates/, decisions/, archive/)
- Naming Convention festgelegt
- Versionierungs-Schema definiert
- Best Practices dokumentiert

---

**Status:** ✅ Active & Maintained  
**Owner:** Development Team  
**Letzte Aktualisierung:** 10. Dezember 2025, 20:55 CET
