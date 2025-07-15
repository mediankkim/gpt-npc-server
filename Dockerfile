FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# requirements 먼저 복사하고 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 전체 코드 복사
COPY . .

# FastAPI 서버 실행 (루트에 main.py 있으므로 main:app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]