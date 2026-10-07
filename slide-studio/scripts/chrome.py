"""Locate a Chrome/Chromium/Edge binary for headless rendering. Override with $CHROME."""
import os
import shutil
import sys
from pathlib import Path

CANDIDATES = {
    "win32": [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"],
    "darwin": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
               "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"],
}


def find_chrome():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    for p in CANDIDATES.get(sys.platform, []):
        if Path(p).exists():
            return p
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge"):
        if shutil.which(name):
            return shutil.which(name)
    raise SystemExit("Chrome not found: set the CHROME environment variable to its path")


CHROME = find_chrome()
