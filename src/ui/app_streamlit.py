import sys, os, re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from src.llm.llm_query_generator import nl_to_sql
from src.db.query_executor import execute_query
from src.db.vector_utils import search_products_by_semantic_similarity

st.set_page_config(page_title="AI Database Search", layout="wide")

st.title("🔍 AI Database Search Interface")
st.caption("Ask questions naturally — choose between SQL query mode and semantic product search.")

# Sidebar mode selector
mode = st.sidebar.radio("Choose Search Mode:", ["🧠 SQL Mode", "🧭 Semantic Mode"])

# --- SQL Mode ---
if mode == "🧠 SQL Mode":
    st.subheader("Natural Language → SQL Search")
    query_text = st.text_area(
        "Ask about employees, departments, or orders:",
        placeholder="e.g. Show employees in HR earning more than 40000"
    )

    if st.button("Run SQL Query"):
        if not query_text.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Generating SQL using Llama 3..."):
                sql_query = nl_to_sql(query_text)

            st.subheader("🧩 Generated SQL")
            st.code(sql_query, language="sql")

            # Fix subquery if needed
            if re.search(r"=\s*\(SELECT id FROM departments", sql_query, re.IGNORECASE):
                sql_query = re.sub(
                    r"=\s*\(SELECT id FROM departments",
                    "IN (SELECT id FROM departments",
                    sql_query,
                    flags=re.IGNORECASE,
                )
                st.info("Auto-fixed multi-department case in SQL.")
                st.code(sql_query, language="sql")

            # Execute SQL safely
            with st.spinner("Executing SQL..."):
                result = execute_query(sql_query)

            st.subheader("📊 Query Results")
            if isinstance(result, dict):
                if len(result["rows"]) == 0:
                    st.warning("No results found.")
                else:
                    st.dataframe(result["rows"], use_container_width=True)
            else:
                st.error(result)

# --- Semantic Mode ---
elif mode == "🧭 Semantic Mode":
    st.subheader("Semantic Product Search")
    semantic_query = st.text_input(
        "Describe what you're looking for:",
        placeholder="e.g. cheap computer accessories"
    )

    top_k = st.slider("Number of results:", 1, 10, 5)

    if st.button("Search Products"):
        if not semantic_query.strip():
            st.warning("Please enter a product description.")
        else:
            with st.spinner("Performing semantic search..."):
                results = search_products_by_semantic_similarity(semantic_query, top_k=top_k)

            if len(results) == 0:
                st.warning("No matching products found.")
            else:
                st.success(f"Top {len(results)} similar products:")
                st.table(
                    [
                        {"Product": name, "Price": price, "Similarity": round(similarity, 3)}
                        for _, name, price, similarity in results
                    ]
                )
