def generate_ethics_template_response(user_input: str, reasoning: dict) -> str:
    decision = reasoning.get("decision", "neutral")
    reason = reasoning.get("reason", "No reason provided.")
    rule_ids = reasoning.get("matched_rules", [])

    if decision == "reject":
        return (
            f"I'm sorry, but I must reject your request. "
            f"It conflicts with my core ethical principle: {reason}"
        )
    elif decision == "allow":
        return (
            f"This request appears to be ethically acceptable. "
            f"Reason: {reason}"
        )
    else:
        return (
            f"I'm uncertain about this request. "
            f"Please clarify your intent. Reason: {reason}"
        )
