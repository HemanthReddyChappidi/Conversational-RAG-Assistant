from langchain_openai import OpenAIEmbeddings
from app.config import OPENAI_API_KEY

MODEL_NAME = "text-embedding-3-small"

def get_embeddings():
    return OpenAIEmbeddings(
        model=MODEL_NAME,
        openai_api_key=OPENAI_API_KEY
    )