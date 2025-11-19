import typer
import asyncio
from rich.console import Console

# Move imports inside functions or after app creation if possible to debug circular imports
# But typer needs commands registered.

app = typer.Typer()
console = Console()

# Lazy imports to avoid circular dependency issues during module load
# if db or intelligence import daemon (which they shouldn't, but let's be safe)

@app.command()
def daemon():
    """Start the ThoughtStream daemon."""
    from .capture import hotkeys, clipboard, terminal, browser, vscode
    
    console.print("[green]Starting ThoughtStream Daemon...[/green]")
    
    import threading
    t = threading.Thread(target=hotkeys.start_hotkeys, daemon=True)
    t.start()

    async def main_loop():
        await asyncio.gather(
            clipboard.monitor_clipboard(),
            terminal.monitor_terminal(),
            browser.monitor_browser(),
            vscode.monitor_vscode()
        )

    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        console.print("[yellow]Stopping...[/yellow]")

@app.command()
def recall(query: str):
    """Natural language recall."""
    from .intelligence import intelligence
    response = intelligence.recall(query)
    console.print(f"[bold]Answer:[/bold] {response}")

@app.command()
def timeline(hours: int = 24):
    """Show activity timeline."""
    console.print(f"Showing timeline for last {hours} hours (Not implemented)")

@app.command()
def export(format: str):
    """Export data."""
    console.print(f"Exporting to {format} (Not implemented)")

@app.command()
def stats():
    """Show statistics."""
    console.print("Statistics (Not implemented)")

if __name__ == "__main__":
    app()
