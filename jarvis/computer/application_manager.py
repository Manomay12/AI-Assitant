# ==================================================
# JARVIS AI — Master Application Manager
# ==================================================

import logging
import os
import subprocess
from typing import Any, Dict, List, Optional

try:
    # pyrefly: ignore [missing-import]
    import pygetwindow as gw
except ImportError:
    gw = None

from jarvis.config.constants import DEFAULT_APPS

logger = logging.getLogger("jarvis.computer.app_manager")

# Windows Shell / Run mappings for applications
APP_COMMANDS: Dict[str, str] = {
    "chrome": "start chrome",
    "google chrome": "start chrome",
    "notepad": "notepad",
    "calculator": "calc",
    "calc": "calc",
    "code": "code",
    "vscode": "code",
    "vs code": "code",
    "visual studio code": "code",
    "paint": "mspaint",
    "mspaint": "mspaint",
    "cmd": "cmd",
    "command prompt": "cmd",
    "powershell": "powershell",
    "terminal": "wt",
    "taskmgr": "taskmgr",
    "task manager": "taskmgr",
    "explorer": "explorer",
    "file explorer": "explorer",
    "settings": "start ms-settings:",
    "camera": "start microsoft.windows.camera:",
    "word": "start winword",
    "excel": "start excel",
    "powerpoint": "start powerpnt",
}

APP_PROCESSES: Dict[str, str] = {
    "chrome": "chrome.exe",
    "notepad": "notepad.exe",
    "calculator": "CalculatorApp.exe",
    "calc": "CalculatorApp.exe",
    "code": "Code.exe",
    "vscode": "Code.exe",
    "vs code": "Code.exe",
    "paint": "mspaint.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "taskmgr": "Taskmgr.exe",
    "explorer": "explorer.exe",
}


class ApplicationManager:
    """
    Manages opening, closing, and querying Windows desktop applications.
    """

    def __init__(self):
        self.apps = DEFAULT_APPS.copy()

    def get_open_windows(self) -> List[str]:
        """Returns titles of all non-empty active windows."""
        if not gw:
            return []
        try:
            return [w.title for w in gw.getAllWindows() if w.title and w.title.strip()]
        except Exception as e:
            logger.error(f"Error listing windows: {e}")
            return []

    def open_application(self, app_name: str) -> Dict[str, Any]:
        """
        Instantly launch an application by canonical name.
        """
        name_clean = app_name.lower().strip()
        command = APP_COMMANDS.get(name_clean, f"start {name_clean}")

        logger.info(f"Launching application: '{name_clean}' via command: '{command}'")
        try:
            subprocess.Popen(
                command,
                shell=True,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            return {
                "success": True,
                "app": name_clean,
                "message": f"Successfully launched {name_clean.capitalize()}.",
            }
        except Exception as e:
            logger.error(f"Failed to launch {name_clean}: {e}")
            return {
                "success": False,
                "app": name_clean,
                "error": str(e),
                "message": f"Could not launch {name_clean}: {e}",
            }

    def close_application(self, app_name: str) -> Dict[str, Any]:
        """
        Terminate an application process safely.
        """
        name_clean = app_name.lower().strip()
        exe = APP_PROCESSES.get(name_clean, f"{name_clean}.exe")

        logger.info(f"Terminating application: '{name_clean}' ({exe})")
        try:
            result = subprocess.run(
                ["taskkill", "/F", "/IM", exe],
                capture_output=True,
                text=True,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            if result.returncode == 0:
                return {
                    "success": True,
                    "app": name_clean,
                    "message": f"Closed {name_clean.capitalize()}.",
                }
            else:
                return {
                    "success": False,
                    "app": name_clean,
                    "message": f"{name_clean.capitalize()} was not running.",
                }
        except Exception as e:
            logger.error(f"Error closing {name_clean}: {e}")
            return {
                "success": False,
                "app": name_clean,
                "error": str(e),
                "message": f"Could not close {name_clean}: {e}",
            }


app_manager = ApplicationManager()
