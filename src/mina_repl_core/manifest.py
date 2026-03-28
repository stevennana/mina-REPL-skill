from __future__ import annotations

from importlib.resources import files
from typing import Any

import yaml

from .models import SkillManifest, SourceNote


def _load_yaml(name: str) -> dict[str, Any]:
    raw = files("mina_repl_core.data").joinpath(name).read_text(encoding="utf-8")
    return yaml.safe_load(raw)


def load_skill_manifest() -> SkillManifest:
    data = _load_yaml("manifest.yaml")["skill"]
    return SkillManifest(
        id=data["id"],
        version=data["version"],
        kind=data["kind"],
        title=data["title"],
        description=data["description"],
        status=data["status"],
        capabilities=list(data["capabilities"]),
        modes=list(data["modes"]),
        recommended_runtime=dict(data["recommended_runtime"]),
        packaging=dict(data["packaging"]),
        integration_points=list(data["integration_points"]),
        included_files=dict(data["included_files"]),
    )


def load_source_catalog() -> list[SourceNote]:
    data = _load_yaml("sources.yaml")["sources"]
    return [
        SourceNote(
            id=item["id"],
            title=item["title"],
            url=item["url"],
            kind=item["kind"],
            role=item["role"],
            why_it_matters=item["why_it_matters"],
            extracted_guidance=list(item["extracted_guidance"]),
        )
        for item in data
    ]


def load_contracts() -> dict[str, Any]:
    return _load_yaml("contracts.yaml")


def load_best_practices() -> dict[str, Any]:
    return _load_yaml("best_practices.yaml")
