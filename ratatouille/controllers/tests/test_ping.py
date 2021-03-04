from ratatouille.controllers.tests.base import APITestCase


class TestPingRoute(APITestCase):
    """Tests for ping route."""

    def test_ping(self):
        expected_response = {'pong': True}

        response = self.client.get('/ping')
        self.assertEqual(response.json(), expected_response)
