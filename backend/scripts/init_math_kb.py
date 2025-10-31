import json
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer

# Initialize embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Embedding model loaded")

# Initialize Qdrant client
client = QdrantClient("localhost", port=6333)
print("✅ Qdrant client initialized")

# Create or reset collection
client.recreate_collection(
    collection_name="math_kb",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)
print("✅ Created Qdrant collection: math_kb")

# Load KB entries from JSON
with open("backend/data/kb.json", "r") as f:
    kb_entries = json.load(f)

# Convert entries to Qdrant points
points = []
for i, entry in enumerate(kb_entries):
    vector = model.encode(entry["question"]).tolist()
    points.append(PointStruct(
        id=i,
        vector=vector,
        payload=entry
    ))

# Upload to Qdrant
client.upsert(collection_name="math_kb", points=points)
print(f"✅ Uploaded {len(points)} KB entries to Qdrant")
