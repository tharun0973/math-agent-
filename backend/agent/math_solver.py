import logging, re
from sympy import symbols, Eq, solve, integrate, diff, simplify, sympify, latex
from sympy.parsing.sympy_parser import parse_expr

logger = logging.getLogger(__name__)

class MathSolver:
    def __init__(self):
        self.x, self.y, self.z = symbols("x y z")

    def normalize_equation(self, expr: str) -> str:
        expr = expr.replace("^", "**")
        repl = {
            "²": "**2", "³": "**3", "⁴": "**4", "⁵": "**5",
            "⁶": "**6", "⁷": "**7", "⁸": "**8", "⁹": "**9"
        }
        for k, v in repl.items():
            expr = expr.replace(k, v)
        expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
        expr = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', expr)
        return expr

    def solve_equation(self, question: str) -> dict:
        try:
            q = self.normalize_equation(question)
            q = q.replace("?", "").strip()
            q = re.sub(r"(?i)solve", "", q).strip()

            math_keywords = ["+", "-", "*", "/", "=", "^", "**", "∫", "lim", "∑", "dx", "dy"]
            if not any(kw in q for kw in math_keywords):
                return {
                    "answer": (
                        "❌ This assistant only handles mathematics-related questions.\n\n"
                        "Please ask a valid math problem such as an equation, derivative, or integral."
                    ),
                    "solution": "",
                    "confidence": 0.0
                }

            # ✅ Handle integration
            if re.search(r"(?i)integrate|∫", q):
                expr = re.sub(r"(?i)integrate|∫", "", q).strip()
                sym_expr = sympify(expr)
                result = integrate(sym_expr, self.x)
                latex_expr = latex(sym_expr)
                latex_result = latex(result)

                answer = (
                    f"Problem: Integrate {expr}\n\n"
                    f"Step 1: Parsed expression: ${latex_expr}$\n\n"
                    f"Step 2: Apply integration rule\n\n"
                    f"Final Answer: $\\int {latex_expr}\\,dx = {latex_result} + C$"
                )
                return {"answer": answer, "solution": latex_result, "confidence": 1.0}

            # ✅ Handle differentiation
            if re.search(r"(?i)d/dx|differentiate", q):
                expr = re.sub(r"(?i)d/dx|differentiate", "", q).strip()
                sym_expr = sympify(expr)
                result = diff(sym_expr, self.x)
                latex_expr = latex(sym_expr)
                latex_result = latex(result)

                answer = (
                    f"Problem: Differentiate {expr}\n\n"
                    f"Step 1: Parsed expression: ${latex_expr}$\n\n"
                    f"Step 2: Apply derivative rule\n\n"
                    f"Final Answer: $\\frac{{d}}{{dx}}({latex_expr}) = {latex_result}$"
                )
                return {"answer": answer, "solution": latex_result, "confidence": 1.0}

            # ✅ Handle equation solving
            if "==" not in q and "=" in q:
                q = q.replace("=", "==")

            if "==" in q:
                lhs, rhs = q.split("==")
                lhs_expr = parse_expr(lhs.strip(), evaluate=False)
                rhs_expr = parse_expr(rhs.strip(), evaluate=False)
                eq = Eq(lhs_expr, rhs_expr)
            else:
                expr = parse_expr(q.strip(), evaluate=False)
                eq = Eq(expr, 0)

            result = solve(eq)
            latex_eq = latex(eq)

            if result:
                latex_results = [latex(simplify(r)) for r in result]
                latex_final = ", ".join(latex_results)

                answer = (
                    f"Problem: Solve ${latex_eq}$\n\n"
                    f"Step 1: Equation parsed as ${latex_eq}$\n\n"
                    f"Step 2: Apply solving rule\n\n"
                    f"Final Answer: $x = {latex_final}$"
                )
                return {"answer": answer, "solution": latex_final, "confidence": 1.0}

            return {
                "answer": (
                    "I couldn't solve this mathematical problem.\n\n"
                    "Step 1: No suitable solver or formula found for this input."
                ),
                "solution": "",
                "confidence": 0.0,
            }

        except Exception as e:
            logger.error(f"SymPy error: {e}")
            return {
                "answer": (
                    f"⚠️ I couldn't solve this mathematical problem.\n"
                    f"Error: {e}\n\n"
                    "Step 1: SymPy parsing or solving failed."
                ),
                "solution": "",
                "confidence": 0.0,
            }
