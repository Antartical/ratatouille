import pytest
from unittest import TestCase


class TestPingRoute(TestCase):
    """Gandalf vendor test"""

    @pytest.mark.asyncio
    async def test_login_success(self):
        pass

    @pytest.mark.asyncio
    async def test_login_error(self):
        pass

    @pytest.mark.asyncio
    async def me_success(self):
        pass

    @pytest.mark.asyncio
    async def me_error(self):
        pass
