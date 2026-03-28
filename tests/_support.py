from __future__ import annotations

import sys
from pathlib import Path


def configure_src_path() -> None:
    src = Path(__file__).resolve().parents[1] / "src"
    src_str = str(src)
    if src_str not in sys.path:
        sys.path.insert(0, src_str)
