# GPT-NPC Server (FastAPI + ChromaDB)

캐릭터 성격을 부여한 AI NPC와의 자연스러운 대화를 지원하는 서버입니다.
OpenAI GPT-4o, FastAPI, ChromaDB를 기반으로 구현되었습니다.

---

## ⚙️ 기술 스택

- **FastAPI**: 비동기 Python 웹 프레임워크
- **OpenAI GPT-4o**: AI 응답 생성
- **ChromaDB**: 유저별 대화 내용 임벤딩 벡터 저장
- **uuid4**: 각 메시지의 고유 ID
- **python-dotenv**: 환경 변수 로드

---

## 💻 로컬 실행 방법

### ✅ 1. 가상환경 만들기

**Mac/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

> _PowerShell 실행 경찰 오류가 날 경우:_
> 관리자 권한 PowerShell에서 다음 실행
>
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

### ✅ 2. 의존성 설치

```bash
pip install -r requirements.txt
```

---

### ✅ 3. `.env` 설정

`.env` 파일 생성 후 다음 입력

```
OPENAI_API_KEY=sk-xxxxxxx
```

---

### ✅ 4. 서버 실행

```bash
uvicorn main:app --reload
```

실행 후 [http://localhost:8000](http://localhost:8000) 로 접속 가능

---

## 📁 주요 구조

```
gpt-npc-server/
├─ chroma/              # ChromaDB 클라이언트 구성
│   └─ client.py
├─ npcs/                # NPC별 라우터
│   └─ eren.py
├─ chroma_db/           # Chroma 저장소 (자동 생성됨)
├─ main.py
├─ requirements.txt
└─ .env
```

---

## 🧠 주요 기능

- NPC 이름별로 `/npc/{npc_name}/chat` REST API 제공
- 각 유저 UID별로 Chroma 콜렉션 생성
- 대화는 UUID로 저장, 벡터 임벤딩 처리
- 가장 유사한 과거 메시지 3개를 보기로 추적
- GPT 응답 생성 후 반환

---

## 📌 예시 요청

```
POST /npc/eren/chat
Content-Type: application/json

{
  "uid": "user_123",
  "message": "이것는 네 자유의지약이야?"
}
```

---

## 📝 참고 사항

- `chroma_db` 폴더는 프로젝트 루트에 자동 생성되며 벡터 데이터가 저장됩니다.
- huggingface tokenizers 경고는 무시해도 되는 내용입니다.
- GPT context window는 요약 기능 등으로 관리 가능 (최근 복사중)
