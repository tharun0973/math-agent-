from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from tqdm import tqdm
import json
import os

def ingest_gsm8k():
    # Load dataset and embedding model
    dataset = load_dataset("openai/gsm8k", "main", split="train")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = QdrantClient("http://localhost:6333")

    # Create collection if it doesn't exist
    if not client.collection_exists("math_kb"):
        client.create_collection(
            collection_name="math_kb",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

    points = []

    for i, item in enumerate(tqdm(dataset, desc="Embedding GSM8K")):
        question = item["question"].strip()
        solution = item["answer"].strip()
        steps = [step.strip() for step in solution.split("\n") if step.strip()]
        answer = steps[-1] if steps else solution

        vector = model.encode(question).tolist()

        payload = {
            "question": question,
            "answer": answer,
            "solution": solution,
            "steps": steps,
            "source": "gsm8k",
            "difficulty": "easy",
            "topics": ["word problems", "reasoning"]
        }

        points.append(PointStruct(id=i + 20000, vector=vector, payload=payload))

    # Batch upsert to Qdrant
    for i in range(0, len(points), 500):
        batch = points[i:i+500]
        client.upsert(collection_name="math_kb", points=batch)

    # Optional: Save to local JSON for inspection
    os.makedirs("backend/data", exist_ok=True)
    with open("backend/data/math_dataset.json", "w") as f:
        json.dump([p.payload for p in points], f, indent=2)

    print(f"✅ Embedded {len(points)} GSM8K questions into Qdrant.")

if __name__ == "__main__":
    ingest_gsm8k()
