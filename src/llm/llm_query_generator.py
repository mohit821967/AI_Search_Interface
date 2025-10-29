import subprocess
import textwrap

PROMPT_TEMPLATE = textwrap.dedent("""
You are a PostgreSQL expert.
Convert the user's natural language request into an SQL SELECT query.

Database schema:
- employees(id, name, department_id, email, salary)
- departments(id, name)
- orders(id, customer_name, employee_id, order_total, order_date)
- products(id, name, price, embedding)

Foreign keys:
- employees.department_id -> departments.id
- orders.employee_id -> employees.id

User request: "{query}"

Return ONLY SQL (no explanation, no code block).
""")

def nl_to_sql(query_text: str) -> str:
    """Call local Llama 3 via Ollama and return an SQL string."""
    full_prompt = PROMPT_TEMPLATE.format(query=query_text)

    # 🧠 Fix: set encoding explicitly
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=full_prompt.encode("utf-8"),  # send prompt as bytes
        capture_output=True
    )

    sql_output = result.stdout.decode("utf-8", errors="ignore").strip()

    # Clean up accidental code-block formatting
    if "```" in sql_output:
        parts = sql_output.split("```")
        sql_output = "".join(
            p for p in parts if "SELECT" in p or "select" in p
        ).replace("sql", "").strip()
    return sql_output
