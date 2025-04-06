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
Diese Datei verwaltet den Überprüfungsmodus von FIONA.
Sie stellt eine Benutzeroberfläche bereit,
um Ethikvorschläge und unbestätigte Fragen zu überprüfen und zu validieren.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

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
