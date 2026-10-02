from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import chat, documents, database
from backend.sql.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="DataQuery AI API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(database.router, prefix="/api/database", tags=["Database"])

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    code = "INTERNAL_SERVER_ERROR"
    if isinstance(exc, OperationalError):
        code = "DATABASE_UNAVAILABLE"
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False, 
            "error": {
                "code": code,
                "message": str(exc)
            }
        }
    )

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
