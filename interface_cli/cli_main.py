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
stellt die Hauptlogik für die Kommandozeilenschnittstelle von FIONA bereit.
Sie ermöglicht es Entwicklern, FIONA über die Kommandozeile zu steuern und zu testen.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import sys
import argparse
import logging
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from core_ethics.ethics_link import check_ethics_validity
from core_interface.context_memory import ContextMemory
from core_decision.decision_engine import DecisionEngine
from core_expression.expression_engine import generate_response
from learnlog.logger import log_question

logging.basicConfig(level=logging.INFO, format='[FIONA][CLI] %(message)s')

def print_intro():
    print("\n🌸 Welcome to FIONA – Friendly Intelligence Of Neutral Assistance")
    print("Type 'exit' to quit.\n")

def run_loop(engine: DecisionEngine, memory: ContextMemory, debug: bool = False):
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ('exit', 'quit'):
                print("👋 Goodbye.")
                break

            result = engine.decide(user_input)
            response = generate_response(result)
            print(f"FIONA: {response}")

            if result["decision"] == "reject":
                log_question(user_input)

            if debug:
                print("--- DEBUG INFO ---")
                print(f"Intents: {result['parsed'].get('intents', [])}")
                print(f"Ethics: {result['ethics']}")
                print(f"Decision: {result['decision']}")
                if result.get("suggested_rule"):
                    print(f"Suggested Rule: {result['suggested_rule']}")
                print("-------------------")

            last = memory.get_last_ethics()
            if last and last["input"] != user_input:
                print(f"🧠 Last context: '{last['input']}' → {last['decision']}")

        except Exception as e:
            logging.error(f"Exception occurred while processing input: {e}")


def main():
    parser = argparse.ArgumentParser(description="Run FIONA in CLI mode.")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    print("\n🔍 Validating FIONA Ethics Core...")
    valid, message = check_ethics_validity()
    if not valid:
        print(f"❌ Ethics core validation failed: {message}")
        return

    print("✅ Ethics core is valid and active.")
    print_intro()

    engine = DecisionEngine()
    memory = ContextMemory()

    run_loop(engine, memory, debug=args.debug)

if __name__ == "__main__":
    main()