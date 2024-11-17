import click
from colorama import init as init_colorama

from . import core


@click.group()
def cli():
    """A tool to deploy an app to a VPS."""
    pass


@cli.command(help="Initialize a project for deployment setup")
@click.option('--name', required=True)
def init(name):
    core.initialise_project(name)


@cli.command(help="Specify the target machine for deploying the project")
@click.option('--ip', required=True)
@click.option('--ssh-key-file', required=True, type=click.Path(exists=True))
@click.option('--username', required=True)
def set_host(ip: str, ssh_key_file: str, username: str):
    core.set_host(username, ip, ssh_key_file)


@cli.command(help="Deploy a bead")
@click.option('--domain-name', required=False)
@click.option('--env-file', required=False)
@click.option('--image', required=False)
def provision(domain_name: str, env_file: str, image: str):
    core.put_bead_on_server(domain_name, env_file, image)


@cli.command(help="Serves your app behind HTTPS")
def apply_ssl():
    core.obtain_ssl_certificate()


@cli.command(help="Run a bead")
def run():
    core.run()


init_colorama(autoreset=True)


if __name__ == '__main__':
    cli()
