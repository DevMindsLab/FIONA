import json
import hashlib
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[FIONA][EthicsLink] %(message)s')

# Speicherort der Ethikdaten
ETHICS_PATH = Path(__file__).resolve().parent / "core_ethics.json"
ETHICS_HASH_PATH = Path(__file__).resolve().parent / "core_ethics.hash"

def load_ethics():
    if not ETHICS_PATH.exists():
        logging.warning("Ethics core file not found.")
        return None
    with open(ETHICS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        logging.info("Ethics core loaded successfully.")
        return data

def compute_ethics_hash():
    if not ETHICS_PATH.exists():
        logging.warning("Cannot compute hash: ethics core file missing.")
        return None
    content = ETHICS_PATH.read_bytes()
    hash_val = hashlib.sha256(content).hexdigest()
    logging.info(f"Computed current ethics hash: {hash_val}")
    return hash_val

def check_ethics_validity():
    current_hash = compute_ethics_hash()
    if not current_hash or not ETHICS_HASH_PATH.exists():
        logging.warning("Missing ethics core or hash file.")
        return False, "Ethics core or hash file missing."

    with open(ETHICS_HASH_PATH, "r") as f:
        saved_hash = f.read().strip()

    if current_hash != saved_hash:
        logging.error("Ethics core hash mismatch!")
        return False, "Hash mismatch. Ethics core may have been tampered with."

    logging.info("Ethics core validated successfully.")
    return True, "Ethics core valid."

def update_ethics_hash():
    current_hash = compute_ethics_hash()
    if current_hash:
        with open(ETHICS_HASH_PATH, "w") as f:
            f.write(current_hash)
        logging.info("Ethics hash file updated successfully.")
        return True
    return False

if __name__ == "__main__":
    valid, message = check_ethics_validity()
    print(f"\nValidation: {message}")
    if not valid:
        choice = input("Update hash file with current core? (y/n): ").strip().lower()
        if choice == "y":
            success = update_ethics_hash()
            print("✅ Hash updated." if success else "❌ Failed to update hash.")
