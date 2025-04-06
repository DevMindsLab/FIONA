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
ist für die Generierung von Texten durch das Sprachmodell verantwortlich.
Es nutzt das trainierte Modell, um neue Texte basierend auf Benutzereingaben zu erzeugen.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import torch
from llm_core.core import LanguageModel
from llm_core.tokenizer.bpe_tokenizer import BPETokenizer

MODEL_PATH = "llm_core/checkpoints/mini_gpt.pth"
TOKENIZER_MODEL = "llm_core/tokenizer/fiona_bpe.model"
VOCAB_SIZE = 4096
EMBED_DIM = 256
N_HEADS = 4
N_LAYERS = 4
BLOCK_SIZE = 64
MAX_TOKENS = 50
TOP_K = 10

def generate(model, tokenizer, prompt: str, max_tokens: int = MAX_TOKENS, top_k: int = TOP_K):
    model.eval()
    with torch.no_grad():
        encoded = tokenizer.encode(prompt).unsqueeze(0)  # [1, T]
        for _ in range(max_tokens):
            idx_cond = encoded[:, -BLOCK_SIZE:]
            logits = model(idx_cond)
            logits = logits[:, -1, :]
            probs = torch.softmax(logits, dim=-1)

            # Top-k Sampling
            top_k = min(top_k, probs.shape[-1])
            top_k_probs, top_k_indices = torch.topk(probs, top_k)
            top_k_probs = top_k_probs / top_k_probs.sum()  # normalize

            try:
                next_token = torch.multinomial(top_k_probs, num_samples=1)
            except RuntimeError as e:
                print(f"⚠️ Sampling error: {e}. Falling back to argmax.")
                next_token = torch.argmax(top_k_probs, dim=-1, keepdim=True)

            next_id = top_k_indices.gather(-1, next_token)
            encoded = torch.cat([encoded, next_id], dim=1)

        return tokenizer.decode(encoded[0].tolist())

def main():
    tokenizer = BPETokenizer(TOKENIZER_MODEL)
    model = LanguageModel(VOCAB_SIZE, EMBED_DIM, N_HEADS, N_LAYERS, BLOCK_SIZE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))

    while True:
        prompt = input("🧠 Prompt: ").strip()
        if not prompt:
            break
        output = generate(model, tokenizer, prompt)
        print(f"FIONA: {output}\n")

if __name__ == "__main__":
    main()
