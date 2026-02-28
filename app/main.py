from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import shutil
import os
from app.rag_pipeline import build_rag_chain
from app.ingest import ingest_documents
from app.config import DATA_PATH

app = FastAPI(title="RAG Knowledge Assistant")

qa_chain = None

@app.on_event("startup")
def startup_event():
    global qa_chain
    if os.path.exists("vector_db"):
        qa_chain = build_rag_chain()

@app.get("/health")
def health():
    return {"status": "running"}

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    file_path = f"{DATA_PATH}/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_documents()

    global qa_chain
    qa_chain = build_rag_chain()

    return {"message": "File uploaded and indexed"}

@app.post("/ask")
def ask_question(question: str, session_id: str = "default"):

    if qa_chain is None:
        return {"error": "Please upload a document first."}

    result = qa_chain.invoke(
        {"input": question},
        config={"configurable": {"session_id": session_id}}
    )

    sources = []
    for doc in result["context"]:
        sources.append(doc.metadata.get("source"))

    return {
        "answer": result["answer"],
        "sources": list(set(sources))
    }


@app.post("/ask_stream")
def ask_question_stream(question: str, session_id: str = "streamlit_user"):

    if qa_chain is None:
        return StreamingResponse(
            iter(["Please upload a document first."]),
            media_type="text/plain"
        )

    def generate():
        for chunk in qa_chain.stream(
            {"input": question},
            config={"configurable": {"session_id": session_id}}
        ):
            if "answer" in chunk:
                yield chunk["answer"]

    return StreamingResponse(generate(), media_type="text/plain")