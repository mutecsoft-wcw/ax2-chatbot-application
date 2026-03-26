from fastapi.middleware.cors import CORSMiddleware


# TODO[sjh] origin .env이나 config.yml파일로 관리
def cors(app):
    origins = [
        "http://192.168.0.240:13000",
        "http://localhost:13000",
        "http://192.168.0.6:13000",
        "http://localhost:13001",
        "http://192.168.0.6:13001",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
