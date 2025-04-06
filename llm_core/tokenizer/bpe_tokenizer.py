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
implementiert den Byte Pair Encoding (BPE)-Tokenizer,
der für die Aufteilung von Texten in Tokens zuständig ist.
Dies ist ein wichtiger Schritt bei der Textverarbeitung für das Sprachmodell.


Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import torch
import sentencepiece as spm
import logging
from typing import List, Union

logging.basicConfig(level=logging.INFO, format='[FIONA][Tokenizer] %(message)s')

class BPETokenizer:
    def __init__(self, model_path: str):
        self.sp = spm.SentencePieceProcessor()
        self.sp.load(model_path)
        self.vocab_size = self.sp.get_piece_size()
        logging.info(f"Loaded BPE tokenizer model from: {model_path} (vocab size: {self.vocab_size})")

    def encode(self, text: str) -> torch.Tensor:
        ids = self.sp.encode(text, out_type=int)
        logging.debug(f"Encoded: '{text}' → {ids}")
        return torch.tensor(ids, dtype=torch.long)

    def decode(self, ids: Union[List[int], torch.Tensor]) -> str:
        if isinstance(ids, torch.Tensor):
            ids = ids.tolist()
        try:
            decoded = self.sp.decode(ids)
            logging.debug(f"Decoded: {ids} → '{decoded}'")
            return decoded
        except Exception as e:
            logging.error(f"Failed to decode IDs {ids}: {e}")
            return "<decode-error>"

    def pad_sequence(self, ids: List[int], max_length: int) -> List[int]:
        padded = ids[:max_length] + [0] * (max_length - len(ids))
        return padded