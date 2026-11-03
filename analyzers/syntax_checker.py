import ast

def check_python_syntax(code):

    try:
        ast.parse(code)

        return {
            "valid": True,
            "message": "No syntax errors found."
        }

    except SyntaxError as error:

        return {
            "valid": False,
            "message": error.msg,
            "line": error.lineno,
            "column": error.offset
        }