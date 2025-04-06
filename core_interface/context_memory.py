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
speichert und verwaltet den Kontext von Benutzerinteraktionen.
Es hilft FIONA, sich an frühere Gespräche zu erinnern und kontextuelle
Zusammenhänge für fundierte Entscheidungen zu nutzen.

Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='[FIONA][ContextMemory] %(message)s')

class ContextMemory:
    def __init__(self, max_entries=100):
        self.history = []
        self.max_entries = max_entries

    def remember(self, user_input: str, decision: str, reason: str):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "input": user_input,
            "decision": decision,
            "reason": reason
        }
        self.history.append(entry)
        if len(self.history) > self.max_entries:
            self.history.pop(0)
        logging.info(f"Remembered input with decision '{decision}': {user_input}")

    def get_last_ethics(self, keyword=None):
        for entry in reversed(self.history):
            if keyword is None or keyword.lower() in entry["input"].lower():
                logging.info(f"Found context match for: {keyword if keyword else 'last'}")
                return entry
        logging.info("No matching context found.")
        return None

    def save(self, filepath: str):
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2)
            logging.info(f"Context memory saved to '{filepath}'")
        except Exception as e:
            logging.error(f"Failed to save context: {e}")

    def load(self, filepath: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                self.history = json.load(f)
            logging.info(f"Context memory loaded from '{filepath}'")
        except Exception as e:
            logging.warning(f"Failed to load context: {e}")