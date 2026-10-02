from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class DocumentResponse(BaseModel):
    id: str
    filename: str
    status: str

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    query_type: str
    answer: str
    sources: Optional[List[Dict[str, Any]]] = None
    sql_query: Optional[str] = None
    session_id: str

class SummaryRequest(BaseModel):
    document_id: str

class SummaryResponse(BaseModel):
    document_id: str
    summary: str
