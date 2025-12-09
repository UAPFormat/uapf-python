"""CLI entry point for the UAPF parser."""

from __future__ import annotations

import click

from .parser import load_uapf, validate_uapf


@click.group()
def cli() -> None:
    """UAPF parser and validator."""


@cli.command()
@click.argument("path", type=click.Path(exists=True))
def validate(path: str) -> None:
    """Validate a .uapf file against UAPF schemas."""

    validate_uapf(path)
    click.echo("UAPF file is valid.")


@cli.command()
@click.argument("path", type=click.Path(exists=True))
def inspect(path: str) -> None:
    """Print manifest summary of a .uapf file."""

    pkg = load_uapf(path, validate=False)
    click.echo(pkg.manifest)


if __name__ == "__main__":
    cli()
