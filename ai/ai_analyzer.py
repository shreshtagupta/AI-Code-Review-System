import os
import json
from google import genai
from dotenv import load_dotenv

from ai.my_ai_features import (
    syntax_analysis,
    correct_code,
    improve_code,
    security_analysis,
    compare_code
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

MODEL = "gemini-flash-lite-latest"


def analyze_code(code, filename):

    prompt = f"""
You are CodeGuard AI, an expert programming code reviewer.

Analyze the submitted code carefully.

Return ONLY valid JSON with these exact fields:

{{
    "status": "Completed",
    "detected_language": "Programming language name",
    "syntax_analysis": {{
        "status": "Passed or Failed",
        "errors": []
    }},
    "bugs": [],
    "logical_errors": [],
    "security_issues": [],
    "code_explanation": "Simple explanation of the code",
    "suggestions": [],
    "corrected_code": null
}}

IMPORTANT RULES:

1. Detect the actual programming language.
2. Check syntax carefully.
3. Do not report indentation errors when indentation is correct.
4. Identify actual logical bugs.
5. Do not confuse code quality suggestions with actual bugs.
6. Identify genuine security vulnerabilities only.
7. Do not invent errors or vulnerabilities.
8. If there are no syntax errors, return an empty errors list.
9. If there are no bugs, return an empty bugs list.
10. Explain findings in simple English.
11. Do not execute the submitted code.
12. If the code is already correct, corrected_code must be null.
13. If a correction is needed, provide the complete corrected code.
14. Make sure the corrected code matches the intended function of the original code.
15. Do not assume a function name alone proves its intended behavior.

Filename: {filename}

Code:
{code}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    response_text = response.text.strip()

    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "").strip()

    result = json.loads(response_text)

    language = result.get("detected_language", "Unknown")

    # Syntax Analysis
    syntax_result = syntax_analysis(
        code, language, client, MODEL
    )

    if isinstance(syntax_result, dict):
        result["syntax_analysis"] = syntax_result
    else:
        result["syntax_analysis"] = {
            "status": "Completed",
            "errors": syntax_result if isinstance(syntax_result, list)
            else [str(syntax_result)]
        }

    # Corrected Code
    if result.get("bugs") or result.get("logical_errors") or result["syntax_analysis"].get("errors"):
        corrected = correct_code(
            code, language, client, MODEL
        )

        result["corrected_code"] = corrected

    else:
        result["corrected_code"] = None

    # Code Improvement Suggestions
    suggestions = improve_code(
        code, language, client, MODEL
    )

    if suggestions:
        if isinstance(suggestions, list):
            result["suggestions"] = suggestions
        else:
            result["suggestions"] = [suggestions]

    # Security Analysis
    security_result = security_analysis(
        code, language, client, MODEL
    )

    if isinstance(security_result, list):
        result["security_issues"] = security_result
    elif isinstance(security_result, dict):
        result["security_issues"] = security_result.get(
            "findings", [security_result]
        )
    else:
        result["security_issues"] = [security_result] if security_result else []

    return result