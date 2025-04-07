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
Diese Datei validiert die Ethikregeln und stellt sicher,
dass alle Eingaben und Vorschläge den ethischen Standards von FIONA entsprechen.
Sie überprüft die Korrektheit und Relevanz der Ethikdaten,
bevor sie in die Hauptlogik integriert werden.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import json
import hashlib
import logging
import argparse
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='[FIONA][Validator] %(message)s')

CORE_FILE = Path(__file__).parent / "ethics_core.json"
HASH_FILE = Path(__file__).parent / "ethics_core.hash"

def calculate_hash(file_path):
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
            logging.debug(f"File content: {file_data[:100]}...")  # Zeigt die ersten 100 Bytes an (optional)
        return hashlib.sha256(file_data).hexdigest()
    except Exception as e:
        logging.error(f"Failed to read or hash the file: {e}")
        return None

def validate_ethics_core():
    if not CORE_FILE.exists() or not HASH_FILE.exists():
        return False, "Missing core file or hash file."

    actual_hash = calculate_hash(CORE_FILE)
    with open(HASH_FILE, "r") as f:
        expected_hash = f.read().strip()

    if actual_hash != expected_hash:
        return False, "Hash mismatch. Ethics core may have been tampered with."

    return True, "Ethics core is valid."

def load_ethics_core():
    with open(CORE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def show_rules(data):
    rules = data.get("rules", [])
    if not rules:
        logging.warning("No rules found in ethics_core.json")
    for rule in rules:
        rule_id = rule.get("id", "<no id>")
        description = rule.get("description", "<no description>")
        logging.info(f"- [{rule_id}] {description}")

def recalculate_hash():
    try:
        # Lese die Datei und berechne den Hash
        new_hash = calculate_hash(CORE_FILE)
        if new_hash:
            with open(HASH_FILE, "w") as f:
                f.write(new_hash)
            logging.info("Hash file updated.")
        else:
            logging.error("Failed to compute the new hash.")
    except Exception as e:
        logging.error(f"Error recalculating the hash: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate the ethics core integrity.")
    parser.add_argument("--show-rules", action="store_true", help="Print all loaded ethics rules")
    parser.add_argument("--recalculate-hash", action="store_true", help="Recalculate and update the hash file")
    args = parser.parse_args()

    valid, message = validate_ethics_core()
    logging.info(message)

    if valid:
        data = load_ethics_core()
        if args.show_rules:
            show_rules(data)
        if args.recalculate_hash:
            recalculate_hash()
    elif args.recalculate_hash:
        recalculate_hash()
