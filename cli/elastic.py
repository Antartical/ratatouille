"""Elastisearch commands cli."""

import typer
from tqdm import tqdm
from colorama import Fore

from cli.helpers import with_initialize_connections
from ratatouille import models as ratatouille_models


app = typer.Typer()


@app.command()
@with_initialize_connections
async def rebuild(models: str = ''):
    "Rebuild elastic index and fill them again."""
    if not models:
        models = ratatouille_models.__all__
    else:
        models = models.split(',')

    for model in models:
        cls = getattr(ratatouille_models, model, None)
        if not cls or not getattr(cls, 'Document', None):
            typer.echo(
                Fore.YELLOW + f"There's no model called {model}; Skipping."
            )
            continue

        objects_to_index = await cls.all().count()
        if objects_to_index > 0:
            cls.destroy_index()
            cls.build_index()

            with tqdm(total=objects_to_index) as pbar:
                pbar.set_description(Fore.GREEN + f'Indexing {model}')
                async for obj in cls.all():
                    obj._index_id = None
                    obj._index_id = obj.index()
                    await obj.save(update_fields=['_index_id'])
                    pbar.update()
        else:
            typer.echo(
                Fore.YELLOW + f"No objects to index of type {model}"
            )
