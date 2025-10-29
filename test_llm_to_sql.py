from src.llm.llm_query_generator import nl_to_sql

query = "show employees in HR earning more than 40000"
sql = nl_to_sql(query)

print("\nUser Query:", query)
print("\nGenerated SQL:\n", sql)
