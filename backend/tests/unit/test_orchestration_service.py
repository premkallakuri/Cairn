import pytest

from app.core.config import reset_settings_cache
from app.modules.catalog.service import AppManifest
from app.modules.orchestration.service import AppOrchestrator

pytestmark = [pytest.mark.unit, pytest.mark.platform]


class FakeAdapter:
    def __init__(self, should_fail_update: bool = False) -> None:
        self.calls: list[str] = []
        self.should_fail_update = should_fail_update

    def install(self, manifest: AppManifest) -> None:
        self.calls.append(f"install:{manifest.id}")

    def start(self, service_name: str) -> None:
        self.calls.append(f"start:{service_name}")

    def stop(self, service_name: str) -> None:
        self.calls.append(f"stop:{service_name}")

    def remove(self, service_name: str) -> None:
        self.calls.append(f"remove:{service_name}")

    def update(self, manifest: AppManifest) -> None:
        self.calls.append(f"update:{manifest.id}")
        if self.should_fail_update:
            raise RuntimeError("update failed")


def build_manifest() -> AppManifest:
    return AppManifest.model_validate(
        {
            "id": "nomad_kiwix_server",
            "kind": "sibling_app",
            "display": {"name": "Kiwix", "description": "Docs", "icon": "IconBooks", "order": 1},
            "runtime": {"image": "ghcr.io/kiwix/kiwix-serve:3.8.1"},
            "network": {"join": "project-nomad_default"},
            "storage": {"requires": ["storage/zim"]},
            "dependencies": [],
            "healthcheck": {"type": "http", "target": "http://kiwix"},
            "hooks": {},
            "updates": {},
            "permissions": {},
            "capabilities": {},
            "docs": {"slug": "app-kiwix"},
            "tests": {"smoke": "apps/kiwix/tests/test_smoke.py"},
        }
    )


def test_install_app_emits_stages_in_order() -> None:
    adapter = FakeAdapter()
    orchestrator = AppOrchestrator(adapter)

    events = orchestrator.install_app(build_manifest())

    assert adapter.calls == ["install:nomad_kiwix_server", "start:nomad_kiwix_server"]
    assert [(event.stage, event.status) for event in events] == [
        ("preflight", "running"),
        ("install", "success"),
        ("start", "success"),
    ]


def test_update_app_emits_rollback_event_on_failure() -> None:
    adapter = FakeAdapter(should_fail_update=True)
    orchestrator = AppOrchestrator(adapter)

    with pytest.raises(RuntimeError):
        orchestrator.update_app(build_manifest())

    assert orchestrator.events[-1].stage == "rollback"


def test_install_app_runs_preinstall_hook_when_declared(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ATLAS_HAVEN_STORAGE_PATH", str(tmp_path / "storage"))
    adapter = FakeAdapter()
    orchestrator = AppOrchestrator(adapter)
    manifest = build_manifest()
    manifest.hooks = {"preinstall": "apps.kiwix.hooks.preinstall"}

    events = orchestrator.install_app(manifest)

    assert (tmp_path / "storage" / "zim" / "wikipedia_en_100_mini_2025-06.zim").exists()
    assert [(event.stage, event.status) for event in events] == [
        ("preflight", "running"),
        ("preinstall", "running"),
        ("preinstall", "success"),
        ("install", "success"),
        ("start", "success"),
    ]


def test_install_app_runs_full_hook_lifecycle(tmp_path, monkeypatch) -> None:
    workspace_root = tmp_path / "workspace"
    hook_log = tmp_path / "hook-log.txt"
    hooks_dir = workspace_root / "apps" / "sample" / "hooks.py"
    hooks_dir.parent.mkdir(parents=True, exist_ok=True)
    hooks_dir.write_text(
        "from pathlib import Path\n"
        "import os\n\n"
        "def _append(name: str) -> None:\n"
        "    path = Path(os.environ['ATLAS_HAVEN_HOOK_LOG'])\n"
        "    existing = path.read_text() if path.exists() else ''\n"
        "    path.write_text(existing + name + '\\n')\n\n"
        "def preflight() -> None:\n"
        "    _append('preflight')\n\n"
        "def preinstall() -> None:\n"
        "    _append('preinstall')\n\n"
        "def postinstall() -> None:\n"
        "    _append('postinstall')\n\n"
        "def prestart() -> None:\n"
        "    _append('prestart')\n\n"
        "def poststart() -> None:\n"
        "    _append('poststart')\n"
    )
    monkeypatch.setenv("ATLAS_HAVEN_WORKSPACE_ROOT", str(workspace_root))
    monkeypatch.setenv("ATLAS_HAVEN_STORAGE_PATH", str(tmp_path / "storage"))
    monkeypatch.setenv("ATLAS_HAVEN_HOOK_LOG", str(hook_log))
    reset_settings_cache()

    adapter = FakeAdapter()
    orchestrator = AppOrchestrator(adapter)
    manifest = build_manifest()
    manifest.hooks = {
        "preflight": "apps.sample.hooks.preflight",
        "preinstall": "apps.sample.hooks.preinstall",
        "postinstall": "apps.sample.hooks.postinstall",
        "prestart": "apps.sample.hooks.prestart",
        "poststart": "apps.sample.hooks.poststart",
    }

    events = orchestrator.install_app(manifest)

    assert hook_log.read_text().splitlines() == [
        "preflight",
        "preinstall",
        "postinstall",
        "prestart",
        "poststart",
    ]
    assert [(event.stage, event.status) for event in events] == [
        ("preflight", "running"),
        ("preflight", "running"),
        ("preflight", "success"),
        ("preinstall", "running"),
        ("preinstall", "success"),
        ("install", "success"),
        ("postinstall", "running"),
        ("postinstall", "success"),
        ("prestart", "running"),
        ("prestart", "success"),
        ("start", "success"),
        ("poststart", "running"),
        ("poststart", "success"),
    ]


def test_update_app_runs_preupdate_and_rollback_hook(tmp_path, monkeypatch) -> None:
    workspace_root = tmp_path / "workspace"
    hook_log = tmp_path / "hook-log.txt"
    hooks_dir = workspace_root / "apps" / "sample" / "hooks.py"
    hooks_dir.parent.mkdir(parents=True, exist_ok=True)
    hooks_dir.write_text(
        "from pathlib import Path\n"
        "import os\n\n"
        "def _append(name: str) -> None:\n"
        "    path = Path(os.environ['ATLAS_HAVEN_HOOK_LOG'])\n"
        "    existing = path.read_text() if path.exists() else ''\n"
        "    path.write_text(existing + name + '\\n')\n\n"
        "def preupdate() -> None:\n"
        "    _append('preupdate')\n\n"
        "def rollback() -> None:\n"
        "    _append('rollback')\n"
    )
    monkeypatch.setenv("ATLAS_HAVEN_WORKSPACE_ROOT", str(workspace_root))
    monkeypatch.setenv("ATLAS_HAVEN_STORAGE_PATH", str(tmp_path / "storage"))
    monkeypatch.setenv("ATLAS_HAVEN_HOOK_LOG", str(hook_log))
    reset_settings_cache()

    adapter = FakeAdapter(should_fail_update=True)
    orchestrator = AppOrchestrator(adapter)
    manifest = build_manifest()
    manifest.hooks = {
        "preupdate": "apps.sample.hooks.preupdate",
        "rollback": "apps.sample.hooks.rollback",
    }

    with pytest.raises(RuntimeError):
        orchestrator.update_app(manifest)

    assert hook_log.read_text().splitlines() == ["preupdate", "rollback"]
