import click
import collections
from platformer.cli.code import code
from platformer.cli.test import test
from platformer.cli.deploy import deploy
from platformer.cli.oneclick import oneclick
from platformer import __version__


class OrderedGroup(click.Group):
    def __init__(self, name=None, commands=None, **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        #: the registered subcommands by their exported names.
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        return self.commands


@click.group(cls=OrderedGroup)
@click.version_option(
    prog_name = 'Platformer',
    version   = __version__
)
def cli():
    """
    Platform Builder Framework

    \b
    All your platform infrastructure based on git code
      - Code generator based on Terraform, Ansible and YAML based pipelines
      - Deploy files to Git repository and setup automatic pipelines

    :: Read the docs: https://github.com/rfsantanna/platformer
    """
    ...

cli.add_command(code)
cli.add_command(test)
cli.add_command(deploy)
cli.add_command(oneclick)
