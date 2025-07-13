import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text: str, model="text-embedding-3-small"):
    response = openai.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding