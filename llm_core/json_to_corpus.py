"""
======================================
FIONA - Projektname

Autor: Rene Baumgarten (DevMindsLab)
Datum: 21.03.2025
Version: 0.4

Beschreibung:
---------------
Diese Python-Datei ist Teil des **FIONA**-Projekts,
einer ethisch ausgerichteten,
Open-Source-basierten Künstlichen Intelligenz (KAI). Das Projekt strebt an,
verantwortungsbewusste, nachvollziehbare und kontrollierte Entscheidungen in ethischen Dilemmata zu treffen.
Der Code in dieser Datei ist Teil des Backends, das für [Beschreibung der Funktionalität der Datei] zuständig ist.

Funktions Beschreibung:
---------------
Diese Datei konvertiert JSON-Daten in ein Textkorpus,
das für das Training des Sprachmodells verwendet werden kann.
Sie sorgt für die Umwandlung und Bereitstellung von Daten im richtigen Format.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import json

# Eingabepfad zur JSON-Datei
input_file = "llm_core/training_data/fiona_facts.json"
output_file = "llm_core/training_data/corpus.txt"

# Liest die JSON-Datei
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Überprüfen, ob der Schlüssel 'data' existiert
if "data" not in data:
    print("Fehler: Die JSON-Daten enthalten keinen 'data'-Schlüssel.")
    exit(1)

# Öffnet die Ausgabe-Datei im Schreibmodus
with open(output_file, "w", encoding="utf-8") as corpus_file:
    # Verarbeite jedes Element in der 'data'-Liste
    for item in data["data"]:
        # Extrahieren der verschiedenen Felder
        text = item.get("text", "")
        category = item.get("category", "")
        question = item.get("question", "")
        answer = item.get("answer", "")

        # Überprüfen, ob alle notwendigen Felder vorhanden sind
        if text and question and answer:
            # Formatierte Zeile im Format "Frage -> Antwort | Kategorie: {category}, Text: {text}"
            corpus_file.write(f"{category} | {text} | Frage: {question} -> Antwort: {answer}\n")

print("✅ JSON wurde erfolgreich in das Corpus umgewandelt.")
