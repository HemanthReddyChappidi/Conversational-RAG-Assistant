from langchain_community.document_loaders import PyPDFLoader
import os

def load_documents(data_path: str):
    documents = []
    
    for file in os.listdir(data_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(data_path, file))
            docs = loader.load()
            documents.extend(docs)
    
    return documents