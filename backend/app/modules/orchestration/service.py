from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Protocol

from app.core.config import get_settings
from app.modules.catalog.service import AppManifest


@dataclass(slots=True)
class OperationEvent:
    operation: str
    service_name: str
    stage: str
    status: str


class ContainerAdapter(Protocol):
    def install(self, manifest: AppManifest) -> None: ...
    def start(self, service_name: str) -> None: ...
    def stop(self, service_name: str) -> None: ...
    def remove(self, service_name: str) -> None: ...
    def update(self, manifest: AppManifest) -> None: ...


class HookExecutor:
    def __init__(self, workspace_root: Path | None = None) -> None:
        settings = get_settings()
        self.workspace_root = workspace_root or settings.workspace_root

    def run(self, manifest: AppManifest, hook_name: str) -> object | None:
        hook_ref = manifest.hooks.get(hook_name)
        if not hook_ref:
            return None

        module_path, function_name = hook_ref.rsplit(".", 1)
        file_path = self.workspace_root / Path(*module_path.split("."))
        hook_file = file_path.with_suffix(".py")
        spec = spec_from_file_location(f"atlas_haven_hook_{manifest.id}_{hook_name}", hook_file)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Unable to load hook {hook_ref}")
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        hook = getattr(module, function_name)
        return hook()


class AppOrchestrator:
    def __init__(
        self,
        adapter: ContainerAdapter,
        hook_executor: HookExecutor | None = None,
    ) -> None:
        self.adapter = adapter
        self.hook_executor = hook_executor or HookExecutor()
        self.events: list[OperationEvent] = []

    def _emit(self, operation: str, service_name: str, stage: str, status: str) -> None:
        self.events.append(OperationEvent(operation, service_name, stage, status))

    def _run_optional_hook(self, manifest: AppManifest, hook_name: str) -> None:
        if not manifest.hooks.get(hook_name):
            return
        self._emit("hook", manifest.id, hook_name, "running")
        self.hook_executor.run(manifest, hook_name)
        self._emit("hook", manifest.id, hook_name, "success")

    def install_app(self, manifest: AppManifest) -> list[OperationEvent]:
        self._emit("install", manifest.id, "preflight", "running")
        self._run_optional_hook(manifest, "preflight")
        self._run_optional_hook(manifest, "preinstall")
        self.adapter.install(manifest)
        self._emit("install", manifest.id, "install", "success")
        self._run_optional_hook(manifest, "postinstall")
        self._run_optional_hook(manifest, "prestart")
        self.adapter.start(manifest.id)
        self._emit("install", manifest.id, "start", "success")
        self._run_optional_hook(manifest, "poststart")
        return self.events

    def reinstall_app(self, manifest: AppManifest) -> list[OperationEvent]:
        self._emit("reinstall", manifest.id, "preflight", "running")
        self._run_optional_hook(manifest, "preflight")
        self._run_optional_hook(manifest, "preuninstall")
        self._emit("reinstall", manifest.id, "stop", "running")
        self.adapter.stop(manifest.id)
        self.adapter.remove(manifest.id)
        self._emit("reinstall", manifest.id, "remove", "success")
        self._run_optional_hook(manifest, "postuninstall")
        self._run_optional_hook(manifest, "preinstall")
        self.adapter.install(manifest)
        self._emit("reinstall", manifest.id, "install", "success")
        self._run_optional_hook(manifest, "postinstall")
        self._run_optional_hook(manifest, "prestart")
        self.adapter.start(manifest.id)
        self._emit("reinstall", manifest.id, "start", "success")
        self._run_optional_hook(manifest, "poststart")
        return self.events

    def update_app(self, manifest: AppManifest) -> list[OperationEvent]:
        self._emit("update", manifest.id, "prepare", "running")
        self._run_optional_hook(manifest, "preflight")
        self._run_optional_hook(manifest, "preupdate")
        try:
            self.adapter.update(manifest)
            self._emit("update", manifest.id, "update", "success")
        except Exception:
            self._run_optional_hook(manifest, "rollback")
            self._emit("update", manifest.id, "rollback", "success")
            raise
        return self.events
