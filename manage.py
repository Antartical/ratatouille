#!/usr/bin/env python


import typer
from colorama import init

from cli import elastic


app = typer.Typer()


if __name__ == "__main__":
    init()
    app.add_typer(elastic.app, name='elastic')
    app()
