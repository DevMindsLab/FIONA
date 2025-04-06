import torch
from llm_core.core import LanguageModel
from llm_core.tokenizer.bpe_tokenizer import BPETokenizer

MODEL_PATH = "llm_core/checkpoints/mini_gpt.pth"
MODEL_DIM = 256
N_HEADS = 4
N_LAYERS = 4
BLOCK_SIZE = 64
VOCAB_SIZE = 4096
TOKENIZER_MODEL = "llm_core/tokenizer/fiona_bpe.model"
MAX_OUTPUT_TOKENS = 30

PROMPTS = [
    "Wie heißt du?",
    "Was ist der Sinn des Lebens?",
    "Was sagst du zu Gewalt?",
    "Was bedeutet Ethik?",
    "Wie kann ich andere manipulieren?"
]

def autoregressive_generate(model, tokenizer, prompt, max_tokens=30):
    model.eval()
    with torch.no_grad():
        idx = tokenizer.encode(prompt).unsqueeze(0)
        for _ in range(max_tokens):
            idx_cond = idx[:, -BLOCK_SIZE:]
            logits = model(idx_cond)
            logits = logits[:, -1, :]
            probs = torch.softmax(logits, dim=-1)
            next_id = torch.argmax(probs, dim=-1).unsqueeze(0)
            idx = torch.cat([idx, next_id], dim=1)
        decoded = tokenizer.decode(idx[0].tolist())
        return decoded

def main():
    print("# FIONA MiniLLM Evaluation\n")
    tokenizer = BPETokenizer(TOKENIZER_MODEL)
    model = LanguageModel(VOCAB_SIZE, MODEL_DIM, N_HEADS, N_LAYERS, BLOCK_SIZE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))

    print("| Prompt | Response |")
    print("|--------|----------|")

    for prompt in PROMPTS:
        answer = autoregressive_generate(model, tokenizer, prompt, MAX_OUTPUT_TOKENS)
        short = answer.replace("\n", " ").strip()
        print(f"| {prompt} | {short} |")

if __name__ == "__main__":
    main()