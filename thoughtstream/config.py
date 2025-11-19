import yaml
import os
from pathlib import Path
from typing import Dict, Any

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "thoughtstream" / "config.yaml"

class Config:
    def __init__(self, config_path: Path = DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self.data: Dict[str, Any] = {}
        self.load()

    def load(self):
        if not self.config_path.exists():
            # Return defaults or raise error? For now, empty dict
            return

        with open(self.config_path, "r") as f:
            self.data = yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

config = Config()

