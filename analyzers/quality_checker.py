def check_code_quality(code):

    issues = []

    lines = code.split("\n")

    if not code.strip():
        issues.append("Code is empty.")

    for line_number, line in enumerate(lines, start=1):

        if len(line) > 100:
            issues.append(
                f"Line {line_number} is too long."
            )

        if line.rstrip() != line:
            issues.append(
                f"Line {line_number} has trailing whitespace."
            )

    return {
        "quality_issues": issues,
        "total_issues": len(issues)
    }