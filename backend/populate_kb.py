#!/usr/bin/env python3
"""
Script to populate Qdrant knowledge base with math dataset.
"""
import os
import json
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
from sentence_transformers import SentenceTransformer
import sys

# Initialize Qdrant client
client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))

# Initialize embedding model
print("Loading Sentence Transformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Model loaded successfully")

# Load dataset
print("Loading math dataset...")
with open("math_dataset.json", "r") as f:
    data = json.load(f)

print(f"✅ Loaded {len(data)} items from dataset")

# Create or recreate collection
collection_name = "math_kb"
try:
    print(f"\nCreating collection '{collection_name}'...")
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    print("✅ Collection created successfully")
except Exception as e:
    print(f"⚠️ Collection may already exist or error: {e}")

# Generate embeddings and prepare points
print("\nGenerating embeddings...")
points = []
for i, item in enumerate(data):
    if i % 5 == 0:
        print(f"Processing {i+1}/{len(data)}...")
    
    question = item.get("question", "")
    if not question:
        continue
    
    # Generate embedding
    vector = model.encode(question).tolist()
    
    # Prepare payload
    payload = {
        "question": question,
        "answer": item.get("answer", ""),
        "steps": item.get("steps", []),
        "solution": item.get("solution", ""),
        "topic": item.get("topic", "General"),
        "difficulty": item.get("difficulty", "Unknown"),
        "confidence": item.get("confidence", 0.9)
    }
    
    points.append(PointStruct(id=i, vector=vector, payload=payload))

print(f"✅ Generated {len(points)} embeddings")

# Upload to Qdrant
print("\nUploading to Qdrant...")
client.upsert(collection_name=collection_name, points=points)
print(f"✅ Successfully uploaded {len(points)} points to Qdrant!")

# Verify upload
collection_info = client.get_collection(collection_name)
print(f"\n📊 Collection info:")
print(f"  - Name: {collection_info.name}")
print(f"  - Points count: {collection_info.points_count}")
print(f"  - Vector size: {collection_info.config.params.vectors.size}")

# Test search
print("\n🔍 Testing search...")
test_query = "solve quadratic equation"
test_vector = model.encode(test_query).tolist()
hits = client.search(collection_name=collection_name, query_vector=test_vector, limit=3)

print(f"✅ Search test successful! Found {len(hits)} results:")
for i, hit in enumerate(hits):
    print(f"\n  Result {i+1}:")
    print(f"    Question: {hit.payload.get('question', '')}")
    print(f"    Score: {hit.score:.4f}")
    print(f"    Topic: {hit.payload.get('topic', '')}")

print("\n🎉 Knowledge base population complete!")

