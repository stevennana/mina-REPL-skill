from __future__ import annotations

import asyncio
import inspect
from abc import ABC, abstractmethod
from typing import Awaitable, Callable

from .models import ShellResult, utc_now_iso

StreamCallback = Callable[[str, str], Awaitable[None] | None]


class BaseShellBridge(ABC):
    @abstractmethod
    async def run(self, command: str, on_chunk: StreamCallback | None = None) -> ShellResult:
        raise NotImplementedError


class LocalShellBridge(BaseShellBridge):
    """Async local shell bridge built on asyncio subprocesses."""

    async def run(self, command: str, on_chunk: StreamCallback | None = None) -> ShellResult:
        started = asyncio.get_running_loop().time()
        started_at = utc_now_iso()
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout_parts: list[str] = []
        stderr_parts: list[str] = []

        async def drain(stream: asyncio.StreamReader | None, channel: str, bucket: list[str]) -> None:
            if stream is None:
                return
            while True:
                chunk = await stream.readline()
                if not chunk:
                    break
                text = chunk.decode(errors="replace")
                bucket.append(text)
                if on_chunk is not None:
                    maybe = on_chunk(channel, text)
                    if inspect.isawaitable(maybe):
                        await maybe

        await asyncio.gather(
            drain(process.stdout, "stdout", stdout_parts),
            drain(process.stderr, "stderr", stderr_parts),
        )
        exit_code = await process.wait()
        finished_at = utc_now_iso()
        duration = asyncio.get_running_loop().time() - started

        return ShellResult(
            command=command,
            exit_code=exit_code,
            stdout="".join(stdout_parts),
            stderr="".join(stderr_parts),
            started_at=started_at,
            finished_at=finished_at,
            duration_seconds=duration,
        )


class AsyncSSHShellBridge(BaseShellBridge):
    """Optional async SSH bridge using AsyncSSH."""

    def __init__(
        self,
        host: str,
        *,
        username: str | None = None,
        port: int = 22,
        known_hosts: str | None = None,
        client_keys: list[str] | None = None,
        password: str | None = None,
    ) -> None:
        self.host = host
        self.username = username
        self.port = port
        self.known_hosts = known_hosts
        self.client_keys = client_keys
        self.password = password

    async def run(self, command: str, on_chunk: StreamCallback | None = None) -> ShellResult:
        try:
            import asyncssh  # type: ignore
        except Exception as exc:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "AsyncSSH is not installed. Install with: pip install -e .[ssh]"
            ) from exc

        started = asyncio.get_running_loop().time()
        started_at = utc_now_iso()
        stdout_parts: list[str] = []
        stderr_parts: list[str] = []

        async with asyncssh.connect(
            self.host,
            username=self.username,
            port=self.port,
            known_hosts=self.known_hosts,
            client_keys=self.client_keys,
            password=self.password,
        ) as conn:
            process = await conn.create_process(command)

            async def drain(stream, channel: str, bucket: list[str]) -> None:
                async for text in stream:
                    bucket.append(text)
                    if on_chunk is not None:
                        maybe = on_chunk(channel, text)
                        if inspect.isawaitable(maybe):
                            await maybe

            await asyncio.gather(
                drain(process.stdout, "stdout", stdout_parts),
                drain(process.stderr, "stderr", stderr_parts),
            )
            await process.wait_closed()
            exit_code = int(process.exit_status or 0)

        finished_at = utc_now_iso()
        duration = asyncio.get_running_loop().time() - started

        return ShellResult(
            command=command,
            exit_code=exit_code,
            stdout="".join(stdout_parts),
            stderr="".join(stderr_parts),
            started_at=started_at,
            finished_at=finished_at,
            duration_seconds=duration,
        )
