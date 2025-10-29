from src.llm.llm_query_generator import nl_to_sql
from src.db.query_executor import execute_query
import re

query_text = "show employees in HR earning more than 40000"

print("\n🧠 Natural Language Query:")
print(query_text)

# Step 1: Convert to SQL using LLM
sql_query = nl_to_sql(query_text)
print("\n🧩 Generated SQL (from LLM):")
print(sql_query)

# Step 2: Basic auto-fix for common LLM mistakes
# Fix single-value subqueries that return multiple rows
if re.search(r"=\s*\(SELECT id FROM departments", sql_query, re.IGNORECASE):
    sql_query = re.sub(r"=\s*\(SELECT id FROM departments", 
                       "IN (SELECT id FROM departments", sql_query, flags=re.IGNORECASE)
    print("\n⚙️ Auto-fixed SQL for multi-department case:")
    print(sql_query)

# Step 3: Execute the final SQL
result = execute_query(sql_query)

print("\n📊 Query Results:\n")

if isinstance(result, dict):
    if len(result["rows"]) == 0:
        print("No matching records found.")
    else:
        # Print headers
        print(" | ".join(result["columns"]))
        print("-" * 80)
        for row in result["rows"]:
            print(" | ".join(str(x) for x in row))
else:
    print(result)
