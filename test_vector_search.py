from src.db.vector_utils import search_products_by_semantic_similarity

query = "computer accessories"
results = search_products_by_semantic_similarity(query)

print(f"\nTop similar products for: '{query}'\n")
for row in results:
    pid, name, price, similarity = row
    print(f"{name:25} | ₹{price} | similarity: {similarity:.3f}")
