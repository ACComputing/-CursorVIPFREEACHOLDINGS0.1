import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import os
from pathlib import Path
import platform
import uuid
import datetime
from typing import Optional, Dict, Any

class CursorProChecker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cursor VIP / PRO Status Checker  •  Cat's Eye Scanner v1.0")
        self.geometry("780x640")
        self.minsize(720, 580)
        self.configure(bg="#0d1117")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure("TLabel", background="#0d1117", foreground="#c9d1d9", font=("Consolas", 11))
        self.style.configure("Header.TLabel", background="#0d1117", foreground="#58a6ff", font=("Consolas", 16, "bold"))
        self.style.configure("TButton", font=("Consolas", 11), padding=8)
        self.style.map("TButton", background=[("active", "#238636")], foreground=[("active", "white")])

        self.status = {
            "found_install": False,
            "settings_pro": False,
            "storage_pro": False,
            "machine_id_exists": False,
            "telemetry_off": False,
            "quota_unlimited": False,
            "lifetime": False,
            "pro_features": False,
        }

        self._build_ui()
        self.after(100, self.scan)

    def _build_ui(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="CURSOR VIP / PRO DETECTOR", style="Header.TLabel").pack(pady=(0, 20))

        self.result_text = scrolledtext.ScrolledText(
            main_frame,
            font=("Consolas", 12),
            bg="#161b22",
            fg="#c9d1d9",
            insertbackground="white",
            height=22,
            wrap=tk.WORD
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        self.scan_btn = ttk.Button(btn_frame, text="SCAN AGAIN", command=self.scan)
        self.scan_btn.pack(side=tk.LEFT, padx=8)

        ttk.Button(btn_frame, text="Copy Report", command=self.copy_report).pack(side=tk.LEFT, padx=8)

        self.status_label = ttk.Label(main_frame, text="Ready...", foreground="#8b949e")
        self.status_label.pack(pady=6)

    def get_cursor_base_path(self) -> Optional[Path]:
        sys = platform.system()
        home = Path.home()

        if sys == "Darwin":
            return home / "Library" / "Application Support" / "Cursor"
        elif sys == "Windows":
            appdata = os.getenv("APPDATA") or str(home / "AppData" / "Roaming")
            return Path(appdata) / "Cursor"
        elif sys == "Linux":
            return home / ".config" / "Cursor"
        return None

    def scan(self):
        self.result_text.delete("1.0", tk.END)
        self.status_label.config(text="Scanning...", foreground="#ffa500")

        base = self.get_cursor_base_path()
        if not base or not base.exists():
            self._report_not_installed()
            return

        self.status["found_install"] = True
        self._log(f"[+] Cursor install found → {base}")

        # ─── SETTINGS.JSON ───────────────────────────────────────────────
        settings_path = base / "settings.json"
        if settings_path.exists():
            try:
                with open(settings_path, encoding="utf-8") as f:
                    data = json.load(f)
                
                pro_signals = 0
                
                if data.get("isPro") is True:
                    pro_signals += 3
                    self.status["settings_pro"] = True
                    self._log("  → settings.json : isPro = True")

                if data.get("subscriptionStatus") == "active":
                    pro_signals += 2
                    self._log("  → subscriptionStatus = active")

                if data.get("subscriptionTier") in ("pro", "lifetime", "vip"):
                    pro_signals += 2
                    self._log(f"  → subscriptionTier = {data['subscriptionTier']}")

                if "features" in data and data["features"].get("pro"):
                    pro_signals += 2
                    self.status["pro_features"] = True
                    self._log("  → features.pro = True")

                if data.get("hasLifetimeAccess") is True:
                    self.status["lifetime"] = True
                    pro_signals += 4
                    self._log("  → hasLifetimeAccess = True  ← lifetime king")

                if pro_signals >= 5:
                    self._log("  → SETTINGS.JSON looks VERY pro", color="#3fb950")
                elif pro_signals >= 3:
                    self._log("  → settings.json has some pro signals", color="#ffa500")
                else:
                    self._log("  → settings.json looks free / weak", color="#ff7b72")

            except Exception as e:
                self._log(f"[!] Failed to read settings.json → {e}", color="#ff7b72")

        # ─── STORAGE.JSON ────────────────────────────────────────────────
        storage_path = base / "storage.json"
        if storage_path.exists():
            try:
                with open(storage_path, encoding="utf-8") as f:
                    data = json.load(f)
                
                if "telemetry.macMachineId" in data or "telemetry.devDeviceId" in data:
                    self.status["machine_id_exists"] = True
                    self._log("  → storage.json : machine ID present")

                if data.get("telemetryLevel") == "off" or data.get("enableTelemetry") is False:
                    self.status["telemetry_off"] = True
                    self._log("  → telemetry disabled (based)")

                quota = data.get("monthlyFastRequestLimit")
                if isinstance(quota, (int, float)) and quota > 500000:
                    self.status["quota_unlimited"] = True
                    self._log(f"  → monthlyFastRequestLimit = {quota}  ← looks cracked / unlimited", color="#3fb950")

            except Exception as e:
                self._log(f"[!] Failed to read storage.json → {e}", color="#ff7b72")

        self._print_verdict()

    def _report_not_installed(self):
        self._log("Cursor installation NOT found.", color="#ff7b72")
        self._log("")
        self._log("Common locations we checked:")
        self._log("  • macOS:  ~/Library/Application Support/Cursor")
        self._log("  • Windows: %APPDATA%\\Cursor")
        self._log("  • Linux:   ~/.config/Cursor")
        self.status_label.config(text="Cursor not installed / wrong path", foreground="#ff7b72")

    def _print_verdict(self):
        self._log("\n" + "═" * 48, color="#8b949e")
        self._log("           FINAL VERDICT", color="#58a6ff")
        self._log("═" * 48, color="#8b949e")

        points = 0
        if self.status["found_install"]:
            points += 10

        if self.status["settings_pro"]:
            points += 35
        if self.status["pro_features"]:
            points += 20
        if self.status["lifetime"]:
            points += 40
        if self.status["quota_unlimited"]:
            points += 25
        if self.status["machine_id_exists"]:
            points += 5

        if points >= 90:
            verdict = "100% LEGIT PRO / LIFETIME"
            color = "#3fb950"
            emoji = "👑 GOD MODE"
        elif points >= 70:
            verdict = "Very likely PRO (strong signals)"
            color = "#3fb950"
            emoji = "PRO"
        elif points >= 45:
            verdict = "Probably PRO / cracked"
            color = "#ffa500"
            emoji = "≈ PRO"
        else:
            verdict = "Looks FREE / weak / not cracked"
            color = "#ff7b72"
            emoji = "FREE"

        self._log(f" → {emoji}  {verdict}", color=color)
        self._log(f"   Total PRO confidence points: {points}/140", color=color)
        self._log("═" * 48 + "\n", color="#8b949e")

        self.status_label.config(text=verdict, foreground=color)

    def _log(self, msg: str, color: str = "#c9d1d9"):
        tag = f"tag_{len(msg)}"
        self.result_text.tag_configure(tag, foreground=color)
        self.result_text.insert(tk.END, msg + "\n", tag)
        self.result_text.see(tk.END)

    def copy_report(self):
        report = self.result_text.get("1.0", tk.END).strip()
        self.clipboard_clear()
        self.clipboard_append(report)
        self.status_label.config(text="Report copied to clipboard!", foreground="#3fb950")
        self.after(2200, lambda: self.status_label.config(text="Ready...", foreground="#8b949e"))


if __name__ == "__main__":
    app = CursorProChecker()
    app.mainloop()