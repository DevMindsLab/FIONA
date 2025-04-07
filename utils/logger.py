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
Der Logger dient der zentralen Verwaltung und Speicherung von Log-Nachrichten in einer rotierenden Datei.
Er ermöglicht das Loggen von Nachrichten mit verschiedenen Schweregraden (INFO, DEBUG, ERROR),
speichert Logs in einer Datei und archiviert ältere Dateien automatisch, wenn die Größe überschritten wird.

Wichtige Hinweise:
------------------
- Diese Datei ist ein Bestandteil des gesamten FIONA-Systems und sollte nicht isoliert verwendet werden.
- Achte darauf, alle Änderungen gründlich zu testen, da das System stark auf ethische Validierungen angewiesen ist.
- Weitere Dokumentation findest du in der `README.md` und der `DEV_README.md`.

"""

import logging
from logging.handlers import RotatingFileHandler
import os
import re

class Logger:
    def __init__(self, log_file="system.log", max_bytes=100*1024*1024, backup_count=5):
        """
        Initialisiere den Logger.
        :param log_file: Name der Log-Datei
        :param max_bytes: Maximale Größe der Log-Datei bevor sie rotiert wird
        :param backup_count: Anzahl der Backups der alten Log-Datei
        """
        log_dir = os.path.join(os.path.dirname(__file__), "../logs")  # Verzeichnis für Logs
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)  # Erstelle das Verzeichnis, falls es nicht existiert

        log_file_path = os.path.join(log_dir, log_file)  # Vollständiger Pfad zur Log-Datei

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)  # Setze das Log-Level auf INFO

        # Erstelle Handler für das Loggen in eine Datei mit Rotation
        handler = RotatingFileHandler(log_file_path, maxBytes=max_bytes, backupCount=backup_count)
        handler.setLevel(logging.INFO)

        # Definiere das Format der Log-Nachricht
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(filename)s][%(funcName)s] %(message)s')
        handler.setFormatter(formatter)

        # Füge den Handler zum Logger hinzu
        self.logger.addHandler(handler)

    def remove_ansi_escape_sequences(self, text: str) -> str:
        """
        Entfernt ANSI Escape Codes für Farben und Formatierungen aus dem Text.
        :param text: Der Text, aus dem die Escape-Sequenzen entfernt werden sollen.
        :return: Der bereinigte Text ohne Escape-Sequenzen.
        """
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        return ansi_escape.sub('', text)

    def log(self, message: str, level: str = "INFO", *args, **kwargs):
        """
        Loggt eine Nachricht mit dem angegebenen Log-Level.
        :param message: Die zu loggende Nachricht
        :param level: Das Log-Level (z.B. "INFO", "ERROR", "DEBUG", "WARNING")
        """
        message = self.remove_ansi_escape_sequences(message)  # Entferne Escape-Sequenzen aus der Nachricht
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
