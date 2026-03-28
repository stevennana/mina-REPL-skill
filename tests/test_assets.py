from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_NAMES = ("manifest.yaml", "contracts.yaml", "best_practices.yaml", "sources.yaml")


class AssetSyncTests(unittest.TestCase):
    def test_packaged_assets_match_canonical_skill_assets(self) -> None:
        skill_dir = ROOT
        packaged_dir = ROOT / "src" / "mina_repl_core" / "data"

        for name in ASSET_NAMES:
            self.assertEqual(
                (skill_dir / name).read_text(encoding="utf-8"),
                (packaged_dir / name).read_text(encoding="utf-8"),
            )

    def test_sync_script_check_mode_passes_when_assets_match(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "sync_skill_assets.py"), "--check"],
            capture_output=True,
            text=True,
            check=False,
            cwd=ROOT,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
