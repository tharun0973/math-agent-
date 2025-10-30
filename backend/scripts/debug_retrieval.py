from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient("http://localhost:6333")

query = "Find the value of x in 2x + 3 = 7"
vector = model.encode(query).tolist()

results = client.search(
    collection_name="math_kb",
    query_vector=vector,
    limit=3,
    with_payload=True
)

if not results:
    print("❌ No results found.")
else:
    print("✅ Retrieved results:")
    for r in results:
        print(f"- Q: {r.payload.get('question_text', '')}")
        print(f"  A: {r.payload.get('short_answer', '')}\n")
