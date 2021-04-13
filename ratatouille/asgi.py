from fastapi import FastAPI
from fastapi.middleware import cors
from tortoise.contrib.fastapi import register_tortoise

from ratatouille import settings
from ratatouille import router


def make_app() -> FastAPI:
    """Builds the ASGI application

    Returns:
        FastAPI: ASGI app.
    """
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        debug=settings.DEBUG
    )

    # Database
    register_tortoise(app, config=settings.DATABASES)

    # Middlewares
    app.add_middleware(
        cors.CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_methods=['*'],
        allow_headers=['*']
    )

    # Routes
    router.register(app)

    return app


app = make_app()
