from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient("localhost", port=6333)

client.create_collection(
    collection_name="math_kb",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

print("✅ Created Qdrant collection: math_kb")
