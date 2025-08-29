"""Simple dependency installer."""

import os
import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Install requirements listed in ``req.txt``.

    The installer upgrades ``pip`` first and then installs the packages
    listed in the requirements file.  Missing files or installation errors
    are reported to the console so that setup on multiple machines remains
    straightforward.
    """

    req_file = Path("req.txt")
    if not req_file.exists():
        print(f"{req_file} not found.")
        return

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
    except subprocess.CalledProcessError as exc:  # pragma: no cover - network issues
        print(f"Dependency installation failed: {exc}")


if __name__ == "__main__":
    main()
