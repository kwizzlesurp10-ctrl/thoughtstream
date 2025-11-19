from __future__ import annotations

import asyncio
import logging
from typing import Optional

from .config import ThoughtStreamConfig

LOGGER = logging.getLogger(__name__)


class ThoughtStreamDaemon:
    """Minimal asynchronous daemon loop placeholder.

    The current implementation emits periodic heartbeat messages while waiting.
    It is intended as a scaffold for the fully featured data capture system
    described in the project roadmap.
    """

    def __init__(self, config: ThoughtStreamConfig) -> None:
        self.config = config
        self._stop_event = asyncio.Event()

    async def run(self, duration: float | None = None) -> None:
        """Run the daemon loop until stopped or the optional duration elapses."""
        loop = asyncio.get_running_loop()
        end_time: Optional[float] = None
        if duration is not None:
            if duration <= 0:
                return
            end_time = loop.time() + duration

        LOGGER.info(
            "ThoughtStream daemon starting | db=%s | poll=%.2fs",
            self.config.database.path,
            self.config.capture.poll_interval,
        )

        try:
            while not self._stop_event.is_set():
                if end_time is not None:
                    remaining = end_time - loop.time()
                    if remaining <= 0:
                        break
                    sleep_for = min(self.config.capture.poll_interval, remaining)
                else:
                    sleep_for = self.config.capture.poll_interval

                try:
                    await asyncio.wait_for(self._stop_event.wait(), timeout=sleep_for)
                except asyncio.TimeoutError:
                    self._emit_heartbeat()
                    continue
        finally:
            LOGGER.info("ThoughtStream daemon stopping")

    def stop(self) -> None:
        """Signal the daemon to stop at the next loop iteration."""
        self._stop_event.set()

    def _emit_heartbeat(self) -> None:
        LOGGER.debug("ThoughtStream heartbeat tick")


__all__ = ["ThoughtStreamDaemon"]

