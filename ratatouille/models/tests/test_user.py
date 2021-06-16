from ratatouille.common import test
from ratatouille.models.factories import user_factories


class UserModelTest(test.AsyncRatatouilleTestCase):

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
