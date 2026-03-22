import pytest

from app.modules.catalog.service import (
    AppManifest,
    DependencyCycleError,
    DependencyResolver,
    ManifestScanner,
    PortConflictValidator,
)

pytestmark = [pytest.mark.unit, pytest.mark.content_updates]


def test_manifest_scanner_loads_app_catalog() -> None:
    manifests = ManifestScanner().scan()
    assert len(manifests) >= 8
    assert manifests[0].id
    assert any(manifest.id == "nomad_sample_notes" for manifest in manifests)


def test_dependency_resolver_orders_dependencies() -> None:
    manifests = [
        AppManifest.model_validate(
            {
                "id": "dep",
                "kind": "dependency_app",
                "display": {
                    "name": "Dep",
                    "description": "Dependency",
                    "icon": "IconPlug",
                    "order": 1,
                },
                "runtime": {"image": "dep:latest"},
                "network": {"join": "project-nomad_default"},
                "storage": {"requires": []},
                "dependencies": [],
                "healthcheck": {"type": "http", "target": "http://dep"},
                "hooks": {},
                "updates": {},
                "permissions": {},
                "capabilities": {},
                "docs": {"slug": "dep"},
                "tests": {"smoke": "dep"},
            }
        ),
        AppManifest.model_validate(
            {
                "id": "app",
                "kind": "sibling_app",
                "display": {
                    "name": "App",
                    "description": "Application",
                    "icon": "IconAppWindow",
                    "order": 2,
                },
                "runtime": {"image": "app:latest"},
                "network": {"join": "project-nomad_default"},
                "storage": {"requires": []},
                "dependencies": ["dep"],
                "healthcheck": {"type": "http", "target": "http://app"},
                "hooks": {},
                "updates": {},
                "permissions": {},
                "capabilities": {},
                "docs": {"slug": "app"},
                "tests": {"smoke": "app"},
            }
        ),
    ]

    order = DependencyResolver().resolve_install_order(manifests)

    assert order == ["dep", "app"]


def test_dependency_resolver_detects_cycle() -> None:
    manifests = [
        AppManifest.model_validate(
            {
                "id": "a",
                "kind": "sibling_app",
                "display": {"name": "A", "description": "A", "icon": "IconA", "order": 1},
                "runtime": {"image": "a:latest"},
                "network": {"join": "project-nomad_default"},
                "storage": {"requires": []},
                "dependencies": ["b"],
                "healthcheck": {"type": "http", "target": "http://a"},
                "hooks": {},
                "updates": {},
                "permissions": {},
                "capabilities": {},
                "docs": {"slug": "a"},
                "tests": {"smoke": "a"},
            }
        ),
        AppManifest.model_validate(
            {
                "id": "b",
                "kind": "sibling_app",
                "display": {"name": "B", "description": "B", "icon": "IconB", "order": 2},
                "runtime": {"image": "b:latest"},
                "network": {"join": "project-nomad_default"},
                "storage": {"requires": []},
                "dependencies": ["a"],
                "healthcheck": {"type": "http", "target": "http://b"},
                "hooks": {},
                "updates": {},
                "permissions": {},
                "capabilities": {},
                "docs": {"slug": "b"},
                "tests": {"smoke": "b"},
            }
        ),
    ]

    with pytest.raises(DependencyCycleError):
        DependencyResolver().resolve_install_order(manifests)


def test_port_conflict_validator_rejects_duplicate_ports() -> None:
    manifests = [
        AppManifest.model_validate(
            {
                "id": "a",
                "kind": "sibling_app",
                "display": {"name": "A", "description": "A", "icon": "IconA", "order": 1},
                "runtime": {"image": "a:latest", "ports": [{"host": 8080, "container": 8080}]},
                "network": {"join": "project-nomad_default"},
                "storage": {"requires": []},
                "dependencies": [],
                "healthcheck": {"type": "http", "target": "http://a"},
                "hooks": {},
                "updates": {},
                "permissions": {},
                "capabilities": {},
                "docs": {"slug": "a"},
                "tests": {"smoke": "a"},
            }
        ),
        AppManifest.model_validate(
            {
                "id": "b",
                "kind": "sibling_app",
                "display": {"name": "B", "description": "B", "icon": "IconB", "order": 2},
                "runtime": {"image": "b:latest", "ports": [{"host": 8080, "container": 9090}]},
                "network": {"join": "project-nomad_default"},
                "storage": {"requires": []},
                "dependencies": [],
                "healthcheck": {"type": "http", "target": "http://b"},
                "hooks": {},
                "updates": {},
                "permissions": {},
                "capabilities": {},
                "docs": {"slug": "b"},
                "tests": {"smoke": "b"},
            }
        ),
    ]

    with pytest.raises(ValueError):
        PortConflictValidator().validate(manifests)


def test_manifest_validation_rejects_blank_ids_and_invalid_hooks() -> None:
    with pytest.raises(ValueError, match="manifest id must not be blank"):
        AppManifest.model_validate(
            {
                "id": " ",
                "kind": "sibling_app",
                "display": {"name": "A", "description": "A", "icon": "IconA", "order": 1},
                "runtime": {"image": "a:latest"},
                "network": {"join": "project-nomad_default"},
                "storage": {"requires": []},
                "dependencies": [],
                "healthcheck": {"type": "http", "target": "http://a"},
                "hooks": {},
                "updates": {},
                "permissions": {},
                "capabilities": {},
                "docs": {"slug": "a"},
                "tests": {"smoke": "apps/a/tests/test_smoke.py"},
            }
        )

    with pytest.raises(ValueError, match="hook preinstall must point to a dotted python reference"):
        AppManifest.model_validate(
            {
                "id": "sample-app",
                "kind": "sibling_app",
                "display": {"name": "A", "description": "A", "icon": "IconA", "order": 1},
                "runtime": {"image": "a:latest"},
                "network": {"join": "project-nomad_default"},
                "storage": {"requires": []},
                "dependencies": [],
                "healthcheck": {"type": "http", "target": "http://a"},
                "hooks": {"preinstall": "preinstall"},
                "updates": {},
                "permissions": {},
                "capabilities": {},
                "docs": {"slug": "a"},
                "tests": {"smoke": "apps/a/tests/test_smoke.py"},
            }
        )
