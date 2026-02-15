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
        self.title("Cat's CursorVIP 1.X Auto-Pwner + Update Killer 😼💥🛡️")
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
            "high_quota": False,
            "lifetime": False,
            "telemetry_off": False,
            "machine_id_ok": False,
            "updates_blocked": False,  # now tracked
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

        ttk.Label(frame, text="🐱 Cat's CursorVIP Auto-Pwner + Eternal Update Block 😼🔥🛑", style="Header.TLabel").pack(pady=(0, 15))

        self.log = scrolledtext.ScrolledText(
            frame, font=("Consolas", 12), bg="#161b22", fg="#c0c0ff",
            insertbackground="#ff69b4", height=24, wrap=tk.WORD
        )
        self.log.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=12)

        self.pwn_btn = ttk.Button(btn_frame, text="PWN TO VIP + KILL UPDATES FOREVER 💥🛡️", style="BigButton.TButton", command=self.pwn_cursor)
        self.pwn_btn.pack(side=tk.LEFT, padx=10)

        ttk.Button(btn_frame, text="SCAN & RE-ENFORCE 🐾", command=self.scan).pack(side=tk.LEFT, padx=10)

        ttk.Button(btn_frame, text="COPY LOG 📋", command=self.copy_log).pack(side=tk.LEFT, padx=10)

        self.verdict_label = ttk.Label(frame, text="Waiting for scan nya~", font=("Consolas", 14, "bold"), foreground="#ff69b4")
        self.verdict_label.pack(pady=12)

    def log_msg(self, msg, color="#c0c0ff"):
        tag = f"tag_{random.randint(1000,9999)}"
        self.log.tag_configure(tag, foreground=color)
        ts = datetime.now().strftime("%H:%M:%S")
        self.log.insert(tk.END, f"[{ts}] {msg}\n", tag)
        self.log.see(tk.END)

    def _enforce_no_updates(self):
        """Silently force-disable updates in settings.json & storage.json"""
        self.log_msg("🛡️ Auto-enforcing update blockade...", "#ff69b4")

        settings_path = self.base_path / "settings.json"

        anti_update = {
            "update.mode": "none",
            "update.enableWindowsBackgroundUpdates": False,
            "update.autoCheck": False,
            "update.channel": "none",
            "extensions.autoUpdate": False,
            "update.showReleaseNotes": False,
        }

        sdata = {}
        modified = False
        if settings_path.exists():
            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    sdata = json.load(f)
            except:
                pass

        for k, v in anti_update.items():
            if sdata.get(k) != v:
                sdata[k] = v
                modified = True

        if modified or not settings_path.exists():
            try:
                with open(settings_path, "w", encoding="utf-8") as f:
                    json.dump(sdata, f, indent=2)
                self.log_msg("→ settings.json → update.mode = none + full lockdown 🛑", "#88ff88")
                self.status["updates_blocked"] = True
            except Exception as e:
                self.log_msg(f"[FAIL] settings write error: {e}", "#ff4444")
        else:
            self.log_msg("→ settings.json already locked (good kitten)", "#aaffaa")

        # storage.json extra tricks
        storage_dir = self.base_path / "User" / "globalStorage"
        storage_dir.mkdir(parents=True, exist_ok=True)
        storage_path = storage_dir / "storage.json"

        extra = {
            "update.lastCheck": "2099-12-31T23:59:59.999Z",
            "extensions.lastUpdateCheck": "2099-12-31T23:59:59.999Z",
        }

        sdata2 = {}
        if storage_path.exists():
            try:
                with open(storage_path, "r", encoding="utf-8") as f:
                    sdata2 = json.load(f)
            except:
                pass

        sdata2.update(extra)
        try:
            with open(storage_path, "w", encoding="utf-8") as f:
                json.dump(sdata2, f, indent=2)
            self.log_msg("→ storage.json → fake future timestamps (no more checks)", "#88ff88")
        except:
            pass

    def scan(self):
        self.log.delete("1.0", tk.END)
        self.log_msg("🔍 Scanning Cursor + checking update block... nya~", "#ff69b4")

        if not self.base_path or not self.base_path.exists():
            self.log_msg("❌ Cursor not found! Install first meow~", "#ff4444")
            self.verdict_label.config(text="NO CURSOR DETECTED 😿", foreground="#ff4444")
            return

        self.status["installed"] = True
        self.log_msg(f"[OK] Cursor found → {self.base_path}", "#88ff88")

        # settings.json checks
        settings_path = self.base_path / "settings.json"
        if settings_path.exists():
            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if data.get("isPro") is True:
                    self.status["settings_pro"] = True
                    self.log_msg("→ isPro = True 🔥", "#ffdd00")

                if data.get("hasLifetimeAccess") is True:
                    self.status["lifetime"] = True
                    self.log_msg("→ LIFETIME KING 👑", "#ff69b4")

                # update block check
                if data.get("update.mode") == "none" and \
                   data.get("extensions.autoUpdate") is False:
                    self.status["updates_blocked"] = True
                    self.log_msg("→ Update block ACTIVE (mode=none)", "#88ff88")
                else:
                    self.log_msg("→ Update block MISSING — will be forced on pwn", "#ffaa00")

            except Exception as e:
                self.log_msg(f"[ERR] settings.json: {e}", "#ff6666")

        # storage.json (quota + ids)
        storage_path = self.base_path / "User" / "globalStorage" / "storage.json"
        if not storage_path.exists():
            storage_path = self.base_path / "storage.json"

        if storage_path.exists():
            try:
                with open(storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if any(k in data for k in ["telemetry.machineId", "telemetry.macMachineId"]):
                    self.status["machine_id_ok"] = True
                    self.log_msg("→ Machine IDs ok", "#aaffaa")

                if data.get("telemetryLevel") == "off":
                    self.status["telemetry_off"] = True
                    self.log_msg("→ Telemetry OFF based", "#88ff88")

                quota = data.get("monthlyFastRequestLimit", 0)
                if quota > 500_000:
                    self.status["high_quota"] = True
                    self.log_msg(f"→ GOD QUOTA: {quota}", "#ff69b4")

            except Exception as e:
                self.log_msg(f"[ERR] storage.json: {e}", "#ff6666")

        self._show_verdict()

    def _show_verdict(self):
        points = sum([
            10 if self.status["installed"] else 0,
            30 if self.status["settings_pro"] else 0,
            25 if self.status["high_quota"] else 0,
            40 if self.status["lifetime"] else 0,
            15 if self.status["telemetry_off"] else 0,
            10 if self.status["machine_id_ok"] else 0,
            30 if self.status["updates_blocked"] else 0,   # heavier weight now
        ])

        self.log_msg("\n" + "═" * 60, "#555577")
        self.log_msg("     CAT'S FINAL VERDICT NYA~", "#ff69b4")
        self.log_msg("═" * 60, "#555577")

        if points >= 120:
            v = "GODMODE VIP + UPDATES PERMA-DEAD 😼👑🛑"
            c = "#ff1493"
            emoji = "NYAAA~ LOCKED & LOADED!"
        elif points >= 80:
            v = "SEMI-VIP — updates will be slain on next pwn"
            c = "#ffaa00"
            emoji = "≈ PRO"
        else:
            v = "FREE TIER TRASH 😿"
            c = "#ff4444"
            emoji = "PAW Patrol"

        self.log_msg(f" → {emoji}  {v}", color=c)
        self.log_msg(f"   Score: {points}/160", color=c)
        self.verdict_label.config(text=v, foreground=c)

    def pwn_cursor(self):
        if not self.base_path or not self.base_path.exists():
            messagebox.showerror("Error", "No Cursor folder nya~ Install first!")
            return

        if not messagebox.askyesno("DANGER ZONE", "PWN → VIP + PERMANENTLY DISABLE UPDATES?\nFiles overwritten. IDs spoofed. Updates murdered.\nBackup if soft kitten~"):
            return

        self.log_msg("\n💥 FULL PWN + UPDATE EXTERMINATION STARTED...", "#ff1493")

        # ── storage.json ── VIP + telemetry + quota + fake update stamps
        storage_dir = self.base_path / "User" / "globalStorage"
        storage_dir.mkdir(parents=True, exist_ok=True)
        storage_path = storage_dir / "storage.json"

        new_data = {
            "telemetry.machineId": str(uuid.uuid4()),
            "telemetry.macMachineId": ':'.join(f"{random.randint(0,255):02x}" for _ in range(6)).upper(),
            "telemetry.devDeviceId": str(uuid.uuid4()),
            "telemetry.sqmId": "{" + str(uuid.uuid4()) + "}",
            "monthlyFastRequestLimit": 999_999_999,
            "monthlyFastRequestsUsed": 0,
            "enableTelemetry": False,
            "telemetryLevel": "off",
            "update.lastCheck": "2099-12-31T23:59:59.999Z",
            "extensions.lastUpdateCheck": "2099-12-31T23:59:59.999Z",
        }

        data = {}
        if storage_path.exists():
            try:
                with open(storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except:
                pass
        data.update(new_data)

        with open(storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        self.log_msg("→ storage.json → VIP quota + IDs + future timestamps", "#ffdd00")

        # ── settings.json ── PRO + anti-update
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
        self.log_msg("→ settings.json → FULL PRO injected", "#ffdd00")

        # Now enforce update death
        self._enforce_no_updates()

        # Nuke caches
        for folder in ["Cache", "CachedData", "CachedExtensions", "Code Cache", "GPUCache"]:
            p = self.base_path / folder
            if p.exists():
                try:
                    shutil.rmtree(p)
                    self.log_msg(f"→ Nuked {folder}", "#88ff88")
                except:
                    pass

        self.log_msg("\nPWN + UPDATE MURDER COMPLETE — relaunching Cursor... 😼✨", "#ff69b4")

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

        self.after(2500, self.scan)

    def copy_log(self):
        text = self.log.get("1.0", tk.END).strip()
        self.clipboard_clear()
        self.clipboard_append(text)
        self.log_msg("Log copied nya~ 📋", "#88ff88")


if __name__ == "__main__":
    app = CatsCursorVIP_Pwner()
    app.mainloop()
