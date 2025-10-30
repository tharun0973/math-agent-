from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(url="http://localhost:6333")

client.recreate_collection(
    collection_name="math_kb",
    vectors_config=VectorParams(size=2048, distance=Distance.COSINE)
)


print("✅ Qdrant collection 'math_kb' created.")
