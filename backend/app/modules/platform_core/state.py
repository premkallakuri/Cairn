from __future__ import annotations

import json
import socket
from datetime import datetime
from app.core.compat import UTC
from pathlib import Path
from typing import Any

from app.core.config import get_settings

DEFAULT_SYSTEM_SETTINGS: dict[str, Any] = {
    "chat.suggestionsEnabled": True,
    "chat.lastModel": None,
    "ui.hasVisitedEasySetup": False,
    "system.earlyAccess": False,
    "ai.assistantCustomName": None,
}


class JsonStateStore:
    def __init__(self, root: Path | None = None) -> None:
        settings = get_settings()
        self.root = root or settings.storage_path / "system"
        self.root.mkdir(parents=True, exist_ok=True)

    def read_json(self, filename: str, default: dict[str, Any]) -> dict[str, Any]:
        path = self.root / filename
        if not path.exists():
            return dict(default)

        payload = json.loads(path.read_text())
        if not isinstance(payload, dict):
            return dict(default)
        return {**default, **payload}

    def write_json(self, filename: str, payload: dict[str, Any]) -> None:
        path = self.root / filename
        path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    def read_text(self, filename: str) -> str:
        path = self.root / filename
        if not path.exists():
            return ""
        return path.read_text()

    def write_text(self, filename: str, payload: str) -> None:
        path = self.root / filename
        path.write_text(payload)

    def append_line(self, filename: str, payload: str) -> None:
        path = self.root / filename
        with path.open("a", encoding="utf-8") as handle:
            handle.write(payload)
            if not payload.endswith("\n"):
                handle.write("\n")


class SystemSettingsService:
    def __init__(self, store: JsonStateStore | None = None) -> None:
        self.store = store or JsonStateStore()

    def get_setting(self, key: str) -> Any:
        settings = self.store.read_json("settings.json", DEFAULT_SYSTEM_SETTINGS)
        return settings.get(key)

    def update_setting(self, key: str, value: Any) -> None:
        settings = self.store.read_json("settings.json", DEFAULT_SYSTEM_SETTINGS)
        settings[key] = value
        self.store.write_json("settings.json", settings)


class SystemUpdateService:
    def __init__(self, store: JsonStateStore | None = None) -> None:
        self.store = store or JsonStateStore()

    def get_latest_version(self) -> dict[str, Any]:
        settings = get_settings()
        return {
            "success": True,
            "updateAvailable": False,
            "currentVersion": settings.version,
            "latestVersion": settings.version,
            "message": "Atlas Haven is running the bundled local version.",
        }

    def subscribe_release_notes(self, email: str) -> None:
        subscribers = {
            line.strip()
            for line in self.store.read_text("release-notes-subscribers.txt").splitlines()
            if line.strip()
        }
        if email not in subscribers:
            self.store.append_line("release-notes-subscribers.txt", email)

    def get_status(self) -> dict[str, Any]:
        default = {
            "stage": "idle",
            "progress": 0,
            "message": "No system update is running.",
            "timestamp": self._now(),
        }
        return self.store.read_json("update-status.json", default)

    def request_update(self) -> dict[str, Any]:
        status = self.get_status()
        if status["stage"] not in {"idle", "complete", "error"}:
            raise RuntimeError("A system update is already running.")

        starting = {
            "stage": "starting",
            "progress": 10,
            "message": "Preparing local update workflow.",
            "timestamp": self._now(),
        }
        complete = {
            "stage": "complete",
            "progress": 100,
            "message": "Local distribution is already on the bundled version.",
            "timestamp": self._now(),
        }
        self.store.write_json("update-status.json", complete)
        self.store.write_text(
            "update.log",
            (
                f"{starting['timestamp']} preparing local update workflow\n"
                f"{complete['timestamp']} no remote update applied; "
                "bundled version already active\n"
            ),
        )
        return {
            "success": True,
            "message": "System update check completed.",
            "note": "Atlas Haven local-first distributions do not auto-pull remote updates.",
        }

    def get_logs(self) -> str:
        return self.store.read_text("update.log")

    def internet_reachable(self) -> bool:
        try:
            with socket.create_connection(("1.1.1.1", 53), timeout=0.3):
                return True
        except OSError:
            return False

    def _now(self) -> str:
        return datetime.now(UTC).isoformat()
