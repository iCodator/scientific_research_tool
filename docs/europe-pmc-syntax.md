# ═══════════════════════════════════════════════════════════════════════════
# EUROPE PMC SEARCH SYNTAX - REGELWERK
# ═══════════════════════════════════════════════════════════════════════════
#
# Quelle: https://europepmc.org/searchsyntax
# Stand: 09.12.2025
#
# Dieses Dokument definiert die korrekte Syntax für Europe PMC Queries
# für die Verwendung im Scientific Research Tool.
#
# ═══════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════
# 1. DIRECT SEARCH (Direkte Suche ohne Feldangaben)
# ═══════════════════════════════════════════════════════════════════════════

## 1.1 EINFACHE SUCHBEGRIFFE
## ═════════════════════════

# REGEL:
# Einzelne Wörter werden in allen Feldern gesucht (Titel, Abstract, Author, etc.)

# BEISPIELE:
malaria
diabetes
cancer

# WICHTIG:
# - Groß-/Kleinschreibung wird IGNORIERT (case-insensitive)
# - Sonderzeichen können die Suche beeinflussen


## 1.2 PHRASENSUCHE (Exakte Wortfolge)
## ═══════════════════════════════════

# REGEL:
# Nutze DOPPELTE Anführungszeichen " " für exakte Phrasen
# NICHT einfache Anführungszeichen ' ' !

# RICHTIG:
"Coenzym Q10"
"systematic review"
"CRISPR Cas9"
"breast cancer"

# FALSCH:
'Coenzym Q10'        # ← Einfache Anführungszeichen funktionieren NICHT!
'systematic review'  # ← Einfache Anführungszeichen funktionieren NICHT!


## 1.3 BOOLEAN-OPERATOREN
## ═══════════════════════

# REGEL:
# Boolean-Operatoren müssen GROSSGESCHRIEBEN sein: AND, OR, NOT
# (Kleinschreibung "and", "or", "not" wird als normaler Suchbegriff behandelt!)

# AND - beide Begriffe müssen vorkommen
diabetes AND exercise
"Coenzym Q10" AND mitochondria

# OR - mindestens einer der Begriffe muss vorkommen
cancer OR tumor
diabetes OR "glucose intolerance"

# NOT - Begriff darf NICHT vorkommen
cancer NOT mouse
diabetes NOT animal

# WICHTIG:
# - Operatoren MÜSSEN großgeschrieben sein!
# - Implizites AND: Wenn kein Operator → automatisch AND
#   Beispiel: diabetes exercise  =  diabetes AND exercise


## 1.4 KLAMMERN FÜR KOMPLEXE QUERIES
## ══════════════════════════════════

# REGEL:
# Nutze runde Klammern ( ) für Gruppierung und Logik-Priorisierung

# BEISPIELE:
(cancer OR tumor) AND therapy
(diabetes OR "metabolic syndrome") AND (exercise OR "physical activity")
"Coenzym Q10" AND (mitochondria OR energy)

# WICHTIG:
# - Klammern müssen balanciert sein: gleiche Anzahl ( und )
# - Verschachtelte Klammern sind erlaubt


## 1.5 WILDCARD-SUCHE
## ═══════════════════

# REGEL:
# Nutze * für beliebig viele Zeichen
# Nutze ? für genau EIN Zeichen

# STERN (*) - beliebig viele Zeichen
carcino*          # findet: carcinoma, carcinogenic, carcinogenesis
diabet*           # findet: diabetes, diabetic, diabetologist

# FRAGEZEICHEN (?) - genau ein Zeichen
wom?n             # findet: woman, women
colo?r            # findet: color, colour

# WICHTIG:
# - Wildcards NICHT am Anfang eines Wortes: *cancer funktioniert NICHT
# - Minimum 3 Zeichen vor Wildcard: ca* funktioniert NICHT, car* funktioniert


## 1.6 PROXIMITY-SUCHE (Wörter in der Nähe)
## ═════════════════════════════════════════

# REGEL:
# Nutze ~N um Wörter zu finden, die max. N Wörter auseinander liegen

# SYNTAX:
"Begriff1 Begriff2"~N

# BEISPIELE:
"coenzyme ubiquinone"~5      # max. 5 Wörter zwischen coenzyme und ubiquinone
"diabetes exercise"~10       # max. 10 Wörter zwischen diabetes und exercise

# WICHTIG:
# - N ist die maximale Distanz
# - Reihenfolge der Wörter ist egal


# ═══════════════════════════════════════════════════════════════════════════
# 2. FIELD SEARCH (Feldspezifische Suche)
# ═══════════════════════════════════════════════════════════════════════════

