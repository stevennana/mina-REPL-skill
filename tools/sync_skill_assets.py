from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIR = ROOT
PACKAGED_DIR = ROOT / "src" / "mina_repl_core" / "data"
ASSET_NAMES = ("manifest.yaml", "contracts.yaml", "best_practices.yaml", "sources.yaml")


def sync_assets(*, check: bool) -> int:
    PACKAGED_DIR.mkdir(parents=True, exist_ok=True)
    mismatches: list[str] = []

    for name in ASSET_NAMES:
        source = CANONICAL_DIR / name
        target = PACKAGED_DIR / name

        if not source.exists():
            raise FileNotFoundError(f"Missing canonical asset: {source}")

        source_text = source.read_text(encoding="utf-8")
        target_text = target.read_text(encoding="utf-8") if target.exists() else None

        if source_text == target_text:
            continue

        mismatches.append(name)
        if not check:
            shutil.copyfile(source, target)

    if mismatches:
        action = "out of sync" if check else "updated"
        print(f"Skill assets {action}: {', '.join(mismatches)}")
        return 1 if check else 0

    print("Skill assets are in sync.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Synchronize canonical skill YAML assets into packaged runtime data."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail instead of copying when packaged assets differ from the repo-root skill files.",
    )
    args = parser.parse_args()
    return sync_assets(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
