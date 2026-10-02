import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from backend.config import settings

def get_embeddings():
    return OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)

def load_and_split_document(file_path: str):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len
    )
    return text_splitter.split_documents(documents)

def add_to_vector_store(chunks):
    embeddings = get_embeddings()
    if os.path.exists(settings.VECTOR_STORE_PATH) and os.path.exists(os.path.join(settings.VECTOR_STORE_PATH, "index.faiss")):
        vector_store = FAISS.load_local(settings.VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
        vector_store.add_documents(chunks)
        vector_store.save_local(settings.VECTOR_STORE_PATH)
    else:
        vector_store = FAISS.from_documents(chunks, embeddings)
        vector_store.save_local(settings.VECTOR_STORE_PATH)

def get_retriever():
    embeddings = get_embeddings()
    if os.path.exists(settings.VECTOR_STORE_PATH) and os.path.exists(os.path.join(settings.VECTOR_STORE_PATH, "index.faiss")):
        vector_store = FAISS.load_local(settings.VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
        return vector_store.as_retriever(search_kwargs={"k": 3})
    return None
