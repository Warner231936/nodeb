"""Dispatch responses to listening ports."""

import socket
from typing import Iterable

def dispatch(message: str, ports: Iterable[int], host: str = 'localhost'):
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, port))
                sock.sendall(message.encode())
        except Exception as e:
            print(f"Dispatch to {port} failed: {e}")
