from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.zim]


def test_kiwix_preinstall_hook_seeds_demo_zim(tmp_path: Path) -> None:
    hook_path = Path(__file__).resolve().parents[3] / "apps" / "kiwix" / "hooks.py"
    spec = spec_from_file_location("atlas_haven_kiwix_hooks", hook_path)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    destination = module.preinstall(target_dir=tmp_path)

    seeded_file = Path(destination)
    assert seeded_file.exists()
    assert seeded_file.name == "wikipedia_en_100_mini_2025-06.zim"
    assert seeded_file.read_bytes() == b"atlas-haven-demo-zim"
