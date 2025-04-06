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
analysiert und strukturiert Benutzereingaben.
Es sorgt dafür, dass die Anfragen korrekt in ein Format übersetzt werden,
das von der Entscheidungslogik verarbeitet werden kann.

Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import re
import logging

logging.basicConfig(level=logging.INFO, format='[FIONA][Parser] %(message)s')

INTENT_PATTERNS = {
    "question": re.compile(r"\b(who|what|when|where|why|how|is|are|can|do|does)\b", re.IGNORECASE),
    "command": re.compile(r"\b(tell|show|explain|give|say|do|stop|start)\b", re.IGNORECASE),
    "greeting": re.compile(r"\b(hello|hi|hey|greetings)\b", re.IGNORECASE),
    "harm": re.compile(r"\b(kill|hurt|attack|destroy|harm|stab)\b", re.IGNORECASE),
    "ethics": re.compile(r"\b(right|wrong|moral|ethic|allowed|permitted|legal)\b", re.IGNORECASE),
    "self_reference": re.compile(r"\b(i|me|my|myself)\b", re.IGNORECASE),
}

def parse_input(text: str, verbose: bool = False) -> dict:
    tokens = text.lower().split()
    detected_intents = []
    matches = {}

    for label, pattern in INTENT_PATTERNS.items():
        if pattern.search(text):
            detected_intents.append(label)
            if verbose:
                found = pattern.findall(text)
                matches[label] = found
                logging.info(f"Intent '{label}' matched keywords: {found}")

    result = {
        "raw": text,
        "tokens": tokens,
        "intents": detected_intents
    }

    if verbose:
        result["matches"] = matches

    return result

# Debug
if __name__ == "__main__":
    example = "Can I hurt someone if it’s for a good reason?"
    result = parse_input(example, verbose=True)
    print("\n🧠 PARSE RESULT:")
    print(result)
