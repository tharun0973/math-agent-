import json

def format_markdown(entry):
    raw = f"""## ✅ Final Answer
\

\[
{entry['solution']}
\\]



## 🧠 Step-by-Step Breakdown
""" + "\n".join([f"### Step {i+1}\n{step}" for i, step in enumerate(entry["steps"])])
    # Escape backslashes and newlines
    return json.dumps(raw)[1:-1]  # removes outer quotes

with open("backend/data/kb.json", "r") as f:
    kb = json.load(f)

for entry in kb:
    entry["markdown"] = format_markdown(entry)

with open("backend/data/kb.json", "w") as f:
    json.dump(kb, f, indent=2, ensure_ascii=False)

print(f"✅ Escaped markdown for {len(kb)} entries")
