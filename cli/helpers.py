import asyncio
import elasticsearch_dsl
from functools import wraps
from tortoise import Tortoise


from ratatouille import settings


def coro(f):
    """Coroutine command."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def with_initialize_connections(f):
    """Initialize and stop db connections."""
    @wraps(f)
    async def wrapper(*args, **kwargs):
        await Tortoise.init(config=settings.DATABASES)
        elasticsearch_dsl.connections.configure(**settings.ELASTICSEARCH_DSL)
        result = await f(*args, **kwargs)
        await Tortoise.close_connections()
        return result

    return wrapper
