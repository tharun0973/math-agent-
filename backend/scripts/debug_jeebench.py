from datasets import load_dataset

dataset = load_dataset("daman1209arora/jeebench", split="test")

for i in range(5):
    item = dataset[i]
    print(f"\n🔍 Entry {i+1}")
    for k, v in item.items():
        print(f"{k}: {v}")
