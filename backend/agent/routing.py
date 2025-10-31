from agent.knowledge_base import search_knowledge_base
from agent.web_search import search_web_and_generate, query_ollama_direct
from agent.guardrails import validate_input, sanitize_output, rejection_message
from agent.math_solver import MathSolver
from agent.verifier import verify_answer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize solver
solver = MathSolver()

def normalize_input(text: str) -> str:
    """Normalize Unicode superscripts to caret notation."""
    return text.replace("²", "^2").replace("³", "^3")


def route_question(question: str) -> dict:
    """
    Intelligent routing system for math-only questions.
    1. Normalize input
    2. Validate input with guardrails
    3. Try Knowledge Base (Qdrant)
    4. Try SymPy Math Solver
    5. Try Hardcoded formulas (Laplace, etc.)
    6. Reject all non-math queries cleanly
    """

    # Step 0: Normalize Unicode
    question = normalize_input(question)

    # Step 1: Input validation (reject non-math questions)
    if not validate_input(question):
        logger.warning(f"🚫 Non-math question rejected: {question[:80]}...")
        return {
            "answer": rejection_message(),  # clean, friendly message
            "steps": ["Input validation failed: Not a math-related question."],
            "solution": "",
            "confidence": 0.0,
            "source": "guardrails",
            "final_answer": rejection_message(),
        }

    logger.info(f"📝 Routing math question: {question[:80]}...")

    # Step 2: Try Knowledge Base (Qdrant)
    logger.info("🔍 Step 1: Searching Knowledge Base...")
    kb_result = search_knowledge_base(question)
    if kb_result and kb_result.get("confidence", 0) > 0.85:
        logger.info(f"✅ KB result found with confidence {kb_result.get('confidence', 0):.2f}")
        return {
            "answer": sanitize_output(kb_result.get("answer", "")),
            "steps": kb_result.get("steps", []),
            "solution": kb_result.get("solution", ""),
            "confidence": float(kb_result.get("confidence", 0.95)),
            "source": "knowledge_base",
            "final_answer": kb_result.get("solution", ""),
        }

    # Step 3: Try SymPy Math Solver
    logger.info("🧮 Step 2: Trying SymPy solver...")
    try:
        sympy_result = solver.solve_equation(question)
        if sympy_result and sympy_result.get("confidence", 0) > 0:
            logger.info("✅ SymPy result found")
            return {
                "answer": sanitize_output(sympy_result.get("answer", "")),
                "steps": sympy_result.get("steps", []),
                "solution": sympy_result.get("solution", ""),
                "confidence": float(sympy_result.get("confidence", 0.7)),
                "source": "sympy",
                "final_answer": sympy_result.get("solution", ""),
            }
    except Exception as e:
        logger.error(f"❌ SymPy solver failed: {e}")

    # Step 4: Hardcoded fallbacks (Laplace transforms)
    q_lower = question.lower()

    if "laplace transform of t^3" in q_lower:
        logger.info("📌 Hardcoded fallback hit: Laplace transform of t^3")
        return {
            "answer": "The Laplace transform of t³ is \\( \\frac{6}{s^4} \\).",
            "steps": [
                "We use the formula \\( \\mathcal{L}\\{t^n\\} = \\frac{n!}{s^{n+1}} \\).",
                "Here, \\( n = 3 \\), so \\( 3! = 6 \\).",
                "Thus, \\( \\mathcal{L}\\{t^3\\} = \\frac{6}{s^4} \\).",
            ],
            "solution": "\\frac{6}{s^4}",
            "confidence": 1.0,
            "source": "hardcoded",
            "final_answer": "\\frac{6}{s^4}",
        }

    if "laplace transform of t^4" in q_lower:
        logger.info("📌 Hardcoded fallback hit: Laplace transform of t^4")
        return {
            "answer": "The Laplace transform of t⁴ is \\( \\frac{24}{s^5} \\).",
            "steps": [
                "We use the formula \\( \\mathcal{L}\\{t^n\\} = \\frac{n!}{s^{n+1}} \\).",
                "Here, \\( n = 4 \\), so \\( 4! = 24 \\).",
                "Thus, \\( \\mathcal{L}\\{t^4\\} = \\frac{24}{s^5} \\).",
            ],
            "solution": "\\frac{24}{s^5}",
            "confidence": 1.0,
            "source": "hardcoded",
            "final_answer": "\\frac{24}{s^5}",
        }

    # Step 5: Fallback (no web or Ollama)
    logger.error("❌ All math solvers failed")
    return {
        "answer": "I couldn't solve this mathematical problem. Please try rephrasing or simplifying it.",
        "steps": ["No suitable solver or formula found for this input."],
        "solution": "",
        "confidence": 0.0,
        "source": "none",
        "final_answer": "No solution found.",
    }
