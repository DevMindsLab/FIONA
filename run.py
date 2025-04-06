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
ist das Hauptskript, das das FIONA-System startet. Es initialisiert die Anwendung,
lädt alle erforderlichen Module und startet den Webserver oder andere erforderliche Prozesse.
Dieses Skript dient als Einstiegspunkt für die Ausführung der gesamten Anwendung und stellt sicher,
dass alle Komponenten korrekt ausgeführt werden.

Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

# run.py – Starte FIONA mit korrektem Importpfad

import os
import subprocess
import sys
from pathlib import Path

# Projekt-Root ermitteln und setzen
project_root = Path(__file__).resolve().parent
os.chdir(project_root)  # Wichtig für Flask & Templates

# Sicherheitshalber Projekt-Root zum sys.path hinzufügen
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# App starten über Modul
subprocess.run([sys.executable, "-m", "app"])