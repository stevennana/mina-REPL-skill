import unittest

from _support import configure_src_path

configure_src_path()

from mina_repl_core import load_contracts
from mina_repl_core import load_skill_manifest, load_source_catalog


class ManifestTests(unittest.TestCase):
    def test_manifest_loads(self) -> None:
        manifest = load_skill_manifest()
        self.assertEqual(manifest.id, "mina-repl-core")
        self.assertEqual(manifest.version, "0.1.0")
        self.assertIn("chat", manifest.modes)

    def test_sources_load(self) -> None:
        sources = load_source_catalog()
        self.assertTrue(any(source.id == "python.cmd" for source in sources))
        self.assertTrue(any(source.id == "prompt_toolkit.sqlite_repl" for source in sources))

    def test_contracts_include_documented_commands(self) -> None:
        contracts = load_contracts()
        self.assertIn("/quit", contracts["contracts"]["slash_commands"]["built_in"])


if __name__ == "__main__":
    unittest.main()
