from fastapi import FastAPI
from npcs import eren

app = FastAPI()

# 에렌 NPC 라우터 등록
app.include_router(eren.router, prefix="/npc/eren", tags=["에렌 NPC"])

# 헬스 체크용 기본 엔드포인트
@app.get("/")
def root():
    return {"message": "GPT NPC FastAPI 서버 작동 중!"}