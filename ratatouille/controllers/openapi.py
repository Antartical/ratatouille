"""Openapi helper controllers.

The handlers located here will not be included in the production code they
only exist for testing with openAPI purposes. For this reason there will
not be test for those ones.
"""


from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ratatouille.vendors import gandalf


router = APIRouter()


@router.post('/login', include_in_schema=False)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        tokens = gandalf.login(
            form_data.email, form_data.password, ['user:read'])
    except gandalf.GandalfError:
        raise HTTPException(
            status_code=400, detail='Incorrect username or password')

    return {
        'access_token': tokens.access_token,
        'token_type': 'bearer'
    }
