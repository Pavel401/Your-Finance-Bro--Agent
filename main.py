from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import uvicorn
import os
from pathlib import Path

from app.endpoint.agent import router

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Your Finance Bro API",
    description="AI-powered financial assistant API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router, prefix="/agent", tags=["Agent"])

frontend_path = Path(__file__).parent / "frontend"

app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/", tags=["Frontend"])
async def serve_frontend():
    """Serve the frontend HTML file."""
    return FileResponse(frontend_path / "index.html")


@app.get("/config", tags=["Config"])
async def get_config():
    """Get frontend configuration."""
    backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    if not backend_url.startswith(("http://", "https://")):
        backend_url = f"https://{backend_url}"
    return {"apiBaseUrl": backend_url}


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Your Finance Bro API is running"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
