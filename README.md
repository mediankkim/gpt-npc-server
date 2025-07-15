# GPT-NPC Server (FastAPI + ChromaDB)

캐릭터 성격을 부여한 AI NPC와의 자연스러운 대화를 지원하는 서버입니다.  
OpenAI GPT-4o, FastAPI, ChromaDB 기반으로 구현되었습니다.

---

## ⚙️ 기술 스택

- **FastAPI**: 비동기 Python 웹 프레임워크
- **OpenAI GPT-4o**: AI 응답 생성
- **ChromaDB**: 유저별 대화 임베딩 저장
- **Redis**: 대화 기록 캐싱
- **uuid4**, **dotenv** 등

---

## 📦 Docker로 실행하기

### 1. `.env` 파일 생성

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

### 2. 도커 실행

```bash
docker-compose up --build
```

→ 실행 후 [http://localhost:8000/docs](http://localhost:8000/docs) 에서 Swagger API 확인 가능

---

## 📁 주요 구조

```
gpt-npc-server/
├─ main.py
├─ chroma/
├─ npcs/
├─ chroma_db/   # 자동 생성됨
├─ .env
└─ requirements.txt
```

---

## 📌 예시 요청

```http
POST /npc/eren/chat
Content-Type: application/json

{
  "uid": "user_123",
  "message": "이것은 네 자유의지약이야?"
}
```
