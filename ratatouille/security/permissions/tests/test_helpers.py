from ratatouille.common.tests import AsyncRatatouilleTestCase
from ratatouille.security.permissions import helpers


class TestRequireDependency(AsyncRatatouilleTestCase):
    """Require depencency test"""

    async def test_wraps_permissions_runner_dependency(self):
        self.assertIsInstance(helpers.require().dependency,
                              helpers.base.PermissionRunner)
