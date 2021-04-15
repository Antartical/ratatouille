"""Elastisearch commands cli."""

import typer
from tqdm import tqdm
from colorama import Fore

from cli.helpers import coro, with_initialize_connections
from ratatouille import models as ratatouille_models


app = typer.Typer()


@app.command()
@coro
@with_initialize_connections
async def rebuild(models: str = ''):
    "Rebuild elastic index and fill them again."""
    if not models:
        models = ratatouille_models.__all__
    else:
        models = models.split(',')

    for model in models:
        cls = getattr(ratatouille_models, model, None)
        if not cls:
            typer.echo(
                Fore.YELLOW + f"There's no model called {model}; Skipping."
            )
            continue

        objects_to_index = await cls.all().count()
        cls.destroy_index()
        cls.build_index()

        with tqdm(total=objects_to_index) as pbar:
            pbar.set_description(f'Indexing {model}')
            async for obj in cls.all():
                obj._index_id = None
                obj._index_id = obj.index()
                await obj.save(update_fields=['_index_id'])
                pbar.update()
