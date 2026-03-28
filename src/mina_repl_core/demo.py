from __future__ import annotations

import asyncio

from .session import ReplCoreSession


async def demo_assistant(user_text: str, session: ReplCoreSession) -> str:
    lowered = user_text.lower().strip()

    if lowered in {"hi", "hello"}:
        return (
            "Hello. This is the `mina-repl-core` demo.\n\n"
            "Try `/help`, `/sources`, `/skill`, or `/run echo demo`."
        )

    if "source" in lowered:
        return (
            "This package bundles a source catalog under `sources.yaml` "
            "and deeper source guidance under `references/repl-source-baseline.md`."
        )

    if "mode" in lowered:
        return (
            "Use `/mode chat`, `/mode shell`, or `/mode multiline` to switch runtime behavior."
        )

    if "history" in lowered:
        return "Use `/history 5` to inspect the last five transcript entries."

    if "transcript" in lowered:
        return "Use `/transcript ./session.md` or let the session auto-save JSONL on exit."

    return (
        "This is a starter REPL skill, not a domain agent yet.\n\n"
        f"Input received: `{user_text}`\n\n"
        "Wire your own assistant callback into `ReplCoreSession` to make it project-specific."
    )


async def _main_async() -> None:
    session = ReplCoreSession(assistant=demo_assistant)
    await session.run()


def main() -> None:
    asyncio.run(_main_async())


if __name__ == "__main__":
    main()
