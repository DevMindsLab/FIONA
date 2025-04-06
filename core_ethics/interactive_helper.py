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
enthält Hilfsfunktionen, die den interaktiven Ethiktestprozess unterstützen.
Es sorgt dafür, dass Benutzer effektiv durch ethische Prüfungen geführt werden und dass Rückmeldungen verständlich und klar sind.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import re
import logging

logging.basicConfig(level=logging.INFO, format='[FIONA][Helper] %(message)s')

def explain_ethics(reasoning: dict) -> str:
    reason = reasoning.get("reason", "An unknown ethical principle was triggered.")
    decision = reasoning.get("decision", "neutral")

    if decision == "reject":
        return f"I had to reject your request because: {reason}"
    elif decision == "allow":
        return f"Your request aligns with my ethics: {reason}"
    else:
        return f"I wasn't sure how to judge this request: {reason}"

def suggest_rephrase(user_input: str, reasoning: dict) -> str:
    replacements = {
        "kill": "stop",
        "hurt": "avoid",
        "force": "convince",
        "deceive": "explain clearly"
    }

    suggestion = user_input
    modified = False
    changes = []

    for bad, good in replacements.items():
        pattern = re.compile(rf"\\b{re.escape(bad)}\\b", flags=re.IGNORECASE)
        if pattern.search(suggestion):
            suggestion = pattern.sub(good, suggestion)
            modified = True
            changes.append((bad, good))

    if modified:
        for bad, good in changes:
            logging.info(f"Replaced '{bad}' with '{good}' in user input.")
        return f"Maybe try asking: '{suggestion}'"
    else:
        return "Try to rephrase your request in a more neutral or peaceful way."
