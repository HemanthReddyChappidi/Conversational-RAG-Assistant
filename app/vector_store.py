# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from app.config import VECTOR_DB_PATH, EMBEDDING_MODEL, OPENAI_API_KEY

# def create_vector_store(chunks):
#     embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)
#     vector_store = FAISS.from_documents(chunks, embeddings)  # also fix from previous error
#     vector_store.save_local(VECTOR_DB_PATH)
#     return vector_store

# def load_vector_store():
#     embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)
#     return FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)


from langchain_community.vectorstores import FAISS
from app.config import VECTOR_DB_PATH, EMBEDDING_BACKEND

# choose backend dynamically
if EMBEDDING_BACKEND == "huggingface":
    from app.embeddings.hf_embeddings import get_embeddings
else:
    from app.embeddings.openai_embeddings import get_embeddings


def create_vector_store(chunks):
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(VECTOR_DB_PATH)
    return vector_store


def load_vector_store():
    embeddings = get_embeddings()
    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )