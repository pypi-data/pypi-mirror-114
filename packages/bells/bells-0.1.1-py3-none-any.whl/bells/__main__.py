import click
from .commands import init


@click.group()
def main():
    pass

main.add_command(init)

if __name__ == '__main__':
    main()
