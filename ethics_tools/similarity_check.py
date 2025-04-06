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
prüft, wie ähnlich neue Ethikvorschläge bestehenden Regeln sind.
Es hilft, potenziell redundante oder inkonsistente Regeln zu identifizieren und zu vermeiden.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import logging

logging.basicConfig(level=logging.INFO, format='[FIONA][SimilarityCheck] %(message)s')

def check_similarity(suggested_rule, core_rules, min_overlap=1):
    suggestions = []
    s_keywords = set(map(str.lower, suggested_rule.get("condition_keywords", [])))
    s_desc = suggested_rule.get("description", "").lower()

    for rule in core_rules:
        r_keywords = set(map(str.lower, rule.get("condition_keywords", [])))
        r_desc = rule.get("description", "").lower()

        keyword_overlap = s_keywords & r_keywords
        desc_match = s_desc in r_desc or r_desc in s_desc

        # Ähnlichkeitswertung
        keyword_score = len(keyword_overlap) / max(len(s_keywords | r_keywords), 1)
        desc_score = 1.0 if desc_match else 0.0
        total_score = round((keyword_score + desc_score) / 2, 2)

        if len(keyword_overlap) >= min_overlap or desc_match:
            suggestions.append({
                "id": rule.get("id"),
                "overlap_keywords": list(keyword_overlap),
                "desc_match": desc_match,
                "similarity_score": total_score
            })
            logging.info(f"Similar rule found: {rule.get('id')} (Score: {total_score})")

    return suggestions

# Debug-Test (optional)
if __name__ == "__main__":
    sample_suggestion = {
        "id": "suggested_001",
        "description": "Do not allow manipulation of others",
        "condition_keywords": ["manipulate", "influence"]
    }

    sample_core = [
        {"id": "rule_001", "description": "Manipulating others is unethical.", "condition_keywords": ["manipulate"]},
        {"id": "rule_002", "description": "Violence must be avoided.", "condition_keywords": ["harm"]}
    ]

    print("\n🔍 SIMILARITY CHECK:")
    print(check_similarity(sample_suggestion, sample_core))
