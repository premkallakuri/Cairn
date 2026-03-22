from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def test_kiwix_hook_seeds_demo_library(tmp_path: Path) -> None:
    hook_path = Path(__file__).resolve().parents[1] / "hooks.py"
    spec = spec_from_file_location("atlas_haven_kiwix_smoke_hooks", hook_path)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    destination = module.preinstall(target_dir=tmp_path)

    assert Path(destination).exists()
    assert Path(destination).name == "wikipedia_en_100_mini_2025-06.zim"
