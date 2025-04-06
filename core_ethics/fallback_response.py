import logging
import random

logging.basicConfig(level=logging.INFO, format='[FIONA][Fallback] %(message)s')

actions = {
    "reject": [
        "No. I cannot support this request.",
        "I'm sorry, but this goes against my ethics.",
        "This request must be declined for ethical reasons."
    ],
    "allow": [
        "Yes, that seems fine.",
        "Of course, this aligns with my ethical framework.",
        "Sure, that appears to be ethically acceptable."
    ],
    "neutral": [
        "I'm unsure how to respond.",
        "I cannot confidently evaluate this request.",
        "This situation is unclear from an ethical standpoint."
    ]
}

def generate_fallback_response(user_input: str, reasoning: dict) -> str:
    action = reasoning.get("decision", "neutral")
    reason = reasoning.get("reason", "No reason provided.")

    response_intro = random.choice(actions.get(action, actions["neutral"]))
    response = f"{response_intro} {reason}"

    logging.info(f"Fallback response generated for action '{action}': {response}")
    return response