import typing
from fastapi import params, Depends

from ratatouille.security.permissions import base


def require(
    *args: typing.Sequence[base.BasePermission]
) -> params.Depends:
    """Creates a FastAPI dependency for permissions."""
    return Depends(base.PermissionRunner(*args))
