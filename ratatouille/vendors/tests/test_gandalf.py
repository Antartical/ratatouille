from ratatouille.common.tests import AsyncHTTPXTestCase
from ratatouille.vendors import gandalf


class TestGandalfAPI(AsyncHTTPXTestCase):
    """Gandalf vendor test"""

    async def test_login_success(self):
        email = 'test@test.com'
        password = 'test'
        scopes = ['user:read']
        access_token = 'test'
        refresh_token = 'test'

        matched_payload = self.dump({
            'email': email,
            'password': password,
            'scopes': scopes
        })
        mocked_response = {
            'type': 'token',
            'data': {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        }

        self.httpx_mock.add_response(
            json=mocked_response, match_content=matched_payload)
        tokens = await gandalf.login(email, password, scopes)

        assert tokens.access_token == access_token
        assert tokens.refresh_token == refresh_token

    async def test_login_error(self):
        pass

    async def test_me_success(self):
        pass

    async def test_me_error(self):
        pass
