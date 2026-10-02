from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from backend.config import settings
from backend.rag.vector_store import load_and_split_document, add_to_vector_store, get_retriever

def index_document(file_path: str, filename: str):
    chunks = load_and_split_document(file_path)
    # Add metadata
    for chunk in chunks:
        chunk.metadata["filename"] = filename
    add_to_vector_store(chunks)

def query_rag(question: str):
    retriever = get_retriever()
    if not retriever:
        return "No documents indexed yet.", []
    
    docs = retriever.invoke(question)
    if not docs:
        return "I couldn't find any relevant information in the documents.", []
    
    context = "\n\n".join([f"Document: {doc.metadata.get('filename', 'Unknown')} (Page {doc.metadata.get('page', 'Unknown')})\nContent: {doc.page_content}" for doc in docs])
    
    llm = ChatOpenAI(temperature=0, api_key=settings.OPENAI_API_KEY)
    prompt = PromptTemplate.from_template(
        "You are an enterprise assistant answering questions based on the following context. "
        "If you don't know the answer, just say you don't know. Don't make up information.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    )
    
    chain = prompt | llm
    response = chain.invoke({"context": context, "question": question})
    
    sources = []
    for doc in docs:
        sources.append({
            "filename": doc.metadata.get("filename", "Unknown"),
            "page": doc.metadata.get("page", 0) + 1
        })
    
    # deduplicate sources
    unique_sources = [dict(t) for t in {tuple(d.items()) for d in sources}]
    
    return response.content, unique_sources

def generate_document_summary(file_path: str):
    chunks = load_and_split_document(file_path)
    # Only use first few chunks to avoid token limits for simple summary
    text_to_summarize = "\n".join([chunk.page_content for chunk in chunks[:5]])
    
    llm = ChatOpenAI(temperature=0, api_key=settings.OPENAI_API_KEY)
    prompt = PromptTemplate.from_template(
        "Summarize the following document content into key points and important policies.\n\n"
        "Document Text:\n{text}\n\n"
        "Summary:"
    )
    
    chain = prompt | llm
    response = chain.invoke({"text": text_to_summarize})
    return response.content
