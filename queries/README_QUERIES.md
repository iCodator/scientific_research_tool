# 📂 Abfrage-Bibliothek (Queries)

In diesem Ordner kannst du deine komplexen Suchanfragen als Textdateien speichern. 
Das hat den Vorteil, dass du komplizierte Logik (viele Klammern, OR/AND Verknüpfungen) nicht jedes Mal neu in die Kommandozeile tippen musst.

## 📝 Wie erstelle ich eine Query-Datei?
Erstelle einfach eine `.txt` Datei (z.B. `meine_suche.txt`) und schreibe deine Suchanfrage hinein.

**Regeln:**
- Keine Anführungszeichen um die gesamte Query nötig.
- Zeilenumbrüche sind erlaubt (werden vom Tool automatisch zu Leerzeichen umgewandelt).
- Kommentare sind (noch) nicht unterstützt, nur die reine Query.

### Beispiel-Inhalt (`queries/cancer_immunotherapy.txt`):
```text
((cancer OR tumor OR neoplasm) 
 AND 
 (immunotherapy OR "immune checkpoint inhibitor")) 
 AND 
 (2023:2025)
```

## 🚀 Wie nutze ich die Dateien?
Nutze das Flag `--query-file` (oder `-qf` falls implementiert) beim Starten des Tools:

```bash
# Aus dem Hauptverzeichnis des Projekts:
python main.py --query-file queries/cancer_immunotherapy.txt --source pubmed
```

## 🗂 Empfohlene Struktur
Du kannst Unterordner erstellen, um deine Suchen zu sortieren:

- `queries/medical/`
- `queries/biology/`
- `queries/temp/`
