from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.memory import ChatMessageHistory

from app.vector_store import load_vector_store
from app.config import LLM_MODEL, OPENAI_API_KEY


# store sessions in memory
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def build_rag_chain():
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0,
        openai_api_key=OPENAI_API_KEY,
        streaming=True
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Answer the question based only on the provided context."),
            ("human", "{input}")
        ]
    )

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    conversational_chain = RunnableWithMessageHistory(
        retrieval_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    return conversational_chain