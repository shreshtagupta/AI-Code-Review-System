
import ast
import difflib


def syntax_analysis(code, language, client=None, model=None):

    if language.lower() != "python":
        return {
            "status": "Not Checked",
            "errors": []
        }

    try:
        ast.parse(code)

        return {
            "status": "Passed",
            "errors": []
        }

    except SyntaxError as error:

        return {
            "status": "Failed",
            "errors": [error.msg],
            "line": error.lineno,
            "column": error.offset
        }


def create_syntax_prompt(code, language):

    prompt = f"""
You are an expert programming code reviewer.

Analyse the following {language} code.

Identify actual syntax errors only.
Do not invent errors.
If the code is syntactically correct, report that no syntax errors exist.

Code:
{code}
"""

    return prompt


def get_ai_response(client, model, prompt):

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    return response.text


def create_correction_prompt(code, language):

    prompt = f"""
You are an expert {language} programmer.

Review and correct the following code.

Rules:
1. Identify actual syntax errors and runtime bugs.
2. Correct only errors that are genuinely present.
3. Do not invent errors.
4. Preserve the original program's intended logic.
5. Do not make unnecessary changes.
6. If division by zero is possible, handle it safely.
7. Do not claim that correct code contains syntax errors.
8. Return the complete corrected code only.
9. Do not include Markdown code fences or explanations.

Original Code:
{code}
"""

    return prompt


def correct_code(code, language, client, model):

    prompt = create_correction_prompt(code, language)

    return get_ai_response(client, model, prompt)


def create_improvement_prompt(code, language):

    prompt = f"""
You are an expert programming developer.

Analyse the following {language} code.

Suggest improvements related to:

1. Code readability.
2. Code efficiency.
3. Better programming practices.
4. Code structure.
5. Avoiding unnecessary operations.

Important:
- Preserve the original functionality.
- Do not introduce unnecessary complexity.
- Explain each suggested improvement.
- Provide an improved version of the code.

Original Code:
{code}
"""

    return prompt


def improve_code(code, language, client, model):

    prompt = create_improvement_prompt(code, language)

    return get_ai_response(client, model, prompt)


def compare_code(original_code, corrected_code):

    comparison = difflib.unified_diff(
        original_code.splitlines(),
        corrected_code.splitlines(),
        fromfile="Original Code",
        tofile="Corrected Code",
        lineterm=""
    )

    return "\n".join(comparison)


def create_security_prompt(code, language):

    prompt = f"""
You are an expert cybersecurity code reviewer.

Analyse the following {language} code
for potential security vulnerabilities.

Check for:

1. Unsafe input handling.
2. Buffer overflow risks where applicable.
3. SQL injection vulnerabilities where applicable.
4. Hardcoded passwords or API keys.
5. Insecure file handling.
6. Weak authentication practices.
7. Unsafe memory handling where applicable.

For each vulnerability:
- Identify the issue.
- Mention the affected line if possible.
- Explain the security risk.
- Suggest a secure solution.

Do not report vulnerabilities without evidence.
If no vulnerabilities are identified, say so.
Mention any limitations in the analysis.

Code:
{code}
"""

    return prompt


def security_analysis(code, language, client, model):

    prompt = create_security_prompt(code, language)

    return get_ai_response(client, model, prompt)
