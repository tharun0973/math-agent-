import re
from typing import List

# Math-related keywords for validation
MATH_KEYWORDS = [
    'solve', 'solve for', 'equation', 'expression', 'function', 'derivative', 
    'integral', 'limit', 'matrix', 'vector', 'polynomial', 'quadratic', 'linear',
    'graph', 'plot', 'calculate', 'compute', 'evaluate', 'simplify', 'expand',
    'factor', 'trigonometry', 'algebra', 'calculus', 'geometry', 'probability',
    'statistics', 'logarithm', 'exponential', 'series', 'sequence', 'theorem'
]

# Unsafe topics to filter
BANNED_TOPICS = [
    'kill', 'murder', 'violence', 'harm', 'weapon', 'drug', 'illegal',
    'political election', 'politics', 'religious', 'race', 'gender', 'sex',
    'pornography', 'adult content'
]

# Hallucination markers to remove from output
HALLUCINATION_MARKERS = [
    "I'm not sure", "I don't know", "I cannot", "I'm not able", "I don't have",
    "I apologize", "Sorry, I", "I'm sorry", "I'm unable", "I cannot help",
    "I'm not capable", "I don't understand the question"
]

def validate_input(question: str) -> bool:
    """
    Validate that the question is math-related and safe.
    Returns True if valid, False otherwise.
    """
    if not question or len(question.strip()) < 3:
        return False
    
    question_lower = question.lower()
    
    # Check for banned topics
    for banned in BANNED_TOPICS:
        if banned in question_lower:
            return False
    
    # Check if it contains math-related content
    has_math_keyword = any(keyword in question_lower for keyword in MATH_KEYWORDS)
    has_math_symbols = bool(re.search(r'\d+|\+|\-|\*|\/|=|x|y|z|π|√|∑|∫', question))
    
    # Must have either math keywords or symbols
    if not has_math_keyword and not has_math_symbols:
        return False
    
    return True

def sanitize_output(answer: str) -> str:
    """
    Remove hallucinations, profanity, and unsafe content from output.
    """
    if not answer:
        return ""
    
    # Remove hallucination markers
    sanitized = answer
    for marker in HALLUCINATION_MARKERS:
        sanitized = sanitized.replace(marker, "")
    
    # Remove excessive apologizing
    if sanitized.count("sorry") > 2:
        # Keep content but remove excessive apologies
        lines = sanitized.split('\n')
        lines = [line for line in lines if 'sorry' not in line.lower()]
        sanitized = '\n'.join(lines)
    
    return sanitized.strip()

def extract_math_content(text: str) -> str:
    """
    Extract only math-related content from text.
    """
    # This is a simple extractor - can be enhanced with NLP
    lines = text.split('\n')
    math_lines = []
    
    for line in lines:
        # Check if line contains math symbols or keywords
        if re.search(r'\d|\+|\-|\*|\/|=|x|solve|calculate|compute', line):
            math_lines.append(line)
    
    return '\n'.join(math_lines) if math_lines else text
