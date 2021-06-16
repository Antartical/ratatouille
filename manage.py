#!/usr/local/bin/python


import typer
from colorama import init, Fore

from cli import elastic


app = typer.Typer()


if __name__ == "__main__":
    try:
        init()
        app.add_typer(elastic.app, name='elastic')
        app()
    except Exception as e:
        typer.echo(
            Fore.RED + f"{e}"
        )
