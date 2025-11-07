from pydantic import ValidationError
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelRequest, ModelResponse
from typing import List, AsyncIterator

from app.configs.model_config import LLMModelName
from app.model.agent_model import AgentResponse, ChatMessage
from app.model.finance_model import FinanceInfo
from app.services.finance_service import flatten_finance_info
from app.services.llm_service import get_llm_model_config
from app.services.utility_service import convert_chat_history_to_messages


class FinanceDeps:
    """Dependencies for the finance agent containing user's financial context."""

    def __init__(self, finance_context: str):
        self.finance_context = finance_context


_finance_agent = None


def get_finance_agent() -> Agent:
    """
    Get or create the finance agent instance (lazy initialization).

    Returns:
        Configured finance Agent instance
    """
    global _finance_agent
    if _finance_agent is None:
        _finance_agent = Agent(
            output_type=AgentResponse,
            model=get_llm_model_config(LLMModelName.GPT_4O_MINI),
            deps_type=FinanceDeps,
            system_prompt=(
                "You are a helpful financial assistant. You have access to the user's financial information "
                "including transactions, accounts, and budgets. Use this information to answer their questions "
                "accurately and provide insightful financial advice. Always be clear, concise, and helpful."
            ),
        )

        @_finance_agent.system_prompt
        def finance_system_prompt(ctx: RunContext[FinanceDeps]) -> str:
            """Dynamic system prompt that includes the user's finance information."""
            return (
                f"Here is the user's financial information:\n\n{ctx.deps.finance_context}\n\n"
                "Use this information to answer the user's questions about their finances."
            )

    return _finance_agent


async def process_agent_output(
    user_query: str, finance_info: FinanceInfo, chat_history: List[ChatMessage]
) -> AsyncIterator[str]:
    """
    Process the agent output with user query, finance info, and chat history.
    Streams validated JSON response objects back to the client.

    Args:
        user_query: The user's question
        finance_info: The user's financial information
        chat_history: Previous conversation history

    Yields:
        Newline-delimited JSON strings containing validated AgentResponse objects
    """
    # Flatten finance info into readable text context
    finance_context = flatten_finance_info(finance_info)

    # Create dependencies with financial context
    deps = FinanceDeps(finance_context=finance_context)

    # Convert chat history to PydanticAI message format
    message_history = convert_chat_history_to_messages(chat_history)

    # Get the finance agent instance (lazy initialization)
    agent = get_finance_agent()

    # Stream the agent's response
    async with agent.run_stream(
        user_query,
        deps=deps,
        message_history=message_history,
    ) as result:
        async for message, last in result.stream_responses(debounce_by=0.01):
            try:
                profile = await result.validate_response_output(
                    message,
                    allow_partial=not last,
                )
                # Convert validated response to JSON and yield for the frontend
                if profile:
                    # Convert Pydantic model to JSON string with newline delimiter
                    yield profile.model_dump_json() + "\n"
            except ValidationError:
                continue
