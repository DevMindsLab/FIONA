import json
import hashlib
import logging
import argparse
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='[FIONA][Validator] %(message)s')

CORE_FILE = Path(__file__).parent / "ethics_core.json"
HASH_FILE = Path(__file__).parent / "ethics_core.hash"

def calculate_hash(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()
    return hashlib.sha256(file_data).hexdigest()

def validate_ethics_core():
    if not CORE_FILE.exists() or not HASH_FILE.exists():
        return False, "Missing core file or hash file."

    actual_hash = calculate_hash(CORE_FILE)
    with open(HASH_FILE, "r") as f:
        expected_hash = f.read().strip()

    if actual_hash != expected_hash:
        return False, "Hash mismatch. Ethics core may have been tampered with."

    return True, "Ethics core is valid."

def load_ethics_core():
    with open(CORE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def show_rules(data):
    rules = data.get("rules", [])
    if not rules:
        logging.warning("No rules found in ethics_core.json")
    for rule in rules:
        rule_id = rule.get("id", "<no id>")
        description = rule.get("description", "<no description>")
        logging.info(f"- [{rule_id}] {description}")

def recalculate_hash():
    new_hash = calculate_hash(CORE_FILE)
    with open(HASH_FILE, "w") as f:
        f.write(new_hash)
    logging.info("Hash file updated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate the ethics core integrity.")
    parser.add_argument("--show-rules", action="store_true", help="Print all loaded ethics rules")
    parser.add_argument("--recalculate-hash", action="store_true", help="Recalculate and update the hash file")
    args = parser.parse_args()

    valid, message = validate_ethics_core()
    logging.info(message)

    if valid:
        data = load_ethics_core()
        if args.show_rules:
            show_rules(data)
        if args.recalculate_hash:
            recalculate_hash()
    elif args.recalculate_hash:
        recalculate_hash()
