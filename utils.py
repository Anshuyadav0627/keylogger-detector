import os
import json
import logging
from pathlib import Path

ROOT = Path(__file__).parent
CONFIG_DIR = ROOT / "config"
LOG_DIR = ROOT / "logs"
OUTPUT_DIR = ROOT / "output"

LOG_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=str(LOG_DIR / "scan_log.txt"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def load_keywords():
    path = CONFIG_DIR / "suspicious_keywords.txt"
    if not path.exists():
        return []
    return [l.strip().lower() for l in path.read_text().splitlines() if l.strip()]

def load_excludes():
    path = CONFIG_DIR / "exclude_list.txt"
    if not path.exists():
        return []
    return [l.strip().lower() for l in path.read_text().splitlines() if l.strip()]

def load_paths():
    path = CONFIG_DIR / "paths.json"
    if not path.exists():
        return []
    raw = json.loads(path.read_text()).get("scan_paths", [])
    return [os.path.expandvars(p) for p in raw]
