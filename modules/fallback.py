"""Fallback strategies when errors occur."""

try:
    import tkinter.messagebox as messagebox
except Exception:  # pragma: no cover - tkinter may be unavailable
    messagebox = None


def handle_error(error: Exception):
    msg = f"Fallback activated: {error}"
    if messagebox:
        try:
            messagebox.showerror("System Error", msg)
        except Exception:
            print(msg)
    else:
        print(msg)
