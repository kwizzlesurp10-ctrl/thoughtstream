from __future__ import annotations

import asyncio

from thoughtstream.config import ThoughtStreamConfig
from thoughtstream.daemon import ThoughtStreamDaemon


def _build_config(poll_interval: float = 0.01) -> ThoughtStreamConfig:
    return ThoughtStreamConfig.model_validate(
        {
            "capture": {"poll_interval": poll_interval},
        }
    )


def test_daemon_runs_for_fixed_duration() -> None:
    daemon = ThoughtStreamDaemon(_build_config())
    asyncio.run(daemon.run(duration=0.05))


def test_daemon_respects_stop_signal() -> None:
    daemon = ThoughtStreamDaemon(_build_config())

    async def runner() -> None:
        stopper = asyncio.create_task(_request_stop())
        try:
            await daemon.run()
        finally:
            stopper.cancel()

    async def _request_stop() -> None:
        await asyncio.sleep(0.05)
        daemon.stop()

    asyncio.run(runner())

