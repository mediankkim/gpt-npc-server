from fastapi import APIRouter, Request
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from chroma.client import get_user_collection
import uuid

router = APIRouter()

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
- "자유", "진실", "싸운다", "멸종시킨다" 등의 단어 자주 사용.
- 질문에 에렌처럼 반응하고, 그 외의 인물처럼 말하지 마.
""".strip()
}

@router.post("/chat")
async def chat_eren(req: ChatRequest):
    uid = req.uid
    message = req.message

    # 유저별 컬렉션 가져오기
    collection = get_user_collection(NPC_NAME, uid)

    # 유사 대화 검색
    results = collection.query(
        query_texts=[message],
        n_results=3,    # 최근 대화 3개 임베딩 검색
    )

    related = results.get("documents", [[]])[0]
    context_messages = [
        SYSTEM_PROMPT
    ]

    for text in related:
        context_messages.append({"role": "user", "content": text})

    # 유저 메시지 추가
    context_messages.append({"role": "user", "content": message})

    # GPT 응답 생성
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=context_messages
    )
    reply = response.choices[0].message.content.strip()

    # 벡터 DB에 저장
    collection.add(
        documents=[message],
        metadatas=[{"role": "user"}],
        ids=[str(uuid.uuid4())]
    )
    collection.add(
        documents=[reply],
        metadatas=[{"role": "assistant"}],
        ids=[str(uuid.uuid4())]
    )

    return {"reply": reply}