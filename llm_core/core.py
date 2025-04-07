import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[FIONA][LLM-Core] %(message)s')


__all__ = ["CoreLLM", "check_model_integrity"]

def check_model_integrity(model_path: str, tokenizer_path: str) -> bool:
    required_files = [
        "config.json",
        "pytorch_model.bin",  # oder: model.safetensors
        "tokenizer.json",
        "vocab.json",
        "tokenizer_config.json"
    ]

    all_paths = [
        os.path.join(model_path, f) for f in required_files[:2]
    ] + [
        os.path.join(tokenizer_path, f) for f in required_files[2:]
    ]

    missing = [f for f in all_paths if not os.path.exists(f)]
    if missing:
        logging.error("[FIONA][LLM-Core] Missing required model/tokenizer files:")
        for f in missing:
            logging.error(f"  - {f}")
        return False

    logging.info("[FIONA][LLM-Core] Model and tokenizer files verified.")
    return True

class CoreLLM:
    def __init__(self, model_path: str, tokenizer_path: str, ethics_rules_path: str):
        model_path = Path(model_path).resolve()
        tokenizer_path = Path(tokenizer_path).resolve()

        logging.info(f"Loading model from: {model_path}")
        self.model = GPT2LMHeadModel.from_pretrained(
            pretrained_model_name_or_path=model_path,
            local_files_only=True,
            use_safetensors=False  # Wichtig: zwingt das Laden von .bin
        )
        logging.info("Model loaded successfully.")

        logging.info(f"Loading tokenizer from: {tokenizer_path}")
        self.tokenizer = GPT2Tokenizer.from_pretrained(
            pretrained_model_name_or_path=tokenizer_path,
            local_files_only=True
        )
        logging.info("Tokenizer loaded successfully.")

        self.model.eval()

    def generate_response(self, prompt: str, max_length: int = 100) -> str:
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        outputs = self.model.generate(
            inputs,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            top_k=50,
            top_p=0.95,
            temperature=1.0
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
