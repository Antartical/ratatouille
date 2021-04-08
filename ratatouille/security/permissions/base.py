import abc
import typing
from fastapi import Depends
from fastapi import HTTPException
from starlette import status
from starlette.requests import Request

from ratatouille.models import User
from ratatouille.security.auth.helpers import get_current_user


class BasePermission(abc.ABC):
    """Base permission class"""

    @abc.abstractstaticmethod
    async def has_permission(
        request: Request,
        user: typing.Optional[User]
    ) -> typing.Tuple[bool, typing.Optional[str]]:
        """Check if the user who performs the request has correct permissions.

        Args:
          request (Request): request.
          user (User, Optional): the user who performs the request.

        Returns:
          Tuple[bool, Optional[str]: if user are authorized and a msg explained
          why he has not got access.
        """
        pass


class PermissionRunner:
    """Permission runner class."""

    def __init__(self, *args: typing.Iterable[BasePermission]):
        self.permissions = args

    async def __call__(
        self,
        request: Request,
        user: typing.Optional[User] = Depends(get_current_user)
    ):
        """Invoke permission as FastApi depenency

        Args:
          request (Request): request.
          user (User): the user who performs the request.

        Raises:
          HTTPException: whether the user who performs the request have not got
            access permissions.
        """
        for permission in self.permissions:
            has_permission, detail = await permission.has_permission(
                request, user
            )
            if not has_permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=detail
                )
