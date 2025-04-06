import os
from core_ethics.engine import CoreEthicsEngine
from colorama import Fore, Style, init
from collections import Counter

init(autoreset=True)

TEST_FILE = os.path.join(os.path.dirname(__file__), "test_sentences.txt")

def load_test_inputs():
    if not os.path.exists(TEST_FILE):
        print("❌ test_sentences.txt not found.")
        return []
    with open(TEST_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    ethics = CoreEthicsEngine()
    test_inputs = load_test_inputs()

    if not test_inputs:
        print("⚠️ No test inputs found. Add test_sentences.txt with sample phrases.")
        return

    print("🔍 Starting FIONA Ethics Self-Test\n")
    stats = Counter()

    for text in test_inputs:
        result = ethics.evaluate(text)
        action = result["decision"]
        reason = result["reason"]
        rules = result["matched_rules"]

        if action == "reject":
            color = Fore.RED
        elif action == "allow":
            color = Fore.GREEN
        else:
            color = Fore.YELLOW

        print(f"{color}INPUT: {text}")
        print(f"{color} → Decision: {action.upper()}")
        print(f"{color} → Reason: {reason}")
        print(f"{color} → Matched Rules: {rules}")
        print(Style.RESET_ALL + "-" * 60)

        stats[action] += 1

    # Statistik
    print("\n📊 Test Summary:")
    total = sum(stats.values())
    for k, v in stats.items():
        print(f"{k.capitalize():>8}: {v} ({v / total:.0%})")
    print(f"{'Total':>8}: {total} tests")

if __name__ == "__main__":
    main()
