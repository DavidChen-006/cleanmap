from pathlib import Path

import click
from dotenv import load_dotenv

from .core import DEFAULT_PROMPT, clean_image


@click.command()
@click.argument("input_path")
@click.option("--output", "-o", default=None, help="Where to save the cleaned image.")
@click.option("--prompt", "-p", default=DEFAULT_PROMPT, help="Override the cleaning instruction.")
def main(input_path, output, prompt):
    """Clean an image: strip clutter, keep the main subject."""
    load_dotenv()

    if output is None:
        p = Path(input_path)
        output = str(p.with_suffix(f".cleaned{p.suffix}"))

    click.echo(f"cleaning {input_path} -> {output}")
    clean_image(input_path, output, prompt)
    click.echo(f"saved {output}")
