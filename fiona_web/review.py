import json
from pathlib import Path

# Speicherort der Learnlog-Datei
LOG_PATH = Path(__file__).resolve().parent / "learnlog" / "learnlog.jsonl"

def load_unreviewed():
    """
    Gibt alle Learnlog-Einträge mit Status 'unreviewed' zurück.
    """
    if not LOG_PATH.exists():
        return []

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if '"status": "unreviewed"' in line]

def update_question_status(timestamp, new_status):
    """
    Aktualisiert den Status (approved/rejected/ignored) eines Learnlog-Eintrags anhand seines Timestamps.
    """
    if not LOG_PATH.exists():
        return

    updated_logs = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            if entry.get("timestamp") == timestamp:
                entry["status"] = new_status
            updated_logs.append(entry)

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for entry in updated_logs:
            f.write(json.dumps(entry) + "\n")
