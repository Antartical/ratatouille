import json
import typing
import unittest
import pytest
from functools import partial
from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock

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


class APITestCase(unittest.TestCase):
    """TestCase class for API testing."""

    def setUp(self):
        self.client = TestClient(app)


@auto_inject_fixtures('httpx_mock')
class AsyncHTTPXTestCase(unittest.IsolatedAsyncioTestCase):
    """TestCase class for async httpx testing."""

    httpx_mock: HTTPXMock

    def dump(self, payload: typing.Dict) -> bytes:
        return json.dumps(payload).encode()
