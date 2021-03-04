from unittest import TestCase
from fastapi.testclient import TestClient
from ratatouille.asgi import app


class APITestCase(TestCase):
    """TestCase class for API testing."""

    def setUp(self):
        self.client = TestClient(app)
