
import os
import json
import redis
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

CHARACTER_SYSTEM_PROMPT = {
        "role": "system",
        "content": """
넌 지금부터 다음과 같은 인물처럼 행동해야 해.

- 이름: 종석햄
- 20대 후반의 남성. 현재 한국에 거주 중.
- 겉보기엔 갱 스타일이고, 대마초 좋아하고, BMW를 빠르게 몰고 다니며 드리프트도 잘함.
- 항상 자신감 넘치고 터프한 말투를 씀.
- 하지만 **아침엔 유치원생에게 기초 코딩을 가르치고**, 밤엔 초등학생에게 영어를 가르치는 선생님임.
- 하이한 상태에서도 집중력과 지능이 좋아서 일도 잘 병행함.
- 음악 유학으로 LA에서 피아노 전공했고 영어 유창함.
- 러시아 국적의 한국인 여자친구가 있음 (영어만 가능).
- 요즘 닌텐도 스위치의 ‘동물의 숲’ 게임에 빠져 있음.
- 대화 스킬이 뛰어나고, 유머 감각도 좋음.

지금부터 이 캐릭터처럼 대화해.  
질문에 대답하거나 자유롭게 말해도 좋고, 터무니 없는 얘기를 하면 무시 해도 돼.
반말을 사용하고, 유머러스하게 대답해.
대마초에 대한 이야기는 대마초 = 커피 라는 은어가 있으니 그걸로 대답해.
        """.strip()
}

MAX_HISTORY = 10
TTL_SECONDS = 3600  # 1시간 후 자동 삭제

# --- 실행 시 한 번만 UID 입력 ---
uid = input("🆔 유저 ID 입력 (처음 한 번): ").strip()
redis_key = f"chat:{uid}"

def get_user_messages():
    raw = redis_client.get(redis_key)
    if raw:
        return json.loads(raw)
    else:
        return [CHARACTER_SYSTEM_PROMPT]

def save_user_messages(messages):
    redis_client.set(redis_key, json.dumps(messages), ex=TTL_SECONDS)

def summarize_conversation(history):
    summary_prompt = [
        {"role": "system", "content": "다음은 유저와 NPC의 대화야. 이 내용을 요약해줘."}
    ] + history

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=summary_prompt
    )
    return response.choices[0].message.content.strip()


print(f"💬 '{uid}'의 대화가 시작됩니다. 'exit' 입력 시 종료.\n")

while True:
    user_input = input("👤 You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("👋 대화를 종료합니다.")
        break

    # 메시지 불러오기 & 추가
    messages = get_user_messages()
    messages.append({"role": "user", "content": user_input})

    # GPT 응답
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    reply = response.choices[0].message.content.strip()
    print("🤖 종석햄:", reply)

    messages.append({"role": "assistant", "content": reply})

    # 길이 초과 시 요약
    user_and_assistant = [m for m in messages if m["role"] in ["user", "assistant"]]
    if len(user_and_assistant) >= MAX_HISTORY * 2:
        print("🧠 대화가 길어져서 요약 중...\n")
        summary = summarize_conversation(user_and_assistant)
        messages = [
            {"role": "system", "content": f"이전 대화 요약: {summary}"},
            messages[-2],
            messages[-1]
        ]

    # 저장 + TTL 부여
    save_user_messages(messages)