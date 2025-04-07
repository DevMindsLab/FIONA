"""
======================================
FIONA - Projektname

Autor: Rene Baumgarten (DevMindsLab)
Datum: 07.04.2025
Version: 0.5

Beschreibung:
---------------
Diese Python-Datei ist Teil des **FIONA**-Projekts,
einer ethisch ausgerichteten,
Open-Source-basierten Künstlichen Intelligenz (KAI). Das Projekt strebt an,
verantwortungsbewusste, nachvollziehbare und kontrollierte Entscheidungen in ethischen Dilemmata zu treffen.
Der Code in dieser Datei ist Teil des Backends, das für zentrale Log-Verwaltung zuständig ist.

Funktions Beschreibung:
---------------
Der Logger verwaltet Log-Nachrichten in einer rotierenden Datei.
Er unterstützt verschiedene Schweregrade (INFO, DEBUG, ERROR),
speichert in /logs/system.log und archiviert ältere Logs automatisch.

Wichtige Hinweise:
------------------
- Nutze die Funktion `log(...)` überall im Projekt.
- Änderungen hier betreffen das gesamte Logging-Verhalten.
"""

import logging
from logging.handlers import RotatingFileHandler
import os
import re

class Logger:
    def __init__(self, log_file="system.log", max_bytes=100*1024*1024, backup_count=5):
        log_dir = os.path.join(os.path.dirname(__file__), "../logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file_path = os.path.join(log_dir, log_file)

        self.logger = logging.getLogger("FIONA")
        self.logger.setLevel(logging.DEBUG)

        handler = RotatingFileHandler(log_file_path, maxBytes=max_bytes, backupCount=backup_count)
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(filename)s][%(funcName)s] %(message)s')
        handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def remove_ansi_escape_sequences(self, text: str) -> str:
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        return ansi_escape.sub('', text)

    def log(self, message: str, level: str = "INFO", *args, **kwargs):
        message = self.remove_ansi_escape_sequences(message)
        level = level.upper()

        if level == "DEBUG":
            self.logger.debug(message, *args, **kwargs)
        elif level == "INFO":
            self.logger.info(message, *args, **kwargs)
        elif level == "WARNING":
            self.logger.warning(message, *args, **kwargs)
        elif level == "ERROR":
            self.logger.error(message, *args, **kwargs)
        elif level == "CRITICAL":
            self.logger.critical(message, *args, **kwargs)
        else:
            self.logger.info(message, *args, **kwargs)

# === Globale Instanz & Shortcut-Funktion ===

_logger_instance = Logger()

def log(message: str, level: str = "INFO", *args, **kwargs):
    """
    Globale Log-Funktion für das gesamte Projekt.
    Importierbar mit: from utils.logger import log
    """
    try:
        _logger_instance.log(message, level, *args, **kwargs)
    except Exception as e:
        print(f"[Logger Fallback] Fehler beim Loggen: {e}")