# REGEL:
# Feldsuchen haben das Format:  FELDNAME:Wert
# oder bei Phrasen:             FELDNAME:"Phrase mit Wörtern"

# WICHTIG:
# - Feldnamen sind CASE-SENSITIVE (Groß-/Kleinschreibung beachten!)
# - KEIN Leerzeichen zwischen Feldname und Doppelpunkt!
# - Nach Doppelpunkt: Wert oder "Phrase"


## 2.1 TITLE (Titel-Suche)
## ════════════════════════

# BESCHREIBUNG:
# Sucht nur im Titel des Artikels

# SYNTAX:
TITLE:Begriff
TITLE:"Phrase"

# BEISPIELE:
TITLE:cancer
TITLE:diabetes
TITLE:"systematic review"
TITLE:"Coenzym Q10"

# KOMBINIERT:
TITLE:"breast cancer" AND YEAR:2020


## 2.2 ABSTRACT (Abstract-Suche)
## ══════════════════════════════

# BESCHREIBUNG:
# Sucht nur im Abstract des Artikels

# SYNTAX:
ABSTRACT:Begriff
ABSTRACT:"Phrase"

# BEISPIELE:
ABSTRACT:mitochondria
ABSTRACT:"oxidative stress"
ABSTRACT:"Coenzym Q10"


## 2.3 AUTH (Autoren-Suche)
## ═════════════════════════

# BESCHREIBUNG:
# Sucht nach Autor-Namen

# SYNTAX:
AUTH:Nachname
AUTH:"Nachname Initials"

# BEISPIELE:
AUTH:Smith
AUTH:"Smith J"
AUTH:"Müller M"

# WICHTIG:
# - Format: "Nachname Initials" (mit Leerzeichen!)
# - Umlaute werden unterstützt


## 2.4 JOURNAL (Journal-Suche)
## ════════════════════════════

# BESCHREIBUNG:
# Sucht nach Journal-Namen

# SYNTAX:
JOURNAL:Name
JOURNAL:"Journal Name"

# BEISPIELE:
JOURNAL:Nature
JOURNAL:"The Lancet"
JOURNAL:"New England Journal of Medicine"


## 2.5 PUB_YEAR (Publikationsjahr)
## ════════════════════════════════

# BESCHREIBUNG:
# Filtert nach Publikationsjahr oder -bereich

# SYNTAX (einzelnes Jahr):
PUB_YEAR:YYYY

# SYNTAX (Bereich):
PUB_YEAR:(YYYY-YYYY)

# BEISPIELE:
PUB_YEAR:2020                # Nur 2020
PUB_YEAR:2025                # Nur 2025
PUB_YEAR:(2015-2025)         # Bereich 2015 bis 2025 (inklusiv)
PUB_YEAR:(2020-2023)         # Bereich 2020 bis 2023

# WICHTIG:
# - Bereich in RUNDEN Klammern: (YYYY-YYYY)
# - Bindestrich (-) zwischen den Jahren, NICHT "TO"!
# - KEINE eckigen Klammern!

# KOMBINIERT:
"Coenzym Q10" AND PUB_YEAR:(2015-2025)
diabetes AND PUB_YEAR:2020


## 2.6 FIRST_PDATE (Erstes Publikationsdatum)
## ═══════════════════════════════════════════

# BESCHREIBUNG:
# Filtert nach erstem Publikationsdatum (wenn Online-Vorab-Publikation)

# SYNTAX (einzelnes Datum):
FIRST_PDATE:YYYY-MM-DD

# SYNTAX (Bereich):
FIRST_PDATE:[YYYY-MM-DD TO YYYY-MM-DD]

# BEISPIELE:
FIRST_PDATE:2020-01-15
FIRST_PDATE:[2020-01-01 TO 2020-12-31]

# WICHTIG:
# - Format: YYYY-MM-DD (ISO 8601)
# - Bereich in ECKIGEN Klammern: [DATUM TO DATUM]
# - "TO" ist hier GROSSGESCHRIEBEN


## 2.7 SRC (Source/Datenbank)
## ═══════════════════════════

# BESCHREIBUNG:
# Filtert nach Datenbank-Quelle

# SYNTAX:
SRC:Quelle

# MÖGLICHE WERTE:
SRC:MED        # PubMed/MEDLINE
SRC:PMC        # PubMed Central
SRC:PPR        # Preprints
SRC:AGR        # Agris
SRC:CBA        # Chinese Biological Abstracts
SRC:CTX        # CiteXplore
SRC:ETH        # EthOS (UK Theses)
SRC:HIR        # NHS Evidence
SRC:PAT        # Patents

# BEISPIELE:
cancer AND SRC:MED
"systematic review" AND SRC:PMC

