from qdrant_client import QdrantClient

client = QdrantClient("http://localhost:6333")
info = client.get_collection("math_kb")

print("✅ Collection found.")

# Access vector config from nested dictionary
vectors_config = info.config.params.vectors

if isinstance(vectors_config, dict):
    for name, params in vectors_config.items():
        print(f"Vector name: {name}")
        print(f"Size: {params.size}")
        print(f"Distance: {params.distance}")
else:
    print(f"Size: {vectors_config.size}")
    print(f"Distance: {vectors_config.distance}")
