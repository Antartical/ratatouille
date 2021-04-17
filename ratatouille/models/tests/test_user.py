import asyncio
from unittest import mock
from ratatouille.common import test
from ratatouille.models import User
from ratatouille.models.factories import user_factories


class UserModelTest(test.AsyncRatatouilleTestCase):

    async def delay_due_to_es_index(self):
        await asyncio.sleep(1)

    async def test_call_destroy_index(self):
        with mock.patch('ratatouille.models.User.Document._index.delete') as m:
            User.destroy_index()
            m.assert_called_once()

    async def test_call_build_index(self):
        with mock.patch('ratatouille.models.User.Document.init') as m:
            User.build_index()
            m.assert_called_once()

    @test.db_test
    async def test_user_search(self):
        user = await user_factories.user_factory()

        await self.delay_due_to_es_index()
        self.assertTrue(
            await User.search(user.email).filter(id=user.id).exists()
        )

        last_email = user.email
        user.email = 'test@test.com'
        await user.save(update_fields=['email'])

        await self.delay_due_to_es_index()
        self.assertFalse(
            await User.search(last_email).filter(id=user.id).exists()
        )

        await user.delete()
        await self.delay_due_to_es_index()
        self.assertFalse(
            await User.search(user.email).filter(id=user.id).exists()
        )

    @test.db_test
    async def test_user_search_over_specific_fields(self):
        user = await user_factories.user_factory()
        await self.delay_due_to_es_index()
        self.assertTrue(await User.search(
            user.email, fields=['email']
        ).filter(id=user.id).exists())
        self.assertFalse(await User.search(
            user.email, fields=['name']
        ).filter(id=user.id).exists())

    @test.db_test
    async def test_user_match(self):
        user = await user_factories.user_factory()
        await self.delay_due_to_es_index()
        self.assertTrue(await User.match(
            user.email, field='email'
        ).filter(id=user.id).exists())

    @test.db_test
    async def test_to_document(self):
        user = await user_factories.user_factory()
        expected_response = {
            'id': user.id,
            'uuid': user.uuid,
            'email': user.email,
            'name': user.name
        }
        self.assertEqual(expected_response, user.to_document)
