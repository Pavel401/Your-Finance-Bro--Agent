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
    chat_history: Optional[List[ChatMessage]] = []


class AgentResponse(BaseModel):
    """Response model for the agent endpoint."""

    response_text: str
