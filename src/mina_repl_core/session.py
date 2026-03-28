from __future__ import annotations

import asyncio
import inspect
import shlex
from pathlib import Path
from typing import Awaitable, Callable, Iterable

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory, InMemoryHistory
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .manifest import load_skill_manifest, load_source_catalog
from .models import SessionState
from .shell import BaseShellBridge, LocalShellBridge
from .transcript import TranscriptRecorder

AssistantCallback = Callable[[str, "ReplCoreSession"], Awaitable[str] | str]


class ReplCoreSession:
    """Prompt-toolkit based REPL runtime for multi-turn AI agents."""

    BUILTIN_COMMANDS = [
        "/help",
        "/mode",
        "/status",
        "/history",
        "/sources",
        "/skill",
        "/run",
        "/transcript",
        "/clear",
        "/quit",
    ]

    def __init__(
        self,
        *,
        assistant: AssistantCallback | None = None,
        shell_bridge: BaseShellBridge | None = None,
        history_path: str | None = "~/.mina_repl_core/history.txt",
        transcript_path: str | None = "~/.mina_repl_core/session.jsonl",
        extra_slash_commands: Iterable[str] | None = None,
        console: Console | None = None,
    ) -> None:
        self.assistant = assistant or self._default_assistant
        self.shell_bridge = shell_bridge or LocalShellBridge()
        self.state = SessionState(
            mode="chat",
            running=True,
            history_path=history_path,
            transcript_path=transcript_path,
        )
        self.transcript = TranscriptRecorder()
        self.manifest = load_skill_manifest()
        self.sources = load_source_catalog()
        self.console = console or Console()
        # These are completion hints for custom commands implemented by
        # subclasses or wrapper dispatchers.
        self.extra_slash_commands = sorted(set(extra_slash_commands or []))
        self._prompt_session = PromptSession(
            completer=WordCompleter(
                self.BUILTIN_COMMANDS + self.extra_slash_commands + ["chat", "shell", "multiline"],
                ignore_case=True,
                sentence=True,
            ),
            history=self._make_history(history_path),
        )

    def _make_history(self, history_path: str | None):
        if history_path:
            return FileHistory(str(Path(history_path).expanduser()))
        return InMemoryHistory()

    async def run(self) -> None:
        self._render_banner()
        while self.state.running:
            try:
                prompt_text = self._prompt_label()
                text = await self._prompt_session.prompt_async(
                    prompt_text,
                    multiline=(self.state.mode == "multiline"),
                )
            except KeyboardInterrupt:
                self.console.print("[yellow]Cancelled current input.[/yellow]")
                continue
            except EOFError:
                self.console.print("\n[cyan]Exiting REPL.[/cyan]")
                break

            cleaned = text.strip()
            if not cleaned:
                continue

            self.transcript.add("user", self.state.mode, cleaned)

            if cleaned.startswith("/"):
                await self._handle_slash_command(cleaned)
                continue

            if self.state.mode == "shell":
                await self._execute_shell(cleaned)
                continue

            await self._handle_chat(cleaned)

        await self._auto_export_transcript()

    async def _auto_export_transcript(self) -> None:
        if self.state.transcript_path and self.transcript.entries:
            path = self.transcript.export_jsonl(self.state.transcript_path)
            self.console.print(f"[dim]Transcript saved to {path}[/dim]")

    async def _handle_chat(self, text: str) -> None:
        result = self.assistant(text, self)
        response = await result if inspect.isawaitable(result) else result
        response = str(response)
        self.transcript.add("assistant", self.state.mode, response)
        self.console.print(Panel(Markdown(response), title="assistant", border_style="cyan"))

    async def _execute_shell(self, command: str) -> None:
        self.console.print(Panel(Text(command), title="shell command", border_style="magenta"))

        async def on_chunk(channel: str, chunk: str) -> None:
            style = "dim" if channel == "stdout" else "red"
            end = "" if chunk.endswith("\n") else "\n"
            self.console.print(chunk.rstrip("\n"), style=style, end=end)

        result = await self.shell_bridge.run(command, on_chunk=on_chunk)
        self.transcript.add(
            "shell",
            self.state.mode,
            command,
            metadata={
                "exit_code": result.exit_code,
                "duration_seconds": round(result.duration_seconds, 4),
            },
        )
        table = Table(title="shell result")
        table.add_column("field")
        table.add_column("value")
        table.add_row("exit_code", str(result.exit_code))
        table.add_row("duration_seconds", f"{result.duration_seconds:.4f}")
        table.add_row("started_at", result.started_at)
        table.add_row("finished_at", result.finished_at)
        self.console.print(table)
        if result.stderr and not result.stderr.endswith("\n"):
            self.console.print(result.stderr, style="red")

    async def _handle_slash_command(self, text: str) -> None:
        try:
            parts = shlex.split(text[1:])
        except ValueError as exc:
            self.console.print(f"[red]Command parse error:[/red] {exc}")
            return
        if not parts:
            return
        name, *args = parts

        if name == "help":
            self.console.print(self._help_panel())
            return
        if name == "mode":
            await self._command_mode(args)
            return
        if name == "status":
            self._render_status()
            return
        if name == "history":
            self._render_history(args)
            return
        if name == "sources":
            self._render_sources()
            return
        if name == "skill":
            self._render_skill()
            return
        if name == "run":
            if not args:
                self.console.print("[red]/run requires a shell command[/red]")
                return
            await self._execute_shell(" ".join(args))
            return
        if name == "transcript":
            self._export_transcript(args)
            return
        if name == "clear":
            self.console.clear()
            self._render_banner()
            return
        if name == "quit":
            self.state.running = False
            return

        self.console.print(f"[yellow]Unknown slash command:[/yellow] /{name}")

    async def _command_mode(self, args: list[str]) -> None:
        if not args:
            self.console.print(f"[cyan]Current mode:[/cyan] {self.state.mode}")
            return
        target = args[0].lower()
        if target not in {"chat", "shell", "multiline"}:
            self.console.print("[red]Mode must be one of: chat, shell, multiline[/red]")
            return
        self.state.mode = target
        self.console.print(f"[green]Mode changed to:[/green] {self.state.mode}")

    def _render_banner(self) -> None:
        title = f"{self.manifest.title} ({self.manifest.id} v{self.manifest.version})"
        body = "\n".join(
            [
                "REPL-first runtime for multi-turn AI agents",
                "Type /help for commands",
                "Ctrl-C cancels current input, Ctrl-D exits",
            ]
        )
        self.console.print(Panel(body, title=title, border_style="blue"))

    def _render_status(self) -> None:
        table = Table(title="session status")
        table.add_column("field")
        table.add_column("value")
        table.add_row("mode", self.state.mode)
        table.add_row("history_path", self.state.history_path or "(memory)")
        table.add_row("transcript_path", self.state.transcript_path or "(manual export)")
        table.add_row("entries", str(len(self.transcript.entries)))
        table.add_row("assistant", getattr(self.assistant, "__name__", self.assistant.__class__.__name__))
        table.add_row("shell_bridge", self.shell_bridge.__class__.__name__)
        self.console.print(table)

    def _render_history(self, args: list[str]) -> None:
        limit = 10
        if args:
            try:
                limit = max(1, int(args[0]))
            except ValueError:
                self.console.print("[red]History limit must be an integer[/red]")
                return

        table = Table(title=f"last {limit} transcript entries")
        table.add_column("timestamp")
        table.add_column("role")
        table.add_column("mode")
        table.add_column("content")
        for entry in self.transcript.last(limit):
            table.add_row(entry.timestamp, entry.role, entry.mode, entry.content[:120])
        self.console.print(table)

    def _render_sources(self) -> None:
        table = Table(title="included sources")
        table.add_column("id")
        table.add_column("title")
        table.add_column("role")
        table.add_column("url")
        for source in self.sources:
            table.add_row(source.id, source.title, source.role, source.url)
        self.console.print(table)

    def _render_skill(self) -> None:
        table = Table(title="skill summary")
        table.add_column("field")
        table.add_column("value")
        table.add_row("id", self.manifest.id)
        table.add_row("version", self.manifest.version)
        table.add_row("kind", self.manifest.kind)
        table.add_row("title", self.manifest.title)
        table.add_row("status", self.manifest.status)
        table.add_row("capabilities", ", ".join(self.manifest.capabilities))
        table.add_row("modes", ", ".join(self.manifest.modes))
        self.console.print(table)

    def _export_transcript(self, args: list[str]) -> None:
        target = args[0] if args else self.state.transcript_path
        if not target:
            self.console.print("[red]No transcript path configured[/red]")
            return
        if target.endswith(".md"):
            out = self.transcript.export_markdown(target)
        else:
            out = self.transcript.export_jsonl(target)
        self.console.print(f"[green]Transcript exported:[/green] {out}")

    def _help_panel(self) -> Panel:
        markdown = """\
# Built-in commands

- `/help`
- `/mode <chat|shell|multiline>`
- `/status`
- `/history [n]`
- `/sources`
- `/skill`
- `/run <shell command>`
- `/transcript [path]`
- `/clear`
- `/quit`

## Modes

- `chat`: send plain input to your assistant callback
- `shell`: treat plain input as shell commands
- `multiline`: ask prompt_toolkit for multiline input before submission
"""
        return Panel(Markdown(markdown), title="help", border_style="green")

    def _prompt_label(self) -> str:
        if self.state.mode == "shell":
            return "shell> "
        if self.state.mode == "multiline":
            return "multi> "
        return "agent> "

    async def _default_assistant(self, user_text: str, _: "ReplCoreSession") -> str:
        return (
            "This is the bundled demo assistant.\n\n"
            f"You said: `{user_text}`\n\n"
            "Replace the `assistant` callback in `ReplCoreSession` with your real agent."
        )
