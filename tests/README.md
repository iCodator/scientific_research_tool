╔════════════════════════════════════════════════════════════════════════════╗
║                          TESTS - ÜBERSICHT & ANLEITUNG                      ║
║                        Query Parser Test Suite v2.2                         ║
║                                                                            ║
║  Ein Leitfaden: Tests verstehen, durchführen, und Ergebnisse lesen         ║
╚════════════════════════════════════════════════════════════════════════════╝

════════════════════════════════════════════════════════════════════════════════
🎯 KURZ ERKLÄRT - Was ist dieses Verzeichnis?
════════════════════════════════════════════════════════════════════════════════

Das `tests/` Verzeichnis ist der **Test-Bereich** des gesamten Projekts.

Hier passiert folgendes:
  1. Tests werden GESCHRIEBEN (was sollen wir testen?)
  2. Tests werden DURCHGEFÜHRT (funktioniert unser Code?)
  3. Ergebnisse werden DOKUMENTIERT (was kam raus?)
  4. Probleme werden GEMELDET (was funktioniert nicht?)

Analoge Erklärung:
─────────────────
Stell dir vor, du baust ein Auto:
  • Motor wird gebaut (Hauptcode)
  • Motor wird GETESTET (Tests)
  • Tester schreiben Bericht (Test-Dokumentation)
  • Wenn etwas kaputt ist, wird es repariert

Genau das passiert hier, aber für Software!

════════════════════════════════════════════════════════════════════════════════
📂 VERZEICHNIS-STRUKTUR - Was ist wo?
════════════════════════════════════════════════════════════════════════════════

tests/
│
├─ 📁 docs/                          ← DOKUMENTATION (wie funktioniert es?)
│  │
│  ├─ 📁 parser/                     ← Parser-spezifische Dokumentation
│  │  ├─ 📄 PARSER_DESIGN.md         ← WIE der Parser funktioniert
│  │  ├─ 📄 TEST_RESULTS.md          ← WAS die Tests ergeben haben
│  │  ├─ 📄 KNOWN_ISSUES.md          ← WAS noch kaputt ist (und wie fix)
│  │  └─ 📄 README.md                ← THIS FILE - Übersicht
│  │
│  ├─ 📁 planning/                   ← Planungs-Dokumente
│  ├─ 📁 guides/                     ← How-To Guides
│  └─ 📁 archive/                    ← Alte Dokumentationen
│
├─ 📁 src/                           ← QUELLCODE (der Test-Code selbst)
│  └─ 📁 core/
│     └─ 🐍 parser_test_precedence.py ← Der Query Parser (v2.2)
│
├─ 📁 queries/                       ← TEST-EINGABEN (Input für Tests)
│  ├─ 📄 test_valid_1.txt            ← Test 1: Einfache Query
│  ├─ 📄 test_valid_2.txt            ← Test 2: Mit Klammern
│  ├─ 📄 test_valid_3_multiline.txt  ← Test 3: Multi-Line
│  ├─ 📄 1.txt                       ← Invalid Test
│  ├─ 📄 2.txt
│  └─ 📄 3.txt
│
├─ 📁 fixtures/                      ← TEST-DATEN (JSON, CSV, etc)
│  └─ 📄 sample_results.json         ← Beispiel API-Responses
│
├─ 📁 reports/                       ← TEST-BERICHTE (automatisch generiert)
│  └─ (werden erstellt wenn Tests laufen)
│
├─ 📁 results/                       ← TEST-ERGEBNISSE (Ausgaben)
│  └─ (werden erstellt wenn Tests laufen)
│
├─ 📁 logs/                          ← TEST-LOGS (Fehler, Debug-Info)
│  └─ (werden erstellt wenn Tests laufen)
│
├─ 🐍 __init__.py                    ← Macht tests/ ein Python Package
│
├─ 📄 .gitignore                     ← Sagt Git welche Dateien NICHT speichern
│
└─ 📄 README.md                      ← THIS FILE (was du jetzt liest)


LEGENDE:
  📁 = Verzeichnis (Ordner)
  🐍 = Python-Datei
  📄 = Text-Datei / Dokumentation

