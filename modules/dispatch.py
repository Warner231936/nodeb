"""Dispatch responses to listening ports."""

import socket
from typing import Iterable


def dispatch(message: str, ports: Iterable[int], host: str) -> None:
    """Send ``message`` to each ``port`` on ``host`` and report replies."""

    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, port))
                sock.sendall(message.encode())
                response = sock.recv(1024).decode() or ""
                print(f"Dispatch to {port} reply: {response}")
        except Exception as e:
            print(f"Dispatch to {port} failed: {e}")
