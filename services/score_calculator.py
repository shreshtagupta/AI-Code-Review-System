
def calculate_score(security_result, quality_result, syntax_result=None, ai_result=None):

    score = 100

    # Deduct points for security issues
    security_issues = security_result.get("total_issues", 0)
    score -= security_issues * 10

    # Deduct points for code quality issues
    quality_issues = quality_result.get("total_issues", 0)
    score -= quality_issues * 5

    # Deduct points for syntax errors
    if syntax_result is not None and not syntax_result.get("valid", True):
        score -= 20

    # Deduct points for AI-detected bugs
    if ai_result is not None:

        bugs = ai_result.get("bugs", [])
        logical_errors = ai_result.get("logical_errors", [])

        bug_count = len(bugs) if isinstance(bugs, list) else 0
        logical_count = len(logical_errors) if isinstance(logical_errors, list) else 0

        # Avoid double-counting overlapping AI findings
        unique_ai_issues = max(bug_count, logical_count)

        score -= unique_ai_issues * 10

    # Keep score between 0 and 100
    score = max(0, min(100, score))

    # Assign rating
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
