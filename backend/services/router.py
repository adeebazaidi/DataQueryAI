from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from backend.config import settings
from backend.models.schemas import ChatRequest, ChatResponse
from backend.services.rag_service import query_rag
from backend.services.sql_service import query_sql

def determine_query_type(question: str) -> str:
    llm = ChatOpenAI(temperature=0, api_key=settings.OPENAI_API_KEY)
    prompt = PromptTemplate.from_template(
        "You are a router. The user will ask a question. Determine if the question should be answered using:\n"
        "1. 'Database' - for questions about employees, departments, leave requests, expenses, salaries, counts, aggregations.\n"
        "2. 'Document' - for questions about company policies, rules, handbooks, guidelines, textual knowledge.\n\n"
        "Respond with ONLY the word 'Database' or 'Document'.\n\n"
        "Question: {question}\n"
        "Type:"
    )
    chain = prompt | llm
    response = chain.invoke({"question": question})
    type_str = response.content.strip().lower()
    
    if "database" in type_str:
        return "Database"
    return "Document Search"

def route_query(request: ChatRequest) -> ChatResponse:
    query_type = determine_query_type(request.query)
    
    if query_type == "Database":
        answer, sql_query = query_sql(request.query)
        return ChatResponse(
            query_type="Database",
            answer=answer,
            sql_query=sql_query,
            session_id=request.session_id
        )
    else:
        answer, sources = query_rag(request.query)
        return ChatResponse(
            query_type="Document Search",
            answer=answer,
            sources=sources,
            session_id=request.session_id
        )
