import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from backend.config import settings
from backend.sql.database import get_schema
from backend.sql.query_executor import execute_safe_sql, is_safe_sql

def query_sql(question: str):
    schema = get_schema()
    schema_str = "\n".join([f"Table {table}: {', '.join(columns)}" for table, columns in schema.items()])
    
    llm = ChatOpenAI(temperature=0, api_key=settings.OPENAI_API_KEY)
    
    # Step 1: Generate SQL
    prompt_gen = PromptTemplate.from_template(
        "You are an expert SQL assistant. Given the following database schema, write a valid SQLite SELECT query to answer the user's question.\n"
        "Return ONLY the SQL query, without any markdown formatting, backticks, or extra text.\n\n"
        "Schema:\n{schema}\n\n"
        "Question: {question}\n\n"
        "SQL Query:"
    )
    
    chain_gen = prompt_gen | llm
    sql_response = chain_gen.invoke({"schema": schema_str, "question": question})
    sql_query = sql_response.content.strip().replace("```sql", "").replace("```", "").strip()
    
    if not is_safe_sql(sql_query):
        return "The generated SQL query is unsafe or invalid.", sql_query
    
    # Step 2: Execute SQL
    results = execute_safe_sql(sql_query)
    
    if isinstance(results, dict) and "error" in results:
        return f"Error executing query: {results['error']}", sql_query
    
    if not results:
        return "No results found for your query.", sql_query
        
    # Step 3: Explain Results
    prompt_explain = PromptTemplate.from_template(
        "You are a helpful data analyst. The user asked a question, we executed a SQL query, and got the following results.\n"
        "Explain the results in a concise, natural language format directly answering the question.\n\n"
        "Question: {question}\n"
        "SQL Executed: {sql}\n"
        "Results: {results}\n\n"
        "Answer:"
    )
    
    chain_explain = prompt_explain | llm
    explanation_response = chain_explain.invoke({
        "question": question,
        "sql": sql_query,
        "results": json.dumps(results[:50]) # limit results for prompt
    })
    
    return explanation_response.content, sql_query
