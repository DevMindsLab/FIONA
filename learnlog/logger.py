import json
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[FIONA][Logger] %(message)s')

LOG_PATH = Path(__file__).resolve().parent / "learnlog.jsonl"

def log_question(question: str, source: str = "unknown"):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "source": source,
        "status": "unreviewed"
    }

    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        logging.info(f"Logged question from {source}: {question}")
    except Exception as e:
        logging.error(f"Failed to log question: {e}")