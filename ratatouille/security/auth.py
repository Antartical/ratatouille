import typing
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from ratatouille.models import User
from ratatouille.vendors import gandalf


authorization = OAuth2PasswordBearer('/login', auto_error=False)


async def get_current_user(
    authorization_token: str = Depends(authorization)
) -> typing.Optional[User]:
    """Get current user from the request metadata.

    This method should be used as fastAPI dependency.

    Args:
      authorization_token (str): authorization token.

    Returns:
      Optional[User]: the user who performs the request.
    """
    if not authorization_token:
        return None

    try:
        gandalf_user = await gandalf.me(authorization_token)
        user, _ = await User.get_or_create(
            email=gandalf_user.email,
            defaults=gandalf_user.dict(exclude={'email'})
        )
        return user
    except gandalf.GandalfError:
        return None
