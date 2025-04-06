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
bietet einen Notfallmechanismus für die Verarbeitung von Benutzereingaben.
Wenn die primäre Ethikprüfung nicht erfolgreich ist,
übernimmt dieser Mechanismus die Eingabe und gibt eine Antwort,
um die Anwendung stabil zu halten.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

def generate_ethics_template_response(user_input: str, reasoning: dict) -> str:
    decision = reasoning.get("decision", "neutral")
    reason = reasoning.get("reason", "No reason provided.")
    rule_ids = reasoning.get("matched_rules", [])

    if decision == "reject":
        return (
            f"I'm sorry, but I must reject your request. "
            f"It conflicts with my core ethical principle: {reason}"
        )
    elif decision == "allow":
        return (
            f"This request appears to be ethically acceptable. "
            f"Reason: {reason}"
        )
    else:
        return (
            f"I'm uncertain about this request. "
            f"Please clarify your intent. Reason: {reason}"
        )
