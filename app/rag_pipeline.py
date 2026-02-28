from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from app.vector_store import load_vector_store
from app.config import LLM_MODEL
from app.config import OPENAI_API_KEY


def build_rag_chain():
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    llm = ChatOpenAI(model=LLM_MODEL,temperature=0,openai_api_key=OPENAI_API_KEY)
    prompt = ChatPromptTemplate.from_template("""
Answer the question based ONLY on the context below.
If you don't know the answer, say you don't know.

Context:
{context}

Question:
{input}
""")

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    return retrieval_chain