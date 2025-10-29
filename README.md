# Natural Language SQL Search (Streamlit + PostgreSQL + pgvector)

**Objective:** Build a Natural Language Search Interface to query a PostgreSQL database using Streamlit. Supports hybrid search (LLM → SQL and semantic vector search).

## Features
- Local PostgreSQL with `pgvector` for embeddings.
- Local embeddings using `sentence-transformers` (`all-MiniLM-L6-v2`).
- Local LLM (Ollama + Llama 3) to convert NL → SQL.
- Safe SQL execution (only `SELECT` allowed) + basic auto-fixes for common LLM mistakes.
- Streamlit UI with two modes:
  - **SQL Mode:** natural language → SQL → executed on DB.
  - **Semantic Mode:** product semantic search using vector similarity.

## Repo Structure

natural_language_sql_search/
├── data/ # SQL schema + embedding init script
├── src/
│ ├── db/
│ ├── llm/
│ ├── ui/
│ └── utils/
├── notebooks/
├── docs/
├── .env.example
├── requirements.txt
└── README.md


## Quick Setup (Local, free)
1. Install PostgreSQL, create DB `nlss_db`, and enable `pgvector`.
2. Clone repo and create Python venv:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate   # Windows
   pip install -r requirements.txt
