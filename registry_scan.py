import winreg
from utils import load_keywords, load_excludes

KEYWORDS = load_keywords()
EXCLUDES = load_excludes()

RUN_KEYS = [
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run")
]

def scan_run_keys():
    results = []

    for hive, path in RUN_KEYS:
        try:
            key = winreg.OpenKey(hive, path)
        except:
            continue

        i = 0
        while True:
            try:
                name, value, _ = winreg.EnumValue(key, i)
                i += 1

                v = str(value).lower()

                if any(k in v for k in KEYWORDS):
                    if not any(e in v for e in EXCLUDES):
                        results.append({
                            "key": name,
                            "value": value,
                            "location": path
                        })
            except:
                break

    return results
