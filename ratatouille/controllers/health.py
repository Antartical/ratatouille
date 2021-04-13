"""This module contains endpoint for health app measure."""


from fastapi import APIRouter


router = APIRouter()


@router.get('/ping')
async def ping():
    """Ping endpoint."""
    return {'pong': True}
