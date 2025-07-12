import chromadb
from chromadb.config import Settings
import os

# ChromaDB 클라이언트 생성 (로컬 디스크에 저장)
# client = chromadb.Client(Settings(
#     persist_directory="./chroma_db",   # 저장 경로 (폴더 자동 생성됨)
#     anonymized_telemetry=False         # 익명 사용 통계 전송 비활성화
# ))
client = chromadb.PersistentClient(path="./chroma_db")

# 함수: 유저 ID로 컬렉션 가져오기 (없으면 생성)
def get_user_collection(npc_name:str, uid: str):
    collection = client.get_or_create_collection(name=f"{npc_name}_{uid}")
    return collection