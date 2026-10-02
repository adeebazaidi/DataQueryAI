from sqlalchemy import text
from backend.sql.database import engine

def is_safe_sql(query: str) -> bool:
    query = query.upper()
    unsafe_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE", "GRANT", "REVOKE"]
    for keyword in unsafe_keywords:
        if keyword in query.split():
            return False
    if not query.strip().startswith("SELECT"):
        return False
    return True

def execute_safe_sql(query: str):
    if not is_safe_sql(query):
        return {"error": "Only SELECT queries are allowed for safety reasons."}
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            keys = result.keys()
            rows = result.fetchall()
            return [dict(zip(keys, row)) for row in rows]
    except Exception as e:
        return {"error": str(e)}
