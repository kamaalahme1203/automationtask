import subprocess
import json
import tempfile
import re

def extract_pylint_score(output):
    """Extract pylint score from output"""
    match = re.search(r"Your code has been rated at ([\-0-9.]+)/10", output)
    return float(match.group(1)) if match else 5.0  # Default to 5 if not found

def extract_flake8_issues(output):
    """Counts number of issues in flake8 output"""
    return len(output.split("\n")) if output.strip() else 0

def extract_radon_complexity(output):
    """Extracts average complexity from radon output"""
    match = re.search(r"Average complexity: (\d+(\.\d+)?)", output)
    return float(match.group(1)) if match else 10.0  # Default to 10

def analyze_python(code):
    """Analyzes Python code using pylint, flake8, and radon"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(code)
        temp_file.close()

        pylint_output = subprocess.getoutput(f"pylint {temp_file.name} --disable=all --enable=convention,refactor,warning,error")
        radon_output = subprocess.getoutput(f"radon cc {temp_file.name} -a")
        flake8_output = subprocess.getoutput(f"flake8 {temp_file.name} --statistics")

    # Extract values
    pylint_score = extract_pylint_score(pylint_output) * 10  # Convert to percentage
    radon_score = extract_radon_complexity(radon_output)
    flake8_issues = extract_flake8_issues(flake8_output)

    # Individual category scores (scaled to the total of 100)
    naming_score = max(10 - flake8_issues, 0)
    modularity_score = max(20 - radon_score * 2, 0)
    comments_score = max(20 - pylint_score * 0.5, 0)
    formatting_score = max(15 - flake8_issues * 1.5, 0)
    reusability_score = max(15 - radon_score, 0)
    best_practices_score = max(20 - pylint_score * 0.3, 0)

    # Overall Score Calculation
    overall_score = (
        naming_score + modularity_score + comments_score +
        formatting_score + reusability_score + best_practices_score
    )

    return {
        "overall_score": round(overall_score, 2),
        "breakdown": {
            "naming": round(naming_score, 2),
            "modularity": round(modularity_score, 2),
            "comments": round(comments_score, 2),
            "formatting": round(formatting_score, 2),
            "reusability": round(reusability_score, 2),
            "best_practices": round(best_practices_score, 2),
        },
        "recommendations": [
            "Refactor complex functions.",
            "Improve naming conventions.",
            "Reduce code duplication."
        ]
    }

def analyze_js(code):
    """Analyzes JavaScript code using ESLint"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".js") as temp_file:
        temp_file.write(code)
        temp_file.close()

        eslint_output = subprocess.getoutput(f"eslint {temp_file.name} --format json")
        
        # Debugging: Print ESLint output to terminal
        print(f"ESLint Output: {eslint_output}")

        try:
            eslint_data = json.loads(eslint_output)
            warnings = sum(len(file["messages"]) for file in eslint_data)  # Count warnings
        except (json.JSONDecodeError, KeyError, TypeError):
            warnings = 5  # Default warning count if ESLint output is invalid

    # Individual category scores (scaled to 100)
    naming_score = max(10 - warnings * 0.5, 0)
    modularity_score = max(20 - warnings * 1.5, 0)
    comments_score = max(20 - warnings, 0)
    formatting_score = max(15 - warnings * 0.8, 0)
    reusability_score = max(15 - warnings * 0.7, 0)
    best_practices_score = max(20 - warnings * 1.2, 0)

    # Overall Score Calculation
    overall_score = (
        naming_score + modularity_score + comments_score +
        formatting_score + reusability_score + best_practices_score
    )

    return {
        "overall_score": round(overall_score, 2),
        "breakdown": {
            "naming": round(naming_score, 2),
            "modularity": round(modularity_score, 2),
            "comments": round(comments_score, 2),
            "formatting": round(formatting_score, 2),
            "reusability": round(reusability_score, 2),
            "best_practices": round(best_practices_score, 2),
        },
        "recommendations": [
            "Use camelCase for variables.",
            "Avoid deeply nested loops.",
            "Ensure proper indentation."
        ]
    }
