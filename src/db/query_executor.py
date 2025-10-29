# src/db/query_executor.py
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
import re

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "nlss_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

def connect_db():
    """Establish a connection to PostgreSQL."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def is_safe_sql(query: str) -> bool:
    """Simple SQL validator — allows only SELECT queries."""
    query = query.strip().lower()
    # allow only SELECT ... and disallow any write/drop commands
    return (
        query.startswith("select")
        and not any(word in query for word in ["insert", "update", "delete", "drop", "alter"])
    )

def execute_query(query: str):
    """Validate and execute a SQL query safely."""
    if not is_safe_sql(query):
        return "❌ Unsafe or invalid query. Only SELECT statements are allowed."

    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return {"columns": columns, "rows": rows}
    except Exception as e:
        return f"❌ Error executing query: {e}"
