# cursor_injection_checker.py
# Standalone Cursor VIP Injection Status Checker
# Shows quota, telemetry, machine IDs + verdict
# [C] Pwned by Cat 'n Co Holdings [C] 1999-2026
# @ItsJustaCat00 x ProfesserCatsan – Feb 2026

import tkinter as tk
from tkinter import scrolledtext
import json
from pathlib import Path
import os
import time
import platform

class CursorChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("CURSOR INJECTION CHECKER 😼🔍")
        self.root.geometry("680x520")
        self.root.configure(bg="#0a0a14")
        self.root.resizable(False, False)

        tk.Label(root, text="CURSOR VIP STATUS CHECK", font=("Helvetica", 28, "bold"),
                 fg="#ff00aa", bg="#0a0a14").pack(pady=20)

        tk.Label(root, text="[C] Pwned by Cat 'n Co Holdings [C] 1999-2026",
                 font=("Helvetica", 12, "italic"), fg="#ff66ff", bg="#0a0a14").pack(pady=6)

        self.status = tk.Label(root, text="Press CHECK to scan Cursor install",
                               font=("Helvetica", 14), fg="#00ff9d", bg="#0a0a14")
        self.status.pack(pady=10)

        self.btn = tk.Button(root, text="CHECK INJECTION", font=("Helvetica", 18, "bold"),
                             bg="#ff00aa", fg="white", command=self.run_check)
        self.btn.pack(pady=20)

        self.text = scrolledtext.ScrolledText(root, width=78, height=18,
                                              font=("Consolas", 11), bg="#0f0f1f", fg="#e0e0ff",
                                              insertbackground="#ff00aa")
        self.text.pack(padx=20, pady=10, fill="both", expand=True)

        self.footer = tk.Label(root, text="Close Cursor first for clean read • Works on macOS/Windows/Linux",
                               font=("Helvetica", 10), fg="#8888aa", bg="#0a0a14")
        self.footer.pack(pady=8)

    def run_check(self):
        self.text.delete(1.0, tk.END)
        self.status.config(text="Scanning...", fg="#ffcc00")
        self.root.update()
        time.sleep(0.5)

        lines = []
        lines.append("══════════════════════════════════════════════════════════════")
        lines.append("      CURSOR INJECTION CHECK – GOD MODE SCAN 2026       ")
        lines.append("══════════════════════════════════════════════════════════════\n")

        sys = platform.system()
        lines.append(f"OS Detected: {sys} {platform.machine()}")

        # Try common Cursor paths
        possible_paths = []
        if sys == "Darwin":
            possible_paths.append(Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage" / "storage.json")
        elif sys == "Windows":
            possible_paths.append(Path(os.getenv("APPDATA")) / "Cursor" / "User" / "globalStorage" / "storage.json")
        elif sys == "Linux":
            possible_paths.append(Path.home() / ".config" / "Cursor" / "User" / "globalStorage" / "storage.json")

        storage_path = None
        for p in possible_paths:
            if p.exists():
                storage_path = p
                break

        if not storage_path:
            lines.append("[ERROR] storage.json not found")
            lines.append("→ Cursor not installed or path changed")
            lines.append("Tried:")
            for p in possible_paths:
                lines.append(f"  • {p}")
            self.show(lines)
            return

        lines.append(f"Found: {storage_path}")
        lines.append(f"Last modified: {time.ctime(os.path.getmtime(storage_path))}\n")

        try:
            with open(storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Core keys
            telemetry_keys = [
                ("telemetry.machineId", data.get("telemetry.machineId", "NOT FOUND")),
                ("telemetry.macMachineId", data.get("telemetry.macMachineId", "NOT FOUND")),
                ("telemetry.devDeviceId", data.get("telemetry.devDeviceId", "NOT FOUND")),
                ("telemetry.telemetryLevel", data.get("telemetry.telemetryLevel", "NOT SET")),
                ("telemetry.enableTelemetry", data.get("telemetry.enableTelemetry", "NOT SET")),
            ]

            quota_keys = [
                ("monthlyFastRequestLimit", data.get("monthlyFastRequestLimit", "NOT FOUND")),
                ("monthlyFastRequestsUsed", data.get("monthlyFastRequestsUsed", "NOT FOUND")),
            ]

            lines.append("TELEMETRY STATUS")
            lines.append("──────────────────────────")
            for k, v in telemetry_keys:
                lines.append(f"{k:22} : {v}")

            lines.append("\nQUOTA STATUS")
            lines.append("──────────────────────────")
            for k, v in quota_keys:
                lines.append(f"{k:22} : {v}")

            # Verdict
            lines.append("\nVERDICT")
            lines.append("───────────────")

            god = True
            msgs = []

            if quota_keys[0][1] == 999999 and quota_keys[1][1] == 0:
                msgs.append("999999 LIMIT PATCH ✓ (local unlimited illusion active)")
            else:
                god = False
                msgs.append("No 999999 quota patch detected")

            if telemetry_keys[3][1] == "off" and telemetry_keys[4][1] is False:
                msgs.append("TELEMETRY DISABLED ✓ (phone-home castrated)")
            else:
                god = False
                msgs.append("Telemetry still active / not fully off")

            machine_id = telemetry_keys[0][1]
            if machine_id in ["00000000-0000-0000-0000-000000000000", "NOT FOUND"] or len(str(machine_id)) < 8:
                msgs.append("Machine IDs zeroed / blanked ✓ (fingerprint killed)")
            else:
                god = False
                msgs.append(f"Machine ID still present: {str(machine_id)[:8]}...")

            for msg in msgs:
                lines.append("→ " + msg)

            lines.append("\nOVERALL: " + ("** GOD MODE – INJECTION WORKING **" if god else "Partial / Injection incomplete"))

        except Exception as e:
            lines.append(f"[CRITICAL] Read error: {str(e)}")
            lines.append("→ File corrupted?")

        self.show(lines)

    def show(self, lines):
        self.text.delete(1.0, tk.END)
        for line in lines:
            self.text.insert(tk.END, line + "\n")
        self.text.see(tk.END)

        self.status.config(
            text="SCAN COMPLETE – check below",
            fg="#00ff9d" if "GOD MODE" in lines[-1] else "#ffaa00"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = CursorChecker(root)
    root.mainloop()
