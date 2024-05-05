from fastapi import APIRouter

from .endpoints import (
    extract_text,
    client
)

api_router = APIRouter()
api_router.include_router(extract_text.router, prefix='', tags=['Extract Text'])
api_router.include_router(client.router, prefix='', tags=['Client'])
