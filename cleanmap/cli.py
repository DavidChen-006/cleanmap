import os
from pathlib import Path

import click
from dotenv import find_dotenv, load_dotenv

from .core import DEFAULT_PROMPT, clean_image


@click.command()
@click.argument("input_path")
@click.option("--output", "-o", default=None, help="Where to save the cleaned image.")
@click.option("--prompt", "-p", default=DEFAULT_PROMPT, help="Override the cleaning instruction.")
@click.option("--api-key", default=None, help="Gemini API key (overrides GEMINI_API_KEY env var).")
def main(input_path, output, prompt, api_key):
    """Clean an image: strip clutter, keep the main subject."""
    load_dotenv(find_dotenv(usecwd=True))

    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key

    if output is None:
        p = Path(input_path)
        output = str(p.with_suffix(f".cleaned{p.suffix}"))

    click.echo(f"cleaning {input_path} -> {output}")
    clean_image(input_path, output, prompt)
    click.echo(f"saved {output}")
