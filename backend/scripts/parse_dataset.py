import json

def parse_raw_dataset():
    # Replace this with actual dataset loading logic
    raw_data = [
        {
            "question": "Evaluate lim(x→0) (sin x - x) / x^3",
            "solution": [
                "Use Taylor expansion: sin x ≈ x - x^3/6 + x^5/120",
                "Substitute into numerator: (x - x^3/6 + ...) - x = -x^3/6 + ...",
                "Divide by x^3: (-x^3/6 + ...) / x^3 = -1/6 + ...",
                "Take limit as x→0: answer is -1/6"
            ],
            "answer": "-1/6",
            "source": "JEE 2020",
            "topics": ["calculus", "limits"],
            "difficulty": "medium"
        }
    ]

    formatted = []
    for i, item in enumerate(raw_data):
        formatted.append({
            "id": f"Q{i+1:03}",
            "question_text": item["question"],
            "canonical_solution_steps": item["solution"],
            "short_answer": item["answer"],
            "topics": item["topics"],
            "difficulty": item["difficulty"],
            "source": item["source"]
        })

    with open("backend/data/math_dataset.json", "w") as f:
        json.dump(formatted, f, indent=2)

if __name__ == "__main__":
    parse_raw_dataset()
