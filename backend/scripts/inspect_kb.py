from qdrant_client import QdrantClient

client = QdrantClient("http://localhost:6333")

points = client.scroll(
    collection_name="math_kb",
    limit=5,
    with_payload=True
)

for p in points[0]:
    print("\n🧠 KB Entry:")
    print("ID:", p.id)
    print("Payload:", p.payload)
