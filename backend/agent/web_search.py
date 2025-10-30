import os
import requests
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Tavily client (optional)
try:
    from tavily import TavilyClient
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    logger.info("✅ Tavily client initialized")
except Exception as e:
    logger.warning(f"⚠️ Tavily not available: {e}")
    client = None

def query_ollama_mcp(question: str, context: str = "") -> dict:
    """Query Ollama model for math solution"""
    prompt = f"""You are a math tutor. Answer the following question with a step-by-step solution.
Question: {question}
Context: {context}
Instructions: Use clear steps, simplify for a student. Show all work."""
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma:2b", "prompt": prompt, "stream": False},
            timeout=60
        )
        result = response.json()
        answer_text = result.get("response", "").strip()

        # Parse steps from answer
        steps = answer_text.split("\n")
        steps = [s.strip() for s in steps if s.strip()]

        return {
            "answer": answer_text,
            "steps": steps,
            "solution": answer_text.split(".")[0] if answer_text else "",
            "confidence": 0.85
        }
    except Exception as e:
        logger.error(f"❌ Ollama MCP failed: {e}")
        return None

def package_mcp_context(question: str, retrieved_docs: list) -> str:
    """Package context from retrieved documents for MCP"""
    system_instructions = (
        "You are a math tutor. Produce a step-by-step solution simplified for a high-school student. "
        "Cite sources. If content is not confirmed or insufficient, return 'INSUFFICIENT_EXTERNAL_EVIDENCE'."
    )
    context_chunks = [
        f"Source: {doc['source']}\nContent: {doc['text']}\n"
        for doc in retrieved_docs
    ]
    context = "\n---\n".join(context_chunks)
    prompt = f"""
System Instructions:
{system_instructions}

User Question:
{question}

Retrieved Context:
{context}
"""
    return prompt.strip()

def search_web_and_generate(question: str) -> dict:
    """
    Search web using Tavily and generate response using Ollama MCP.
    Returns None if search fails.
    """
    if not client:
        logger.warning("⚠️ Tavily not configured, skipping web search")
        return None
    
    try:
        logger.info(f"🌐 Searching web for: {question[:50]}...")
        results = client.search(query=question, max_results=5)
        
        if not results or len(results) == 0:
            logger.warning("⚠️ No web search results found")
            return None
        
        # Extract relevant docs
        docs = [{"source": r["url"], "text": r["content"]} for r in results]
        logger.info(f"✅ Retrieved {len(docs)} web results")
        
        # Package context and query MCP
        prompt = package_mcp_context(question, docs)
        result = query_ollama_mcp(question, prompt)
        
        if result:
            logger.info(f"✅ Generated answer from web search")
        else:
            logger.warning("⚠️ Failed to generate answer from web search")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Web search failed: {e}")
        return None

def query_ollama_direct(question: str) -> dict:
    """
    Query Ollama directly without web search (pure MCP fallback).
    """
    logger.info(f"🤖 Querying Ollama directly: {question[:50]}...")
    return query_ollama_mcp(question, "")
