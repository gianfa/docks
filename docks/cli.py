"""
CLI Command for docks (Unified Command)
"""

import click
from docks.generate_doc import generate_markdown


@click.command()
@click.argument("dockerfile", type=click.Path(exists=True))
@click.argument("output", type=click.Path(writable=True))
@click.option(
    "--title",
    "-t",
    default="Dockerfile Documentation",
    help="Custom title for the generated documentation.",
)
def cli(dockerfile: str, output: str, title: str):
    """
    Generate Markdown documentation for a Dockerfile.

    Arguments:
        dockerfile: Path to the Dockerfile to document.
        output: Path to save the generated Markdown documentation.

    Options:
        --title, -t: Custom title for the Markdown documentation (default: 'Dockerfile Documentation').

    Example:
        docks Dockerfile dockerfile-doc.md --title "My Custom Dockerfile"
    """
    click.echo(
        f"Generating documentation for Dockerfile: {dockerfile} with title '{title}'"
    )
    generate_markdown(dockerfile, output, title=title, verbose=False)
    click.echo(f"Documentation saved to: {output}")


if __name__ == "__main__":
    cli()
