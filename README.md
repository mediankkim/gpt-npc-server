# 🧠 GPT NPC Server (with Redis & Flask)

AI 캐릭터 '종석햄'과 자연스럽게 대화할 수 있는 NPC 서버 프로젝트입니다.  
Redis를 활용해 사용자별 대화 상태를 기억하며, OpenAI GPT 모델을 활용하여 개성 있는 반응을 제공합니다.

---

## 🧩 주요 기능

- 💬 **캐릭터 설정**: system 프롬프트로 독특한 NPC 성격 부여 (ex. 종석햄)
- 🧠 **대화 히스토리 기억**: Redis를 활용한 사용자별 상태 관리 (UID 기반)
- ✂️ **요약 기능**: 대화가 길어지면 GPT가 자동 요약 → 프롬프트 리셋
- 🔁 **Flask API 제공**: `/chat` 엔드포인트로 POST 요청을 통해 대화 수행
- 🌐 **CORS 지원**: 다양한 클라이언트 환경에서 호출 가능

---

## 🔧 설치 방법

### 1. Python & 의존성 설치

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate.ps1(powershell)
pip install -r requirements.txt
```

### 2. `.env` 파일 생성

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Redis 설치 및 실행

#### ✅ macOS

```bash
brew install redis
brew services start redis
```

#### ✅ Windows

1. [https://github.com/tporadowski/redis/releases](https://github.com/tporadowski/redis/releases) 에서 최신 Windows용 Redis 다운로드
2. 압축 해제 후 `redis-server.exe` 실행 (CLI 또는 PowerShell에서 가능)
3. `redis-cli.exe` 를 통해 접속 가능 (옵션)

※ 권장 경로: `C:\redis`

```cmd
cd C:\redis
redis-server.exe
```

---

## 🚀 실행 방법

```bash
python your_flask_file.py
```

기본적으로 `localhost:5050`에서 Flask 서버가 실행됩니다.

---

## 📡 API 사용 예시

### ▶️ POST `/chat`

**Request Body (JSON):**

```json
{
  "uid": "user123",
  "message": "안녕? 뭐하고 있어?"
}
```

**Response (JSON):**

```json
{
  "reply": "요~ 잘 있었냐? 요즘 커피 좀 줄이려고 했는데 또 마셨어ㅋㅋ"
}
```

---

## 📦 기술 스택

- Python 3.9+
- Flask
- Redis
- OpenAI GPT (gpt-4o / gpt-3.5-turbo)
- python-dotenv
- flask-cors

---

## 📁 폴더 구조 예시

```
gpt-npc-server/
├── .env
├── .gitignore
├── requirements.txt
├── app.py (혹은 main.py)
├── README.md
```

---

## 📌 향후 개발 방향

- Unity / VRChat 연동
- 캐릭터별 프리셋 관리
- 다국어 / 번역 지원
- 로그 분석 및 감정 상태 추론
- Redis 아닌 DB 전환 고려 (ex. MongoDB, PostgreSQL)

---

## 🙏 Special Thanks

이 프로젝트는 GPT를 활용한 인터랙티브 게임 제작 학습을 목적으로 제작되었습니다.  
피드백 및 아이디어 환영합니다!
