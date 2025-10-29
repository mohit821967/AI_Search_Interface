# src/db/vector_utils.py

import psycopg2
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "nlss_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")

# Initialize embedding model (same as before)
model = SentenceTransformer('all-MiniLM-L6-v2')

def connect_db():
    """Connect to PostgreSQL and return connection + cursor."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn, conn.cursor()

def search_products_by_semantic_similarity(query_text, top_k=5):
    """Return top_k most semantically similar products to the query text."""
    query_embedding = model.encode(query_text).tolist()
    conn, cur = connect_db()

    # vector similarity search using cosine distance (pgvector)
    sql = """
        SELECT id, name, price,
               1 - (embedding <=> %s::vector) AS similarity
        FROM products
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
    """
    cur.execute(sql, (query_embedding, query_embedding, top_k))
    results = cur.fetchall()

    cur.close()
    conn.close()
    return results
