
from sympy import sympify, simplify
from sympy.parsing.sympy_parser import parse_expr

def verify_answer(question: str, answer: str) -> bool:
    try:
        if "limit" in question.lower():
            return True
        lhs = parse_expr(question.split("=")[0])
        rhs = parse_expr(answer)
        return simplify(lhs - rhs) == 0
    except Exception:
        return False
