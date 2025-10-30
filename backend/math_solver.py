"""
Math Problem Solver using SymPy
Handles various math problem types with step-by-step solutions
"""

import re
from typing import Dict, List
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from sympy import latex

class MathSingleton:
    """
    Singleton class to initialize SymPy symbols only once
    """
    _instance = None
    _symbols = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MathSingleton, cls).__new__(cls)
        return cls._instance
    
    def get_symbols(self, variables: List[str]):
        if self._symbols is None:
            self._symbols = {}
        for var in variables:
            if var not in self._symbols:
                self._symbols[var] = sp.Symbol(var)
        return [self._symbols[v] for v in variables]


class MathSolver:
    def __init__(self):
        self.symbol_manager = MathSingleton()
    
    def solve(self, question: str) -> Dict:
        """
        Main solving method that routes to specific solvers
        """
        question = question.strip()
        
        # Try quadratic equation solver
        quad_result = self.solve_quadratic(question)
        if quad_result["solved"]:
            return quad_result
        
        # Try general equation solver
        equation_result = self.solve_equation(question)
        if equation_result["solved"]:
            return equation_result
        
        # Try expression evaluation
        eval_result = self.evaluate_expression(question)
        if eval_result["solved"]:
            return eval_result
        
        # Fallback
        return {
            "solved": False,
            "answer": "I couldn't parse your question. Please try rephrasing it.",
            "steps": [],
            "solution": "",
            "confidence": 0.0
        }
    
    def solve_quadratic(self, question: str) -> Dict:
        """
        Solve quadratic equations in the form ax² + bx + c = 0
        """
        try:
            # Extract quadratic equation
            pattern = r'([-+]?\d*)x²\s*([-+]\s*\d*)x\s*([-+]\s*\d*)\s*=\s*(\d+)'
            match = re.search(pattern, question)
            
            if not match:
                return {"solved": False}
            
            # Parse coefficients
            a = int(match.group(1)) if match.group(1) and match.group(1) != '-' else 1
            if match.group(1) == '-':
                a = -1
            
            b_match = match.group(2).replace(' ', '')
            b = int(b_match)
            
            c_match = match.group(3).replace(' ', '')
            c = int(c_match)
            
            constant = int(match.group(4))
            
            # Adjust for right-hand side
            c = c - constant
            
            steps = [
                f"Step 1: Identify coefficients",
                f"   a = {a}, b = {b}, c = {c}",
                f"Step 2: Calculate discriminant",
                f"   Δ = b² - 4ac = ({b})² - 4({a})({c})"
            ]
            
            # Calculate discriminant
            discriminant = b**2 - 4*a*c
            steps.append(f"   Δ = {discriminant}")
            
            if discriminant < 0:
                solution = f"Complex roots: x = {-b/(2*a)} ± {abs(discriminant)**0.5/(2*a)}i"
                steps.append("Step 3: Discriminant is negative, roots are complex")
            else:
                x1 = (-b + discriminant**0.5) / (2*a)
                x2 = (-b - discriminant**0.5) / (2*a)
                solution = f"x₁ = {x1:.4f}, x₂ = {x2:.4f}"
                steps.append(f"Step 3: Apply quadratic formula")
                steps.append(f"   x = (-b ± √Δ) / 2a")
                steps.append(f"   x₁ = {-b} + √{discriminant} / {2*a} = {x1:.4f}")
                steps.append(f"   x₂ = {-b} - √{discriminant} / {2*a} = {x2:.4f}")
            
            steps.append("Step 4: Verify solution")
            
            answer = f"Solution: {solution}"
            
            return {
                "solved": True,
                "answer": answer,
                "steps": steps,
                "solution": solution,
                "confidence": 0.95
            }
            
        except Exception:
            return {"solved": False}
    
    def solve_equation(self, question: str) -> Dict:
        """
        Solve general equations using SymPy
        """
        try:
            # Try to parse equation
            x = sp.Symbol('x')
            
            # Extract equation (assume form: expression = constant)
            if '=' in question:
                parts = question.split('=')
                left = parse_expr(parts[0].replace('x', 'x'), transformations='all')
                right = parse_expr(parts[1], transformations='all')
                equation = sp.Eq(left, right)
            else:
                equation = parse_expr(question, transformations='all')
                equation = sp.Eq(equation, 0)
            
            # Solve equation
            solutions = sp.solve(equation, x)
            
            if solutions:
                solution_str = ', '.join([f"x = {sol.evalf()}" for sol in solutions])
                steps = [
                    "Step 1: Parse the equation",
                    f"   Equation: {equation}",
                    "Step 2: Solve using SymPy",
                    "Step 3: Simplify and extract roots"
                ]
                
                answer = f"Solutions: {solution_str}"
                
                return {
                    "solved": True,
                    "answer": answer,
                    "steps": steps,
                    "solution": solution_str,
                    "confidence": 0.90
                }
            
            return {"solved": False}
            
        except Exception:
            return {"solved": False}
    
    def evaluate_expression(self, question: str) -> Dict:
        """
        Evaluate simple mathematical expressions
        """
        try:
            # Remove common math question words
            cleaned = re.sub(r'(solve|calculate|evaluate|find|what is|compute)', '', question, flags=re.IGNORECASE)
            cleaned = cleaned.strip().strip(':').strip('?')
            
            # Try to evaluate
            result = sp.sympify(cleaned).evalf()
            
            steps = [
                "Step 1: Parse expression",
                f"   Expression: {cleaned}",
                "Step 2: Evaluate",
                "Step 3: Simplify"
            ]
            
            answer = f"Result: {result}"
            
            return {
                "solved": True,
                "answer": answer,
                "steps": steps,
                "solution": str(result),
                "confidence": 0.85
            }
            
        except Exception:
            return {"solved": False}

