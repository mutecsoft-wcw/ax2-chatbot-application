FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY config.yml .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY ./app ./app

# 애플리케이션 실행 (예: FastAPI/Uvicorn 기준)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "18000"]