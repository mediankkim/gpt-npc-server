import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 초기 히스토리
# 🧠 캐릭터 설정 (system 프롬프트)
messages = [
    {
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
]

MAX_HISTORY = 10  # 이 이상 길어지면 요약 (user+assistant 쌍 기준)

def summarize_conversation(history):
    """GPT에게 대화 요약 요청"""
    summary_prompt = [
        {"role": "system", "content": "다음은 유저와 NPC의 대화야. 이 내용을 요약해줘."}
    ] + history

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=summary_prompt
    )

    return response.choices[0].message.content.strip()

print("💬 NPC와 대화를 시작하세요. 'exit' 입력 시 종료됩니다.\n")

while True:
    user_input = input("👤 You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 대화를 종료합니다.")
        break

    # 대화 추가
    messages.append({"role": "user", "content": user_input})

    # GPT 응답
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    reply = response.choices[0].message.content.strip()
    print("🤖 종석햄:", reply)

    # 응답 저장
    messages.append({"role": "assistant", "content": reply})

    # 👉 요약 조건 체크: user + assistant 메시지가 MAX_HISTORY 쌍을 넘으면 요약
    conversation_only = [m for m in messages if m["role"] in ["user", "assistant"]]
    if len(conversation_only) >= MAX_HISTORY * 2:
        print("\n🧠 대화가 길어져서 요약 중...\n")
        summary = summarize_conversation(conversation_only)
        print("📄 요약:", summary)

        # 새로운 system 메시지로 교체 + 마지막 유저 메시지만 남기기
        messages = [
            {"role": "system", "content": f"이전 대화 요약: {summary}"},
            messages[-2],  # 마지막 user
            messages[-1]   # 마지막 assistant
        ]