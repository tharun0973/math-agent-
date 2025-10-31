import json
import os

KB_PATH = "backend/data/kb.json"

def escape_markdown(text: str) -> str:
    """Escape markdown for safe JSON storage."""
    return json.dumps(text)[1:-1]

def to_kb_entry(fallback: dict) -> dict:
    """Convert DSPy fallback result to KB format."""
    return {
        "question": fallback["question"],
        "answer": fallback["answer"],
        "solution": fallback["solution"],
        "steps": fallback["steps"],
        "confidence": fallback["confidence"],
        "source": "DSPy fallback",
        "markdown": escape_markdown(
            f"## ✅ Final Answer\n\n{fallback['solution']}\n\n" +
            "## 🧠 Step-by-Step Breakdown\n" +
            "\n".join([f"### Step {i+1}\n{step}" for i, step in enumerate(fallback["steps"])])
        )
    }

def cache_fallback(fallback: dict):
    """Append fallback result to KB."""
    if not os.path.exists(KB_PATH):
        print("❌ KB file not found.")
        return

    with open(KB_PATH, "r") as f:
        kb = json.load(f)

    kb.append(to_kb_entry(fallback))

    with open(KB_PATH, "w") as f:
        json.dump(kb, f, indent=2)

    print(f"✅ Cached fallback: {fallback['question']}")

# Example usage:
if __name__ == "__main__":
    # Replace this with your actual fallback result
    fallback_result = {
        "question": "What is the Laplace transform of t^3?",
        "answer": "The Laplace transform of t^3 is 6 / s^4.",
        "solution": "L{t^3} = 3! / s^4 = 6 / s^4",
        "steps": [
            "Use the identity: L{t^n} = n! / s^(n+1)",
            "Here, n = 3 → 3! = 6",
            "So, L{t^3} = 6 / s^4"
        ],
        "confidence": 0.9
    }

    cache_fallback(fallback_result)
