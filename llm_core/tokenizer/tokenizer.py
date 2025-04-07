import logging
from transformers import GPT2Tokenizer

logging.basicConfig(level=logging.INFO, format='[FIONA][Tokenizer] %(message)s')

class Tokenizer:
    def __init__(self, tokenizer_path: str):
        """
        Lädt den Tokenizer von einem lokalen Pfad.
        :param tokenizer_path: Der Pfad zu den gespeicherten Tokenizer-Dateien.
        """
        self.tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_path)
        logging.info(f"Tokenizer loaded from {tokenizer_path}")

    def encode(self, prompt: str):
        """
        Kodiert den Eingabe-Prompt in Tokens.
        :param prompt: Der Eingabeprompt, der in Tokens umgewandelt werden soll.
        :return: Die codierten Tokens.
        """
        return self.tokenizer.encode(prompt, return_tensors="pt")

    def decode(self, tokens):
        """
        Dekodiert die Tokens zurück in Text.
        :param tokens: Die Tokens, die in Text umgewandelt werden sollen.
        :return: Der decodierte Text.
        """
        return self.tokenizer.decode(tokens[0], skip_special_tokens=True)
