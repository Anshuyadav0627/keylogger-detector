import psutil
from utils import load_excludes

EXCLUDES = load_excludes()

def is_excluded(p):
    if not p:
        return False
    p = p.lower()
    return any(e in p for e in EXCLUDES)

def scan_connections():
    results = []

    for conn in psutil.net_connections(kind="inet"):
        if conn.raddr and conn.pid:
            try:
                proc = psutil.Process(conn.pid)
                name = proc.name()
                path = proc.exe() or ""
            except:
                name = "UNKNOWN"
                path = ""

            if is_excluded(path):
                continue

            results.append({
                "pid": conn.pid,
                "process": name,
                "path": path,
                "remote": f"{conn.raddr.ip}:{conn.raddr.port}"
            })

    return results
