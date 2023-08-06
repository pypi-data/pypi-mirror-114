import click
from platformer.core.parser import PlatformerConfigReader
from platformer.core.coders.terraform import TerraformCoder

@click.group()
def code():
    """| Code generator for terraform, ansible or yaml pipelines"""
    pass

@code.command()
@click.option('-f', '--file', type=click.File('r'), required=False)
def terraform(file):
    """
    | Terraform code generator
    """
    if file:
        config = PlatformerConfigReader(file.read())
        terraform_code = TerraformCoder(config.get_terraform())
        click.echo(terraform_code.print_code())
    else: 
        click.echo("No input files")

@code.command()
def ansible():
    """
    | Ansible Playbook generator
    """
    print("Ansible module")

@code.command()
def pipeline():
    """
    | YAML Pipeline generator (Github, Azure Devops)
    """
    print("Pipeline module")
