from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class SourceNote:
    id: str
    title: str
    url: str
    kind: str
    role: str
    why_it_matters: str
    extracted_guidance: list[str]


@dataclass(slots=True)
class SkillManifest:
    id: str
    version: str
    kind: str
    title: str
    description: str
    status: str
    capabilities: list[str]
    modes: list[str]
    recommended_runtime: dict[str, str]
    packaging: dict[str, str]
    integration_points: list[str]
    included_files: dict[str, str]


@dataclass(slots=True)
class TranscriptEntry:
    timestamp: str
    role: str
    mode: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ShellResult:
    command: str
    exit_code: int
    stdout: str
    stderr: str
    started_at: str
    finished_at: str
    duration_seconds: float


@dataclass(slots=True)
class SessionState:
    mode: str = "chat"
    running: bool = True
    history_path: str | None = None
    transcript_path: str | None = None
