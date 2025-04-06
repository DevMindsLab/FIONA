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
ist für die kontinuierliche Verbesserung der Ethikprüfung verantwortlich.
Durch maschinelles Lernen optimiert es die Entscheidungskompetenz von FIONA und hilft,
die Ethikregeln dynamisch anzupassen.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import json
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='[FIONA][LearningEngine] %(message)s')

RULE_FILE = os.path.join(os.path.dirname(__file__), "../core_ethics/core_ethics.json")
SUGGESTION_LOG = os.path.join(os.path.dirname(__file__), "suggested_rules.json")

def suggest_rule(input_text, matched_keywords, priority=0.6, save=True):
    rule_id = f"suggested_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{abs(hash(input_text)) % 1000}"
    description = f"Suggested rule based on unknown input: '{input_text}'"

    new_rule = {
        "id": rule_id,
        "description": description,
        "priority": priority,
        "condition_keywords": matched_keywords,
        "action": "reject"
    }

    if not save:
        logging.info(f"Dry run: would suggest rule {rule_id} for input: '{input_text}'")
        return new_rule

    # Regel in Review-Datei speichern
    if os.path.exists(SUGGESTION_LOG):
        with open(SUGGESTION_LOG, "r", encoding="utf-8") as f:
            suggestions = json.load(f)
    else:
        suggestions = []

    # Duplikatprüfung (einfache Keyword-Check)
    for rule in suggestions:
        if set(rule.get("condition_keywords", [])) == set(matched_keywords):
            logging.warning(f"Duplicate suggestion detected. Skipping rule for: {matched_keywords}")
            return rule

    suggestions.append(new_rule)

    with open(SUGGESTION_LOG, "w", encoding="utf-8") as f:
        json.dump(suggestions, f, indent=2)

    logging.info(f"Suggested new rule saved: {rule_id}")
    return new_rule
