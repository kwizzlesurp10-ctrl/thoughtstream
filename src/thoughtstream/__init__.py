"""
ThoughtStream package initializer.

Provides easy access to the public API surface exposed by the package.
"""

from .config import DEFAULT_CONFIG_PATH, ThoughtStreamConfig, load_config
from .daemon import ThoughtStreamDaemon

__all__ = [
    "DEFAULT_CONFIG_PATH",
    "ThoughtStreamConfig",
    "ThoughtStreamDaemon",
    "load_config",
]

__version__ = "0.1.0"
