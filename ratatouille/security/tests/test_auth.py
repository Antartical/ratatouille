import pytest
from unittest import TestCase


class TestGetCurrentUser(TestCase):
    """Test get current user dependency."""

    @pytest.mark.asyncio
    async def test_get_user_no_token(self):
        pass

    @pytest.mark.asyncio
    async def test_get_user_none_wrong_credential(self):
        pass

    @pytest.mark.asyncio
    async def test_get_user_success(self):
        pass
