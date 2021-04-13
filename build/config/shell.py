
"""This file will be launched at new ipython shell session.

Please include in this file everything you need to be imported in your
ipython shell.
"""


import sys


def debugger_is_active() -> bool:
    """Return if the debugger is currently active"""
    gettrace = getattr(sys, 'gettrace', lambda: None)
    return gettrace() is not None


if not debugger_is_active():
    import atexit
    import asyncio
    from tortoise import Tortoise

    from ratatouille import settings
    from ratatouille.models import *

    def on_shutdown():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(Tortoise.close_connections())

    atexit.register(on_shutdown)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(Tortoise.init(config=settings.DATABASES))
