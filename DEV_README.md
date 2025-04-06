
# Mini-FIONA v0.1 - Entwicklerdokumentation

Mini-FIONA ist eine **ethische, hybride Künstliche Intelligenz** (KI), die **natürliche Sprachverarbeitung** mit **ethischer Entscheidungsfindung** kombiniert. Das Projekt nutzt die **Transformer-Architektur**, **BPE-Tokenization** und eine **Webschnittstelle** für die Interaktion.

## 📖 Inhaltsverzeichnis

1. [Projektübersicht](#projektübersicht)
2. [Technische Architektur](#technische-architektur)
3. [Installation und Setup](#installation-und-setup)
4. [Verzeichnisse und Dateien](#verzeichnisse-und-dateien)
5. [Modelldetails](#modelldetails)
6. [Ethische Entscheidungslogik](#ethische-entscheidungslogik)
7. [Webschnittstelle](#webschnittstelle)
8. [Erweiterungsmöglichkeiten](#erweiterungsmöglichkeiten)
9. [Beitragen](#beitragen)
10. [Lizenz](#lizenz)

## Projektübersicht

Mini-FIONA ist eine KI, die auf **ethischer Entscheidungsfindung** basiert. Das Modell nutzt eine **Transformer-Architektur** (ähnlich GPT) und kombiniert diese mit einer **ethischen Entscheidungslogik**, um in Echtzeit Entscheidungen zu treffen, die sowohl sprachlich als auch ethisch sinnvoll sind.

- **Transformer** für die Sprachverarbeitung
- **Ethikprüfung** zur Validierung von Antworten
- **Kontextspeicherung** für nachhaltige Entscheidungsfindung

## Technische Architektur

### 1. **Sprachmodell**:  
Das Modell basiert auf einem Transformer mit einer **Self-Attention**-Schicht, die durch **Token- und Positions-Embeddings** unterstützt wird. Es nutzt **BPE (Byte Pair Encoding)** zur Tokenisierung und wird durch **PyTorch** trainiert.

### 2. **Ethikprüfungsmechanismus**:  
Der Ethik-Kern validiert jede Benutzeranfrage und sorgt dafür, dass die Antworten **ethisch vertretbar** sind. Regeln und Vorschläge werden von Benutzern und Entwicklern überprüft, um die ethische Integrität zu gewährleisten.

### 3. **Webschnittstelle**:  
Die Web-App ermöglicht es Benutzern, Fragen zu stellen und Antworten von Mini-FIONA zu erhalten. Die Flask-App verwendet **Jinja2-Templates** und **Formulare** für die Benutzerinteraktion.

---

## Installation und Setup

### Voraussetzungen

- **Python 3.8+**
- **Abhängigkeiten installieren**:
  ```bash
  pip install -r requirements.txt
  ```

### Modelltraining

1. **Tokenizer trainieren**:
   Um den BPE-Tokenizer zu trainieren, führe das folgende Skript aus:
   ```bash
   python train_tokenizer.py
   ```

2. **Modell trainieren**:
   Das Sprachmodell wird mit dem Trainer-Skript trainiert:
   ```bash
   python trainer.py
   ```

3. **Modell evaluieren**:
   Führe das Evaluierungsskript aus, um das Modell zu testen:
   ```bash
   python evaluate_model.py
   ```

### Flask Web-App starten

Um die Web-App zu starten, führe `app.py` aus:
```bash
python fiona_web/app.py
```
Rufe die Webanwendung unter [http://127.0.0.1:5000/](http://127.0.0.1:5000/) im Browser auf.

---

## Verzeichnisse und Dateien

### Hauptdateien

1. **`fiona_web/app.py`**: Die Flask-App, die die gesamte Webschnittstelle verwaltet.
2. **`review.py`**: Logik zur Verwaltung und Überprüfung von Fragen im Learnlog.
3. **`train_tokenizer.py`**: Trainiert den BPE-Tokenizer.
4. **`trainer.py`**: Trainiert das Sprachmodell.
5. **`evaluate_model.py`**: Bewertet das Modell anhand von Testdaten.

### `fiona_web/templates/`:
Enthält die HTML-Templates für die Benutzeroberfläche:
- **`index.html`**: Eingabemaske und Antwortanzeige.
- **`review.html`**: Anzeige und Verwaltung von „unreviewed“ Fragen.
- **`suggestions.html`**: Verwaltung von Regelvorschlägen.

---

## Modelldetails

Das **Mini-FIONA-Modell** basiert auf einer **Transformer-Architektur** und wird mit **PyTorch** trainiert. Die wichtigsten Komponenten:

1. **Tokenisierung**: Das Modell verwendet **Byte Pair Encoding (BPE)** zur Tokenisierung von Texten.
2. **Transformer**: Der Transformer-Block besteht aus Multi-Head Attention, Feedforward-Netzwerken und Residual Connections.
3. **Positional Encoding**: Positional Encodings werden hinzugefügt, um die Reihenfolge der Tokens zu berücksichtigen.

---

## Ethische Entscheidungslogik

1. **Regelvalidierung**: Vor jeder Antwort prüft FIONA, ob die Antwort ethisch vertretbar ist, basierend auf vordefinierten Regeln.
2. **Entscheidungsfindung**: FIONA verwendet eine **entscheidungsbasierte Logik**, um jede Antwort zu validieren und sicherzustellen, dass sie sowohl sprachlich korrekt als auch ethisch unbedenklich ist.

---

## Webschnittstelle

Die Webschnittstelle besteht aus einer **Flask-App** mit den folgenden Hauptkomponenten:

1. **Eingabe**: Benutzer stellen Fragen über ein einfaches Formular auf der `index.html`.
2. **Antwort**: Die Antwort wird von FIONA generiert und auf der Seite angezeigt.
3. **Ethikprüfung**: FIONA validiert die Antwort vor der Anzeige.
4. **Review und Vorschläge**: Im Review-Bereich können Nutzer ethische Fragen und Regelvorschläge überprüfen und akzeptieren oder ablehnen.

---

## Erweiterungsmöglichkeiten

- **Erweiterung des Modells**: Du kannst zusätzliche Layer oder eine größere Vokabulargröße hinzufügen, um das Modell leistungsfähiger zu machen.
- **Erweiterte ethische Entscheidungslogik**: Hinzufügen von komplexeren Ethikprüfungen und Entscheidungshilfen.
- **API**: Du kannst eine RESTful API hinzufügen, um FIONA als Backend für andere Anwendungen zu verwenden.

---

## Beitragen

1. **Fork das Repository**.
2. **Erstelle einen neuen Branch** (`git checkout -b feature-xyz`).
3. **Nimm deine Änderungen vor**.
4. **Führe Tests durch** und stelle sicher, dass alles funktioniert.
5. **Erstelle einen Pull Request**.

---

## Lizenz

Mini-FIONA ist ein **Open-Source-Projekt** unter der **MIT-Lizenz**.  
Siehe [LICENSE](LICENSE) für weitere Details.
