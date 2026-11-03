from fastapi import FastAPI
from routes.review_routes import router as review_router

app = FastAPI(title="AI Code Reviewer")

app.include_router(review_router)


@app.get("/")
def home():
    return {
        "message": "AI Code Reviewer backend is running!"
    }