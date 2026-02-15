import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
from pathlib import Path
import platform
import uuid
import random
import string
import shutil
import subprocess
import time
from datetime import datetime

class CatsCursorVIP_Pwner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cat's CursorVIP 1.X Checker & Pwner 😼💥")
        self.geometry("860x720")
        self.minsize(780, 620)
        self.configure(bg="#0a0e14")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#0a0e14", foreground="#a0d0ff", font=("Consolas", 11))
        self.style.configure("Header.TLabel", background="#0a0e14", foreground="#ff69b4", font=("Consolas", 18, "bold"))
        self.style.configure("BigButton.TButton", font=("Consolas", 14, "bold"), padding=12)
        self.style.map("BigButton.TButton", background=[("active", "#ff1493")], foreground=[("active", "white")])

        self.base_path = self._get_cursor_path()
        self.status = {
            "installed": False,
            "settings_pro": False,
            "storage_pro": False,
            "high_quota": False,
            "lifetime": False,
            "telemetry_off": False,
            "machine_id_ok": False,
        }

        self._build_ui()
        self.after(200, self.scan)

    def _get_cursor_path(self):
        sys = platform.system()
        home = Path.home()
        if sys == "Darwin":
            return home / "Library" / "Application Support" / "Cursor"
        elif sys == "Windows":
            return Path(os.getenv("APPDATA") or str(home / "AppData" / "Roaming")) / "Cursor"
        elif sys == "Linux":
            return home / ".config" / "Cursor"
        return None

    def _build_ui(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="🐱 Cat's CursorVIP 1.X Pwner 😼🔥", style="Header.TLabel").pack(pady=(0, 15))

        self.log = scrolledtext.ScrolledText(
            frame, font=("Consolas", 12), bg="#161b22", fg="#c0c0ff",
            insertbackground="#ff69b4", height=24, wrap=tk.WORD
        )
        self.log.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=12)

        self.pwn_btn = ttk.Button(btn_frame, text="PWN TO VIP GOD MODE 💥", style="BigButton.TButton", command=self.pwn_cursor)
        self.pwn_btn.pack(side=tk.LEFT, padx=10)

        ttk.Button(btn_frame, text="SCAN AGAIN 🐾", command=self.scan).pack(side=tk.LEFT, padx=10)

        ttk.Button(btn_frame, text="COPY LOG 📋", command=self.copy_log).pack(side=tk.LEFT, padx=10)

        self.verdict_label = ttk.Label(frame, text="Waiting for scan nya~", font=("Consolas", 14, "bold"), foreground="#ff69b4")
        self.verdict_label.pack(pady=12)

    def log_msg(self, msg, color="#c0c0ff"):
        tag = f"tag_{random.randint(1000,9999)}"
        self.log.tag_configure(tag, foreground=color)
        ts = datetime.now().strftime("%H:%M:%S")
        self.log.insert(tk.END, f"[{ts}] {msg}\n", tag)
        self.log.see(tk.END)

    def scan(self):
        self.log.delete("1.0", tk.END)
        self.log_msg("🔍 Scanning Cursor... nya~", "#ff69b4")

        if not self.base_path or not self.base_path.exists():
            self.log_msg("❌ Cursor not found! Install it first kitten~", "#ff4444")
            self.verdict_label.config(text="NO CURSOR DETECTED 😿", foreground="#ff4444")
            return

        self.status["installed"] = True
        self.log_msg(f"[OK] Cursor found → {self.base_path}", "#88ff88")

        # SETTINGS.JSON
        settings_path = self.base_path / "settings.json"
        if settings_path.exists():
            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if data.get("isPro") is True:
                    self.status["settings_pro"] = True
                    self.log_msg("→ settings.json : isPro = True 🔥", "#ffdd00")

                if data.get("subscriptionStatus") == "active":
                    self.log_msg("→ subscriptionStatus = active", "#ffdd00")

                if data.get("subscriptionTier") in ("pro", "lifetime"):
                    self.log_msg(f"→ subscriptionTier = {data.get('subscriptionTier')}", "#ffdd00")

                if data.get("hasLifetimeAccess") is True:
                    self.status["lifetime"] = True
                    self.log_msg("→ LIFETIME ACCESS KING 👑", "#ff69b4")

            except Exception as e:
                self.log_msg(f"[ERR] settings.json read fail: {e}", "#ff6666")

        # STORAGE.JSON
        storage_path = self.base_path / "User" / "globalStorage" / "storage.json"
        if not storage_path.exists():
            storage_path = self.base_path / "storage.json"  # fallback

        if storage_path.exists():
            try:
                with open(storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if any(k in data for k in ["telemetry.machineId", "telemetry.macMachineId", "telemetry.devDeviceId"]):
                    self.status["machine_id_ok"] = True
                    self.log_msg("→ Machine IDs present (good for spoofing later)", "#aaffaa")

                if data.get("telemetryLevel") == "off":
                    self.status["telemetry_off"] = True
                    self.log_msg("→ Telemetry OFF (based af)", "#88ff88")

                quota = data.get("monthlyFastRequestLimit", 0)
                if isinstance(quota, (int, float)) and quota > 500_000:
                    self.status["high_quota"] = True
                    self.log_msg(f"→ UNLIMITED QUOTA VIBES: {quota}", "#ff69b4")

            except Exception as e:
                self.log_msg(f"[ERR] storage.json fail: {e}", "#ff6666")

        self._show_verdict()

    def _show_verdict(self):
        points = sum([
            10 if self.status["installed"] else 0,
            30 if self.status["settings_pro"] else 0,
            25 if self.status["high_quota"] else 0,
            40 if self.status["lifetime"] else 0,
            15 if self.status["telemetry_off"] else 0,
            10 if self.status["machine_id_ok"] else 0,
        ])

        self.log_msg("\n" + "═" * 60, "#555577")
        self.log_msg("     CAT'S VERDICT TIME NYA~", "#ff69b4")
        self.log_msg("═" * 60, "#555577")

        if points >= 90:
            v = "FULL GODMODE PRO / LIFETIME 😼👑"
            c = "#ff1493"
            emoji = "NYAAA~ PWNED!"
        elif points >= 60:
            v = "SEMI-VIP — strong illusion kitten~"
            c = "#ffaa00"
            emoji = "≈ PRO"
        else:
            v = "STILL FREE / WEAK SAUCE 😿"
            c = "#ff4444"
            emoji = "FREE TIER PAW Patrol"

        self.log_msg(f" → {emoji}  {v}", color=c)
        self.log_msg(f"   Confidence: {points}/130", color=c)
        self.verdict_label.config(text=v, foreground=c)

    def pwn_cursor(self):
        if not self.base_path or not self.base_path.exists():
            messagebox.showerror("Error", "Cursor not found! Can't pwn what isn't there nya~")
            return

        if messagebox.askyesno("DANGER ZONE", "Ready to FORCE Cursor into VIP mode?\nThis will overwrite files & spoof IDs!\nBackup first if you're scared kitten~"):
            self.log_msg("\n💥 PWN SEQUENCE STARTED — hold on tight~", "#ff1493")

            # Spoof machine IDs
            storage_dir = self.base_path / "User" / "globalStorage"
            storage_dir.mkdir(parents=True, exist_ok=True)
            storage_path = storage_dir / "storage.json"

            new_ids = {
                "telemetry.machineId": str(uuid.uuid4()),
                "telemetry.macMachineId": ':'.join(f"{random.randint(0,255):02x}" for _ in range(6)).upper(),
                "telemetry.devDeviceId": str(uuid.uuid4()),
                "telemetry.sqmId": "{" + str(uuid.uuid4()) + "}",
                "monthlyFastRequestLimit": 999_999_999,
                "monthlyFastRequestsUsed": 0,
                "enableTelemetry": False,
                "telemetryLevel": "off",
            }

            data = {}
            if storage_path.exists():
                try:
                    with open(storage_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except:
                    pass

            data.update(new_ids)
            with open(storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            self.log_msg("→ storage.json pwned with god-tier IDs + unlimited quota", "#ffdd00")

            # Force settings.json PRO keys
            settings_path = self.base_path / "settings.json"
            pro_keys = {
                "isPro": True,
                "subscriptionStatus": "active",
                "subscriptionTier": "pro",
                "hasLifetimeAccess": True,
                "features": {
                    "pro": True,
                    "unlimitedContext": True,
                    "backgroundAgents": True,
                }
            }

            sdata = {}
            if settings_path.exists():
                try:
                    with open(settings_path, "r", encoding="utf-8") as f:
                        sdata = json.load(f)
                except:
                    pass

            sdata.update(pro_keys)
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump(sdata, f, indent=2)

            self.log_msg("→ settings.json injected FULL PRO KEYS 🔥", "#ffdd00")

            # Nuke some caches to force UI refresh
            for folder in ["Cache", "CachedData", "CachedExtensions", "Code Cache", "GPUCache"]:
                p = self.base_path / folder
                if p.exists():
                    try:
                        shutil.rmtree(p)
                        self.log_msg(f"→ Nuked {folder} cache", "#88ff88")
                    except:
                        pass

            self.log_msg("\nPWN COMPLETE — relaunching Cursor... 😼✨", "#ff69b4")

            # Relaunch Cursor
            sys = platform.system()
            if sys == "Darwin":
                subprocess.Popen(["open", "-a", "Cursor"])
            elif sys == "Windows":
                try:
                    subprocess.Popen(["start", "cursor"], shell=True)
                except:
                    pass
            elif sys == "Linux":
                subprocess.Popen(["cursor"])

            self.after(2000, self.scan)

    def copy_log(self):
        text = self.log.get("1.0", tk.END).strip()
        self.clipboard_clear()
        self.clipboard_append(text)
        self.log_msg("Log copied nya~ 📋", "#88ff88")


if __name__ == "__main__":
    app = CatsCursorVIP_Pwner()
    app.mainloop()