from pathlib import Path

import pytest

from app.modules.catalog.scaffold import AppScaffolder, ScaffoldedAppSpec
from app.modules.catalog.service import ManifestScanner

pytestmark = [pytest.mark.unit, pytest.mark.platform]


def test_app_scaffolder_writes_a_catalog_valid_package(tmp_path: Path) -> None:
    scaffolded = AppScaffolder(workspace_root=tmp_path).scaffold(
        ScaffoldedAppSpec(
            package_name="sample-widget",
            display_name="Sample Widget",
            description="A tiny sample package used to prove app scaffolding.",
            include_hook_stub=True,
        )
    )

    assert (scaffolded / "app.yaml").exists()
    assert (scaffolded / "docs" / "overview.md").exists()
    assert (scaffolded / "tests" / "test_smoke.py").exists()
    assert (scaffolded / "hooks.py").exists()

    manifests = ManifestScanner(root=tmp_path / "apps").scan()

    assert [manifest.id for manifest in manifests] == ["nomad_sample_widget"]
