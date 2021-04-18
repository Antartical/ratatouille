"""Elastisearch commands cli."""

import typer
import elasticsearch
from tqdm import tqdm
from colorama import Fore

from cli.helpers import with_initialize_connections
from ratatouille import models as ratatouille_models


app = typer.Typer()


@app.command()
@with_initialize_connections
async def build(models: str = ''):
    """Init elastic indexes."""
    if not models:
        models = ratatouille_models.__all__
    else:
        models = models.split(',')

    errors = []
    retries = []

    with tqdm(total=len(models)) as pbar:
        pbar.set_description(Fore.GREEN + 'Build indexes')
        for model in models:
            cls = getattr(ratatouille_models, model, None)
            if not cls or not getattr(cls, 'Document', None):
                errors.append(
                    Fore.YELLOW + f'Model {model} does not exists.'
                )
                pbar.update()
                continue
            if cls.Document._index.exists():
                pbar.update()
                continue
            try:
                cls.build_index()
            except elasticsearch.exceptions.RequestError:
                errors.append(
                    Fore.YELLOW + f'Exception on build index for {model}'
                )
                retries.append[cls]
            pbar.update()

    for error in errors:
        typer.echo(error)

    if retries:
        errors = []
        with tqdm(total=len(models)) as pbar:
            pbar.set_description(Fore.GREEN + 'Retrying build failed indexes')
            for model in retries:
                try:
                    model.build_index()
                except elasticsearch.exceptions.RequestError:
                    errors.append(
                        Fore.RED +
                        f'Exception on build index for {model.__name__}'
                    )
                pbar.update()

        for error in errors:
            typer.echo(error)


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
