"""YAML configuration loading utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML file from disk.

    Args:
        path: Path to a YAML configuration file.

    Returns:
        Parsed configuration dictionary.
    """

    data = Path(path).read_text(encoding="utf-8")
    return yaml.safe_load(data)
