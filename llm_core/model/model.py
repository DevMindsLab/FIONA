import logging
from transformers import GPT2LMHeadModel

logging.basicConfig(level=logging.INFO, format='[FIONA][Model] %(message)s')


class Model:
    def __init__(self, model_path: str):
        """
        Lädt das Modell von einem lokalen Pfad.
        :param model_path: Der Pfad zu den gespeicherten Modell-Dateien.
        """
        self.model = GPT2LMHeadModel.from_pretrained(model_path)
        self.model.eval()  # Setzt das Modell in den Evaluierungsmodus
        logging.info(f"Model loaded from {model_path}")

    def generate(self, inputs, max_length=100):
        """
        Generiert Text basierend auf den Eingaben.
        :param inputs: Die Eingabedaten für das Modell.
        :param max_length: Maximale Länge des generierten Textes.
        :return: Der generierte Text.
        """
        outputs = self.model.generate(inputs, max_length=max_length, num_return_sequences=1,
                                      no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=1.0)
        return outputs
