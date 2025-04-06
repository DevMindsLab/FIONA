"""
======================================
FIONA - Projektname

Autor: Rene Baumgarten (DevMindsLab)
Datum: 18.03.2025
Version: 0.8

Beschreibung:
---------------
Diese Python-Datei ist Teil des **FIONA**-Projekts,
einer ethisch ausgerichteten,
Open-Source-basierten Künstlichen Intelligenz (KAI). Das Projekt strebt an,
verantwortungsbewusste, nachvollziehbare und kontrollierte Entscheidungen in ethischen Dilemmata zu treffen.
Der Code in dieser Datei ist Teil des Backends, das für [Beschreibung der Funktionalität der Datei] zuständig ist.

Funktions Beschreibung:
---------------
Das zentrale Skript zum Training des gesamten FIONA-Modells.
Es übernimmt die Aufgaben der Datensatzvorbereitung, Tokenisierung,
Modelltraining sowie das Speichern von Modellen und Checkpoints.
Das Skript integriert alle Schritte des Trainingsprozesses,
um das Modell vollständig zu trainieren und zu optimieren.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import os
import shutil
from datetime import datetime
import subprocess

# === KONSTANTEN ===
CORPUS_PATH = "llm_core/training_data/corpus.txt"
FACTS_PATH = "llm_core/training_data/fiona_facts.json"
BACKUP_PATH = f"llm_core/training_data/backups/corpus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
TOKENIZER_SCRIPT = "llm_core/train_tokenizer.py"
TRAINER_SCRIPT = "llm_core/trainer.py"
EVALUATE_SCRIPT = "llm_core/evaluate_model.py"
CONVERT_SCRIPT = "llm_core/json_to_corpus.py"

# === BACKUP ===
print("🛡️ Backup erfolgreich erstellt.")
os.makedirs(os.path.dirname(BACKUP_PATH), exist_ok=True)
shutil.copy(CORPUS_PATH, BACKUP_PATH)

# === JSON zu Text umwandeln ===
print("🔄 JSON wird in lesbare Textform umgewandelt...")
result = subprocess.run(["python", CONVERT_SCRIPT, FACTS_PATH, CORPUS_PATH], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ Neue Trainingsdaten aus fiona_facts.json hinzugefügt.\n")
else:
    print("❌ Fehler bei der JSON-Konvertierung:\n", result.stderr)
    exit(1)

# === TOKENIZER-TRAINING ===
print("🚀 Running llm_core/train_tokenizer.py\n")
result = subprocess.run(["python", TOKENIZER_SCRIPT], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ Tokenizer training completed.\n")
else:
    print("❌ Fehler beim Tokenizer-Training:\n", result.stderr)
    exit(1)

# === MODELL-TRAINING ===
print("🚀 Running llm_core/trainer.py\n")
result = subprocess.run(["python", TRAINER_SCRIPT], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ Training complete & model saved.\n")
else:
    print("❌ Fehler beim Training:\n", result.stderr)
    exit(1)

# === EVALUATION (optional) ===
if os.path.exists(EVALUATE_SCRIPT):
    print("🔍 Modellbewertung wird gestartet...")
    subprocess.run(["python", EVALUATE_SCRIPT])
else:
    print("ℹ️ Kein evaluate_model.py gefunden – Bewertung übersprungen.")

print("\n✅ Training und Evaluation abgeschlossen.")