# WICHTIG:
# - Quellenkürzel sind CASE-SENSITIVE
# - MED = hauptsächlich PubMed-Einträge


## 2.8 ISSN / ESSN (Journal-Identifikatoren)
## ══════════════════════════════════════════

# BESCHREIBUNG:
# Filtert nach ISSN (Print) oder ESSN (Electronic)

# SYNTAX:
ISSN:XXXX-XXXX
ESSN:XXXX-XXXX

# BEISPIELE:
ISSN:0028-0836      # Nature (Print)
ESSN:1476-4687      # Nature (Online)


## 2.9 GRANT_AGENCY (Förderorganisation)
## ══════════════════════════════════════

# BESCHREIBUNG:
# Sucht nach Artikeln, die von bestimmter Organisation gefördert wurden

# SYNTAX:
GRANT_AGENCY:"Organisation"

# BEISPIELE:
GRANT_AGENCY:"NIH"
GRANT_AGENCY:"Wellcome Trust"
GRANT_AGENCY:"DFG"


## 2.10 GRANT_ID (Förderungsnummer)
## ═════════════════════════════════

# BESCHREIBUNG:
# Sucht nach spezifischer Grant-Nummer

# SYNTAX:
GRANT_ID:Nummer

# BEISPIELE:
GRANT_ID:R01CA123456
GRANT_ID:203128/Z/16/Z


## 2.11 EXT_ID (Externe IDs)
## ═════════════════════════

# BESCHREIBUNG:
# Sucht nach externen Identifikatoren (DOI, PMID, etc.)

# SYNTAX:
EXT_ID:ID

# BEISPIELE:
EXT_ID:10.1038/nature12345    # DOI
EXT_ID:12345678               # PMID


## 2.12 OPEN_ACCESS (Open Access Filter)
## ══════════════════════════════════════

# BESCHREIBUNG:
# Filtert nur Open-Access-Artikel

# SYNTAX:
OPEN_ACCESS:Y

# BEISPIELE:
cancer AND OPEN_ACCESS:Y
"systematic review" AND OPEN_ACCESS:Y AND PUB_YEAR:(2020-2025)

# WICHTIG:
# - Wert ist immer "Y" (für Yes)


## 2.13 HAS_ABSTRACT (Abstract vorhanden)
## ═══════════════════════════════════════

# BESCHREIBUNG:
# Filtert nur Artikel mit Abstract

# SYNTAX:
HAS_ABSTRACT:Y

# BEISPIELE:
diabetes AND HAS_ABSTRACT:Y


## 2.14 HAS_PDF (PDF verfügbar)
## ═════════════════════════════

# BESCHREIBUNG:
# Filtert nur Artikel mit verfügbarem PDF

# SYNTAX:
HAS_PDF:Y

# BEISPIELE:
cancer AND HAS_PDF:Y


## 2.15 IN_EPMC (In Europe PMC Volltext)
## ══════════════════════════════════════

# BESCHREIBUNG:
# Filtert nur Artikel mit Volltext in Europe PMC

# SYNTAX:
IN_EPMC:Y

# BEISPIELE:
diabetes AND IN_EPMC:Y


# ═══════════════════════════════════════════════════════════════════════════
# 3. KOMBINIERTE BEISPIELE (Best Practices)
# ═══════════════════════════════════════════════════════════════════════════

## BEISPIEL 1: Einfache Phrasensuche mit Zeitfilter
## ═════════════════════════════════════════════════
"Coenzym Q10" AND PUB_YEAR:(2015-2025)

# Erklärung:
# - "Coenzym Q10" in doppelten Anführungszeichen (Phrase!)
# - PUB_YEAR:(2015-2025) mit Bindestrich (nicht TO!)


## BEISPIEL 2: Komplexe Boolean-Suche
## ═══════════════════════════════════
(diabetes OR "metabolic syndrome") AND (exercise OR "physical activity") AND PUB_YEAR:(2020-2025)

# Erklärung:
# - Klammern gruppieren OR-Ausdrücke
# - Phrasen in doppelten Anführungszeichen
# - AND verbindet die Gruppen


## BEISPIEL 3: Titel- und Abstract-Suche kombiniert
## ═════════════════════════════════════════════════
TITLE:"systematic review" AND ABSTRACT:"Coenzym Q10"

# Erklärung:
# - TITLE: sucht nur im Titel
# - ABSTRACT: sucht nur im Abstract
# - AND verbindet beide Bedingungen


## BEISPIEL 4: Autor und Journal
## ══════════════════════════════
AUTH:"Smith J" AND JOURNAL:Nature AND PUB_YEAR:(2020-2023)

