from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator

DEFAULT_CONFIG_PATH = Path(os.path.expanduser("~/.config/thoughtstream/config.yaml"))
DEFAULT_DATABASE_PATH = Path(
    os.path.expanduser("~/.local/share/thoughtstream/thoughtstream.db")
)


def _expand_path(path_value: str | os.PathLike[str]) -> Path:
    """Expand user variables and environment markers in a filesystem path."""
    return Path(os.path.expanduser(str(path_value))).expanduser()


class DatabaseConfig(BaseModel):
    path: Path = Field(default_factory=lambda: DEFAULT_DATABASE_PATH)
    retention_days: int = 30

    @field_validator("path", mode="before")
    @classmethod
    def _expand(cls, value: str | os.PathLike[str]) -> Path:
        return _expand_path(value)


class LLMConfig(BaseModel):
    provider: str = "ollama"
    embedding_model: str = "nomic-embed-text"
    query_model: str = "llama3.2:3b"
    host: str = "http://localhost:11434"
    hybrid_search: bool = True


class CaptureConfig(BaseModel):
    blacklist_apps: List[str] = Field(default_factory=list)
    blacklist_dirs: List[Path] = Field(default_factory=list)
    poll_interval: float = 5.0

    @field_validator("blacklist_dirs", mode="before")
    @classmethod
    def _expand_dirs(cls, value: Iterable[str] | None) -> List[Path]:
        if value is None:
            return []
        return [_expand_path(item) for item in value]


class PrivacyConfig(BaseModel):
    encrypt: bool = False
    retention_policy: str = "keep_all_except_blacklist"


class ExportConfig(BaseModel):
    obsidian_vault: Path | None = None

    @field_validator("obsidian_vault", mode="before")
    @classmethod
    def _expand_vault(cls, value: str | os.PathLike[str] | None) -> Path | None:
        if value in (None, ""):
            return None
        return _expand_path(value)


class ThoughtStreamConfig(BaseModel):
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    capture: CaptureConfig = Field(default_factory=CaptureConfig)
    privacy: PrivacyConfig = Field(default_factory=PrivacyConfig)
    export: ExportConfig = Field(default_factory=ExportConfig)


def load_raw_config(path: Path) -> dict[str, Any]:
    """Load a raw configuration dictionary from a YAML file."""
    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file not found at {path}. "
            "Create it from config.yaml.example before starting the daemon."
        )

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ValueError(
            f"Configuration file at {path} must contain a YAML mapping at the top level."
        )

    return data


def load_config(path: Path | None = None) -> ThoughtStreamConfig:
    """Load and validate the ThoughtStream configuration."""
    resolved_path = _expand_path(path) if path else DEFAULT_CONFIG_PATH
    raw_config = load_raw_config(resolved_path)

    try:
        return ThoughtStreamConfig.model_validate(raw_config)
    except ValidationError as exc:
        raise ValueError(
            f"Invalid configuration values in {resolved_path}:\n{exc}"
        ) from exc


__all__ = [
    "CaptureConfig",
    "DEFAULT_CONFIG_PATH",
    "DEFAULT_DATABASE_PATH",
    "ThoughtStreamConfig",
    "load_config",
    "load_raw_config",
]

