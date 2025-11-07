from pydantic_ai import Agent, RunContext, UserPromptPart
from pydantic_ai.messages import ModelRequest, ModelResponse
from typing import List, AsyncIterator

from app.configs.model_config import LLMModelName
from app.services.finance_service import flatten_finance_info
from app.services.llm_service import get_llm_model_config
from app.model.finance_model import FinanceInfo, ChatMessage


def convert_chat_history_to_messages(chat_history: List[ChatMessage]) -> list:
    """
    Convert chat history to PydanticAI message format.

    Args:
        chat_history: List of ChatMessage objects

    Returns:
        List of ModelMessage objects for PydanticAI
    """
    messages = []
    for msg in chat_history:
        if msg.role == "user":
            messages.append(ModelRequest(parts=[UserPromptPart(content=msg.content)]))
        elif msg.role == "assistant":
            messages.append(ModelResponse(parts=[msg.content]))
        elif msg.role == "system":
            messages.append(ModelRequest(parts=[msg.content]))
    return messages
