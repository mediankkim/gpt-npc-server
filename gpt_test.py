from flask import Flask, request, jsonify
import redis
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 모든 origin 허용

# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Redis 클라이언트
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# OpenAI 클라이언트
client = OpenAI(api_key=OPENAI_API_KEY)

# 캐릭터 시스템 프롬프트
CHARACTER_PROMPT = {
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

MAX_HISTORY = 10  # user+assistant 쌍 기준
TTL_MINUTES = 60  # Redis TTL (분)

def summarize_conversation(history):
    summary_prompt = [
        {"role": "system", "content": "다음은 유저와 NPC의 대화야. 이 내용을 요약해줘."}
    ] + history

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=summary_prompt
    )
    return response.choices[0].message.content.strip()

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    data = request.get_json()
    uid = data.get("uid")
    message = data.get("message")

    if not uid or not message:
        return jsonify({"error": "uid와 message는 필수입니다."}), 400

    print(f"Received message from {uid}: {message}")

    key = f"chat:{uid}"
    raw_history = r.get(key)
    if raw_history:
        messages = json.loads(raw_history)
    else:
        messages = [CHARACTER_PROMPT]

    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    reply = response.choices[0].message.content.strip()
    print(f"Reply from GPT: {reply}")

    messages.append({"role": "assistant", "content": reply})

    # 대화 요약 조건 체크
    conversation_only = [m for m in messages if m["role"] in ["user", "assistant"]]
    if len(conversation_only) >= MAX_HISTORY * 2:
        print("\n🧠 대화가 길어져서 요약 중...\n")
        summary = summarize_conversation(conversation_only)
        print("📄 요약:", summary)
        messages = [
            {"role": "system", "content": f"이전 대화 요약: {summary}"},
            messages[-2],  # 마지막 user
            messages[-1]   # 마지막 assistant
        ]

    r.setex(key, TTL_MINUTES * 60, json.dumps(messages))

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5050)
