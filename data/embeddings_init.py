# data/embeddings_init.py

from sentence_transformers import SentenceTransformer
import psycopg2
#from psycopg2.extras import register_vector
from tqdm import tqdm
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "nlss_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Connect to database
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cur = conn.cursor()

# Initialize model
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Fetch all product names
cur.execute("SELECT id, name FROM products")
products = cur.fetchall()

print(f"Found {len(products)} products. Generating embeddings...")

for pid, name in tqdm(products):
    embedding = model.encode(name).tolist()  # convert to list of floats
    cur.execute(
        "UPDATE products SET embedding = %s WHERE id = %s",
        (embedding, pid)
    )

conn.commit()
cur.close()
conn.close()

print("✅ Embeddings stored successfully in 'products' table!")
