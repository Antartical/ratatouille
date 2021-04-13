from unittest import mock

from ratatouille.common.tests import AsyncRatatouilleTestCase, db_test
from ratatouille.security import auth


class TestGetCurrentUser(AsyncRatatouilleTestCase):
    """Test get current user dependency."""

    async def test_get_user_no_token(self):
        self.assertIsNone(await auth.get_current_user(''))

    async def test_get_user_none_wrong_credential(self):
        access_token = 'test'
        with mock.patch(
            'ratatouille.vendors.gandalf.me',
            side_effect=mock.AsyncMock(side_effect=auth.gandalf.GandalfError)
        ) as mocked_gandalf_me:
            self.assertIsNone(await auth.get_current_user(access_token))
            mocked_gandalf_me.assert_called_once_with(access_token)

    @db_test
    async def test_get_user_success(self):
        access_token = 'test'
        mocked_gandalf_user = auth.gandalf.GandalfUser(
            email='test@example.com',
            name='Agapito',
            surname='Disousa',
            birthday='1997-12-21T00:00:00Z',
            phone='+34666123456'
        )
        with mock.patch(
            'ratatouille.vendors.gandalf.me',
            side_effect=mock.AsyncMock(return_value=mocked_gandalf_user)
        ) as mocked_gandalf_me:
            user = await auth.get_current_user(access_token)
            mocked_gandalf_me.assert_called_once_with(access_token)

        self.assertEqual(user.email, mocked_gandalf_user.email)
        self.assertEqual(user.name, mocked_gandalf_user.name)
        self.assertEqual(user.surname, mocked_gandalf_user.surname)
        self.assertEqual(user.birthday, mocked_gandalf_user.birthday)
        self.assertEqual(user.phone, mocked_gandalf_user.phone)
