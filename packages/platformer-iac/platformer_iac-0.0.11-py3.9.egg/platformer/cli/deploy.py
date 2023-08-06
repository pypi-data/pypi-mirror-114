import click

@click.group()
def deploy():
    """| Git repository and pipeline configuration""" 
    pass

@deploy.command()
def azdo():
    """| Azure Devops Deployer"""
    print("Azure Devops module")

@deploy.command()
def github():
    """| Github Deployer"""
    print("Github module")
