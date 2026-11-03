import re

def check_security(code):

    issues = []

    security_patterns = {
        "Use of eval()": r"\beval\s*\(",
        "Use of exec()": r"\bexec\s*\(",
        "Hardcoded password": r"password\s*=\s*['\"].+?['\"]",
        "Hardcoded API key": r"api_key\s*=\s*['\"].+?['\"]"
    }

    for issue, pattern in security_patterns.items():

        if re.search(pattern, code, re.IGNORECASE):
            issues.append(issue)

    return {
        "security_issues": issues,
        "total_issues": len(issues)
    }