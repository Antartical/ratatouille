
"""This file will be launched at new ipython shell session.

Please include in this file everything you need to be imported in your
ipython shell.
"""


import atexit
import asyncio
from tortoise import Tortoise

from ratatouille import settings
from ratatouille.models import *


def on_shutdown():
    Tortoise.close_connections()


atexit.register(on_shutdown)

loop = asyncio.get_event_loop()
loop.run_until_complete(Tortoise.init(config=settings.DATABASES))
