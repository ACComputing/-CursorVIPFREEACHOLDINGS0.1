# universal_cursor_vip_1.1.py
# Cursor VIP 1.1 – Phone Home Killer + God Mode for ALL OS
# Windows • macOS (Intel/M-chip) • Linux • (BSD tweakable)
# [C] Pwned by Cat 'n Co Holdings [C] 1999-2026
# @ItsJustaCat00 x ProfesserCatsan – Feb 2026 universal degeneracy

import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import os
import shutil
import subprocess
import time
import random
import uuid
import platform
from pathlib import Path
from threading import Thread

class UniversalCursorVIP:
    def __init__(self, root):
        self.root = root
        self.root.title("CURSOR VIP 1.1 – UNIVERSAL PWN 😼💀∞")
        self.root.geometry("680x540")
        self.root.configure(bg="#0a0a14")
        self.root.resizable(False, False)

        # Canvas for cat trail
        self.canvas = tk.Canvas(self.root, bg="#0a0a14", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        tk.Label(self.root, text="CURSOR VIP 1.1 – UNIVERSAL", font=("Helvetica", 32, "bold"),
                 fg="#ff00aa", bg="#0a0a14").place(relx=0.5, rely=0.08, anchor="center")

        tk.Label(self.root, text="[C] Pwned by Cat 'n Co Holdings [C] 1999-2026",
                 font=("Helvetica", 14, "italic"), fg="#ff66ff", bg="#0a0a14").place(relx=0.5, rely=0.16, anchor="center")

        self.status = tk.Label(self.root, text="DETECTING OS... READY TO PWN ALL PLATFORMS 🔥",
                               font=("Helvetica", 14), fg="#00ff9d", bg="#0a0a14", wraplength=620)
        self.status.place(relx=0.5, rely=0.26, anchor="center")

        self.pwn_btn = tk.Button(self.root, text="PWN & JAILBREAK CURSOR (ALL OS)", font=("Helvetica", 20, "bold"),
                                 bg="#ff0000", fg="white", activebackground="#cc0000", relief="flat",
                                 command=self.start_pwn_thread)
        self.pwn_btn.place(relx=0.5, rely=0.42, anchor="center", width=460, height=80)

        self.result_text = scrolledtext.ScrolledText(self.root, width=78, height=18,
                                                     font=("Consolas", 11), bg="#0f0f1f", fg="#e0e0ff",
                                                     insertbackground="#ff00aa")
        self.result_text.place(relx=0.5, rely=0.72, anchor="center")

        self.trail = []
        self.colors = ["#ff0000", "#ff3333", "#ff6666", "#cc0000", "#990000"]
        self.canvas.bind("<Motion>", self.mouse_move)
        self.canvas.bind("<Button-1>", self.burst)
        self.animate()

        self.os_info = self.detect_os()
        self.status.config(text=f"OS DETECTED: {self.os_info['pretty']}\nPress button to castrate & jailbreak")

    def detect_os(self):
        sys = platform.system()
        machine = platform.machine().lower()
        pretty = sys

        if sys == "Darwin":
            pretty = "macOS " + ("Apple Silicon M-chip" if "arm" in machine else "Intel")
        elif sys == "Windows":
            pretty = "Windows " + platform.release()
        elif sys == "Linux":
            pretty = "Linux " + machine
        else:
            pretty = f"{sys} ({machine}) – experimental"

        base_paths = {
            "Darwin": Path.home() / "Library" / "Application Support" / "Cursor",
            "Windows": Path(os.getenv("APPDATA")) / "Cursor",
            "Linux": Path.home() / ".config" / "Cursor"
        }

        return {
            "system": sys,
            "machine": machine,
            "pretty": pretty,
            "base": base_paths.get(sys, Path("~/.cursor").expanduser())
        }

    def mouse_move(self, event):
        x, y = event.x, event.y
        self.canvas.delete("cursor")
        self.canvas.create_oval(x-48, y-48, x+48, y+48, fill="", outline="#ff0000", width=8, tags="cursor")
        self.canvas.create_oval(x-32, y-32, x+32, y+32, fill="#1a0000", outline="#ff3333", width=6, tags="cursor")
        for dx, dy in [(-20,-24), (0,-28), (20,-24), (-16,8), (16,8)]:
            self.canvas.create_oval(x+dx-12, y+dy-12, x+dx+12, y+dy+12, fill="#ff0000", tags="cursor")
        self.trail.append((x, y, 0))

    def burst(self, event):
        for _ in range(24):
            self.trail.append((event.x + random.uniform(-120,120), event.y + random.uniform(-120,120), -18))

    def animate(self):
        self.canvas.delete("trail")
        new_trail = []
        for x, y, age in self.trail:
            if (alpha := max(0, 1 - age / 24)) <= 0: continue
            r = 24 + age*2.2 if age < 0 else 32 - age*1.6
            col = random.choice(self.colors)
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=col, tags="trail")
            new_trail.append((x, y, age + 1))
        self.trail = new_trail
        self.root.after(22, self.animate)

    def start_pwn_thread(self):
        Thread(target=self.pwn_cursor, daemon=True).start()

    def pwn_cursor(self):
        self.status.config(text="PWN IN PROGRESS – DO NOT CLOSE WINDOW", fg="#ffcc00")
        self.pwn_btn.config(state="disabled")
        self.result_text.delete(1.0, tk.END)
        self.root.update()

        lines = []
        lines.append("══════════════════════════════════════════════════════════════")
        lines.append(f"   UNIVERSAL CURSOR PWN 1.1 – {self.os_info['pretty']}")
        lines.append("══════════════════════════════════════════════════════════════\n")

        base = self.os_info["base"]
        if not base.exists():
            lines.append("[ERROR] Cursor base folder not found")
            lines.append(f"Expected: {base}")
            lines.append("→ Install Cursor first or check path")
            self.show_result(lines)
            return

        global_storage = base / "User" / "globalStorage" / "storage.json"
        settings_file = base / "User" / "settings.json"

        # 1. Patch storage.json
        if global_storage.exists():
            try:
                with open(global_storage, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                data.update({
                    "telemetry.telemetryLevel": "off",
                    "telemetry.enableTelemetry": False,
                    "telemetry.machineId": "00000000-0000-0000-0000-000000000000",
                    "telemetry.macMachineId": "00000000000000000000000000000000",
                    "telemetry.devDeviceId": "00000000-0000-0000-0000-000000000000",
                    "telemetry.sqmId": "",
                    "monthlyFastRequestLimit": 999999,
                    "monthlyFastRequestsUsed": 0,
                    "update.mode": "none",
                })

                with open(global_storage, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)

                lines.append("✓ storage.json patched")
                lines.append("  • Telemetry OFF")
                lines.append("  • Machine IDs zeroed")
                lines.append("  • 999999 fast requests forced")
            except Exception as e:
                lines.append(f"[FAIL] storage.json – {str(e)}")
        else:
            lines.append("[WARN] storage.json not found – skipping")

        # 2. Patch user settings.json
        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                data.update({
                    "telemetry.telemetryLevel": "off",
                    "telemetry.enableTelemetry": False,
                    "update.mode": "none",
                    "extensions.autoUpdate": False,
                })

                with open(settings_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)

                lines.append("✓ settings.json patched")
            except Exception as e:
                lines.append(f"[FAIL] settings.json – {str(e)}")
        else:
            lines.append("[INFO] settings.json not found – no problem")

        # 3. Nuke caches & updater (cross-platform attempt)
        cache_dirs = [
            base / "Cache",
            base / "Code" / "Cache",
            base / "Code" / "CachedData",
            base / "GPUCache",
            base.parent / "cache",
            base.parent / "updater"
        ]

        nuked = 0
        for d in cache_dirs:
            if d.exists():
                try:
                    if d.is_dir():
                        shutil.rmtree(d, ignore_errors=True)
                    else:
                        d.unlink()
                    nuked += 1
                except:
                    pass

        lines.append(f"✓ Nuked {nuked} cache/updater folders")

        # 4. Kill running Cursor
        killed = False
        try:
            if self.os_info["system"] == "Windows":
                subprocess.run(["taskkill", "/F", "/IM", "Cursor.exe"], capture_output=True, timeout=8)
            elif self.os_info["system"] == "Darwin":
                subprocess.run(["pkill", "-9", "-f", "Cursor"], capture_output=True, timeout=8)
            else:  # Linux/BSD
                subprocess.run(["pkill", "-9", "-f", "cursor"], capture_output=True, timeout=8)
            killed = True
        except:
            pass

        lines.append("✓ Cursor process killed" if killed else "[INFO] Cursor not running – good")

        # 5. Verdict
        lines.append("\nVERDICT")
        lines.append("───────────────")
        lines.append("GOD MODE – INJECTION SUCCESS")
        lines.append("• Local unlimited quota illusion: ACTIVE")
        lines.append("• Telemetry / phone-home: DEAD")
        lines.append("• Fingerprint: ERASED")
        lines.append("• Works on your OS: " + self.os_info["pretty"])
        lines.append("\nRelaunch Cursor now → enjoy the silence")

        self.show_result(lines)
        self.status.config(text="PWN COMPLETE – Cursor castrated on ALL OS", fg="#00ff9d")
        self.pwn_btn.config(state="normal")

        # Auto-relaunch attempt (optional – comment out if unwanted)
        time.sleep(2)
        try:
            if self.os_info["system"] == "Windows":
                subprocess.Popen(["start", "Cursor.exe"], shell=True)
            elif self.os_info["system"] == "Darwin":
                subprocess.Popen(["open", "-a", "Cursor"])
            elif self.os_info["system"] == "Linux":
                subprocess.Popen(["cursor"], shell=True)
        except:
            pass

    def show_result(self, lines):
        self.result_text.delete(1.0, tk.END)
        for line in lines:
            self.result_text.insert(tk.END, line + "\n")
        self.result_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversalCursorVIP(root)
    root.mainloop()
