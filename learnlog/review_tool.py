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
Diese Datei enthält die Hauptlogik für die Ethikprüfung.
Sie analysiert Eingaben und prüft deren Übereinstimmung mit den Ethikrichtlinien von FIONA.
Entscheidungen werden basierend auf diesen Prüfungen getroffen und zur weiteren Verarbeitung zurückgegeben.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[FIONA][ReviewTool] %(message)s')

LOG_PATH = Path(__file__).resolve().parent / "learnlog.jsonl"
VALID_STATUSES = {"approved", "rejected", "ignored"}


def load_unreviewed():
    if not LOG_PATH.exists():
        logging.warning("Learnlog file not found.")
        return []

    questions = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("status") == "unreviewed":
                    questions.append(entry)
            except json.JSONDecodeError:
                continue
    return questions

def save_all(entries):
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def interactive_review():
    entries = []
    unreviewed = load_unreviewed()

    if not unreviewed:
        print("✅ No unreviewed questions found.")
        return

    print("🔍 Starting interactive review of questions")
    print("a = Approve | r = Reject | i = Ignore | q = Quit\n")

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                entries.append(line.strip())
                continue

            if entry.get("status") != "unreviewed":
                entries.append(json.dumps(entry, ensure_ascii=False))
                continue

            print("------------------------------")
            print(f"Question: {entry['question']}")
            print(f"Time:     {entry['timestamp']}")

            decision = input("→ (a/r/i/q): ").strip().lower()

            if decision == "q":
                logging.info("Review aborted by user.")
                break
            elif decision == "a":
                entry["status"] = "approved"
            elif decision == "r":
                entry["status"] = "rejected"
            elif decision == "i":
                entry["status"] = "ignored"
            else:
                print("⚠️ Unknown input. Skipping entry.")
                entries.append(json.dumps(entry, ensure_ascii=False))
                continue

            logging.info(f"Set status to '{entry['status']}' for: {entry['question']}")
            entries.append(json.dumps(entry, ensure_ascii=False))

    save_all(entries)
    print("\n✅ Review completed.")

if __name__ == "__main__":
    interactive_review()