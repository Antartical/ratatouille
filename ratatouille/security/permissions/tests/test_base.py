from unittest import mock
from fastapi import HTTPException
from starlette import status

from ratatouille.common.tests import AsyncRatatouilleTestCase
from ratatouille.security.permissions import base


class TestPermissionRunner(AsyncRatatouilleTestCase):
    """Permission runner tests"""

    async def test_permissions_success(self):
        request = ''
        user = ''
        mock_permission = mock.Mock(
            has_permission=mock.AsyncMock(return_value=(True, '')))
        runner = base.PermissionRunner(mock_permission)

        await runner(request, user)
        mock_permission.has_permission.assert_called_once_with(request, user)

    async def test_permissions_error(self):
        detail = 'Forbidden'
        request = ''
        user = ''
        mock_permission = mock.Mock(
            has_permission=mock.AsyncMock(side_effect=HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=detail
            )))
        runner = base.PermissionRunner(mock_permission)

        with self.assertRaises(HTTPException):
            await runner(request, user)

        mock_permission.has_permission.assert_called_once_with(request, user)
