from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.model.finance_model import AgentRequest
from app.services.agent_services import process_agent_output


router = APIRouter()


@router.post("/chat")
async def chat(request: AgentRequest):
    """
    Chat endpoint that processes user queries with financial context.

    Streams the agent's response back to the client in real-time.

    Args:
        request: AgentRequest containing user_query, finance_info, and chat_history

    Returns:
        StreamingResponse with the agent's response
    """
    # Validate user query
    if not request.user_query or not request.user_query.strip():
        raise HTTPException(status_code=400, detail="User query cannot be empty")

    # Validate finance info
    if not request.finance_info:
        raise HTTPException(status_code=400, detail="Finance info is required")

    # Initialize chat history if not provided
    chat_history = request.chat_history if request.chat_history else []

    try:
        # Process the request and stream the response
        return StreamingResponse(
            process_agent_output(
                user_query=request.user_query,
                finance_info=request.finance_info,
                chat_history=chat_history,
            ),
            media_type="text/plain",
        )
    except Exception as e:
        # Log the error (in production, use proper logging)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}",
        )
