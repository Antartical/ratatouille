import typing
import httpx
import datetime
import pydantic
import dateutil.parser
from starlette import status

from ratatouille import settings
from ratatouille.models import User
from ratatouille.security.auth import errors


class GandalfUser(pydantic.BaseModel):
    email: pydantic.EmailStr
    name: str
    surname: str
    birthday: datetime.date
    phone: typing.Optional[str]

    @pydantic.validator('birthday', pre=True)
    def parse_date_iso8601(date: str) -> datetime.date:
        return dateutil.parser.parse(date)


async def authenticate(access_token: str) -> User:
    """Authenticates a user with the given credentials.

    Args:
      access_token (str): Gandalf Oauth2 token.

    Raises:
      errors.UserCredentialsError: whether the user could not be verified.

    Returns:
      User: the user who match with the given credentials.
    """
    async with httpx.AsyncClient() as client:
        headers = {'Authorization': f'Bearer {access_token}'}
        response = await client.get(settings.GANDALF_ME_URL, headers=headers)

    if response.status_code != status.HTTP_200_OK:
        raise errors.UserCredentialsError()

    gandalf_user = GandalfUser(**response.json()['data'])
    return await User.get_or_create(
        email=gandalf_user.email,
        defaults=gandalf_user.dict(exclude={'email'})
    )
