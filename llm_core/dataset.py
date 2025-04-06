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
ist für die Verarbeitung von Trainingsdaten verantwortlich.
Sie bereitet Textdaten für das Training des Sprachmodells auf und sorgt dafür,
dass sie im richtigen Format vorliegen.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

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