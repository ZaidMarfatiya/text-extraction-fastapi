from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api.api import api_router


app = FastAPI(title="Text Extraction Service")

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://127.0.0.1:8000',
    ],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'OPTIONS', 'HEAD', 'DELETE'],
    allow_headers=['*'],
)
