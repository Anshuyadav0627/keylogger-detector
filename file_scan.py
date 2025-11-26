import os
import hashlib
import logging
from utils import load_keywords, load_excludes, load_paths

KEYWORDS = load_keywords()
EXCLUDES = load_excludes()

def is_excluded(path):
    p = path.lower()
    return any(e in p for e in EXCLUDES)

def file_hash(path):
    try:
        import hashlib
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except:
        return None

def scan_paths():
    results = []
    paths = load_paths()
    logging.info("File scan started")

    for base in paths:
        if not os.path.exists(base):
            continue

        for root, _, files in os.walk(base):
            for file in files:
                fp = os.path.join(root, file)
                lower = fp.lower()

                if is_excluded(lower):
                    continue

                suspicious = (
                    any(k in lower for k in KEYWORDS)
                    or file.lower().endswith((".exe", ".dll", ".sys", ".scr", ".bat"))
                )

                if suspicious:
                    try:
                        results.append({
                            "path": fp,
                            "size": os.path.getsize(fp),
                            "hash": file_hash(fp)
                        })
                    except:
                        pass

    return results
