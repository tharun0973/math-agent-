import os
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, PointStruct, SearchParams, Distance, VectorParams
from qdrant_client.http.models import SearchRequest
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import logging

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
        collection_names = [col.name for col in collections.collections]
        return collection_name in collection_names
    except Exception as e:
        logger.error(f"❌ Error checking collections: {e}")
        return False

def generate_embedding(text: str) -> list:
    """Generate embedding using Sentence Transformer or Ollama fallback"""
    try:
        # Try Sentence Transformer first (more reliable and faster)
        if model:
            embedding = model.encode(text).tolist()
            return embedding
        else:
            # Fallback to Ollama if Sentence Transformer not available
            import requests
            response = requests.post(
                "http://localhost:11434/api/embeddings",
                json={"model": "gemma:2b", "prompt": text},
                timeout=30
            )
            result = response.json()
            return result.get("embedding", [])
    except Exception as e:
        logger.error(f"❌ Embedding generation failed: {e}")
        # Return dummy embedding to prevent crash
        return [0.0] * 384

def search_knowledge_base(question: str, collection_name: str = "math_kb", min_score: float = 0.5) -> dict:
    """
    Search the knowledge base for relevant math content.
    Returns dict with answer, steps, solution, confidence or None if not found.
    """
    # Check if collection exists
    if not check_collection_exists(collection_name):
        logger.warning(f"⚠️ Collection '{collection_name}' does not exist. Skipping KB search.")
        return None
    
    try:
        # Generate embedding
        embedding = generate_embedding(question)
        
        # Search Qdrant
        hits = client.search(
            collection_name=collection_name,
            query_vector=embedding,
            limit=3,  # Get top 3 results
            score_threshold=min_score,
            search_params=SearchParams(hnsw_ef=128)
        )
        
        if not hits or len(hits) == 0:
            logger.info(f"📭 No results found for question: {question[:50]}...")
            return None
        
        # Get top hit
        top_hit = hits[0]
        
        # Parse steps (handle both string and list formats)
        steps = top_hit.payload.get("steps", [])
        if isinstance(steps, str):
            steps = [s.strip() for s in steps.split("\n") if s.strip()]
        
        result = {
            "answer": top_hit.payload.get("answer", ""),
            "steps": steps,
            "solution": top_hit.payload.get("solution", ""),
            "confidence": float(top_hit.score),
            "topic": top_hit.payload.get("topic", "General"),
            "difficulty": top_hit.payload.get("difficulty", "Unknown")
        }
        
        logger.info(f"✅ Found KB result with confidence {result['confidence']:.2f}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Qdrant search failed: {e}")
        return None
