from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillLayoutTests(unittest.TestCase):
    def test_root_skill_files_exist(self) -> None:
        required = (
            "SKILL.md",
            "manifest.yaml",
            "contracts.yaml",
            "best_practices.yaml",
            "sources.yaml",
        )
        for name in required:
            self.assertTrue((ROOT / name).exists(), msg=f"missing root skill file: {name}")

    def test_agents_metadata_exists(self) -> None:
        self.assertTrue((ROOT / "agents" / "openai.yaml").exists())

    def test_references_layer_exists(self) -> None:
        references = ROOT / "references"
        self.assertTrue(references.exists())
        for name in (
            "repl-runtime-contract.md",
            "repl-approval-and-autonomy.md",
            "repl-session-lifecycle.md",
            "repl-plan-build-modes.md",
            "repl-architecture.md",
            "repl-extension-points.md",
            "repl-terminal-ui-best-practices.md",
            "repl-source-baseline.md",
            "repl-design-opencode.md",
        ):
            self.assertTrue((references / name).exists(), msg=f"missing reference file: {name}")


if __name__ == "__main__":
    unittest.main()
