# commands.py
import click

from utils import extract_cookies

@click.group()
def command():
    pass

@command.command()
@click.option('--export', required=True, help='Is required expecific action export')
@click.option('--system', required=True, help='Is required expecific action systems')
@click.pass_context
def cookie(ctx, export, system):
    print("Inicializando exportacion...")
    extract_cookies(export, system)

if __name__ == "__main__":
    command()