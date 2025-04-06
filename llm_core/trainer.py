import os
import torch
import logging
from torch.utils.data import DataLoader
from llm_core.core import LanguageModel
from llm_core.dataset import TextDataset
from llm_core.tokenizer.bpe_tokenizer import BPETokenizer

logging.basicConfig(level=logging.INFO, format='[FIONA][Trainer] %(message)s')

# Hyperparameter
EMBED_DIM = 256
N_HEADS = 4
N_LAYERS = 4
BLOCK_SIZE = 64
BATCH_SIZE = 32
EPOCHS = 3
LR = 3e-4
VOCAB_SIZE = 4096

# Pfade
CORPUS_PATH = "llm_core/training_data/corpus.txt"
MODEL_PATH = "llm_core/checkpoints/mini_gpt.pth"
TOKENIZER_PATH = "llm_core/tokenizer/fiona_bpe.model"

def train():
    tokenizer = BPETokenizer(TOKENIZER_PATH)
    dataset = TextDataset(CORPUS_PATH, tokenizer, BLOCK_SIZE)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    model = LanguageModel(VOCAB_SIZE, EMBED_DIM, N_HEADS, N_LAYERS, BLOCK_SIZE)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)

    logging.info(f"Training Mini-FIONA for {EPOCHS} epochs on {len(dataset)} samples")

    model.train()
    for epoch in range(EPOCHS):
        total_loss = 0.0
        for i, (x, y) in enumerate(dataloader):
            optimizer.zero_grad()
            loss = model(x, y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

            if (i + 1) % 100 == 0:
                avg_loss = total_loss / (i + 1)
                logging.info(f"Epoch {epoch+1} Step {i+1}/{len(dataloader)} Loss: {avg_loss:.4f}")

        epoch_loss = total_loss / len(dataloader)
        logging.info(f"Epoch {epoch+1} finished. Avg Loss: {epoch_loss:.4f}")

    torch.save(model.state_dict(), MODEL_PATH)
    logging.info(f"Model saved to: {MODEL_PATH}")

if __name__ == "__main__":
    train()