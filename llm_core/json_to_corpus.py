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
