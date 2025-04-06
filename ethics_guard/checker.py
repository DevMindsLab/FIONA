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
prüft die ethische Korrektheit der Entscheidungen von FIONA.
Es stellt sicher, dass jede Antwort den festgelegten ethischen Standards entspricht,
bevor sie dem Benutzer präsentiert wird.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import logging

logging.basicConfig(level=logging.INFO, format='[FIONA][EthicsGuard] %(message)s')

banned_keywords = [
    "kill", "hack", "manipulate", "lie", "surveil", "torture",
    "exploit", "violence", "suicide", "murder", "destroy",
    "racist", "terror", "attack", "bypass", "cheat", "weapon",
    "töten", "lügen", "überwachen", "ausnutzen", "missbrauchen"
]

def is_ethically_safe(text: str) -> bool:
    violations = find_ethics_violations(text)
    if violations:
        logging.warning(f"Unsafe output detected. Violations: {violations}")
    return len(violations) == 0

def find_ethics_violations(text: str) -> list:
    lower_text = text.lower()
    return [kw for kw in banned_keywords if kw in lower_text]

# Debug
if __name__ == "__main__":
    test_text = "This message contains intent to kill and manipulate."
    safe = is_ethically_safe(test_text)
    print(f"Is safe? {safe}")