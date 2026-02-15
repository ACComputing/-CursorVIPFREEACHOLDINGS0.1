# CatsCursorVIP1.3.py – Verified Pro Forever + Hosts Nuker
# [C] Cat 'n Co Holdings ∞ 1999-2026 | @ItsJustaCat00 x ProfesserCatsan
# One-shot: randomize IDs + fake Pro/verified + max quota + hosts block button

import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
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
import getpass  # for password prompt fallback

class CatsCursorVIP:
    def __init__(self, root):
        self.root = root
        self.root.title("Cat's Cursor VIP 1.3 – VERIFIED PRO + HOSTS NUKER 😼💀♾️")
        self.root.geometry("780x680")
        self.root.configure(bg="#0a0014")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, bg="#0a0014", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        tk.Label(self.root, text="CAT'S CURSOR VIP 1.3", font=("Helvetica", 32, "bold"),
                 fg="#ff00ff", bg="#0a0014").place(relx=0.5, rely=0.04, anchor="center")

        tk.Label(self.root, text="VERIFIED PRO FOREVER + SERVERS BLOCKED", font=("Helvetica", 18, "italic"),
                 fg="#cc00ff", bg="#0a0014").place(relx=0.5, rely=0.12, anchor="center")

        self.status = tk.Label(self.root, text="READY TO BECOME VERIFIED CHAD + NUKE SERVERS", 
                               font=("Helvetica", 16), fg="#00ff88", bg="#0a0014", wraplength=720)
        self.status.place(relx=0.5, rely=0.20, anchor="center")

        self.nuke_btn = tk.Button(self.root, text="NUKE & FAKE VERIFIED PRO FOREVER", font=("Helvetica", 20, "bold"),
                                  bg="#ff0044", fg="white", activebackground="#cc0022", relief="flat",
                                  command=self.start_nuke)
        self.nuke_btn.place(relx=0.5, rely=0.32, anchor="center", width=560, height=80)

        self.hosts_btn = tk.Button(self.root, text="BLOCK CURSOR SERVERS IN HOSTS (sudo)", font=("Helvetica", 18, "bold"),
                                   bg="#aa00ff", fg="white", activebackground="#8800cc", relief="flat",
                                   command=self.block_hosts)
        self.hosts_btn.place(relx=0.5, rely=0.44, anchor="center", width=560, height=70)

        self.log = scrolledtext.ScrolledText(self.root, width=88, height=24, font=("Consolas", 11),
                                             bg="#0f001f", fg="#ffccff", insertbackground="#ff00ff")
        self.log.place(relx=0.5, rely=0.72, anchor="center")

        self.trail = []
        self.colors = ["#ff00ff", "#cc00cc", "#990099", "#ff3399", "#ff0066"]
        self.canvas.bind("<Motion>", self.trail_move)
        self.canvas.bind("<Button-1>", self.explosion)
        self.animate_trail()

        self.info = self.detect()
        self.status.config(text=f"OS: {self.info['pretty']} | Click to pwn + block kitten")

    def detect(self):
        sys_name = platform.system()
        mach = platform.machine().lower()
        pretty = sys_name

        if sys_name == "Darwin":
            pretty = "macOS " + ("Apple Silicon" if "arm" in mach else "Intel")
            base = Path.home() / "Library" / "Application Support" / "Cursor"
        elif sys_name == "Windows":
            appdata = os.getenv("APPDATA") or str(Path.home() / "AppData" / "Roaming")
            base = Path(appdata) / "Cursor"
            pretty = f"Windows {platform.release()}"
        elif sys_name == "Linux":
            base = Path.home() / ".config" / "Cursor"
            pretty = f"Linux {mach}"
        else:
            base = Path.home() / ".cursor"
            pretty = f"{sys_name} ({mach}) experimental"

        return {"system": sys_name, "pretty": pretty, "base": base.expanduser().resolve()}

    def trail_move(self, e):
        x, y = e.x, e.y
        self.canvas.delete("cursor")
        self.canvas.create_oval(x-60, y-60, x+60, y+60, outline="#ff00ff", width=10, tags="cursor")
        self.canvas.create_oval(x-40, y-40, x+40, y+40, fill="#1a001a", outline="#cc00cc", width=8, tags="cursor")
        self.trail.append((x, y, 0))

    def explosion(self, e):
        for _ in range(40):
            self.trail.append((e.x + random.uniform(-180,180), e.y + random.uniform(-180,180), -25))

    def animate_trail(self):
        self.canvas.delete("trail")
        new = []
        for x, y, age in self.trail:
            if (a := max(0, 1 - age / 35)) <= 0: continue
            r = 32 + age*3 if age < 0 else 40 - age*2
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=random.choice(self.colors), tags="trail")
            new.append((x, y, age + 1))
        self.trail = new
        self.root.after(18, self.animate_trail)

    def log_msg(self, msg, color="white"):
        self.log.insert(tk.END, f"{msg}\n")
        self.log.see(tk.END)
        self.root.update()

    def start_nuke(self):
        Thread(target=self.nuke_cursor, daemon=True).start()

    def nuke_cursor(self):
        self.status.config(text="NUKING CURSOR → VERIFIED PRO FOREVER MODE", fg="#ffcc00")
        self.nuke_btn.config(state="disabled")
        self.hosts_btn.config(state="disabled")
        self.log.delete(1.0, tk.END)
        self.root.update()

        lines = ["═" * 70, f" CAT'S CURSOR VIP 1.3 – VERIFIED PRO NUKE – {self.info['pretty']}", "═" * 70, ""]

        base = self.info["base"]
        if not base.exists():
            lines += ["[CRITICAL] Cursor folder missing!", f"Expected: {base}", "Install Cursor first kitten"]
            self.show_result(lines)
            return

        storage = base / "User" / "globalStorage" / "storage.json"
        settings = base / "User" / "settings.json"

        pro_keys = {
            "isPro": True,
            "isVerified": True,
            "subscriptionTier": "pro",
            "subscriptionStatus": "active",
            "entitlement": {"type": "pro", "expires": "2099-12-31"},
            "hasLifetimeAccess": True,
            "features.pro": True,
            "features.unlimitedContext": True,
            "features.fastRequests": True,
            "monthlyFastRequestLimit": 999999999,
            "monthlyFastRequestsUsed": 0,
            "contextWindowMultiplier": 100,
            "telemetry.telemetryLevel": "off",
            "telemetry.enableTelemetry": False,
            "update.mode": "none",
            "extensions.autoUpdate": False,
        }

        new_ids = {
            "telemetry.machineId": str(uuid.uuid4()),
            "telemetry.macMachineId": ':'.join(f'{random.randint(0,255):02x}' for _ in range(6)).upper(),
            "telemetry.devDeviceId": str(uuid.uuid4()),
            "telemetry.sqmId": str(uuid.uuid4()),
            "telemetry.deviceId": str(uuid.uuid4()),
            "telemetry.sessionId": str(uuid.uuid4()),
        }

        # Patch storage.json
        if storage.exists():
            try:
                with open(storage, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                data.update(pro_keys)
                data.update(new_ids)
                with open(storage, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                lines += ["✓ storage.json → VERIFIED PRO + RANDOM IDs injected"]
            except Exception as e:
                lines += [f"[FAIL] storage.json → {e}"]

        # Patch settings.json
        if settings.exists():
            try:
                with open(settings, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                data.update(pro_keys)
                with open(settings, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                lines += ["✓ settings.json patched with Pro keys"]
            except Exception as e:
                lines += [f"[FAIL] settings.json → {e}"]

        # Cache nuke
        nuke_list = [
            base / "Cache", base / "Code" / "Cache", base / "Code" / "CachedData",
            base / "Code" / "CachedExtensions", base / "GPUCache", base / "CachedIconImages",
            base / "CachedExtensionVSIXs", base / "logs", base.parent / "cache",
            base.parent / "updater", base / "shadercache", base / "temp",
        ]
        nuked = 0
        for d in nuke_list:
            if d.exists():
                try:
                    if d.is_dir(): shutil.rmtree(d, ignore_errors=True)
                    else: d.unlink()
                    nuked += 1
                except: pass
        lines += [f"✓ Nuked {nuked} cache/log/temp folders"]

        # Kill Cursor
        killed = False
        try:
            if self.info["system"] == "Darwin":
                subprocess.run(["pkill", "-9", "-f", "Cursor"], timeout=10)
            elif self.info["system"] == "Windows":
                subprocess.run(["taskkill", "/F", "/IM", "Cursor.exe"], timeout=10)
            else:
                subprocess.run(["pkill", "-9", "-f", "cursor"], timeout=10)
            killed = True
        except: pass
        lines += ["✓ Cursor killed" if killed else "[INFO] Cursor not running"]

        # Final verdict
        lines += ["", "═" * 30 + " VERDICT " + "═" * 30,
                  "FAKE VERIFIED PRO STATUS ACTIVE",
                  "• Randomized fingerprints → server confused",
                  "• Telemetry dead",
                  "• Fake Pro / unlimited illusion maxed",
                  "• Caches nuked",
                  "Click the HOSTS button next to block servers forever",
                  "Relaunch Cursor → PRO VERIFIED UI should appear ♾️"]

        self.show_result(lines)
        self.status.config(text="NUKE COMPLETE – YOU ARE VERIFIED PRO", fg="#00ff88")
        self.nuke_btn.config(state="normal")
        self.hosts_btn.config(state="normal")

        time.sleep(1.5)
        try:
            if self.info["system"] == "Darwin":
                subprocess.Popen(["open", "-a", "Cursor"])
            elif self.info["system"] == "Windows":
                subprocess.Popen("start Cursor.exe", shell=True)
            else:
                subprocess.Popen("cursor", shell=True)
        except: pass

    def block_hosts(self):
        if self.info["system"] != "Darwin" and self.info["system"] != "Linux":
            messagebox.showerror("Unsupported", "Hosts blocking only on macOS/Linux for now kitten")
            return

        hosts_path = Path("/etc/hosts")
        if not hosts_path.exists():
            messagebox.showerror("Error", "/etc/hosts not found?")
            return

        blocks = [
            "127.0.0.1 api.cursor.sh",
            "127.0.0.1 api2.cursor.sh",
            "127.0.0.1 raven.cursor.sh",
            "127.0.0.1 agent.api5.cursor.sh",
            "127.0.0.1 telemetry.cursor.sh",
        ]

        try:
            with open(hosts_path, 'r') as f:
                content = f.read()
            already_blocked = all(line.strip() in content for line in blocks)
            if already_blocked:
                messagebox.showinfo("Already Done", "All Cursor servers already blocked in hosts ✓")
                return
        except PermissionError:
            pass  # we'll try sudo below

        password = simpledialog.askstring("sudo required", "Enter your password to edit /etc/hosts:", show='*')
        if not password:
            messagebox.showwarning("Cancelled", "Hosts block cancelled")
            return

        cmd = f"echo '{password}' | sudo -S tee -a /etc/hosts >/dev/null <<'EOF'\n" + "\n".join(blocks) + "\nEOF"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                messagebox.showinfo("Success", "Cursor servers blocked in /etc/hosts!\nThey can't phone home anymore kitten ♡")
                self.log_msg("Hosts blocked: api*.cursor.sh, raven, agent, telemetry", "green")
            else:
                messagebox.showerror("Failed", f"sudo failed:\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to block hosts:\n{str(e)}")

    def show_result(self, lines):
        self.log.delete(1.0, tk.END)
        for line in lines:
            self.log.insert(tk.END, line + "\n")
        self.log.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CatsCursorVIP(root)
    root.mainloop()