# Erklärung:
# - AUTH: Autor-Name in Anführungszeichen
# - JOURNAL: Journal-Name
# - PUB_YEAR: Zeitbereich


## BEISPIEL 5: Open Access Filter
## ═══════════════════════════════
"breast cancer" AND OPEN_ACCESS:Y AND PUB_YEAR:(2020-2025) AND HAS_PDF:Y

# Erklärung:
# - Nur Open-Access-Artikel
# - Mit PDF verfügbar
# - Zeitbereich 2020-2025


## BEISPIEL 6: Quelle und Zeitfilter
## ══════════════════════════════════
cancer AND SRC:MED AND PUB_YEAR:(2023-2025)

# Erklärung:
# - Nur aus MEDLINE/PubMed
# - Nur aktuelle Jahre


## BEISPIEL 7: Wildcard und Proximity
## ═══════════════════════════════════
diabet* AND "exercise training"~5

# Erklärung:
# - diabet* findet: diabetes, diabetic, diabetologist
# - ~5 bedeutet: max. 5 Wörter zwischen "exercise" und "training"


# ═══════════════════════════════════════════════════════════════════════════
# 4. HÄUFIGE FEHLER UND LÖSUNGEN
# ═══════════════════════════════════════════════════════════════════════════

## FEHLER 1: Einfache Anführungszeichen
## ═════════════════════════════════════
# FALSCH:
'Coenzym Q10' AND PUB_YEAR:(2015-2025)

# RICHTIG:
"Coenzym Q10" AND PUB_YEAR:(2015-2025)


## FEHLER 2: Falsches Datumsformat
## ════════════════════════════════
# FALSCH:
PUB_YEAR:(2015 TO 2025)       # "TO" funktioniert nicht!
PUB_YEAR:[2015-2025]          # Eckige Klammern funktionieren nicht!
PUB_YEAR:2015:2025[pdat]      # PubMed-Format funktioniert nicht!

# RICHTIG:
PUB_YEAR:(2015-2025)          # Runde Klammern, Bindestrich!


## FEHLER 3: Kleingeschriebene Boolean-Operatoren
## ═══════════════════════════════════════════════
# FALSCH:
diabetes and exercise         # "and" wird als Wort gesucht!

# RICHTIG:
diabetes AND exercise         # "AND" ist Boolean-Operator


## FEHLER 4: Leerzeichen in Feldnamen
## ═══════════════════════════════════
# FALSCH:
PUB_YEAR : (2015-2025)        # Leerzeichen vor/nach Doppelpunkt!
PUB_ YEAR:(2015-2025)         # Leerzeichen im Feldnamen!

# RICHTIG:
PUB_YEAR:(2015-2025)          # Kein Leerzeichen!


## FEHLER 5: Unbalancierte Klammern
## ═════════════════════════════════
# FALSCH:
(diabetes OR exercise AND PUB_YEAR:(2020-2025)    # Eine Klammer fehlt!

# RICHTIG:
(diabetes OR exercise) AND PUB_YEAR:(2020-2025)   # Alle Klammern geschlossen


# ═══════════════════════════════════════════════════════════════════════════
# 5. CHEAT SHEET (Schnellreferenz)
# ═══════════════════════════════════════════════════════════════════════════

# OPERATOREN:
AND                    # Beide Begriffe müssen vorkommen
OR                     # Mindestens ein Begriff muss vorkommen
NOT                    # Begriff darf nicht vorkommen

# PHRASENSUCHE:
"exakte Phrase"        # Doppelte Anführungszeichen!

# WILDCARDS:
*                      # Beliebig viele Zeichen
?                      # Genau ein Zeichen

# PROXIMITY:
"Begriff1 Begriff2"~N  # Max. N Wörter zwischen Begriffen

# WICHTIGSTE FELDER:
TITLE:"..."            # Titel-Suche
ABSTRACT:"..."         # Abstract-Suche
AUTH:"Nachname I"      # Autoren-Suche
JOURNAL:"..."          # Journal-Suche
PUB_YEAR:(YYYY-YYYY)   # Jahr oder Zeitbereich (Bindestrich!)
SRC:MED                # Quelle (z.B. MED, PMC)
OPEN_ACCESS:Y          # Nur Open Access
HAS_PDF:Y              # Nur mit PDF

# ZEITBEREICH (WICHTIG!):
PUB_YEAR:2020          # Einzelnes Jahr
PUB_YEAR:(2015-2025)   # Bereich mit Bindestrich (-)
                       # NICHT "TO"!
                       # NICHT [eckige Klammern]!
                       # NICHT :Doppelpunkt:


# ═══════════════════════════════════════════════════════════════════════════
# END OF DOCUMENT
# ═══════════════════════════════════════════════════════════════════════════
