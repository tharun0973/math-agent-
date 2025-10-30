from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from tqdm import tqdm

# Load JEEBench dataset
dataset = load_dataset("daman1209arora/jeebench", split="test")

# Initialize embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Qdrant client
client = QdrantClient("http://localhost:6333")

# Create or recreate collection
client.recreate_collection(
    collection_name="math_kb",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Prepare points
points = []
for i, item in enumerate(tqdm(dataset, desc="Embedding JEEBench")):
    question = item.get("question", "").strip()
    answer = str(item.get("gold", "")).strip()

    if not question or not answer:
        continue

    vector = model.encode(question).tolist()
    payload = {
        "question_text": question,
        "short_answer": answer
    }

    points.append(PointStruct(id=i, vector=vector, payload=payload))

# Upload to Qdrant
client.upsert(collection_name="math_kb", points=points)
