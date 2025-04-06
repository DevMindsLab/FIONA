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
import argparse

logging.basicConfig(level=logging.INFO, format='[FIONA][ExportApproved] %(message)s')

LOG_PATH = Path(__file__).resolve().parent / "learnlog.jsonl"
OUT_PATH = Path(__file__).resolve().parent / "approved_questions.json"

def export_questions(status="approved", dry_run=False):
    if not LOG_PATH.exists():
        logging.warning("Learnlog file not found.")
        return

    entries = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("status") == status:
                    entries.append(entry)
            except json.JSONDecodeError:
                logging.warning("Invalid line skipped.")

    if not entries:
        logging.info(f"No entries found with status '{status}'.")
        return

    if dry_run:
        logging.info(f"Dry run: {len(entries)} entries with status '{status}' would be exported.")
        for e in entries:
            print(f"- {e['timestamp']} | {e['question']}")
        return

    with open(OUT_PATH, "w", encoding="utf-8") as out:
        json.dump(entries, out, indent=2)
        logging.info(f"Exported {len(entries)} entries to '{OUT_PATH.name}'.")

def main():
    parser = argparse.ArgumentParser(description="Export questions from learnlog.jsonl")
    parser.add_argument("--status", default="approved", help="Status to filter for (default: approved)")
    parser.add_argument("--dry-run", action="store_true", help="Only print what would be exported")
    args = parser.parse_args()

    export_questions(status=args.status, dry_run=args.dry_run)

if __name__ == "__main__":
    main()