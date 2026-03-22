import json
import re
from dataclasses import dataclass
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, ValidationError, model_validator

from app.core.config import get_settings
from app.modules.catalog.repository import CatalogRepository


class DisplayConfig(BaseModel):
    name: str
    description: str
    icon: str
    powered_by: str | None = None
    order: int
    ui_location: str = "bridge"


class PortMapping(BaseModel):
    host: int
    container: int


class VolumeMount(BaseModel):
    source: str
    target: str


class RuntimeConfig(BaseModel):
    image: str | None = None
    command: list[str] = Field(default_factory=list)
    ports: list[PortMapping] = Field(default_factory=list)
    mounts: list[VolumeMount] = Field(default_factory=list)
    restart: str = "unless-stopped"
    builtin: bool = False


class StorageConfig(BaseModel):
    requires: list[str] = Field(default_factory=list)


class HealthcheckConfig(BaseModel):
    type: str
    target: str


class AppManifest(BaseModel):
    id: str
    kind: str
    display: DisplayConfig
    runtime: RuntimeConfig
    network: dict[str, object]
    storage: StorageConfig
    dependencies: list[str] = Field(default_factory=list)
    healthcheck: HealthcheckConfig
    hooks: dict[str, str] = Field(default_factory=dict)
    updates: dict[str, object] = Field(default_factory=dict)
    permissions: dict[str, object] = Field(default_factory=dict)
    capabilities: dict[str, object] = Field(default_factory=dict)
    docs: dict[str, object] = Field(default_factory=dict)
    tests: dict[str, object] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_runtime_requirements(self) -> "AppManifest":
        self._validate_identity_fields()
        self._validate_runtime_ports()
        self._validate_hook_targets()
        if self.kind != "core_capability" and not self.runtime.image:
            raise ValueError("runtime.image is required for non-core capabilities")
        if self.kind == "core_capability" and not (self.runtime.image or self.runtime.builtin):
            raise ValueError("core capabilities must declare runtime.builtin or runtime.image")
        return self

    def _validate_identity_fields(self) -> None:
        if not self.id.strip():
            raise ValueError("manifest id must not be blank")
        if self.id != self.id.strip():
            raise ValueError("manifest id must not contain leading or trailing whitespace")
        if not re.fullmatch(r"[a-z][a-z0-9_-]*", self.id):
            raise ValueError(
                "manifest id must use lowercase letters, numbers, underscores, or dashes"
            )
        if self.id in self.dependencies:
            raise ValueError("manifest dependencies must not include the app itself")

        if not self.display.name.strip():
            raise ValueError("display.name must not be blank")
        if not self.display.description.strip():
            raise ValueError("display.description must not be blank")
        if not self.display.icon.strip():
            raise ValueError("display.icon must not be blank")

        if not self.network.get("join"):
            raise ValueError("network.join must not be blank")

        if not self.docs.get("slug"):
            raise ValueError("docs.slug must not be blank")
        if not self.tests.get("smoke"):
            raise ValueError("tests.smoke must not be blank")

        requires = self.storage.requires
        if len(requires) != len({item.strip() for item in requires if item.strip()}):
            raise ValueError("storage.requires must not contain duplicate entries")
        if any(not item.strip() for item in requires):
            raise ValueError("storage.requires must not contain blank entries")

        if len(self.dependencies) != len(set(self.dependencies)):
            raise ValueError("dependencies must not contain duplicates")

    def _validate_runtime_ports(self) -> None:
        seen_hosts: set[int] = set()
        seen_containers: set[int] = set()
        for mapping in self.runtime.ports:
            if mapping.host <= 0 or mapping.container <= 0:
                raise ValueError("runtime.ports values must be positive integers")
            if mapping.host in seen_hosts:
                raise ValueError("runtime.ports host values must be unique")
            if mapping.container in seen_containers:
                raise ValueError("runtime.ports container values must be unique")
            seen_hosts.add(mapping.host)
            seen_containers.add(mapping.container)

    def _validate_hook_targets(self) -> None:
        for hook_name, hook_ref in self.hooks.items():
            if not hook_ref or "." not in hook_ref:
                raise ValueError(f"hook {hook_name} must point to a dotted python reference")
            module_path, function_name = hook_ref.rsplit(".", 1)
            if not module_path or not function_name:
                raise ValueError(f"hook {hook_name} must point to a valid python reference")


@dataclass(slots=True)
class ManifestValidationIssue:
    path: str
    message: str


class DependencyCycleError(ValueError):
    pass


class ManifestScanner:
    def __init__(self, root: Path | None = None) -> None:
        settings = get_settings()
        self.root = root or settings.resolved_app_catalog_path

    def scan(self) -> list[AppManifest]:
        manifests: list[AppManifest] = []
        for manifest_path in sorted(self.root.glob("*/app.yaml")):
            payload = yaml.safe_load(manifest_path.read_text())
            manifests.append(AppManifest.model_validate(payload))
        return manifests


class DependencyResolver:
    def resolve_install_order(self, manifests: list[AppManifest]) -> list[str]:
        manifest_ids = {manifest.id: manifest for manifest in manifests}
        visited: set[str] = set()
        active: set[str] = set()
        order: list[str] = []

        def visit(node_id: str) -> None:
            if node_id in active:
                raise DependencyCycleError(f"Dependency cycle detected for {node_id}")
            if node_id in visited:
                return
            active.add(node_id)
            manifest = manifest_ids[node_id]
            for dependency in manifest.dependencies:
                visit(dependency)
            active.remove(node_id)
            visited.add(node_id)
            order.append(node_id)

        for manifest in manifests:
            visit(manifest.id)

        return order


class PortConflictValidator:
    def validate(self, manifests: list[AppManifest]) -> None:
        seen: dict[int, str] = {}
        for manifest in manifests:
            for mapping in manifest.runtime.ports:
                if mapping.host in seen:
                    raise ValueError(
                        f"Host port {mapping.host} already used by {seen[mapping.host]}"
                    )
                seen[mapping.host] = manifest.id


class CatalogSyncService:
    def __init__(
        self, scanner: ManifestScanner | None = None, repository: CatalogRepository | None = None
    ) -> None:
        self.scanner = scanner or ManifestScanner()
        self.repository = repository or CatalogRepository()

    def sync_from_disk(self) -> list[AppManifest]:
        manifests = self.scanner.scan()
        DependencyResolver().resolve_install_order(manifests)
        PortConflictValidator().validate(manifests)

        for manifest in manifests:
            self.repository.upsert_catalog_entry(
                {
                    "service_name": manifest.id,
                    "kind": manifest.kind,
                    "friendly_name": manifest.display.name,
                    "description": manifest.display.description,
                    "icon": manifest.display.icon,
                    "powered_by": manifest.display.powered_by,
                    "display_order": manifest.display.order,
                    "container_image": manifest.runtime.image or "builtin://atlas-haven",
                    "ui_location": manifest.display.ui_location,
                    "manifest_json": json.dumps(manifest.model_dump(mode="json")),
                }
            )

        return manifests


def validate_manifest_payload(payload: dict[str, object]) -> AppManifest:
    try:
        return AppManifest.model_validate(payload)
    except ValidationError as exc:
        raise ValueError(str(exc)) from exc
