import os

def detect_language(filename):
    extension = os.path.splitext(filename)[1].lower()

    languages = {
        ".c": "C",
        ".cpp": "C++",
        ".java": "Java",
        ".py": "Python"
    }

    return languages.get(extension, "Unknown")