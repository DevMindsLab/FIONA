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
ist die zentrale Datei für die Webanwendung von FIONA.
Sie steuert den Webserver, verwaltet Benutzeranfragen und stellt sicher,
dass die richtigen ethischen Prüfungen und Antworten ausgegeben werden.

Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

from flask import Flask, render_template, request, redirect, url_for
import json
import os
import logging

# Dummy-Implementierung von respond_to_input (wegen der Entfernung von hybrid_core)
def respond_to_input(user_input):
    # Rückgabe einer einfachen Antwort basierend auf der Eingabe
    return {
        "response": f"Antwort auf die Frage: {user_input}",
        "type": "text",
        "decision": "accepted",
        "reason": "Antwort wurde basierend auf den Regeln generiert."
    }

# Dummy-Ethische Validierung (wegen Entfernung von check_ethics_validity)
def check_ethics_validity():
    # Immer als gültig zurückgeben, da keine Ethikprüfung mehr vorhanden ist
    return True, "Ethikprüfung erfolgreich."

# Dummy-Implementierung von ContextMemory (wegen Entfernung)
class ContextMemory:
    def __init__(self):
        self.memory = []

    def remember(self, user_input, decision, reason):
        self.memory.append({"input": user_input, "decision": decision, "reason": reason})

    def get_last_ethics(self):
        return self.memory[-1] if self.memory else None

logging.basicConfig(level=logging.INFO, format='[FIONA][App] %(message)s')

app = Flask(__name__)
memory = ContextMemory()

SUGGESTED_PATH = os.path.join(os.path.dirname(__file__), "../ethics_tools/suggested_rules.json")
CORE_PATH = os.path.join(os.path.dirname(__file__), "../core_ethics/core_ethics.json")

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.warning(f"Failed to load JSON from {path}: {e}")
        return []

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to save JSON to {path}: {e}")

def is_valid_rule(rule):
    required_keys = ["id", "description", "condition_keywords", "action"]
    return all(k in rule for k in required_keys)

@app.route("/", methods=["GET", "POST"])
def index():
    valid, ethics_msg = check_ethics_validity()
    user_input = ""
    response = ""
    debug_info = ""
    context_info = ""

    if request.method == "POST":
        user_input = request.form.get("question", "").strip()

        if not valid:
            response = "⚠️ Ethikprüfung fehlgeschlagen."
            debug_info = "ETHIK-KERN UNGÜLTIG"
        elif not user_input:
            response = "Bitte gib eine Frage ein."
            debug_info = "Keine Eingabe."
        else:
            result = respond_to_input(user_input)
            response = result.get("response", "(keine Antwort)")
            debug_info = f"Antworttyp: {result.get('type', '?')}"

            memory.remember(user_input, result.get("decision", "?"), result.get("reason", ""))
            last = memory.get_last_ethics()
            if last and last["input"] != user_input:
                context_info = f"🧠 Letzte Frage: '{last['input']}' → Antwort: '{last['decision']}'"

            logging.info(f"Frage: {user_input} → Typ: {result.get('type')} | Entscheidung: {result.get('decision')}")

    return render_template("index.html",
        question=user_input,
        answer=response,
        ethics_valid=valid,
        ethics_msg=ethics_msg,
        debug_info=debug_info,
        context_info=context_info
    )

@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "POST":
        timestamp = request.form.get("timestamp")
        action = request.form.get("action")
        if timestamp and action:
            update_question_status(timestamp, action)

    questions = load_unreviewed()
    return render_template("review.html", questions=questions)

@app.route("/suggestions", methods=["GET", "POST"])
def suggestions():
    suggestions = load_json(SUGGESTED_PATH)
    core_rules = load_json(CORE_PATH)

    if request.method == "POST":
        action = request.form.get("action")
        rule_id = request.form.get("rule_id")

        updated_suggestions = []
        for rule in suggestions:
            if rule.get("id") == rule_id:
                if action == "accept" and is_valid_rule(rule):
                    core_rules.append(rule)
                    logging.info(f"Angenommene Regel: {rule_id}")
                elif action == "reject":
                    logging.info(f"Abgelehnte Regel: {rule_id}")
                    continue
            else:
                updated_suggestions.append(rule)

        save_json(CORE_PATH, core_rules)
        save_json(SUGGESTED_PATH, updated_suggestions)
        return redirect(url_for("suggestions"))

    for rule in suggestions:
        rule["similar"] = check_similarity(rule, core_rules)

    return render_template("suggestions.html", suggestions=suggestions)

if __name__ == "__main__":
    app.run(debug=True)