import typing
import httpx
import datetime
import pydantic
import dateutil.parser
from starlette import status

from ratatouille import settings


class GandalfError(Exception):
    """This exception will be raised on gandalf API error."""


class GandalfUser(pydantic.BaseModel):
    email: pydantic.EmailStr
    name: str
    surname: str
    birthday: datetime.date
    phone: typing.Optional[str]

    @pydantic.validator('birthday', pre=True)
    def parse_date_iso8601(date: str) -> datetime.date:
        return dateutil.parser.parse(date)


class GandalfToken(pydantic.BaseModel):
    access_token: str
    refresh_token: str


async def login(
    email: str, password: str, scopes: typing.List[str]
) -> GandalfToken:
    """Login user into gandalf by the given credentials.

    Args:
        email (str): user email.
        password (str): user password.
        scopes (typing.List[str]): gandalf scopes

    Raises:
        GandalfError: whether the giver credentials does not authenticate any
          user in gandalf system.

    Returns:
        GandalfToken: gandalf access tokens.
    """
    async with httpx.AsyncClient() as client:
        payload = {
            'email': email,
            'password': password,
            'scopes': scopes
        }
        response = await client.post(settings.GANDALF_LOGIN_URL, json=payload)

    if response.status_code != status.HTTP_200_OK:
        raise GandalfError()

    return GandalfToken(**response.json()['data'])


async def me(access_token: str) -> GandalfUser:
    """Obtains user info.

    Args:
        access_token (str): auth token.

    Raises:
        GandalfError: whether the given access_token does not
          authenticate any user in gandalf system.

    Returns:
        GandalfUser: gandalf user info.
    """
    async with httpx.AsyncClient() as client:
        headers = {'Authorization': f'Bearer {access_token}'}
        response = await client.get(settings.GANDALF_ME_URL, headers=headers)

    if response.status_code != status.HTTP_200_OK:
        raise GandalfError()

    return GandalfUser(**response.json()['data'])
