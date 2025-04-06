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