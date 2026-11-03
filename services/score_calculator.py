def calculate_score(security_result, quality_result, syntax_result=None, ai_result=None):

    score = 100

    # Deduct points for security issues
    security_issues = security_result["total_issues"]
    score -= security_issues * 10

    # Deduct points for code quality issues
    quality_issues = quality_result["total_issues"]
    score -= quality_issues * 5

    # Deduct points for syntax errors
    if syntax_result is not None and not syntax_result["valid"]:
        score -= 20

    # Deduct points for AI-detected bugs
    if ai_result is not None:
        bugs = ai_result.get("bugs", [])
        logical_errors = ai_result.get("logical_errors", [])

        score -= (len(bugs) + len(logical_errors)) * 10

    # Prevent score from going below zero
    score = max(0, score)

    if score >= 90:
        rating = "Excellent"
    elif score >= 70:
        rating = "Good"
    else:
        rating = "Needs Improvement"

    return {
        "score": score,
        "rating": rating
    }