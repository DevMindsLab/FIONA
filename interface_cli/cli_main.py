import sys
import argparse
import logging
import warnings
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from core_ethics.ethics_link import check_ethics_validity
from core_interface.context_memory import ContextMemory
from core_decision.decision_engine import DecisionEngine
from learnlog.logger import log_question
from utils.logger import log
from llm_core.core import CoreLLM, check_model_integrity  # <— hinzugefügt

logging.basicConfig(level=logging.INFO, format='[FIONA][CLI] %(message)s')
warnings.filterwarnings("ignore", category=FutureWarning)

def print_intro():
    print("\n🌸 Welcome to FIONA – Friendly Intelligence Of Neutral Assistance")
    print("Type 'exit' to quit.\n")

def run_loop(engine: DecisionEngine, memory: ContextMemory, model: CoreLLM, debug: bool = False):
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ('exit', 'quit'):
                print("👋 Goodbye.")
                break

            prompts = [prompt.strip() for prompt in user_input.split(',') if prompt]
            if not prompts:
                continue

            results = [engine.decide(prompt) for prompt in prompts]
            responses = [model.generate_response(r["input"]) for r in results]

            for prompt, response in zip(prompts, responses):
                print(f"FIONA: {response}")

                if results[prompts.index(prompt)]["decision"] == "reject":
                    log_question(prompt)

                if debug:
                    log(f"Prompt: {prompt}", level="INFO")
                    log(f"Intents: {results[prompts.index(prompt)]['parsed'].get('intents', [])}", level="DEBUG")
                    log(f"Ethics: {results[prompts.index(prompt)]['ethics']}", level="DEBUG")
                    log(f"Decision: {results[prompts.index(prompt)]['decision']}", level="INFO")

                    if results[prompts.index(prompt)].get("suggested_rule"):
                        log(f"Suggested Rule: {results[prompts.index(prompt)]['suggested_rule']}", level="INFO")

            last = memory.get_last_ethics()
            if last:
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

    # === Modellpfade ===
    model_path = "../llm_core/model/gpt2"
    tokenizer_path = "../llm_core/model/gpt2"
    ethics_rules_path = "../core_ethics/core_ethics.json"

    # ✅ Integritätsprüfung für das Modell
    if not check_model_integrity(model_path, tokenizer_path):
        print("🚫 Modellprüfung fehlgeschlagen. Bitte überprüfe die Dateien im Pfad.")
        return

    engine = DecisionEngine()
    memory = ContextMemory()

    model = CoreLLM(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        ethics_rules_path=ethics_rules_path
    )

    run_loop(engine, memory, model, debug=args.debug)

if __name__ == "__main__":
    main()
