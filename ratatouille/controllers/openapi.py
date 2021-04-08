"""Openapi helper controllers.

The handlers located here will not be included in the production code they
only exist for testing with openAPI purposes. For this reason there will
not be test for those ones.
"""


import httpx
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from ratatouille import settings


router = APIRouter()


@router.post('/login', include_in_schema=False)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    async with httpx.AsyncClient() as client:
        payload = {
            'email': form_data.username,
            'password': form_data.password,
            'scopes': ['user:read']
        }
        response = await client.post(settings.GANDALF_LOGIN_URL, json=payload)

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=400, detail='Incorrect username or password')

    return {
        'access_token': response.json()['data']['access_token'],
        'token_type': 'bearer'
    }
