
# Mini-FIONA v0.1

Mini-FIONA ist eine **ethische, hybride KI**, die mit einem kleinen Sprachmodell arbeitet und sowohl natürliche Sprachverarbeitung als auch ethische Entscheidungen trifft. Diese Version nutzt die **Transformer-Architektur** mit **BPE-Tokenization** und beinhaltet sowohl ein Web-Interface als auch eine **ethische Entscheidungslogik**.

## 📁 Projektstruktur

```
fiona_web/
├── app.py                  ← Die Haupt-Web-Anwendung (Flask)
├── review.py               ← Reviewlogik für Learnlog
├── templates/              ← HTML-Templates für die Webanwendung
│   ├── index.html
│   ├── review.html
│   └── suggestions.html
├── static/                 ← (Optional) Statische Dateien wie CSS, JS, etc.
├── __init__.py             ← Initialisierungsdatei für das Webmodul
```

## 🚀 Installation

1. **Python 3.8+** installieren (falls noch nicht geschehen).
2. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Flask-Server starten**:
   ```bash
   python web/app.py
   ```
   oder
   **CLI starten** (Für Entwickler):
   ```bash
   python Interface_cli/cli_main.py
   ```

4. Gehe auf [http://127.0.0.1:5000/](http://127.0.0.1:5000/) im Browser, um die Web-App zu testen.

## 🧠 Funktionsweise

- **Ethische Prüfung**: FIONA validiert den ethischen Kern, bevor sie auf Benutzeranfragen reagiert.
- **Antwortlogik**: Mini-FIONA nutzt eine Transformer-basierte Architektur (GPT-ähnlich), die mit Regeln und ethischen Entscheidungen kombiniert wird.
- **Review und Vorschläge**: Verwaltung von „unreviewed“ Fragen und Regelvorschlägen, die durch die Benutzer überprüft werden können.

## 🛠 Wichtige Dateien

- **`app.py`**: Hauptdatei für den Flask-Server und das Routing.
- **`review.py`**: Logik zur Verwaltung und Überprüfung von Fragen im Learnlog.
- **`templates/`**: HTML-Templates für die Benutzeroberfläche.
- **`suggested_rules.json`**: JSON-Datei mit Regelvorschlägen, die überprüft und angenommen/abgelehnt werden können.

## ⚙️ Training und Modell

1. **Tokenizer trainieren**:  
   Um den BPE-Tokenizer zu trainieren, führe das Skript aus:
   ```bash
   python train_tokenizer.py
   ```

2. **Modell trainieren**:  
   Um das Sprachmodell zu trainieren, verwende das Trainer-Skript:
   ```bash
   python trainer.py
   ```

3. **Modell evaluieren**:  
   Nach dem Training kannst du das Modell evaluieren, indem du:
   ```bash
   python evaluate_model.py
   ```

## 📚 Weitere Funktionen

- **Ethik-Regeln**: Während der Interaktion kann FIONA Vorschläge für ethische Regeln annehmen oder ablehnen. Die Regeln können durch das Web-Interface überprüft werden.
- **Kontextspeicher**: FIONA merkt sich die letzten Eingaben und Entscheidungen, um kontinuierlich auf die Ethikprüfung zu reagieren.

## 📝 Lizenz

Mini-FIONA ist ein **Open-Source-Projekt** unter der **GNU-Lizenz**.  
Siehe [LICENSE](LICENSE) für weitere Details.
# FIONA
