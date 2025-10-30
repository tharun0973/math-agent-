from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from tqdm import tqdm
import json

def ingest_gsm8k():
    dataset = load_dataset("openai/gsm8k", "main", split="train")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = QdrantClient("http://localhost:6333")

    formatted = []
    vectors = []

    for i, item in enumerate(tqdm(dataset, desc="Embedding GSM8K")):
        question = item["question"].strip()
        solution = item["answer"].strip()
        steps = solution.split("\n")
        answer = steps[-1] if steps else ""

        entry = {
            "id": f"GSM8K_{i+1:04}",
            "question_text": question,
            "canonical_solution_steps": steps,
            "short_answer": answer,
            "topics": ["word problems", "reasoning"],
            "difficulty": "easy",
            "source": "gsm8k"
        }

        formatted.append(entry)
        vectors.append(model.encode(question).tolist())

    points = [
        PointStruct(id=i + 20000, vector=vectors[i], payload=formatted[i])
        for i in range(len(formatted))
    ]

    for i in range(0, len(points), 500):
        batch = points[i:i+500]
        client.upsert(collection_name="math_kb", points=batch)

    with open("backend/data/math_dataset.json", "a") as f:
        json.dump(formatted, f, indent=2)

if __name__ == "__main__":
    ingest_gsm8k()
