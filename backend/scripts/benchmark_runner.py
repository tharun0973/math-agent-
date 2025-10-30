from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from tqdm import tqdm

def run_benchmark():
    dataset = load_dataset("daman1209arora/jeebench", split="test")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = QdrantClient("http://localhost:6333")

    correct = 0
    total = 0
    mismatches = []

    for i, item in enumerate(tqdm(dataset, desc="Benchmarking")):
        query = item.get("question", "").strip()
        expected = str(item.get("gold", "")).strip()  # Use gold field

        if not query or not expected:
            continue

        vector = model.encode(query).tolist()
        results = client.search(
            collection_name="math_kb",
            query_vector=vector,
            limit=1,
            with_payload=True
        )

        if not results:
            print(f"⚠️ No match for: {query}")
            continue

        retrieved = results[0].payload.get("short_answer", "").strip()
        total += 1

        # Loose match: normalize and check substring
        if expected and (expected in retrieved or retrieved in expected):
            correct += 1
        else:
            mismatches.append({
                "question": query,
                "expected": expected,
                "retrieved": retrieved
            })

        # Debug first few queries
        if i < 5:
            print(f"\n🔍 Q{i+1}: {query}")
            print(f"Expected: {expected}")
            print(f"Retrieved: {retrieved}")

    if total == 0:
        print("\n⚠️ Benchmark ran but no results were retrieved. Check collection name or embedding logic.")
    else:
        print(f"\n✅ Benchmark complete: {correct}/{total} correct ({(correct/total)*100:.2f}%)")

    if mismatches:
        print("\n❌ Mismatches:")
        for m in mismatches[:10]:
            print(f"- Q: {m['question']}\n  Expected: {m['expected']}\n  Retrieved: {m['retrieved']}\n")

if __name__ == "__main__":
    run_benchmark()
