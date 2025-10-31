import os
import logging
import requests
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import SearchParams, Distance, VectorParams
from sentence_transformers import SentenceTransformer

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize embedding model
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("✅ Sentence Transformer model loaded")
except Exception as e:
    logger.error(f"❌ Failed to load Sentence Transformer: {e}")
    model = None

# Initialize Qdrant client
try:
    client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
    logger.info("✅ Qdrant client initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize Qdrant client: {e}")
    client = None

def check_collection_exists(collection_name: str = "math_kb") -> bool:
    """Check if the collection exists in Qdrant"""
    if not client:
        return False
    try:
        collections = client.get_collections()
        return any(col.name == collection_name for col in collections.collections)
    except Exception as e:
        logger.error(f"❌ Error checking collections: {e}")
        return False

def generate_embedding(text: str) -> list:
    """Generate embedding using Sentence Transformer or Ollama fallback"""
    try:
        if model:
            return model.encode(text).tolist()
        else:
            response = requests.post(
                "http://localhost:11434/api/embeddings",
                json={"model": "gemma:2b", "prompt": text},
                timeout=30
            )
            return response.json().get("embedding", [])
    except Exception as e:
        logger.error(f"❌ Embedding generation failed: {e}")
        return [0.0] * 384  # Dummy fallback

def search_knowledge_base(question: str, collection_name: str = "math_kb", min_score: float = 0.75) -> dict:
    """
    Search the knowledge base for relevant math content.
    Returns dict with answer, steps, solution, confidence or None if not found.
    """
    if not check_collection_exists(collection_name):
        logger.warning(f"⚠️ Collection '{collection_name}' does not exist. Skipping KB search.")
        return None

    try:
        embedding = generate_embedding(question)

        hits = client.search(
            collection_name=collection_name,
            query_vector=embedding,
            limit=3,
            score_threshold=min_score,
            search_params=SearchParams(hnsw_ef=128)
        )

        if not hits:
            logger.info(f"📭 No KB results for: {question[:50]}...")
            return None

        top_hit = hits[0]
        payload = top_hit.payload

        # Debug: show matched KB question
        logger.info(f"🎯 Matched KB question: {payload.get('question', '')}")

        steps = payload.get("steps", [])
        if isinstance(steps, str):
            steps = [s.strip() for s in steps.split("\n") if s.strip()]

        result = {
            "answer": payload.get("answer", ""),
            "steps": steps,
            "solution": payload.get("solution", ""),
            "confidence": float(top_hit.score),
            "topic": payload.get("topic", "General"),
            "difficulty": payload.get("difficulty", "Unknown"),
            "source": payload.get("source", "Unknown")
        }

        logger.info(f"✅ KB hit: {payload.get('question', '')} | Score: {result['confidence']:.2f}")
        return result

    except Exception as e:
        logger.error(f"❌ Qdrant search failed: {e}")
        return None
