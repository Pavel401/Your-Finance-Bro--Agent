from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from pydantic_ai import Agent
from pydantic_ai.ui.vercel_ai import VercelAIAdapter
import uvicorn

from app.endpoint.agent import router


app = FastAPI()


app.include_router(router=router, prefix="/agent")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
