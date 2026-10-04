from __future__ import annotations

import typer

app = typer.Typer(help="Watchtower CLI")


@app.command()
def health() -> None:
    typer.echo("ok")


@app.command()
def worker() -> None:
    typer.echo("Worker is running")


@app.command()
def watch_add(url: str, name: str, source_type: str = "http", extraction_type: str = "html") -> None:
    typer.echo(f"Created watch {name} for {url}")


@app.command()
def watch_list() -> None:
    typer.echo("No watches configured")


@app.command()
def watch_run(watch_id: str) -> None:
    typer.echo(f"Running watch {watch_id}")
