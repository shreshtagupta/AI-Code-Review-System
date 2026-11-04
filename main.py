
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.review_routes import router as review_router

app = FastAPI(title="AI Code Reviewer")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(review_router)


@app.get("/")
def home():
    return {
        "message": "AI Code Reviewer backend is running!"
    }
