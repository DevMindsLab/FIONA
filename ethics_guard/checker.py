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