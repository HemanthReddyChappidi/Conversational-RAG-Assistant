from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.utils import load_documents
from app.vector_store import create_vector_store
from app.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP

def ingest_documents():
    print("Loading documents...")
    docs = load_documents(DATA_PATH)

    print("Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(docs)

    print(f"Created {len(chunks)} chunks")

    print("Creating FAISS index...")
    create_vector_store(chunks)

    print("Ingestion complete!")