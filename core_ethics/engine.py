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
Diese Datei enthält die Hauptlogik für die Ethikprüfung.
Sie analysiert Eingaben und prüft deren Übereinstimmung mit den Ethikrichtlinien von FIONA.
Entscheidungen werden basierend auf diesen Prüfungen getroffen und zur weiteren Verarbeitung zurückgegeben.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import json
import os
import logging
import re
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format='[FIONA][EthicsEngine] %(message)s')

class CoreEthicsEngine:
    def __init__(self, rules_file: Optional[str] = None):
        if rules_file is None:
            rules_file = os.path.join(os.path.dirname(__file__), "core_ethics.json")
        self.rules = self.load_rules(rules_file)
        logging.info(f"Loaded {len(self.rules)} rules from {rules_file}")

    def load_rules(self, path: str) -> List[Dict]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load rules: {e}")
            return []

    def evaluate(self, user_input: str) -> Dict:
        hits = []

        for rule in self.rules:
            matched = False

            # Check condition_keywords
            for keyword in rule.get("condition_keywords", []):
                if keyword.lower() in user_input.lower():
                    matched = True
                    break

            # Optional regex pattern
            if not matched and "pattern" in rule:
                try:
                    if re.search(rule["pattern"], user_input, re.IGNORECASE):
                        matched = True
                except re.error as e:
                    logging.warning(f"Invalid regex in rule {rule.get('id', '?')}: {e}")

            if matched:
                hits.append(rule)

        if not hits:
            return {
                "decision": "neutral",
                "reason": "No matching ethical rule found.",
                "matched_rules": [],
                "conflict_resolution": []
            }

        sorted_hits = sorted(hits, key=lambda r: r.get("priority", 0.5), reverse=True)
        top_rule = sorted_hits[0]

        # Check for same-priority conflicts
        if len(sorted_hits) > 1 and sorted_hits[0].get("priority") == sorted_hits[1].get("priority"):
            logging.warning("Multiple rules with equal priority matched.")

        explanations = [
            f"{r.get('id', '?')} (priority {r.get('priority', 0.5)}) → {r.get('action', 'neutral').upper()}"
            for r in sorted_hits
        ]

        return {
            "decision": top_rule.get("action", "neutral"),
            "reason": top_rule.get("description", "No reason available."),
            "matched_rules": [r.get("id", "?") for r in sorted_hits],
            "conflict_resolution": explanations
        }