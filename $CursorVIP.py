import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
from pathlib import Path
import platform
import uuid
import random
import shutil
import subprocess
import time
from datetime import datetime
import threading

class CursorGodmodeChef(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🐱 Cursor GODMODE CHEF v3.2 — Stealth Anti-Ban 2026 😼🕵️‍♂️🔥")
        self.geometry("980x860")
        self.minsize(880, 760)
        self.configure(bg="#0a0e14")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#0a0e14", foreground="#a0d0ff", font=("Consolas", 11))
        self.style.configure("Header.TLabel", background="#0a0e14", foreground="#ff1493", font=("Consolas", 22, "bold"))
        self.style.configure("BigButton.TButton", font=("Consolas", 16, "bold"), padding=16)
        self.style.map("BigButton.TButton", background=[("active", "#ff1493")], foreground=[("active", "white")])

        self.base_path = self._get_cursor_path()
        self.running = False
        self.reset_thread = None
        self.stealth_mode = tk.BooleanVar(value=True)
        self.first_run = True
        self.original_ids_backup_path = self.base_path / "OriginalMachineIds.json" if self.base_path else None

        self.status = {
            "installed": False, "pro_ui": False, "god_quota": False,
            "hosts_nuked": False, "processes_dead": False, "loop_active": False
        }

        self._build_ui()
        self.after(600, self.quick_scan)

    def _get_cursor_path(self):
        p = platform.system()
        h = Path.home()
        if p == "Darwin":   return h / "Library" / "Application Support" / "Cursor"
        if p == "Windows":  return Path(os.getenv("APPDATA") or str(h / "AppData" / "Roaming")) / "Cursor"
        if p == "Linux":    return h / ".config" / "Cursor"
        return None

    def _build_ui(self):
        f = ttk.Frame(self, padding=30)
        f.pack(fill=tk.BOTH, expand=True)

        ttk.Label(f, text="CURSOR GODMODE CHEF v3.2 — 2026 STEALTH & ANTI-BAN", style="Header.TLabel").pack(pady=(0,20))

        self.log_text = scrolledtext.ScrolledText(f, font=("Consolas", 13), bg="#0d1117", fg="#c9d1d9",
                                                  insertbackground="#ff69b4", height=30, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btnf = ttk.Frame(f)
        btnf.pack(fill=tk.X, pady=20)

        self.pwn_btn = ttk.Button(btnf, text="START STEALTH GODMODE LOOP 🕵️‍♂️♾️", style="BigButton.TButton", command=self.start_chef)
        self.pwn_btn.pack(side=tk.LEFT, padx=12)

        ttk.Button(btnf, text="QUICK SCAN", command=self.quick_scan).pack(side=tk.LEFT, padx=8)
        ttk.Button(btnf, text="STOP LOOP", command=self.stop_loop).pack(side=tk.LEFT, padx=8)
        ttk.Button(btnf, text="RESTORE ORIGINAL IDs", command=self.restore_original_ids).pack(side=tk.LEFT, padx=8)
        ttk.Button(btnf, text="COPY LOG", command=lambda: self.clipboard_append(self.log_text.get("1.0", tk.END).strip())).pack(side=tk.LEFT, padx=8)

        stealth_check = ttk.Checkbutton(f, text="Stealth Mode (slower, NO quota spoof, lowest ban risk)", variable=self.stealth_mode)
        stealth_check.pack(pady=10)

        self.status_label = ttk.Label(f, text="Waiting to cook nya~ 😿", font=("Consolas", 17, "bold"), foreground="#ff69b4")
        self.status_label.pack(pady=20)

        self.update_idletasks()

    def log(self, msg, color="#c9d1d9"):
        tag = f"c_{random.randint(10000,99999)}"
        self.log_text.tag_configure(tag, foreground=color)
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{ts}] {msg}\n", tag)
        self.log_text.see(tk.END)

    def restore_original_ids(self):
        if not self.original_ids_backup_path or not self.original_ids_backup_path.exists():
            self.log("No original IDs backup found — nothing to restore", "#ffaa00")
            return
        if not messagebox.askyesno("Restore?", "Overwrite current storage.json with original IDs?\nCursor restarts. Continue?"):
            return
        sp = self.base_path / "User" / "globalStorage" / "storage.json"
        try:
            shutil.copy2(self.original_ids_backup_path, sp)
            self.log("→ Restored original machine IDs", "#88ff88")
            self._kill_all_cursor()
            self._relaunch()
        except Exception as e:
            self.log(f"Restore failed: {e}", "#ff4444")

    def _is_cursor_running(self):
        p = platform.system()
        try:
            if p == "Darwin":
                out = subprocess.check_output(["pgrep", "-f", "[C]ursor|Cursor"]).decode().strip()
                return bool(out)
            elif p == "Windows":
                out = subprocess.check_output('tasklist /FI "IMAGENAME eq cursor.exe"', shell=True).decode(errors='ignore')
                return "cursor.exe" in out.lower()
            elif p == "Linux":
                out = subprocess.check_output(["pgrep", "-f", "cursor"]).decode().strip()
                return bool(out)
        except:
            return False

    def _kill_all_cursor(self):
        p = platform.system()
        self.log("💀 Killing Cursor processes...", "#ff1493")
        if p == "Windows":
            subprocess.run('taskkill /IM cursor.exe /F', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif p == "Darwin":
            subprocess.run(["pkill", "-9", "-f", "Cursor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif p == "Linux":
            subprocess.run(["pkill", "-9", "-f", "cursor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2.5)
        if self._is_cursor_running():
            self.log("→ Cursor survived kill — close manually", "#ffaa00")
        else:
            self.status["processes_dead"] = True
            self.log("→ Cursor terminated", "#88ff88")

    def _backup(self, path):
        if not path or not path.exists():
            return
        bak_dir = self.base_path / "ChefBackup" / datetime.now().strftime("%Y%m%d_%H%M%S")
        bak_dir.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(path, bak_dir / path.name)
            self.log(f"→ Backed up {path.name}", "#aaffaa")
        except Exception as e:
            self.log(f"Backup failed {path.name}: {e}", "#ff5555")

    def _backup_original_ids(self):
        sp = self.base_path / "User" / "globalStorage" / "storage.json"
        if sp.exists() and self.first_run:
            try:
                shutil.copy2(sp, self.original_ids_backup_path)
                self.log(f"→ Original IDs backed up → {self.original_ids_backup_path}", "#aaffaa")
                self.first_run = False
            except Exception as e:
                self.log(f"Original backup failed: {e}", "#ff5555")

    def _nuke_hosts(self):
        if platform.system() not in ("Darwin", "Linux"):
            self.log("Hosts lock skipped (Windows — manual)", "#ffaa00")
            return
        hp = Path("/etc/hosts")
        domains = ["cursor.sh", "cursor.com", "api.cursor", "updates.cursor", "telemetry.cursor"]
        self.log("🛡️ Locking Cursor domains in /etc/hosts (sudo needed)...", "#ff69b4")
        try:
            with open(hp, "a") as f:
                f.write("\n# Cursor Godmode Chef Stealth Block\n")
                for d in domains:
                    for sub in ["", "api.", "updates.", "telemetry."]:
                        f.write(f"127.0.0.1 {sub}{d}\n")
            self.status["hosts_nuked"] = True
            self.log("→ /etc/hosts updated — Cursor can't phone home 🔥", "#88ff88")
        except PermissionError:
            self.log("→ sudo required! Run with: sudo python3 your_script.py", "#ff4444")
            messagebox.showerror("Root Needed", "Hosts lock requires sudo — rerun with sudo")
        except Exception as e:
            self.log(f"Hosts error: {e}", "#ff4444")

    def _inject_chaos(self):
        self._kill_all_cursor()
        self._backup_original_ids()

        sp = self.base_path / "User" / "globalStorage" / "storage.json"
        self._backup(sp)

        if self.stealth_mode.get():
            god = {
                "telemetry.machineId": str(uuid.uuid4()),
                "telemetry.macMachineId": ':'.join(f"{random.randint(0,255):02x}" for _ in range(6)).upper(),
                "telemetry.devDeviceId": str(uuid.uuid4()),
                "telemetryLevel": "off",
                "enableTelemetry": False,
                "telemetryConsent": False,
                "usageStatisticsEnabled": False,
                "lastTelemetryPing": "2099-12-31T23:59:59.999Z",
                "machineIdLastReset": str(time.time())
            }
            quota_str = "no quota spoof (stealth)"
        else:
            quota = random.randint(750000, 1100000)
            god = {
                "telemetry.machineId": str(uuid.uuid4()),
                "telemetry.macMachineId": ':'.join(f"{random.randint(0,255):02x}" for _ in range(6)).upper(),
                "telemetry.devDeviceId": str(uuid.uuid4()),
                "telemetryLevel": "off",
                "enableTelemetry": False,
                "telemetryConsent": False,
                "usageStatisticsEnabled": False,
                "monthlyFastRequestLimit": quota,
                "monthlyFastRequestsUsed": random.randint(0, quota // 12),
                "update.lastCheck": "2099-12-31T23:59:59.999Z",
                "lastKnownEntitlement": "pro_active",
                "subscriptionStatus": "active",
                "lastTelemetryPing": "2099-12-31T23:59:59.999Z",
                "machineIdLastReset": str(time.time())
            }
            quota_str = f"quota ~{quota:,}"

        d = {}
        if sp.exists():
            try:
                with open(sp, "r", encoding="utf-8") as f:
                    d = json.load(f)
            except Exception as e:
                self.log(f"Read storage.json error: {e}", "#ff6666")

        d.update(god)

        try:
            with open(sp, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2)
            self.log(f"→ storage.json updated → {quota_str} + fresh IDs", "#ffdd00")
            if not self.stealth_mode.get():
                self.status["god_quota"] = True
        except Exception as e:
            self.log(f"Write storage.json failed: {e}", "#ff5555")

        setp = self.base_path / "settings.json"
        self._backup(setp)
        pro = {
            "isPro": True,
            "hasLifetimeAccess": True,
            "subscriptionStatus": "active",
            "update.mode": "none",
            "update.autoCheck": False,
            "extensions.autoUpdate": False,
            "telemetryLevel": "off"
        }
        sd = {}
        if setp.exists():
            try:
                with open(setp, "r", encoding="utf-8") as f:
                    sd = json.load(f)
            except: pass
        sd.update(pro)
        try:
            with open(setp, "w", encoding="utf-8") as f:
                json.dump(sd, f, indent=2)
            self.log("→ settings.json → PRO flags injected", "#ffdd00")
            self.status["pro_ui"] = True
        except Exception as e:
            self.log(f"settings write failed: {e}", "#ff5555")

        for fld in ["Cache", "CachedData", "CachedExtensions", "Code Cache", "GPUCache"]:
            pth = self.base_path / fld
            if pth.exists():
                try:
                    shutil.rmtree(pth)
                    self.log(f"→ Cleared {fld}", "#88ff88")
                except: pass

        time.sleep(random.uniform(1.5, 4.5))

    def start_chef(self):
        if not self.base_path or not self.base_path.exists():
            messagebox.showerror("Error", "Cursor not found nya~")
            return

        if not messagebox.askyesno("WARNING", "This will kill Cursor, rotate IDs periodically,\nspoof quota (if not stealth) & block updates.\nContinue?"):
            return

        self.log("\n🕵️‍♂️ STEALTH GODMODE ACTIVATED — LOW PROFILE ♾️", "#ff1493")
        self._nuke_hosts()
        self._inject_chaos()
        self._relaunch()

        self.running = True
        self.status["loop_active"] = True
        self.reset_thread = threading.Thread(target=self._reset_loop, daemon=True)
        self.reset_thread.start()

        mode = "STEALTH (safe)" if self.stealth_mode.get() else "AGGRESSIVE"
        self.status_label.config(text=f"GODMODE LOOP RUNNING — {mode} MODE", foreground="#ff1493")
        self.update_idletasks()

    def _reset_loop(self):
        cycle = 0
        while self.running:
            cycle += 1
            wait_min = random.randint(180, 480) if self.stealth_mode.get() else random.randint(45, 120)
            self.log(f"Cycle {cycle} — sleeping ~{wait_min//60}h {wait_min%60}m", "#88aaff")
            time.sleep(wait_min * 60 + random.uniform(-300, 300))

            if not self.running: break

            self.log(f"Reset #{cycle} — low-profile refresh...", "#ff69b4")
            self._inject_chaos()
            self._relaunch(silent=True)
            self.quick_scan(silent=True)

    def stop_loop(self):
        self.running = False
        self.status["loop_active"] = False
        self.log("→ Reset loop stopped — Cursor remains usable", "#88ff88")
        self.status_label.config(text="LOOP STOPPED — manual control now", foreground="#ffaa00")
        self.update_idletasks()

    def _relaunch(self, silent=False):
        p = platform.system()
        if p == "Darwin":
            subprocess.Popen(["open", "-a", "Cursor"])
        elif p == "Windows":
            subprocess.Popen("start cursor", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif p == "Linux":
            subprocess.Popen(["cursor"])
        if not silent:
            self.log("→ Relaunch command sent — pray it feels unlimited nya~", "#aaffaa")
        time.sleep(random.uniform(4, 9))

    def quick_scan(self, silent=False):
        if not self.base_path or not self.base_path.exists():
            if not silent: self.log("Cursor folder missing!", "#ff4444")
            return

        self.status["installed"] = True

        est_days = 7 if self.status["hosts_nuked"] and self.stealth_mode.get() else 2
        est_days += 3 if self.status["god_quota"] else 0
        est_days += 2 if self.status["loop_active"] else 0

        msg = f"Installed: {self.status['installed']} | PRO UI: {self.status['pro_ui']} | Quota spoof: {self.status['god_quota']}\nHosts blocked: {self.status['hosts_nuked']} | Loop: {self.status['loop_active']}\nEst. ban-free window (2026): ~{est_days}-{est_days+10} days"
        if not silent:
            self.log(msg, "#ffdd00")
            self.status_label.config(text=msg.split("\n")[0], foreground="#ff69b4")
            self.update_idletasks()

if __name__ == "__main__":
    p = platform.system()
    if p in ("Darwin", "Linux") and os.geteuid() != 0:
        print("For full stealth (hosts lock) run with: sudo python3 your_script_name.py")
    else:
        print("Running without sudo — hosts lock will fail (run with sudo for full power)")
    app = CursorGodmodeChef()
    app.mainloop()
