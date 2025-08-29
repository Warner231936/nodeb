"""Simple TCP listener acknowledging dispatched messages."""

import json
import socket
import threading
from pathlib import Path


def _handle(conn: socket.socket):
    try:
        data = conn.recv(4096)
        if data:
            conn.sendall(b"ACK")
        else:
            conn.sendall(b"ERR")
    except Exception as e:  # pragma: no cover - network errors
        try:
            conn.sendall(f"ERR:{e}".encode())
        except Exception:
            pass
    finally:
        conn.close()


def _serve(port: int, host: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        while True:
            conn, _ = s.accept()
            threading.Thread(target=_handle, args=(conn,), daemon=True).start()


def main():
    cfg = json.loads(Path("config.json").read_text())
    listener_cfg = cfg.get("listener", {})
    host = listener_cfg.get("host", "0.0.0.0")
    ports = listener_cfg.get("ports", [])
    threads = []
    for port in ports:
        t = threading.Thread(target=_serve, args=(port, host), daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


if __name__ == "__main__":  # pragma: no cover
    main()
