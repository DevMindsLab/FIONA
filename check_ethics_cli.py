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
ist ein Kommandozeilen-Tool, das es ermöglicht, die ethischen Prüfungen von FIONA direkt aus der Konsole heraus durchzuführen.
Es überprüft Benutzereingaben auf Übereinstimmung mit den festgelegten Ethikregeln
und gibt eine detaillierte Rückmeldung zu den ethischen Entscheidungen, die das System trifft.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

from core_ethics.ethics_link import check_ethics_validity

def main():
    valid, message = check_ethics_validity()
    if valid:
        print(f"✅ Ethics core is valid: {message}")
    else:
        print(f"❌ Ethics core failed: {message}")

if __name__ == "__main__":
    main()
