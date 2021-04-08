from fastapi import FastAPI

from ratatouille import controllers
from ratatouille import settings


def register(app: FastAPI):
    """Register the api endpoints into the FastAPI application.
    Args:
      app (FastAPI): the FastAPI application.
    """
    # Register openapi routes for non productive environments
    if not settings.IS_PRODUCTION:
        app.include_router(controllers.openapi.router, tags=['Auth'])

    app.include_router(controllers.health.router, tags=['Health'])
