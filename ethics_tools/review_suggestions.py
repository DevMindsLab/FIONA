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
Diese Datei ermöglicht die Überprüfung und Bearbeitung von Ethikvorschlägen.
Sie hilft, neue Ethikregeln zu validieren und zu integrieren,
um die Ethikprüfung von FIONA stetig zu verbessern.

Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import json
import os
import logging
from pprint import pprint

logging.basicConfig(level=logging.INFO, format='[FIONA][Review] %(message)s')

CORE_RULES_PATH = os.path.join(os.path.dirname(__file__), "../core_ethics/core_ethics.json")
SUGGESTIONS_PATH = os.path.join(os.path.dirname(__file__), "suggested_rules.json")

REQUIRED_FIELDS = ["id", "description", "priority", "condition_keywords", "action"]

def load_json(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load JSON from {path}: {e}")
        return []

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to save JSON to {path}: {e}")


def is_valid_rule(rule):
    return all(k in rule for k in REQUIRED_FIELDS)

def review_suggestions():
    suggestions = load_json(SUGGESTIONS_PATH)
    if not suggestions:
        print("✅ No pending rule suggestions.")
        return

    core_rules = load_json(CORE_RULES_PATH)
    print(f"🔍 Found {len(suggestions)} suggestion(s) for review.\n")

    kept = []
    for idx, rule in enumerate(suggestions):
        print(f"🧠 Rule #{idx + 1}")
        pprint(rule)

        if not is_valid_rule(rule):
            logging.warning(f"Invalid rule structure: {rule.get('id', '<no id>')}")
            print("❌ Invalid rule structure. Skipping.\n")
            continue

        print("Options: [y] accept  [n] reject  [s] skip")
        choice = input("→ Your choice: ").lower().strip()

        if choice == "y":
            core_rules.append(rule)
            logging.info(f"Accepted rule: {rule['id']}")
            print("✅ Rule added to core_ethics.json.\n")
        elif choice == "n":
            logging.info(f"Rejected rule: {rule['id']}")
            print("🗑️ Rule rejected.\n")
            continue
        elif choice == "s":
            kept.append(rule)
            logging.info(f"Skipped rule: {rule['id']}")
            print("⏭️ Rule skipped.\n")
        else:
            kept.append(rule)
            logging.warning(f"Unknown input. Skipping rule: {rule['id']}")
            print("❓ Unknown input. Skipping.\n")

    save_json(CORE_RULES_PATH, core_rules)
    save_json(SUGGESTIONS_PATH, kept)

    print("\n📦 Review complete.")
    print(f"✔️ {len(core_rules)} total rules in core.")
    print(f"🕒 {len(kept)} suggestions remaining for later review.")

if __name__ == "__main__":
    review_suggestions()
