from __future__ import annotations

import json
import typing
import unittest
import pytest
import tortoise
import elasticsearch_dsl
from functools import partial, wraps
from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock
from tortoise import models

from ratatouille import settings
from ratatouille.asgi import app


def _inject(cls, names):
    @pytest.fixture(autouse=True)
    def auto_injector_fixture(self, request):
        for name in names:
            setattr(self, name, request.getfixturevalue(name))

    cls._auto_injector_fixture = auto_injector_fixture
    return cls


def auto_inject_fixtures(*names):
    return partial(_inject, names=names)


def db_test(func):
    @wraps(func)
    async def wrapped(*args):
        result = None
        try:
            async with tortoise.transactions.in_transaction():
                result = await func(*args)
                raise tortoise.exceptions.TransactionManagementError()
        except tortoise.exceptions.TransactionManagementError:
            return result
    return wrapped


class AsyncRatatouilleTestCase(unittest.IsolatedAsyncioTestCase):
    """TestCase class for Testing with bd rollback transacions."""

    async def asyncSetUp(self):
        await tortoise.Tortoise.init(config=settings.TEST_DATABASES)
        await tortoise.Tortoise.generate_schemas()
        elasticsearch_dsl.connections.configure(**settings.ELASTICSEARCH_DSL)

    async def asyncTearDown(self):
        await tortoise.Tortoise.close_connections()


class AsyncAbstractModelTestCase(AsyncRatatouilleTestCase):

    Model: models.Model

    async def get_model(self) -> models.Model:
        with unittest.mock.patch.object(self.Model._meta, 'basequery'):
            self.Model.filter = unittest.mock.MagicMock()
            model = await self.Model.create()
        return model


class AsyncAPITestCase(AsyncRatatouilleTestCase):
    """TestCase class for API testing."""

    client: TestClient

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.client = TestClient(app)


@auto_inject_fixtures('httpx_mock')
class AsyncHTTPXTestCase(AsyncRatatouilleTestCase):
    """TestCase class for async httpx testing."""

    httpx_mock: HTTPXMock

    def dump(self, payload: typing.Dict) -> bytes:
        return json.dumps(payload).encode()
