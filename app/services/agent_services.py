import logfire
from pydantic import ValidationError
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelRequest, ModelResponse, SystemPromptPart
from typing import List, AsyncIterator, Optional
from threading import Lock

from app.configs.model_config import LLMModelName
from app.model.agent_model import AgentResponse, ChatMessage
from app.model.finance_model import FinanceInfo
from app.services.finance_service import flatten_finance_info
from app.services.llm_service import get_llm_model_config
from app.services.utility_service import (
    convert_chat_history_to_messages,
)

from app.configs.prompt import base_prompt

# configure logfire
logfire.configure(token="pylf_v1_us_L1PBl6ddHRBrDvk9wst2F1jzKMYsjSwgpwVw0YPmvqWd")
logfire.instrument_pydantic_ai()


class FinanceDeps:
    """Dependencies for the finance agent containing user's financial context."""

    def __init__(self, finance_context: str):
        self.finance_context = finance_context


class FinanceAgentService:
    """
    Singleton service for managing the Finance Agent.
    Ensures a single agent instance is created and reused across all requests.
    """

    _instance: Optional["FinanceAgentService"] = None
    _lock: Lock = Lock()
    _agent: Optional[Agent] = None

    def __new__(cls):
        """
        Singleton pattern implementation using thread-safe double-checked locking.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the singleton instance.
        Note: __init__ is called every time the singleton is accessed,
        but we only want to initialize the agent once.
        """
        # Only initialize if agent hasn't been created yet
        if self._agent is None:
            with self._lock:
                if self._agent is None:
                    self._initialize_agent()

    def _initialize_agent(self) -> None:
        """
        Private method to initialize the agent with configuration and system prompt.
        This is called only once during the first instantiation.
        """
        self._agent = Agent(
            model=get_llm_model_config(LLMModelName.GPT_4O_MINI),
            output_type=AgentResponse,
        )

        # Register system prompt after agent creation
        @self._agent.system_prompt
        def finance_system_prompt(ctx: RunContext[FinanceDeps]) -> str:
            """Dynamic system prompt that includes the user's finance information."""
            return FinanceAgentService._build_finance_system_prompt(
                ctx.deps.finance_context
            )

    @staticmethod
    def _build_finance_system_prompt(finance_context: str) -> str:
        """Construct the full system prompt text including the finance context."""
        return (
            base_prompt
            + f"Here is the user's financial information:\n\n{finance_context}\n\n"
            "Use this information to answer the user's questions about their finances."
        )

    @staticmethod
    def get_agent() -> Agent:
        """
        Static method to get the singleton agent instance.

        Returns:
            Agent: The configured finance agent instance
        """
        instance = FinanceAgentService()
        return instance._agent

    @staticmethod
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

        # Convert chat history to PydanticAI message format
        message_history = convert_chat_history_to_messages(chat_history)

        system_text = FinanceAgentService._build_finance_system_prompt(finance_context)
        priming_request = ModelRequest(parts=[SystemPromptPart(content=system_text)])
        message_history = [priming_request, *message_history]

        # Get the finance agent instance (singleton)
        agent = FinanceAgentService.get_agent()

        # Stream the agent's response
        async with agent.run_stream(
            user_query,
            deps=FinanceDeps(finance_context=finance_context),
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


# Convenience function for backward compatibility
def get_agent() -> Agent:
    """
    Get the singleton finance agent instance.

    Returns:
        Agent: The configured finance agent instance
    """
    return FinanceAgentService.get_agent()


# Convenience function for backward compatibility
async def process_agent_output(
    user_query: str, finance_info: FinanceInfo, chat_history: List[ChatMessage]
) -> AsyncIterator[str]:
    """
    Process the agent output with user query, finance info, and chat history.

    This is a convenience wrapper around FinanceAgentService.process_agent_output()
    for backward compatibility.

    Args:
        user_query: The user's question
        finance_info: The user's financial information
        chat_history: Previous conversation history

    Yields:
        Newline-delimited JSON strings containing validated AgentResponse objects
    """
    async for response in FinanceAgentService.process_agent_output(
        user_query, finance_info, chat_history
    ):
        yield response
