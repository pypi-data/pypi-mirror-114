import click
from pprint import pprint
from platformer.core.parser import PlatformerConfigReader

from platformer.templates.base_terraform import standard_resource

@click.command()
@click.option('-f', '--file', type=click.File('r'), required=True)
def oneclick(file):
    """| Template based code generation and deployment"""
    ...
    config = PlatformerConfigReader(file.read())
    for resource in config.config['resources']:
        print(standard_resource.render(
            object_name = resource["name"],
            object_options = resource["options"]
        ))

