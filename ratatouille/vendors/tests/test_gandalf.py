import dateutil.parser

from ratatouille.core.testing import AsyncHTTPXTestCase
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

        self.assertEqual(tokens.access_token, access_token)
        self.assertEqual(tokens.refresh_token, refresh_token)

    async def test_login_error(self):
        with self.assertRaises(gandalf.GandalfError):
            self.httpx_mock.add_response(status_code=400)
            await gandalf.login('', '', [])

    async def test_me_success(self):
        access_token = 'test'
        email = 'test@example.com'
        name = 'Agapito'
        surname = 'Disousa'
        birthday = '1997-12-21T00:00:00Z'
        p_birthday = dateutil.parser.parse(birthday).date()
        phone = '+34666123456'

        matched_headers = {'Authorization': f'Bearer {access_token}'}
        mocked_response = {
            'type': 'user',
            'data': {
                'email': email,
                'name': name,
                'surname': surname,
                'birthday': birthday,
                'phone': phone
            }
        }

        self.httpx_mock.add_response(
            json=mocked_response, match_headers=matched_headers)
        user = await gandalf.me(access_token)

        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertEqual(user.surname, surname)
        self.assertEqual(user.birthday, p_birthday)
        self.assertEqual(user.phone, phone)

    async def test_me_error(self):
        with self.assertRaises(gandalf.GandalfError):
            self.httpx_mock.add_response(status_code=400)
            await gandalf.me('')
