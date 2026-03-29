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
            "repl-context-engineering.md",
            "repl-prompt-composition.md",
            "repl-memory-and-model-config.md",
            "repl-prompt-templates.md",
            "repl-mcp-and-tool-registry.md",
            "repl-tool-selection-and-usage.md",
            "repl-tool-loop-and-turn-orchestration.md",
            "repl-orchestrator-guidance.md",
            "repl-plan-execution.md",
            "repl-approval-and-autonomy.md",
            "repl-session-lifecycle.md",
            "repl-plan-build-modes.md",
            "repl-three-surface-ux.md",
            "repl-architecture.md",
            "repl-extension-points.md",
            "repl-terminal-ui-best-practices.md",
            "repl-verification-and-evaluation.md",
            "repl-failure-and-recovery.md",
            "repl-maturity-matrix.md",
            "repl-source-traceability.md",
            "repl-subsystem-map-codex.md",
            "repl-subsystem-map-opencode.md",
            "repl-source-baseline.md",
            "repl-design-opencode.md",
        ):
            self.assertTrue((references / name).exists(), msg=f"missing reference file: {name}")

    def test_agents_metadata_mentions_skill_name(self) -> None:
        text = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("mina-repl-core", text)

    def test_traceability_reference_uses_status_vocabulary(self) -> None:
        text = (ROOT / "references" / "repl-source-traceability.md").read_text(encoding="utf-8")
        self.assertIn("Verified", text)
        self.assertIn("Inferred", text)
        self.assertIn("Recommended", text)


if __name__ == "__main__":
    unittest.main()
