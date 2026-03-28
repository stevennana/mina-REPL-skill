from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import TranscriptEntry, utc_now_iso


class TranscriptRecorder:
    """Durable transcript recorder for REPL sessions."""

    def __init__(self) -> None:
        self.entries: list[TranscriptEntry] = []

    def add(self, role: str, mode: str, content: str, metadata: dict | None = None) -> TranscriptEntry:
        entry = TranscriptEntry(
            timestamp=utc_now_iso(),
            role=role,
            mode=mode,
            content=content,
            metadata=metadata or {},
        )
        self.entries.append(entry)
        return entry

    def last(self, limit: int = 10) -> list[TranscriptEntry]:
        if limit <= 0:
            return []
        return self.entries[-limit:]

    def export_jsonl(self, path: str | Path) -> Path:
        out = Path(path).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as handle:
            for entry in self.entries:
                handle.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")
        return out

    def export_markdown(self, path: str | Path) -> Path:
        out = Path(path).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        lines = ["# REPL Transcript", ""]
        for entry in self.entries:
            lines.append(f"## {entry.timestamp} [{entry.role}] [{entry.mode}]")
            lines.append("")
            lines.append("```text")
            lines.append(entry.content.rstrip())
            lines.append("```")
            if entry.metadata:
                lines.append("")
                lines.append("Metadata:")
                lines.append("")
                lines.append("```json")
                lines.append(json.dumps(entry.metadata, ensure_ascii=False, indent=2))
                lines.append("```")
            lines.append("")
        out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        return out
