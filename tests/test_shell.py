import asyncio
import unittest

from _support import configure_src_path

configure_src_path()

from mina_repl_core import LocalShellBridge


class ShellTests(unittest.TestCase):
    def test_local_shell_bridge(self) -> None:
        async def _run() -> None:
            bridge = LocalShellBridge()
            result = await bridge.run("echo hello")
            self.assertEqual(result.exit_code, 0)
            self.assertIn("hello", result.stdout)
            self.assertGreaterEqual(result.duration_seconds, 0.0)

        asyncio.run(_run())


if __name__ == "__main__":
    unittest.main()
