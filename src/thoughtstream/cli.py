from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Optional

import typer

from .config import DEFAULT_CONFIG_PATH, ThoughtStreamConfig, load_config
from .daemon import ThoughtStreamDaemon

app = typer.Typer(add_completion=False, no_args_is_help=True)


def configure_logging(verbosity: int) -> None:
    """Configure logging level based on verbosity flag."""
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def _load_config(path: Optional[Path]) -> ThoughtStreamConfig:
    try:
        return load_config(path)
    except FileNotFoundError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    except ValueError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc


@app.command()
def daemon(
    duration: float = typer.Option(
        None,
        help="Optional duration (seconds) to run before exiting automatically.",
    ),
    config: Path = typer.Option(
        DEFAULT_CONFIG_PATH,
        "--config",
        "-c",
        help="Path to the ThoughtStream configuration file.",
        exists=False,
    ),
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        help="Increase log verbosity (use -vv for debug).",
    ),
) -> None:
    """Start the ThoughtStream daemon."""
    configure_logging(verbose)
    cfg = _load_config(config)
    daemon_instance = ThoughtStreamDaemon(cfg)

    try:
        asyncio.run(daemon_instance.run(duration=duration))
    except KeyboardInterrupt:
        typer.secho("Received interrupt. Stopping daemon...", fg=typer.colors.YELLOW)
    finally:
        typer.secho("ThoughtStream daemon stopped.", fg=typer.colors.GREEN)


def main() -> None:
    """Entry point used by the console script."""
    app()


if __name__ == "__main__":
    main()

