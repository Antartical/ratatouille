from fastapi import APIRouter


router = APIRouter(prefix='/ping')


@router.get('')
async def ping():
    """Herathbleed endpoint."""
    return {'pong': True}
