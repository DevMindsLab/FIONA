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
trainiert den Tokenizer für das FIONA-Sprachmodell. Er verarbeitet Textdaten und erstellt ein Vokabular,
das die Grundlage für die Texterstellung und -verarbeitung im Modell bildet. Der Tokenizer ermöglicht es,
Texte in handhabbare Einheiten (Tokens) zu zerlegen, um eine effiziente Verarbeitung zu gewährleisten.

Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import os
import logging
import sentencepiece as spm

logging.basicConfig(level=logging.INFO, format='[FIONA][TokenizerTrain] %(message)s')

corpus_path = "llm_core/training_data/corpus.txt"
output_path = "llm_core/tokenizer/fiona_bpe"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(corpus_path, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]
    line_count = len(lines)

vocab_size = min(4096, max(500, line_count * 10))
logging.info(f"Training tokenizer on {line_count} lines with vocab size {vocab_size}.")

spm.SentencePieceTrainer.train(
    input=corpus_path,
    model_prefix=output_path,
    vocab_size=vocab_size,
    pad_id=0,
    bos_id=1,
    eos_id=2,
    unk_id=3,
    model_type="bpe",
    user_defined_symbols=["<|sep|>", "<|user|>", "<|fiona|>"]
)

logging.info("Tokenizer training completed.")
