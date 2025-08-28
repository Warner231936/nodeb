"""GUI module for displaying system status."""

import threading

try:
    import tkinter as tk
except Exception:  # pragma: no cover - GUI may not be available
    tk = None

import psutil

class SystemGUI:
    """Simple Tkinter GUI showing system stats."""

    def __init__(self, refresh_ms: int = 1000):
        self.refresh_ms = refresh_ms
        self.root = None
        self.labels = {}

    def _create_widgets(self):
        stats = ["CPU", "Memory", "Disk", "GPU"]
        for stat in stats:
            label = tk.Label(self.root, text=f"{stat}: N/A")
            label.pack()
            self.labels[stat] = label

    def _update_stats(self):
        try:
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            gpu = self._get_gpu_usage()
            self.labels["CPU"].config(text=f"CPU: {cpu}%")
            self.labels["Memory"].config(text=f"Memory: {mem}%")
            self.labels["Disk"].config(text=f"Disk: {disk}%")
            self.labels["GPU"].config(text=f"GPU: {gpu}")
        except Exception as e:  # pragma: no cover
            print(f"GUI update failed: {e}")
        finally:
            if self.root:
                self.root.after(self.refresh_ms, self._update_stats)

    @staticmethod
    def _get_gpu_usage():
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                return f"{gpus[0].load * 100:.1f}%"
        except Exception:
            return "N/A"
        return "N/A"

    def run(self):
        if tk is None:
            print("Tkinter not available; GUI will not start.")
            return
        self.root = tk.Tk()
        self.root.title("System Status")
        self._create_widgets()
        self._update_stats()
        threading.Thread(target=self.root.mainloop, daemon=True).start()
