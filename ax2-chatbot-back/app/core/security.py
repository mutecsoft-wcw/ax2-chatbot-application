from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# TODO[sjh] origin .env이나 config.yml파일로 관리
def cors(app):
    origins = [
        settings.cors_url,
        "http://localhost:13000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
