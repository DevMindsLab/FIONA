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