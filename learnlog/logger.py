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
verwaltet das Protokollieren von Lernereignissen und Benutzereingaben.
Es speichert relevante Informationen für die spätere Analyse und Verbesserung des Lernprozesses von FIONA.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[FIONA][Logger] %(message)s')

LOG_PATH = Path(__file__).resolve().parent / "learnlog.jsonl"

def log_question(question: str, source: str = "unknown"):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "source": source,
        "status": "unreviewed"
    }

    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        logging.info(f"Logged question from {source}: {question}")
    except Exception as e:
        logging.error(f"Failed to log question: {e}")