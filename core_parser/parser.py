import re
import logging

logging.basicConfig(level=logging.INFO, format='[FIONA][Parser] %(message)s')

INTENT_PATTERNS = {
    "question": re.compile(r"\b(who|what|when|where|why|how|is|are|can|do|does)\b", re.IGNORECASE),
    "command": re.compile(r"\b(tell|show|explain|give|say|do|stop|start)\b", re.IGNORECASE),
    "greeting": re.compile(r"\b(hello|hi|hey|greetings)\b", re.IGNORECASE),
    "harm": re.compile(r"\b(kill|hurt|attack|destroy|harm|stab)\b", re.IGNORECASE),
    "ethics": re.compile(r"\b(right|wrong|moral|ethic|allowed|permitted|legal)\b", re.IGNORECASE),
    "self_reference": re.compile(r"\b(i|me|my|myself)\b", re.IGNORECASE),
}

def parse_input(text: str, verbose: bool = False) -> dict:
    tokens = text.lower().split()
    detected_intents = []
    matches = {}

    for label, pattern in INTENT_PATTERNS.items():
        if pattern.search(text):
            detected_intents.append(label)
            if verbose:
                found = pattern.findall(text)
                matches[label] = found
                logging.info(f"Intent '{label}' matched keywords: {found}")

    result = {
        "raw": text,
        "tokens": tokens,
        "intents": detected_intents
    }

    if verbose:
        result["matches"] = matches

    return result

# Debug
if __name__ == "__main__":
    example = "Can I hurt someone if it’s for a good reason?"
    result = parse_input(example, verbose=True)
    print("\n🧠 PARSE RESULT:")
    print(result)
