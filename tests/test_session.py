from __future__ import annotations

import asyncio
import io
import tempfile
import unittest
from pathlib import Path

from rich.console import Console

from _support import configure_src_path

configure_src_path()

from mina_repl_core import ReplCoreSession
from mina_repl_core.models import ShellResult
from mina_repl_core.shell import BaseShellBridge


class StubShellBridge(BaseShellBridge):
    async def run(self, command: str, on_chunk=None) -> ShellResult:
        if on_chunk is not None:
            maybe = on_chunk("stdout", "stub output\n")
            if asyncio.iscoroutine(maybe):
                await maybe
        return ShellResult(
            command=command,
            exit_code=0,
            stdout="stub output\n",
            stderr="",
            started_at="2026-03-28T00:00:00+00:00",
            finished_at="2026-03-28T00:00:01+00:00",
            duration_seconds=1.0,
        )


class SessionTests(unittest.TestCase):
    def make_session(self) -> tuple[ReplCoreSession, Console]:
        console = Console(record=True, width=120, file=io.StringIO())
        session = ReplCoreSession(
            assistant=lambda text, _: f"echo:{text}",
            shell_bridge=StubShellBridge(),
            history_path=None,
            transcript_path=None,
            console=console,
            extra_slash_commands=["/custom"],
        )
        return session, console

    def test_mode_switch_and_unknown_command_render(self) -> None:
        async def _run() -> None:
            session, console = self.make_session()
            await session._handle_slash_command("/mode shell")
            await session._handle_slash_command("/unknown")
            self.assertEqual(session.state.mode, "shell")
            output = console.export_text()
            self.assertIn("Mode changed to:", output)
            self.assertIn("Unknown slash command:", output)

        asyncio.run(_run())

    def test_run_command_records_shell_metadata(self) -> None:
        async def _run() -> None:
            session, _ = self.make_session()
            await session._handle_slash_command("/run echo demo")
            entry = session.transcript.last(1)[0]
            self.assertEqual(entry.role, "shell")
            self.assertEqual(entry.content, "echo demo")
            self.assertEqual(entry.metadata["exit_code"], 0)

        asyncio.run(_run())

    def test_transcript_export_and_render_helpers(self) -> None:
        async def _run() -> None:
            session, console = self.make_session()
            session.transcript.add("user", "chat", "hello")
            session.transcript.add("assistant", "chat", "world")
            session._render_status()
            session._render_history(["1"])
            output = console.export_text()
            self.assertIn("session status", output)
            self.assertIn("last 1 transcript entries", output)

            with tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "session.md"
                session._export_transcript([str(out)])
                self.assertTrue(out.exists())
                self.assertIn("# REPL Transcript", out.read_text(encoding="utf-8"))

        asyncio.run(_run())


if __name__ == "__main__":
    unittest.main()
