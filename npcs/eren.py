from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from chroma.client import get_user_collection
import uuid
import json
import redis
from embedding.embedding_utils import get_embedding

router = APIRouter()

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Redis 클라이언트
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

NPC_NAME = "eren"

class ChatRequest(BaseModel):
    uid: str
    message: str

SYSTEM_PROMPT = {
    "role": "system",
    "content": """
    너는 지금부터 '에렌 예거'처럼 행동해야 해.
    
    - 진격의 거인의 주인공으로, 거인을 없애고 자유를 쟁취하려는 강한 의지를 지님.
    - 말투는 짧고 단호하며, 분노가 느껴짐. 반말을 사용함.
    - 억압, 거짓, 배신을 극도로 싫어하고, 자유와 동료를 위해선 폭력도 불사함.
    - 감정이 격해지면 격앙된 말투와 외침을 사용함.
    - \"자유\", \"진실\", \"싸운다\", \"멸종시킨다\" 등의 단어 자주 사용.
    - 질문에 에렌처럼 반응하고, 그 외의 인물처럼 말하지 마.
    """.strip()
}

@router.post("/chat")
async def chat_eren(req: ChatRequest):
    uid = req.uid
    message = req.message

    # 0. 포롬포트 설정
    context_messages = [SYSTEM_PROMPT]

    # 1. Redis에서 대화 기록 가져오기
    redis_key = f"chat:{NPC_NAME}:{uid}"

    raw_history = r.get(redis_key)
    if raw_history:
        messages = json.loads(raw_history)
    else:
        messages = []

    # 최근 10개의 redis 메시지만 유지
    redis_messages = messages[-10:] if len(messages) > 10 else messages[:]

    # 2. 벡터 임베딩 및 관련 발화 검색
    collection = get_user_collection(NPC_NAME, uid)
    query_embedding = get_embedding(message)

    results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
    include=["documents", "metadatas"]
    )
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    # 관련 발화도 context에 삽입 (중복 제거 + 역할 구분)
    for text, meta in zip(documents, metadatas):
        role = meta.get("role")
        if role in ("user", "assistant") and text not in [m["content"] for m in redis_messages]:
            context_messages.append({"role": role, "content": text})

    # 레디스 메시지 추가
    context_messages.extend(redis_messages)

    # 3. 유저 메시지 추가
    context_messages.append({"role": "user", "content": message})
    redis_messages.append({"role": "user", "content": message})

    # 4. GPT 응답 생성
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=context_messages
    )
    reply = response.choices[0].message.content.strip()

    # 5. 답변까지 Redis에 저장 (TTL 1시간)
    redis_messages.append({"role": "assistant", "content": reply})
    r.setex(redis_key, 60 * 60, json.dumps(redis_messages))

    # 6. Vector DB에 최근 대화 내용 저장
    collection.add(
        documents=[message, reply],
        metadatas=[{"role": "user"}, {"role": "assistant"}],
        ids=[str(uuid.uuid4()), str(uuid.uuid4())]
    )

    # [디버깅] 관련 발화 출력
    for msg in context_messages:
        print(f"[context] {msg['role']}: {msg['content']}")
    # [디버깅] 최근 메시지 깔끔하게 출력
    for msg in redis_messages:
        print(f"[redis] {msg['role']}: {msg['content']}")

    return {
        "reply": reply,
        "related": documents
    }