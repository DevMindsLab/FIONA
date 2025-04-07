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
from utils.logger import Logger  # Importiere den Logger aus dem utils-Ordner
from ethics_tools.similarity_check import check_similarity
from review import update_question_status
from core_decision.decision_engine import DecisionEngine
from core_ethics.engine import CoreEthicsEngine  # Importiere die CoreEthicsEngine
from core_interface.context_memory import ContextMemory  # Importiere die ContextMemory-Klasse

# Initialisiere den Logger
logger = Logger()

logging.basicConfig(level=logging.INFO, format='[FIONA][App] %(message)s')

app = Flask(__name__)

# Initialisiere die Engines und das ContextMemory-Objekt
ethics_engine = CoreEthicsEngine()  # Initialisiere den CoreEthicsEngine
decision_engine = DecisionEngine()  # Initialisiere die DecisionEngine
memory = ContextMemory()  # Initialisiere das ContextMemory-Objekt

SUGGESTED_PATH = os.path.join(os.path.dirname(__file__), "../ethics_tools/suggested_rules.json")
CORE_PATH = os.path.join(os.path.dirname(__file__), "../core_ethics/core_ethics.json")

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.log(f"Failed to load JSON from {path}: {e}", level="ERROR")  # Logge den Fehler
        return []

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.log(f"Failed to save JSON to {path}: {e}", level="ERROR")  # Logge den Fehler

def is_valid_rule(rule):
    required_keys = ["id", "description", "condition_keywords", "action"]
    return all(k in rule for k in required_keys)

def load_unreviewed():
    all_questions = load_json(SUGGESTED_PATH)
    unreviewed_questions = [q for q in all_questions if q.get("status") not in ["approved", "rejected"]]
    return unreviewed_questions

@app.route("/", methods=["GET", "POST"])
def index():
    user_input = ""
    response = ""
    debug_info = ""
    context_info = ""
    valid, ethics_msg = "valid", "Ethikprüfung erfolgreich."

    if request.method == "POST":
        user_input = request.form.get("question", "").strip()

        # Logge die Benutzeranfrage
        logger.log(f"User input: {user_input}")

        # Überprüfe die Ethik mit der CoreEthicsEngine
        valid, ethics_msg = ethics_engine.evaluate(user_input)["decision"], ethics_msg

        if not valid:
            response = "⚠️ Ethikprüfung fehlgeschlagen."
            debug_info = f"ETHIK-PRÜFUNG: {ethics_msg}"
            logger.log(f"Ethikprüfung fehlgeschlagen: {ethics_msg}", level="ERROR")  # Logge das Fehlschlagen
        elif not user_input:
            response = "Bitte gib eine Frage ein."
            debug_info = "Keine Eingabe."
            logger.log("Keine Benutzereingabe erhalten", level="WARNING")  # Logge die Warnung bei fehlender Eingabe
        else:
            decision_result = decision_engine.decide(user_input)
            response = decision_result.get("response", "(keine Antwort)")
            debug_info = f"Antworttyp: {decision_result.get('type', '?')}"

            reason = decision_result.get("reason", "Keine Information verfügbar")  # Ersetze None durch eine Standardnachricht
            logger.log(f"Entscheidung: {decision_result.get('decision')} | Grund: {reason}") # Logge die Entscheidung und den Grund

            memory.remember(user_input, decision_result.get("decision", "?"), decision_result.get("reason", ""))
            last = memory.get_last_ethics()
            if last and last["input"] != user_input:
                context_info = f"🧠 Letzte Frage: '{last['input']}' → Antwort: '{last['decision']}'"

            logging.info(f"Frage: {user_input} → Entscheidung: {decision_result.get('decision')}")

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
                    logger.log(f"Angenommene Regel: {rule_id}")  # Logge die Annahme der Regel
                elif action == "reject":
                    logger.log(f"Abgelehnte Regel: {rule_id}")  # Logge die Ablehnung der Regel
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