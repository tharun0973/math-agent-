from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from tqdm import tqdm

custom_questions = [
    {
        "question": "If there are 3 apples and you eat 1, how many are left?",
        "answer": "2",
        "steps": ["Start with 3 apples.", "Eat 1 apple.", "3 - 1 = 2 apples left."],
        "solution": "Start with 3 apples. Eat 1. 3 - 1 = 2 apples left."
    },
    {
        "question": "What is the derivative of x^2?",
        "answer": "2x",
        "steps": ["The derivative of x^n is n*x^(n-1).", "Here, n = 2.", "So, derivative of x^2 is 2x."],
        "solution": "Using power rule: d/dx(x^2) = 2x"
    },
    {
        "question": "What is the integral of 1/x?",
        "answer": "ln|x| + C",
        "steps": ["The integral of 1/x is a standard result.", "∫1/x dx = ln|x| + C."],
        "solution": "∫1/x dx = ln|x| + C"
    }
]

def ingest_custom():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = QdrantClient("http://localhost:6333")

    points = []
    for i, item in enumerate(tqdm(custom_questions, desc="Embedding custom questions")):
        vector = model.encode(item["question"]).tolist()
        payload = {
            "question": item["question"],
            "answer": item["answer"],
            "steps": item["steps"],
            "solution": item["solution"],
            "source": "custom",
            "difficulty": "easy",
            "topics": ["basic math", "demo"]
        }
        points.append(PointStruct(id=90000 + i, vector=vector, payload=payload))

    client.upsert(collection_name="math_kb", points=points)
    print("✅ Custom questions added to Qdrant.")

if __name__ == "__main__":
    ingest_custom()
