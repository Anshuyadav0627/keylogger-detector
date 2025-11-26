import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import subprocess, threading, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUTPUT = ROOT / "output"

def run_command(cmd, box):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
    for line in p.stdout:
        box.insert(tk.END, line)
        box.see(tk.END)

def run_scan(box):
    box.delete("1.0", tk.END)
    cmd = f'"{sys.executable}" "{ROOT / "detector.py"}"'
    threading.Thread(target=run_command, args=(cmd, box), daemon=True).start()

def show_report(box):
    rep = OUTPUT / "scan_report.txt"
    if rep.exists():
        box.delete("1.0", tk.END)
        box.insert(tk.END, rep.read_text())
    else:
        box.insert(tk.END, "Run a scan first.\n")

root = tk.Tk()
root.title("Keylogger Detector")
root.geometry("800x600")

frame = tk.Frame(root)
frame.pack(fill="x")

btn = tk.Button(frame, text="Run Scan", command=lambda: run_scan(out))
btn.pack(side="left", padx=5)

btn2 = tk.Button(frame, text="Show Report", command=lambda: show_report(out))
btn2.pack(side="left", padx=5)

out = ScrolledText(root)
out.pack(fill="both", expand=True)

root.mainloop()