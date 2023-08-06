import sys
import click


@click.group()
@click.version_option("0.0.3")
def main():
    """A PySwag CLI"""
    pass


@main.command()
@click.argument("path", required=False)
def start(**kwargs):
    """start the server"""
    click.echo("Hey!")


if __name__ == "__main__":
    args = sys.argv
    if "--help" in args or len(args) == 1:
        click.echo("PySwag")
    main()
