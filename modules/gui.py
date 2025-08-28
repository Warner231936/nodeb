"""GUI module for displaying system status."""

import threading
import time

try:
    import tkinter as tk
    from tkinter import ttk
except Exception:  # pragma: no cover - GUI may not be available
    tk = None
    ttk = None

import psutil


class SystemGUI:
    """Tkinter GUI showing system stats and message activity."""

    def __init__(self, memory, refresh_ms: int = 1000):
        self.refresh_ms = refresh_ms
        self.memory = memory
        self.root = None
        self.labels = {}
        self.queue_bar = None
        self.queue_label = None
        self.messages_box = None
        self.chaos_box = None
        self.start_time = time.time()

    # ------------------------------------------------------------------
    def _create_widgets(self):
        stats = ["CPU", "Memory", "Disk", "GPU", "Uptime"]
        for stat in stats:
            label = tk.Label(self.root, text=f"{stat}: N/A")
            label.pack()
            self.labels[stat] = label

        tk.Label(self.root, text="Messages").pack()
        self.messages_box = tk.Text(self.root, height=8, state="disabled")
        self.messages_box.pack(fill="both", expand=True)

        self.queue_bar = ttk.Progressbar(self.root, maximum=self.memory.capacity)
        self.queue_bar.pack(fill="x")
        self.queue_label = tk.Label(self.root, text=f"Queue: 0/{self.memory.capacity}")
        self.queue_label.pack()

        tk.Label(self.root, text="Chaos").pack()
        self.chaos_box = tk.Text(self.root, height=8, state="disabled")
        self.chaos_box.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    def _update_stats(self):
        try:
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            gpu = self._get_gpu_usage()
            uptime = int(time.time() - self.start_time)
            queue_len = len(self.memory)

            self.labels["CPU"].config(text=f"CPU: {cpu}%")
            self.labels["Memory"].config(text=f"Memory: {mem}%")
            self.labels["Disk"].config(text=f"Disk: {disk}%")
            self.labels["GPU"].config(text=f"GPU: {gpu}")
            self.labels["Uptime"].config(text=f"Uptime: {uptime}s")
            if self.queue_bar is not None:
                self.queue_bar['value'] = queue_len
            if self.queue_label is not None:
                self.queue_label.config(text=f"Queue: {queue_len}/{self.memory.capacity}")
        except Exception as e:  # pragma: no cover
            print(f"GUI update failed: {e}")
        finally:
            if self.root:
                self.root.after(self.refresh_ms, self._update_stats)

    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    def display_message(self, entry):
        if not self.messages_box:
            return
        self.messages_box.configure(state="normal")
        self.messages_box.insert(tk.END, f"{entry['user']}: {entry['message']}\n")
        self.messages_box.see(tk.END)
        self.messages_box.configure(state="disabled")

    def log_event(self, text: str) -> None:
        if not self.chaos_box:
            return
        self.chaos_box.configure(state="normal")
        self.chaos_box.insert(tk.END, text + "\n")
        self.chaos_box.see(tk.END)
        self.chaos_box.configure(state="disabled")

    # ------------------------------------------------------------------
    def run(self):
        if tk is None:
            print("Tkinter not available; GUI will not start.")
            return
        self.root = tk.Tk()
        self.root.title("System Status")
        self._create_widgets()
        self._update_stats()
        threading.Thread(target=self.root.mainloop, daemon=True).start()
