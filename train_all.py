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
