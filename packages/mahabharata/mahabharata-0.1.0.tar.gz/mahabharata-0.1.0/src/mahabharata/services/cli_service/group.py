import click

from ._commands import query_poem


@click.group()
def cli() -> None:
    pass


cli.add_command(query_poem)
