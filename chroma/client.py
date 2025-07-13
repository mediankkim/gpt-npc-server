import chromadb
import os
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

embedding_fn = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"))

# ChromaDB 클라이언트 생성 (로컬 디스크에 저장)
client = chromadb.PersistentClient(path="./chroma_db")

def get_user_collection(npc_name: str, uid: str):
    return client.get_or_create_collection(
        name=f"{npc_name}_{uid}",
        embedding_function=embedding_fn
    )