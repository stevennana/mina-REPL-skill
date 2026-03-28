import asyncio

from mina_repl_core import LocalShellBridge, ReplCoreSession


async def my_agent(user_text: str, session: ReplCoreSession) -> str:
    if user_text.lower().strip() == "ping":
        return "pong"
    return f"Agent received: {user_text}"


async def main() -> None:
    session = ReplCoreSession(
        assistant=my_agent,
        shell_bridge=LocalShellBridge(),
        history_path="~/.mina_repl_core/history.txt",
        transcript_path="~/.mina_repl_core/session.jsonl",
    )
    await session.run()


if __name__ == "__main__":
    asyncio.run(main())
