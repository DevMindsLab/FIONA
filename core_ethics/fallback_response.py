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
Diese Datei definiert eine Fallback-Antwortlogik, die verwendet wird,
wenn eine ethische Entscheidung aufgrund von fehlenden oder unklaren Eingaben nicht getroffen werden kann.
Sie stellt sicher, dass der Benutzer trotzdem eine Antwort erhält.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import logging
import random

logging.basicConfig(level=logging.INFO, format='[FIONA][Fallback] %(message)s')

actions = {
    "reject": [
        "No. I cannot support this request.",
        "I'm sorry, but this goes against my ethics.",
        "This request must be declined for ethical reasons."
    ],
    "allow": [
        "Yes, that seems fine.",
        "Of course, this aligns with my ethical framework.",
        "Sure, that appears to be ethically acceptable."
    ],
    "neutral": [
        "I'm unsure how to respond.",
        "I cannot confidently evaluate this request.",
        "This situation is unclear from an ethical standpoint."
    ]
}

def generate_fallback_response(user_input: str, reasoning: dict) -> str:
    action = reasoning.get("decision", "neutral")
    reason = reasoning.get("reason", "No reason provided.")

    response_intro = random.choice(actions.get(action, actions["neutral"]))
    response = f"{response_intro} {reason}"

    logging.info(f"Fallback response generated for action '{action}': {response}")
    return response