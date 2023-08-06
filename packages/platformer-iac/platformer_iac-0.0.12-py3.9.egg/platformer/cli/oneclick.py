import click
from pprint import pprint
from platformer.core.parser import PlatformerConfigReader

@click.command()
@click.option('-f', '--file', type=click.File('r'), required=True)
def oneclick(file):
    """
    | Template based code generation and deployment
    """
    pass
