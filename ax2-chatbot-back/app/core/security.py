from fastapi.middleware.cors import CORSMiddleware


# TODO[sjh] origin .env이나 config.yml파일로 관리
def cors(app):
    origins = [
        "http://localhost:3000",
        "http://192.168.0.6:3000",
        "http://localhost:3001",
        "http://192.168.0.6:3001",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
