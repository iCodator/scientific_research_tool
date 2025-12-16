# Boolean Query Parser - Documentation

**Deutsch:** Siehe unten / **English:** See above

---

## English

### Overview

This directory contains all documentation for the Boolean Query Parser v7.0.

### Documentation Files

#### User Guides

- **[USER_GUIDE_EN.md](USER_GUIDE_EN.md)** - Complete English user guide for end users
- **[BENUTZERHANDBUCH_DE.md](BENUTZERHANDBUCH_DE.md)** - Vollständiges deutsches Benutzerhandbuch für Endbenutzer

#### Developer Documentation

- **[DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md)** - Internal development documentation covering:
  - Project overview and evolution (v1.0 → v7.0)
  - Design goals and decisions
  - Technical challenges and solutions
  - Architecture and testing strategy
  - Lessons learned

### Quick Reference - Operators

#### English Operators
```
AND  - Both terms must appear
OR   - Either term must appear
NOT  - Term must NOT appear
```

#### German Operators
```
UND  - Beide Begriffe müssen vorkommen
ODER - Einer der Begriffe muss vorkommen
NICHT, KEIN, KEINE, OHNE - Begriff darf NICHT vorkommen
```

### Quick Reference - Formats

#### Single-Line Format
```
"A" AND "B" OR "C"
```
- Everything on one line
- Use for complex nested queries
- Mixed operators require explicit parentheses

#### Multi-Line Format
```
"A"
OR
"B"
OR
"C"
```
- Queries spread across multiple lines
- Operators on separate lines
- Requires: 3+ lines, odd count, same operator throughout
- Each line must have balanced parentheses

### Key Rules

✅ **DO:**
- Quote all terms: `"term"`
- Use parentheses for mixed operators: `("A" OR "B") AND "C"`
- Keep multi-line operators consistent
- Balance parentheses within each line (multi-line)

❌ **DON'T:**
- Leave terms unquoted: `term`
- Mix operators without parentheses: `"A" OR "B" AND "C"`
- Use different operators in multi-line format
- Span parentheses across operator lines

### Document Structure

| Document | Audience | Content | Length |
|----------|----------|---------|--------|
| USER_GUIDE_EN.md | End users, researchers | How to write queries, operators, examples, troubleshooting | ~400 lines |
| BENUTZERHANDBUCH_DE.md | German-speaking users | German version of user guide | ~400 lines |
| DEVELOPMENT_HISTORY.md | Developers, maintainers | Design decisions, challenges, architecture, lessons learned | ~600 lines |

### Common Questions

**Q: Can I use operator precedence (AND before OR)?**  
A: No. Require explicit parentheses to avoid ambiguity: `("A" OR "B") AND "C"`

**Q: Can I span parentheses across lines in multi-line format?**  
A: No. Each line must have balanced parentheses. Use single-line format for complex nesting.

**Q: Can I use unquoted terms?**  
A: No. All terms must be quoted to prevent parsing ambiguity: `"cancer"`

**Q: What operators are supported?**  
A: English (AND, OR, NOT) and German (UND, ODER, NICHT, KEIN, KEINE, OHNE)

**Q: Can I mix English and German operators?**  
A: Yes. Both are supported: `"A" AND "B" UND "C"`

### Examples

See the [examples/](../examples/) directory for more examples.

**Simple AND:**
```
"cancer" AND "treatment"
→ ((cancer) AND (treatment))
```

**Multi-line OR:**
```
"cancer"
OR
"tumor"
OR
"neoplasm"
→ (((cancer) OR (tumor)) OR (neoplasm))
```

**Complex mixed:**
```
("cancer" OR "tumor") AND ("treatment" OR "therapy")
→ ((((cancer) OR (tumor))) AND (((treatment) OR (therapy))))
```

---

---

## Deutsch

### Übersicht

Dieses Verzeichnis enthält die gesamte Dokumentation für den Boolean Query Parser v7.0.

### Dokumentationsdateien

#### Benutzerhandbücher

- **[USER_GUIDE_EN.md](USER_GUIDE_EN.md)** - Vollständiges englisches Benutzerhandbuch für Endbenutzer
- **[BENUTZERHANDBUCH_DE.md](BENUTZERHANDBUCH_DE.md)** - Vollständiges deutsches Benutzerhandbuch für Endbenutzer

#### Entwicklerdokumentation

