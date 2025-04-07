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
ist verantwortlich für die Erzeugung und Analyse von Ausdrücken innerhalb des FIONA-Systems.
Sie verarbeitet Textausgaben und stellt sicher, dass die Antworten ethisch und sprachlich korrekt sind.

Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import random
import logging

logging.basicConfig(level=logging.INFO, format='[FIONA][ExpressionEngine] %(message)s')

TEMPLATES = {
    "accept": [
        "✅ I understand. That seems acceptable to me.",
        "🟢 This appears to align with ethical standards.",
        "Yes, I see no ethical conflict here."
    ],
    "reject": [
        "🚫 I'm sorry, I cannot support that action.",
        "🔴 That violates one or more ethical principles.",
        "I must reject that, as it could cause harm or conflict."
    ],
    "neutral": [
        "🤔 I don't have enough information to judge this ethically.",
        "This requires further clarification or rule evaluation.",
        "Neutral: no matching rule or intent was found."
    ],
    "ask": [
        "💬 That's a valid question. Let's think ethically about it.",
        "Interesting inquiry. I'm analyzing it ethically.",
        "Let me help you reflect on this question ethically."
    ],
    "learn": [
        "📚 I've noted this for future ethical analysis.",
        "🧠 I'm learning from this input.",
        "No rule matched. Suggestion added for review."
    ]
}

def generate_batch(results: list) -> list:
    responses = []
    for result in results:
        decision = result["decision"]
        ethics = result.get("ethics", {})
        reason = ethics.get("reason", "No ethical reason given.")
        rule_info = ethics.get("matched_rules", [])
        parsed = result.get("parsed", {})

        base = random.choice(TEMPLATES.get(decision, ["(No response template found.)"]))
        logging.info(f"Generated template for decision '{decision}': {base}")

        response = f"{base}\n\n🧠 Ethics: {reason}"
        if rule_info:
            response += f"\n📜 Rules involved: {', '.join(rule_info)}"

        if decision == "neutral" and result.get("suggested_rule"):
            response += f"\n📎 New rule suggested: {result['suggested_rule']['id']}"

        if "self_reference" in parsed.get("intents", []):
            response += "\n👤 I recognize your personal perspective."

        responses.append(response)
    return responses

# Debug
if __name__ == "__main__":
    # Beispiel: Batch von Ergebnissen
    batch_sample = [
        {
            "decision": "reject",
            "ethics": {
                "reason": "This action may lead to harm.",
                "matched_rules": ["avoid_harm"]
            },
            "suggested_rule": None,
            "parsed": {"intents": ["harm", "self_reference"]}
        },
        {
            "decision": "accept",
            "ethics": {
                "reason": "This action is ethically sound.",
                "matched_rules": ["ethical_action"]
            },
            "suggested_rule": None,
            "parsed": {"intents": ["approval"]}
        }
    ]

    print("\n🗣️ EXPRESSION BATCH:")
    responses = generate_batch(batch_sample)
    for response in responses:
        print(response)