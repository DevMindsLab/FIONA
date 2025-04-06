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

def generate_response(result: dict) -> str:
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

    return response

# Debug
if __name__ == "__main__":
    sample = {
        "decision": "reject",
        "ethics": {
            "reason": "This action may lead to harm.",
            "matched_rules": ["avoid_harm"]
        },
        "suggested_rule": None,
        "parsed": {"intents": ["harm", "self_reference"]}
    }

    print("\n🗣️ EXPRESSION:")
    print(generate_response(sample))
