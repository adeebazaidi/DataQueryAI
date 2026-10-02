import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.models.schemas import DocumentResponse, SummaryResponse
from backend.config import settings
from backend.services.rag_service import index_document, generate_document_summary

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_path = os.path.join(settings.DOCUMENTS_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Index document
        index_document(file_path, file.filename)
        
        return DocumentResponse(
            id=file.filename,
            filename=file.filename,
            status="Indexed"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[DocumentResponse])
def get_documents():
    if not os.path.exists(settings.DOCUMENTS_DIR):
        return []
    files = os.listdir(settings.DOCUMENTS_DIR)
    return [
        DocumentResponse(id=f, filename=f, status="Indexed")
        for f in files if f.endswith(".pdf")
    ]

@router.delete("/{document_id}")
def delete_document(document_id: str):
    file_path = os.path.join(settings.DOCUMENTS_DIR, document_id)
    if os.path.exists(file_path):
        os.remove(file_path)
        # TODO: removing from vector store is complex, we just remove file here
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Document not found")

@router.post("/{document_id}/summarize", response_model=SummaryResponse)
def summarize_document(document_id: str):
    file_path = os.path.join(settings.DOCUMENTS_DIR, document_id)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        summary = generate_document_summary(file_path)
        return SummaryResponse(document_id=document_id, summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