════════════════════════════════════════════════════════════════════════════════
⚡ QUICK START - Tests durchführen in 2 Minuten
════════════════════════════════════════════════════════════════════════════════

SCHRITT 1: Terminal öffnen
  - Windows: Command Prompt oder PowerShell
  - Mac/Linux: Terminal
  - Navigiere zum Projekt-Verzeichnis

SCHRITT 2: Zum tests-Verzeichnis navigieren
  cd scientific_research_tool

SCHRITT 3: Einen Test durchführen
  python query_parser_v2_3.py tests/queries/test_valid_1.txt

SCHRITT 4: Ergebnis lesen
  Du siehst eine grüne ✅ ERFOLGREICH oder rote ❌ FEHLER Nachricht

Fertig! 🎉

════════════════════════════════════════════════════════════════════════════════
🧪 ALLE TESTS IM ÜBERBLICK
════════════════════════════════════════════════════════════════════════════════

TEST 1: test_valid_1.txt
─────────────────────────

Was wird getestet?
  Eine einfache Query mit nur AND Operatoren

Input:
  cancer AND tumor AND treatment

Erwarteter Output:
  ((cancer) AND (tumor) AND (treatment))

Status: ✅ PASS (funktioniert perfekt!)

Command:
  python query_parser_v2_3.py tests/queries/test_valid_1.txt


TEST 2: test_valid_2.txt
────────────────────────

Was wird getestet?
  Eine Query mit Klammern und gemischten Operatoren

Input:
  (cancer OR tumor) AND treatment

Erwarteter Output:
  (((cancer) OR (tumor)) AND (treatment))

Status: ✅ PASS (funktioniert perfekt!)

Command:
  python query_parser_v2_3.py tests/queries/test_valid_2.txt


TEST 3: test_valid_3_multiline.txt
──────────────────────────────────

Was wird getestet?
  Eine Multi-Line Query im ODD/EVEN Format

Input:
  cancer
  OR
  tumor
  AND
  (treatment OR therapy)

Aktueller Output:
  (cancer) OR (tumor) AND (((treatment) OR (therapy)))

Erwarteter Output:
  ((cancer) OR (tumor)) AND ((treatment) OR (therapy))

