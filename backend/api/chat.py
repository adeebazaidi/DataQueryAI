from fastapi import APIRouter
from backend.models.schemas import ChatRequest, ChatResponse
from backend.services.router import route_query

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def handle_chat(request: ChatRequest):
    return route_query(request)
