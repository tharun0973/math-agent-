from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from tqdm import tqdm
import json
import os

def ingest_pw2025():
    dataset = load_dataset("PhysicsWallahAI/JEE-Main-2025-Math", "jan", split="test")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = QdrantClient("http://localhost:6333")

    if not client.collection_exists("math_kb"):
        client.create_collection(
            collection_name="math_kb",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

    formatted = []
    vectors = []

    for i, item in enumerate(tqdm(dataset, desc="Embedding PW2025")):
        question = item.get("question", "").strip()
        solution = item.get("solution", "").strip()
        steps = solution.split("\n") if solution else []
        answer = item.get("answer", "").strip()

        entry = {
            "id": f"PW2025_{i+1:04}",
            "question_text": question,
            "canonical_solution_steps": steps,
            "short_answer": answer,
            "topics": ["math"],
            "difficulty": item.get("difficulty", "medium"),
            "source": "PhysicsWallahAI"
        }

        formatted.append(entry)
        vectors.append(model.encode(question).tolist())

    points = [
        PointStruct(id=i + 10000, vector=vectors[i], payload=formatted[i])
        for i in range(len(formatted))
    ]

    for i in range(0, len(points), 500):
        batch = points[i:i+500]
        client.upsert(collection_name="math_kb", points=batch)

    os.makedirs("backend/data", exist_ok=True)
    with open("backend/data/math_dataset.json", "a") as f:
        json.dump(formatted, f, indent=2)

if __name__ == "__main__":
    ingest_pw2025()
