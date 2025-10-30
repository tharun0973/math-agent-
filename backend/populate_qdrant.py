from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
from sentence_transformers import SentenceTransformer
import json

# ✅ Load model and Qdrant client
model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient("http://localhost:6333")

# ✅ Create collection if not exists
client.recreate_collection(
    collection_name="math_questions",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# ✅ Load your dataset
with open("math_dataset.json", "r") as f:
    data = json.load(f)

points = []
for i, item in enumerate(data):
    question = item["question"]
    vector = model.encode(question).tolist()

    # ✅ Ensure structured payload
    payload = {
        "question": question,
        "answer": item.get("answer", ""),
        "steps": item.get("steps", []),
        "solution": item.get("solution", ""),
        "confidence": item.get("confidence", 0.9)
    }

    points.append(PointStruct(id=i, vector=vector, payload=payload))

# ✅ Upload to Qdrant
client.upsert(collection_name="math_questions", points=points)
print(f"✅ Uploaded {len(points)} questions to Qdrant.")
