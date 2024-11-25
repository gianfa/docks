"""
"""

import click

from docks.generate_doc import generate_markdown


@click.command()
@click.argument("dockerfile", type=click.Path(exists=True))
@click.argument("output", type=click.Path(writable=True))
def cli(dockerfile: str, output: str):
    """
    Generate Markdown documentation for a Dockerfile.

    Arguments\n
    \tdockerfile: (str). Path to the Dockerfile to document.\n
    \toutput: (str). Path to save the generated Markdown documentation.

    Example\n
    \tdocks myproject/Dockerfile myproject/dockerfile-doc.md
    """
    click.echo(f"Generating documentation for Dockerfile: {dockerfile}")
    generate_markdown(dockerfile, output, verbose=False)
    click.echo(f"Documentation saved to: {output}")


if __name__ == "__main__":
    cli()
