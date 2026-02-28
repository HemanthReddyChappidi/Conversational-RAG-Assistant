# 📚 RAG Knowledge Assistant

End-to-end Retrieval-Augmented Generation (RAG) system that answers questions from custom documents using LLMs.

## Features
- Upload PDFs and index documents
- Semantic search using embeddings + FAISS
- FastAPI backend
- Streamlit chat UI
- Docker-ready
- Environment variable based secrets

## Tech Stack
Python, LangChain, OpenAI, FAISS, FastAPI, Streamlit, Docker

## Run locally

### 1. Install deps
pip install -r requirements.txt

### 2. Add API key
Create `.env`
OPENAI_API_KEY=your_key_here

### 3. Start backend
uvicorn app.main:app --reload

### 4. Start UI
streamlit run streamlit_app.py


### 5.Test Docker locally

Build image:

docker build -t rag-backend .

Run container:

docker run -p 8000:8000 --env-file .env rag-backend

Open browser:

http://localhost:8000/docs

If this works → you are cloud-ready.


### 🔌 Embedding Backends

This project supports two embedding modes.

Option 1 — OpenAI Embeddings (default)

Uses OpenAI API for embeddings.

Create .env:

OPENAI_API_KEY=your_key_here

EMBEDDING_BACKEND=openai


Option 2 — Local HuggingFace Embeddings (free)

Runs embeddings locally using Sentence Transformers.

Create .env:

OPENAI_API_KEY=your_key_here

EMBEDDING_BACKEND=huggingface

Install extra dependency:

pip install sentence-transformers

⚠️ When switching embedding backend, delete the vector DB and re-index:

rm -rf vector_db

mkdir vector_db
