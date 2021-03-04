from fastapi import FastAPI
from fastapi.middleware import cors
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
