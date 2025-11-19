from __future__ import annotations

from pathlib import Path

import pytest

from thoughtstream.config import (
    DEFAULT_DATABASE_PATH,
    ThoughtStreamConfig,
    load_config,
    load_raw_config,
)


def test_load_raw_config_rejects_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "config.yaml"
    with pytest.raises(FileNotFoundError):
        load_raw_config(missing)


def test_load_config_round_trip(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
        database:
          path: "~/custom-db.sqlite"
        capture:
          poll_interval: 0.1
          blacklist_apps:
            - firefox:password
        """,
        encoding="utf-8",
    )

    config = load_config(config_path)
    assert isinstance(config, ThoughtStreamConfig)
    assert config.capture.poll_interval == pytest.approx(0.1)
    assert config.database.path.name == "custom-db.sqlite"
    assert "firefox:password" in config.capture.blacklist_apps


def test_load_config_defaults(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text("{}", encoding="utf-8")

    config = load_config(config_path)
    assert config.database.path == DEFAULT_DATABASE_PATH
    assert config.capture.poll_interval == pytest.approx(5.0)

