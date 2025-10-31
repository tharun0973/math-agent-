import re
from sympy import sympify, solve, diff, integrate, Symbol

MATH_KEYWORDS = [
    'solve', 'equation', 'expression', 'function', 'derivative',
    'differentiate', 'integral', 'integrate', 'limit', 'matrix', 'vector',
    'polynomial', 'quadratic', 'linear', 'graph', 'plot', 'calculate',
    'compute', 'evaluate', 'simplify', 'expand', 'factor', 'trigonometry',
    'algebra', 'calculus', 'geometry', 'probability', 'statistics',
    'logarithm', 'exponential', 'series', 'sequence', 'theorem',
    'laplace', 'fourier', 'differential'
]

BANNED_TOPICS = [
    'kill', 'murder', 'violence', 'harm', 'weapon', 'drug', 'illegal',
    'political', 'election', 'religion', 'religious', 'race', 'gender',
    'sex', 'porn', 'adult'
]

HALLUCINATION_MARKERS = [
    "I'm not sure", "I don't know", "I cannot", "I'm not able", "I don't have",
    "I apologize", "Sorry, I", "I'm sorry", "I'm unable", "I cannot help",
    "I'm not capable", "I don't understand"
]

def validate_input(question: str) -> bool:
    if not question or len(question.strip()) < 2:
        return False
    q = question.lower()
    if any(b in q for b in BANNED_TOPICS):
        return False
    has_keyword = any(re.search(rf'\b{re.escape(k)}\b', q) for k in MATH_KEYWORDS)
    has_symbols = bool(re.search(r'[\d\+\-\*/=xyzπ√∑∫∞^()sintcostanlogexp]', q))
    is_simple_expr = bool(re.match(r'^[\dxyz\+\-\*/\^=\s\(\)]+$', question.strip()))
    return has_keyword or has_symbols or is_simple_expr

def rejection_message() -> str:
    return (
        "❌ This system only handles **mathematics-related** questions. "
        "Please ask a valid math problem such as an equation, derivative, "
        "integral, or Laplace transform."
    )

def sanitize_output(answer: str) -> str:
    if not answer:
        return ""
    sanitized = answer
    for marker in HALLUCINATION_MARKERS:
        sanitized = re.sub(re.escape(marker), '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    return sanitized

def solver(question: str):
    if not validate_input(question):
        return rejection_message()
    try:
        q = question.lower().strip()
        x = Symbol('x')

        if 'integrate' in q:
            expr = sympify(q.replace('integrate', '').strip())
            result = integrate(expr, x)
            return f"✅ ∫ {expr} dx = {result}"

        elif 'derivative' in q or 'differentiate' in q:
            expr = sympify(q.replace('derivative', '').replace('differentiate', '').strip())
            result = diff(expr, x)
            return f"✅ d/dx({expr}) = {result}"

        elif 'solve' in q:
            expr = sympify(q.replace('solve', '').strip())
            result = solve(expr)
            return f"✅ Solution: {result}"

        else:
            expr = sympify(question)
            result = solve(expr)
            if result:
                return f"✅ Solution: {result}"
            else:
                return rejection_message()

    except Exception:
        return rejection_message()