- **[DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md)** - Interne Entwicklungsdokumentation mit:
  - Projektübersicht und Evolution (v1.0 → v7.0)
  - Designziele und Entscheidungen
  - Technische Herausforderungen und Lösungen
  - Architektur- und Teststrategie
  - Gewonnene Erkenntnisse

### Schnellreferenz - Operatoren

#### Englische Operatoren
```
AND  - Beide Begriffe müssen vorkommen
OR   - Einer der Begriffe muss vorkommen
NOT  - Begriff darf NICHT vorkommen
```

#### Deutsche Operatoren
```
UND  - Beide Begriffe müssen vorkommen
ODER - Einer der Begriffe muss vorkommen
NICHT, KEIN, KEINE, OHNE - Begriff darf NICHT vorkommen
```

### Schnellreferenz - Formate

#### Einzeiliges Format
```
"A" UND "B" ODER "C"
```
- Alles in einer Zeile
- Verwendung für komplexe verschachtelte Anfragen
- Gemischte Operatoren erfordern explizite Klammern

#### Mehrzeiliges Format
```
"A"
ODER
"B"
ODER
"C"
```
- Anfragen über mehrere Zeilen verteilt
- Operatoren auf separaten Zeilen
- Erforderlich: 3+ Zeilen, ungerade Anzahl, gleicher Operator durchgehend
- Jede Zeile muss ausgeglichene Klammern haben

### Wichtige Regeln

✅ **Tun Sie:**
- Alle Begriffe in Anführungszeichen: `"Begriff"`
- Klammern für gemischte Operatoren: `("A" ODER "B") UND "C"`
- Mehrzeilige Operatoren konsistent halten
- Klammern innerhalb jeder Zeile ausgleichen (mehrzeilig)

❌ **Tun Sie nicht:**
- Begriffe ohne Anführungszeichen: `Begriff`
- Operatoren ohne Klammern mischen: `"A" ODER "B" UND "C"`
- Verschiedene Operatoren im mehrzeiligen Format verwenden
- Klammern über Operatorzeilen spannen

### Dokumentstruktur

| Dokument | Zielgruppe | Inhalt | Länge |
|----------|-----------|--------|-------|
| USER_GUIDE_EN.md | Endbenutzer, Forscher | Wie man Anfragen schreibt, Operatoren, Beispiele, Fehlerbehebung | ~400 Zeilen |
| BENUTZERHANDBUCH_DE.md | Deutschsprachige Benutzer | Deutsche Version des Benutzerhandbuchs | ~400 Zeilen |
| DEVELOPMENT_HISTORY.md | Entwickler, Maintainer | Designentscheidungen, Herausforderungen, Architektur, Erkenntnisse | ~600 Zeilen |

### Häufig Gestellte Fragen

**F: Kann ich Operator-Vorrang verwenden (UND vor ODER)?**  
A: Nein. Verwenden Sie explizite Klammern, um Mehrdeutigkeit zu vermeiden: `("A" ODER "B") UND "C"`

**F: Kann ich Klammern über Zeilen im mehrzeiligen Format spannen?**  
A: Nein. Jede Zeile muss ausgeglichene Klammern haben. Verwenden Sie das einzeilige Format für komplexe Verschachtelung.

**F: Kann ich Begriffe ohne Anführungszeichen verwenden?**  
A: Nein. Alle Begriffe müssen in Anführungszeichen stehen, um Parsing-Mehrdeutigkeit zu vermeiden: `"Krebs"`

**F: Welche Operatoren werden unterstützt?**  
A: Englisch (AND, OR, NOT) und Deutsch (UND, ODER, NICHT, KEIN, KEINE, OHNE)

**F: Kann ich englische und deutsche Operatoren mischen?**  
A: Ja. Beide werden unterstützt: `"A" AND "B" UND "C"`

### Beispiele

Weitere Beispiele finden Sie im Verzeichnis [examples/](../examples/).

**Einfaches UND:**
```
"Krebs" UND "Behandlung"
→ ((Krebs) AND (Behandlung))
```

**Mehzeiliges ODER:**
```
"Krebs"
ODER
"Tumor"
ODER
"Neoplasma"
→ (((Krebs) OR (Tumor)) OR (Neoplasma))
```

**Komplex gemischt:**
```
("Krebs" ODER "Tumor") UND ("Behandlung" ODER "Therapie")
→ ((((Krebs) OR (Tumor))) AND (((Behandlung) OR (Therapie))))
```
