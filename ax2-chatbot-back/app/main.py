from fastapi import FastAPI
from app.api.chat import router
from app.core.security import cors

# FastAPI 인스턴스 생성
app = FastAPI()

# CORS 관련 설정 적용
cors(app)

# 라우터 등록
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=18000, reload=True)
