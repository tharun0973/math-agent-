import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("backend/data/math_dataset.json", "r") as f:
    data = json.load(f)

questions = [item["question_text"] for item in data]
embeddings = model.encode(questions)

client = QdrantClient("http://localhost:6333")
client.recreate_collection(
    collection_name="math_kb",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

points = [
    PointStruct(id=i, vector=embedding.tolist(), payload=data[i])
    for i, embedding in enumerate(embeddings)
]

client.upsert(collection_name="math_kb", points=points)
