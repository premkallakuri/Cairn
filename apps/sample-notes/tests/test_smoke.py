from pathlib import Path


def test_sample_notes_app_package_exists() -> None:
    assert (Path(__file__).resolve().parents[1] / "app.yaml").exists()
