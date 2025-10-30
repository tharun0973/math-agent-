from agent.knowledge_base import search_knowledge_base
from agent.web_search import search_web_and_generate, query_ollama_direct
from agent.guardrails import validate_input, sanitize_output
from agent.math_solver import MathSolver
from agent.verifier import verify_answer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize solver
solver = MathSolver()

def route_question(question: str) -> dict:
    """
    Intelligent routing system:
    1. Validate input with guardrails
    2. Try Knowledge Base (Qdrant)
    3. Try Web Search + MCP (Tavily + Ollama)
    4. Try Direct MCP (Ollama only)
    5. Fallback to SymPy solver
    """
    # Step 1: Input validation
    if not validate_input(question):
        logger.warning(f"❌ Invalid input rejected: {question[:50]}...")
        return {
            "answer": "Invalid input. Please ask a math-related question.",
            "steps": ["Input validation failed."],
            "solution": "",
            "confidence": 0.0
        }

    logger.info(f"📝 Routing question: {question[:50]}...")

    # Step 2: Try Knowledge Base first
    logger.info("🔍 Step 1: Searching Knowledge Base...")
    kb_result = search_knowledge_base(question)
    if kb_result and kb_result.get("confidence", 0) > 0.5:
        logger.info(f"✅ KB result found with confidence {kb_result.get('confidence', 0):.2f}")
        return {
            "answer": sanitize_output(kb_result.get("answer", "")),
            "steps": kb_result.get("steps", []),
            "solution": kb_result.get("solution", ""),
            "confidence": float(kb_result.get("confidence", 0.95)),
            "source": "knowledge_base"
        }

    # Step 3: Try Web Search + MCP
    logger.info("🌐 Step 2: Trying Web Search...")
    web_result = search_web_and_generate(question)
    if web_result:
        logger.info("✅ Web search result found")
        return {
            "answer": sanitize_output(web_result.get("answer", "")),
            "steps": web_result.get("steps", []),
            "solution": web_result.get("solution", ""),
            "confidence": float(web_result.get("confidence", 0.85)),
            "source": "web_search"
        }

    # Step 4: Try Direct MCP (Ollama)
    logger.info("🤖 Step 3: Trying Direct MCP...")
    ollama_result = query_ollama_direct(question)
    if ollama_result:
        # Verify answer if possible
        verified = verify_answer(question, ollama_result.get("answer", ""))
        logger.info(f"✅ MCP result found (verified: {verified})")
        return {
            "answer": sanitize_output(ollama_result.get("answer", "")),
            "steps": ollama_result.get("steps", []),
            "solution": ollama_result.get("solution", ""),
            "confidence": 0.9 if verified else 0.75,
            "source": "ollama_mcp"
        }

    # Step 5: Fallback to SymPy solver
    logger.info("🧮 Step 4: Trying SymPy solver...")
    try:
        sympy_result = solver.solve_equation(question)
        if sympy_result and sympy_result.get("confidence", 0) > 0:
            logger.info("✅ SymPy result found")
            return {
                "answer": sanitize_output(sympy_result.get("answer", "")),
                "steps": sympy_result.get("steps", []),
                "solution": sympy_result.get("solution", ""),
                "confidence": float(sympy_result.get("confidence", 0.7)),
                "source": "sympy"
            }
    except Exception as e:
        logger.error(f"❌ SymPy solver failed: {e}")

    # Final fallback
    logger.error("❌ All routing methods failed")
    return {
        "answer": "I couldn't find a solution. Please try rephrasing your question or provide more context.",
        "steps": ["No suitable method found to solve this question."],
        "solution": "",
        "confidence": 0.0,
        "source": "none"
    }
