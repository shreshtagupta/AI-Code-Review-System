from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
import os

from services.code_processor import process_code
from services.report_generator import generate_report

router = APIRouter()


class CodeRequest(BaseModel):
    filename: str
    code: str


# EXISTING FUNCTION
@router.post("/review")
def review_code(request: CodeRequest):

    if not request.code.strip():
        raise HTTPException(
            status_code=400,
            detail="Code cannot be empty."
        )

    result = process_code(request.code, request.filename)
    report = generate_report(result)

    return {
        "message": "Code review completed successfully",
        "report": report
    }


# NEW FUNCTION — ADD BELOW THE EXISTING ONE
@router.post("/review-file")
async def review_file(file: UploadFile = File(...)):

    filename = file.filename

    allowed_extensions = [".py", ".c", ".cpp", ".java"]
    extension = os.path.splitext(filename)[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type."
        )

    content = await file.read()

    try:
        code = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must contain valid UTF-8 text."
        )

    if not code.strip():
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    result = process_code(code, filename)
    report = generate_report(result)

    return {
        "message": "File reviewed successfully",
        "report": report
    }