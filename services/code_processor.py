
from analyzers.language_detector import detect_language
from analyzers.syntax_checker import check_python_syntax
from analyzers.security_checker import check_security
from analyzers.quality_checker import check_code_quality

from services.score_calculator import calculate_score
from ai.ai_analyzer import analyze_code


def process_code(code, filename):

    # Detect language using filename
    language = detect_language(filename)

    # Security analysis
    security_result = check_security(code)

    # Code quality analysis
    quality_result = check_code_quality(code)

    # AI analysis with error handling
    try:

        ai_result = analyze_code(code, filename)

        if not isinstance(ai_result, dict):
            raise ValueError("Invalid AI response format")

    except Exception as error:

        ai_result = {
            "status": "Failed",
            "detected_language": "Unavailable",
            "syntax_analysis": {
                "status": "Not Checked",
                "errors": []
            },
            "bugs": [],
            "logical_errors": [],
            "security_issues": [],
            "code_explanation": "AI analysis is temporarily unavailable.",
            "suggestions": [],
            "corrected_code": None,
            "error_message": str(error)
        }

    # Use AI-detected language if filename detection fails
    if language == "Unknown":

        detected_language = ai_result.get("detected_language")

        if detected_language and detected_language != "Unavailable":
            language = detected_language

    # Local syntax analysis
    syntax_result = None

    if language.lower() == "python":
        syntax_result = check_python_syntax(code)

    # Use local syntax result as the source of truth
    if syntax_result is not None:

        ai_result["syntax_analysis"] = {
            "status": "Passed" if syntax_result["valid"] else "Failed",
            "errors": [] if syntax_result["valid"] else [
                syntax_result["message"]
            ]
        }

    # Calculate overall score
    score_result = calculate_score(
        security_result,
        quality_result,
        syntax_result,
        ai_result
    )

    # Return complete report
    return {
        "filename": filename,
        "language": language,
        "syntax_analysis": syntax_result,
        "security_analysis": security_result,
        "quality_analysis": quality_result,
        "score_analysis": score_result,
        "ai_analysis": ai_result
    }
