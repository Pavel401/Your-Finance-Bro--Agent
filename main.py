from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

from app.endpoint.agent import router

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Your Finance Bro API",
    description="AI-powered financial assistant API",
    version="0.1.0",
)

# Configure CORS for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include agent router
app.include_router(router=router, prefix="/agent", tags=["Agent"])


@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Your Finance Bro API is running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
