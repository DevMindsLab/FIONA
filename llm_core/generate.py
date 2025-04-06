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
