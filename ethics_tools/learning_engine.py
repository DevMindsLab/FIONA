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
