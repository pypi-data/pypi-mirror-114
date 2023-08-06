import click

@click.group()
def test():
    """| Test code running on local machine""" 
    pass

@test.command()
def terraform():
    """| Run Generated Terraform code"""
    print("Run Terraform Init")
    print("Run Terraform Plan")
    print("Run Terraform Apply")

@test.command()
def ansible():
    """| Run Generated Ansible code"""
    print("Run Ansible Playbook")
