import logging
from llm_core.model.model import Model
from llm_core.tokenizer.tokenizer import Tokenizer

logging.basicConfig(level=logging.INFO, format='[FIONA][Train] %(message)s')


def train(model_path: str, tokenizer_path: str, data):
    """
    Trainiert das Modell mit den angegebenen Daten.
    :param model_path: Der Pfad zum Modell.
    :param tokenizer_path: Der Pfad zum Tokenizer.
    :param data: Die Trainingsdaten.
    """
    model = Model(model_path)
    tokenizer = Tokenizer(tokenizer_path)

    # Beispielhafte Trainingslogik (diese kann je nach Bedarf angepasst werden)
    for epoch in range(3):
        for batch in data:
            inputs = tokenizer.encode(batch["input"])
            targets = tokenizer.encode(batch["target"])

            # Training durchführen (diese Logik muss je nach Modell angepasst werden)
            outputs = model.generate(inputs)
            # Berechne Verlust (hier nur als Beispiel)
            loss = compute_loss(outputs, targets)
            logging.info(f"Epoch {epoch + 1}, Loss: {loss}")

            # Optimierungs-Schritte etc.


def compute_loss(outputs, targets):
    # Dummy loss function
    return 0.1
