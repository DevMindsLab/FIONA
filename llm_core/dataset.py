import torch
from torch.utils.data import Dataset
import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO, format='[FIONA][Dataset] %(message)s')

class TextDataset(Dataset):
    def __init__(self, filepath: str, tokenizer, block_size: int):
        self.tokenizer = tokenizer
        self.block_size = block_size
        self.data = []

        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    ids = tokenizer.encode(line)
                    ids = tokenizer.pad_sequence(ids.tolist(), block_size)
                    x = torch.tensor(ids[:-1], dtype=torch.long)
                    y = torch.tensor(ids[1:], dtype=torch.long)
                    self.data.append((x, y))
                except Exception as e:
                    logging.warning(f"Skipped line due to error: {e}")

        logging.info(f"Loaded {len(self.data)} samples from {filepath}")

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.data[idx]