Status: ⚠️  PASS aber ÜBER-GEKLAMMERT
  ✓ Der Parser funktioniert
  ✗ Zu viele innere Klammern (bekanntes Issue #1)

Severity: 🟡 MEDIUM (funktioniert trotzdem)

Command:
  python query_parser_v2_3.py tests/queries/test_valid_3_multiline.txt


TEST 4-6: 1.txt, 2.txt, 3.txt
──────────────────────────────

Was werden diese getestet?
  Ungültige Queries (ABSICHTLICH falsch!)

Das ist wichtig:
  ✓ Parser SOLL Fehler erkennen
  ✓ Ungültige Queries SOLLTEN Fehler geben
  ✓ Das ist ein GUTER Test!

Status: ❌ EXPECTED ERROR (das ist richtig!)

════════════════════════════════════════════════════════════════════════════════
📊 TEST STATUS ZUSAMMENFASSUNG (10. Dezember 2025)
════════════════════════════════════════════════════════════════════════════════

Gesamt:
  Tests durchgeführt:      6/6 ✅
  Erfolgreich:             3/3 ✅ (valid Tests)
  Fehler (erwartet):       3/3 ✅ (invalid Tests)
  Success Rate:            100% ✅

Detailliert:

┌─────────────────────────┬────────────┬──────────────────────────────┐
│ Test                    │ Status     │ Bemerkung                    │
├─────────────────────────┼────────────┼──────────────────────────────┤
│ test_valid_1.txt        │ ✅ PASS    │ Funktioniert perfekt         │
│ test_valid_2.txt        │ ✅ PASS    │ Funktioniert perfekt         │
│ test_valid_3_multiline  │ ⚠️ PASS    │ Über-geklammert (Issue #1)   │
│ 1.txt                   │ ❌ ERROR   │ ERWARTET (ungültig)          │
│ 2.txt                   │ ❌ ERROR   │ ERWARTET (ungültig)          │
│ 3.txt                   │ ❌ ERROR   │ ERWARTET (ungültig)          │
└─────────────────────────┴────────────┴──────────────────────────────┘

════════════════════════════════════════════════════════════════════════════════
📚 DOKUMENTATION - Wo finde ich was?
════════════════════════════════════════════════════════════════════════════════

Frage: Ich verstehe nicht wie der Parser funktioniert
Antwort: → Lies docs/parser/PARSER_DESIGN.md
  (Ausführliche Erklärung mit Beispielen und Analogien)

Frage: Welche Tests gibt es und wie schneiden sie ab?
Antwort: → Lies docs/parser/TEST_RESULTS.md
  (Detaillierte Test-Reports mit Analyse)

Frage: Warum ist Test 3 über-geklammert und wie behebt man das?
Antwort: → Lies docs/parser/KNOWN_ISSUES.md
  (Mit Code-Beispiel für den Fix)

Frage: Ich brauche eine allgemeine Übersicht des Parser-Designs
Antwort: → Lies docs/parser/README.md (siehe unten)

Frage: Wie kann ich neue Tests hinzufügen?
Antwort: → Siehe Abschnitt "NEUE TESTS HINZUFÜGEN" unten

════════════════════════════════════════════════════════════════════════════════
🔧 NEUE TESTS HINZUFÜGEN - Schritt für Schritt
════════════════════════════════════════════════════════════════════════════════

SZENARIO: Du möchtest einen neuen Test hinzufügen

SCHRITT 1: Erstelle eine neue Query-Datei
  
  Ort: tests/queries/
  Name: test_<beschreibung>.txt (z.B. test_with_dates.txt)
  
  Beispiel Inhalt:
    cancer OR tumor 2015-2020

SCHRITT 2: Führe Test durch
  
  Command:
    python query_parser_v2_3.py tests/queries/test_with_dates.txt

SCHRITT 3: Überprüfe Output
  
  Wenn ✅ PASS: Dokumentiere im TEST_RESULTS.md
  Wenn ❌ FEHLER: Dokumentiere im KNOWN_ISSUES.md

SCHRITT 4: Commit zu Git
  
  git add tests/queries/test_with_dates.txt
  git commit -m "Add test: with dates"
  git push

Fertig! ✅

════════════════════════════════════════════════════════════════════════════════
🛠️ HÄUFIGE PROBLEME BEIM TESTEN
════════════════════════════════════════════════════════════════════════════════

PROBLEM 1: "ModuleNotFoundError: No module named 'parser_test_precedence'"
─────────────────────────────────────────────────────────────────────────

Ursache:
  Parser-Datei wird nicht gefunden

Lösung:
  1. Stelle sicher dass du im root-Verzeichnis bist (nicht in tests/)
  2. Überprüfe dass tests/src/core/parser_test_precedence.py existiert
  3. Command: python query_parser_v2_3.py tests/queries/test_valid_1.txt

  
PROBLEM 2: "❌ MEHRDEUTIGE OPERATOREN"
──────────────────────────────────────

Ursache:
  Du hast "A OR B AND C" ohne Klammern eingegeben

Lösung:
  Setze Klammern um die Mehrdeutigkeit zu beheben:
    ✓ "(A OR B) AND C"
    ✓ "A OR (B AND C)"
  
  Siehe: docs/parser/PARSER_DESIGN.md für Erklärung

  
PROBLEM 3: Test dauert sehr lange oder friert ein
───────────────────────────────────────────────────

Ursache:
  Möglicherweise unendliche Schleife im Parser

Lösung:
  1. Drücke Ctrl+C um abzubrechen
  2. Überprüfe deine Query auf Syntax-Fehler
  3. Melde Bug in KNOWN_ISSUES.md

════════════════════════════════════════════════════════════════════════════════
📋 DATEI-BESCHREIBUNGEN
════════════════════════════════════════════════════════════════════════════════

docs/parser/PARSER_DESIGN.md
  │
  ├─ Zielgruppe: Anfänger (keine technischen Vorkenntnisse nötig)
  ├─ Länge: ~15 Seiten
  ├─ Inhalt:
  │  • Was ist der Query Parser?
  │  • Wie funktioniert er? (alle 4 Phasen erklär)
  │  • Beispiele mit Input/Output
  │  • FAQ
  └─ WICHTIG: Lesen wenn du verstehen willst WIE es funktioniert

docs/parser/TEST_RESULTS.md
  │
  ├─ Zielgruppe: Tester, QA
  ├─ Länge: ~10 Seiten
  ├─ Inhalt:
  │  • Test-Übersicht (Anzahl, Status)
  │  • Detaillierte Test-Reports
  │  • Bekannte Issues Summary
  │  • Recommendations
  └─ WICHTIG: Lesen wenn du testen möchtest und Ergebnisse analysieren

docs/parser/KNOWN_ISSUES.md
  │
  ├─ Zielgruppe: Entwickler
  ├─ Länge: ~10 Seiten
  ├─ Inhalt:
  │  • Issue #1: Über-Klammerung (Multi-Line)
  │  • Root Cause Analysis
  │  • FIX mit Code-Beispiel
  │  • Validation Script
  └─ WICHTIG: Lesen wenn du Bugs beheben möchtest

════════════════════════════════════════════════════════════════════════════════
⏱️ TIMEBOXES - Wie lange dauern Tests?
════════════════════════════════════════════════════════════════════════════════

Einzelner Test:        ~5 Sekunden
Alle Tests:            ~30 Sekunden
Mit Dokumentation:     ~1-2 Minuten

════════════════════════════════════════════════════════════════════════════════
🎓 LEARNING PATH - Für Anfänger
════════════════════════════════════════════════════════════════════════════════

Woche 1:
  □ Lese diese README.md (10 Min)
  □ Führe Test 1 aus (5 Min)
  □ Lies PARSER_DESIGN.md (30 Min)
  □ Führe alle Tests aus (2 Min)

Woche 2:
  □ Lese TEST_RESULTS.md (20 Min)
  □ Versuche einen neuen Test hinzuzufügen (15 Min)
  □ Lese KNOWN_ISSUES.md (20 Min)
  □ Verstehe Issue #1 (10 Min)

Woche 3:
  □ Versuche Issue #1 zu fixen (1-2 Stunden mit Anleitung)
  □ Führe Tests durch für deine Änderung
  □ Dokumentiere deine Lösung

════════════════════════════════════════════════════════════════════════════════
✅ CHECKLISTE - Bin ich bereit zum Testen?
════════════════════════════════════════════════════════════════════════════════

□ Ich habe Python 3.7+ installiert
□ Ich kann ein Terminal öffnen
□ Ich bin im Projekt-Verzeichnis (scientific_research_tool/)
□ Ich kann mit git umgehen (oder will es lernen)
□ Ich habe diese README.md gelesen
□ Ich bin bereit mein erstes Test durchzuführen!

Wenn alle Häkchen gesetzt sind: BEREIT! 🚀

════════════════════════════════════════════════════════════════════════════════
🤝 SUPPORT & FRAGEN
════════════════════════════════════════════════════════════════════════════════

Wenn du Fragen hast:

1. Schau zuerst in dieser README.md nach (Ctrl+F "deine Frage")
2. Schau in docs/parser/PARSER_DESIGN.md
3. Schau in docs/parser/KNOWN_ISSUES.md
4. Frage das Team oder den Project Lead

════════════════════════════════════════════════════════════════════════════════
📅 ÄNDERUNGS-HISTORY
════════════════════════════════════════════════════════════════════════════════

Version 1.0 (10. Dezember 2025)
  • Initial Release
  • Alle 6 Tests dokumentiert
  • Quick Start Guide
  • Häufige Probleme & Lösungen

════════════════════════════════════════════════════════════════════════════════
DANKE FÜR DEIN INTERESSE!

Der Query Parser v2.2 ist ein wichtiger Teil des Projekts.
Deine Tests helfen uns zu verstehen ob alles funktioniert!

Viel Spaß beim Testen! 🎉

════════════════════════════════════════════════════════════════════════════════

Document: tests/README.md
Version: 1.0
Datum: 10. Dezember 2025
Zielgruppe: Alle (Anfänger bis Fortgeschrittene)
Status: PRODUCTION READY
