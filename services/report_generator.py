def generate_report(analysis_result):

    syntax = analysis_result["syntax_analysis"]
    security = analysis_result["security_analysis"]
    quality = analysis_result["quality_analysis"]
    score = analysis_result["score_analysis"]
    ai = analysis_result["ai_analysis"]

    report = {

        "FILE DETAILS": {
            "Filename": analysis_result["filename"],
            "Language": analysis_result["language"]
        },

        "OVERALL RESULT": {
            "Score": f'{score["score"]}/100',
            "Rating": score["rating"]
        },

        "SYNTAX ANALYSIS": {
            "Status": (
                "Passed" if syntax and syntax["valid"]
                else "Not Checked" if syntax is None
                else "Failed"
            ),
            "Message": syntax["message"] if syntax else "Not available"
        },

        "SECURITY ANALYSIS": {
            "Total Issues": security["total_issues"],
            "Findings": security["security_issues"]
        },

        "CODE QUALITY": {
            "Total Issues": quality["total_issues"],
            "Findings": quality["quality_issues"]
        },

        "AI ANALYSIS": {
            "Status": ai.get("status", "Completed"),
            "Error Message": ai.get("error_message", None),
            "Detected Language": ai["detected_language"],
            "Syntax Analysis": ai["syntax_analysis"],
            "Bugs": ai["bugs"],
            "Logical Errors": ai["logical_errors"],
            "Security Issues": ai["security_issues"],
            "Code Explanation": ai["code_explanation"],
            "Suggestions": ai["suggestions"],
            "Corrected Code": ai["corrected_code"]
        }
    }

    return report