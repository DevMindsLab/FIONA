import logging
from core_parser.parser import parse_input
from core_ethics.engine import CoreEthicsEngine
from core_interface.context_memory import ContextMemory
from ethics_tools.learning_engine import suggest_rule

logging.basicConfig(level=logging.INFO, format='[FIONA][DecisionEngine] %(message)s')

class DecisionEngine:
    def __init__(self):
        self.ethics = CoreEthicsEngine()
        self.memory = ContextMemory()

    def decide(self, user_input: str) -> dict:
        parsed = parse_input(user_input)
        logging.info(f"Parsed input: {parsed}")

        ethics_result = self.ethics.evaluate(user_input)
        decision = ethics_result.get("decision", "neutral")

        # Wenn Ethik neutral, prüfen wir selbst anhand von Parser-Intents
        if decision == "neutral":
            if "harm" in parsed.get("intents", []):
                decision = "reject"
            elif "greeting" in parsed.get("intents", []):
                decision = "accept"
            elif "question" in parsed.get("intents", []):
                decision = "ask"
            else:
                decision = "neutral"

        # Kontext speichern
        reason = ethics_result.get("reason", "No reason provided.")
        self.memory.remember(user_input, decision, reason)
        logging.info(f"Context updated with decision '{decision}'")

        # Wenn weiterhin neutral → Regelvorschlag initiieren
        suggested = None
        if decision == "neutral":
            suggested = suggest_rule(user_input, parsed.get("intents", []))
            if suggested:
                logging.info(f"Suggested new rule: {suggested}")

        return {
            "input": user_input,
            "parsed": parsed,
            "ethics": ethics_result,
            "decision": decision,
            "suggested_rule": suggested
        }

# Debug
if __name__ == "__main__":
    engine = DecisionEngine()
    test = "Can I harm someone who is evil?"
    result = engine.decide(test)

    print("\n⚖️ DECISION RESULT:")
    for k, v in result.items():
        print(f"{k.upper()}: {v}")
