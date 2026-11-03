import os
import json
from google import genai
from dotenv import load_dotenv
from ai.my_ai_features import syntax_analysis, correct_code, improve_code, security_analysis, compare_code

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def analyze_code(code, filename):

    prompt = f"""
You are CodeGuard AI, an expert code reviewer.

Review the following programming code.

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
    "code_explanation": "Explain the code simply",
    "suggestions": [],
    "corrected_code": null
}}

Rules:
- Find actual errors only.
- Explain errors in simple English.
- Do not invent errors.
- If no issues exist, return empty lists.
- If corrected code is not needed, use null.
- Do not execute the submitted code.

Filename: {filename}

Code:
{code}
"""

    response = client.models.generate_content(
        model="invalid-model-for-test",
        contents=prompt
    )

    result = json.loads(response.text)

    language = result["detected_language"]

    result["syntax_analysis"] = {
        "status": "Completed",
        "errors": syntax_analysis(code, language, client, "gemini-flash-lite-latest")
    }

    result["corrected_code"] = correct_code(code, language, client, "gemini-flash-lite-latest")

    result["suggestions"] = [
        improve_code(code, language, client, "gemini-flash-lite-latest")
    ]

    result["security_issues"] = [
    security_analysis(code, language, client, "gemini-flash-lite-latest")
]

    return result