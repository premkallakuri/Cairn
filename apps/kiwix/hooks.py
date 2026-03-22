from pathlib import Path

from app.modules.zim.service import KiwixSeedService


def preinstall(target_dir: str | Path | None = None) -> str:
    resolved_target = Path(target_dir) if target_dir is not None else None
    return str(KiwixSeedService().seed_demo_zim(resolved_target))
