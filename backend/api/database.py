from fastapi import APIRouter
from backend.sql.database import get_schema

router = APIRouter()

@router.get("/schema")
def schema():
    return get_schema()
