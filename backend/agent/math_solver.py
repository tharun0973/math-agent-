from sympy import symbols, Eq, solve, simplify, expand, factor, diff, integrate, limit, sin, cos, tan, log, exp
from sympy.parsing.sympy_parser import parse_expr
import re

class MathSolver:
    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')

    def solve_equation(self, question: str):
        """Enhanced solver that handles multiple math problem types"""
        try:
            # Clean question
            question_clean = question.strip()
            
            # Detect problem type
            if any(op in question_clean.lower() for op in ['derivative', 'differentiate', "d/dx"]):
                return self._solve_derivative(question_clean)
            elif any(op in question_clean.lower() for op in ['integrate', 'integral', '∫']):
                return self._solve_integral(question_clean)
            elif 'limit' in question_clean.lower():
                return self._solve_limit(question_clean)
            elif '=' in question_clean:
                return self._solve_equation(question_clean)
            elif any(op in question_clean for op in ['+', '-', '*', '/']):
                return self._evaluate_expression(question_clean)
            else:
                return {
                    "answer": "Could not identify problem type",
                    "steps": ["Unsupported operation"],
                    "solution": "",
                    "confidence": 0.0
                }
        except Exception as e:
            return {
                "answer": "Error solving problem",
                "steps": [f"Error: {str(e)}"],
                "solution": "",
                "confidence": 0.0
            }

    def _solve_equation(self, question: str):
        """Solve algebraic equations"""
        try:
            # Extract equation parts
            if '=' not in question:
                return None
            
            left, right = question.split('=', 1)
            left_expr = parse_expr(left.strip().replace('^', '**'))
            right_expr = parse_expr(right.strip().replace('^', '**'))
            eq = Eq(left_expr, right_expr)
            
            # Solve
            solutions = solve(eq, self.x)
            
            steps = [
                f"Given equation: {left.strip()} = {right.strip()}",
                f"Rearranged: {eq}",
                f"Solution(s): x = {', '.join([str(s) for s in solutions])}"
            ]
            
            solution_str = f"x = {', '.join([str(s) for s in solutions])}"
            
            return {
                "answer": solution_str,
                "steps": steps,
                "solution": solution_str,
                "confidence": 0.85
            }
        except Exception as e:
            raise Exception(f"Equation solving error: {e}")

    def _solve_derivative(self, question: str):
        """Solve derivatives"""
        try:
            # Extract expression
            expr_str = re.sub(r'(derivative|differentiate|d/dx|of)', '', question, flags=re.I)
            expr_str = expr_str.replace('^', '**').strip()
            
            # Remove common prefixes
            for prefix in ['find the', 'solve', 'compute', 'calculate', 'what is']:
                if expr_str.lower().startswith(prefix):
                    expr_str = expr_str[len(prefix):].strip()
            
            expr = parse_expr(expr_str)
            deriv = diff(expr, self.x)
            
            steps = [
                f"Function: f(x) = {expr}",
                f"Derivative: f'(x) = {deriv}"
            ]
            
            return {
                "answer": f"f'(x) = {deriv}",
                "steps": steps,
                "solution": str(deriv),
                "confidence": 0.8
            }
        except Exception as e:
            raise Exception(f"Derivative error: {e}")

    def _solve_integral(self, question: str):
        """Solve integrals"""
        try:
            # Extract expression
            expr_str = re.sub(r'(integral|integrate|∫)', '', question, flags=re.I)
            expr_str = expr_str.replace('^', '**').strip()
            
            # Remove common prefixes
            for prefix in ['find the', 'solve', 'compute', 'calculate', 'of']:
                if expr_str.lower().startswith(prefix):
                    expr_str = expr_str[len(prefix):].strip()
            
            expr = parse_expr(expr_str)
            integral = integrate(expr, self.x)
            
            steps = [
                f"Integral: ∫{expr} dx",
                f"Solution: {integral} + C"
            ]
            
            return {
                "answer": f"∫{expr} dx = {integral} + C",
                "steps": steps,
                "solution": str(integral),
                "confidence": 0.8
            }
        except Exception as e:
            raise Exception(f"Integral error: {e}")

    def _solve_limit(self, question: str):
        """Solve limits"""
        try:
            # Extract expression and limit point
            match = re.search(r'limit.*?\bas\s+(?:x|n)\s*→\s*(\S+)', question, re.I)
            if not match:
                return None
            
            limit_point = parse_expr(match.group(1))
            expr_str = re.sub(r'limit.*?\bas.*', '', question, flags=re.I).strip()
            expr_str = expr_str.replace('^', '**')
            
            expr = parse_expr(expr_str)
            lim = limit(expr, self.x, limit_point)
            
            steps = [
                f"Limit: lim(x→{limit_point}) {expr}",
                f"Solution: {lim}"
            ]
            
            return {
                "answer": str(lim),
                "steps": steps,
                "solution": str(lim),
                "confidence": 0.75
            }
        except Exception as e:
            raise Exception(f"Limit error: {e}")

    def _evaluate_expression(self, question: str):
        """Evaluate simple expressions"""
        try:
            expr_str = question.replace('^', '**').strip()
            expr = parse_expr(expr_str)
            result = expr.evalf()
            
            steps = [
                f"Expression: {question}",
                f"Result: {result}"
            ]
            
            return {
                "answer": str(result),
                "steps": steps,
                "solution": str(result),
                "confidence": 0.9
            }
        except Exception as e:
            raise Exception(f"Evaluation error: {e}")
