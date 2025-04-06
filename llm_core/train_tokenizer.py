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
