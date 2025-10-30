# backend/eval/jee_bench_runner.py

import json
from agent.routing import route_question

# Load benchmark dataset
with open("data/jee_bench.json") as f:
    benchmark = json.load(f)

results = []

for item in benchmark:
    question = item["question"]
    expected = item["answer"]

    result = route_question(question)
    predicted = result["answer"]
    confidence = result["confidence"]

    # Simple match check (can be improved with fuzzy or semantic match)
    correct = expected.strip().lower() in predicted.strip().lower()

    results.append({
        "question": question,
        "expected": expected,
        "predicted": predicted,
        "confidence": confidence,
        "correct": correct
    })

# Summary
total = len(results)
correct = sum(r["correct"] for r in results)
avg_conf = sum(r["confidence"] for r in results) / total

print(f"\n✅ Benchmark Results on JEE Bench")
print(f"Total Questions: {total}")
print(f"Correct: {correct}")
print(f"Accuracy: {correct / total:.2%}")
print(f"Avg Confidence: {avg_conf:.2f}\n")
