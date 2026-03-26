from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.core.security import cors

# FastAPI 인스턴스 생성
app = FastAPI()

# CORS 관련 설정 적용
cors(app)

# 라우터 등록
app.include_router(chat_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=18000, reload=True)
