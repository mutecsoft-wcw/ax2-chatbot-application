import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

class Settings:
    GEMMA_BASE_URL = os.getenv("GEMMA_BASE_URL")
    GEMMA_MODEL_NAME= os.getenv("GEMMA_MODEL_NAME")
    ES_URL = os.getenv("ELASTICSEARCH_URL")

settings = Settings()