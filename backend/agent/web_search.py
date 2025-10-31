import os
import requests
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Tavily client
try:
    from tavily import TavilyClient
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    logger.info("✅ Tavily client initialized")
except Exception as e:
    logger.warning(f"⚠️ Tavily not available: {e}")
    client = None

def query_ollama_mcp(question: str, context: str = "") -> dict:
    """Query Ollama model for math solution with optional context"""
    prompt = f"""You are a math tutor. Answer the following question with a step-by-step solution.
Use Laplace transform identities only. For t^n, return n! / s^(n+1). Do not attempt symbolic integration unless explicitly asked.
Question: {question}
Context: {context}
Instructions: Use clear steps, simplify for a student. Show all work. If context is insufficient, return 'INSUFFICIENT_EXTERNAL_EVIDENCE'."""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma:2b", "prompt": prompt, "stream": False},
            timeout=60
        )
        result = response.json()
        answer_text = result.get("response", "").strip()

        if "INSUFFICIENT_EXTERNAL_EVIDENCE" in answer_text.upper():
            return {
                "answer": "No reliable external sources found.",
                "steps": ["Web search returned insufficient context."],
                "solution": "",
                "confidence": 0.0
            }

        steps = [s.strip() for s in answer_text.split("\n") if s.strip()]
        final_answer = steps[-1] if steps else answer_text.split(".")[0]

        return {
            "answer": answer_text,
            "steps": steps,
            "solution": final_answer,
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

        if not results or not isinstance(results, list):
            logger.warning("⚠️ No valid web search results found")
            return None

        try:
            docs = [{"source": r["url"], "text": r["content"]} for r in results if isinstance(r, dict)]
        except Exception as e:
            logger.error(f"❌ Failed to parse Tavily results: {e}")
            return None

        logger.info(f"✅ Retrieved {len(docs)} web results")

        prompt = package_mcp_context(question, docs)
        result = query_ollama_mcp(question, prompt)

        if result:
            logger.info("✅ Generated answer from web search")
        else:
            logger.warning("⚠️ Failed to generate answer from web search")

        return result

    except Exception as e:
        logger.error(f"❌ Web search failed: {e}")
        return None

def query_ollama_direct(question: str) -> dict:
    """Query Ollama directly without web search (pure MCP fallback)."""
    logger.info(f"🤖 Querying Ollama directly: {question[:50]}...")
    return query_ollama_mcp(question, "")
