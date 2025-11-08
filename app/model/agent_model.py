from typing import List, Optional
from pydantic import BaseModel

from app.model.finance_model import FinanceInfo


class ChatMessage(BaseModel):
    """Represents a single message in the chat conversation."""

    role: str
    content: str


class AgentRequest(BaseModel):
    """Request model for the agent endpoint."""

    user_query: str
    finance_info: FinanceInfo
    # Avoid mutable default list which can leak state across requests
    chat_history: Optional[List[ChatMessage]] = None


class AgentResponse(BaseModel):
    """Response model for the agent endpoint."""

    response_text: str
