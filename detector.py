from file_scan import scan_paths
from network_scan import scan_connections
from registry_scan import scan_run_keys
from utils import load_keywords, load_excludes, OUTPUT_DIR
import psutil
import json

KEYWORDS = load_keywords()
EXCLUDES = load_excludes()

def scan_processes():
    results = []

    for p in psutil.process_iter(["pid", "name", "exe", "cmdline"]):
        try:
            name = p.info["name"] or ""
            path = p.info["exe"] or ""
            cmd = " ".join(p.info["cmdline"] or [])

            text = (name + path + cmd).lower()

            if any(k in text for k in KEYWORDS):
                if not any(e in text for e in EXCLUDES):
                    results.append({
                        "pid": p.info["pid"],
                        "name": name,
                        "path": path,
                        "cmd": cmd
                    })
        except:
            pass

    return results

def create_report(a, b, c, d):
    data = {
        "processes": a,
        "files": b,
        "registry": c,
        "network": d
    }

    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "detected_items.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Report saved in output/detected_items.json")

if __name__ == "__main__":
    print("Running Keylogger Detector...\n")

    p = scan_processes()
    f = scan_paths()
    r = scan_run_keys()
    n = scan_connections()

    create_report(p, f, r, n)

    print("\nScan complete.")
