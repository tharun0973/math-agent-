from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import json, os

# ✅ Step 1: Extract math-only questions from JEEBench
print("📦 Loading JEEBench dataset...")
dataset = load_dataset("daman1209arora/jeebench", split="test")
math_only = [item for item in dataset if item.get("subject", "").lower() == "math"]

# ✅ Save to local file for audit
os.makedirs("backend/data", exist_ok=True)
with open("backend/data/jeebench_math.json", "w") as f:
    json.dump(math_only, f, indent=2)
print(f"✅ Saved {len(math_only)} math questions to backend/data/jeebench_math.json")

# ✅ Step 2: Embed and upsert into Qdrant
print("🔗 Connecting to Qdrant and embedding questions...")
client = QdrantClient("http://localhost:6333")
model = SentenceTransformer("all-MiniLM-L6-v2")

points = []
for i, item in enumerate(math_only):
    question = item["question"].strip()
    answer = str(item["gold"]).strip()
    vector = model.encode(question).tolist()

    payload = {
        "question": question,
        "short_answer": answer,
        "source": "jee_gold",
        "confidence": 0.95
    }

    points.append(PointStruct(id=i, vector=vector, payload=payload))

print(f"📤 Upserting {len(points)} entries into Qdrant collection 'math_kb'...")
client.upsert(collection_name="math_kb", points=points)
print("✅ Upsert complete.")
