from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from tqdm import tqdm
import json, os

# ✅ Config
COLLECTION_NAME = "math_kb"
DATASET_NAME = "daman1209arora/jeebench"
RESULTS_PATH = "backend/data/benchmark_results.json"

def run_benchmark():
    # ✅ Load dataset and filter for math-only
    dataset = load_dataset(DATASET_NAME, split="test")
    math_only = [item for item in dataset if item.get("subject", "").lower() == "math"]

    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = QdrantClient("http://localhost:6333")

    correct = 0
    total = 0
    mismatches = []
    results = []

    for i, item in enumerate(tqdm(math_only, desc="Benchmarking")):
        query = item.get("question", "").strip()
        expected = str(item.get("gold", "")).strip()

        if not query or not expected:
            continue

        vector = model.encode(query).tolist()
        search_results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=1,
            with_payload=True
        )

        if not search_results:
            print(f"⚠️ No match for: {query}")
            continue

        # ✅ Fallback to 'answer' if 'short_answer' missing
        payload = search_results[0].payload
        retrieved = payload.get("short_answer") or payload.get("answer", "")
        retrieved = retrieved.strip()

        source = payload.get("source", "unknown")
        confidence = search_results[0].score
        total += 1

        match = bool(retrieved) and (expected in retrieved or retrieved in expected)

        if match:
            correct += 1
        else:
            mismatches.append({
                "question": query,
                "expected": expected,
                "retrieved": retrieved,
                "source": source,
                "confidence": confidence
            })

        results.append({
            "question": query,
            "expected": expected,
            "retrieved": retrieved,
            "source": source,
            "confidence": confidence,
            "match": match
        })

        if i < 5:
            print(f"\n🔍 Q{i+1}: {query}")
            print(f"Expected: {expected}")
            print(f"Retrieved: {retrieved}")
            print(f"Match: {match} | Confidence: {confidence:.2f}")

    # ✅ Summary
    if total == 0:
        print("\n⚠️ Benchmark ran but no results were retrieved.")
    else:
        accuracy = (correct / total) * 100
        print(f"\n✅ Benchmark complete: {correct}/{total} correct ({accuracy:.2f}%)")

    if mismatches:
        print("\n❌ Mismatches:")
        for m in mismatches[:10]:
            print(f"- Q: {m['question']}\n  Expected: {m['expected']}\n  Retrieved: {m['retrieved']}\n")

    # ✅ Save results
    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n📁 Results saved to {RESULTS_PATH}")

if __name__ == "__main__":
    run_benchmark()
