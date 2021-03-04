from fastapi import FastAPI
from ratatouille.controllers import ping


def register(app: FastAPI):
    """Register the api endpoints into the FastAPI application.
    Args:
      app (FastAPI): the FastAPI application.
    """
    app.include_router(ping.router, tags=['Ping'])
