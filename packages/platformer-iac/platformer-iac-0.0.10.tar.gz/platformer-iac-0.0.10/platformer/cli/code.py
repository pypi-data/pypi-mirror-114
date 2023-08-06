import click

@click.group()
def code():
    """| Code generator for terraform, ansible or yaml pipelines"""
    pass

@code.command()
def terraform():
    """| Terraform code generator"""
    print("Terraform module")

@code.command()
def ansible():
    """| Ansible Playbook generator"""
    print("Ansible module")

@code.command()
def pipeline():
    """| YAML Pipeline generator (Github, Azure Devops)"""
    print("Pipeline module")
